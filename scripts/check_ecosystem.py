#!/usr/bin/env python3
"""Verify the ecosystem map against the GitHub API (stdlib only).

For each entry in data/ecosystem.json this records whether the repository still exists, whether it
is archived, when it was last pushed to, and whether it was renamed. It never changes an entry's
evidence class, section or technique mapping: those are analyst decisions.

    python scripts/check_ecosystem.py                       # report only
    python scripts/check_ecosystem.py --write               # also update verified_at, last_push, status
    python scripts/check_ecosystem.py --fail-on-drift       # exit 1 if a verified state differs from the recorded one

Set GITHUB_TOKEN to raise the API rate limit from 60 to 5000 requests per hour.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DATA, load_data, write_json  # noqa: E402

API = "https://api.github.com/repos/{owner}/{name}"
Fetcher = Callable[[str], dict[str, Any]]


class NotFound(Exception):
    pass


class RateLimited(Exception):
    pass


def fetch_repo(url: str) -> dict[str, Any]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "LLMInjection-Ecosystem-Check/1.0"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise NotFound(url) from exc
        if exc.code in (403, 429):
            raise RateLimited(url) from exc
        raise


def check_entry(entry: dict[str, Any], fetch: Fetcher, today: str) -> dict[str, Any]:
    """Return the verified fields for one entry."""
    try:
        repo = fetch(API.format(owner=entry["owner"], name=entry["name"]))
    except NotFound:
        return {"status": "not-found", "verified_at": today}
    result: dict[str, Any] = {
        "status": "archived-verified" if repo.get("archived") else "active-verified",
        "verified_at": today,
        "last_push": (repo.get("pushed_at") or "")[:10] or None,
    }
    full = repo.get("full_name", "")
    if full and full.lower() != f"{entry['owner']}/{entry['name']}".lower():
        result["renamed_to"] = full
    return result


def drift(entry: dict[str, Any], verified: dict[str, Any]) -> str | None:
    """Describe a meaningful change between the recorded and the verified state."""
    old, new = entry.get("status"), verified["status"]
    if new == "not-found":
        return "repository not found"
    if new == "archived-verified" and old != "archived-verified":
        return "now archived" if old != "archived-reported" else "archived, as previously reported (now verified)"
    if old in ("archived-verified", "archived-reported") and new == "active-verified":
        return "recorded as archived but active"
    if "renamed_to" in verified:
        return f"renamed to {verified['renamed_to']}"
    return None


def run(entries: list[dict[str, Any]], fetch: Fetcher = fetch_repo, today: str | None = None) -> tuple[list[dict], list[str]]:
    today = today or datetime.now(UTC).date().isoformat()
    updated, notes = [], []
    for entry in entries:
        try:
            verified = check_entry(entry, fetch, today)
        except RateLimited:
            notes.append(f"{entry['id']}: rate limited, stopped; set GITHUB_TOKEN and re-run")
            updated.extend(entries[len(updated):])
            break
        change = drift(entry, verified)
        if change:
            notes.append(f"{entry['id']} {entry['owner']}/{entry['name']}: {change}")
        updated.append({**entry, **verified})
    return updated, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true", help="update data/ecosystem.json with verified fields")
    parser.add_argument("--fail-on-drift", action="store_true")
    parser.add_argument("--report", help="write a Markdown report to this path")
    args = parser.parse_args()
    entries = load_data("ecosystem")
    updated, notes = run(entries)
    verified = sum(1 for e in updated if e.get("verified_at") and e.get("status", "").endswith("verified"))
    lines = [f"Ecosystem check: {len(entries)} entries, {verified} verified, {len(notes)} finding(s)"] + [f"- {n}" for n in notes]
    print("\n".join(lines))
    if args.report:
        Path(args.report).write_text("# Ecosystem verification\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    if args.write:
        write_json(DATA / "ecosystem.json", updated)
    return 1 if args.fail_on_drift and notes else 0


if __name__ == "__main__":
    raise SystemExit(main())
