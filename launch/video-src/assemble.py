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


def write_ass(path: Path, caps, playres=(1920, 1080), size=50, marginv=100, marginh=150):
    W, H = playres
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Figtree SemiBold,{size},&H00F6F7F4,&H00F6F7F4,&H38241C0F,&H00000000,0,0,0,0,100,100,0.3,0,3,16,0,2,{marginh},{marginh},{marginv},1

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


def mix_audio(shots, shot_wavs, extra: list[Snd], out: Path, total: float):
    starts = timeline(shots)
    snds = []
    for i, (s, w) in enumerate(zip(shots, shot_wavs)):
        nxt = shots[i + 1].xfade if i + 1 < len(shots) else 0.0
        snds.append(Snd(w, starts[i], s.dur, 0.0, max(0.02, s.xfade), max(0.03, nxt)))
    snds += extra
    args, fc, labels = ["ffmpeg"], [], []
    for i, sd in enumerate(snds):
        args += ["-i", sd.wav]
        d_ms = int(round(sd.start * 1000))
        fc.append(f"[{i}:a]atrim=start={sd.offset:.3f}:duration={sd.dur:.3f},asetpts=PTS-STARTPTS,"
                  f"afade=in:d={sd.fin:.3f},afade=out:st={max(0, sd.dur - sd.fout):.3f}:d={sd.fout:.3f},"
                  f"volume={sd.gain_db}dB,adelay={d_ms}|{d_ms}[a{i}]")
        labels.append(f"[a{i}]")
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,"
              f"apad,atrim=duration={total:.3f}[mix]")
    args += ["-filter_complex", ";".join(fc), "-map", "[mix]", "-c:a", "pcm_s24le", "-ar", "48000", out]
    run(args)
    return out


def loudnorm_filter(wav: Path, target=-16.0) -> str:
    err = run(["ffmpeg", "-i", wav, "-af", f"loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json",
               "-f", "null", "-"], quiet=False)
    m = json.loads(re.findall(r"\{[^{}]*\}", err)[-1])
    return (f"loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
            f"offset={m['target_offset']}:linear=true")


def assemble(shots, shot_vids, mix_wav: Path, ass: Path, out: Path, crf=17):
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
    fc.append(f"{acc}ass={ass_rel}:fontsdir=fonts,format=yuv420p[vout]")
    ai = len(shot_vids)
    args += ["-i", mix_wav, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", f"{ai}:a",
             "-af", loudnorm_filter(mix_wav) + ",aresample=48000",
             "-c:v", "libx264", "-preset", "slow", "-crf", crf, "-profile:v", "high", "-pix_fmt", "yuv420p",
             "-r", FPS, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
             "-t", f"{acc_len:.3f}", out]
    run(args, cwd=WORK)
    return out
