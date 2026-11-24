# frontend — Cloudflare Pages

Served at **https://kayttis.kiirikki.fi**, everything behind a demo-user login.

| path | served by |
|---|---|
| `/` | redirect to `/app/` (`public/_redirects`) |
| `/app/*` | static UI in `public/app/` (dependency-free ES modules, no build step): `index.html`, `app.js`, `icons.js`, `app.css` |
| `/api/*` | `functions/api/[[path]].js` proxies to `https://kayttis-api.kiirikki.fi/api/*`, the Pi service through Cloudflare Tunnel |
| all | `functions/_middleware.js`: HTTP Basic login with `DEMO_USER` / `DEMO_PASSWORD` |

The proxy keeps the `/api` prefix, so the Pi service serves its routes under `/api/...`.

## The UI

Smart-home prototype: rooms as collapsible lists, devices sorted on-first then
alphabetically, the icon toggles a device, the row opens the camera view
(`/api/camera/latest.jpg`, refreshed every 3 s), a floating "away" button turns
everything off and a floating "+" adds a device.

**Switching is simulated in the browser** (state in `localStorage`, key `kayttis.home.v1`);
the backend is read-only and never switches real devices. A device can be *connected* to
a backend device id and then shows its live state (`/api/stream`, polling `/api/devices`
as fallback). Without the API the UI works fully and shows "Live data offline".

## Local dev

```sh
cd frontend
cp .dev.vars.example .dev.vars
npx wrangler pages dev
```

## One-time Cloudflare setup

1. `kiirikki.fi` must be a zone on the Cloudflare account.
2. Create the Pages project: `npx wrangler pages project create kayttis --production-branch main`,
   or connect the GitHub repo in the dashboard (root directory `frontend`, no build command).
3. Custom domain: Pages project → Custom domains → `kayttis.kiirikki.fi`.
4. Secrets: `npx wrangler pages secret put DEMO_USER` (and `DEMO_PASSWORD`,
   `ACCESS_CLIENT_ID`, `ACCESS_CLIENT_SECRET`).
5. Lock the tunnel hostname: Zero Trust → Access → Service Auth → create a service token
   (its id/secret are the two ACCESS_* secrets), then an Access application for
   `kayttis-api.kiirikki.fi` with one policy: action **Service Auth**, include that token.
   Without this the Pi API would be public on the tunnel hostname.
6. Tunnel on the Pi: see `deploy/pi/cloudflared/`.

Deploy manually with `npx wrangler pages deploy` from this directory (the Git integration
deploys on every push to `main` instead).
