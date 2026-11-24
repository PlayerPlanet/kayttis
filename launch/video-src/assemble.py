"""Join rendered shots (hard cuts / short crossfades), mix natural sound with the
synthesised sound design, burn in captions and normalise loudness to -16 LUFS."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from common import FPS, WORK, ass_ts, run, ts


@dataclass
class Snd:
    wav: Path
    start: float            # timeline seconds
    dur: float
    gain_db: float = 0.0
    fin: float = 0.05
    fout: float = 0.05
    offset: float = 0.0     # seconds into the wav
    bus: str = "bed"        # bed | vo  (the bed is ducked under the VO)
    af: str = ""            # extra per-sound filter chain (the VO processing)


def timeline(shots) -> list[float]:
    """Start time of every shot on the output timeline."""
    starts, t = [], 0.0
    for s in shots:
        t0 = t - s.xfade if starts else 0.0
        starts.append(t0)
        t = t0 + s.dur
    return starts


def total_len(shots) -> float:
    st = timeline(shots)
    return st[-1] + shots[-1].dur


def write_ass(path: Path, caps, playres=(1920, 1080), size=40, marginv=100, marginh=150, pad=13):
    """v2 captions: Geist Medium, ink on a translucent graphite box (#181c21 @ ~70 %)."""
    W, H = playres
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Geist Medium,{size},&H00EFECE8,&H00EFECE8,&H4A211C18,&H00000000,0,0,0,0,100,100,0,0,3,{pad},0,2,{marginh},{marginh},{marginv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [f"Dialogue: 0,{ass_ts(a)},{ass_ts(b)},Cap,,0,0,0,,{{\\fad(150,150)}}{txt}"
             for a, b, txt in caps]
    path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def write_srt(path: Path, entries):
    out = []
    for i, (a, b, txt) in enumerate(sorted(entries), 1):
        out.append(f"{i}\n{ts(a)} --> {ts(b)}\n{txt}\n")
    path.write_text("\n".join(out), encoding="utf-8")


DUCK_DB = -9.0              # bed + SFX under the VO
DUCK_ATTACK, DUCK_RELEASE = 0.20, 0.50


def duck_expr(windows) -> str:
    """Gain envelope keyed from the VO: ramps down DUCK_ATTACK s before each line,
    holds while it speaks, recovers over DUCK_RELEASE s (linear-gain ramps)."""
    if not windows:
        return "1"
    d = 1 - 10 ** (DUCK_DB / 20)
    a, r = DUCK_ATTACK, DUCK_RELEASE
    ws = "+".join(f"max(0,min(1,(t-{s0:.3f}+{a})/{a}))*max(0,min(1,({s1:.3f}+{r}-t)/{r}))"
                  for s0, s1 in windows)
    return f"1-{d:.4f}*min(1,{ws})"


def write_vtt(path: Path, entries):
    def vt(sec):
        return ts(sec).replace(",", ".")
    out = ["WEBVTT", ""]
    for i, (a, b, txt) in enumerate(sorted(entries), 1):
        out += [str(i), f"{vt(a)} --> {vt(b)}", txt, ""]
    path.write_text(chr(10).join(out), encoding="utf-8")


def mix_audio(shots, shot_wavs, extra: list[Snd], out: Path, total: float, stems: Path | None = None):
    starts = timeline(shots)
    snds = []
    for i, (s, w) in enumerate(zip(shots, shot_wavs)):
        nxt = shots[i + 1].xfade if i + 1 < len(shots) else 0.0
        snds.append(Snd(w, starts[i], s.dur, 0.0, max(0.02, s.xfade), max(0.03, nxt)))
    snds += extra
    args, fc, bed, vo = ["ffmpeg"], [], [], []
    for i, sd in enumerate(snds):
        args += ["-i", sd.wav]
        d_ms = int(round(sd.start * 1000))
        fx = (sd.af + ",") if sd.af else ""
        fc.append(f"[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
                  f"atrim=start={sd.offset:.3f}:duration={sd.dur:.3f},asetpts=PTS-STARTPTS,{fx}"
                  f"afade=in:d={sd.fin:.3f},afade=out:st={max(0, sd.dur - sd.fout):.3f}:d={sd.fout:.3f},"
                  f"volume={sd.gain_db}dB,adelay={d_ms}|{d_ms}[a{i}]")
        (vo if sd.bus == "vo" else bed).append(f"[a{i}]")
    win = [(sd.start, sd.start + sd.dur) for sd in snds if sd.bus == "vo"]
    env = duck_expr(win)
    fc.append("".join(bed) + f"amix=inputs={len(bed)}:normalize=0:dropout_transition=0,"
              f"apad=whole_dur={total:.3f}[bed]")
    fc.append(f"aevalsrc='{env}|{env}':s=48000:d={total:.3f},aformat=sample_fmts=fltp:channel_layouts=stereo[env]")
    fc.append("[bed]asplit=2[bedA][bedS];[bedA][env]amultiply[bedd]")
    if vo:
        fc.append("".join(vo) + f"amix=inputs={len(vo)}:normalize=0:dropout_transition=0,"
                  f"apad=whole_dur={total:.3f}[vo]")
        fc.append("[bedd]asplit=2[beddA][beddS];[vo]asplit=2[voA][voS];"
                  "[beddA][voA]amix=inputs=2:normalize=0:dropout_transition=0[mix]")
    else:
        fc.append("[bedd]asplit=2[mix][beddS];anullsrc=r=48000:cl=stereo,"
                  f"atrim=duration={total:.3f}[voS]")
    cap = ["-t", f"{total:.3f}"]
    args += ["-filter_complex", ";".join(fc), "-map", "[mix]", *cap, "-c:a", "pcm_s24le", "-ar", "48000", out]
    if stems:   # for the ducking / overlap measurements
        args += ["-map", "[bedS]", *cap, "-c:a", "pcm_s16le", stems / f"{out.stem}-bed.wav",
                 "-map", "[beddS]", *cap, "-c:a", "pcm_s16le", stems / f"{out.stem}-bed-ducked.wav",
                 "-map", "[voS]", *cap, "-c:a", "pcm_s16le", stems / f"{out.stem}-vo.wav"]
    else:
        args += ["-map", "[bedS]", *cap, "-f", "null", "-", "-map", "[beddS]", *cap, "-f", "null", "-",
                 "-map", "[voS]", *cap, "-f", "null", "-"]
    run(args)
    return out


# brick-wall limiter ahead of the (linear) loudnorm, so the transients (door slam, impact)
# don't cap the gain and the film actually lands at -16 LUFS
PRE_LIMIT = "alimiter=limit=0.4:attack=1:release=60:level=disabled,"


def loudnorm_filter(wav: Path, target=-16.0) -> str:
    err = run(["ffmpeg", "-i", wav, "-af", f"{PRE_LIMIT}loudnorm=I={target}:TP=-2:LRA=11:print_format=json",
               "-f", "null", "-"], quiet=False)
    m = json.loads(re.findall(r"\{[^{}]*\}", err)[-1])
    return (f"{PRE_LIMIT}loudnorm=I={target}:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
            f"offset={m['target_offset']}:linear=true")


def finish_chain(letterbox: int = 0, grain: int = 5) -> str:
    """Film-wide finishing: fine temporal luma grain (one texture over phone footage and
    renders alike), then the letterbox bars (pure black, drawn after the grain)."""
    ch = f"noise=c0s={grain}:c0f=t+u" if grain else "null"
    if letterbox:
        ch += (f",drawbox=x=0:y=0:w=iw:h={letterbox}:color=black:t=fill"
               f",drawbox=x=0:y=ih-{letterbox}:w=iw:h={letterbox}:color=black:t=fill")
    return ch


def assemble(shots, shot_vids, mix_wav: Path, ass: Path, out: Path, crf=17,
             letterbox: int = 0, grain: int = 5):
    starts = timeline(shots)
    args, fc = ["ffmpeg"], []
    for v in shot_vids:
        args += ["-i", v]
    for i in range(len(shot_vids)):
        fc.append(f"[{i}:v]setpts=PTS-STARTPTS,fps={FPS},settb=AVTB,format=yuv420p[n{i}]")
    acc, acc_len = "[n0]", shots[0].dur
    for i in range(1, len(shots)):
        s = shots[i]
        lab = f"[c{i}]"
        if s.xfade > 0:
            fc.append(f"{acc}[n{i}]xfade=transition=fade:duration={s.xfade:.3f}:"
                      f"offset={acc_len - s.xfade:.3f},fps={FPS},settb=AVTB{lab}")
        else:
            fc.append(f"{acc}[n{i}]concat=n=2:v=1:a=0,fps={FPS},settb=AVTB{lab}")
        acc_len = starts[i] + s.dur
        acc = lab
    ass_rel = ass.relative_to(WORK).as_posix()
    fc.append(f"{acc}{finish_chain(letterbox, grain)},ass={ass_rel}:fontsdir=fonts,format=yuv420p[vout]")
    ai = len(shot_vids)
    args += ["-i", mix_wav, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", f"{ai}:a",
             "-af", loudnorm_filter(mix_wav) + ",aresample=48000",
             "-c:v", "libx264", "-preset", "slow", "-crf", crf, "-profile:v", "high", "-pix_fmt", "yuv420p",
             "-r", FPS, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
             "-t", f"{acc_len:.3f}", out]
    run(args, cwd=WORK)
    return out
