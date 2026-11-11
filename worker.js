export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Handle OAuth callback from Monetag
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

    // Handle Monetag push service worker
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

    // Proxy API calls directly to Railway live bot backend with Edge Caching & CORS
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

      // Check Cloudflare edge cache for GET requests (prevents worker subrequest exhaustion)
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
        // Edge cache for 5s; stale-while-revalidate for 10s
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
        return new Response(JSON.stringify({ error: "Backend proxy error", details: err.message }), {
          status: 502,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
        });
      }
    }

    // Clean URL mappings for canonical pages & sitemap entries
    const cleanPath = url.pathname.replace(/\/$/, "");

    if (cleanPath === "/notifier") {
      return env.ASSETS.fetch(new Request(new URL("/notifier.html", request.url), request));
    }
    if (cleanPath === "/calculator") {
      return env.ASSETS.fetch(new Request(new URL("/calculator.html", request.url), request));
    }
    if (cleanPath === "/stock") {
      return env.ASSETS.fetch(new Request(new URL("/stock.html", request.url), request));
    }
    if (cleanPath === "/predictions") {
      return env.ASSETS.fetch(new Request(new URL("/predictions.html", request.url), request));
    }
    if (cleanPath === "/script" || cleanPath === "/scripts") {
      return env.ASSETS.fetch(new Request(new URL("/script/index.html", request.url), request));
    }
    if (cleanPath === "/tier-list" || cleanPath === "/tierlist" || cleanPath === "/tier_list") {
      return env.ASSETS.fetch(new Request(new URL("/tier_list.html", request.url), request));
    }
    if (cleanPath === "/codes") {
      return env.ASSETS.fetch(new Request(new URL("/codes.html", request.url), request));
    }
    if (cleanPath === "/event") {
      return env.ASSETS.fetch(new Request(new URL("/event.html", request.url), request));
    }
    if (cleanPath === "/values" || cleanPath === "/trading") {
      return env.ASSETS.fetch(new Request(new URL("/tier_list.html", request.url), request));
    }

    // Serve static assets from ./website with automatic .html and SPA 404 fallback (prevents origin 429s)
    let assetResponse = await env.ASSETS.fetch(request);
    if (assetResponse.status === 404 && !url.pathname.includes(".")) {
      // Try resolving with .html appended
      const htmlUrl = new URL(url.pathname + ".html", request.url);
      const htmlResponse = await env.ASSETS.fetch(new Request(htmlUrl, request));
      if (htmlResponse.status === 200) {
        return htmlResponse;
      }
      // Clean SPA fallback to index.html instead of hitting rate-limited origin
      return env.ASSETS.fetch(new Request(new URL("/index.html", request.url), request));
    }

    return assetResponse;
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
