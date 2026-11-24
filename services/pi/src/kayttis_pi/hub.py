"""In-memory state of every device, fed by the sources, read by the API.

Sources call ``update`` from their own threads (paho's network thread, worker threads);
listeners (the SSE endpoint) receive changes on the asyncio loop.
"""

import asyncio
import threading
import time
from collections import Counter, deque
from datetime import UTC, datetime

from kayttis_core import DeviceState, Observation

from .config import DeviceConfig


class Smoother:
    """Majority vote over the last ``window`` visible states (states change rarely)."""

    def __init__(self, window: int) -> None:
        self.recent: deque[str] = deque(maxlen=window)

    def push(self, state: str) -> str:
        self.recent.append(state)
        counts = Counter(self.recent)
        best = max(counts.values())
        # On a tie keep the most recent of the tied states.
        for s in reversed(self.recent):
            if counts[s] == best:
                return s
        return state


class StateHub:
    def __init__(self, devices: list[DeviceConfig]) -> None:
        self._cfg = {d.id: d for d in devices}
        self._states = {
            d.id: DeviceState(id=d.id, name=d.name, kind=d.kind, source=d.source) for d in devices
        }
        self._updated_mono: dict[str, float] = {}
        self._smoothers = {d.id: Smoother(d.smooth_window) for d in devices if d.smooth_window > 1}
        self._lock = threading.Lock()
        self._listeners: set[asyncio.Queue[DeviceState]] = set()
        self._loop: asyncio.AbstractEventLoop | None = None

    def bind_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    # -- writes -------------------------------------------------------------------------
    def update(self, device_id: str, obs: Observation | None) -> DeviceState | None:
        """Apply an observation. ``None`` or ``obs.state is None`` keeps the old state."""
        if obs is None or obs.state is None:
            return None
        with self._lock:
            old = self._states[device_id]
            smoother = self._smoothers.get(device_id)
            raw_state = obs.state
            state = smoother.push(raw_state) if smoother else raw_state
            attributes = dict(obs.attributes)
            if smoother and state != raw_state:
                attributes["raw_state"] = raw_state
            new = old.model_copy(
                update={
                    "state": state,
                    "value": obs.value,
                    "unit": obs.unit,
                    "confidence": obs.confidence,
                    "attributes": attributes,
                    "updated_at": datetime.now(UTC),
                    "stale": False,
                }
            )
            self._states[device_id] = new
            self._updated_mono[device_id] = time.monotonic()
        self._notify(new)
        return new

    # -- reads --------------------------------------------------------------------------
    def get(self, device_id: str) -> DeviceState:
        with self._lock:
            return self._with_staleness(self._states[device_id])

    def all(self) -> list[DeviceState]:
        with self._lock:
            return [self._with_staleness(s) for s in self._states.values()]

    def __contains__(self, device_id: str) -> bool:
        return device_id in self._states

    def _with_staleness(self, s: DeviceState) -> DeviceState:
        t = self._updated_mono.get(s.id)
        stale = t is None or time.monotonic() - t > self._cfg[s.id].stale_after
        return s if s.stale == stale else s.model_copy(update={"stale": stale})

    # -- listeners ----------------------------------------------------------------------
    def subscribe(self) -> asyncio.Queue[DeviceState]:
        q: asyncio.Queue[DeviceState] = asyncio.Queue(maxsize=256)
        self._listeners.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue[DeviceState]) -> None:
        self._listeners.discard(q)

    def _notify(self, state: DeviceState) -> None:
        loop = self._loop
        if loop is None or loop.is_closed():
            return
        loop.call_soon_threadsafe(self._fan_out, state)

    def _fan_out(self, state: DeviceState) -> None:
        for q in list(self._listeners):
            try:
                q.put_nowait(state)
            except asyncio.QueueFull:
                pass  # a slow client misses an update; it still gets the next one
