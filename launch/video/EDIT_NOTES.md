# Hanax launch video v2 ("SF deeptech"): edit notes

Built by `launch/video-src/build_all.py` (ffmpeg 8, OpenCV for the Ken Burns moves, headless
Chrome for the cards). Re-render: `python launch/video-src/build_all.py all [--force]`
(or `main`, `teaser`, `web`). Shots are cached in `_work/shots*`; pass `--force` after
changing a shot.

Direction: Figure 02's cinematic industrial minimalism + Physical Intelligence's proof.
Formula (brand/README.md): claim *Tavallinen hana. Hanax tietää, onko se auki.* → proof:
the live prototype in the guild kitchen → action *Katso livenä*.

## Main film, 16:9, 1920×1080, 65.6 s

Beats: cold open (amber dot, 13:56:04 readout) → the everyday story (couch, bus, rush,
door slam, hard cut to the tap and the stove) → the claim on black → product reveal
(HX-P reveal, macros, exploded view, turntable, family) → rewind → the same moment with
Hanax (2 PÄÄLLÄ, knob press, tap and stove off, KAIKKI KIINNI ✓) → proof → end card.

### Cut list
| # | out start | dur | source | in → out (s) | fx | trans. in | what |
|---|---|---|---|---|---|---|---|
| C0 |  0.00 | 3.00 | `CARD:black` | — | `dot`, `ro0`, `ro1` | cut | Cold open: amber dot, 13:56:04 -> :05 |
| S01 |  2.70 | 2.60 | `video_2026-11-24_14-08-09.mp4` | 1.00 → 3.60 | — | dissolve 0.3s | Couch, scrolling the phone |
| S02 |  5.30 | 2.40 | `video_2026-11-24_14-17-34.mp4` | 0.30 → 2.70 | portrait | cut | Route app: bus leaves 14.00 |
| S03 |  7.70 | 2.20 | `video_2026-11-24_14-25-26.mp4` | 0.50 → 2.70 | — | cut | Jumps up |
| S04 |  9.90 | 1.80 | `video_2026-11-24_14-27-39.mp4` | 0.40 → 2.20 | — | cut | Through the doorway |
| S05 | 11.70 | 2.20 | `video_2026-11-24_14-29-06.mp4` | 0.70 → 2.90 | — | cut | Down the hallway |
| S06 | 13.90 | 3.20 | `video_2026-11-24_14-31-48.mp4` | 2.20 → 5.40 | — | cut | Door slams (at +1.35 s); still frame, clock ticking |
| S07 | 17.10 | 3.80 | `video_2026-11-24_14-35-21.mp4` | 3.60 → 7.40 | — | cut | Tap left running (hard cut) |
| S08 | 20.90 | 3.00 | `video_2026-11-24_14-36-53.mp4` | 0.00 → 3.00 | — | cut | Stove indicator on |
| CL | 23.90 | 7.60 | `CARD:black` | — | `claim1`, `claim2` | cut | Claim: 'Tavallinen hana.' ... 'Hanax tietää, onko se auki.' |
| P1 | 30.90 | 3.80 | `hxp-reveal.mp4` | 1.20 → 5.00 | eased push, `lab_hxp` | dissolve 0.6s | hxp-reveal render: screen on, light sweep, amber ring; slow push |
| P2 | 34.45 | 2.00 | `STILL:hx01-macro-led.png` | — | eased push, `lab_hx01` | dissolve 0.25s | HX-01 LED macro, push-in |
| P5 | 36.20 | 2.20 | `hx01-turntable.mp4` | 0.00 → 2.20 | eased push, `lab_hx01` | dissolve 0.25s | HX-01 turntable |
| P4 | 38.15 | 2.30 | `STILL:hx01-exploded.png` | — | eased push, `lab_hx01` | dissolve 0.25s | HX-01 exploded view, labels |
| P3 | 40.20 | 1.90 | `STILL:hxp-knob-macro.png` | — | eased push, `lab_hxp` | dissolve 0.25s | HX-P knob macro, push-in |
| P6 | 41.85 | 2.60 | `STILL:family.png` | — | eased pull-out, `lab_fam` | dissolve 0.25s | Family, slow pull-out |
| R1 | 44.45 | 0.55 | `video_2026-11-24_14-29-06.mp4` | 0.70 → 2.90 | 4×, reversed | cut | Rewind |
| R2 | 45.00 | 0.45 | `video_2026-11-24_14-27-39.mp4` | 0.40 → 2.20 | 4×, reversed | cut | Rewind |
| R3 | 45.45 | 0.55 | `video_2026-11-24_14-25-26.mp4` | 0.50 → 2.70 | 4×, reversed | cut | Rewind |
| R4 | 46.00 | 2.00 | `video_2026-11-24_14-08-09.mp4` | 1.00 → 3.00 | `rewind` | cut | Same moment, now with Hanax |
| U1 | 48.00 | 2.60 | `CARD:panel_on` | — | — | cut | HX-P UI: 2 PÄÄLLÄ |
| K1 | 50.60 | 2.40 | `STILL:hxp-knob-macro.png` | — | eased push, ring_off crossfade | cut | Knob press: amber ring fades out |
| T1 | 53.00 | 1.70 | `video_2026-11-24_14-34-29.mp4` | 0.60 → 2.30 | — | cut | Tap off |
| T2 | 54.70 | 2.20 | `video_2026-11-24_14-48-40.mp4` | 0.80 → 3.00 | — | cut | Stove off (click at +1.0 s) |
| U2 | 56.60 | 2.20 | `CARD:panel_off` | — | — | dissolve 0.3s | HX-P UI: KAIKKI KIINNI ✓ |
| PF | 58.40 | 3.60 | `CARD:proof` | — | — | dissolve 0.4s | Proof card (slot: launch/video/in/proof-kitchen.mp4) |
| E | 61.40 | 4.20 | `CARD:end` | — | — | dissolve 0.6s | End card |

