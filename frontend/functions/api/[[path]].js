// Same-origin proxy: /api/* on the Pages site -> API_ORIGIN/api/* (the Pi, via the tunnel).
// The tunnel hostname is locked down with Cloudflare Access; only this function holds
// the service token, so the Pi is reachable only through the demo login.

export async function onRequest({ request, env }) {
  if (!env.API_ORIGIN) {
    return Response.json({ ok: false, error: "API_ORIGIN not configured" }, { status: 503 });
  }
  const url = new URL(request.url);
  const target = new URL(url.pathname + url.search, env.API_ORIGIN);

  const headers = new Headers(request.headers);
  for (const h of ["Authorization", "Cookie", "Host"]) headers.delete(h);
  headers.set("CF-Access-Client-Id", env.ACCESS_CLIENT_ID ?? "");
  headers.set("CF-Access-Client-Secret", env.ACCESS_CLIENT_SECRET ?? "");

  try {
    return await fetch(target, {
      method: request.method,
      headers,
      body: request.body,
      redirect: "manual",
    });
  } catch {
    return Response.json({ ok: false, error: "pi unreachable" }, { status: 502 });
  }
}
