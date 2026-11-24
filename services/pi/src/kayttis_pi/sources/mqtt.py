"""MQTT source: subscribes to the zigbee2mqtt broker already running on the Pi.

Read-only by design: this module never publishes. (Publishing to ``zigbee2mqtt/<dev>/set``
would switch the coffee machines' plugs.)
"""

import json
import logging
from collections import defaultdict
from typing import Any

from kayttis_core import Interpreter, build_interpreter

from ..config import DeviceConfig, MqttConfig
from ..hub import StateHub

log = logging.getLogger(__name__)


class MqttSource:
    def __init__(self, cfg: MqttConfig, devices: list[DeviceConfig], hub: StateHub) -> None:
        self.cfg = cfg
        self.hub = hub
        self.routes: dict[str, list[tuple[str, Interpreter]]] = defaultdict(list)
        for d in devices:
            if d.source == "mqtt":
                topic = d.topic if "/" in d.topic else f"{cfg.base_topic}/{d.topic}"
                self.routes[topic].append((d.id, build_interpreter(d.interpreter, d.params)))
        self.connected = False
        self.messages = 0
        self._client: Any = None

    def handle(self, topic: str, raw: bytes) -> None:
        """Route one message to its devices. Separate from paho so tests can call it."""
        routes = self.routes.get(topic)
        if not routes:
            return
        try:
            payload = json.loads(raw)
        except ValueError:
            return
        if not isinstance(payload, dict):
            return
        self.messages += 1
        for device_id, interpret in routes:
            try:
                self.hub.update(device_id, interpret(payload))
            except Exception:  # noqa: BLE001 - a bad payload must not kill paho's thread
                log.warning("interpreter failed for %s on %s", device_id, topic, exc_info=True)

    def start(self) -> None:
        if not self.cfg.enabled or not self.routes:
            log.info(
                "mqtt source disabled (enabled=%s, %d topics)", self.cfg.enabled, len(self.routes)
            )
            return
        import paho.mqtt.client as mqtt

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="kayttis-pi")
        if self.cfg.user:
            client.username_pw_set(self.cfg.user, self.cfg.password())

        def on_connect(c, _userdata, _flags, reason_code, _props=None):
            self.connected = not reason_code.is_failure
            if self.connected:
                for topic in self.routes:
                    c.subscribe(topic)
                log.info("mqtt connected, subscribed to %s", ", ".join(sorted(self.routes)))
            else:
                log.warning("mqtt connect refused: %s", reason_code)

        def on_disconnect(_c, _userdata, *_args, **_kw):
            self.connected = False

        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = lambda _c, _u, msg: self.handle(msg.topic, msg.payload)
        client.reconnect_delay_set(min_delay=1, max_delay=60)
        client.connect_async(self.cfg.host, self.cfg.port, keepalive=60)
        client.loop_start()  # paho reconnects on its own
        self._client = client

    def stop(self) -> None:
        if self._client is not None:
            self._client.disconnect()
            self._client.loop_stop()
            self._client = None

    def status(self) -> dict[str, Any]:
        return {
            "enabled": bool(self.cfg.enabled and self.routes),
            "connected": self.connected,
            "topics": sorted(self.routes),
            "messages": self.messages,
        }
