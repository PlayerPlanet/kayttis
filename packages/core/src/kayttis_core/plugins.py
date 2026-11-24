"""Plugin registry: interpreters (MQTT payload -> Observation), classifiers (frame -> Observation).

A device in the config names its plugin either by a registered name (``"power_levels"``)
or by an import path (``"my_package.module:factory"``). A factory is called with the
device's ``params`` table as keyword arguments and returns the plugin instance.

    @register_interpreter("my_sensor")
    def my_sensor(field: str = "value"):
        def interpret(payload: dict) -> Observation | None: ...
        return interpret
"""

from collections.abc import Callable
from importlib import import_module
from typing import Any, Protocol

from .models import Observation


class Interpreter(Protocol):
    def __call__(self, payload: dict[str, Any]) -> Observation | None: ...


class Classifier(Protocol):
    def __call__(self, image: Any) -> Observation:
        """``image`` is an RGB ``PIL.Image`` of a full camera frame."""
        ...


InterpreterFactory = Callable[..., Interpreter]
ClassifierFactory = Callable[..., Classifier]

_INTERPRETERS: dict[str, InterpreterFactory] = {}
_CLASSIFIERS: dict[str, ClassifierFactory] = {}


def register_interpreter(name: str) -> Callable[[InterpreterFactory], InterpreterFactory]:
    def deco(factory: InterpreterFactory) -> InterpreterFactory:
        _INTERPRETERS[name] = factory
        return factory

    return deco


def register_classifier(name: str) -> Callable[[ClassifierFactory], ClassifierFactory]:
    def deco(factory: ClassifierFactory) -> ClassifierFactory:
        _CLASSIFIERS[name] = factory
        return factory

    return deco


def _resolve(ref: str, registry: dict[str, Callable[..., Any]], what: str) -> Callable[..., Any]:
    if ":" in ref:
        module, _, attr = ref.partition(":")
        return getattr(import_module(module), attr)
    try:
        return registry[ref]
    except KeyError:
        known = ", ".join(sorted(registry)) or "none"
        raise LookupError(f"unknown {what} {ref!r} (registered: {known})") from None


def build_interpreter(ref: str, params: dict[str, Any] | None = None) -> Interpreter:
    return _resolve(ref, _INTERPRETERS, "interpreter")(**(params or {}))


def build_classifier(ref: str, params: dict[str, Any] | None = None) -> Classifier:
    return _resolve(ref, _CLASSIFIERS, "classifier")(**(params or {}))


def registered() -> dict[str, list[str]]:
    return {"interpreters": sorted(_INTERPRETERS), "classifiers": sorted(_CLASSIFIERS)}
