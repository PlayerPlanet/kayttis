"""Shared paths and helpers for the Hanax launch-video build.

Re-render everything with:  python launch/video-src/build_all.py
Requires ffmpeg 8 (with libass, libfreetype) and Google Chrome on PATH/default location.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # kayttis/
SRC_DIR = Path(__file__).resolve().parent            # launch/video-src
BRAND = ROOT / "brand"
FONTS = BRAND / "fonts"
LOGO = BRAND / "logo"
OUT = ROOT / "launch" / "video"
WORK = OUT / "_work"
WEB = ROOT / "frontend" / "public" / "media"

# Raw phone clips (read-only). Override with HANAX_CLIPS env var.
CLIPS = Path(os.environ.get(
    "HANAX_CLIPS",
    r"C:\Users\Käyttäjä\AppData\Local\Temp\claude\fd212a09e56455f8"
    r"\d2d6deb6-817f-42cc-bac5-fc2dcdec7f3c\scratchpad\klipit\clips"))

CHROME = os.environ.get(
    "CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")

FPS = 30

# Brand colours (brand/tokens.css)
INK = "#0f1c24"
PAPER = "#f4f7f6"
VESI = "#136a87"
MERKKIVALO = "#f08a16"
KIINNI = "#2c8564"
# dark-surface variants
D_SURFACE = "#15242d"
D_SURFACE2 = "#1d313c"
D_MUTED = "#a3b2b8"
D_KIINNI = "#4fc096"
D_MERKKI_INK = "#ffb866"


def clip(name: str) -> Path:
    """'08-09' -> full path of video_2026-11-24_14-08-09.mp4"""
    return CLIPS / f"video_2026-11-24_14-{name}.mp4"


# Gentle, consistent grade: tame the warm indoor light a little toward the
# brand's cool, natural look; small contrast lift; light sharpening after upscale.
GRADE = ("eq=contrast=1.05:saturation=0.94:gamma=0.98,"
         "colorbalance=rs=-0.03:gs=0.0:bs=0.035:rm=-0.025:bm=0.025:rh=-0.01:bh=0.01,"
         "unsharp=5:5:0.45:5:5:0.0")


def run(args: list, cwd: Path | None = None, quiet: bool = True) -> str:
    cmd = [str(a) for a in args]
    if cmd[0] == "ffmpeg":
        cmd[1:1] = ["-hide_banner", "-y"] + (["-loglevel", "error"] if quiet else [])
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)[:600]}\n{p.stderr[-3000:]}")
    return p.stderr


def probe_duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True)
    return float(json.loads(out.stdout)["format"]["duration"])


def ensure_dirs():
    for d in (OUT, WORK, WORK / "gfx", WORK / "shots", WORK / "shots9", WORK / "audio",
              WORK / "fonts", WEB):
        d.mkdir(parents=True, exist_ok=True)
    # libass gets a local fonts dir (static TTFs only, so names resolve cleanly)
    for f in ("Figtree-SemiBold.ttf", "Figtree-Regular.ttf", "FamiljenGrotesk-Bold.ttf",
              "FamiljenGrotesk-SemiBold.ttf", "JetBrainsMono-Medium.ttf"):
        dst = WORK / "fonts" / f
        if not dst.exists():
            shutil.copy(FONTS / f, dst)


def ts(sec: float) -> str:
    """SRT timestamp."""
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ass_ts(sec: float) -> str:
    cs = int(round(sec * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"
