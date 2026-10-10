#!/usr/bin/env python3
"""Validate candidate-only registry and queue without promoting any findings."""

import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def validate():
    sources = json.loads((ROOT / "data/ai-source-registry.json").read_text())
    queue = json.loads((ROOT / "data/enrichment-review-queue.json").read_text())
    errors = []
    ids = set()
    supported = {"avid-list", "veris-json", "mcp-list", "osv-local",
                 "git-commits", "reference-only"}
    for entry in sources.get("sources", []):
        ident = entry.get("id")
        if not ident or ident in ids:
            errors.append("missing/duplicate source id: " + str(ident))
        ids.add(ident)
        if entry.get("adapter") not in supported:
            errors.append("unknown adapter " + str(ident))
        if entry.get("enabled") and entry.get("adapter") == "reference-only":
            errors.append("reference-only adapter enabled: " + str(ident))
        if urlsplit(entry.get("url", "")).scheme != "https":
            errors.append("non-https source " + str(ident))
        if entry.get("source_grade") not in "ABCDE":
            errors.append("invalid grade " + str(ident))
    seen = set()
    for entry in queue.get("items", []):
        ident = entry.get("id")
        if not ident or ident in seen:
            errors.append("missing/duplicate candidate id: " + str(ident))
        seen.add(ident)
        if entry.get("source_feed_id") not in ids:
            errors.append("unknown feed for " + str(ident))
        if entry.get("status") not in {"candidate", "reviewing", "accepted",
                                       "rejected", "duplicate"}:
            errors.append("invalid review status for " + str(ident))
        if urlsplit(entry.get("url", "")).scheme != "https":
            errors.append("non-https candidate " + str(ident))
        if not entry.get("evidence_sha256"):
            errors.append("candidate missing fingerprint " + str(ident))
    return errors


if __name__ == "__main__":
    issues = validate()
    if issues:
        raise SystemExit("\n".join(issues))
    print("Source registry and enrichment candidate queue valid")
