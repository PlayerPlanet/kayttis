"""Generate sound effects with Higgsfield (Mirelo text-to-audio, 0.25 credits / s).

    python launch/video-src/gen_sfx.py [sfx_id ...]

Writes launch/video/in/sfx/<id>.<ext>; skips existing files. Checks the cost first.
"""

import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "launch" / "video" / "in" / "sfx"

SFX = {
    "door-slam": (2, "A heavy wooden front door of a Finnish house slammed shut from inside a hallway, sharp impact, short wooden rattle, then quiet room. Close mic, no music, no voices."),
    "water-run": (5, "Kitchen tap running steadily into a stainless steel sink, continuous water stream splashing, quiet kitchen room tone. No music, no voices."),
    "stove-click": (2, "Close-up of an electric stove's rotary control knob turned off: a firm plastic click, a faint relay tick. Quiet kitchen. No music, no voices."),
    "knob-detent": (2, "Premium machined aluminium rotary knob pressed and clicked once: a precise, solid, satisfying mechanical click with a tiny metallic resonance. High-end hardware product sound. No music."),
    "rewind": (2, "Cinematic tape-rewind whoosh, fast reverse swoosh rising in pitch, clean and modern. No music, no voices."),
    "impact-low": (3, "Deep, clean cinematic low-frequency impact hit with a soft sub-bass tail, minimal and modern, for a tech product title reveal. No music, no voices."),
    "confirm": (2, "A soft, warm two-note electronic confirmation tone from a premium smart-home panel, gentle and calm, short decay. No voices."),
}


def hf(*args: str) -> str:
    exe = shutil.which("higgsfield") or "higgsfield"
    r = subprocess.run([exe, *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(r.stdout + r.stderr)
    return r.stdout


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    wanted = sys.argv[1:] or list(SFX)
    total = 0.0
    for sid in wanted:
        dur, prompt = SFX[sid]
        if list(OUT.glob(f"{sid}.*")):
            print("skip", sid)
            continue
        cost = hf("generate", "cost", "mirelo_text_to_audio", "--prompt", prompt, "--duration", str(dur)).strip().splitlines()[-1]
        res = json.loads(hf("generate", "create", "mirelo_text_to_audio", "--prompt", prompt,
                            "--duration", str(dur), "--wait", "--json"))
        job = res[0] if isinstance(res, list) else res
        url = job.get("result_url")
        if job.get("status") != "completed" or not url:
            raise SystemExit(f"{sid}: {json.dumps(job)[:400]}")
        ext = url.split("?")[0].rsplit(".", 1)[-1][:4]
        urllib.request.urlretrieve(url, OUT / f"{sid}.{ext}")
        with (OUT / "jobs.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps({"id": sid, "job": job.get("id"), "url": url, "cost": cost, "prompt": prompt}) + "\n")
        total += float(cost.split()[0])
        print("ok", sid, cost)
    print(f"spent ~{total:.2f} credits")


if __name__ == "__main__":
    main()
