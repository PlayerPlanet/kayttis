"""Brand graphics (titles, readouts, state cards, end cards) rendered to
transparent PNGs with headless Chrome, so typography uses the real brand fonts."""
from __future__ import annotations

from pathlib import Path

from common import (CHROME, D_KIINNI, D_MERKKI_INK, D_MUTED, D_SURFACE, D_SURFACE2,
                    FONTS, INK, KIINNI, LOGO, MERKKIVALO, PAPER, WORK, run)

FONT_CSS = f"""
@font-face{{font-family:FG;font-weight:700;src:url('{(FONTS/'FamiljenGrotesk-Bold.ttf').as_uri()}')}}
@font-face{{font-family:FG;font-weight:600;src:url('{(FONTS/'FamiljenGrotesk-SemiBold.ttf').as_uri()}')}}
@font-face{{font-family:FT;font-weight:400;src:url('{(FONTS/'Figtree-Regular.ttf').as_uri()}')}}
@font-face{{font-family:FT;font-weight:600;src:url('{(FONTS/'Figtree-SemiBold.ttf').as_uri()}')}}
@font-face{{font-family:JB;font-weight:500;src:url('{(FONTS/'JetBrainsMono-Medium.ttf').as_uri()}')}}
"""

BASE_CSS = f"""
.c{{margin:0 -0.14em}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:transparent;overflow:hidden}}
body{{position:relative;font-family:FT;color:{PAPER};-webkit-font-smoothing:antialiased}}
.mono{{font-family:JB;font-weight:500;font-variant-numeric:tabular-nums;letter-spacing:-0.01em}}
.disp{{font-family:FG;font-weight:700;letter-spacing:-0.015em;line-height:1.0}}
.label{{font-family:FT;font-weight:600;text-transform:uppercase;letter-spacing:0.06em}}
.shade{{text-shadow:0 2px 18px rgba(15,28,36,.55),0 1px 3px rgba(15,28,36,.6)}}
"""

MARK_DARK = (LOGO / "hanax-mark-on-dark.svg").as_uri()
LOCKUP_DARK = (LOGO / "hanax-lockup-on-dark.svg").as_uri()


def render(name: str, body: str, w: int, h: int, extra_css: str = "") -> Path:
    gdir = WORK / "gfx"
    html = gdir / f"{name}.html"
    png = gdir / f"{name}.png"
    html.write_text(
        f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{BASE_CSS}"
        f"body{{width:{w}px;height:{h}px}}{extra_css}</style></head><body>{body}</body></html>",
        encoding="utf-8")
    run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--virtual-time-budget=1500",
         f"--window-size={w},{h}", "--default-background-color=00000000",
         f"--screenshot={png}", html.as_uri()])
    return png


# ---------- reusable fragments -------------------------------------------------

def state_row(name: str, state: str) -> str:
    """Device row following the brand state rule: never colour alone."""
    if state == "on":
        chip = (f"<span class='label' style='background:{MERKKIVALO};color:{INK};"
                f"padding:8px 16px;border-radius:999px;font-size:22px;display:inline-flex;"
                f"align-items:center;gap:10px'><i style='width:12px;height:12px;border-radius:50%;"
                f"background:{INK};display:inline-block'></i>PÄÄLLÄ</span>")
    else:
        chip = (f"<span class='label' style='background:{D_SURFACE2};color:{D_MUTED};"
                f"padding:8px 16px;border-radius:999px;font-size:22px'>POIS</span>")
    return (f"<div style='display:flex;justify-content:space-between;align-items:center;"
            f"padding:18px 0;border-top:1px solid #2c414c'>"
            f"<span style='font-weight:600;font-size:30px'>{name}</span>{chip}</div>")


def panel_card(rows: list[tuple[str, str]], header: str, sub: str, width: int = 560) -> str:
    rows_html = "".join(state_row(n, s) for n, s in rows)
    return (f"<div style='width:{width}px;background:{D_SURFACE};border-radius:20px;"
            f"padding:28px 32px 18px;box-shadow:0 18px 48px rgba(0,0,0,.35)'>"
            f"<div style='display:flex;align-items:center;gap:14px;margin-bottom:14px'>"
            f"<img src='{MARK_DARK}' style='height:40px'>"
            f"<span class='label' style='font-size:20px;color:{D_MUTED}'>Kotipaneeli</span>"
            f"<span class='mono' style='margin-left:auto;font-size:22px;color:{D_MUTED}'>13:57</span></div>"
            f"<div class='disp' style='font-size:44px;margin:6px 0 4px'>{header}</div>"
            f"<div style='font-size:24px;color:{D_MUTED};margin-bottom:12px'>{sub}</div>"
            f"{rows_html}</div>")


def all_clear_chip(size: float = 1.0) -> str:
    s = size
    return (f"<div style='display:inline-flex;align-items:center;gap:{18*s}px;background:{KIINNI};"
            f"color:{PAPER};border-radius:999px;padding:{18*s}px {34*s}px {18*s}px {22*s}px;"
            f"box-shadow:0 14px 40px rgba(0,0,0,.3)'>"
            f"<svg width='{46*s}' height='{46*s}' viewBox='0 0 46 46'><circle cx='23' cy='23' r='23' fill='{PAPER}'/>"
            f"<path d='M13 24l7 7 13-15' stroke='{KIINNI}' stroke-width='5' fill='none' "
            f"stroke-linecap='round' stroke-linejoin='round'/></svg>"
            f"<span><span class='label' style='display:block;font-size:{34*s}px;letter-spacing:0.06em'>Kaikki kiinni</span>"
            f"<span class='mono' style='display:block;font-size:{20*s}px;opacity:.85;margin-top:2px'>"
            f"tarkistettu 2 s sitten</span></span></div>")


def end_card(w: int, h: int, vertical: bool = False) -> str:
    lock_w = 620 if not vertical else 640
    tag = 96 if not vertical else 92
    return (f"<div style='position:absolute;inset:0;background:{INK};display:flex;flex-direction:column;"
            f"align-items:center;justify-content:center;text-align:center'>"
            f"<img src='{LOCKUP_DARK}' style='width:{lock_w}px'>"
            f"<div class='disp' style='font-size:{tag}px;margin-top:{64 if not vertical else 80}px'>"
            f"Lähde kotoa huoletta.</div>"
            f"<div style='font-size:{34 if not vertical else 38}px;color:{D_MUTED};margin-top:28px;"
            f"max-width:{1300 if not vertical else 860}px;line-height:1.4'>"
            f"Näet yhdellä vilkaisulla, jäikö hana, liesi tai valot päälle.</div>"
            f"<div class='mono' style='font-size:{40 if not vertical else 44}px;color:{PAPER};"
            f"margin-top:{56 if not vertical else 90}px;padding:14px 30px;border:2px solid #2c414c;"
            f"border-radius:999px'>kayttis.kiirikki.fi</div>"
            f"<div style='position:absolute;bottom:{70 if not vertical else 150}px;font-size:24px;"
            f"color:{D_MUTED};letter-spacing:0.02em'>Aalto-yliopisto · Käytettävyys 2026 · Ryhmä 1</div>"
            f"</div>")
