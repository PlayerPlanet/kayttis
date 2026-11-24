"""Reader source: polls the kahvi reader service and feeds three kinds of devices.

* ``signal = "lights"``: on while the reader has a recent *lit* frame (its own luma test).
* ``signal = "coffee_level"``: the reader's millilitre reading for one pot side.
* ``source = "frame"``: any registered classifier run on the reader's latest frame.

Rules that keep us from disturbing kahvibot: we never open the camera; a frame is only
requested with ``max_age = dark_after`` and only after ``ping`` shows a lit frame younger
than that, so the reader answers from memory instead of capturing; a frame is processed
once per reader ``seq``.
"""

import asyncio
import io
import logging
import time
from typing import Any

from kayttis_core import Classifier, Observation, build_classifier
from PIL import Image

from ..config import DeviceConfig, ReaderConfig
from ..hub import StateHub
from ..reader_ipc import ReaderClient, ReaderError

log = logging.getLogger(__name__)


class ReaderSource:
    def __init__(self, cfg: ReaderConfig, devices: list[DeviceConfig], hub: StateHub) -> None:
        self.cfg = cfg
        self.hub = hub
        self.client = ReaderClient(cfg.socket, cfg.timeout)
        self.lights = [d.id for d in devices if d.source == "reader" and d.signal == "lights"]
        self.levels = [
            (d.id, d.side) for d in devices if d.source == "reader" and d.signal == "coffee_level"
        ]
        self.classifiers: list[tuple[str, Classifier]] = [
            (d.id, build_classifier(d.classifier, d.params)) for d in devices if d.source == "frame"
        ]
        self.reachable = False
        self.last_error = ""
        self.last_seq: int | None = None
        self._seq_changed_at = time.monotonic()
        self._frame_seq: int | None = None
        self.frames_processed = 0
        # Latest lit frame for /api/camera: (jpeg, captured_at epoch, reader seq).
        self.latest_frame: tuple[bytes, float, int | None] | None = None
        self._task: asyncio.Task[None] | None = None

    @property
    def active(self) -> bool:
        return self.cfg.enabled and bool(
            self.lights or self.levels or self.classifiers or self.cfg.serve_camera
        )

    # -- one poll -----------------------------------------------------------------------
    def poll_once(self) -> None:
        """Blocking; run in a worker thread."""
        try:
            ping = self.client.ping()
        except ReaderError as exc:
            self._fail(str(exc))
            return
        if not ping.get("ok"):
            self._fail(str(ping.get("error", "ping not ok")))
            return
        self.reachable, self.last_error = True, ""

        seq = ping.get("seq")
        now = time.monotonic()
        if seq != self.last_seq:
            self.last_seq, self._seq_changed_at = seq, now
        if now - self._seq_changed_at > self.cfg.stall_after:
            self.last_error = "reader seq not advancing"
            return  # stalled reader: let our devices go stale rather than guess

        age = ping.get("last_lit_age")
        lit = age is not None and age <= self.cfg.dark_after
        for device_id in self.lights:
            self.hub.update(
                device_id,
                Observation(state="on" if lit else "off", attributes={"last_lit_age": age}),
            )
        if not lit or not (self.levels or self.classifiers or self.cfg.serve_camera):
            return

        try:
            header, jpeg = self.client.frame(max_age=self.cfg.dark_after)
        except ReaderError as exc:
            self._fail(str(exc))
            return
        if not header.get("ok") or not jpeg:
            return
        if header.get("seq") is not None and header.get("seq") == self._frame_seq:
            return  # same frame as last time
        self._frame_seq = header.get("seq")
        captured = header.get("captured_at") or time.time() - float(header.get("age") or 0)
        if self.cfg.serve_camera:
            self.latest_frame = (jpeg, float(captured), header.get("seq"))
        self._apply_levels(header.get("pots") or [], header)
        self._apply_classifiers(jpeg, header)
        self.frames_processed += 1

    def _apply_levels(self, pots: list[dict[str, Any]], header: dict[str, Any]) -> None:
        by_side = {p.get("side"): p for p in pots}
        for device_id, side in self.levels:
            pot = by_side.get(side)
            if pot is None:
                self.hub.update(device_id, Observation(state="no_pot", attributes={"side": side}))
                continue
            tier = pot.get("tier") or ("ok" if pot.get("ok") else "abstain")
            if tier == "abstain" or pot.get("ml") is None:
                continue  # the reader itself does not trust this reading
            self.hub.update(
                device_id,
                Observation(
                    state=tier,  # ok | uncertain
                    value=round(float(pot["ml"]), 0),
                    unit="ml",
                    attributes={"side": side, "frame_age": header.get("age")},
                ),
            )

    def _apply_classifiers(self, jpeg: bytes, header: dict[str, Any]) -> None:
        if not self.classifiers:
            return
        try:
            image = Image.open(io.BytesIO(jpeg)).convert("RGB")
        except OSError:
            return
        for device_id, classify in self.classifiers:
            try:
                obs = classify(image)
            except Exception:  # noqa: BLE001 - one broken plugin must not stop the others
                log.warning("classifier failed for %s", device_id, exc_info=True)
                continue
            obs.attributes.setdefault("frame_seq", header.get("seq"))
            self.hub.update(device_id, obs)

    def _fail(self, error: str) -> None:
        if self.reachable or error != self.last_error:
            log.warning("reader: %s", error)
        self.reachable, self.last_error = False, error

    # -- lifecycle ----------------------------------------------------------------------
    async def _run(self) -> None:
        while True:
            try:
                await asyncio.to_thread(self.poll_once)
            except Exception:  # noqa: BLE001 - keep polling
                log.exception("reader poll failed")
            await asyncio.sleep(self.cfg.poll_interval)

    def start(self) -> None:
        if not self.active:
            log.info("reader source disabled")
            return
        self._task = asyncio.get_running_loop().create_task(self._run())

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def status(self) -> dict[str, Any]:
        return {
            "enabled": self.active,
            "reachable": self.reachable,
            "error": self.last_error or None,
            "seq": self.last_seq,
            "frames_processed": self.frames_processed,
        }
