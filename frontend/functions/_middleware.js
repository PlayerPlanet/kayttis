// Demo-user login for the logged-in demo (/app and /api) via HTTP Basic auth.
// Everything else (the public landing page, /brand, /media, /site) passes through.
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

// "/app", "/app/...", "/api", "/api/..." (but not e.g. "/apple" or "/apix").
// The pathname is matched case-insensitively and after URL normalisation,
// so "/APP" or "/%61pp" cannot slip past.
function isProtected(pathname) {
  let path = pathname;
  try {
    path = decodeURIComponent(pathname);
  } catch {
    return true; // malformed escape: fail closed
  }
  path = path.toLowerCase().replace(/\/{2,}/g, "/");
  return /^\/(app|api)(\/|\.|$)/.test(path);
}

export async function onRequest({ request, env, next }) {
  const { pathname } = new URL(request.url);
  if (!isProtected(pathname)) {
    return next();
  }
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
