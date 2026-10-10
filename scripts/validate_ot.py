#!/usr/bin/env python3
"""Validate structured Cyber OT research metadata independently of attack claims."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_ROLES = {"advisory", "framework", "incident-research", "detection-research",
                 "dataset", "enrichment", "taxonomy", "telemetry-reference",
                 "assessment", "curated-list"}
ALLOWED_ADAPTERS = {"github-directory", "reference-only"}


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def safe_url(value):
    if not isinstance(value, str):
        return False
    parsed = urlsplit(value)
    return parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username and not parsed.password


def validate(registry=None, scenarios=None, datasets=None, queue=None):
    registry = registry if registry is not None else load("ot-source-registry.json")
    scenarios = scenarios if scenarios is not None else load("ot-scenarios.json")
    datasets = datasets if datasets is not None else load("ot-datasets.json")
    queue = queue if queue is not None else load("ot-review-queue.json")
    errors = []
    sources = {}
    if registry.get("schema_version") != "1.0" or not isinstance(registry.get("sources"), list):
        errors.append("registry schema and sources[] required")
        return errors
    for source in registry["sources"]:
        sid = source.get("id")
        if not isinstance(sid, str) or not sid.startswith("OT-SRC-") or sid in sources:
            errors.append("invalid or duplicate OT source ID")
        sources[sid] = source
        if source.get("category") not in ALLOWED_ROLES or source.get("adapter") not in ALLOWED_ADAPTERS:
            errors.append(f"{sid}: invalid source classification")
        if not safe_url(source.get("url")) or source.get("source_grade") not in "ABCDE":
            errors.append(f"{sid}: invalid URL/grade")
        try:
            date.fromisoformat(source["last_verified"])
        except (TypeError, ValueError, KeyError):
            errors.append(f"{sid}: invalid last_verified date")
        if source.get("enabled") and (
                source.get("adapter") != "github-directory"
                or urlsplit(source["url"]).hostname != "api.github.com"):
            errors.append(f"{sid}: enabled source must be a public GitHub directory")
        if source.get("review_required") is not True:
            errors.append(f"{sid}: analyst review must be mandatory")
    seen = set()
    for entry in scenarios:
        sid = entry.get("id")
        if not isinstance(sid, str) or not sid.startswith("AIOT-SC-") or sid in seen:
            errors.append("invalid or duplicate scenario ID")
        seen.add(sid)
        if entry.get("status") != "hypothetical" or entry.get("ai_involvement") != "design-hypothesis":
            errors.append(f"{sid}: scenarios must not claim observed AI/OT compromises")
        if not entry.get("ot_context", {}).get("authority") or not entry.get("controls") or not entry.get("telemetry"):
            errors.append(f"{sid}: missing operating boundary, telemetry or controls")
        for ref in entry.get("source_ids", []):
            if ref not in sources:
                errors.append(f"{sid}: unknown source reference {ref}")
    seen = set()
    for entry in datasets:
        sid = entry.get("id")
        if not isinstance(sid, str) or not sid.startswith("AIOT-DS-") or sid in seen:
            errors.append("invalid or duplicate dataset ID")
        seen.add(sid)
        if entry.get("source_id") not in sources or not safe_url(entry.get("url")):
            errors.append(f"{sid}: invalid dataset provenance")
        if entry.get("not_incident_evidence") is not True or not entry.get("redistribution"):
            errors.append(f"{sid}: benchmark evidence boundaries absent")
    seen = set()
    for item in queue.get("items", []):
        sid = item.get("id")
        if not isinstance(sid, str) or not sid.startswith("RQ-OT-") or sid in seen:
            errors.append("invalid or duplicate OT research candidate")
        seen.add(sid)
        if (item.get("source_id") not in sources or item.get("review_required") is not True
                or item.get("evidence_status") != "unreviewed-metadata"
                or item.get("status") not in {"candidate", "reviewing", "accepted", "rejected", "duplicate"}
                or not safe_url(item.get("url")) or not item.get("evidence_sha256")):
            errors.append(f"{sid}: invalid OT candidate")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        raise SystemExit("\n".join(problems))
    print("Cyber OT sources, scenarios, datasets and review queue valid")
