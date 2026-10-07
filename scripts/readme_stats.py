#!/usr/bin/env python3
"""Keep the README statistics block in sync with the datasets (stdlib only).

    python scripts/readme_stats.py          # rewrite the block
    python scripts/readme_stats.py --check  # exit 1 if the block is stale
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START, END = "<!-- stats:start -->", "<!-- stats:end -->"
GROUPS = [
    [("Actors", "actors"), ("Campaigns", "campaigns"), ("Incidents", "incidents"),
     ("Vulnerabilities", "vulnerabilities"), ("Techniques", "techniques"), ("Sources", "sources")],
    [("Test cases", "test-cases"), ("Detections", "detections"), ("Controls", "controls"),
     ("Frameworks", "frameworks"), ("Model families", "models"), ("Relationships", "relationships")],
]


def count(name: str) -> int:
    return len(json.loads((ROOT / "data" / f"{name}.json").read_text(encoding="utf-8")))


def render() -> str:
    tables = []
    for group in GROUPS:
        head = "| " + " | ".join(label for label, _ in group) + " |"
        rule = "|" + ":---:|" * len(group)
        vals = "| " + " | ".join(f"**{count(key)}**" for _, key in group) + " |"
        tables.append("\n".join([head, rule, vals]))
    return START + "\n" + "\n\n".join(tables) + "\n" + END


def updated(text: str) -> str:
    a, b = text.index(START), text.index(END) + len(END)
    return text[:a] + render() + text[b:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    current = README.read_text(encoding="utf-8")
    new = updated(current)
    if args.check:
        if new != current:
            print("README statistics are stale; run python scripts/readme_stats.py", file=sys.stderr)
            return 1
        return 0
    README.write_text(new, encoding="utf-8")
    print("README statistics updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
