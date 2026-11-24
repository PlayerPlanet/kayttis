"""Build everything:  python launch/video-src/build_all.py [main|teaser|web|all]

Outputs (launch/video/, gitignored):
  hanax-launch-60s-16x9.mp4, hanax-teaser-20s-9x16.mp4, hanax-thumbnail-1280x720.jpg,
  hanax-launch-60s-16x9.fi.srt, hanax-teaser-20s-9x16.fi.srt
Web copies (frontend/public/media/): hanax-60s.mp4, hanax-60s-poster.jpg, hanax-teaser.mp4
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor

from assemble import assemble, mix_audio, timeline, total_len, write_ass, write_srt
from audio import build_audio_assets
from cards import build_cards
from common import OUT, WEB, WORK, ensure_dirs, probe_duration, run
from shots import render_shot


def _cached(s, outdir, size):
    v, a = outdir / f"{s.id}.mp4", outdir / f"{s.id}.wav"
    if FORCE or not (v.exists() and a.exists()):
        return render_shot(s, outdir, size)
    return v, a


FORCE = "--force" in sys.argv


def render_all(shots, outdir, size):
    outdir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(lambda s: _cached(s, outdir, size), shots))
    return [r[0] for r in res], [r[1] for r in res]


def build(edit, name, size, ass_kw, assets):
    shots = edit.SHOTS
    vids, wavs = render_all(shots, WORK / ("shots" if size[0] > size[1] else "shots9"), size)
    total = total_len(shots)
    mix = mix_audio(shots, wavs, edit.sounds(assets), WORK / "audio" / f"{name}-mix.wav", total)
    caps = edit.captions()
    ass = WORK / f"{name}.ass"
    write_ass(ass, caps, playres=size, **ass_kw)
    write_srt(OUT / f"{name}.fi.srt", caps + edit.card_texts())
    out = assemble(shots, vids, mix, ass, OUT / f"{name}.mp4")
    print(f"{out.name}: {probe_duration(out):.2f} s, {out.stat().st_size/1e6:.1f} MB "
          f"(timeline {total:.2f} s)")
    return out


def web_copies():
    main = OUT / "hanax-launch-60s-16x9.mp4"
    teaser = OUT / "hanax-teaser-20s-9x16.mp4"
    run(["ffmpeg", "-i", main, "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264",
         "-preset", "slow", "-crf", "25", "-maxrate", "1500k", "-bufsize", "3000k",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "112k", "-movflags", "+faststart",
         WEB / "hanax-60s.mp4"])
    run(["ffmpeg", "-i", teaser, "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264",
         "-preset", "slow", "-crf", "25", "-maxrate", "2000k", "-bufsize", "4000k",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "112k", "-movflags", "+faststart",
         WEB / "hanax-teaser.mp4"])
    # thumbnail/poster: the Hanax panel moment
    import edit_main as em
    t = timeline(em.SHOTS)[[s.id for s in em.SHOTS].index("M13")] + 1.6
    run(["ffmpeg", "-ss", f"{t:.2f}", "-i", main, "-frames:v", "1", "-vf", "scale=1280:720:flags=lanczos",
         "-q:v", "2", OUT / "hanax-thumbnail-1280x720.jpg"])
    run(["ffmpeg", "-ss", f"{t:.2f}", "-i", main, "-frames:v", "1", "-vf", "scale=1280:720:flags=lanczos",
         "-q:v", "3", WEB / "hanax-60s-poster.jpg"])
    for f in (WEB / "hanax-60s.mp4", WEB / "hanax-teaser.mp4", WEB / "hanax-60s-poster.jpg",
              OUT / "hanax-thumbnail-1280x720.jpg"):
        print(f"{f.name}: {f.stat().st_size/1e6:.2f} MB")


def main(what="all"):
    ensure_dirs()
    build_cards()
    assets = build_audio_assets(70)
    if what in ("main", "all"):
        import edit_main
        build(edit_main, "hanax-launch-60s-16x9", (1920, 1080), dict(size=52, marginv=100), assets)
    if what in ("teaser", "all"):
        import edit_teaser
        build(edit_teaser, "hanax-teaser-20s-9x16", (1080, 1920),
              dict(size=58, marginv=430, marginh=90), assets)
    if what in ("web", "all"):
        web_copies()
    from notes import write_notes
    write_notes()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
