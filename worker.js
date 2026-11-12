export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1. Enforce primary domain canonicalization (www -> apex)
    if (url.hostname === "www.eggstock.xyz") {
      return Response.redirect(`https://eggstock.xyz${url.pathname}${url.search}`, 301);
    }

    // 2. Trailing slash normalization (eliminate duplicate URLs & canonical issues)
    if (url.pathname.length > 1 && url.pathname.endsWith("/")) {
      const cleanPath = url.pathname.replace(/\/+$/, "");
      return Response.redirect(`https://eggstock.xyz${cleanPath}${url.search}`, 301);
    }

    // 3. 301 Permanent Redirects for legacy and alias routes
    const legacyRedirects = {
      "/prediction": "/predictions",
      "/scripts": "/script",
      "/tierlist": "/tier-list",
      "/tier_list": "/tier-list",
      "/servers": "/",
      "/feed": "/stock",
      "/halloween": "/event",
      "/guides": "/blog"
    };

    if (legacyRedirects[url.pathname]) {
      return Response.redirect(`https://eggstock.xyz${legacyRedirects[url.pathname]}${url.search}`, 301);
    }

    // 4. Handle OAuth callback from Monetag
    if (url.pathname === "/oauth/callback") {
      const code = url.searchParams.get("code");
      const error = url.searchParams.get("error");
      if (error) {
        return new Response(`<h1>OAuth Error: ${error}</h1>`, {
          status: 400,
          headers: { "Content-Type": "text/html" }
        });
      }
      if (!code) {
        return new Response(`<h1>Missing authorization code</h1>`, {
          status: 400,
          headers: { "Content-Type": "text/html" }
        });
      }

      // Automatically exchange authorization code for access token via PKCE
      const tokenUrl = "https://publishers.monetag.com/api/oauth2/token";
      const verifier = "EggStockMonetagMcpVerifierSecureKey20261023SafeRandomStr999";
      const clientId = "mcp_dyn_2fe369d9bc20f449bd5ec09ae1bba14b";
      const redirectUri = "https://eggstock.xyz/oauth/callback";

      const tokenParams = new URLSearchParams();
      tokenParams.set("grant_type", "authorization_code");
      tokenParams.set("client_id", clientId);
      tokenParams.set("code", code);
      tokenParams.set("redirect_uri", redirectUri);
      tokenParams.set("code_verifier", verifier);

      try {
        const tokenRes = await fetch(tokenUrl, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: tokenParams.toString()
        });
        const tokenData = await tokenRes.json();
        const tokenVal = tokenData.access_token || JSON.stringify(tokenData);

        const html = `<!DOCTYPE html>
<html>
<head><title>Monetag MCP Authorized</title>
<style>
body { background: #0b0f19; color: #fff; font-family: monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
.card { background: #161f30; padding: 2rem; border-radius: 12px; border: 1px solid #00f0ff; max-width: 600px; width: 90%; }
h1 { color: #00f0ff; margin-top: 0; }
textarea { width: 100%; height: 90px; background: #090d16; color: #00ff66; border: 1px solid #334155; padding: 10px; font-family: monospace; border-radius: 6px; box-sizing: border-box; }
button { background: #00f0ff; color: #000; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 10px; }
</style>
</head>
<body>
<div class="card">
<h1>🎉 Monetag Connected!</h1>
<p>Here is your Monetag MCP Access Token:</p>
<textarea id="tok" readonly>${tokenVal}</textarea>
<br>
<button onclick="navigator.clipboard.writeText(document.getElementById('tok').value); this.innerText='COPIED!';">📋 Copy Token</button>
<p style="color: #94a3b8; font-size: 0.85rem; margin-top: 1rem;">Paste this token back into chat to finish setup!</p>
</div>
</body>
</html>`;

        return new Response(html, {
          status: 200,
          headers: { "Content-Type": "text/html" }
        });
      } catch (e) {
        return new Response(`<h1>Exchange Error: ${e.message}</h1><p>Code: ${code}</p>`, {
          status: 500,
          headers: { "Content-Type": "text/html" }
        });
      }
    }

    // 5. Handle Monetag push service worker
    if (url.pathname === "/sw.js") {
      const swResponse = await env.ASSETS.fetch(request);
      const headers = new Headers(swResponse.headers);
      headers.set("Content-Type", "application/javascript");
      headers.set("Service-Worker-Allowed", "/");
      return new Response(swResponse.body, {
        status: swResponse.status,
        headers: headers
      });
    }

    // 6. Proxy API calls directly to Railway live bot backend with Edge Caching & CORS
    if (url.pathname.startsWith("/api/")) {
      if (request.method === "OPTIONS") {
        return new Response(null, {
          status: 204,
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Accept, Origin, X-Requested-With, X-EggStock-Token",
            "Access-Control-Max-Age": "86400"
          }
        });
      }

      // Check Cloudflare edge cache for GET requests
      const cache = caches.default;
      const cacheKey = new Request(url.toString(), request);

      if (request.method === "GET") {
        try {
          const cached = await cache.match(cacheKey);
          if (cached) {
            return cached;
          }
        } catch (e) {
          // ignore cache read failure
        }
      }

      const backendUrl = "https://eggstock-web-production-3b27.up.railway.app" + url.pathname + url.search;
      const headers = new Headers(request.headers);
      headers.set("Host", "www.eggstock.xyz");
      headers.set("Referer", "https://eggstock.xyz");
      headers.set("Origin", "https://eggstock.xyz");

      try {
        const response = await fetch(backendUrl, {
          method: request.method,
          headers: headers,
          body: request.method !== "GET" && request.method !== "HEAD" ? request.body : undefined
        });

        const newHeaders = new Headers(response.headers);
        newHeaders.set("Access-Control-Allow-Origin", "*");
        newHeaders.set("Cache-Control", "public, max-age=2, s-maxage=5, stale-while-revalidate=10");

        const proxiedResponse = new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: newHeaders
        });

        if (request.method === "GET" && response.status === 200) {
          try {
            await cache.put(cacheKey, proxiedResponse.clone());
          } catch (e) {
            // ignore cache write failure
          }
        }

        return proxiedResponse;
      } catch (err) {
        return new Response(JSON.stringify({ error: "Backend proxy error", details: err.message, status: "degraded" }), {
          status: 502,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      }
    }

    // 7. Clean Canonical Route Mappings
    const staticMap = {
      "/": "/index.html",
      "/stock": "/stock.html",
      "/predictions": "/predictions.html",
      "/notifier": "/notifier.html",
      "/calculator": "/calculator.html",
      "/codes": "/codes.html",
      "/tier-list": "/tier-list.html",
      "/values": "/values.html",
      "/trading": "/trading.html",
      "/event": "/event.html",
      "/script": "/script.html",
      "/faq": "/faq.html",
      "/blog": "/blog.html",
      "/about": "/about.html",
      "/contact": "/contact.html",
      "/terms": "/terms.html",
      "/privacy": "/privacy.html",
      "/soundboard": "/soundboard.html"
    };

    if (staticMap[url.pathname]) {
      return env.ASSETS.fetch(new Request(new URL(staticMap[url.pathname], request.url), request));
    }

    // 8. Blog Post Routes (/blog/:slug)
    if (url.pathname.startsWith("/blog/")) {
      const blogHtmlUrl = new URL(url.pathname + ".html", request.url);
      const blogResponse = await env.ASSETS.fetch(new Request(blogHtmlUrl, request));
      if (blogResponse.status === 200) {
        return blogResponse;
      }
    }

    // 9. Standard Static Asset Fetch (Images, CSS, JS, Favicons)
    let assetResponse = await env.ASSETS.fetch(request);
    if (assetResponse.status === 200) {
      return assetResponse;
    }

    // 10. True 404 Response (NO SOFT 404s — prevents duplicate canonical index penalty in GSC)
    try {
      const notFoundPage = await env.ASSETS.fetch(new Request(new URL("/404.html", request.url), request));
      return new Response(notFoundPage.body, {
        status: 404,
        statusText: "Not Found",
        headers: {
          "Content-Type": "text/html; charset=UTF-8",
          "Cache-Control": "public, max-age=60"
        }
      });
    } catch (e) {
      return new Response("<h1>404 Not Found</h1><p>The requested egg does not exist.</p>", {
        status: 404,
        headers: { "Content-Type": "text/html; charset=UTF-8" }
      });
    }
  },

  // Keep-alive cron: pings Railway backend every 10 minutes to maintain 24/7 uptime
  async scheduled(controller, env, ctx) {
    ctx.waitUntil(
      fetch("https://eggstock-web-production-3b27.up.railway.app/api/status", {
        headers: { "User-Agent": "EggStock-Cloudflare-KeepAlive/1.0" }
      })
        .then(res => console.log(`[KeepAlive] Railway ping status: ${res.status}`))
        .catch(err => console.error(`[KeepAlive] Railway ping failed: ${err.message}`))
    );
  }
};
