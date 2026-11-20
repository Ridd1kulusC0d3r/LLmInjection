#!/usr/bin/env python3
"""Draw the masthead SVG for each intelligence product, in the banner's analyst-desk style (stdlib only).

    python scripts/build_report_mastheads.py                 # the four product mastheads
    python scripts/build_report_mastheads.py --kind dossier --title "ARTEX" --out assets/reports/artex.svg
"""

from __future__ import annotations

import argparse
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
KINDS = {
    "report": ("RELATÓRIO DE INTELIGÊNCIA", "Um achado, julgamentos com confiança, o que fazer."),
    "landscape": ("THREAT LANDSCAPE MENSAL", "O mês em dados: o que mudou e o que vem."),
    "trends": ("TENDÊNCIAS DA SEMANA", "Sete digests, uma tese, um contraponto."),
    "dossier": ("DOSSIÊ", "Uma ferramenta ou campanha, todos os atores, toda a evidência."),
}


def masthead(kind: str, title: str) -> str:
    label, tagline = KINDS[kind]
    t, lab, tag = escape(title), escape(label), escape(tagline)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="220" viewBox="0 0 1280 220" role="img" aria-labelledby="t">
  <title id="t">LLMInjection {lab}: {t}</title>
  <rect width="1280" height="220" fill="#f3f0e8"/>
  <rect x="0.5" y="0.5" width="1279" height="219" fill="none" stroke="#17150f"/>
  <g font-family="'Courier New',Courier,monospace" font-size="12" letter-spacing="2" fill="#4a463c" font-weight="700">
    <text x="48" y="40">LLMINJECTION / {lab}</text>
    <text x="1232" y="40" text-anchor="end" fill="#b43c0e">TLP:CLEAR</text>
  </g>
  <line x1="48" y1="56" x2="1232" y2="56" stroke="#17150f"/>
  <text x="48" y="128" font-family="Georgia,'Times New Roman',serif" font-size="58" font-weight="700" fill="#17150f" letter-spacing="-1">{t}</text>
  <text x="50" y="168" font-family="Georgia,'Times New Roman',serif" font-size="21" font-style="italic" fill="#4a463c">{tag}</text>
  <line x1="50" y1="192" x2="170" y2="192" stroke="#b43c0e" stroke-width="4"/>
  <g transform="translate(1012 82)">
    <rect width="220" height="104" fill="#fbf9f3" stroke="#17150f"/>
    <g fill="#cfc9ba"><rect x="16" y="16" width="120" height="6"/><rect x="16" y="32" width="188" height="4"/></g>
    <rect x="16" y="46" width="96" height="11" fill="#17150f"/><rect x="120" y="49" width="84" height="4" fill="#cfc9ba"/>
    <rect x="16" y="66" width="188" height="16" fill="#b43c0e"/>
    <text x="22" y="78" font-family="'Courier New',Courier,monospace" font-size="9" font-weight="700" fill="#fff" letter-spacing="1">TREAT AS DATA</text>
    <rect x="16" y="90" width="64" height="5" fill="#17150f"/>
  </g>
</svg>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--kind", choices=sorted(KINDS))
    ap.add_argument("--title")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    if a.kind:
        out = a.out or ROOT / "assets" / "reports" / f"{a.kind}.svg"
        out.write_text(masthead(a.kind, a.title or KINDS[a.kind][0].title()), encoding="utf-8")
        return 0
    defaults = {"report": "Relatório de inteligência", "landscape": "Threat Landscape de IA",
                "trends": "Tendências da semana", "dossier": "Dossiê de ameaça"}
    for kind, title in defaults.items():
        (ROOT / "assets" / "reports" / f"masthead-{kind}.svg").write_text(masthead(kind, title), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
