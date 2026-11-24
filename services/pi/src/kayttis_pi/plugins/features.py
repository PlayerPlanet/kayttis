"""Cheap image features for small fixed-crop classifiers (numpy + Pillow only, no scikit-image,
so nothing heavy is imported on the Pi). Shared by inference and tools/train_*.py, so the
two can never drift apart."""

import numpy as np
from PIL import Image


def hog(gray: np.ndarray, cell: int = 10, bins: int = 9, block: int = 2) -> np.ndarray:
    """Histogram of oriented gradients: unsigned orientations, hard binning per cell,
    L2-Hys normalisation over overlapping ``block``x``block`` cell blocks."""
    g = gray.astype(np.float32)
    gx = np.zeros_like(g)
    gy = np.zeros_like(g)
    gx[:, 1:-1] = g[:, 2:] - g[:, :-2]
    gy[1:-1, :] = g[2:, :] - g[:-2, :]
    mag = np.hypot(gx, gy)
    ang = np.rad2deg(np.arctan2(gy, gx)) % 180.0
    idx = np.minimum((ang / (180.0 / bins)).astype(np.int64), bins - 1)

    ch, cw = g.shape[0] // cell, g.shape[1] // cell
    mag = mag[: ch * cell, : cw * cell]
    idx = idx[: ch * cell, : cw * cell]
    cell_id = (np.arange(ch * cell)[:, None] // cell) * cw + (np.arange(cw * cell)[None, :] // cell)
    flat = (cell_id * bins + idx).ravel()
    hist = np.bincount(flat, weights=mag.ravel(), minlength=ch * cw * bins).reshape(ch, cw, bins)

    out = []
    for y in range(ch - block + 1):
        for x in range(cw - block + 1):
            v = hist[y : y + block, x : x + block].ravel()
            v = v / np.sqrt(np.sum(v * v) + 1e-6)
            v = np.minimum(v, 0.2)
            v = v / np.sqrt(np.sum(v * v) + 1e-6)
            out.append(v)
    return np.concatenate(out).astype(np.float32)


def crop_features(image: Image.Image, box: tuple[int, int, int, int]) -> np.ndarray:
    """HOG of the crop + a 9x7 colour thumbnail + mean/std brightness."""
    crop = image.crop(box)
    gray = np.asarray(crop.convert("L"), dtype=np.float32) / 255.0
    thumb = np.asarray(crop.convert("RGB").resize((9, 7)), dtype=np.float32).ravel() / 255.0
    return np.concatenate([hog(gray), thumb, [gray.mean(), gray.std()]]).astype(np.float32)
