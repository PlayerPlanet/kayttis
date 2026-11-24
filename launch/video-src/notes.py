"""Write launch/video/EDIT_NOTES.md from the v2 edit lists (cut list, text, slots)."""
from __future__ import annotations

from pathlib import Path

from assemble import timeline, total_len
from common import OUT


def _src(s) -> str:
    if s.kind == "CLIP":
        return f"`video_2026-11-24_14-{s.src}.mp4`"
    if s.kind == "MOV":
        return f"`{Path(s.src[4:]).name}`"
    return f"`{s.src}`"


def _table(edit) -> str:
    st = timeline(edit.SHOTS)
    rows = ["| # | out start | dur | source | in → out (s) | fx | trans. in | what |",
            "|---|---|---|---|---|---|---|---|"]
    for s, t in zip(edit.SHOTS, st):
        io = f"{s.tin:.2f} → {s.tout:.2f}" if s.kind in ("CLIP", "MOV") else "—"
        fx = []
        if s.speed != 1:
            fx.append(f"{s.speed:g}×")
        if s.reverse:
            fx.append("reversed")
        if s.kb:
            fx.append("eased push" if s.kb[1][2] < s.kb[0][2] else "eased pull-out")
        if s.variant:
            fx.append(f"{s.variant} crossfade")
        if s.mode != "wide":
            fx.append(s.mode + (f" cx={s.cx:g}" if s.mode == "v_crop" else ""))
        fx += [f"`{o.card}`" for o in s.overlays]
        tr = f"dissolve {s.xfade:g}s" if s.xfade else "cut"
        rows.append(f"| {s.id} | {t:5.2f} | {s.dur:.2f} | {_src(s)} | {io} | {', '.join(fx) or '—'} | {tr} | {s.note} |")
    return "\n".join(rows)


def _text(edit) -> str:
    lines = ["| in | out | text |", "|---|---|---|"]
    for a, b, txt in sorted(edit.captions() + edit.card_texts()):
        lines.append(f"| {a:5.2f} | {b:5.2f} | {txt} |")
    return "\n".join(lines)


def _cues(edit) -> str:
    from vo import SEG
    rows = ["| line | file [in → out] | start | end | text |", "|---|---|---|---|---|"]
    for c in sorted(edit.vo_cues(), key=lambda c: c.start):
        f, a, b, t = SEG[c.key]
        rows.append(f"| {c.key} | `{f}.mp3` [{a:.2f} → {b:.2f}] | {c.start:5.2f} | {c.end:5.2f} | {t} |")
    rows += ["", "| SFX | at | use |", "|---|---|---|"]
    rows += [f"| `{n}.mp3` | {t:5.2f} | {w} |" for t, n, w in sorted(edit.sfx_cues())]
    return chr(10).join(rows)


def _status(p) -> str:
    return "**present, in use**" if p else "not present → fallback"


