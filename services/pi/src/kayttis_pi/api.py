"""HTTP API. All routes live under /api (the Pages proxy forwards /api/* unchanged)."""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from kayttis_core import DeviceState, registered

from . import plugins  # noqa: F401 - registers the built-in plugins
from .config import Config
from .hub import StateHub
from .sources import MqttSource, ReaderSource

KEEPALIVE_S = 20.0  # well under Cloudflare's 100 s idle timeout


def create_app(cfg: Config) -> FastAPI:
    hub = StateHub(cfg.devices)
    mqtt = MqttSource(cfg.mqtt, cfg.devices, hub)
    reader = ReaderSource(cfg.reader, cfg.devices, hub)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        hub.bind_loop(asyncio.get_running_loop())
        mqtt.start()
        reader.start()
        try:
            yield
        finally:
            await reader.stop()
            mqtt.stop()

    app = FastAPI(
        title="kayttis-pi",
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url=None,
    )
    app.state.hub, app.state.mqtt, app.state.reader = hub, mqtt, reader

    @app.get("/api/health")
    def health() -> dict:
        return {
            "ok": True,
            "mqtt": mqtt.status(),
            "reader": reader.status(),
            "devices": len(cfg.devices),
            "plugins": registered(),
        }

    @app.get("/api/devices")
    def devices() -> list[DeviceState]:
        return hub.all()

    @app.get("/api/devices/{device_id}")
    def device(device_id: str) -> DeviceState:
        if device_id not in hub:
            raise HTTPException(404, f"unknown device {device_id!r}")
        return hub.get(device_id)

    @app.get("/api/stream")
    async def stream(request: Request) -> StreamingResponse:
        """Server-sent events: every device once, then each change as it happens."""

        def event(s: DeviceState) -> str:
            return f"event: device\ndata: {s.model_dump_json()}\n\n"

        async def gen() -> AsyncIterator[str]:
            q = hub.subscribe()
            try:
                for s in hub.all():
                    yield event(s)
                while not await request.is_disconnected():
                    try:
                        s = await asyncio.wait_for(q.get(), timeout=KEEPALIVE_S)
                    except TimeoutError:
                        yield ": keepalive\n\n"
                        continue
                    yield event(s)
            finally:
                hub.unsubscribe(q)

        return StreamingResponse(
            gen(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"},
        )

    return app
