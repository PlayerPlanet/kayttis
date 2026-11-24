"""Finnish voiceover (ElevenLabs, voice "Helena") and AI sound effects (Mirelo).

Files live in launch/video/in/vo and launch/video/in/sfx (generated once by gen_vo.py /
gen_sfx.py; not regenerated here). Each VO file is cut into sentence segments at its
natural pauses (bounds measured with silencedetect -45 dB), so every sentence can be
locked to its card or shot. Leading/trailing silence is trimmed by the segment bounds.
"""
from __future__ import annotations

from dataclasses import dataclass

from assemble import Snd
from common import OUT

VO_DIR = OUT / "in" / "vo"
SFX_DIR = OUT / "in" / "sfx"

# speech bounds (s) inside each file, per sentence
SEG = {
    "vo1":  ("vo1", 0.144, 4.736, "Kello on viisi vaille kaksi. Bussi lähtee neljän minuutin päästä."),
    "vo2":  ("vo2", 0.137, 2.068, "Ja kotiin jäi hana auki."),
    "vo3a": ("vo3", 0.144, 1.197, "Tavallinen hana."),
    "vo3b": ("vo3", 1.672, 4.025, "Siinä ei ole sähköä eikä sirua."),
    "vo3c": ("vo3", 4.598, 6.683, "Mutta Hanax tietää, onko se auki."),
    "vo4a": ("vo4", 0.129, 3.053, "Pieni kamera-anturi lukee venttiilin asennon."),
    "vo4b": ("vo4", 3.632, 7.448, "Eteisen paneeli näyttää yhdellä vilkaisulla, mikä jäi päälle."),
    "vo5a": ("vo5", 0.143, 1.058, "Sama hetki."),
    "vo5b": ("vo5", 1.661, 3.770, "Nyt Hanax kertoo ennen kuin lähdet."),
    "vo5c": ("vo5", 4.457, 6.574, "Paina nuppia, niin kaikki on pois."),
    "vo6":  ("vo6", 0.122, 2.843, "Prototyyppi toimii jo killan keittiössä."),
    "vo7":  ("vo7", 0.130, 3.074, "Hanax. Lähde kotoa huoletta."),
}
# "Paina nuppia," ends 0.46 s into vo5c (comma pause 4.917-5.047 in vo5.mp3)
PAINA_NUPPIA_END = 0.46

LEAD, TAIL = 0.03, 0.12            # keep a breath of room tone around each sentence
VO_GAIN_DB = -2.0           # VO peaks ~ -8 dBFS: clear of the pre-limiter
# VO chain: gentle high-pass, light compression (about 3 dB GR on peaks), de-click fades
VO_AF = ("highpass=f=80:poles=2,"
         "acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:knee=4:makeup=2")


@dataclass
class Cue:
    key: str
    start: float                    # timeline time where the speech starts

    @property
    def text(self) -> str:
        return SEG[self.key][3]

    @property
    def length(self) -> float:
        _, a, b, _ = SEG[self.key]
        return b - a

    @property
    def end(self) -> float:
        return self.start + self.length

    def snd(self) -> Snd:
        f, a, b, _ = SEG[self.key]
        return Snd(VO_DIR / f"{f}.mp3", self.start - LEAD, (b - a) + LEAD + TAIL, VO_GAIN_DB,
                   0.01, 0.08, offset=a - LEAD, bus="vo", af=VO_AF)


def sfx(name: str):
    return SFX_DIR / f"{name}.mp3"


def check_no_overlap(cues: list[Cue]) -> None:
    cs = sorted(cues, key=lambda c: c.start)
    for x, y in zip(cs, cs[1:]):
        if x.end + 0.15 > y.start:
            raise ValueError(f"VO overlap: {x.key} ends {x.end:.2f}, {y.key} starts {y.start:.2f}")


def transcript(cues: list[Cue]):
    """(start, end, text) per VO sentence, for the .srt/.vtt."""
    return [(c.start, c.end + 0.25, c.text) for c in sorted(cues, key=lambda c: c.start)]
