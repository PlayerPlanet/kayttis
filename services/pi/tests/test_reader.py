import io
import socket

import kayttis_pi.plugins  # noqa: F401
import numpy as np
from kayttis_pi.config import DeviceConfig, ReaderConfig
from kayttis_pi.fake_reader import FakeReader
from kayttis_pi.hub import StateHub
from kayttis_pi.sources.reader import ReaderSource
from PIL import Image

DEVICES = [
    DeviceConfig(id="lights", name="L", kind="light", source="reader", signal="lights"),
    DeviceConfig(
        id="pot", name="P", kind="coffee_pot", source="reader", signal="coffee_level", side="left"
    ),
    DeviceConfig(
        id="tap",
        name="T",
        kind="valve",
        source="frame",
        classifier="tap_knob",
        params={"min_confidence": 0.0},
    ),
]


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def write_frames(tmp_path, n=2):
    rng = np.random.default_rng(0)
    out = []
    for i in range(n):
        buf = io.BytesIO()
        Image.fromarray(rng.integers(0, 255, (720, 1280, 3), dtype=np.uint8)).save(buf, "JPEG")
        p = tmp_path / f"f{i}.jpg"
        p.write_bytes(buf.getvalue())
        out.append(p)
    return out


def make(tmp_path, lit=True):
    port = free_port()
    srv = FakeReader(write_frames(tmp_path), interval=60, lit=lit).serve(port=port)
    hub = StateHub(DEVICES)
    src = ReaderSource(ReaderConfig(socket=f"tcp:127.0.0.1:{port}"), DEVICES, hub)
    return srv, hub, src


def test_lit_frame_feeds_all_devices(tmp_path):
    srv, hub, src = make(tmp_path)
    try:
        src.poll_once()
        assert src.reachable
        assert hub.get("lights").state == "on"
        assert hub.get("pot").value == 420
        assert src.frames_processed == 1
        src.poll_once()  # same reader seq: not processed again
        assert src.frames_processed == 1
    finally:
        srv.close()


def test_dark_skips_frames(tmp_path):
    srv, hub, src = make(tmp_path, lit=False)
    try:
        src.poll_once()
        assert hub.get("lights").state == "off"
        assert hub.get("pot").state == "unknown"
        assert src.frames_processed == 0
    finally:
        srv.close()


def test_unreachable_reader():
    hub = StateHub(DEVICES)
    cfg = ReaderConfig(socket=f"tcp:127.0.0.1:{free_port()}", timeout=0.5)
    src = ReaderSource(cfg, DEVICES, hub)
    src.poll_once()
    assert not src.reachable and src.last_error
    assert hub.get("lights").state == "unknown"
