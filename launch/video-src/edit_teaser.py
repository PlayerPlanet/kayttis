"""~20 s 9:16 teaser: hook (tap, stove) -> 'Jäikö jotain päälle?' -> rush ->
app reveal -> things off -> end card. Close-ups are 9:16 crops of the 16:9
footage; wide shots sit framed over a soft fill; the portrait clip is native."""
from __future__ import annotations

from assemble import Snd, timeline, total_len
from shots import Ov, Shot

SHOTS = [
    Shot("T01", "35-21", 6.0, 8.3, mode="v_crop", cx=0.47,
         overlays=[Ov("v_hook", 0.2, None, 0.3, 0.01)], note="Tap running (hook)"),
    Shot("T02", "36-53", 0.0, 2.0, mode="v_crop", cx=0.58,
         overlays=[Ov("v_hook", 0.0, None, 0.01, 0.25)], gain_db=-3, note="Stove indicator on"),
    Shot("T03", "17-34", 0.3, 2.0, mode="v_native", overlays=[Ov("v_bus", 0.1, None, 0.2, 0.15)],
         gain_db=-3, note="Route app: bus 14.00 (native portrait clip)"),
    Shot("T04", "29-06", 1.2, 3.2, mode="v_frame", note="Runs to the door"),
    Shot("T05", "44-27", 0.0, 2.3, speed=0.8, mode="v_crop", cx=0.42,
         overlays=[Ov("v_hanax", 0.1, None, 0.3, 0.15)], gain_db=-3, note="Hanax app reveal"),
    Shot("T06", "34-29", 0.6, 2.8, mode="v_crop", cx=0.5, note="Tap off"),
    Shot("T07", "48-40", 0.8, 3.36, mode="v_crop", cx=0.62,
         overlays=[Ov("v_allclear", 1.3, None, 0.3, 0.01)], note="Stove off; KAIKKI KIINNI"),
    Shot("T08", "50-01", 0.0, 2.6, mode="v_crop", cx=0.5,
         overlays=[Ov("v_allclear", 0.0, 1.2, 0.01, 0.3)], gain_db=-2, note="Walks out calmly"),
    Shot("T09", "CARD:v_end", dur_override=3.0, xfade=0.5, note="End card"),
]
_IDX = {s.id: i for i, s in enumerate(SHOTS)}


def at(shot_id, rel):
    return timeline(SHOTS)[_IDX[shot_id]] + rel


def captions():
    return [
        (at("T01", 0.5), at("T01", 2.2), "Hana jäi auki."),
        (at("T02", 0.1), at("T02", 1.9), "Liesi jäi päälle."),
        (at("T04", 0.1), at("T04", 1.9), "Ja bussi lähtee."),
        (at("T06", 0.6), at("T06", 2.1), "Hana kiinni."),
        (at("T07", 0.2), at("T07", 2.4), "Liesi pois."),
        (at("T08", 0.2), at("T08", 2.4), "Ehdit bussiin."),
    ]


def card_texts():
    return [
        (at("T01", 0.2), at("T02", 2.0), "Jäikö jotain päälle?"),
        (at("T03", 0.1), at("T03", 1.7), "13:56 — Bussi lähtee 14.00."),
        (at("T05", 0.1), at("T05", SHOTS[_IDX['T05']].dur),
         "Hanax kertoo ennen kuin lähdet. [Kotipaneeli: 2 asiaa päällä — Keittiön hana PÄÄLLÄ, "
         "Liesi PÄÄLLÄ, Valot POIS]"),
        (at("T07", 1.3), at("T08", 1.2), "KAIKKI KIINNI · tarkistettu 2 s sitten"),
        (at("T09", 0.0), at("T09", 3.0), "hanax — Lähde kotoa huoletta. Näet yhdellä vilkaisulla, jäikö "
                                         "hana, liesi tai valot päälle. kayttis.kiirikki.fi"),
    ]


def sounds(assets):
    total = total_len(SHOTS)
    return [
        Snd(assets["tick"], 0.0, at("T05", 0.0), -9, 0.3, 0.3),
        Snd(assets["pad"], at("T05", 0.0), total - at("T05", 0.0), -15, 1.0, 2.0),
    ]
