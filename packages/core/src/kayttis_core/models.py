"""Data shapes shared by every source, plugin and the API."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Observation(BaseModel):
    """One reading produced by a plugin (an MQTT interpreter or a frame classifier).

    ``state=None`` means "no information this time" (e.g. the tap knob is hidden behind
    a coffee pot): the hub keeps the previous state instead of overwriting it.
    """

    state: str | None = None
    value: float | None = None
    unit: str | None = None
    confidence: float | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)


class DeviceState(BaseModel):
    """What the API returns for one device."""

    id: str
    name: str
    kind: str
    source: str
    state: str = "unknown"
    value: float | None = None
    unit: str | None = None
    confidence: float | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime | None = None
    stale: bool = True
