# Promo video renderer

Renders the Explorer video tour (`site/media/llminjection-promo-{en,pt}.mp4`) frame by frame
from the live Explorer with Playwright, then encodes with ffmpeg. Deterministic: no screen recorder.

```bash
python3 scripts/build_site.py --out _site
python3 -m http.server 8765 -d _site &
cd scripts/promo && python3 render.py en && python3 render.py pt   # writes ./out/
```

Captions live in `copy.json`; title cards in `cards.html`. Requires `playwright` (chromium) and `ffmpeg`.

## Voice-over

`narrate.py` adds a local neural narration with Kokoro-82M (Apache-2.0) through `kokoro-onnx`;
no cloud TTS. Lines and start times live in `narration.json` (EN: `af_heart`, PT-BR: `pf_dora`).

```bash
pip install kokoro-onnx soundfile
npm pack kokoro-js kokoro-q8-shards           # voices (*.bin) and the q8 ONNX model in 6 shards
tar xzf kokoro-js-*.tgz && tar xzf kokoro-q8-shards-*.tgz
cat package/kokoro-q8.part{0..5}.bin > kokoro-q8.onnx   # sha256 fbae9257…a1478
python3 -c "import numpy as n,glob,os;n.savez('voices.npz',**{os.path.basename(f)[:-4]:n.fromfile(f,'f4').reshape(510,1,256) for f in glob.glob('package/voices/*.bin')})"
python3 narrate.py en --model kokoro-q8.onnx --voices voices.npz
```
