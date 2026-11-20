#!/usr/bin/env python3
"""Fold the daily digest's items into the research queue (stdlib only).

The scheduled "Threat Landscape IA" task writes its edition as Markdown for people and, from now on, as
intake/digests/YYYY-MM-DD.json for this script. Each item becomes a `candidate` in data/research-queue.json under
FEED-LLMI-DAILY-DIGEST, carrying the grade the analyst gave the source (not a feed-wide default), the seal
(read in the original, secondary, unconfirmed) and the techniques the digest mapped. Nothing is promoted into a
dataset: promotion stays with scripts/merge_promotions.py after a primary source is read.

Refused or skipped, and reported: items whose URL is already queued or held as a source, unconfirmed items,
unknown technique IDs (dropped from the item), invalid grades or seals.

    python scripts/import_digest.py intake/digests/2026-11-20.json --dry-run
    python scripts/import_digest.py intake/digests/*.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DATA, load_data, write_json  # noqa: E402

FEED_ID = "FEED-LLMI-DAILY-DIGEST"
GRADES = {"A", "B", "C", "D", "E"}
SEALS = {"original": 30, "secondary": 10, "unconfirmed": 0}
ITEM_ID = re.compile(r"^LLMI-\d{8}-\d{2}$")


def score(item: dict[str, Any]) -> int:
    """0 to 100: grade carries most of it, then the seal, then a Brazil/LATAM bonus."""
    base = {"A": 60, "B": 45, "C": 30, "D": 15, "E": 0}[item["source_grade"]]
    return min(100, base + SEALS[item["seal"]] + (10 if item.get("brazil_latam") else 0))


def to_queue(item: dict[str, Any], digest: dict[str, Any], techniques: set[str], now: str) -> dict[str, Any]:
    known = [t for t in item.get("techniques", []) if t in techniques]
    return {
        "id": f"RQ-DIG-{item['id'].removeprefix('LLMI-')}",
        "status": "candidate",
        "source_feed_id": FEED_ID,
        "source_grade": item["source_grade"],
        "kind": f"digest-{item.get('kind', 'item')}",
        "title": item["title"],
        "url": item["url"],
        "published": item.get("published"),
        "observed_at": now,
        "relevance_score": score(item),
        "matched_terms": known + (["brazil-latam"] if item.get("brazil_latam") else []),
        "summary": f"[{item['id']}] seal: {item['seal']}; {item.get('temporal', 'new')}. {item['summary']}",
        "identifiers": item.get("identifiers", []),
        "review": {"decision": None, "notes": f"From digest {digest['digest_id']}. Read the primary source before promoting."},
    }


def run(paths: list[Path], dry_run: bool) -> dict[str, list[str]]:
    queue = load_data("research-queue")
    held = {i["url"] for i in queue["items"]} | {s["url"] for s in load_data("sources")}
    techniques = {t["id"] for t in load_data("techniques")}
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    report: dict[str, list[str]] = {"added": [], "skipped": [], "refused": []}
    for path in paths:
        digest = json.loads(path.read_text(encoding="utf-8"))
        for item in digest.get("items", []):
            iid = item.get("id", "?")
            if not ITEM_ID.match(iid) or item.get("source_grade") not in GRADES or item.get("seal") not in SEALS:
                report["refused"].append(f"{iid}: needs an LLMI-YYYYMMDD-NN id, a grade A-E and a known seal")
                continue
            if not str(item.get("url", "")).startswith("https://"):
                report["refused"].append(f"{iid}: URL must use https")
                continue
            if item["seal"] == "unconfirmed":
                report["skipped"].append(f"{iid}: unconfirmed")
                continue
            if item["url"] in held:
                report["skipped"].append(f"{iid}: URL already queued or held")
                continue
            dropped = [t for t in item.get("techniques", []) if t not in techniques]
            if dropped:
                report["refused"].append(f"{iid}: dropped unknown techniques {', '.join(dropped)}")
            queue["items"].append(to_queue(item, digest, techniques, now))
            held.add(item["url"])
            report["added"].append(iid)
    if not dry_run and report["added"]:
        queue["meta"]["last_run"] = now
        write_json(DATA / "research-queue.json", queue)
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("digests", nargs="+", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    report = run(a.digests, a.dry_run)
    for key, lines in report.items():
        print(f"{key}: {len(lines)}")
        for line in lines:
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
