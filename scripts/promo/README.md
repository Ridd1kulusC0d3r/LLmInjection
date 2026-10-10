# Promo video renderer

Renders the Explorer video tour (`site/media/llminjection-promo-{en,pt}.mp4`) frame by frame
from the live Explorer with Playwright, then encodes with ffmpeg. Deterministic: no screen recorder.

```bash
python3 scripts/build_site.py --out _site
python3 -m http.server 8765 -d _site &
cd scripts/promo && python3 render.py en && python3 render.py pt   # writes ./out/
```

Captions live in `copy.json`; title cards in `cards.html`. Requires `playwright` (chromium) and `ffmpeg`.
