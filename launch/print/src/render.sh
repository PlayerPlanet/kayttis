#!/usr/bin/env bash
# Export the Hanax v2 print + social kit with headless Chrome.
# Usage: bash launch/print/src/render.sh [job ...]   (no args = everything)
# Jobs: og posters paper onepager tent social stories
# Renders: img/r/*.jpg are q92 JPEG copies of brand/renders/*.png (keeps PDFs small); see prep below.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
OUT="$(dirname "$SRC")"
ROOT="$(cd "$OUT/../.." && pwd)"
CHROME="${CHROME:-/c/Program Files/Google/Chrome/Application/chrome.exe}"
url() { echo "file:///$(cygpath -m "$SRC/$1")${2:+?$2}"; }
win() { cygpath -w "$1"; }

pdf() { # html out.pdf [query]
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw \
    --virtual-time-budget=6000 --print-to-pdf="$(win "$2")" "$(url "$1" "${3:-}")" >/dev/null 2>&1
  echo "pdf  $2"
}
png() { # html out.png width height [scale] [query]
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="${5:-1}" \
    --virtual-time-budget=6000 --window-size="$3,$4" --screenshot="$(win "$2")" "$(url "$1" "${6:-}")" >/dev/null 2>&1
  echo "png  $2"
}

prep() { # regenerate the JPEG render copies if missing
  [ -f "$SRC/img/r/hx01-hero.jpg" ] && return 0
  (cd "$ROOT" && python -c "
from PIL import Image; import os
os.makedirs('launch/print/src/img/r', exist_ok=True)
for f in ['family','hx01-exploded','hx01-front-callouts','hx01-front','hx01-hero','hx01-macro-led','hxp-front','hxp-hero','hxp-knob-macro']:
    im = Image.open(f'brand/renders/{f}.png').convert('RGBA'); bg = Image.new('RGBA', im.size, (0,0,0,255))
    Image.alpha_composite(bg, im).convert('RGB').save(f'launch/print/src/img/r/{f}.jpg', quality=92, subsampling=0)
")
}
prep

POSTERS="${POSTERS:-poster-1-ongelma poster-2-kenelle poster-3-kayttajat}"
for job in ${*:-og posters paper onepager tent social stories}; do
  case "$job" in
    og) png social-og.html "$ROOT/frontend/public/media/og-1200x630.png" 1200 630 ;;
    posters) # A2 = 420 x 594 mm = 1587 x 2245 CSS px; preview at 0.6
      for p in $POSTERS; do
        pdf "$p.html" "$OUT/hanax-$p.pdf"
        png "$p.html" "$OUT/hanax-$p.png" 1587 2245 0.6
      done ;;
    paper) # light variant for print shops with poor dark coverage
      for p in $POSTERS; do
        pdf "$p.html" "$OUT/hanax-$p-paper.pdf" paper
        png "$p.html" "$OUT/hanax-$p-paper.png" 1587 2245 0.6 paper
      done ;;
    onepager)
      pdf one-pager.html "$OUT/hanax-one-pager.pdf" paper
      png one-pager.html "$OUT/hanax-one-pager.png" 794 1123 1.5 paper ;;
    tent)
      pdf tent-card.html "$OUT/hanax-poytakyltti-a5.pdf"
      png tent-card.html "$OUT/hanax-poytakyltti-a5.png" 794 559 1.5
      pdf tent-fold.html "$OUT/hanax-poytakyltti-taitettava-a4.pdf"
      png tent-fold.html "$OUT/hanax-poytakyltti-taitettava-a4.png" 794 1123 1 ;;
    social)
      for n in 1 2 3; do png "social-ig-$n.html" "$OUT/social/hanax-ig-$n-1080x1080.png" 1080 1080; done
      png social-ig-portrait.html "$OUT/social/hanax-ig-portrait-1080x1350.png" 1080 1350
      png social-linkedin.html "$OUT/social/hanax-linkedin-1200x627.png" 1200 627 ;;
    stories)
      for n in 1 2; do png "social-story-$n.html" "$OUT/social/hanax-story-$n-1080x1920.png" 1080 1920; done ;;
    *) echo "unknown job: $job" >&2; exit 1 ;;
  esac
done
