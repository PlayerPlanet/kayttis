"""Write launch/video/EDIT_NOTES.md from the edit lists (cut list + text)."""
from __future__ import annotations

from assemble import timeline, total_len
from common import OUT


def _table(edit) -> str:
    st = timeline(edit.SHOTS)
    rows = ["| # | out start | dur | source clip | in → out (s) | speed / fx | trans. in | what |",
            "|---|---|---|---|---|---|---|---|"]
    for s, t in zip(edit.SHOTS, st):
        src = s.src if s.src.startswith("CARD:") else f"`video_2026-11-24_14-{s.src}.mp4`"
        io = "—" if s.src.startswith("CARD:") else f"{s.tin:.2f} → {s.tout:.2f}"
        fx = []
        if s.speed != 1:
            fx.append(f"{s.speed:g}×")
        if s.reverse:
            fx.append("reversed")
        if s.defocus_at is not None:
            fx.append(f"defocus @{s.defocus_at:g}s")
        if s.mode != "wide":
            fx.append(s.mode + (f" cx={s.cx:g}" if s.mode == "v_crop" else ""))
        fx += [f"card `{o.card}`" for o in s.overlays]
        tr = f"dissolve {s.xfade:g}s" if s.xfade else "cut"
        rows.append(f"| {s.id} | {t:5.2f} | {s.dur:.2f} | {src} | {io} | {', '.join(fx) or '—'} | {tr} | {s.note} |")
    return "\n".join(rows)


def _text(edit) -> str:
    lines = ["| in | out | text |", "|---|---|---|"]
    for a, b, txt in sorted(edit.captions() + edit.card_texts()):
        lines.append(f"| {a:5.2f} | {b:5.2f} | {txt} |")
    return "\n".join(lines)


def write_notes():
    import edit_main as em
    import edit_teaser as et
    md = f"""# Hanax launch video: edit notes

Built by `launch/video-src/build_all.py` (ffmpeg 8 + headless Chrome for the cards).
Re-render: `python launch/video-src/build_all.py all` (or `main`, `teaser`, `web`).
Source: 15 Telegram-compressed phone clips, 848×464 @ 30 fps (one portrait 464×848).

## Main video, 16:9, 1920×1080, {total_len(em.SHOTS):.1f} s

Story: calm moment → the bus leaves at 14.00, it is 13:56 → rush out, door slams →
silence, a ticking clock, water creeping in → tap running, stove on → the problem,
stated once → rewind ("same moment, now with Hanax") → the app shows what was left on →
back, tap and stove off, KAIKKI KIINNI → leave calmly → end card.

Note: the microwave in the source clip shows 14:31. The shot defocuses as the clock
comes into view, and a JetBrains Mono "13:56" readout takes over, so the story time
matches the route app (bus 25 at 14.00).

### Cut list
{_table(em)}

### On-screen text (captions burned in, and the graphics cards)
{_text(em)}

## Teaser, 9:16, 1080×1920, {total_len(et.SHOTS):.1f} s

### Cut list
{_table(et)}

### On-screen text
{_text(et)}

## Look and sound
- Upscale: lanczos to 1974×1080, then centre-cropped to 1920 (the source is 1.83:1).
  Grade on every shot: contrast 1.05, saturation 0.94, a slight cool colour balance, light unsharp.
  No stabilisation: most of the shake is in the whip pan and the running shots, where it reads as
  the rush. The calm shots are steady enough, and deshake would add edge warping and a further crop.
- Cards: brand fonts (Familjen Grotesk, Figtree, JetBrains Mono) and colours. The state rule is kept:
  PÄÄLLÄ is amber #f08a16 with a text label; KAIKKI KIINNI is green #2c8564 with a check mark.
- Captions: Figtree SemiBold, paper on a translucent ink box, inside title-safe margins. They are also
  in `.fi.srt` (the SRT includes the card texts too).
- Audio: natural sound (room, door slam, water, stove click). Synthesised in ffmpeg: a tick-tock clock
  (a quiet one under the 13:56 beat, a louder one after the door slam), a low drone under the disaster,
  a tape-rewind sweep, and a soft A-major pad from the Hanax reveal to the end. The water sound is
  pre-lapped about 2 s before the tap shot (J-cut). Two-pass loudnorm to −16 LUFS, true peak −1.5 dBTP.
  No music and nothing downloaded.
"""
    (OUT / "EDIT_NOTES.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    write_notes()
