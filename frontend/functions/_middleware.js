// Demo-user login for the whole site (UI and /api) via HTTP Basic auth.
// Credentials come from the DEMO_USER / DEMO_PASSWORD secrets (ASCII only).

const encoder = new TextEncoder();

async function safeEqual(a, b) {
  const x = encoder.encode(a);
  const y = encoder.encode(b);
  if (x.byteLength !== y.byteLength) {
    crypto.subtle.timingSafeEqual(x, x);
    return false;
  }
  return crypto.subtle.timingSafeEqual(x, y);
}

export async function onRequest({ request, env, next }) {
  if (!env.DEMO_USER || !env.DEMO_PASSWORD) {
    return new Response("Login is not configured", { status: 503 });
  }
  const expected = "Basic " + btoa(`${env.DEMO_USER}:${env.DEMO_PASSWORD}`);
  const given = request.headers.get("Authorization") ?? "";
  if (await safeEqual(given, expected)) {
    return next();
  }
  return new Response("Authentication required", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="kayttis", charset="UTF-8"',
      "Cache-Control": "no-store",
    },
  });
}
