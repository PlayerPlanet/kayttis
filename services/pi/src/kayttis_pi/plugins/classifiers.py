"""Built-in frame classifiers.

A classifier gets the full RGB frame the reader service already captured and returns an
Observation. ``state=None`` means "can't see it right now" and keeps the previous state.
"""

from importlib import resources
from pathlib import Path

import numpy as np
from kayttis_core import Observation, register_classifier
from PIL import Image

from .features import crop_features


class LinearCropClassifier:
    """Fixed crop -> features -> standardised multinomial logistic regression.

    The model file (.npz) holds ``box, classes, mean, scale, coef, intercept`` and is
    written by ``services/pi/tools/train_crop_classifier.py``.
    """

    def __init__(
        self,
        model: str | Path,
        box: list[int] | None = None,
        hidden_label: str = "hidden",
        min_confidence: float = 0.0,
    ) -> None:
        m = np.load(model, allow_pickle=False)
        self.box = tuple(int(v) for v in (box if box is not None else m["box"]))
        self.classes = [str(c) for c in m["classes"]]
        self.mean, self.scale = m["mean"], m["scale"]
        self.coef, self.intercept = m["coef"], m["intercept"]
        self.hidden_label = hidden_label
        self.min_confidence = min_confidence

    def probabilities(self, image: Image.Image) -> dict[str, float]:
        z = (crop_features(image, self.box) - self.mean) / self.scale
        logits = self.coef @ z + self.intercept
        if len(self.classes) == 2 and logits.shape[0] == 1:  # sklearn's binary layout
            logits = np.array([-logits[0], logits[0]]) / 2
        p = np.exp(logits - logits.max())
        p /= p.sum()
        return {c: float(v) for c, v in zip(self.classes, p, strict=True)}

    def __call__(self, image: Image.Image) -> Observation:
        probs = self.probabilities(image)
        label = max(probs, key=probs.__getitem__)
        conf = probs[label]
        attrs = {"probabilities": {k: round(v, 3) for k, v in probs.items()}}
        if label == self.hidden_label or conf < self.min_confidence:
            return Observation(state=None, confidence=conf, attributes={**attrs, "visible": False})
        return Observation(state=label, confidence=conf, attributes={**attrs, "visible": True})


def _bundled(name: str) -> Path:
    return Path(str(resources.files("kayttis_pi") / "models" / name))


@register_classifier("tap_knob")
def tap_knob(model: str = "", box: list[int] | None = None, min_confidence: float = 0.6):
    """Dishwasher valve lever under the tap: open / closed / hidden (see docs in README)."""
    return LinearCropClassifier(
        model or _bundled("tap_knob.npz"), box, min_confidence=min_confidence
    )


@register_classifier("linear_crop")
def linear_crop(
    model: str,
    box: list[int] | None = None,
    hidden_label: str = "hidden",
    min_confidence: float = 0.0,
):
    """Any classifier trained with tools/train_crop_classifier.py, by model path."""
    return LinearCropClassifier(
        model, box, hidden_label=hidden_label, min_confidence=min_confidence
    )
