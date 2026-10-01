#!/usr/bin/env python3
"""Read-only query helpers and CLI for the LLMInjection intelligence graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

DATASETS = {
    "actor": "actors.json",
    "campaign": "campaigns.json",
    "incident": "incidents.json",
    "technique": "techniques.json",
    "model": "models.json",
    "framework": "frameworks.json",
    "test-case": "test-cases.json",
    "control": "controls.json",
    "detection": "detections.json",
    "source": "sources.json",
    "vulnerability": "vulnerabilities.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def label(record: dict) -> str:
    return str(record.get("name") or record.get("title") or record.get("id") or "unknown")


def build_index() -> dict[str, dict]:
    index: dict[str, dict] = {}
    for object_type, filename in DATASETS.items():
        for record in load_json(DATA / filename):
            rid = record.get("id")
            if not rid:
                continue
            index[rid] = {
                "id": rid,
                "type": record.get("type") or object_type,
                "label": label(record),
                "data": record,
            }
    return index


def load_relationships() -> list[dict]:
    return load_json(DATA / "relationships.json")


def compact_record(node: dict) -> dict:
    data = node["data"]
    return {
        "id": node["id"],
        "type": node["type"],
        "label": node["label"],
        "confidence": data.get("confidence"),
        "summary": data.get("summary") or data.get("description") or data.get("hypothesis"),
    }


def search_intelligence(query: str, object_type: str | None = None, limit: int = 20) -> list[dict]:
    index = build_index()
    needle = query.strip().lower()
    if not needle:
        return []
    matches: list[tuple[int, str, dict]] = []
    for node in index.values():
        if object_type and node["type"] != object_type:
            continue
        haystack = (node["label"] + " " + json.dumps(node["data"], ensure_ascii=False)).lower()
        if needle not in haystack:
            continue
        score = 100 if needle in node["label"].lower() else 60
        if node["data"].get("id", "").lower() == needle:
            score = 120
        matches.append((score, node["label"].lower(), compact_record(node)))
    matches.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in matches[: max(1, min(limit, 100))]]


def get_object(object_id: str) -> dict | None:
    return build_index().get(object_id)


def get_neighbors(object_id: str, relationship: str | None = None, limit: int = 50) -> list[dict]:
    index = build_index()
    if object_id not in index:
        return []
    out: list[dict] = []
    for edge in load_relationships():
        if relationship and edge.get("relationship") != relationship:
            continue
        if edge.get("source") == object_id:
            other = edge.get("target")
            direction = "out"
        elif edge.get("target") == object_id:
            other = edge.get("source")
            direction = "in"
        else:
            continue
        target = index.get(other)
        out.append(
            {
                "edge_id": edge.get("id"),
                "direction": direction,
                "relationship": edge.get("relationship"),
                "confidence": edge.get("confidence"),
                "object": compact_record(target) if target else {"id": other},
                "evidence_sources": edge.get("evidence_sources", []),
            }
        )
    return out[: max(1, min(limit, 200))]


def recent_activity(limit: int = 20) -> list[dict]:
    index = build_index()
    rows: list[tuple[str, dict]] = []
    for node in index.values():
        if node["type"] not in {"campaign", "incident", "vulnerability"}:
            continue
        data = node["data"]
        event_date = str(
            data.get("published")
            or data.get("date")
            or data.get("last_seen")
            or data.get("first_seen")
            or ""
        )
        rows.append((event_date, compact_record(node) | {"date": event_date}))
    rows.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in rows[: max(1, min(limit, 100))]]


def technique_coverage(technique_id: str) -> dict:
    index = build_index()
    technique = index.get(technique_id)
    if not technique or technique["type"] != "technique":
        return {"technique": technique_id, "found": False}

    tests: list[str] = []
    detections: list[str] = []
    controls: list[str] = []
    evidence: set[str] = set()

    for edge in load_relationships():
        source = edge.get("source")
        target = edge.get("target")
        rel = edge.get("relationship")
        if source == technique_id or target == technique_id:
            other = target if source == technique_id else source
            node = index.get(other)
            if not node:
                continue
            if rel == "validates" and node["type"] == "test-case":
                tests.append(other)
            elif rel == "detects" and node["type"] == "detection":
                detections.append(other)
            elif rel == "mitigated-by" and node["type"] == "control":
                controls.append(other)
            evidence.update(edge.get("evidence_sources", []))

    return {
        "technique": compact_record(technique),
        "found": True,
        "tests": sorted(set(tests)),
        "detections": sorted(set(detections)),
        "controls": sorted(set(controls)),
        "evidence_sources": sorted(evidence),
        "external_mappings": technique["data"].get("external_mappings", []),
    }


def current_diff() -> dict:
    candidates = [
        ROOT / "dist" / "intelligence-diff.json",
        ROOT / "reports" / "monthly",
    ]
    if candidates[0].exists():
        return load_json(candidates[0])

    reports_dir = candidates[1]
    if reports_dir.exists():
        files = sorted(reports_dir.glob("*-diff.json"))
        if files:
            return load_json(files[-1])

    return {
        "summary": {"added": 0, "removed": 0, "changed": 0},
        "datasets": {},
        "note": "No generated diff is currently available. Run scripts/build_snapshot.py and scripts/diff_intelligence.py.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Query LLMInjection structured intelligence")
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--type")
    search.add_argument("--limit", type=int, default=20)

    get = sub.add_parser("get")
    get.add_argument("id")

    neighbors = sub.add_parser("neighbors")
    neighbors.add_argument("id")
    neighbors.add_argument("--relationship")
    neighbors.add_argument("--limit", type=int, default=50)

    recent = sub.add_parser("recent")
    recent.add_argument("--limit", type=int, default=20)

    coverage = sub.add_parser("coverage")
    coverage.add_argument("technique_id")

    sub.add_parser("diff")

    args = parser.parse_args()
    if args.command == "search":
        result = search_intelligence(args.query, args.type, args.limit)
    elif args.command == "get":
        result = get_object(args.id)
    elif args.command == "neighbors":
        result = get_neighbors(args.id, args.relationship, args.limit)
    elif args.command == "recent":
        result = recent_activity(args.limit)
    elif args.command == "coverage":
        result = technique_coverage(args.technique_id)
    else:
        result = current_diff()

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
