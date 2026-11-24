"""v2 brand graphics (dark-first: graphite, Geist / Geist Mono, amber the only colour),
rendered to transparent PNGs with headless Chrome so the typography uses the real fonts."""
from __future__ import annotations

from pathlib import Path

from common import (AMBER, AMBER_INK, BG, CHROME, FONTS, LINE, LINE_STRONG, LOGO, RAISED,
                    SURFACE, SURFACE2, TITAANI, V2_INK, V2_MUTED, WORK, run)

FONT_CSS = "".join(
    f"@font-face{{font-family:{fam};font-weight:{w};src:url('{(FONTS / f).as_uri()}')}}"
    for fam, w, f in [("G", 400, "Geist-Regular.ttf"), ("G", 500, "Geist-Medium.ttf"),
                      ("G", 600, "Geist-SemiBold.ttf"), ("GM", 400, "GeistMono-Regular.ttf"),
                      ("GM", 500, "GeistMono-Medium.ttf")])

BASE_CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:transparent;overflow:hidden}}
body{{position:relative;font-family:G;font-weight:400;color:{V2_INK};-webkit-font-smoothing:antialiased}}
.disp{{font-family:G;font-weight:500;letter-spacing:-0.04em;line-height:0.98}}
.mono{{font-family:GM;font-weight:400;font-variant-numeric:tabular-nums}}
.spec{{font-family:GM;font-weight:500;text-transform:uppercase;letter-spacing:0.12em}}
.muted{{color:{V2_MUTED}}}
.dot{{display:inline-block;border-radius:50%;background:{AMBER};
      box-shadow:0 0 0 1px rgba(255,154,46,.35),0 0 18px rgba(255,154,46,.55)}}
