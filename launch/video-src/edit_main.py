"""v2 ~60 s 16:9 film ("SF deeptech"): cold open -> the everyday story -> the claim ->
the product reveal -> rewind and save -> proof -> end card.

Optional material is picked up automatically if the file exists (see EDIT_NOTES.md):
  launch/video/in/proof-kitchen.mp4      -> the proof beat (else a mono title card)
  launch/ai-studio/v1-panel-reveal.mp4   -> replaces the hxp-reveal render (P1)
  launch/ai-studio/v2-valve-rackfocus.mp4-> replaces the HX-01 LED push-in (P2)
  launch/ai-studio/v3-water-tension.mp4  -> cutaway in the second half of the tap shot (S07b)
  launch/ai-studio/v4-knob-off.mp4       -> replaces the knob-press render (K1)
"""
from __future__ import annotations

from assemble import Snd, timeline, total_len
from common import IN_DIR, ai_clip, clip
from shots import Ov, Shot

# ---- slots for material that may arrive later ---------------------------------
_proof = IN_DIR / "proof-kitchen.mp4"
proof_clip = _proof if _proof.exists() else None      # <- Friday footage drops in here
AI = {k: ai_clip(k) for k in ("v1-panel-reveal", "v2-valve-rackfocus",
                              "v3-water-tension", "v4-knob-off")}

XF = 0.25   # dissolve between product shots

SHOTS = [
    # 1. cold open: black, the indicator fades up, the readout ticks
    Shot("C0", "CARD:black", dur_override=3.0,
         overlays=[Ov("dot", 0.2, None, 1.1, 0.01), Ov("ro0", 1.0, 2.0, 0.25, 0.01),
                   Ov("ro1", 2.0, None, 0.01, 0.01)],
         note="Cold open: amber dot, 13:56:04 -> :05"),
    # 2. the everyday story
    Shot("S01", "08-09", 1.0, 3.0, gain_db=-3, xfade=0.3, note="Couch, scrolling the phone"),
    Shot("S02", "17-34", 0.3, 2.4, mode="portrait", gain_db=-3, note="Route app: bus leaves 14.00"),
    Shot("S03", "25-26", 0.5, 2.7, note="Jumps up"),
    Shot("S04", "27-39", 0.4, 2.2, gain_db=-4, note="Through the doorway"),
    Shot("S05", "29-06", 0.7, 2.9, note="Down the hallway"),
    Shot("S06", "31-48", 2.2, 5.4, note="Door slams; still frame, clock ticking"),
]
if AI["v3-water-tension"]:
    SHOTS += [Shot("S07", "35-21", 3.6, 5.6, gain_db=-2, note="Tap left running (hard cut)"),
              Shot("S07b", f"MOV:{AI['v3-water-tension']}", 1.0, 2.8, grade="soft", gain_db=-8,
                   note="AI Studio v3: water tension cutaway")]
else:
    SHOTS += [Shot("S07", "35-21", 3.6, 7.4, gain_db=-2, note="Tap left running (hard cut)")]
