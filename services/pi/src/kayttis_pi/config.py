"""Service configuration, loaded from a TOML file (see services/pi/config.toml)."""

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SOURCES = ("mqtt", "frame", "reader")
READER_SIGNALS = ("lights", "coffee_level")


@dataclass
class ServerConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    log_level: str = "info"


@dataclass
class MqttConfig:
    enabled: bool = True
    host: str = "127.0.0.1"
    port: int = 1883
    user: str = ""
    password_file: str = ""
    base_topic: str = "zigbee2mqtt"

    def password(self) -> str:
        if not self.password_file:
            return ""
        return Path(self.password_file).read_text(encoding="utf-8").strip()


@dataclass
class ReaderConfig:
    """The kahvi reader service (kahvibot). We only ever talk to its socket, never the camera.

    ``socket`` is an AF_UNIX path, or ``tcp:HOST:PORT`` (Windows dev, fake reader).
    """

    enabled: bool = True
    socket: str = "/run/kahvi-sampler/ipc.sock"
    poll_interval: float = 15.0
    timeout: float = 3.0
    # The reader marks a frame "lit" when the room light is on. No lit frame for this
    # long => lights off. Frames are requested with max_age = dark_after, so a frame is
    # only fetched while a recent lit one exists and the reader never captures for us.
    dark_after: float = 90.0
    # The reader's seq must advance within this window, otherwise it is considered stalled.
    stall_after: float = 300.0


@dataclass
class DeviceConfig:
    id: str
    name: str
    kind: str
    source: str
    stale_after: float = 900.0
    # source = "mqtt"
    topic: str = ""
    interpreter: str = ""
    # source = "frame"
    classifier: str = ""
    smooth_window: int = 1
    # source = "reader"
    signal: str = ""
    side: str = ""
    params: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if self.source not in SOURCES:
            raise ValueError(f"device {self.id}: source must be one of {SOURCES}")
        if self.source == "mqtt" and not (self.topic and self.interpreter):
            raise ValueError(f"device {self.id}: mqtt devices need topic and interpreter")
        if self.source == "frame" and not self.classifier:
            raise ValueError(f"device {self.id}: frame devices need a classifier")
        if self.source == "reader" and self.signal not in READER_SIGNALS:
            raise ValueError(f"device {self.id}: reader signal must be one of {READER_SIGNALS}")
        if self.signal == "coffee_level" and not self.side:
            raise ValueError(f"device {self.id}: coffee_level needs side (left/right)")
        if self.smooth_window < 1:
            raise ValueError(f"device {self.id}: smooth_window must be >= 1")


@dataclass
class Config:
    server: ServerConfig = field(default_factory=ServerConfig)
    mqtt: MqttConfig = field(default_factory=MqttConfig)
    reader: ReaderConfig = field(default_factory=ReaderConfig)
    devices: list[DeviceConfig] = field(default_factory=list)


def load_config(path: str | os.PathLike[str]) -> Config:
    data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    return parse_config(data)


def parse_config(data: dict[str, Any]) -> Config:
    cfg = Config(
        server=ServerConfig(**data.get("server", {})),
        mqtt=MqttConfig(**data.get("mqtt", {})),
        reader=ReaderConfig(**data.get("reader", {})),
        devices=[DeviceConfig(**d) for d in data.get("devices", [])],
    )
    # .env on the Pi (EnvironmentFile) may override where we listen.
    if host := os.environ.get("KAYTTIS_HOST"):
        cfg.server.host = host
    if port := os.environ.get("KAYTTIS_PORT"):
        cfg.server.port = int(port)

    seen: set[str] = set()
    for dev in cfg.devices:
        dev.validate()
        if dev.id in seen:
            raise ValueError(f"duplicate device id {dev.id!r}")
        seen.add(dev.id)
    return cfg
