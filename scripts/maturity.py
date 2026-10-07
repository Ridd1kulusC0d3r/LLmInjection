#!/usr/bin/env python3
"""Derive technique maturity from linked evidence (stdlib only).

Levels, strongest first:
  observed-in-the-wild    linked to a campaign, or to an incident whose status is observed
  disclosed-vulnerability linked to a vulnerability record (CVE, GHSA or malicious package)
  research-demonstrated   linked to a research or lab incident, or mapped by a research-technique or benchmark project
  no-linked-evidence      nothing in this repository links to the technique yet (not a claim that it is theoretical)

The validator requires each technique's `maturity` field to equal this derivation, so the
field cannot drift from the graph.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import load_data  # noqa: E402

LEVELS = ["observed-in-the-wild", "disclosed-vulnerability", "research-demonstrated", "no-linked-evidence"]
RESEARCH_CLASSES = {"research-technique", "benchmark"}


def derive_all() -> dict[str, str]:
    rels, incidents, eco = load_data("relationships"), {i["id"]: i for i in load_data("incidents")}, load_data("ecosystem")
    out = {}
    for t in load_data("techniques"):
        tid = t["id"]
        others = [r["target"] if r["source"] == tid else r["source"] for r in rels if tid in (r["source"], r["target"])]
        if any(o.startswith("CAMPAIGN-") for o in others) or any(
            o.startswith("INCIDENT-") and str(incidents.get(o, {}).get("status", "")).startswith("observed") for o in others
        ):
            level = LEVELS[0]
        elif any(o.startswith("VULN-") for o in others):
            level = LEVELS[1]
        elif any(o.startswith("INCIDENT-") for o in others) or any(
            tid in e.get("techniques", []) and e["evidence_class"] in RESEARCH_CLASSES for e in eco
        ):
            level = LEVELS[2]
        else:
            level = LEVELS[3]
        out[tid] = level
    return out


if __name__ == "__main__":
    for tid, level in derive_all().items():
        print(f"{tid}  {level}")
