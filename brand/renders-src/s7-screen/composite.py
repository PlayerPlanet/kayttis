"""Replace the garbled AI text on the S7 panel screen with the real HX-P UI.

    uv run --with pillow --with numpy python brand/renders-src/s7-screen/composite.py
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "launch/ai-studio/s7-family-studio-raw.jpg"
OUT = ROOT / "launch/ai-studio/s7-family-studio.png"
OVL = Path(__file__).with_name("overlay.png")
X0, Y0, W, H = 760, 460, 625, 430  # screen text area in source px

img = Image.open(SRC).convert("RGB")
reg = img.crop((X0, Y0, X0 + W, Y0 + H))

# Clean screen: morphological opening removes the bright strokes but keeps the glass level.
clean = reg.filter(ImageFilter.MinFilter(11)).filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(8))
# Only touch pixels near old text.
diff = ImageChops.subtract(reg.convert("L"), clean.convert("L"))
mask = diff.point(lambda v: 255 if v > 6 else 0).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(4))
reg = Image.composite(clean, reg, mask)

# Fine film grain so the cleaned patches do not look flat.
rng = np.random.default_rng(7)
a = np.asarray(reg).astype(np.float32)
a += rng.normal(0, 1.6, a.shape[:2])[..., None] * (np.asarray(mask, np.float32)[..., None] / 255)
reg = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

ovl = Image.open(OVL).convert("RGBA").resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.5))
bloom = ovl.filter(ImageFilter.GaussianBlur(6))
bloom.putalpha(bloom.getchannel("A").point(lambda v: int(v * 0.35)))
reg = reg.convert("RGBA")
reg.alpha_composite(bloom)
reg.alpha_composite(ovl)

img.paste(reg.convert("RGB"), (X0, Y0))
img.save(OUT, optimize=True)
print("wrote", OUT, img.size)
