# Hanax: Google AI Studio prompt pack

For generating cinematic imagery and B-roll in **Google AI Studio** (aistudio.google.com):
- **Images:** the Gemini image model ("Nano Banana") accepts reference images. Use it for the product shots so the device stays on-model.
- **Video:** Veo, image-to-video from our renders or from the images below.

## How to use

1. **Reference images.** For every prompt marked **REF**, attach the listed file from `brand/renders/` (the 3D concept-model renders) as a reference image, and keep the sentence *"Keep the device exactly as in the reference image"*.
2. **Aspect ratio.** Generate **16:9** first. Then, where noted, a **9:16** version for the teaser and social.
3. **Generate 3–4 variants** of each and keep the best one. Reject any where:
   - the device changed shape
   - there is extra text or a logo
   - there is a second coloured light
   - hands or faces look wrong
4. **Save** into this folder (`launch/ai-studio/`) with the **exact filename** given. The landing page, deck, posters and video pick them up by name. Tell Claude when they are in.
5. **What not to make with AI:** anything that claims to be *real proof*. The proof shots (the live screen, the real kitchen, the ESP32-CAM on the table) must be real photos or recordings. Everything below is **concept imagery** and gets labelled *konseptikuva*.

## Shared style block

Append this to every prompt:

> Cinematic product photography in the style of a premium deep-tech hardware launch (Figure, Oura, Teenage Engineering). Near-monochrome: graphite black, brushed anodised aluminium, frosted dark glass, titanium. The ONLY colour in the frame is a small warm amber indicator light (#FF9A2E) and its soft glow. Low-key lighting: one soft key light from the upper side, a thin rim light, deep falloff into black, subtle film grain, shallow depth of field, 35–85 mm lens look. Scandinavian home, calm, quiet, evening. No text, no letters, no logos, no UI text, no watermarks, no blue or purple light, no green light, no neon, no people's faces in focus.

## Stills (Gemini image)

### S1 `s1-sensor-on-valve.png`: the claim
**REF:** `brand/renders/hx01-hero.png`
> A small square graphite sensor device (keep the device exactly as in the reference image) clipped to the chrome body of an ordinary kitchen faucet's dishwasher shut-off valve, under a stainless steel sink, a Finnish kitchen at night. The sensor's amber indicator light is on and casts a faint warm reflection on the chrome. Macro product shot, device sharp, background tiles falling into darkness. [style block]

9:16 variant: `s1-sensor-on-valve-9x16.png`

### S2 `s2-panel-hallway.png`: the hero environment
**REF:** `brand/renders/hxp-hero.png`
> A slim dark wall-mounted control panel with a titanium knob on its right side (keep the device exactly as in the reference image) mounted at eye level in the entrance hall of a Finnish detached house, beside the front door, at blue-hour dusk. Coats on hooks soft and out of focus, a warm window glow far behind. The panel screen glows softly, the amber ring around the knob is lit. Wide 3/4 composition with the panel on the right third and generous negative space on the left for a headline. [style block]

9:16 variant: `s2-panel-hallway-9x16.png`, with the panel in the lower half and empty dark wall above.

### S3 `s3-hand-knob.png`: the one action
**REF:** `brand/renders/hxp-knob-macro.png`
> Extreme close-up of a hand (fingertips only, no face) pressing a knurled titanium knob on the side of a dark wall panel (keep the knob exactly as in the reference image). The thin amber light ring around the knob is turning off; the moment of switching everything off. Very shallow depth of field, rim light on the knurling. [style block]

### S4 `s4-water-macro.png`: the problem (no device)
> Macro of a thin stream of water running from a chrome kitchen tap into a dark steel sink, frozen droplets, a dark kitchen at night. A single small amber light far out of focus in the background as a bokeh dot. Tense, quiet mood. [style block]

9:16 variant: `s4-water-macro-9x16.png`

### S5 `s5-stove-glow.png`: the problem (no device)
> Low-angle close-up of the control knobs of a white electric stove in a dark kitchen; one small amber indicator light glowing on the control panel is the only light source. Long shadows. [style block, but allow the white enamel]

### S6 `s6-leaving-home.png`: the outcome
> Back view of a person in a dark wool coat walking away from a modern Finnish detached house at dusk towards a bus stop, a phone in hand with its screen softly lit. The house's entrance light is warm, the rest blue-grey. Wide cinematic shot, calm, no face visible. [style block]

### S7 `s7-family-studio.png`: the product family
**REF:** `brand/renders/family.png`
> Studio hero shot of two devices, a small square sensor and a slim wall panel with a titanium knob (keep both exactly as in the reference image), on a dark graphite plinth, a single sweeping light from the left, amber indicators lit, reflections on a dark glossy floor. Apple-keynote-level product photography. [style block]

## Video (Veo, image-to-video)

Keep clips 6–8 s and 16:9 (plus 9:16 where noted). Turn on audio only where described. Save as MP4 with the given name.

### V1 `v1-panel-reveal.mp4`: the hero shot
**Start frame:** `s2-panel-hallway.png` (or `brand/renders/hxp-hero.png`)
> Very slow dolly-in towards the wall panel. A soft light sweeps across its glass, the screen gently brightens, the amber ring around the knob lights up near the end. Static scene, no people. Ambient audio: quiet house, a distant clock ticking.

### V2 `v2-valve-rackfocus.mp4`: the claim in motion
**Start frame:** `s1-sensor-on-valve.png`
> Slow rack focus from the running water in the background to the small sensor on the valve; its amber indicator light pulses once. Audio: soft running water.

### V3 `v3-water-tension.mp4`: the disaster B-roll
**Start frame:** `s4-water-macro.png`
> Locked-off macro of the tap running, the camera pushes in imperceptibly, the water sound grows. No people. Audio: running water, a clock ticking.

### V4 `v4-knob-off.mp4`: the action
**Start frame:** `s3-hand-knob.png`
> Fingertips press the knob, the amber ring fades out, the scene settles into calm darkness. Audio: a soft mechanical click, then near silence.

9:16 variants for the teaser (crop-safe framing, subject centred): `v1-panel-reveal-9x16.mp4`, `v3-water-tension-9x16.mp4`.

## Real proof: shoot these yourself on Friday (not AI)

These carry the credibility, like Figure's BMW footage or π₀'s laundry. Shoot them on a phone in 4K, steady, in good light. AirDrop or USB the **original files**; Telegram compresses them.

1. **P1 · The real kitchen valve:** the tap and the dishwasher valve with the red tape, then a hand turns it open and closed. Hold each state 3 s.
2. **P2 · The live screen:** a screen recording of `kayttis.kiirikki.fi/app/` while P1 happens (the valve changes, the state updates). Keep the clock visible.
3. **P3 · Raw components:** the ESP32-CAM and the components on a dark table, one desk lamp from the side. A slow phone push-in, plus a top-down still.
4. **P4 · ESP32-CAM aimed at the valve:** the board held or taped where the HX-01 would sit.
5. **P5 · The coffee machine plug:** a smart plug on a coffee machine with the machine switching on, and the app's power reading changing.
