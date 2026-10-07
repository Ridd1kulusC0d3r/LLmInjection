#!/usr/bin/env python3
"""Keep the generated blocks of README.md in sync with the datasets (stdlib only).

Blocks sit between <!-- gen:NAME:start --> and <!-- gen:NAME:end --> markers.

    python scripts/readme_stats.py          # rewrite all blocks
    python scripts/readme_stats.py --check  # exit 1 if any block is stale
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

GROUPS = [
    [("Actors", "actors"), ("Campaigns", "campaigns"), ("Incidents", "incidents"),
     ("Vulnerabilities", "vulnerabilities"), ("Techniques", "techniques"), ("Sources", "sources")],
    [("Test cases", "test-cases"), ("Detections", "detections"), ("Controls", "controls"),
     ("Frameworks", "frameworks"), ("Model families", "models"), ("Relationships", "relationships")],
]


def load(name: str) -> list[dict]:
    return json.loads((ROOT / "data" / f"{name}.json").read_text(encoding="utf-8"))


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


def actors() -> str:
    return table(["Actor", "Nexus", "AI role", "Activity", "Confidence"],
                 [[f"**{cell(a['name'])}**", cell(a["nexus"]), cell(a["ai_role"]), cell(a["summary"], 130), cell(a["confidence"])] for a in load("actors")])


def campaigns() -> str:
    return table(["Campaign", "Seen", "Confidence", "Summary"],
                 [[f"**{cell(c['name'])}**", cell(c["first_seen"]), cell(c["confidence"]), cell(c["summary"], 150)] for c in load("campaigns")])


def incidents() -> str:
    return table(["Incident", "Kind", "Status", "Confidence"],
                 [[f"**{cell(i['name'])}**", cell(i.get("kind")), cell(i.get("status")), cell(i["confidence"])] for i in load("incidents")])


def vulnerabilities() -> str:
    return table(["Record", "Identifiers", "Kind", "Severity", "Published"],
                 [[cell(v["name"], 70), "<br>".join(f"`{cell(i)}`" for i in v["identifiers"]), cell(v["kind"]), cell(v["severity"]), cell(v["published"])] for v in load("vulnerabilities")])


def techniques() -> str:
    return table(["ID", "Technique", "Category", "Mapped to"],
                 [[f"`{t['id']}`", f"**{cell(t['name'])}**", cell(t["category"]), cell(t["mappings"])] for t in load("techniques")])


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


BLOCKS = {
    "stats": stats, "actors": actors, "campaigns": campaigns, "incidents": incidents,
    "vulnerabilities": vulnerabilities, "techniques": techniques, "test-cases": test_cases,
    "detections": detections, "controls": controls, "frameworks": frameworks, "models": models,
    "source-grades": source_grades,
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
    current = README.read_text(encoding="utf-8")
    new = updated(current)
    if args.check:
        if new != current:
            print("README generated blocks are stale; run python scripts/readme_stats.py", file=sys.stderr)
            return 1
        return 0
    README.write_text(new, encoding="utf-8")
    print("README generated blocks updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
