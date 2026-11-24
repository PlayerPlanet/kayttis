import time

import kayttis_pi.plugins  # noqa: F401
import numpy as np
from kayttis_core import build_classifier
from kayttis_pi.plugins.features import hog
from PIL import Image


def test_hog_shape():
    # 70x90 crop, 10 px cells -> 7x9 cells -> 6x8 blocks of 2*2*9
    assert hog(np.zeros((70, 90), np.float32)).shape == (6 * 8 * 36,)


def test_tap_knob_bundled_model():
    clf = build_classifier("tap_knob", {"min_confidence": 0.0})
    img = Image.new("RGB", (1280, 720), (128, 128, 128))
    t0 = time.perf_counter()
    obs = clf(img)
    assert time.perf_counter() - t0 < 0.5
    assert set(obs.attributes["probabilities"]) == {"open", "closed", "hidden"}
