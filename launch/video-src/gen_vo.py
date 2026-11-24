"""Generate the Finnish voiceover lines with Higgsfield (ElevenLabs v4, voice Helena).

    python launch/video-src/gen_vo.py [line_id ...]

Writes launch/video/in/vo/<id>.mp3 and a jobs log. Skips lines that already exist.
The claim line (vo3) was generated and picked separately (claim-helena.mp3).
"""

import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "launch" / "video" / "in" / "vo"
VOICE = {"voice_id": "3c2b83c0-2e0a-5ae8-998a-a5fe71b7eccd", "voice_type": "preset"}  # Helena
CUE = "[calm, low, unhurried] "

LINES = {
    "vo1": "Kello on viisi vaille kaksi. Bussi lähtee neljän minuutin päästä.",
    "vo2": "Ja kotiin jäi hana auki.",
    "vo4": "Pieni kamera-anturi lukee venttiilin asennon. Eteisen paneeli näyttää yhdellä vilkaisulla, mikä jäi päälle.",
    "vo5": "Sama hetki. Nyt Hanax kertoo ennen kuin lähdet. Paina nuppia, niin kaikki on pois.",
    "vo6": "Prototyyppi toimii jo killan keittiössä.",
    "vo7": "Hanax. Lähde kotoa huoletta.",
}


def hf(*args: str) -> str:
    exe = shutil.which("higgsfield") or "higgsfield"
    r = subprocess.run([exe, *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(r.stdout + r.stderr)
    return r.stdout


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    claim = OUT / "claim-helena.mp3"
    if claim.exists() and not (OUT / "vo3.mp3").exists():
        shutil.copy(claim, OUT / "vo3.mp3")
    wanted = sys.argv[1:] or list(LINES)
    log = OUT / "jobs.jsonl"
    for lid in wanted:
        dst = OUT / f"{lid}.mp3"
        if dst.exists():
            print("skip", lid)
            continue
        dialogue = json.dumps([{"text": CUE + LINES[lid], **VOICE}], ensure_ascii=False)
        res = json.loads(hf("generate", "create", "elevenlabs_v4", "--dialogue", dialogue, "--wait", "--json"))
        job = res[0] if isinstance(res, list) else res
        url = job.get("result_url")
        if job.get("status") != "completed" or not url:
            raise SystemExit(f"{lid}: {json.dumps(job)[:400]}")
        urllib.request.urlretrieve(url, dst)
        with log.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"id": lid, "job": job.get("id"), "url": url, "text": LINES[lid]}, ensure_ascii=False) + "\n")
        print("ok", lid, re.sub(r"\s+", " ", LINES[lid])[:60])


if __name__ == "__main__":
    main()
