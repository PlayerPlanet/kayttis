#!/usr/bin/env bash
# Ship the committed tree (HEAD) to the Raspberry Pi and restart the service.
# Works from Git Bash on Windows too (needs only git and ssh, no rsync).
# Usage: PI_HOST=kahvibot ./deploy/pi/deploy.sh        (an ~/.ssh/config host, or konsta@192.168.50.169)
#
# One-time on the Pi: install uv (curl -LsSf https://astral.sh/uv/install.sh | sh) and
#   sudo install -m 644 deploy/pi/kayttis-pi.service /etc/systemd/system/
#   sudo systemctl daemon-reload && sudo systemctl enable --now kayttis-pi
set -euo pipefail

PI_HOST="${PI_HOST:?set PI_HOST, e.g. kahvibot or konsta@192.168.50.169}"
PI_DIR="${PI_DIR:-/home/konsta/kayttis}"

if ! git diff --quiet HEAD -- services packages pyproject.toml uv.lock; then
  echo "warning: uncommitted backend changes are NOT deployed (only HEAD is)" >&2
fi

# Overwrites tracked files only; .env and .venv on the Pi are left alone.
git archive --format=tar HEAD -- services packages deploy pyproject.toml uv.lock .python-version .env.example \
  | ssh "$PI_HOST" "mkdir -p '$PI_DIR' && tar -x -C '$PI_DIR'"

ssh "$PI_HOST" "cd '$PI_DIR' && ([ -f .env ] || cp .env.example .env) \
  && ~/.local/bin/uv sync --frozen --no-dev --package kayttis-pi \
  && sudo systemctl restart kayttis-pi \
  && for i in \$(seq 1 60); do curl -fsS -o /dev/null localhost:8000/api/health && break; sleep 1; done; \
  systemctl is-active kayttis-pi && curl -fsS localhost:8000/api/health && echo"
