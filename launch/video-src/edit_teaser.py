"""v2 ~20 s 9:16 teaser: hook (tap, stove, the rush) -> the claim -> the panel reveal ->
knob press -> things off -> KAIKKI KIINNI -> end card.

Optional (picked up if present): launch/ai-studio/v1-panel-reveal-9x16.mp4 replaces the
panel render (V05); launch/ai-studio/v4-knob-off.mp4 replaces the knob render (V06)."""
from __future__ import annotations

from assemble import Snd, timeline, total_len
from common import ai_clip, clip
from shots import Ov, Shot
from vo import Cue, check_no_overlap, sfx

AI_V1 = ai_clip("v1-panel-reveal-9x16")
AI_V4 = ai_clip("v4-knob-off")

SHOTS = [
    Shot("V01", "35-21", 5.2, 7.2, mode="v_crop", cx=0.47, gain_db=-2, note="Tap running (hook)"),
    Shot("V02", "36-53", 0.0, 1.8, mode="v_crop", cx=0.58, gain_db=-3, note="Stove indicator on"),
    Shot("V03", "29-06", 1.2, 2.8, mode="v_frame", note="Runs to the door"),
    Shot("V04", "CARD:v_black", dur_override=4.2,
         overlays=[Ov("v_claim1", 0.3, 4.2, 0.5, 0.4), Ov("v_claim2", 1.8, 4.2, 0.5, 0.4)],
         note="Claim"),
    (Shot("V05", f"MOV:{AI_V1}", 0.5, 3.1, grade="soft", gain_db=-60, xfade=0.4,
          overlays=[Ov("v_lab_hxp", 0.6, None, 0.4, 0.2)], note="AI Studio v1 (9:16): panel reveal")
     if AI_V1 else
     Shot("V05", "MOV:hxp-reveal.mp4", 2.4, 5.0, mode="v_fit", xfade=0.4,
          overlays=[Ov("v_lab_hxp", 0.6, None, 0.4, 0.2)], note="hxp-reveal render on black")),
    (Shot("V06", f"MOV:{AI_V4}", 0.5, 2.5, mode="v_crop", cx=0.5, grade="soft", gain_db=-4,
          overlays=[Ov("v_lab_knob", 0.2, None, 0.3, 0.2)], note="AI Studio v4: knob press")
     if AI_V4 else
     Shot("V06", "STILL:hxp-knob-macro.png", dur_override=2.0, variant="ring_off", mix=(0.8, 1.3),
          kb=((0.6, 0.5, 0.36), (0.6, 0.5, 0.32)),
          overlays=[Ov("v_lab_knob", 0.2, None, 0.3, 0.2)], note="Knob press: amber ring fades out")),
    Shot("V07", "34-29", 0.6, 2.1, mode="v_crop", cx=0.5, note="Tap off"),
    Shot("V08", "48-40", 0.9, 2.9, mode="v_crop", cx=0.62, note="Stove off"),
    Shot("V09", "CARD:v_panel_off", dur_override=1.7, xfade=0.25, note="KAIKKI KIINNI ✓"),
    Shot("V10", "CARD:v_end", dur_override=3.8, xfade=0.5, note="End card"),
]
_IDX = {s.id: i for i, s in enumerate(SHOTS)}


def at(shot_id, rel):
    return timeline(SHOTS)[_IDX[shot_id]] + rel


def end_of(shot_id):
    return at(shot_id, SHOTS[_IDX[shot_id]].dur)


def captions():
    return [
        (at("V01", 0.3), at("V01", 1.9), "Hana jäi auki."),
        (at("V02", 0.1), at("V02", 1.7), "Liesi jäi päälle."),
        (at("V03", 0.1), at("V03", 1.5), "Ja bussi lähtee."),
        (at("V07", 0.2), at("V07", 1.4), "Hana kiinni."),
        (at("V08", 0.2), at("V08", 1.9), "Liesi pois."),
    ]


def card_texts():
    return [
        (at("V04", 0.3), end_of("V04"), "Tavallinen hana. Hanax tietää, onko se auki."),
        (at("V05", 0.6), end_of("V05"), "HX-P · PANEELI · KONSEPTIMALLI"),
        (at("V06", 0.2), end_of("V06"), "PAINA: KAIKKI POIS"),
        (at("V09", 0.0), end_of("V09"), "[HX-P: KAIKKI KIINNI ✓]"),
        (at("V10", 0.0), end_of("V10"), "hanax — Lähde kotoa huoletta. Katso livenä · kayttis.kiirikki.fi · "
                                        "Aalto-yliopisto · Käyttäjälähtöinen tuotekehitysprojekti 2026 · Ryhmä 1 · "
                                    "Laitteet: konseptimalleja"),
    ]


KNOB_PRESS = 0.8   # V06-relative (ring-off crossfade starts here)


def vo_cues():
    # vo3 shortened at its sentence boundaries: "Tavallinen hana." ... "Mutta Hanax tietää, onko se auki."
    cues = [Cue("vo3a", at("V04", 0.35)), Cue("vo3c", at("V04", 1.9)), Cue("vo7", at("V10", 0.4))]
    check_no_overlap(cues)
    return cues


def sfx_cues():
    c = [(0.0, "water-run", "water under the tap hook"),
         (at("V04", 0.3), "impact-low", "under the first claim card"),
         (at("V06", KNOB_PRESS), "knob-detent", "knob press"),
         (at("V08", 0.9), "stove-click", "stove off"),
         (at("V09", 0.15), "confirm", "KAIKKI KIINNI")]
    return [x for x in c if not (AI_V4 and x[1] == "knob-detent")]


def sounds(assets):
    total = total_len(SHOTS)
    claim = at("V04", 0.0)
    snd = [
        Snd(sfx("water-run"), 0.0, at("V02", 0.3), -6, 0.05, 0.3),
        Snd(sfx("impact-low"), at("V04", 0.3), 3.0, -19, 0.0, 0.8),
        Snd(sfx("stove-click"), at("V08", 0.9), 1.0, -4, 0.0, 0.1),
        Snd(sfx("confirm"), at("V09", 0.15), 2.0, -3, 0.0, 0.4),
        Snd(assets["tick"], 0.0, claim, -8, 0.3, 0.02),
        Snd(assets["drone"], 0.0, claim, -17, 1.0, 0.02),
        Snd(assets["hum"], at("V04", 1.8), at("V06", 1.0) - at("V04", 1.8), -17, 1.5, 0.4),
        Snd(assets["pad"], at("V06", 1.0), total - at("V06", 1.0), -18, 1.2, 2.0),
    ]
    if not AI_V4:
        snd.append(Snd(sfx("knob-detent"), at("V06", KNOB_PRESS) - 0.695, 1.4, 24, 0.0, 0.2))
        snd.append(Snd(assets["click"], at("V06", KNOB_PRESS), 0.6, -10, 0.0, 0.1))
    return snd + [c.snd() for c in vo_cues()]
