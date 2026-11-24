# käyttis — kahvibot smart-home prototype

Prototype for the käyttis course: the kahvibot Raspberry Pi shows smart-home state
(are the coffee machines on? is the dishwasher tap open? are the lights on?).
A small service runs on the Pi and its API is consumed by a frontend page.

Current demo: https://k-yttis-demo-backend.vercel.app/

## Layout

```
pyproject.toml          uv workspace root (shared dev tooling: ruff, pytest)
packages/core/          kayttis-core — shared models/helpers
services/pi/            kayttis-pi   — service deployed to the Raspberry Pi
deploy/pi/              systemd unit + rsync deploy script for the Pi
frontend/               frontend page (not yet started)
```

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv sync --all-packages      # create .venv with every workspace member + dev tools
uv run kayttis-pi           # run the Pi service locally
uv run ruff check . && uv run ruff format .
uv run pytest
```

Add a dependency to one member: `uv add --package kayttis-pi <dep>`.

## Deploying to the Pi

One-time on the Pi: install uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`),
copy `.env.example` to `.env`, install `deploy/pi/kayttis-pi.service` into systemd.

Then from your machine:

```sh
PI_HOST=pi@kahvibot.local ./deploy/pi/deploy.sh
```

The Pi supports Python >= 3.11 (Raspberry Pi OS Bookworm default); uv will fetch
a newer interpreter if `.python-version` asks for one.
