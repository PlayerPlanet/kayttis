import time

from kayttis_core import Observation
from kayttis_pi.config import DeviceConfig
from kayttis_pi.hub import Smoother, StateHub


def dev(**kw):
    base = dict(id="d", name="D", kind="k", source="mqtt", topic="t", interpreter="value")
    return DeviceConfig(**{**base, **kw})


def test_unknown_until_first_update_then_fresh():
    hub = StateHub([dev()])
    s = hub.get("d")
    assert s.state == "unknown" and s.stale
    hub.update("d", Observation(state="on", value=5))
    s = hub.get("d")
    assert s.state == "on" and s.value == 5 and not s.stale


def test_none_keeps_previous_state():
    hub = StateHub([dev()])
    hub.update("d", Observation(state="closed"))
    assert hub.update("d", Observation(state=None)) is None
    assert hub.get("d").state == "closed"


def test_stale_after():
    hub = StateHub([dev(stale_after=0.01)])
    hub.update("d", Observation(state="on"))
    time.sleep(0.03)
    assert hub.get("d").stale


def test_smoothing_majority():
    sm = Smoother(5)
    out = [sm.push(s) for s in ["closed", "closed", "open", "closed", "open", "open", "open"]]
    assert out[2] == "closed"  # one stray "open" does not flip it
    assert out[-1] == "open"

    hub = StateHub([dev(smooth_window=3)])
    for s in ["closed", "closed", "open"]:
        hub.update("d", Observation(state=s))
    st = hub.get("d")
    assert st.state == "closed" and st.attributes["raw_state"] == "open"
