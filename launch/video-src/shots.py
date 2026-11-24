"""Render one shot (trimmed, upscaled, graded, with card overlays) to an
intermediate video file plus a separate audio WAV."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from common import FPS, GRADE, WORK, clip, run


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
    src: str               # clip short name, e.g. '08-09'; or 'CARD:<name>' for a still card
    tin: float = 0.0
    tout: float = 0.0
    speed: float = 1.0
    reverse: bool = False
    mode: str = "wide"     # wide | portrait | v_crop | v_frame | v_native
    cx: float = 0.5        # v_crop: horizontal centre of the 9:16 window (0..1)
    defocus_at: float | None = None
    overlays: list = field(default_factory=list)
    gain_db: float = 0.0   # natural sound level
    xfade: float = 0.0     # crossfade INTO this shot (0 = hard cut)
    note: str = ""
    dur_override: float | None = None  # for CARD shots

    @property
    def dur(self) -> float:
        if self.dur_override:
            return self.dur_override
        return (self.tout - self.tin) / self.speed


def _base_chain(s: Shot) -> str:
    """Filter chain from the decoded clip to a graded frame of the target size."""
    sp = f"setpts=(PTS-STARTPTS)/{s.speed}," if s.speed != 1 else "setpts=PTS-STARTPTS,"
    rev = "reverse," if s.reverse else ""
    pre = f"{rev}{sp}fps={FPS},"
    if s.mode == "wide":
        return pre + f"scale=1974:1080:flags=lanczos,crop=1920:1080,{GRADE}"
    if s.mode == "portrait":   # portrait clip inside 16:9: sharp centre over soft fill
        return (pre + f"{GRADE},split[pa][pb];"
                "[pa]scale=1920:-2:flags=bilinear,crop=1920:1080,gblur=sigma=40,"
                "eq=brightness=-0.08:saturation=0.7[pbg];"
                "[pb]scale=-2:1080:flags=lanczos[pfg];[pbg][pfg]overlay=(W-w)/2:0")
    if s.mode == "v_crop":
        cw = 261  # 9:16 window in the 848x464 source
        x = int(max(0, min(848 - cw, 848 * s.cx - cw / 2)))
        return pre + f"crop={cw}:464:{x}:0,scale=1080:1920:flags=lanczos,{GRADE}"
    if s.mode == "v_frame":
        return (pre + f"{GRADE},split[pa][pb];"
                "[pa]scale=-2:1920:flags=bilinear,crop=1080:1920,gblur=sigma=40,"
                "eq=brightness=-0.1:saturation=0.7[pbg];"
                "[pb]scale=1080:-2:flags=lanczos[pfg];[pbg][pfg]overlay=0:(H-h)/2")
    if s.mode == "v_native":
        return pre + f"scale=1080:-2:flags=lanczos,crop=1080:1920,{GRADE}"
    raise ValueError(s.mode)


def render_shot(s: Shot, outdir: Path, size=(1920, 1080)) -> tuple[Path, Path]:
    vout = outdir / f"{s.id}.mp4"
    aout = outdir / f"{s.id}.wav"
    W, H = size
    dur = s.dur
    args = ["ffmpeg"]
    if s.src.startswith("CARD:"):
        args += ["-loop", "1", "-framerate", FPS, "-t", f"{dur:.3f}",
                 "-i", WORK / "gfx" / f"{s.src[5:]}.png"]
        fc = f"[0:v]format=yuv420p,scale={W}:{H}[v0]"
    else:
        args += ["-ss", f"{s.tin:.3f}", "-t", f"{s.tout - s.tin:.3f}", "-i", clip(s.src)]
        fc = f"[0:v]{_base_chain(s)}"
        if s.defocus_at is not None:
            fc += (f",split[da][db];[db]gblur=sigma=22,eq=brightness=-0.06,format=yuva420p,"
                   f"fade=in:st={s.defocus_at:.3f}:d=0.35:alpha=1[dbl];[da][dbl]overlay")
        fc += f",trim=duration={dur:.3f},setsar=1[v0]"
    last = "v0"
    for i, ov in enumerate(s.overlays):
        end = dur if ov.end is None else ov.end
        args += ["-loop", "1", "-framerate", FPS, "-t", f"{dur:.3f}",
                 "-i", WORK / "gfx" / f"{ov.card}.png"]
        idx = i + 1
        fo_st = max(ov.start, end - ov.fout)
        fc += (f";[{idx}:v]format=rgba,fade=in:st={ov.start:.3f}:d={ov.fin:.3f}:alpha=1,"
               f"fade=out:st={fo_st:.3f}:d={ov.fout:.3f}:alpha=1[o{i}];"
               f"[{last}][o{i}]overlay=0:0:enable='between(t,{ov.start:.3f},{end:.3f})'[v{i+1}]")
        last = f"v{i+1}"
    fc += f";[{last}]format=yuv420p[vout]"
    args += ["-filter_complex", fc, "-map", "[vout]", "-an", "-t", f"{dur:.3f}",
             "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-r", FPS, vout]
    run(args)

    # audio
    aargs = ["ffmpeg"]
    if s.src.startswith("CARD:"):
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
        aargs += ["-ss", f"{s.tin:.3f}", "-t", f"{s.tout - s.tin:.3f}", "-i", clip(s.src),
                  "-vn", "-af", af, "-c:a", "pcm_s16le", aout]
    run(aargs)
    return vout, aout
