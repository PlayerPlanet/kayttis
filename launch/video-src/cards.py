"""All text cards for the 16:9 main video and the 9:16 teaser.

Title-safe: 16:9 keeps text >=150 px from the sides and >=100 px from top/bottom;
9:16 keeps >=90 px from the sides, >=240 px from the top and >=400 px from the
bottom (room for social-app UI)."""
from __future__ import annotations

from common import INK, PAPER, D_MUTED
from gfx import all_clear_chip, end_card, panel_card, render

W, H = 1920, 1080
VW, VH = 1080, 1920

ON_ROWS = [("Keittiön hana", "on"), ("Liesi", "on"), ("Valot", "off")]


def build_cards() -> dict[str, str]:
    c = {}
    # 1. small time readout on the calm opening
    c["clock1352"] = render("clock1352", (
        "<div class='mono shade' style='position:absolute;left:150px;top:100px;font-size:60px'>13<span class=c>:</span>52</div>"),
        W, H)
    # 2. clock beat over the defocused microwave
    c["readout1356"] = render("readout1356", (
        f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;"
        f"justify-content:center'>"
        f"<div class='mono shade' style='font-size:250px;line-height:1'>13<span class=c>:</span>56</div>"
        f"<div class='shade' style='font-weight:600;font-size:60px;margin-top:26px'>Bussi lähtee 14.00.</div>"
        f"</div>"), W, H)
    # 3. problem, stated once
    c["problem"] = render("problem", (
        f"<div style='position:absolute;inset:0;background:rgba(15,28,36,.86)'></div>"
        f"<div style='position:absolute;left:150px;right:150px;top:0;bottom:0;display:flex;"
        f"flex-direction:column;justify-content:center'>"
        f"<div class='disp' style='font-size:120px'>Jäikö jotain päälle?</div>"
        f"<div style='font-size:46px;line-height:1.35;margin-top:36px;color:{PAPER};max-width:1300px'>"
        f"Ovelta sitä ei näe. Auki jäänyt hana tai päälle jäänyt liesi huomataan usein vasta myöhään.</div>"
        f"</div>"), W, H)
    # 4. rewind / second take
    c["rewind"] = render("rewind", (
        f"<div style='position:absolute;inset:0;background:rgba(15,28,36,.45)'></div>"
        f"<div style='position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;"
        f"justify-content:center'>"
        f"<div class='mono shade' style='font-size:180px;line-height:1'>13<span class=c>:</span>56</div>"
        f"<div class='disp shade' style='font-size:76px;margin-top:30px'>Sama hetki. Nyt kotona on Hanax.</div>"
        f"</div>"), W, H)
    # 5. the solution: title + state panel (state rule: amber = PÄÄLLÄ, with text)
    c["hanax"] = render("hanax", (
        f"<div style='position:absolute;inset:0;background:linear-gradient(to top,rgba(15,28,36,.78) 0%,"
        f"rgba(15,28,36,.45) 28%,rgba(15,28,36,0) 50%)'></div>"
        f"<div style='position:absolute;right:150px;top:120px'>"
        f"{panel_card(ON_ROWS, '2 asiaa päällä', 'Tarkistettu 2 s sitten')}</div>"
        f"<div class='disp shade' style='position:absolute;left:150px;bottom:110px;font-size:84px;"
        f"max-width:1000px'>Hanax kertoo ennen kuin lähdet.</div>"), W, H)
    # 6. resolved state
    c["allclear"] = render("allclear", (
        f"<div style='position:absolute;left:150px;top:110px'>{all_clear_chip(1.0)}</div>"), W, H)
    # 7. value proposition over the calm exit
    c["value"] = render("value", (
        f"<div style='position:absolute;inset:0;background:linear-gradient(to bottom,rgba(15,28,36,.72) 0%,"
        f"rgba(15,28,36,.5) 30%,rgba(15,28,36,0) 55%)'></div>"
        f"<div style='position:absolute;left:150px;top:100px;max-width:1100px'>"
        f"<div class='disp shade' style='font-size:92px'>Yksi vilkaisu riittää.</div>"
        f"<div class='shade' style='font-weight:600;font-size:44px;line-height:1.3;margin-top:22px'>"
        f"Näet eteisen paneelista ja puhelimesta, jäikö hana, liesi tai valot päälle.</div></div>"),
        W, H)
    c["end"] = render("end", end_card(W, H), W, H)

    # ---------------- 9:16 teaser ----------------
    c["v_hook"] = render("v_hook", (
        f"<div class='disp shade' style='position:absolute;left:90px;right:90px;top:250px;"
        f"font-size:118px;text-align:center'>Jäikö jotain päälle?</div>"), VW, VH)
    c["v_bus"] = render("v_bus", (
        f"<div style='position:absolute;inset:0;background:linear-gradient(to top,rgba(15,28,36,0) 20%,rgba(15,28,36,.6) 42%,rgba(15,28,36,0) 62%)'></div>"
        f"<div style='position:absolute;left:0;right:0;top:1060px;text-align:center'>"
        f"<div class='mono shade' style='font-size:150px;line-height:1'>13<span class=c>:</span>56</div>"
        f"<div class='shade' style='font-weight:600;font-size:52px;margin-top:20px'>Bussi lähtee 14.00.</div>"
        f"</div>"), VW, VH)
    c["v_hanax"] = render("v_hanax", (
        f"<div style='position:absolute;inset:0;background:linear-gradient(to bottom,rgba(15,28,36,.8) 0%,"
        f"rgba(15,28,36,.55) 22%,rgba(15,28,36,0) 40%)'></div>"
        f"<div class='disp shade' style='position:absolute;left:90px;right:90px;top:250px;"
        f"font-size:96px;text-align:center'>Hanax kertoo ennen kuin lähdet.</div>"
        f"<div style='position:absolute;left:50%;transform:translateX(-50%);top:820px;zoom:1.0'><div style='transform:scale(1.4);transform-origin:top center'>"
        f"{panel_card(ON_ROWS, '2 asiaa päällä', 'Tarkistettu 2 s sitten', 600)}</div></div>"),
        VW, VH, extra_css="")
    c["v_allclear"] = render("v_allclear", (
        f"<div style='position:absolute;left:0;right:0;top:270px;text-align:center'>"
        f"{all_clear_chip(1.25)}</div>"), VW, VH)
    c["v_end"] = render("v_end", end_card(VW, VH, vertical=True), VW, VH)
    return c


if __name__ == "__main__":
    from common import ensure_dirs
    ensure_dirs()
    for k, v in build_cards().items():
        print(k, v.name)
