"""Built-in MQTT interpreters. zigbee2mqtt publishes one JSON object per device per change,
e.g. ``{"power": 62.1, "state": "ON", "linkquality": 120}`` for a smart plug."""

from typing import Any

from kayttis_core import Observation, register_interpreter


def _number(payload: dict[str, Any], field: str) -> float | None:
    try:
        return float(payload[field])
    except (KeyError, TypeError, ValueError):
        return None


@register_interpreter("power_levels")
def power_levels(
    field: str = "power",
    levels: dict[str, float] | None = None,
    switch_field: str = "state",
):
    """Smart plug -> named level by power draw, e.g. off / warming / brewing.

    ``levels`` maps state name -> minimum watts; the highest level reached wins.
    A plug switched OFF is "off" regardless of the reading.
    """
    table = sorted((levels or {"off": 0.0, "on": 5.0}).items(), key=lambda kv: kv[1])
    lowest = table[0][0]

    def interpret(payload: dict[str, Any]) -> Observation | None:
        if str(payload.get(switch_field, "")).upper() == "OFF":
            return Observation(state=lowest, value=0.0, unit="W", attributes={"switch": "OFF"})
        watts = _number(payload, field)
        if watts is None:
            return None
        state = lowest
        for name, minimum in table:
            if watts >= minimum:
                state = name
        return Observation(state=state, value=watts, unit="W")

    return interpret


@register_interpreter("threshold")
def threshold(field: str, threshold: float, above: str = "on", below: str = "off", unit: str = ""):
    """Numeric field compared to a threshold, e.g. temperature near the oven -> on/off."""

    def interpret(payload: dict[str, Any]) -> Observation | None:
        v = _number(payload, field)
        if v is None:
            return None
        return Observation(state=above if v >= threshold else below, value=v, unit=unit or None)

    return interpret


@register_interpreter("mapping")
def mapping(field: str, states: dict[str, str]):
    """Discrete field -> state, e.g. a contact sensor ``{"true": "closed", "false": "open"}``.
    Keys are compared as lower-case strings, so JSON true/false map via "true"/"false"."""
    table = {str(k).lower(): v for k, v in states.items()}

    def interpret(payload: dict[str, Any]) -> Observation | None:
        if field not in payload:
            return None
        raw = payload[field]
        state = table.get(str(raw).lower())
        if state is None:
            return None
        return Observation(state=state, attributes={field: raw})

    return interpret


@register_interpreter("value")
def value(field: str, unit: str = "", state: str = "ok"):
    """Pass a numeric field through as the device value (e.g. a plain temperature sensor)."""

    def interpret(payload: dict[str, Any]) -> Observation | None:
        v = _number(payload, field)
        if v is None:
            return None
        return Observation(state=state, value=v, unit=unit or None)

    return interpret
