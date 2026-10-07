#!/usr/bin/env python3
"""Audit the relationship graph for orphaned and uncovered records (stdlib only).

Reports, and exits 1 when `--strict` is set and any hard finding exists:
  hard   test cases not validating a technique, detections not detecting one, controls linked to nothing
  soft   techniques with no test or no detection (coverage gaps, not data errors)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import load_data  # noqa: E402


def audit() -> dict[str, list[str]]:
    rels = load_data("relationships")
    tests, dets, ctrls, techs = (load_data(n) for n in ("test-cases", "detections", "controls", "techniques"))
    validates = {r["source"] for r in rels if r["relationship"] == "validates"}
    detects = {r["source"] for r in rels if r["relationship"] == "detects"}
    linked = {r[k] for r in rels for k in ("source", "target") if r["relationship"] in {"mitigated-by", "supported-by"}}
    tested = {r["target"] for r in rels if r["relationship"] == "validates"}
    detected = {r["target"] for r in rels if r["relationship"] == "detects"}
    return {
        "test cases without a technique": [t["id"] for t in tests if t["id"] not in validates],
        "detections without a technique": [d["id"] for d in dets if d["id"] not in detects],
        "controls linked to nothing": [c["id"] for c in ctrls if c["id"] not in linked],
        "techniques without a test": [t["id"] for t in techs if t["id"] not in tested],
        "techniques without a detection": [t["id"] for t in techs if t["id"] not in detected],
    }


HARD = ("test cases without a technique", "detections without a technique", "controls linked to nothing")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true", help="exit 1 on hard findings")
    args = parser.parse_args()
    findings = audit()
    for name, ids in findings.items():
        kind = "HARD" if name in HARD else "gap "
        print(f"[{kind}] {name}: {len(ids)}" + (f"  ({', '.join(ids)})" if ids else ""))
    return 1 if args.strict and any(findings[k] for k in HARD) else 0


if __name__ == "__main__":
    raise SystemExit(main())
