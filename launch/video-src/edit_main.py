"""~60 s 16:9 main video: shot list, captions, sound design."""
from __future__ import annotations

from assemble import Snd, timeline, total_len
from common import WORK, clip
from shots import Ov, Shot

SHOTS = [
    # 1. calm moment
    Shot("M01", "08-09", 0.3, 3.1, overlays=[Ov("clock1352", 0.2, 2.6)], gain_db=-2,
         note="Lying on bean bags, scrolling the phone"),
    Shot("M02", "08-09", 8.2, 10.4, gain_db=-2, note="Over-the-shoulder: phone"),
    # 2. the bus is leaving
    Shot("M03", "17-34", 0.3, 2.7, mode="portrait", gain_db=-2,
         note="Portrait POV: route app, bus 25 leaves 14.00"),
    Shot("M04", "23-14", 0.2, 3.1, defocus_at=1.1, overlays=[Ov("readout1356", 1.15, None, 0.25, 0.15)],
         note="Whip to the clock; defocus under the 13:56 readout (hides the real 14:31)"),
    # 3. rush out
    Shot("M05", "25-26", 0.5, 3.8, note="Jumps up"),
    Shot("M06", "27-39", 0.4, 3.0, gain_db=-4, note="Runs through the doorway"),
    Shot("M07", "29-06", 0.7, 3.4, note="Runs down the hallway to the front door"),
    Shot("M08", "31-48", 2.2, 7.2, note="Door slams; still frame, clock ticking"),
    # 4. the disaster
    Shot("M09", "35-21", 3.6, 8.4, xfade=0.4, gain_db=-2, note="Tap left running"),
    Shot("M10", "36-53", 0.0, 5.8, overlays=[Ov("problem", 3.2, None, 0.4, 0.2)], gain_db=-3,
         note="Stove indicator on; problem card"),
    # rewind (script: 'videon kelaus alkuun')
    Shot("R1", "29-06", 0.7, 3.4, speed=4, reverse=True, gain_db=-60, note="Rewind"),
    Shot("R2", "27-39", 0.4, 3.0, speed=4, reverse=True, gain_db=-60, note="Rewind"),
    Shot("R3", "25-26", 0.5, 3.8, speed=4, reverse=True, gain_db=-60, note="Rewind"),
    Shot("M11", "08-09", 1.0, 3.2, overlays=[Ov("rewind", 0.0, None, 0.2, 0.2)], gain_db=-4,
         note="Back on the bean bags: same moment, now with Hanax"),
    # 5. Hanax
    Shot("M12", "29-06", 0.9, 3.4, note="Runs to the door again"),
    Shot("M13", "44-27", 0.0, 2.3, speed=0.75, overlays=[Ov("hanax", 0.15, None, 0.3, 0.2)],
         gain_db=-3, note="Hanax app: things left on; title + state panel"),
    # 6. back, turn things off
    Shot("M14", "29-06", 4.2, 5.43, note="Turns back at the door"),
    Shot("M15", "34-29", 0.6, 3.0, note="Turns the tap off"),
    Shot("M16", "48-40", 0.6, 3.36, overlays=[Ov("allclear", 1.5, None, 0.3, 0.01)],
         note="Turns the stove off; KAIKKI KIINNI"),
    Shot("M17", "46-16", 3.0, 5.3, overlays=[Ov("allclear", 0.0, 1.6, 0.01, 0.3)],
         note="Closes the door calmly"),
    # 7. leave calmly
    Shot("M18", "50-01", 0.0, 5.0, xfade=0.5, overlays=[Ov("value", 0.6, 4.9, 0.4, 0.4)],
         gain_db=-2, note="Walks out to campus; value proposition"),
    # 8. end card
    Shot("M19", "CARD:end", dur_override=4.0, xfade=0.6, note="End card"),
]

_IDX = {s.id: i for i, s in enumerate(SHOTS)}


def at(shot_id: str, rel: float) -> float:
    return timeline(SHOTS)[_IDX[shot_id]] + rel


# burned-in captions (lower third)
def captions():
    return [
        (at("M03", 0.15), at("M03", 2.3), "Bussi lähtee Kotikadulta 14.00."),
        (at("M05", 0.4), at("M05", 2.9), "Nyt tulee kiire."),
        (at("M08", 1.2), at("M08", 3.3), "[ovi paukahtaa · kello tikittää]"),
        (at("M08", 3.5), at("M09", 0.6), "[veden lorinaa]"),
        (at("M09", 0.8), at("M09", 4.5), "Hana jäi auki."),
        (at("M10", 0.3), at("M10", 3.0), "Liesi jäi päälle."),
        (at("M14", 0.0), at("M15", 1.1), "Kaksi asiaa päällä. Ehdit vielä."),
        (at("M15", 1.3), at("M15", 2.35), "Hana kiinni."),
        (at("M16", 0.3), at("M16", 2.7), "Liesi pois."),
        (at("M17", 0.2), at("M17", 2.2), "Nyt voi lähteä."),
    ]


# text that is part of graphics (for the .srt / accessibility and the notes)
def card_texts():
    return [
        (at("M01", 0.2), at("M01", 2.6), "13:52"),
        (at("M04", 1.15), at("M04", 2.9), "13:56 — Bussi lähtee 14.00."),
        (at("M10", 3.2), at("M10", 5.8), "Jäikö jotain päälle? Ovelta sitä ei näe. Auki jäänyt hana tai "
                                         "päälle jäänyt liesi huomataan usein vasta myöhään."),
        (at("M11", 0.0), at("M11", 2.2), "13:56 — Sama hetki. Nyt kotona on Hanax."),
        (at("M13", 0.15), at("M13", SHOTS[_IDX['M13']].dur),
         "Hanax kertoo ennen kuin lähdet. [Kotipaneeli: 2 asiaa päällä — Keittiön hana PÄÄLLÄ, "
         "Liesi PÄÄLLÄ, Valot POIS]"),
        (at("M16", 1.5), at("M17", 1.6), "KAIKKI KIINNI · tarkistettu 2 s sitten"),
        (at("M18", 0.6), at("M18", 4.9), "Yksi vilkaisu riittää. Näet eteisen paneelista ja puhelimesta, "
                                         "jäikö hana, liesi tai valot päälle."),
        (at("M19", 0.0), at("M19", 4.0), "hanax — Lähde kotoa huoletta. kayttis.kiirikki.fi · "
                                         "Aalto-yliopisto · Käytettävyys 2026 · Ryhmä 1"),
    ]


def sounds(assets):
    total = total_len(SHOTS)
    slam = at("M08", 1.0)
    end_tension = at("R1", 0.0)
    pad_start = at("M13", 0.0)
    return [
        # quiet tick under the clock beat, the louder tick after the door slam
        Snd(assets["tick"], at("M04", 1.0), 2.0, -14, 0.3, 0.4),
        Snd(assets["tick"], slam + 0.05, end_tension - slam - 0.05, -4, 0.05, 0.25),
        Snd(assets["drone"], slam + 0.6, end_tension - slam - 0.6, -15, 2.5, 0.3),
        # water creeps in before the cut to the tap (J-cut)
        Snd(clip("35-21"), at("M09", 0) - 2.2, 2.2, -6, 2.2, 0.05, offset=1.4),
        Snd(assets["rewind"], at("R1", 0.0), at("M11", 0.15) - at("R1", 0.0), 0, 0.1, 0.2),
        Snd(assets["pad"], pad_start, total - pad_start, -17, 2.0, 2.5),
    ]
