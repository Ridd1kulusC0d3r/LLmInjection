#!/usr/bin/env python3
"""Render the technique coverage matrix as a static SVG for the README (stdlib only).

Counts come from data/relationships.json, the same way the Explorer computes them:
validates -> tests, detects -> detections, mitigated-by -> controls.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "coverage-matrix.svg"
COLS = [("validates", "TESTS"), ("detects", "DETECTIONS"), ("mitigated-by", "CONTROLS")]
FILLS = ["none", "#e9b394", "#d4804f", "#b43c0e", "#7c2406"]  # one hue, light to dark
TEXT_ON = ["#7b766a", "#17150f", "#ffffff", "#ffffff", "#ffffff"]


def load(name: str):
    return json.loads((ROOT / "data" / f"{name}.json").read_text(encoding="utf-8"))


def build() -> str:
    techniques = load("techniques")
    rels = load("relationships")

    def count(tid: str, rel: str) -> int:
        return sum(1 for r in rels if r["relationship"] == rel and tid in (r["source"], r["target"]))

    row_h, top, left, col_w = 26, 92, 40, 92
    name_w = 400
    width = left + name_w + col_w * len(COLS) + 250
    height = top + row_h * len(techniques) + 56
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t">',
        '<title id="t">Technique coverage: linked tests, detections and controls per technique</title>',
        f'<rect width="{width}" height="{height}" fill="#f3f0e8"/>',
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" fill="none" stroke="#17150f"/>',
        '<g font-family="Georgia,serif" fill="#17150f">',
        f'<text x="{left}" y="44" font-size="22" font-weight="700">Technique coverage</text></g>',
        f'<text x="{left}" y="64" font-family="\'Courier New\',monospace" font-size="11" fill="#7b766a">'
        'Linked tests, detections and controls per technique. Flagged rows have a gap.</text>',
        '<g font-family="\'Courier New\',monospace" font-size="11" font-weight="700" letter-spacing="1.5" fill="#4a463c">',
    ]
    for i, (_, label) in enumerate(COLS):
        out.append(f'<text x="{left + name_w + i * col_w + col_w / 2}" y="{top - 14}" text-anchor="middle">{label}</text>')
    out.append("</g>")
    out.append(f'<line x1="{left}" x2="{width - left}" y1="{top - 6}" y2="{top - 6}" stroke="#17150f"/>')
    for r, tech in enumerate(techniques):
        y = top + r * row_h
        counts = [count(tech["id"], rel) for rel, _ in COLS]
        gap = " / ".join(g for g, c in (("no test", counts[0]), ("no detection", counts[1])) if not c)
        out.append(
            f'<text x="{left}" y="{y + 17}" font-family="system-ui,Helvetica,Arial,sans-serif" font-size="13" fill="#17150f">'
            f'<tspan font-family="\'Courier New\',monospace" font-size="10" fill="#7b766a">{escape(tech["id"][-4:])}  </tspan>{escape(tech["name"])}</text>'
        )
        for i, n in enumerate(counts):
            level = min(n, 4)
            cx = left + name_w + i * col_w + col_w / 2
            if n:
                out.append(f'<rect x="{cx - 17}" y="{y + 3}" width="34" height="20" fill="{FILLS[level]}"/>')
            else:
                out.append(f'<rect x="{cx - 17}" y="{y + 3}" width="34" height="20" fill="none" stroke="#cfc9ba" stroke-dasharray="3 2"/>')
            out.append(
                f'<text x="{cx}" y="{y + 18}" text-anchor="middle" font-family="\'Courier New\',monospace" font-size="12" '
                f'font-weight="700" fill="{TEXT_ON[level]}">{n}</text>'
            )
        if gap:
            out.append(
                f'<text x="{left + name_w + col_w * len(COLS) + 18}" y="{y + 17}" font-family="\'Courier New\',monospace" '
                f'font-size="10" font-weight="700" letter-spacing="1" fill="#b43c0e">{escape(gap.upper())}</text>'
            )
        out.append(f'<line x1="{left}" x2="{width - left}" y1="{y + row_h}" y2="{y + row_h}" stroke="#e0dacb"/>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
