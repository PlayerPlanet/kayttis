#!/usr/bin/env bash
# Export the Hanax print kit with headless Chrome.
# Usage: bash launch/print/src/render.sh [name ...]   (no args = everything)
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
OUT="$(dirname "$SRC")"
ROOT="$(cd "$OUT/../.." && pwd)"
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
url() { echo "file:///$(cygpath -m "$SRC/$1")"; }
win() { cygpath -w "$1"; }

pdf() { # html out.pdf
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw \
    --virtual-time-budget=4000 --print-to-pdf="$(win "$2")" "$(url "$1")" >/dev/null 2>&1
  echo "pdf  $2"
}
png() { # html out.png width height [scale]
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="${5:-1}" \
    --virtual-time-budget=4000 --window-size="$3,$4" --screenshot="$(win "$2")" "$(url "$1")" >/dev/null 2>&1
  echo "png  $2"
}

want() { [ $# -eq 0 ] || return 0; }
ALL="${*:-og posters onepager tent social}"
for job in $ALL; do
  case "$job" in
    og) png social-og.html "$ROOT/frontend/public/media/og-1200x630.png" 1200 630 ;;
    posters)
      for p in ${POSTERS:-poster-1-ongelma poster-2-kenelle poster-3-kayttajat}; do
        pdf "$p.html" "$OUT/hanax-$p.pdf"
        # A2 = 420x594 mm = 1587x2245 CSS px; preview at 0.6
        png "$p.html" "$OUT/hanax-$p.png" 1587 2245 0.6
      done ;;
    onepager)
      pdf one-pager.html "$OUT/hanax-one-pager.pdf"
      png one-pager.html "$OUT/hanax-one-pager.png" 794 1123 1 ;;
    tent)
      pdf tent-card.html "$OUT/hanax-poytakyltti-a5.pdf"
      png tent-card.html "$OUT/hanax-poytakyltti-a5.png" 794 559 1
      pdf tent-fold.html "$OUT/hanax-poytakyltti-taitettava-a4.pdf"
      png tent-fold.html "$OUT/hanax-poytakyltti-taitettava-a4.png" 794 1123 1 ;;
    social)
      for n in ${IG:-1 2 3}; do png "social-ig-$n.html" "$OUT/social/hanax-ig-$n-1080x1080.png" 1080 1080; done
      png social-ig-portrait.html "$OUT/social/hanax-ig-portrait-1080x1350.png" 1080 1350
      png social-linkedin.html "$OUT/social/hanax-linkedin-1200x627.png" 1200 627 ;;
  esac
done