### Voiceover and SFX cue sheet
| line | file [in → out] | start | end | text |
|---|---|---|---|---|
| vo1 | `vo1.mp3` [0.14 → 4.74] |  2.85 |  7.44 | Kello on viisi vaille kaksi. Bussi lähtee neljän minuutin päästä. |
| vo2 | `vo2.mp3` [0.14 → 2.07] | 18.30 | 20.23 | Ja kotiin jäi hana auki. |
| vo3a | `vo3.mp3` [0.14 → 1.20] | 24.25 | 25.30 | Tavallinen hana. |
| vo3b | `vo3.mp3` [1.67 → 4.03] | 25.75 | 28.10 | Siinä ei ole sähköä eikä sirua. |
| vo3c | `vo3.mp3` [4.60 → 6.68] | 28.65 | 30.74 | Mutta Hanax tietää, onko se auki. |
| vo4a | `vo4.mp3` [0.13 → 3.05] | 34.75 | 37.67 | Pieni kamera-anturi lukee venttiilin asennon. |
| vo4b | `vo4.mp3` [3.63 → 7.45] | 40.35 | 44.17 | Eteisen paneeli näyttää yhdellä vilkaisulla, mikä jäi päälle. |
| vo5a | `vo5.mp3` [0.14 → 1.06] | 46.20 | 47.11 | Sama hetki. |
| vo5b | `vo5.mp3` [1.66 → 3.77] | 48.20 | 50.31 | Nyt Hanax kertoo ennen kuin lähdet. |
| vo5c | `vo5.mp3` [4.46 → 6.57] | 50.75 | 52.87 | Paina nuppia, niin kaikki on pois. |
| vo6 | `vo6.mp3` [0.12 → 2.84] | 58.85 | 61.57 | Prototyyppi toimii jo killan keittiössä. |
| vo7 | `vo7.mp3` [0.13 → 3.07] | 62.00 | 64.94 | Hanax. Lähde kotoa huoletta. |

| SFX | at | use |
|---|---|---|
| `door-slam.mp3` | 15.23 | door slam |
| `water-run.mp3` | 15.30 | water, J-cut 1.8 s before the tap, looped to the claim |
| `impact-low.mp3` | 24.20 | under the first claim card |
| `rewind.mp3` | 44.45 | rewind |
| `knob-detent.mp3` | 51.25 | knob press (after 'Paina nuppia,') |
| `stove-click.mp3` | 55.70 | stove off |
| `confirm.mp3` | 56.75 | KAIKKI KIINNI |

### On-screen text (designed cards only; no burned-in captions)
| in | out | text |
|---|---|---|
|  1.00 |  3.00 | 13:56:04 |
| 24.20 | 31.50 | Tavallinen hana. Hanax tietää, onko se auki. |
| 31.70 | 34.70 | HX-P · PANEELI · PAINA: KAIKKI POIS |
| 34.75 | 36.45 | HX-01 · ANTURI · KONSEPTIMALLI |
| 42.15 | 44.45 | HX-01 + HX-P · KONSEPTIMALLEJA |
| 46.00 | 48.00 | 13:56:04 — Sama hetki. Nyt eteisessä on Hanax. |
| 48.00 | 50.60 | [HX-P: 2 PÄÄLLÄ — Keittiön hana PÄÄLLÄ, Liesi PÄÄLLÄ] |
| 56.60 | 58.80 | [HX-P: KAIKKI KIINNI ✓ — tarkistettu 2 s sitten] |
| 58.40 | 62.00 | LIVENÄ KILLAN KEITTIÖSSÄ · RASPBERRY PI · 2 KAHVINKEITINTÄ · VALOT · HANAN VENTTIILI |
| 61.40 | 65.60 | hanax — Lähde kotoa huoletta. Katso livenä · kayttis.kiirikki.fi · Aalto-yliopisto · Käyttäjälähtöinen tuotekehitysprojekti 2026 · Ryhmä 1 · Laitteet: konseptimalleja |

## Teaser, 9:16, 1080×1920, 22.0 s