SHOTS += [
    Shot("S08", "36-53", 0.0, 3.2, gain_db=-3, note="Stove indicator on"),
    # 3. the claim: hard cut to black, silence
    Shot("CL", "CARD:black", dur_override=5.0,
         overlays=[Ov("claim1", 0.4, 5.0, 0.6, 0.5), Ov("claim2", 1.8, 5.0, 0.6, 0.5)],
         note="Claim: 'Tavallinen hana.' ... 'Hanax tietää, onko se auki.'"),
    # 4. the product reveal
    (Shot("P1", f"MOV:{AI['v1-panel-reveal']}", 0.5, 4.1, grade="soft", gain_db=-60, xfade=0.6,
          overlays=[Ov("lab_hxp", 1.0, None, 0.5, 0.25)], note="AI Studio v1: panel reveal")
     if AI["v1-panel-reveal"] else
     Shot("P1", "MOV:hxp-reveal.mp4", 0.8, 5.0, xfade=0.6, kb=((0.5, 0.5, 1.0), (0.505, 0.5, 0.88)),
          overlays=[Ov("lab_hxp", 1.0, None, 0.5, 0.25)],
          note="hxp-reveal render: screen on, light sweep, amber ring; slow push")),
    (Shot("P2", f"MOV:{AI['v2-valve-rackfocus']}", 1.0, 3.2, grade="soft", gain_db=-60, xfade=XF,
          overlays=[Ov("lab_hx01", 0.3, None, 0.4, 0.2)], note="AI Studio v2: valve rack focus")
     if AI["v2-valve-rackfocus"] else
     Shot("P2", "STILL:hx01-macro-led.png", dur_override=2.0, xfade=XF,
          kb=((0.52, 0.48, 0.86), (0.565, 0.43, 0.6)),
          overlays=[Ov("lab_hx01", 0.3, None, 0.4, 0.2)], note="HX-01 LED macro, push-in")),
    Shot("P3", "STILL:hxp-knob-macro.png", dur_override=1.9, xfade=XF,
         kb=((0.55, 0.52, 0.72), (0.575, 0.5, 0.56)),
         overlays=[Ov("lab_hxp", 0.2, None, 0.3, 0.2)], note="HX-P knob macro, push-in"),
    Shot("P4", "STILL:hx01-exploded.png", dur_override=2.3, xfade=XF,
         kb=((0.47, 0.46, 1.0), (0.47, 0.455, 0.92)),
         overlays=[Ov("lab_hx01", 0.3, None, 0.3, 0.2)], note="HX-01 exploded view, labels"),
    Shot("P5", "MOV:hx01-turntable.mp4", 0.0, 2.2, xfade=XF, kb=((0.5, 0.48, 0.78), (0.5, 0.48, 0.7)),
         overlays=[Ov("lab_hx01", 0.2, None, 0.3, 0.2)], note="HX-01 turntable"),
    Shot("P6", "STILL:family.png", dur_override=2.4, xfade=XF,
         kb=((0.45, 0.43, 0.8), (0.45, 0.44, 0.9)),
         overlays=[Ov("lab_fam", 0.3, None, 0.4, 0.3)], note="Family, slow pull-out"),
    # 5. rewind and save
    Shot("R1", "29-06", 0.7, 2.9, speed=4, reverse=True, gain_db=-60, note="Rewind"),
    Shot("R2", "27-39", 0.4, 2.2, speed=4, reverse=True, gain_db=-60, note="Rewind"),
    Shot("R3", "25-26", 0.5, 2.7, speed=4, reverse=True, gain_db=-60, note="Rewind"),
    Shot("R4", "08-09", 1.0, 3.2, overlays=[Ov("rewind", 0.0, None, 0.2, 0.3)], gain_db=-6,
         note="Same moment, now with Hanax"),
    Shot("U1", "CARD:panel_on", dur_override=2.2, note="HX-P UI: 2 PÄÄLLÄ"),
    (Shot("K1", f"MOV:{AI['v4-knob-off']}", 0.5, 2.9, grade="soft", gain_db=-4,
          note="AI Studio v4: knob press")
     if AI["v4-knob-off"] else
     Shot("K1", "STILL:hxp-knob-macro.png", dur_override=2.3, variant="ring_off", mix=(0.95, 1.45),
          kb=((0.655, 0.5, 0.70), (0.655, 0.5, 0.66)),
          note="Knob press: amber ring fades out")),
    Shot("T1", "34-29", 0.6, 2.3, note="Tap off"),
    Shot("T2", "48-40", 0.8, 3.0, note="Stove off"),
    Shot("U2", "CARD:panel_off", dur_override=2.2, xfade=0.3, note="HX-P UI: KAIKKI KIINNI ✓"),
    # 6. proof
    (Shot("PF", f"MOV:{proof_clip}", 0.0, 4.0, grade="soft", gain_db=-6, xfade=0.4,
          overlays=[Ov("proof_label", 0.2, None, 0.3, 0.3)], note="Proof: live in the guild kitchen")
     if proof_clip else
     Shot("PF", "CARD:proof", dur_override=3.6, xfade=0.4,
          note="Proof card (slot: launch/video/in/proof-kitchen.mp4)")),
    # 7. end card
    Shot("E", "CARD:end", dur_override=4.6, xfade=0.6, note="End card"),
]

_IDX = {s.id: i for i, s in enumerate(SHOTS)}


