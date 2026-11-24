# kayttis-pi

Service on the kahvibot Raspberry Pi. It collects smart-home state from **sources**, turns
raw data into device states with **plugins**, and serves them under `/api` (reached from
the internet only through the Cloudflare tunnel and the Pages demo login).

```
zigbee2mqtt (MQTT) ──▶ MqttSource ──interpreter──┐
                                                 ├──▶ StateHub ──▶ /api/devices, /api/stream
kahvi reader socket ─▶ ReaderSource ─classifier──┘     (smoothing, staleness)
                        (lights, coffee level, frames)
```

## API

| route | |
|---|---|
| `GET /api/health` | source status (MQTT connected? reader reachable?), registered plugins |
| `GET /api/devices` | every device's current `DeviceState` |
| `GET /api/devices/{id}` | one device |
| `GET /api/stream` | server-sent events: each device once, then every change (`event: device`) |
| `GET /api/camera/latest.jpg` | latest lit frame the poller already holds (headers `X-Captured-At`, `X-Frame-Age`); 503 before the first frame, 404 if `reader.serve_camera = false` |
| `GET /api/docs` | OpenAPI UI |

`DeviceState`: `id, name, kind, source, state, value, unit, confidence, attributes,
updated_at, stale`. `state` is `"unknown"` until the first reading; `stale` is true when
nothing arrived within the device's `stale_after` seconds.

## Sources

| `source` | fed by | rules |
|---|---|---|
| `mqtt` | a zigbee2mqtt topic + an **interpreter** | subscribe only, never publish (`.../set` would switch the coffee machines' plugs) |
| `frame` | a **classifier** on the reader's latest frame | never touches the camera: a frame is requested only while a lit frame younger than `dark_after` exists, so the reader answers from memory; each frame (reader `seq`) is processed once |
| `reader` | `signal = "lights"` (reader's lit/dark) or `"coffee_level"` (its ml reading for `side`) | abstained readings are skipped; a stalled reader (seq not advancing) makes devices go stale instead of guessing |

## Plugins

Built-in interpreters: `power_levels` (plug watts -> off/on/brewing), `threshold`
(number vs threshold -> on/off), `mapping` (discrete field -> state), `value` (pass a number through).
Built-in classifiers: `tap_knob`, `linear_crop` (any model trained with the tool below).

A config can also point at any import path, so new plugins need no change to the service:

```python
# e.g. packages/sensors/src/kayttis_sensors/oven.py (a new workspace package)
from kayttis_core import Observation


def oven_glow(box=(300, 300, 360, 340), threshold=180):
    def classify(image):  # full RGB PIL frame
        r, g, b = image.crop(box).resize((1, 1)).getpixel((0, 0))
        return Observation(state="on" if r > threshold else "off", value=r)

    return classify
```

```toml
[[devices]]
id = "oven"
name = "Uuni"
kind = "oven"
source = "frame"
classifier = "kayttis_sensors.oven:oven_glow"
params = { threshold = 200 }
```

Return `Observation(state=None)` when the thing can't be seen: the device keeps its last
state (and goes stale after `stale_after`). `smooth_window = N` takes a majority over the
last N visible states. Interpreters work the same way with `interpreter = "pkg.mod:factory"`,
receiving the decoded JSON payload. `@register_interpreter` / `@register_classifier` give
plugins a short name instead.

## The tap-knob classifier

Fixed crop (745, 225)–(835, 295) of the 1280×720 frame, HOG + colour thumbnail, logistic
regression; ~3 ms per frame. 95% on held-out frames, **but every "open" example comes from
one ~3 h episode on 2026-09-03**: treat it as a prototype until more open runs are labelled.
If the camera is re-aimed the crop must be moved (`params = { box = [...] }`) or retrained.

Retrain (frames are not in the repo; labels are in `data/tap_knob/labels.csv`):

```sh
uv run python services/pi/tools/train_crop_classifier.py \
  --labels services/pi/data/tap_knob/labels.csv --frames <frames dir> \
  --box 745 225 835 295 --test-from 2026-09-06 --test-window 2026-09-03_10-50 2026-09-03_14 \
  --out services/pi/src/kayttis_pi/models/tap_knob.npz
```

## Running

```sh
# on the Pi (systemd: deploy/pi/kayttis-pi.service)
uv run kayttis-pi --config services/pi/config.toml

# locally, without kahvibot: a fake reader serving JPEGs from a folder
uv run kayttis-fake-reader <frames dir> --interval 3
uv run kayttis-pi --config services/pi/config.dev.toml
curl localhost:8000/api/devices
```
