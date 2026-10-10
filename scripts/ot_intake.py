#!/usr/bin/env python3
"""Passive, bounded Cyber OT public GitHub directory metadata discovery.

Reads only allow-listed public GitHub REST directories. Never probes industrial
devices, downloads packet captures, or promotes candidates into canonical CTI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "ot-source-registry.json"
QUEUE = ROOT / "data" / "ot-review-queue.json"
MAX_BYTES = 2_000_000


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def checked_url(url):
    parts = urllib.parse.urlsplit(url)
    if (parts.scheme != "https" or parts.hostname != "api.github.com"
            or parts.port not in (None, 443) or parts.username or parts.password
            or not parts.path.startswith("/repos/")):
        raise ValueError("source must be an allow-listed public GitHub API endpoint")
    return url


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        checked_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url):
    checked_url(url)
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "LLmInjection-OT-Metadata/1.0"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    opener = urllib.request.build_opener(SafeRedirect())
    with opener.open(urllib.request.Request(url, headers=headers), timeout=20) as response:
        checked_url(response.geturl())
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("metadata response exceeds size bound")
        return json.loads(raw.decode("utf-8"))


def discover(source, payload, limit=15, now=None):
    """Return candidate records from directory metadata; never read file contents."""
    if source["adapter"] != "github-directory" or not source["enabled"]:
        return []
    if not isinstance(payload, list):
        raise ValueError("expected GitHub directory listing")
    now = now or datetime.now(UTC).replace(microsecond=0).isoformat()
    found = []
    for entry in sorted(payload, key=lambda x: x.get("name", ""), reverse=True):
        if len(found) >= limit:
            break
        if not isinstance(entry, dict) or entry.get("type") != "file":
            continue
        name = entry.get("name", "")
        if not isinstance(name, str) or not name.endswith(".json"):
            continue
        if source["id"] == "OT-SRC-ATTACK-ICS" and not name.startswith("ics-attack-"):
            continue
        url = entry.get("html_url")
        if not isinstance(url, str) or not url.startswith("https://github.com/"):
            continue
        path = entry.get("path", "")
        if not isinstance(path, str) or ".." in path.split("/"):
            continue
        evidence = {"path": path, "name": name, "html_url": url, "sha": entry.get("sha")}
        identity = (source["id"] + "|" + path).encode("utf-8")
        found.append({
            "id": "RQ-OT-" + hashlib.sha256(identity).hexdigest()[:16].upper(),
            "status": "candidate",
            "source_id": source["id"],
            "kind": "industrial-advisory-metadata" if source["category"] == "advisory"
                    else "ics-framework-version-metadata",
            "title": name,
            "url": url,
            "external_path": path,
            "evidence_sha256": hashlib.sha256(canonical(evidence).encode("utf-8")).hexdigest(),
            "discovered_at": now,
            "review_required": True,
            "evidence_status": "unreviewed-metadata",
            "review": {"decision": None, "notes": None},
        })
    return found


def merge(queue, incoming):
    index = {item["id"]: item for item in queue.get("items", [])}
    added = changed = 0
    for item in incoming:
        previous = index.get(item["id"])
        if previous is None:
            index[item["id"]] = item
            added += 1
        elif previous["evidence_sha256"] != item["evidence_sha256"]:
            item["status"] = "reviewing"
            item["review"]["notes"] = "Upstream metadata changed; repeat human review."
            index[item["id"]] = item
            changed += 1
    queue["items"] = sorted(index.values(), key=lambda x: x["id"])
    return added, changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default=str(REGISTRY))
    parser.add_argument("--queue", default=str(QUEUE))
    parser.add_argument("--fixture", help="Offline JSON object keyed by source ID")
    parser.add_argument("--live", action="store_true", help="Permit passive public API reads")
    parser.add_argument("--dry-run", action="store_true", help="Never modify review queue")
    parser.add_argument("--limit", type=int, default=15)
    args = parser.parse_args()
    if bool(args.fixture) == bool(args.live):
        parser.error("choose exactly one of --fixture or --live")
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    registry = load(args.registry)
    existing = load(args.queue)
    fixtures = load(args.fixture) if args.fixture else None
    incoming = []
    for source in registry["sources"]:
        if not source.get("enabled"):
            continue
        checked_url(source["url"])
        data = fixtures.get(source["id"], []) if fixtures is not None else fetch(source["url"])
        incoming.extend(discover(source, data, limit=args.limit))
    added, changed = merge(existing, incoming)
    if not args.dry_run:
        Path(args.queue).write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OT candidates={len(incoming)} added={added} changed={changed} dry_run={args.dry_run}")


if __name__ == "__main__":
    main()