def at(shot_id: str, rel: float) -> float:
    return timeline(SHOTS)[_IDX[shot_id]] + rel


def end_of(shot_id: str) -> float:
    return at(shot_id, SHOTS[_IDX[shot_id]].dur)


def captions():
    return [
        (at("S02", 0.15), at("S02", 2.0), "Bussi lähtee 14.00."),
        (at("S03", 0.3), at("S03", 2.1), "Nyt tulee kiire."),
        (at("S06", 1.1), at("S06", 2.9), "[ovi paukahtaa · kello tikittää]"),
        (at("S07", 0.6), at("S07", 3.0), "Hana jäi auki."),
        (at("S08", 0.3), at("S08", 2.9), "Liesi jäi päälle."),
        (at("K1", 0.3), at("K1", 2.1), "Yksi painallus: kaikki pois."),
        (at("T1", 0.3), at("T1", 1.6), "Hana kiinni."),
        (at("T2", 0.3), at("T2", 2.0), "Liesi pois."),
    ]


def card_texts():
    return [
        (at("C0", 1.0), at("C0", 3.0), "13:56:04"),
        (at("CL", 0.4), at("CL", 5.0), "Tavallinen hana. Hanax tietää, onko se auki."),
        (at("P1", 1.0), end_of("P1"), "HX-P · PANEELI · PAINA: KAIKKI POIS"),
        (at("P2", 0.3), end_of("P2"), "HX-01 · ANTURI · KONSEPTIMALLI"),
        (at("P6", 0.3), end_of("P6"), "HX-01 + HX-P · KONSEPTIMALLEJA"),
        (at("R4", 0.0), end_of("R4"), "13:56:04 — Sama hetki. Nyt eteisessä on Hanax."),
        (at("U1", 0.0), end_of("U1"), "[HX-P: 2 PÄÄLLÄ — Keittiön hana PÄÄLLÄ, Liesi PÄÄLLÄ]"),
        (at("U2", 0.0), end_of("U2"), "[HX-P: KAIKKI KIINNI ✓ — tarkistettu 2 s sitten]"),
        (at("PF", 0.0), end_of("PF"), "LIVENÄ KILLAN KEITTIÖSSÄ · RASPBERRY PI · 2 KAHVINKEITINTÄ · "
                                      "VALOT · HANAN VENTTIILI"),
        (at("E", 0.0), end_of("E"), "hanax — Lähde kotoa huoletta. Katso livenä · kayttis.kiirikki.fi · "
                                    "Aalto-yliopisto · Käyttäjälähtöinen tuotekehitysprojekti 2026 · Ryhmä 1 · "
                                    "Laitteet: konseptimalleja"),
    ]


def sounds(assets):
    total = total_len(SHOTS)
    slam = at("S06", 1.0)
    cut_black = at("CL", 0.0)
    snd = [
        # the clock: on the readout, a whisper under the story, loud after the slam
        Snd(assets["tick"], at("C0", 0.98), 2.02, -6, 0.02, 0.05),
        Snd(assets["tick"], at("S01", 0.0), slam - at("S01", 0.0), -22, 0.3, 0.1, offset=0.0),
        Snd(assets["tick"], slam + 0.05, cut_black - slam - 0.05, -5, 0.05, 0.02),
        Snd(assets["drone"], slam + 0.6, cut_black - slam - 0.6, -15, 2.5, 0.02),
        # water creeps in before the hard cut to the tap (J-cut)
        Snd(clip("35-21"), at("S07", 0) - 1.8, 1.8, -7, 1.8, 0.05, offset=1.8),
        # the reveal: a low hum from the second claim line to the end of the reveal
        Snd(assets["hum"], at("CL", 1.8), end_of("P6") - at("CL", 1.8), -17, 2.0, 0.6),
        Snd(assets["rewind"], at("R1", 0.0), at("R4", 0.15) - at("R1", 0.0), 0, 0.1, 0.2),
        Snd(assets["pad"], at("K1", 1.0), total - at("K1", 1.0), -19, 1.5, 2.5),
    ]
    if not AI["v4-knob-off"]:
        snd.append(Snd(assets["click"], at("K1", 0.95), 0.6, -4, 0.0, 0.1))
    return snd
