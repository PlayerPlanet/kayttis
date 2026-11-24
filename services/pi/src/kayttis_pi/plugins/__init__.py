"""Built-in plugins. Importing this package registers them in the kayttis_core registry."""

from . import classifiers, interpreters

__all__ = ["classifiers", "interpreters"]
