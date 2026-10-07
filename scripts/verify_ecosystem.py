#!/usr/bin/env python3
"""Re-verify every repository in data/ecosystem.json with git alone (stdlib only, no GitHub API token).

For each entry it makes a shallow, blob-filtered clone into a temporary directory, then records:
  reachable, last commit date, licence family (from the LICENSE file) and a stale flag.
GitHub's "archived" switch is not visible to git, so archive status is never changed by this script.

  python scripts/verify_ecosystem.py                 # report only
  python scripts/verify_ecosystem.py --write         # update the verification block in data/ecosystem.json
  python scripts/verify_ecosystem.py --only garak    # entries whose owner/name contains the text
  python scripts/verify_ecosystem.py --stale-days 365

Cloned content is untrusted: it is only read as text, never executed, and removed afterwards.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ECO = ROOT / "data" / "ecosystem.json"

LICENCES = [  # first match wins
    ("GNU AFFERO", "AGPL-3.0"), ("GNU LESSER", "LGPL"), ("GNU GENERAL PUBLIC LICENSE", "GPL"),
    ("Apache License", "Apache-2.0"), ("Mozilla Public", "MPL-2.0"), ("MIT License", "MIT"),
    ("Permission is hereby granted", "MIT"), ("CC0", "CC0"), ("Attribution-NonCommercial", "CC-BY-NC"),
    ("Creative Commons", "CC"), ("Unlicense", "Unlicense"), ("BSD", "BSD"),
]


def licence_of(repo_dir: Path) -> str:
    for f in sorted(repo_dir.iterdir()):
        if f.is_file() and re.match(r"(?i)^(licen[cs]e|copying)", f.name):
            text = f.read_text(errors="ignore")[:4000]
            return next((name for key, name in LICENCES if key in text), "other")
    return "none-found"


def check(entry: dict, timeout: int) -> dict:
    url = entry["url"]
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    with tempfile.TemporaryDirectory(prefix="llmi-eco-") as tmp:
        dest = Path(tmp) / "repo"
        cmd = ["git", "clone", "-q", "--depth", "1", "--filter=blob:limit=1m", "--single-branch", url + ".git", str(dest)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
        except subprocess.TimeoutExpired:
            return {"reachable": False, "error": "timeout"}
        if proc.returncode != 0:
            # Public GitHub repos never prompt; an auth prompt means missing, renamed to private, or removed.
            return {"reachable": False, "error": proc.stderr.strip().splitlines()[-1][:160] if proc.stderr.strip() else "clone failed"}
        last = subprocess.run(["git", "-C", str(dest), "log", "-1", "--format=%cs"], capture_output=True, text=True).stdout.strip()
        return {"reachable": True, "last_commit": last, "license": licence_of(dest)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true", help="update data/ecosystem.json")
    ap.add_argument("--only", default="", help="substring filter on owner/name")
    ap.add_argument("--stale-days", type=int, default=540, help="flag repos with no commit in this many days")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=180)
    args = ap.parse_args()

    entries = json.loads(ECO.read_text(encoding="utf-8"))
    todo = [e for e in entries if args.only.lower() in f"{e['owner']}/{e['name']}".lower()]
    today = dt.date.today()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda e: check(e, args.timeout), todo))

    changed, unreachable, stale = 0, [], []
    for entry, res in zip(todo, results):
        name = f"{entry['owner']}/{entry['name']}"
        old = entry.get("verification", {})
        if not res["reachable"]:
            unreachable.append((name, res.get("error", "")))
        else:
            age = (today - dt.date.fromisoformat(res["last_commit"])).days
            if age > args.stale_days:
                stale.append((name, res["last_commit"]))
            if old.get("license") not in (None, res["license"]):
                print(f"licence changed  {name}: {old.get('license')} -> {res['license']}")
        new = {"method": "git clone --depth 1", "checked": today.isoformat(), **{k: v for k, v in res.items() if k != "error"}}
        if {k: v for k, v in new.items() if k != "checked"} != {k: v for k, v in old.items() if k not in ("checked", "method")} | {"method": new["method"]}:
            changed += 1
        entry["verification"] = new

    print(f"checked {len(todo)} · unreachable {len(unreachable)} · stale (> {args.stale_days} d) {len(stale)} · changed {changed}")
    for name, err in unreachable:
        print(f"  UNREACHABLE {name}  {err}")
    for name, last in sorted(stale, key=lambda x: x[1]):
        print(f"  stale       {name}  last commit {last}")
    if args.write:
        ECO.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {ECO.relative_to(ROOT)}")
    return 1 if unreachable else 0


if __name__ == "__main__":
    sys.exit(main())
