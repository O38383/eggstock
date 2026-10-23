export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Proxy API calls directly to Railway live bot backend
    if (url.pathname.startsWith("/api/")) {
      const backendUrl = "https://eggstock-web-production.up.railway.app" + url.pathname + url.search;
      const headers = new Headers(request.headers);
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
        newHeaders.set("Cache-Control", "no-store, no-cache, must-revalidate");

        return new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: newHeaders
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: "Backend proxy error", details: err.message }), {
          status: 502,
          headers: { "Content-Type": "application/json" }
        });
      }
    }

    // Handle /script and /scripts cleanly
    if (url.pathname === "/script" || url.pathname === "/scripts" || url.pathname === "/script/" || url.pathname === "/scripts/") {
      return env.ASSETS.fetch(new Request(new URL("/index.html", request.url), request));
    }

    // Serve all static assets from ./website
    return env.ASSETS.fetch(request);
  }
};
