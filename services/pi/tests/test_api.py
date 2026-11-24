import pytest
from fastapi.testclient import TestClient
from kayttis_core import Observation
from kayttis_pi.api import create_app
from kayttis_pi.config import parse_config

CFG = {
    "mqtt": {"enabled": False},
    "reader": {"enabled": False},
    "devices": [
        {
            "id": "left",
            "name": "Vasen",
            "kind": "coffee_machine",
            "source": "mqtt",
            "topic": "vasen",
            "interpreter": "power_levels",
        },
    ],
}


def test_endpoints():
    app = create_app(parse_config(CFG))
    with TestClient(app) as c:
        h = c.get("/api/health").json()
        assert h["ok"] and "tap_knob" in h["plugins"]["classifiers"]
        assert c.get("/api/devices").json()[0]["state"] == "unknown"
        app.state.hub.update("left", Observation(state="on", value=60, unit="W"))
        d = c.get("/api/devices/left").json()
        assert d["state"] == "on" and d["value"] == 60 and d["stale"] is False
        assert c.get("/api/devices/nope").status_code == 404


def test_deployed_configs_parse():
    from pathlib import Path

    from kayttis_pi.config import load_config

    here = Path(__file__).resolve().parents[1]
    for name in ("config.toml", "config.dev.toml"):
        assert load_config(here / name).devices


def test_bad_config_rejected():
    with pytest.raises(ValueError):
        parse_config({"devices": [{"id": "x", "name": "x", "kind": "x", "source": "frame"}]})