def write_notes():
    import edit_main as em
    import edit_teaser as et
    ai = em.AI
    md = f"""# Hanax launch video v2 ("SF deeptech"): edit notes

Built by `launch/video-src/build_all.py` (ffmpeg 8, OpenCV for the Ken Burns moves, headless
Chrome for the cards). Re-render: `python launch/video-src/build_all.py all [--force]`
(or `main`, `teaser`, `web`). Shots are cached in `_work/shots*`; pass `--force` after
changing a shot.

Direction: Figure 02's cinematic industrial minimalism + Physical Intelligence's proof.
Formula (brand/README.md): claim *Tavallinen hana. Hanax tietää, onko se auki.* → proof:
the live prototype in the guild kitchen → action *Katso livenä*.

## Main film, 16:9, 1920×1080, {total_len(em.SHOTS):.1f} s

Beats: cold open (amber dot, 13:56:04 readout) → the everyday story (couch, bus, rush,
door slam, hard cut to the tap and the stove) → the claim on black → product reveal
(HX-P reveal, macros, exploded view, turntable, family) → rewind → the same moment with
Hanax (2 PÄÄLLÄ, knob press, tap and stove off, KAIKKI KIINNI ✓) → proof → end card.

### Cut list
{_table(em)}

### Voiceover and SFX cue sheet
{_cues(em)}

### On-screen text (designed cards only; no burned-in captions)
{_text(em)}

## Teaser, 9:16, 1080×1920, {total_len(et.SHOTS):.1f} s

### Cut list
{_table(et)}

### Voiceover and SFX cue sheet
{_cues(et)}

### On-screen text (burned-in captions + cards)
{_text(et)}

## Slots for material that arrives later (picked up automatically)

Drop the file in place and re-run `build_all.py all --force`. Missing files fall back silently.

| File | Replaces | Main film | Teaser | Status |
|---|---|---|---|---|
| `launch/video/in/proof-kitchen.mp4` | the proof title card (`proof_clip` in `edit_main.py`) | PF: 0–4 s of the clip, soft grade, label "LIVENÄ · KILLAN KEITTIÖ · LEIKKAAMATON" | — | {_status(em.proof_clip)} |
| `launch/ai-studio/v1-panel-reveal.mp4` | `hxp-reveal.mp4` render | P1: 0.5–4.1 s | — | {_status(ai['v1-panel-reveal'])} |
| `launch/ai-studio/v1-panel-reveal-9x16.mp4` | `hxp-reveal.mp4` render | — | V05: 0.5–3.1 s | {_status(et.AI_V1)} |
| `launch/ai-studio/v2-valve-rackfocus.mp4` | HX-01 LED macro push-in | P2: 1.0–3.2 s | — | {_status(ai['v2-valve-rackfocus'])} |
| `launch/ai-studio/v3-water-tension.mp4` | second half of the real tap shot | S07 shortened to 2 s + S07b 1.0–2.8 s cutaway | — | {_status(ai['v3-water-tension'])} |
| `launch/ai-studio/v4-knob-off.mp4` | knob-macro ring-off render (and the synthesised click; its own audio is used) | K1: 0.5–2.9 s | V06: 0.5–2.5 s, 9:16 centre crop | {_status(ai['v4-knob-off'])} |

AI clips get the soft grade (contrast 1.04, saturation 0.7, slightly cool) and keep the
lower-left labels. They are concept imagery, never proof: the proof slot only takes real footage.

## Look
- **Phone footage grade (v2):** contrast 1.10, brightness −0.05, saturation 0.5, gamma 0.93; a
  curve that crushes the toe and rolls the highlights off to 0.88 (no white walls screaming next
  to the dark renders); cool colour balance in shadows/mids; vignette; light unsharp after the
  lanczos upscale (848×464 → 1974×1080, centre crop).
- **Renders:** ungraded (already the palette). Stills move with a sub-pixel, smootherstep-eased
  affine warp (OpenCV Lanczos), so slow pushes have no zoompan wobble. The same warp gives the
  render movies (hxp-reveal, turntable) a slow push.
- **Knob press:** `hxp-knob-macro.png` crossfades to a generated "ring off" version (saturated
  amber pixels desaturated and darkened) in sync with the synthesised click.
- **One film:** fine temporal luma grain over everything (noise 5), then a 2.39:1 letterbox
  (138 px bars) on the 16:9 film. All text and captions sit inside the picture area.
- **Cards:** Geist / Geist Mono, graphite #0a0c0e, amber #ff9a2e the only colour (the dot, the
  PÄÄLLÄ pills, the knob ring). KAIKKI KIINNI is ink + check mark, no green (state rule).
- **Captions:** the 16:9 film has **no burned-in captions** (the VO carries the story). Its
  `.fi.srt` and `frontend/public/media/hanax-60s.fi.vtt` are the VO transcript with real timings;
  the site's player has the VTT as an off-by-default `<track>`. The teaser keeps burned-in
  captions (Geist Medium 50 px on a translucent graphite box) because social autoplays muted; its
  `.srt` has the captions and the VO lines.

## Sound
- **Voiceover:** ElevenLabs, voice "Helena" (`launch/video/in/vo/`, made by `gen_vo.py`; not
  regenerated by the build). Each file is cut at its sentence pauses (`vo.py`, bounds measured with
  silencedetect −45 dB), which trims the lead/tail silence and lets every sentence land on its card
  or shot. Chain: high-pass 80 Hz, light compression (2.5:1, threshold −24 dB), 10/80 ms fades.
- **AI SFX** (Mirelo, `launch/video/in/sfx/`): door slam, water (looped with a 1 s crossfade, J-cut
  kept), low impact under the claim, rewind, knob detent, stove click, confirm. The detent file is
  nearly silent (peak −38.6 dBFS), so it is lifted +24 dB and the synthesised click is layered under it.
- **Synthesised bed:** tick-tock clock, low drone, 48 Hz hum under the reveal, A-major pad from the
  knob press to the end.
- **Ducking:** the bed (natural sound, synth and SFX) runs through a gain envelope keyed from the
  VO cues: −9 dB, 0.2 s attack before each line, 0.5 s release after it (`assemble.duck_expr`).
- **Master:** limiter, then two-pass loudnorm to −16 LUFS, true peak −2 dBTP.

## Would improve with the Friday footage / AI clips
- `proof-kitchen.mp4`: the strongest beat. Shoot 6–10 s uncut, with the Pi dashboard's live
  timestamps in frame and a real coffee maker / valve state change.
- `v4-knob-off`: a real finger on the knob sells the one action better than the render crossfade.
- `v3-water-tension`: a darker, on-palette tap for the disaster (the phone tap is a bright kitchen).
"""
    (OUT / "EDIT_NOTES.md").write_text(md, encoding="utf-8")


if __name__ == "__main__":
    write_notes()
