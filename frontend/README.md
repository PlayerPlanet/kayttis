# frontend — Cloudflare Pages

Served at **https://kayttis.kiirikki.fi**, everything behind a demo-user login.

| path | served by |
|---|---|
| `/` | redirect to `/app/` (`public/_redirects`) |
| `/app/*` | static UI in `public/app/` (placeholder until a framework is picked; if it is a bundler such as Vite, set its base to `/app/` and point `pages_build_output_dir` at the build output) |
| `/api/*` | `functions/api/[[path]].js` proxies to `https://kayttis-api.kiirikki.fi/api/*`, the Pi service through Cloudflare Tunnel |
| all | `functions/_middleware.js`: HTTP Basic login with `DEMO_USER` / `DEMO_PASSWORD` |

The proxy keeps the `/api` prefix, so the Pi service serves its routes under `/api/...`.

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