"""

LOCKUP_DARK = (LOGO / "hanax-lockup-on-dark.svg").as_uri()
MARK_DARK = (LOGO / "hanax-mark-on-dark.svg").as_uri()


def render(name: str, body: str, w: int, h: int, extra_css: str = "") -> Path:
    gdir = WORK / "gfx"
    html, png = gdir / f"{name}.html", gdir / f"{name}.png"
    html.write_text(
        f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{BASE_CSS}"
        f"body{{width:{w}px;height:{h}px}}{extra_css}</style></head><body>{body}</body></html>",
        encoding="utf-8")
    run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--virtual-time-budget=1500",
         f"--window-size={w},{h}", "--default-background-color=00000000",
         f"--screenshot={png}", html.as_uri()])
    return png


def full(inner: str, bg: str = BG) -> str:
    return f"<div style='position:absolute;inset:0;background:{bg}'>{inner}</div>"


# ---------- the HX-P screen (matches brand/renders/hxp-front.png) ---------------

ROWS_ON = [("Keittiön hana", "on"), ("Liesi", "on"), ("Olohuoneen valot", "off"),
           ("Kahvinkeitin", "off")]
ROWS_OFF = [(n, "off") for n, _ in ROWS_ON]


def _pill(state: str, s: float) -> str:
    if state == "on":
        return (f"<span class='spec' style='font-size:{15*s}px;color:{AMBER_INK};"
                f"border:{1.5*s}px solid {AMBER};border-radius:999px;padding:{5*s}px {13*s}px;"
                f"display:inline-flex;align-items:center;gap:{8*s}px;"
                f"box-shadow:0 0 {14*s}px rgba(255,154,46,.25)'>"
                f"<i class='dot' style='width:{7*s}px;height:{7*s}px'></i>PÄÄLLÄ</span>")
    return (f"<span class='spec' style='font-size:{15*s}px;color:{V2_MUTED};"
            f"border:{1.5*s}px solid {LINE_STRONG};border-radius:999px;padding:{5*s}px {13*s}px'>POIS</span>")


def _check(size: float, color: str = V2_INK) -> str:
    return (f"<svg width='{size}' height='{size}' viewBox='0 0 24 24' style='flex:none'>"
            f"<path d='M4 12.5l5 5L20 6.5' stroke='{color}' stroke-width='2.4' fill='none' "
            f"stroke-linecap='round' stroke-linejoin='round'/></svg>")


def panel_screen(all_clear: bool, s: float = 1.0, clock: str = "13:56") -> str:
    """The HX-P panel as an object: graphite slab, titanium knob, amber ring when on."""
    rows = ROWS_OFF if all_clear else ROWS_ON
    if all_clear:
        head = (f"<div style='display:flex;align-items:center;gap:{12*s}px'>{_check(34*s)}"
                f"<span class='disp' style='font-size:{38*s}px;letter-spacing:-0.02em'>KAIKKI KIINNI</span></div>")
        sub = "ETEINEN · TARKISTETTU 2 S SITTEN"
    else:
        head = (f"<div style='display:flex;align-items:center;gap:{14*s}px'>"
                f"<i class='dot' style='width:{12*s}px;height:{12*s}px'></i>"
                f"<span class='disp' style='font-size:{38*s}px;letter-spacing:-0.02em'>2 PÄÄLLÄ</span></div>")
        sub = "ETEINEN · KAIKKI LAITTEET"
    rows_html = "".join(
        f"<div style='display:flex;justify-content:space-between;align-items:center;"
        f"padding:{13*s}px 0;border-top:1px solid {LINE}'>"
        f"<span><span style='display:block;font-weight:500;font-size:{22*s}px'>{n}</span>"
        f"<span class='mono muted' style='display:block;font-size:{13*s}px;margin-top:{3*s}px'>"
        f"tarkistettu {2 if all_clear else 12} s sitten</span></span>{_pill(st, s)}</div>"
        for n, st in rows)
    ring = ("" if all_clear else
            f"box-shadow:0 0 0 {3*s}px {AMBER},0 0 {30*s}px {6*s}px rgba(255,154,46,.45);")
    knob = (f"<div style='position:absolute;right:{46*s}px;top:50%;transform:translateY(-50%);"
            f"width:{118*s}px;height:{118*s}px;border-radius:50%;{ring}"
            f"background:conic-gradient(from 210deg,#6d747b,#e9edf0,#8a9198,#f4f6f7,#6d747b,#c9ced3,#6d747b);"
            f"border:{2*s}px solid #2a3036'>"
            f"<i style='position:absolute;left:50%;top:{12*s}px;width:{3*s}px;height:{26*s}px;"
            f"background:#3a4046;transform:translateX(-50%);border-radius:2px'></i></div>")
    return (f"<div style='position:relative;text-align:left;width:{900*s}px;height:{560*s}px;border-radius:{56*s}px;"
            f"background:linear-gradient(160deg,#16191d,#07080a 60%);"
            f"border:{3*s}px solid #3a4148;"
            f"box-shadow:0 1px 0 rgba(255,255,255,.12) inset,0 40px 110px rgba(0,0,0,.75)'>"
            f"<div style='position:absolute;left:{58*s}px;top:{50*s}px;width:{560*s}px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center'>{head}"
            f"<span class='mono muted' style='font-size:{17*s}px'>{clock}</span></div>"
            f"<div class='spec muted' style='font-size:{12*s}px;margin:{10*s}px 0 {18*s}px'>{sub}</div>"
            f"{rows_html}</div>{knob}</div>")


def end_card(w: int, h: int, vertical: bool = False) -> str:
    v = vertical
    return full(
        f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;"
        f"justify-content:center;text-align:center'>"
        f"<img src='{LOCKUP_DARK}' style='width:{360 if not v else 420}px'>"
        f"<div class='disp' style='font-size:{78 if not v else 84}px;margin-top:{56 if not v else 80}px'>"
        f"Lähde kotoa huoletta.</div>"
        f"<div style='margin-top:{48 if not v else 70}px;display:flex;align-items:center;gap:16px;"
        f"font-size:{28 if not v else 34}px'>"
        f"<i class='dot' style='width:10px;height:10px'></i>"
        f"<span style='font-weight:500'>Katso livenä</span>"
        f"<span class='muted'>·</span><span class='mono'>kayttis.kiirikki.fi</span></div></div>"
        f"<div class='spec muted' style='position:absolute;left:0;right:0;bottom:{170 if not v else 300}px;"
        f"text-align:center;font-size:{18 if not v else 22}px;line-height:2.1'>"
        + ("Aalto-yliopisto · Käyttäjälähtöinen tuotekehitysprojekti 2026 · Ryhmä 1<br>" if not v else
           "Aalto-yliopisto<br>Käyttäjälähtöinen tuotekehitysprojekti 2026 · Ryhmä 1<br>") +
        f"<span style='color:#6f7981'>Laitteet: konseptimalleja</span></div>")
