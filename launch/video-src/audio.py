"""Synthesised sound design (no downloads, no music samples): a ticking clock,
a quiet low drone for the tension, a soft major pad for the resolution and a
tape-rewind sweep. Everything is made with ffmpeg's aevalsrc/anoisesrc."""
from __future__ import annotations

from pathlib import Path

from common import WORK, run

SR = 48000


def tick(path: Path, dur: float, period: float = 1.0) -> Path:
    # alternating tick/tock: short decaying sine burst + a little filtered noise
    expr = (f"0.55*exp(-420*mod(t,{period}))*sin(2*PI*(2350+650*mod(floor(t/{period}),2))*t)"
            f"+0.35*exp(-900*mod(t,{period}))*(random(0)*2-1)")
    run(["ffmpeg", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s={SR}:d={dur:.3f}",
         "-af", "highpass=f=900,lowpass=f=7000,aecho=0.6:0.4:18|37:0.25|0.12,"
                "aformat=channel_layouts=stereo,volume=-6dB",
         "-c:a", "pcm_s16le", path])
    return path


def drone(path: Path, dur: float) -> Path:
    # low, slightly beating fifth; slow swell
    expr = ("0.35*sin(2*PI*55*t)+0.25*sin(2*PI*82.6*t)+0.12*sin(2*PI*110.4*t)")
    run(["ffmpeg", "-f", "lavfi", "-i", f"aevalsrc='{expr}*(0.75+0.25*sin(2*PI*0.18*t))':s={SR}:d={dur:.3f}",
         "-af", f"lowpass=f=400,afade=in:d={min(2.5, dur/2):.2f},afade=out:st={dur-1.5:.2f}:d=1.5,"
                "aformat=channel_layouts=stereo",
         "-c:a", "pcm_s16le", path])
    return path


def pad(path: Path, dur: float) -> Path:
    # soft A-major add9 pad with gentle tremolo, warm low-pass; very quiet in the mix
    notes = [220.0, 277.18, 329.63, 493.88, 554.37]
    amps = [0.22, 0.16, 0.16, 0.08, 0.06]
    expr = "+".join(f"{a}*sin(2*PI*{f}*t+{i})" for i, (f, a) in enumerate(zip(notes, amps)))
    run(["ffmpeg", "-f", "lavfi",
         "-i", f"aevalsrc='({expr})*(0.85+0.15*sin(2*PI*0.25*t))':s={SR}:d={dur:.3f}",
         "-af", f"lowpass=f=1800,aecho=0.8:0.6:120|230:0.3|0.2,"
                f"afade=in:d=2.0,afade=out:st={dur-2.5:.2f}:d=2.5,aformat=channel_layouts=stereo",
         "-c:a", "pcm_s16le", path])
    return path


def rewind(path: Path, dur: float) -> Path:
    # band-passed noise sweeping upward = tape rewind
    run(["ffmpeg", "-f", "lavfi", "-i", f"anoisesrc=c=pink:r={SR}:d={dur:.3f}:a=0.5",
         "-af", f"bandpass=f=1800:w=1.2,vibrato=f=11:d=0.4,"
                f"afade=in:d=0.15,afade=out:st={dur-0.3:.2f}:d=0.3,aformat=channel_layouts=stereo,volume=-8dB",
         "-c:a", "pcm_s16le", path])
    return path


def build_audio_assets(total: float) -> dict[str, Path]:
    a = WORK / "audio"
    return {
        "tick": tick(a / "tick.wav", 40.0),
        "drone": drone(a / "drone.wav", 16.0),
        "pad": pad(a / "pad.wav", 26.0),
        "rewind": rewind(a / "rewind.wav", 2.4),
    }
