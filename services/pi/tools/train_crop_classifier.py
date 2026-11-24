"""Train a fixed-crop classifier and export it as .npz for kayttis_pi's LinearCropClassifier.

    uv run python services/pi/tools/train_crop_classifier.py \
        --labels services/pi/data/tap_knob/labels.csv \
        --frames <dir with the labelled JPEGs> \
        --box 745 225 835 295 \
        --test-from 2026-09-06 --test-window 2026-09-03_10-50 2026-09-03_14 \
        --out services/pi/src/kayttis_pi/models/tap_knob.npz

labels.csv columns: file,timestamp,label (timestamp sorts lexically, e.g. 2026-09-03_10-09-11).
The split is by time, never random: neighbouring frames are near-duplicates.
Frames are not in the repo; the tap-knob set is the kahvibot survey cache from Sep 2026.
Needs the dev dependencies (scikit-learn): `uv sync --all-packages`.
"""

import argparse
import csv
import time
from collections import Counter
from pathlib import Path

import numpy as np
from kayttis_pi.plugins.features import crop_features
from PIL import Image, ImageFile
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler

ImageFile.LOAD_TRUNCATED_IMAGES = True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", type=Path, required=True)
    ap.add_argument("--frames", type=Path, required=True)
    ap.add_argument("--box", type=int, nargs=4, required=True, metavar=("X0", "Y0", "X1", "Y1"))
    ap.add_argument("--test-from", default="", help="timestamps >= this are held out")
    ap.add_argument(
        "--test-window",
        nargs=2,
        default=None,
        metavar=("FROM", "TO"),
        help="an extra held-out window [FROM, TO)",
    )
    ap.add_argument("--C", type=float, default=0.1)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    rows = list(csv.DictReader(a.labels.open(encoding="utf-8")))
    box = tuple(a.box)
    X = np.stack(
        [crop_features(Image.open(a.frames / r["file"]).convert("RGB"), box) for r in rows]
    )
    y = np.array([r["label"] for r in rows])
    ts = [r["timestamp"] for r in rows]

    def held_out(t: str) -> bool:
        if a.test_from and t >= a.test_from:
            return True
        return bool(a.test_window and a.test_window[0] <= t < a.test_window[1])

    test = np.array([held_out(t) for t in ts])
    classes = sorted(set(y))
    print("train", dict(Counter(y[~test])), "test", dict(Counter(y[test])))

    def fit(Xf, yf):
        scaler = StandardScaler().fit(Xf)
        model = LogisticRegression(C=a.C, max_iter=5000).fit(scaler.transform(Xf), yf)
        return scaler, model

    if test.any():
        scaler, model = fit(X[~test], y[~test])
        pred = model.predict(scaler.transform(X[test]))
        print(f"held-out accuracy {np.mean(pred == y[test]):.3f}  (rows true, cols predicted)")
        print("   ", classes)
        print(confusion_matrix(y[test], pred, labels=classes))
        for t, true, p in zip(np.array(ts)[test], y[test], pred, strict=True):
            if true != p:
                print("  miss", t, true, "->", p)

    # Final model on everything.
    scaler, model = fit(X, y)
    scale = np.where(scaler.scale_ == 0, 1.0, scaler.scale_)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        a.out,
        box=np.array(box, dtype=np.int32),
        classes=np.array(model.classes_, dtype=str),
        mean=scaler.mean_.astype(np.float32),
        scale=scale.astype(np.float32),
        coef=model.coef_.astype(np.float32),
        intercept=model.intercept_.astype(np.float32),
    )
    img = Image.open(a.frames / rows[0]["file"]).convert("RGB")
    n, t0 = 200, time.perf_counter()
    for _ in range(n):
        crop_features(img, box)
    print(f"features: {(time.perf_counter() - t0) / n * 1000:.2f} ms/frame; wrote {a.out}")


if __name__ == "__main__":
    main()
