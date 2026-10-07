#!/usr/bin/env python3
"""Add GitHub-API-only signals to the ecosystem verification block (stdlib only).

scripts/verify_ecosystem.py clones each repository with git and records reachability, last commit and
licence, but the GitHub archive flag and renames are not visible to git. This script asks the GitHub API
for exactly those two things and stores them in each entry's `verification` block:

    archived      the GitHub archive flag
    renamed_to    set when the API reports a different owner/name
    api_checked   the date of this check

It never changes an entry's status, evidence class, section or technique mapping: those are analyst
decisions. It reports drift (for example "listed" but archived) so an analyst can decide.

    python scripts/check_ecosystem.py                  # report only
    python scripts/check_ecosystem.py --write          # also update verification blocks
    python scripts/check_ecosystem.py --fail-on-drift  # exit 1 when any drift is found

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


def check_entry(entry: dict[str, Any], fetch: Fetcher, today: str) -> dict[str, Any] | None:
    """Return the API-only fields for one entry, or None when the repository was not found."""
    try:
        repo = fetch(API.format(owner=entry["owner"], name=entry["name"]))
    except NotFound:
        return None
    fields: dict[str, Any] = {"archived": bool(repo.get("archived")), "api_checked": today}
    full = repo.get("full_name", "")
    if full and full.lower() != f"{entry['owner']}/{entry['name']}".lower():
        fields["renamed_to"] = full
    return fields


def drift(entry: dict[str, Any], fields: dict[str, Any] | None) -> str | None:
    """Describe a meaningful difference between the recorded state and the API."""
    if fields is None:
        return "not found on GitHub"
    status = entry.get("status")
    if fields["archived"] and status != "archived-reported":
        return "archived on GitHub but not recorded as archived"
    if not fields["archived"] and status == "archived-reported":
        return "recorded as archived but active on GitHub"
    if "renamed_to" in fields:
        return f"renamed to {fields['renamed_to']}"
    return None


def run(entries: list[dict[str, Any]], fetch: Fetcher = fetch_repo, today: str | None = None) -> tuple[list[dict], list[str]]:
    today = today or datetime.now(UTC).date().isoformat()
    updated: list[dict] = []
    notes: list[str] = []
    for entry in entries:
        try:
            fields = check_entry(entry, fetch, today)
        except RateLimited:
            notes.append(f"{entry['id']}: rate limited, stopped; set GITHUB_TOKEN and re-run")
            updated.extend(entries[len(updated):])
            break
        change = drift(entry, fields)
        if change:
            notes.append(f"{entry['id']} {entry['owner']}/{entry['name']}: {change}")
        merged = {**entry}
        if fields is not None:
            merged["verification"] = {**entry.get("verification", {}), **fields}
        updated.append(merged)
    return updated, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true", help="update verification blocks in data/ecosystem.json")
    parser.add_argument("--fail-on-drift", action="store_true")
    parser.add_argument("--report", help="write a Markdown report to this path")
    args = parser.parse_args()
    entries = load_data("ecosystem")
    updated, notes = run(entries)
    lines = [f"Ecosystem API check: {len(entries)} entries, {len(notes)} finding(s)"] + [f"- {n}" for n in notes]
    print("\n".join(lines))
    if args.report:
        Path(args.report).write_text("# Ecosystem API check\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    if args.write:
        write_json(DATA / "ecosystem.json", updated)
    return 1 if args.fail_on_drift and notes else 0


if __name__ == "__main__":
    raise SystemExit(main())