### Cut list
| # | out start | dur | source | in → out (s) | fx | trans. in | what |
|---|---|---|---|---|---|---|---|
| V01 |  0.00 | 2.00 | `video_2026-11-24_14-35-21.mp4` | 5.20 → 7.20 | v_crop cx=0.47 | cut | Tap running (hook) |
| V02 |  2.00 | 1.80 | `video_2026-11-24_14-36-53.mp4` | 0.00 → 1.80 | v_crop cx=0.58 | cut | Stove indicator on |
| V03 |  3.80 | 1.60 | `video_2026-11-24_14-29-06.mp4` | 1.20 → 2.80 | v_frame | cut | Runs to the door |
| V04 |  5.40 | 4.20 | `CARD:v_black` | — | `v_claim1`, `v_claim2` | cut | Claim |
| V05 |  9.20 | 2.60 | `hxp-reveal.mp4` | 2.40 → 5.00 | v_fit, `v_lab_hxp` | dissolve 0.4s | hxp-reveal render on black |
| V06 | 11.80 | 2.00 | `STILL:hxp-knob-macro.png` | — | eased push, ring_off crossfade, `v_lab_knob` | cut | Knob press: amber ring fades out |
| V07 | 13.80 | 1.50 | `video_2026-11-24_14-34-29.mp4` | 0.60 → 2.10 | v_crop cx=0.5 | cut | Tap off |
| V08 | 15.30 | 2.00 | `video_2026-11-24_14-48-40.mp4` | 0.90 → 2.90 | v_crop cx=0.62 | cut | Stove off |
| V09 | 17.05 | 1.70 | `CARD:v_panel_off` | — | — | dissolve 0.25s | KAIKKI KIINNI ✓ |
| V10 | 18.25 | 3.80 | `CARD:v_end` | — | — | dissolve 0.5s | End card |

### Voiceover and SFX cue sheet
| line | file [in → out] | start | end | text |
|---|---|---|---|---|
| vo3a | `vo3.mp3` [0.14 → 1.20] |  5.75 |  6.80 | Tavallinen hana. |
| vo3c | `vo3.mp3` [4.60 → 6.68] |  7.30 |  9.38 | Mutta Hanax tietää, onko se auki. |
| vo7 | `vo7.mp3` [0.13 → 3.07] | 18.65 | 21.59 | Hanax. Lähde kotoa huoletta. |

| SFX | at | use |
|---|---|---|
| `water-run.mp3` |  0.00 | water under the tap hook |
| `impact-low.mp3` |  5.70 | under the first claim card |
| `knob-detent.mp3` | 12.60 | knob press |
| `stove-click.mp3` | 16.20 | stove off |
| `confirm.mp3` | 17.20 | KAIKKI KIINNI |

### On-screen text (burned-in captions + cards)
| in | out | text |
|---|---|---|
|  0.30 |  1.90 | Hana jäi auki. |
|  2.10 |  3.70 | Liesi jäi päälle. |
|  3.90 |  5.30 | Ja bussi lähtee. |
|  5.70 |  9.60 | Tavallinen hana. Hanax tietää, onko se auki. |
|  9.80 | 11.80 | HX-P · PANEELI · KONSEPTIMALLI |
| 12.00 | 13.80 | PAINA: KAIKKI POIS |
| 14.00 | 15.20 | Hana kiinni. |
| 15.50 | 17.20 | Liesi pois. |
| 17.05 | 18.75 | [HX-P: KAIKKI KIINNI ✓] |
| 18.25 | 22.05 | hanax — Lähde kotoa huoletta. Katso livenä · kayttis.kiirikki.fi · Aalto-yliopisto · Käyttäjälähtöinen tuotekehitysprojekti 2026 · Ryhmä 1 · Laitteet: konseptimalleja |

## Slots for material that arrives later (picked up automatically)

Drop the file in place and re-run `build_all.py all --force`. Missing files fall back silently.

| File | Replaces | Main film | Teaser | Status |
|---|---|---|---|---|
| `launch/video/in/proof-kitchen.mp4` | the proof title card (`proof_clip` in `edit_main.py`) | PF: 0–4 s of the clip, soft grade, label "LIVENÄ · KILLAN KEITTIÖ · LEIKKAAMATON" | — | not present → fallback |
| `launch/ai-studio/v1-panel-reveal.mp4` | `hxp-reveal.mp4` render | P1: 0.5–4.1 s | — | not present → fallback |
| `launch/ai-studio/v1-panel-reveal-9x16.mp4` | `hxp-reveal.mp4` render | — | V05: 0.5–3.1 s | not present → fallback |
| `launch/ai-studio/v2-valve-rackfocus.mp4` | HX-01 LED macro push-in | P2: 1.0–3.2 s | — | not present → fallback |
| `launch/ai-studio/v3-water-tension.mp4` | second half of the real tap shot | S07 shortened to 2 s + S07b 1.0–2.8 s cutaway | — | not present → fallback |
| `launch/ai-studio/v4-knob-off.mp4` | knob-macro ring-off render (and the synthesised click; its own audio is used) | K1: 0.5–2.9 s | V06: 0.5–2.5 s, 9:16 centre crop | not present → fallback |

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
