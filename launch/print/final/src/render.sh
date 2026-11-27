#!/usr/bin/env bash
# Export the final Hanax A2 poster set (01-06) with headless Chromium (Linux).
# Usage: bash launch/print/final/src/render.sh [dark|paper ...]   (no args = dark + paper)
# Output: launch/print/final/hanax-juliste-0N-*.pdf + .png preview + .jpg (A2 @ 150 dpi, 2480 x 3508) (paper variants: *-paper.*)
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
OUT="$(dirname "$SRC")"
CHROME="${CHROME:-$(ls -d "$HOME"/.cache/ms-playwright/chromium-*/chrome-linux64/chrome 2>/dev/null | tail -1)}"
[ -x "$CHROME" ] || CHROME="$(command -v chromium || command -v google-chrome)"

POSTERS="${POSTERS:-01-ongelma 02-ratkaisu 03-miten-se-toimii 04-miksi-meista 05-tarina 06-demo}"
run() { "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars --run-all-compositor-stages-before-draw \
          --virtual-time-budget=6000 "$@" >/dev/null 2>&1; }

for theme in ${*:-dark paper}; do
  q=""; suf=""; [ "$theme" = paper ] && { q="?paper"; suf="-paper"; }
  for p in $POSTERS; do
    url="file://$SRC/poster-$p.html$q"
    run --no-pdf-header-footer --print-to-pdf="$OUT/hanax-juliste-$p$suf.pdf" "$url"
    # A2 = 420 x 594 mm = 1587 x 2245 CSS px; preview at 0.6
    run --force-device-scale-factor=0.6 --window-size=1587,2245 --screenshot="$OUT/hanax-juliste-$p$suf.png" "$url"
    # print-ready JPEG: A2 at 150 dpi = 1587 CSS px * 1.5625
    tmp="$OUT/.tmp-$p$suf.png"
    run --force-device-scale-factor=1.5625 --window-size=1587,2245 --screenshot="$tmp" "$url"
    python3 -c "import sys; from PIL import Image; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[2], quality=92, dpi=(150, 150))" "$tmp" "$OUT/hanax-juliste-$p$suf.jpg"
    rm -f "$tmp"
    echo "ok   hanax-juliste-$p$suf (.pdf .png .jpg)"
  done
done
