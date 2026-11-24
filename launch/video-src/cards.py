"""v2 text cards and overlays for the 16:9 film and the 9:16 teaser.

16:9 has a 2.39:1 letterbox (138 px bars), so all text sits inside y 138..942 and
>=150 px from the sides. 9:16 keeps >=90 px from the sides, >=240 px from the top and
>=400 px from the bottom (social-app UI)."""
from __future__ import annotations

from common import LB_BAR, LINE_STRONG, V2_MUTED
from gfx import end_card, full, panel_screen, render

W, H = 1920, 1080
VW, VH = 1080, 1920


def _center(inner: str, top: str = "0", bottom: str = "0") -> str:
    return (f"<div style='position:absolute;left:0;right:0;top:{top};bottom:{bottom};display:flex;"
            f"flex-direction:column;align-items:center;justify-content:center;text-align:center'>{inner}</div>")


def _label(text: str, w: int, h: int, left: int, bottom: int, size: int = 19) -> str:
    """Lower-left spec label: hairline + Geist Mono caps (no colour)."""
    return (f"<div style='position:absolute;left:{left}px;bottom:{bottom}px;display:flex;align-items:center;"
            f"gap:16px'><i style='width:28px;height:1px;background:{LINE_STRONG}'></i>"
            f"<span class='spec' style='font-size:{size}px;color:#c9ced3'>{text}</span></div>")


def _claim(line: int, size: int, gap: int, vertical: bool) -> str:
    l1 = (f"<div class='disp' style='font-size:{size}px;color:{V2_MUTED};"
          f"opacity:{1 if line == 1 else 0}'>Tavallinen hana.</div>")
    l2_txt = "Hanax tietää,<br>onko se auki." if vertical else "Hanax tietää, onko se auki."
    l2 = (f"<div class='disp' style='font-size:{size}px;margin-top:{gap}px;"
          f"opacity:{1 if line == 2 else 0}'>{l2_txt}</div>")
    return _center(l1 + l2)


LAB_HX01 = "HX-01 · ANTURI · KONSEPTIMALLI"
LAB_HXP = "HX-P · PANEELI · PAINA: KAIKKI POIS"
LAB_FAM = "HX-01 + HX-P · KONSEPTIMALLEJA"
PROOF_1 = "LIVENÄ KILLAN KEITTIÖSSÄ"
PROOF_2 = "RASPBERRY PI · 2 KAHVINKEITINTÄ · VALOT · HANAN VENTTIILI"


def build_cards() -> None:
    lb = LB_BAR
    render("black", full(""), W, H)
    render("v_black", full(""), VW, VH)
    # ---- cold open: the indicator, then the readout ticking --------------------
    render("dot", _center("<i class='dot' style='width:16px;height:16px;"
                          "box-shadow:0 0 0 1px rgba(255,154,46,.4),0 0 40px 8px rgba(255,154,46,.35)'></i>",
                          bottom="120px"), W, H)
    for i, sec in enumerate(("04", "05", "06", "07")):
        render(f"ro{i}", _center(f"<div class='mono' style='font-size:44px;letter-spacing:0.08em;"
                                 f"color:#e8ecef'>13:56:{sec}</div>", top="120px"), W, H)
    # ---- the claim -----------------------------------------------------------
    render("claim1", _claim(1, 92, 26, False), W, H)
    render("claim2", _claim(2, 92, 26, False), W, H)
    # ---- product labels (lower-left, inside the letterbox) ---------------------
    for k, t in (("lab_hx01", LAB_HX01), ("lab_hxp", LAB_HXP), ("lab_fam", LAB_FAM)):
        render(k, _label(t, W, H, 150, lb + 50), W, H)
    # ---- rewind: same moment ---------------------------------------------------
    render("rewind", (
        "<div style='position:absolute;inset:0;background:rgba(10,12,14,.55)'></div>"
        + _center("<div class='mono' style='font-size:44px;letter-spacing:0.08em'>13:56:04</div>"
                  "<div class='disp' style='font-size:64px;margin-top:26px'>"
                  "Sama hetki. Nyt eteisessä on Hanax.</div>")), W, H)
    # ---- HX-P UI: before / after ----------------------------------------------
    render("panel_on", full(_center(panel_screen(False, 1.12)))
           + _label("HX-P · ETEINEN · 13:56", W, H, 150, lb + 40), W, H)
    render("panel_off", full(_center(panel_screen(True, 1.12, "13:57")))
           + _label("HX-P · ETEINEN · 13:57", W, H, 150, lb + 40), W, H)
    # ---- proof ---------------------------------------------------------------
    render("proof", full(_center(
        "<div style='display:flex;align-items:center;gap:18px'><i class='dot' style='width:12px;height:12px'></i>"
        f"<span class='spec' style='font-size:22px;color:{V2_MUTED}'>Todiste</span></div>"
        f"<div class='spec' style='font-size:46px;letter-spacing:0.08em;margin-top:34px'>{PROOF_1}</div>"
        f"<div style='width:880px;height:1px;background:#2a3036;margin:34px 0'></div>"
        f"<div class='spec' style='font-size:23px;color:#c9ced3'>{PROOF_2}</div>")), W, H)
    render("proof_label", _label("LIVENÄ · KILLAN KEITTIÖ · LEIKKAAMATON", W, H, 150, lb + 40), W, H)
    render("end", end_card(W, H), W, H)

    # ---------------- 9:16 teaser ----------------
    render("v_claim1", _claim(1, 96, 30, True), VW, VH)
    render("v_claim2", _claim(2, 96, 30, True), VW, VH)
    render("v_lab_hxp", _label("HX-P · PANEELI · KONSEPTIMALLI", VW, VH, 90, 470, 22), VW, VH)
    render("v_lab_knob", _label("PAINA: KAIKKI POIS", VW, VH, 90, 470, 22), VW, VH)
    render("v_panel_off", full(_center(panel_screen(True, 0.98, "13:57"))), VW, VH)
    render("v_end", end_card(VW, VH, vertical=True), VW, VH)


if __name__ == "__main__":
    from common import ensure_dirs
    ensure_dirs()
    build_cards()
