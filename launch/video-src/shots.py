"""Render one shot to an intermediate video file plus a separate audio WAV.

Sources (Shot.src):
  '08-09'            phone clip short name (graded to the v2 look)
  'CARD:<name>'      full-frame still from _work/gfx (cards, black frames)
  'STILL:<file>'     product render from brand/renders, Ken Burns move (kenburns.py)
  'MOV:<path>'       any movie: the turntable/reveal renders, AI Studio clips, proof footage
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from common import FPS, GRADE_V2, RENDERS, WORK, clip, run

# light grade for non-phone footage (AI clips, proof): just pull it toward the palette
GRADE_SOFT = ("eq=contrast=1.04:saturation=0.7:gamma=0.97,"
              "colorbalance=rs=-0.02:bs=0.03:rm=-0.015:bm=0.015")


@dataclass
class Ov:
    card: str              # name of PNG in _work/gfx
    start: float = 0.0     # seconds, relative to shot start
    end: float | None = None
    fin: float = 0.3
    fout: float = 0.3


@dataclass
class Shot:
    id: str
    src: str
    tin: float = 0.0
    tout: float = 0.0
    speed: float = 1.0
    reverse: bool = False
    mode: str = "wide"     # wide | portrait | v_crop | v_frame | v_native | v_fit
    cx: float = 0.5        # v_crop: horizontal centre of the 9:16 window (0..1)
    defocus_at: float | None = None
    overlays: list = field(default_factory=list)
    gain_db: float = 0.0   # natural sound level (-60 = mute)
    xfade: float = 0.0     # crossfade INTO this shot (0 = hard cut)
    note: str = ""
    dur_override: float | None = None  # CARD / STILL shots
    kb: tuple | None = None            # STILL: ((cx,cy,w), (cx,cy,w))
    variant: str | None = None         # STILL: 'ring_off'
    mix: tuple | None = None           # STILL: crossfade to variant between (t0, t1)
    grade: str = "auto"                # auto | phone | soft | none

    @property
    def dur(self) -> float:
        if self.dur_override:
            return self.dur_override
        return (self.tout - self.tin) / self.speed

    @property
    def kind(self) -> str:
        for k in ("CARD", "STILL", "MOV"):
            if self.src.startswith(k + ":"):
                return k
        return "CLIP"

    def path(self) -> Path:
        if self.kind == "CLIP":
            return clip(self.src)
        rest = self.src.split(":", 1)[1]
        if self.kind == "STILL":
            return RENDERS / rest
        if self.kind == "CARD":
            return WORK / "gfx" / f"{rest}.png"
        p = Path(rest)
        return p if p.is_absolute() else RENDERS / rest


def _grade(s: Shot) -> str:
    g = s.grade if s.grade != "auto" else ("phone" if s.kind == "CLIP" else "none")
    return {"phone": GRADE_V2 + ",", "soft": GRADE_SOFT + ",", "none": ""}[g]


def _has_audio(p: Path) -> bool:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                          "stream=index", "-of", "json", str(p)], capture_output=True, text=True)
    return bool(json.loads(out.stdout or "{}").get("streams"))


def _base_chain(s: Shot, W: int, H: int) -> str:
    """Filter chain from the decoded source to a graded frame of the target size."""
    sp = f"setpts=(PTS-STARTPTS)/{s.speed}," if s.speed != 1 else "setpts=PTS-STARTPTS,"
    pre = ("reverse," if s.reverse else "") + f"{sp}fps={FPS},"
    G = _grade(s)
    if s.mode == "wide":       # cover the frame
        ch = pre + f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
        return ch + G.rstrip(",") if G else ch.rstrip(",")
    if s.mode == "portrait":   # portrait clip inside 16:9: sharp centre over soft fill
        return (pre + f"{G}split[pa][pb];"
                f"[pa]scale={W}:-2:flags=bilinear,crop={W}:{H},gblur=sigma=40,"
                "eq=brightness=-0.12:saturation=0.6[pbg];"
                f"[pb]scale=-2:{H}:flags=lanczos[pfg];[pbg][pfg]overlay=(W-w)/2:0")
    if s.mode == "v_crop":     # 9:16 window from a 16:9-ish clip
        return (pre + f"scale=-2:{H}:flags=lanczos,"
                f"crop={W}:{H}:'max(0,min(in_w-{W},in_w*{s.cx}-{W}/2))':0,{G}".rstrip(","))
    if s.mode == "v_frame":
        return (pre + f"{G}split[pa][pb];"
                f"[pa]scale=-2:{H}:flags=bilinear,crop={W}:{H},gblur=sigma=40,"
                "eq=brightness=-0.14:saturation=0.6[pbg];"
                f"[pb]scale={W}:-2:flags=lanczos[pfg];[pbg][pfg]overlay=0:(H-h)/2")
    if s.mode == "v_native":
        return pre + f"scale={W}:-2:flags=lanczos,crop={W}:{H},{G}".rstrip(",")
    if s.mode == "v_fit":      # render on black: enlarge, centre-crop, pad with the brand black
        # feather the top/bottom 220 px into the brand black so no box edge shows
        f = "min(1,min(Y,H-1-Y)/220)"
        return (pre + f"scale=-2:{int(H*0.78)}:flags=lanczos,crop={W}:ih:(iw-{W})/2:0,format=yuv420p,"
                f"geq=lum='17+(lum(X,Y)-17)*{f}':cb='128+(cb(X,Y)-128)*{f}':cr='128+(cr(X,Y)-128)*{f}',"
                f"pad={W}:{H}:0:(oh-ih)/2:color=0x0a0c0e,{G}".rstrip(","))
    raise ValueError(s.mode)


def render_shot(s: Shot, outdir: Path, size=(1920, 1080)) -> tuple[Path, Path]:
    vout, aout = outdir / f"{s.id}.mp4", outdir / f"{s.id}.wav"
    W, H = size
    dur = s.dur
    args = ["ffmpeg"]
    if s.kind == "STILL" or (s.kind == "MOV" and s.kb):
        # sub-pixel eased Ken Burns (stills, or a slow push on a movie)
        from kenburns import render_kb
        base = WORK / "kb" / f"{outdir.name}-{s.id}.mp4"
        a, b = s.kb or ((0.5, 0.5, 1.0), (0.5, 0.5, 0.92))
        render_kb(base, s.path(), dur, size, a, b, s.variant, s.mix, tin=s.tin)
        args += ["-i", base]
        g = _grade(s).rstrip(",")
        fc = f"[0:v]setpts=PTS-STARTPTS,{g + ',' if g else ''}format=yuv420p,trim=duration={dur:.3f}[v0]"
    elif s.kind == "CARD":
        args += ["-loop", "1", "-framerate", FPS, "-t", f"{dur:.3f}", "-i", s.path()]
        fc = f"[0:v]format=yuv420p,scale={W}:{H}[v0]"
    else:
        args += ["-ss", f"{s.tin:.3f}", "-t", f"{s.tout - s.tin:.3f}", "-i", s.path()]
        fc = f"[0:v]{_base_chain(s, W, H)}"
        if s.defocus_at is not None:
            fc += (f",split[da][db];[db]gblur=sigma=22,eq=brightness=-0.06,format=yuva420p,"
                   f"fade=in:st={s.defocus_at:.3f}:d=0.35:alpha=1[dbl];[da][dbl]overlay")
        fc += f",trim=duration={dur:.3f},setsar=1[v0]"
    last = "v0"
    for i, ov in enumerate(s.overlays):
        end = dur if ov.end is None else ov.end
        args += ["-loop", "1", "-framerate", FPS, "-t", f"{dur:.3f}",
                 "-i", WORK / "gfx" / f"{ov.card}.png"]
        fo_st = max(ov.start, end - ov.fout)
        fc += (f";[{i+1}:v]format=rgba,scale={W}:{H},fade=in:st={ov.start:.3f}:d={ov.fin:.3f}:alpha=1,"
               f"fade=out:st={fo_st:.3f}:d={ov.fout:.3f}:alpha=1[o{i}];"
               f"[{last}][o{i}]overlay=0:0:enable='between(t,{ov.start:.3f},{end:.3f})'[v{i+1}]")
        last = f"v{i+1}"
    fc += f";[{last}]format=yuv420p[vout]"
    args += ["-filter_complex", fc, "-map", "[vout]", "-an", "-t", f"{dur:.3f}",
             "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-r", FPS, vout]
    run(args)

    # audio: natural sound for clips (and movies that have it), silence otherwise
    aargs = ["ffmpeg"]
    if s.kind in ("CARD", "STILL") or not _has_audio(s.path()) or s.gain_db <= -60:
        aargs += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
                  "-c:a", "pcm_s16le", aout]
    else:
        af = "aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS"
        if s.reverse:
            af += ",areverse"
        sp = s.speed
        while sp > 2.0:
            af += ",atempo=2.0"
            sp /= 2.0
        while sp < 0.5:
            af += ",atempo=0.5"
            sp /= 0.5
        if sp != 1.0:
            af += f",atempo={sp:.4f}"
        af += (f",volume={s.gain_db}dB,apad,atrim=duration={dur:.3f},"
               f"afade=in:d=0.02,afade=out:st={max(0, dur - 0.03):.3f}:d=0.03")
        aargs += ["-ss", f"{s.tin:.3f}", "-t", f"{s.tout - s.tin:.3f}", "-i", s.path(),
                  "-vn", "-af", af, "-c:a", "pcm_s16le", aout]
    run(aargs)
    return vout, aout
