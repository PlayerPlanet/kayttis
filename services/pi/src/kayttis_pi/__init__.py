"""Raspberry Pi service for the käyttis smart-home prototype."""

import argparse
import logging
import os


def main() -> None:
    import uvicorn

    from .api import create_app
    from .config import load_config

    ap = argparse.ArgumentParser(prog="kayttis-pi")
    ap.add_argument(
        "--config",
        default=os.environ.get("KAYTTIS_CONFIG", "services/pi/config.toml"),
        help="TOML config (default: $KAYTTIS_CONFIG or services/pi/config.toml)",
    )
    args = ap.parse_args()

    cfg = load_config(args.config)
    logging.basicConfig(
        level=cfg.server.log_level.upper(), format="%(levelname)s %(name)s: %(message)s"
    )
    uvicorn.run(
        create_app(cfg),
        host=cfg.server.host,
        port=cfg.server.port,
        log_level=cfg.server.log_level,
        proxy_headers=True,
    )
