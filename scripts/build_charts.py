#!/usr/bin/env python3
"""Render the README charts as static SVGs (stdlib only).

    coverage-matrix.svg    technique x (evidence, tests, detections, controls, tools)
    framework-coverage.svg technique x framework mapping
    ecosystem-map.svg      evidence class x ecosystem section

All figures come from the datasets, the same way the Explorer computes them.
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, load_data  # noqa: E402
from readme_stats import EVIDENCE_CLASSES, SECTIONS  # noqa: E402

OUT = ROOT / "assets"
PAPER, INK, INK2, INK3, RULE, RULE2, SIGNAL = "#f3f0e8", "#17150f", "#4a463c", "#7b766a", "#cfc9ba", "#e0dacb", "#b43c0e"
FILLS = ["none", "#e9b394", "#d4804f", "#b43c0e", "#7c2406"]  # one hue, light to dark
TEXT_ON = [INK3, INK, "#ffffff", "#ffffff", "#ffffff"]
MONO = "'Courier New',monospace"
SERIF = "Georgia,serif"
SANS = "system-ui,Helvetica,Arial,sans-serif"
EVIDENCE_PREFIXES = ("CAMPAIGN-", "INCIDENT-", "VULN-")


def frame(width: int, height: int, title: str, subtitle: str, label: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t">',
        f"<title id=\"t\">{escape(label)}</title>",
        f'<rect width="{width}" height="{height}" fill="{PAPER}"/>',
        f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" fill="none" stroke="{INK}"/>',
        f'<text x="40" y="44" font-family="{SERIF}" font-size="22" font-weight="700" fill="{INK}">{escape(title)}</text>',
        f'<text x="40" y="64" font-family="{MONO}" font-size="11" fill="{INK3}">{escape(subtitle)}</text>',
    ]


def heat(out: list[str], cx: float, y: float, n: int, w: int = 34) -> None:
    level = min(n, 4)
    if n:
        out.append(f'<rect x="{cx - w / 2}" y="{y + 3}" width="{w}" height="20" fill="{FILLS[level]}"/>')
    else:
        out.append(f'<rect x="{cx - w / 2}" y="{y + 3}" width="{w}" height="20" fill="none" stroke="{RULE}" stroke-dasharray="3 2"/>')
    out.append(f'<text x="{cx}" y="{y + 18}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{TEXT_ON[level]}">{n}</text>')


def legend(out: list[str], x: float, y: float, note: str) -> None:
    out.append(f'<text x="{x}" y="{y + 11}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1" fill="{INK2}">SCALE</text>')
    for i, label in enumerate(["0", "1", "2", "3", "4+"]):
        cx = x + 64 + i * 40
        if i == 0:
            out.append(f'<rect x="{cx - 14}" y="{y}" width="28" height="16" fill="none" stroke="{RULE}" stroke-dasharray="3 2"/>')
        else:
            out.append(f'<rect x="{cx - 14}" y="{y}" width="28" height="16" fill="{FILLS[i]}"/>')
        out.append(f'<text x="{cx}" y="{y + 12}" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="{TEXT_ON[i]}">{label}</text>')
    out.append(f'<text x="{x + 290}" y="{y + 12}" font-family="{MONO}" font-size="10" fill="{INK3}">{escape(note)}</text>')


def col_header(out: list[str], x: float, y: float, label: str) -> None:
    out.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1.5" fill="{INK2}">{escape(label)}</text>')


def group_header(out: list[str], x1: float, x2: float, y: float, label: str) -> None:
    out.append(f'<text x="{(x1 + x2) / 2}" y="{y - 6}" text-anchor="middle" font-family="{MONO}" font-size="9" font-weight="700" letter-spacing="2" fill="{INK3}">{escape(label)}</text>')
    out.append(f'<line x1="{x1 + 6}" x2="{x2 - 6}" y1="{y}" y2="{y}" stroke="{INK}" stroke-width="1.5"/>')


def technique_stats() -> list[dict]:
    techniques, rels, eco = load_data("techniques"), load_data("relationships"), load_data("ecosystem")
    rows = []
    for t in techniques:
        tid = t["id"]
        linked = [r for r in rels if tid in (r["source"], r["target"])]

        others = [r["target"] if r["source"] == tid else r["source"] for r in linked]
        evidence = {o for o in others if o.startswith(EVIDENCE_PREFIXES)}
        rows.append({
            "id": tid, "name": t["name"], "mappings": t["mappings"],
            "evidence": len(evidence),
            "tests": sum(1 for r in linked if r["relationship"] == "validates"),
            "detections": sum(1 for r in linked if r["relationship"] == "detects"),
            "controls": sum(1 for r in linked if r["relationship"] == "mitigated-by"),
            "tools": sum(1 for e in eco if tid in e.get("techniques", [])),
        })
    return rows


def coverage_matrix() -> str:
    rows = technique_stats()
    cols = [("evidence", "EVIDENCE"), ("tests", "TESTS"), ("detections", "DETECTIONS"), ("controls", "CONTROLS"), ("tools", "TOOLS")]
    row_h, top, left, name_w, col_w, flag_w = 26, 112, 40, 392, 92, 300
    width = left + name_w + col_w * len(cols) + flag_w
    height = top + row_h * len(rows) + 92
    full = sum(1 for r in rows if r["tests"] and r["detections"] and r["controls"])
    observed_gap = sum(1 for r in rows if r["evidence"] and not (r["tests"] and r["detections"]))
    out = frame(width, height, "Technique coverage", "Evidence, tests, detections, controls and tools per technique.",
                "Technique coverage matrix: evidence, tests, detections, controls and tools per technique")
    # summary block, top right
    sx = width - left
    out.append(f'<text x="{sx}" y="44" text-anchor="end" font-family="{MONO}" font-size="22" font-weight="700" fill="{INK}">{full}<tspan font-size="12" fill="{INK3}"> / {len(rows)} fully covered</tspan></text>')
    out.append(f'<text x="{sx}" y="64" text-anchor="end" font-family="{MONO}" font-size="11" font-weight="700" fill="{SIGNAL}">{observed_gap} techniques with linked evidence lack a test or detection</text>')
    x0 = left + name_w
    group_header(out, x0, x0 + col_w, top - 28, "THREAT")
    group_header(out, x0 + col_w, x0 + 4 * col_w, top - 28, "DEFENCE")
    group_header(out, x0 + 4 * col_w, x0 + 5 * col_w, top - 28, "ECOSYSTEM")
    for i, (_, label) in enumerate(cols):
        col_header(out, x0 + i * col_w + col_w / 2, top - 12, label)
    out.append(f'<line x1="{left}" x2="{width - left}" y1="{top - 6}" y2="{top - 6}" stroke="{INK}"/>')
    flag_x = x0 + col_w * len(cols) + 18
    for r, row in enumerate(rows):
        y = top + r * row_h
        out.append(
            f'<text x="{left}" y="{y + 17}" font-family="{SANS}" font-size="13" fill="{INK}">'
            f'<tspan font-family="{MONO}" font-size="10" fill="{INK3}">{escape(row["id"][-4:])}  </tspan>{escape(row["name"])}</text>'
        )
        for i, (key, _) in enumerate(cols):
            heat(out, x0 + i * col_w + col_w / 2, y, row[key])
        gaps = [g for g, ok in (("no test", row["tests"]), ("no detection", row["detections"])) if not ok]
        if gaps:
            priority = row["evidence"] > 0
            text = ("PRIORITY GAP: " if priority else "") + " / ".join(gaps).upper()
            out.append(f'<text x="{flag_x}" y="{y + 17}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1" fill="{SIGNAL if priority else INK3}">{escape(text)}</text>')
        out.append(f'<line x1="{left}" x2="{width - left}" y1="{y + row_h}" y2="{y + row_h}" stroke="{RULE2}"/>')
    ly = top + row_h * len(rows) + 22
    legend(out, left, ly, "Evidence: linked campaigns, incidents and vulnerabilities. Tools: mapped ecosystem projects.")
    out.append(f'<text x="{left}" y="{ly + 40}" font-family="{MONO}" font-size="10" fill="{INK3}">Counted from data/relationships.json and data/ecosystem.json. Regenerate with make charts.</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def framework_coverage() -> str:
    rows = technique_stats()
    frameworks = sorted({m for r in rows for m in r["mappings"]}, key=lambda m: -sum(m in r["mappings"] for r in rows))
    row_h, top, left, name_w, col_w = 26, 112, 40, 392, 104
    width = left + name_w + col_w * len(frameworks) + 90
    height = top + row_h * len(rows) + 90
    out = frame(width, height, "Framework mapping", "Which external frameworks each LLMInjection technique maps to.", "Technique to framework mapping matrix")
    x0 = left + name_w
    for i, fw in enumerate(frameworks):
        label = fw.replace("MITRE ", "").replace("NIST AI 100-2e2025", "NIST AML").replace("Google ", "").replace("OWASP Agentic", "OWASP AGENTIC").upper()
        col_header(out, x0 + i * col_w + col_w / 2, top - 12, label)
    col_header(out, x0 + len(frameworks) * col_w + 45, top - 12, "TOTAL")
    out.append(f'<line x1="{left}" x2="{width - left}" y1="{top - 6}" y2="{top - 6}" stroke="{INK}"/>')
    for r, row in enumerate(rows):
        y = top + r * row_h
        out.append(f'<text x="{left}" y="{y + 17}" font-family="{SANS}" font-size="13" fill="{INK}"><tspan font-family="{MONO}" font-size="10" fill="{INK3}">{escape(row["id"][-4:])}  </tspan>{escape(row["name"])}</text>')
        for i, fw in enumerate(frameworks):
            cx = x0 + i * col_w + col_w / 2
            if fw in row["mappings"]:
                out.append(f'<rect x="{cx - 8}" y="{y + 5}" width="16" height="16" fill="{INK}"/>')
            else:
                out.append(f'<rect x="{cx - 8}" y="{y + 5}" width="16" height="16" fill="none" stroke="{RULE}" stroke-dasharray="3 2"/>')
        heat(out, x0 + len(frameworks) * col_w + 45, y, len(row["mappings"]))
        out.append(f'<line x1="{left}" x2="{width - left}" y1="{y + row_h}" y2="{y + row_h}" stroke="{RULE2}"/>')
    by = top + row_h * len(rows) + 22
    out.append(f'<text x="{left}" y="{by + 12}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1" fill="{INK2}">TECHNIQUES MAPPED</text>')
    for i, fw in enumerate(frameworks):
        out.append(f'<text x="{x0 + i * col_w + col_w / 2}" y="{by + 12}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{INK}">{sum(fw in r["mappings"] for r in rows)}</text>')
    out.append(f'<text x="{left}" y="{by + 38}" font-family="{MONO}" font-size="10" fill="{INK3}">Filled square: mapped. Dashed: not mapped. Exact and related relations are listed in data/techniques.json.</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def ecosystem_map() -> str:
    eco = load_data("ecosystem")
    classes, sections = list(EVIDENCE_CLASSES), list(SECTIONS)
    row_h, top, left, name_w, col_w = 28, 112, 40, 250, 92
    width = left + name_w + col_w * len(sections) + col_w + 40
    height = top + row_h * len(classes) + 120
    out = frame(width, height, "Ecosystem map", f"{len(eco)} related projects by evidence class and section. Class decides what a project can support.", "Ecosystem projects by evidence class and section")
    x0 = left + name_w
    short = {"knowledge": "KNOWLEDGE", "catalog": "CATALOGS", "evaluation": "EVALUATION", "benchmark": "BENCHMARKS", "attack-research": "ATTACK R&D", "defence": "DEFENCE", "agent-security": "AGENTS", "lab": "LABS"}
    for i, s in enumerate(sections):
        col_header(out, x0 + i * col_w + col_w / 2, top - 12, short[s])
    col_header(out, x0 + len(sections) * col_w + col_w / 2, top - 12, "TOTAL")
    out.append(f'<line x1="{left}" x2="{width - left}" y1="{top - 6}" y2="{top - 6}" stroke="{INK}"/>')
    for r, cls in enumerate(classes):
        y = top + r * row_h
        out.append(f'<text x="{left}" y="{y + 18}" font-family="{SANS}" font-size="13" fill="{INK}">{escape(EVIDENCE_CLASSES[cls][0])}</text>')
        for i, s in enumerate(sections):
            heat(out, x0 + i * col_w + col_w / 2, y, sum(1 for e in eco if e["evidence_class"] == cls and e["section"] == s))
        heat(out, x0 + len(sections) * col_w + col_w / 2, y, sum(1 for e in eco if e["evidence_class"] == cls), 40)
        out.append(f'<line x1="{left}" x2="{width - left}" y1="{y + row_h}" y2="{y + row_h}" stroke="{RULE2}"/>')
    ly = top + row_h * len(classes) + 22
    legend(out, left, ly, "Cells count projects. A dashed cell means none.")
    out.append(f'<text x="{left}" y="{ly + 40}" font-family="{MONO}" font-size="10" fill="{INK3}">No project in this map can support attribution or campaign claims. See docs/ECOSYSTEM.md.</text>')
    out.append(f'<text x="{left}" y="{ly + 56}" font-family="{MONO}" font-size="10" fill="{INK3}">Provenance: maintainer research, 2026-10-07. Repository state not independently verified.</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


CHARTS = {"coverage-matrix.svg": coverage_matrix, "framework-coverage.svg": framework_coverage, "ecosystem-map.svg": ecosystem_map}


def build_all() -> dict[str, str]:
    return {name: render() for name, render in CHARTS.items()}


if __name__ == "__main__":
    for name, svg in build_all().items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"Wrote assets/{name}")
