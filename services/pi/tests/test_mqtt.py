import json

import kayttis_pi.plugins  # noqa: F401
from kayttis_pi.config import DeviceConfig, MqttConfig
from kayttis_pi.hub import StateHub
from kayttis_pi.sources.mqtt import MqttSource


def test_routes_payload_to_devices():
    devs = [
        DeviceConfig(
            id="left",
            name="L",
            kind="coffee_machine",
            source="mqtt",
            topic="vasen",
            interpreter="power_levels",
            params={"levels": {"off": 0, "on": 10, "brewing": 300}},
        ),
        DeviceConfig(
            id="other",
            name="O",
            kind="x",
            source="mqtt",
            topic="custom/topic",
            interpreter="value",
            params={"field": "power"},
        ),
    ]
    hub = StateHub(devs)
    src = MqttSource(MqttConfig(enabled=False), devs, hub)
    assert set(src.routes) == {"zigbee2mqtt/vasen", "custom/topic"}
    src.handle("zigbee2mqtt/vasen", json.dumps({"power": 1400, "state": "ON"}).encode())
    src.handle("zigbee2mqtt/vasen", b"not json")
    src.handle("zigbee2mqtt/unrelated", b"{}")
    assert hub.get("left").state == "brewing"
    assert hub.get("left").value == 1400
    assert hub.get("other").state == "unknown"
