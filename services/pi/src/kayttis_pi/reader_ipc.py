"""Client for the kahvi reader service socket (fyysikkokilta/kahvibot reader/pipeline/ipc.py).

Protocol: one JSON request line; the response is one JSON header line followed by
``header["bytes"]`` raw bytes. Requests used here:
  {"op": "ping"}                 -> {ok, seq, last_lit_age}
  {"op": "frame", "max_age": s}  -> {ok, age, reused, seq, pots, captured_at, bytes} + JPEG
A frame younger than max_age is served from the reader's IPC thread without touching
the camera or the model, so polling with a generous max_age costs the reader nothing.
"""

import json
import socket
from typing import Any


def _connect(addr: str, timeout: float) -> socket.socket:
    if addr.startswith("tcp:"):
        host, _, port = addr[4:].rpartition(":")
        s = socket.create_connection((host or "127.0.0.1", int(port)), timeout=timeout)
        return s
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect(addr)
    return s


class ReaderError(Exception):
    pass


class ReaderClient:
    def __init__(self, addr: str, timeout: float = 3.0) -> None:
        self.addr = addr
        self.timeout = timeout

    def call(self, payload: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
        try:
            s = _connect(self.addr, self.timeout)
        except OSError as exc:
            raise ReaderError(f"connect {self.addr}: {exc}") from exc
        try:
            s.sendall(json.dumps(payload).encode() + b"\n")
            buf = b""
            while b"\n" not in buf:
                chunk = s.recv(1 << 16)
                if not chunk:
                    break
                buf += chunk
                if len(buf) > 1 << 20:
                    raise ReaderError("header too long")
            line, _, body = buf.partition(b"\n")
            header = json.loads(line)
            n = int(header.get("bytes", 0))
            while len(body) < n:
                chunk = s.recv(min(1 << 16, n - len(body)))
                if not chunk:
                    break
                body += chunk
            return header, body[:n]
        except (OSError, ValueError) as exc:
            raise ReaderError(f"{payload.get('op')}: {exc}") from exc
        finally:
            s.close()

    def ping(self) -> dict[str, Any]:
        return self.call({"op": "ping"})[0]

    def frame(self, max_age: float) -> tuple[dict[str, Any], bytes]:
        return self.call({"op": "frame", "max_age": max_age})
