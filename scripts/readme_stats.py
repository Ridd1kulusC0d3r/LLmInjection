#!/usr/bin/env python3
"""Keep the generated blocks of README.md and docs/ECOSYSTEM.md in sync with the datasets (stdlib only).

Blocks sit between <!-- gen:NAME:start --> and <!-- gen:NAME:end --> markers.

    python scripts/readme_stats.py          # rewrite all blocks
    python scripts/readme_stats.py --check  # exit 1 if any block is stale
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, load_data  # noqa: E402

README = ROOT / "README.md"
FILES = [README, ROOT / "README.pt-BR.md", ROOT / "docs" / "ECOSYSTEM.md"]

GROUPS = [
    [("Actors", "actors"), ("Campaigns", "campaigns"), ("Incidents", "incidents"),
     ("Vulnerabilities", "vulnerabilities"), ("Techniques", "techniques"), ("Sources", "sources")],
    [("Test cases", "test-cases"), ("Detections", "detections"), ("Controls", "controls"),
     ("Frameworks", "frameworks"), ("Model families", "models"), ("Relationships", "relationships"),
     ("Ecosystem repos", "ecosystem")],
]


load = load_data


def cell(value, limit: int = 0) -> str:
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    text = re.sub(r"\s+", " ", str(value if value is not None else "")).strip().replace("|", "\\|")
    if limit and len(text) > limit:
        text = text[: limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return text


def table(headers: list[str], rows: list[list[str]], align_center: bool = False) -> str:
    rule = "|" + (":---:|" if align_center else "---|") * len(headers)
    lines = ["| " + " | ".join(headers) + " |", rule]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)


def stats() -> str:
    out = []
    for group in GROUPS:
        out.append(table([label for label, _ in group], [[f"**{len(load(key))}**" for _, key in group]], True))
    return "\n\n".join(out)


PT_LABELS = {"actors": "Atores", "campaigns": "Campanhas", "incidents": "Incidentes", "vulnerabilities": "Vulnerabilidades", "techniques": "Técnicas",
             "sources": "Fontes", "test-cases": "Casos de teste", "detections": "Detecções", "controls": "Controles", "frameworks": "Frameworks",
             "models": "Famílias de modelos", "relationships": "Relações", "ecosystem": "Projetos do ecossistema"}


def stats_pt() -> str:
    out = []
    for group in GROUPS:
        out.append(table([PT_LABELS[key] for _, key in group], [[f"**{len(load(key))}**" for _, key in group]], True))
    return "\n\n".join(out)


MATURITY_MEANING = {
    "observed-in-the-wild": "Linked to a campaign, or to an incident whose status is observed",
    "disclosed-vulnerability": "Linked to a vulnerability record (CVE, GHSA or malicious package)",
    "research-demonstrated": "Linked to a research or lab incident, or mapped by a research or benchmark project",
    "no-linked-evidence": "Nothing in this repository links to it yet. Not a claim that it is theoretical",
}


def maturity() -> str:
    techniques = load("techniques")
    rows = []
    for level, meaning in MATURITY_MEANING.items():
        ids = [t["id"][-4:] for t in techniques if t.get("maturity") == level]
        rows.append([f"`{level}`", meaning, str(len(ids)), cell(ids)])
    return table(["Maturity", "Derived from", "Techniques", "IDs"], rows)


def actors() -> str:
    return table(["Actor", "Nexus", "AI role", "Activity", "Confidence"],
                 [[f"**{cell(a['name'])}**", cell(a["nexus"]), cell(a["ai_role"]), cell(a["summary"], 130), cell(a["confidence"])] for a in load("actors")])


def campaigns() -> str:
    return table(["Campaign", "First seen", "Reported", "Regions", "Confidence", "Summary"],
                 [[f"**{cell(c['name'])}**", cell(c["first_seen"]), cell(c.get("reported", "")), cell(c.get("regions", [])), cell(c["confidence"]), cell(c["summary"], 140)] for c in load("campaigns")])


def incidents() -> str:
    return table(["Incident", "Kind", "Status", "Confidence"],
                 [[f"**{cell(i['name'])}**", cell(i.get("kind")), cell(i.get("status")), cell(i["confidence"])] for i in load("incidents")])


def vulnerabilities() -> str:
    return table(["Record", "Identifiers", "Kind", "Severity", "Published"],
                 [[cell(v["name"], 70), "<br>".join(f"`{cell(i)}`" for i in v["identifiers"]), cell(v["kind"]), cell(v["severity"]), cell(v["published"])] for v in load("vulnerabilities")])


def techniques() -> str:
    return table(["ID", "Technique", "Category", "Maturity", "Mapped to"],
                 [[f"`{t['id']}`", f"**{cell(t['name'])}**", cell(t["category"]), cell(t.get("maturity", "")), cell(t["mappings"])] for t in load("techniques")])


def test_cases() -> str:
    return table(["ID", "Test case", "Category", "What the secure system must prove"],
                 [[f"`{t['id']}`", f"**{cell(t['name'])}**", cell(t["category"]), cell(t["goal"], 120)] for t in load("test-cases")])


def detections() -> str:
    return table(["ID", "Detection", "Category", "Severity", "Status"],
                 [[f"`{d['id']}`", f"**{cell(d['name'])}**", cell(d["category"]), cell(d["severity"]), cell(d["status"])] for d in load("detections")])


def controls() -> str:
    return table(["ID", "Control", "Category"],
                 [[f"`{c['id']}`", f"**{cell(c['name'])}**", cell(c["category"])] for c in load("controls")])


def frameworks() -> str:
    return table(["Framework", "Category", "Used for"],
                 [[f"[{cell(f['name'])}]({f['url']})", cell(f["category"]), cell(f["use"], 90)] for f in load("frameworks")])


def models() -> str:
    return table(["Family", "Provider", "Deployment", "Security focus"],
                 [[f"**{cell(m['name'])}**", cell(m["provider"]), cell(m["deployment"]), cell(m["security_focus"], 80)] for m in load("models")])


def source_grades() -> str:
    grades = {"A": "Primary or authoritative", "B": "Strong secondary", "C": "Reputable press", "D": "Community", "E": "Unsupported"}
    sources = load("sources")
    return table(["Grade", "Class", "Sources"],
                 [[f"**{g}**", label, str(sum(1 for s in sources if s["grade"] == g))] for g, label in grades.items()], False)


EVIDENCE_CLASSES = {
    "framework-data": ("Taxonomies and knowledge bases", "Technique definitions and framework mappings", "Observed activity"),
    "incident-data": ("Incident databases", "Incident references, citing the primary report", "Actor attribution or cyber campaigns (scope is broader than cybersecurity)"),
    "detection-content": ("Community detection rules", "Detection ideas and telemetry requirements", "Proof of in-the-wild behavior"),
    "curated-list": ("Curated lists", "Discovering sources and tools", "Any claim on their own"),
    "assessment-tool": ("Scanners and red-team tools", "Test design and control evaluation", "Effectiveness against current models"),
    "benchmark": ("Benchmarks and environments", "Reproducible tests and coverage measurement", "Real-world prevalence"),
    "research-technique": ("Attack research code", "Techniques demonstrated in research", "Use in the wild"),
    "defence-tool": ("Defences and guardrails", "Control design and comparison", "Proven protection"),
    "lab-exercise": ("Training labs", "Analyst training and onboarding", "Threat intelligence"),
    "prompt-corpus": ("Prompt corpora and datasets", "Test inspiration and measurement", "Threat intelligence or attribution"),
}
SECTIONS = {
    "knowledge": "Knowledge bases, taxonomies and incident data", "catalog": "Catalogs and awesome lists",
    "evaluation": "Evaluation tools, scanners and red teaming", "benchmark": "Benchmarks, datasets and environments",
    "attack-research": "Attack technique research", "defence": "Defences, detection and controls",
    "agent-security": "Agent, skill and MCP security", "lab": "Labs, training and example collections",
}


def eco_rows(entries: list[dict]) -> list[list[str]]:
    rows = []
    for e in entries:
        flags = []
        if e["priority"] == "start-here":
            flags.append("**start here**")
        if e["status"] == "archived-reported":
            flags.append("archived (as reported)")
        note = cell(e["summary"]) + (" · " + ", ".join(flags) if flags else "")
        rows.append([f"[{cell(e['owner'])}/{cell(e['name'])}]({e['url']})", f"`{e['evidence_class']}`",
                     cell([f"`{t}`" for t in e["techniques"]]) or "none", note])
    return rows


ECO_HEAD = ["Repository", "Evidence class", "Techniques", "Scope"]


def eco_classes() -> str:
    entries = load("ecosystem")
    return table(["Evidence class", "What it is", "Can support", "Cannot support", "Entries"],
                 [[f"`{k}`", v[0], v[1], v[2], str(sum(1 for e in entries if e["evidence_class"] == k))] for k, v in EVIDENCE_CLASSES.items()])


def eco_start() -> str:
    return table(ECO_HEAD, eco_rows([e for e in load("ecosystem") if e["priority"] == "start-here"]))


def eco_section(name: str):
    return lambda: table(ECO_HEAD, eco_rows([e for e in load("ecosystem") if e["section"] == name]))


BLOCKS = {
    "stats": stats, "stats-pt": stats_pt, "maturity": maturity, "actors": actors, "campaigns": campaigns, "incidents": incidents,
    "vulnerabilities": vulnerabilities, "techniques": techniques, "test-cases": test_cases,
    "detections": detections, "controls": controls, "frameworks": frameworks, "models": models,
    "source-grades": source_grades, "eco-classes": eco_classes, "eco-start": eco_start,
    **{f"eco-{name}": eco_section(name) for name in SECTIONS},
}


def updated(text: str) -> str:
    for name, render in BLOCKS.items():
        start, end = f"<!-- gen:{name}:start -->", f"<!-- gen:{name}:end -->"
        if start not in text or end not in text:
            continue
        a, b = text.index(start) + len(start), text.index(end)
        text = text[:a] + "\n" + render() + "\n" + text[b:]
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path in FILES:
        current = path.read_text(encoding="utf-8")
        new = updated(current)
        if new != current:
            stale.append(path.name)
            if not args.check:
                path.write_text(new, encoding="utf-8")
    if args.check and stale:
        print(f"generated blocks are stale in {', '.join(stale)}; run python scripts/readme_stats.py", file=sys.stderr)
        return 1
    if not args.check:
        print("generated blocks updated" + (f": {', '.join(stale)}" if stale else " (nothing to change)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
