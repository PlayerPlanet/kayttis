import kayttis_pi.plugins  # noqa: F401
import pytest
from kayttis_core import build_interpreter


def test_power_levels():
    f = build_interpreter("power_levels", {"levels": {"off": 0, "on": 10, "brewing": 300}})
    assert f({"power": 1.2}).state == "off"
    assert f({"power": 62}).state == "on"
    assert f({"power": 1450, "state": "ON"}).state == "brewing"
    assert f({"power": 900, "state": "OFF"}).state == "off"  # switched off wins
    assert f({"linkquality": 90}) is None  # no information


def test_threshold_mapping_value():
    t = build_interpreter("threshold", {"field": "temperature", "threshold": 35, "unit": "C"})
    assert t({"temperature": 50}).state == "on"
    assert t({"temperature": 21}).value == 21
    m = build_interpreter(
        "mapping", {"field": "contact", "states": {"true": "closed", "false": "open"}}
    )
    assert m({"contact": False}).state == "open"
    assert m({"other": 1}) is None
    v = build_interpreter("value", {"field": "humidity", "unit": "%"})
    assert v({"humidity": "41.5"}).value == 41.5


def test_import_path_and_unknown():
    f = build_interpreter("kayttis_pi.plugins.interpreters:value", {"field": "x"})
    assert f({"x": 3}).value == 3
    with pytest.raises(LookupError):
        build_interpreter("nope")
