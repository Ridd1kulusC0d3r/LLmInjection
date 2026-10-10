#!/usr/bin/env python3
"""Assemble the README tour GIF from the frames written by scripts/record_tour.js (needs Pillow).

    python scripts/make_tour_gif.py tour-frames assets/explorer-tour.gif [--width 960]

Frames are scaled, quantised to one shared palette (small file, no dither noise on flat colour) and cross-faded
into the next frame so the motion reads as navigation rather than a slideshow.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("frames")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=960)
    ap.add_argument("--fade", type=int, default=2, help="cross-fade steps between frames")
    ap.add_argument("--colors", type=int, default=96)
    args = ap.parse_args()

    src = Path(args.frames)
    steps = json.loads((src / "steps.json").read_text())
    imgs = []
    for name, _ in steps:
        im = Image.open(src / name).convert("RGB")
        imgs.append(im.resize((args.width, round(im.height * args.width / im.width)), Image.LANCZOS))

    frames, durations = [], []
    for i, (im, (_, hold)) in enumerate(zip(imgs, steps, strict=True)):
        frames.append(im)
        durations.append(hold)
        nxt = imgs[(i + 1) % len(imgs)]
        for k in range(1, args.fade + 1):
            frames.append(Image.blend(im, nxt, k / (args.fade + 1)))
            durations.append(70)

    # one palette for the whole loop, sampled from several frames so every tab keeps its colours
    sample = Image.new("RGB", (args.width, imgs[0].height * 3))
    for row, idx in enumerate((0, len(imgs) // 2, len(imgs) - 1)):
        sample.paste(imgs[idx], (0, row * imgs[0].height))
    palette = sample.quantize(colors=args.colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    out = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    out[0].save(args.out, save_all=True, append_images=out[1:], duration=durations, loop=0, optimize=True, disposal=1)
    print(f"wrote {args.out}: {len(out)} frames, {args.width}px, {Path(args.out).stat().st_size / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
