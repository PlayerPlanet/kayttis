#!/usr/bin/env bash
# Sync the repo to the Raspberry Pi and restart the service.
# Usage: PI_HOST=konsta@kahvibot.local ./deploy/pi/deploy.sh
set -euo pipefail

PI_HOST="${PI_HOST:?set PI_HOST, e.g. konsta@kahvibot.local}"
PI_DIR="${PI_DIR:-/home/konsta/kayttis}"

rsync -az --delete \
  --exclude .git --exclude .venv --exclude __pycache__ --exclude .env \
  --exclude node_modules --exclude frontend \
  ./ "${PI_HOST}:${PI_DIR}/"

ssh "$PI_HOST" "cd '$PI_DIR' && ~/.local/bin/uv sync --frozen --no-dev --package kayttis-pi && sudo systemctl restart kayttis-pi"
