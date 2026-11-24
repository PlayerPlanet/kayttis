"""Smooth Ken Burns moves on the product renders.

ffmpeg's zoompan rounds the crop window to whole pixels, which wobbles on slow moves.
Here every frame is a sub-pixel affine warp (OpenCV, Lanczos) of the 2400x1600 source,
with an ease-in-out curve, piped to ffmpeg as raw frames.

A window is (cx, cy, w): centre in 0..1 of the source, width as a fraction of the
source width; the height follows the output aspect ratio.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import cv2
import numpy as np

from common import FPS, WORK


def ease(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return t * t * t * (t * (6 * t - 15) + 10)   # smootherstep: zero velocity + acceleration at ends


def load(path: Path) -> np.ndarray:
    im = cv2.imdecode(np.fromfile(str(path), np.uint8), cv2.IMREAD_UNCHANGED)  # non-ASCII-safe
    if im.shape[2] == 4:                          # flatten alpha onto the brand black
        a = im[:, :, 3:4].astype(np.float32) / 255
        im = (im[:, :, :3] * a + np.array([14, 12, 10]) * (1 - a)).astype(np.uint8)
    return im


def ring_off(im: np.ndarray) -> np.ndarray:
    """The same render with the amber light switched off: saturated orange pixels lose
    their colour and most of their brightness (glow -> dark titanium)."""
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    w = np.clip((s - 14) / 55, 0, 1) * ((h >= 3) & (h <= 40))
    w = cv2.GaussianBlur(w.astype(np.float32), (0, 0), 3)
    hsv[..., 1] = s * (1 - w)
    hsv[..., 2] = v * (1 - 0.86 * w)
    return cv2.cvtColor(hsv.clip(0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR)


def _video_frames(src: Path, tin: float, dur: float):
    """Decode a movie to BGR frames at its native size (non-ASCII-path safe)."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", str(src)],
                         capture_output=True, text=True).stdout.strip().split(",")
    w, h = int(out[0]), int(out[1])
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{tin:.3f}",
                          "-t", f"{dur:.3f}", "-i", str(src), "-vf", f"fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL)
    last = None
    while True:
        buf = p.stdout.read(w * h * 3)
        if len(buf) < w * h * 3:
            break
        last = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        yield last
    p.wait()
    while last is not None:      # hold the last frame if the source runs short
        yield last


def render_kb(out: Path, src: Path, dur: float, size: tuple[int, int],
              a: tuple[float, float, float], b: tuple[float, float, float],
              variant: str | None = None, mix: tuple[float, float] | None = None,
              tin: float = 0.0) -> Path:
    """Render `dur` seconds moving the window from a to b. With variant='ring_off' and
    mix=(t0, t1), crossfade to the ring-off version of the image between t0 and t1."""
    W, H = size
    is_video = src.suffix.lower() in (".mp4", ".mov", ".webm")
    frames = _video_frames(src, tin, dur + 0.5) if is_video else None
    im = next(frames) if is_video else load(src)
    im2 = ring_off(im) if variant == "ring_off" and not is_video else None
    sh, sw = im.shape[:2]
    n = int(round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "12",
                          "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    for i in range(n):
        k = ease(i / max(1, n - 1))
        cx, cy, w = (a[j] + (b[j] - a[j]) * k for j in range(3))
        ww = w * sw
        sc = W / ww
        x0, y0 = cx * sw - ww / 2, cy * sh - (H / sc) / 2
        M = np.array([[sc, 0, -x0 * sc], [0, sc, -y0 * sc]], dtype=np.float64)
        if is_video and i > 0:
            im = next(frames)
        src_im = im
        if im2 is not None and mix:
            f = ease((i / FPS - mix[0]) / max(1e-3, mix[1] - mix[0]))
            src_im = cv2.addWeighted(im, 1 - f, im2, f, 0) if 0 < f < 1 else (im2 if f >= 1 else im)
        fr = cv2.warpAffine(src_im, M, (W, H), flags=cv2.INTER_LANCZOS4,
                            borderMode=cv2.BORDER_CONSTANT, borderValue=(10, 12, 14))
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"kenburns encode failed: {out}")
    return out


if __name__ == "__main__":   # quick preview of the ring-off variant
    from common import RENDERS
    WORK.joinpath("kb").mkdir(parents=True, exist_ok=True)
    ok, buf = cv2.imencode(".jpg", cv2.resize(ring_off(load(RENDERS / "hxp-knob-macro.png")), (1200, 800)))
    buf.tofile(str(WORK / "kb" / "knob_off_preview.jpg"))
