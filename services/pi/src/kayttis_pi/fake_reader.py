"""Stand-in for the kahvi reader service, for development off the Pi.

Serves JPEGs from a directory (cycling, one "tick" every --interval seconds) over the
same line-JSON protocol on loopback TCP:

    uv run kayttis-fake-reader FRAMES_DIR --port 8765
    # then use reader.socket = "tcp:127.0.0.1:8765" in the config
"""

import argparse
import json
import socket
import threading
import time
from pathlib import Path


class FakeReader:
    def __init__(self, frames: list[Path], interval: float = 10.0, lit: bool = True) -> None:
        if not frames:
            raise ValueError("no frames")
        self.frames, self.interval, self.lit = frames, interval, lit
        self.t0 = time.monotonic()

    def _tick(self) -> tuple[int, float]:
        elapsed = time.monotonic() - self.t0
        return int(elapsed // self.interval), elapsed % self.interval

    def respond(self, req: dict) -> tuple[dict, bytes]:
        seq, age = self._tick()
        op = req.get("op")
        if op == "ping":
            return {"ok": True, "seq": seq, "last_lit_age": age if self.lit else None}, b""
        if op == "frame":
            path = self.frames[seq % len(self.frames)]
            pots = [{"side": "left", "ml": 420.0, "tier": "ok"}]
            return {
                "ok": True,
                "age": age,
                "reused": True,
                "seq": seq,
                "pots": pots,
                "frame": path.name,
            }, path.read_bytes()
        return {"ok": False, "error": "unknown op"}, b""

    def serve(self, host: str = "127.0.0.1", port: int = 8765) -> socket.socket:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen(8)

        def handle(conn: socket.socket) -> None:
            with conn:
                buf = b""
                while b"\n" not in buf:
                    chunk = conn.recv(4096)
                    if not chunk:
                        return
                    buf += chunk
                hdr, body = self.respond(json.loads(buf.partition(b"\n")[0]))
                hdr["bytes"] = len(body)
                conn.sendall(json.dumps(hdr).encode() + b"\n" + body)

        def loop() -> None:
            while True:
                try:
                    conn, _ = srv.accept()
                except OSError:
                    return
                threading.Thread(target=handle, args=(conn,), daemon=True).start()

        threading.Thread(target=loop, daemon=True, name="fake-reader").start()
        return srv


def main() -> None:
    ap = argparse.ArgumentParser(prog="kayttis-fake-reader")
    ap.add_argument("frames", type=Path, help="directory of .jpg frames, served in name order")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--interval", type=float, default=10.0)
    ap.add_argument("--dark", action="store_true", help="pretend the lights are off")
    a = ap.parse_args()
    frames = sorted(a.frames.glob("*.jpg"))
    FakeReader(frames, a.interval, lit=not a.dark).serve(port=a.port)
    print(f"fake reader: {len(frames)} frames on tcp:127.0.0.1:{a.port}, Ctrl+C to stop")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass
