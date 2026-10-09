#!/usr/bin/env python3
"""Adoption and supply-chain signals for the ecosystem entries, from keyless public OSINT (stdlib only).

For every GitHub repository in data/ecosystem.json it asks two free APIs, no token needed:

  deps.dev   stars, forks and open issues; the packages (PyPI, npm, Go, ...) published from the repository,
             and whether any release carries a verified SLSA build-provenance attestation
  OSV.dev    published security advisories for each of those packages

Why: a red-team tool or guardrail is itself part of the AI supply chain. "Is it used?" and "has it
published security advisories (patched or not), and do its releases carry verifiable builds?" are things a maintainer would otherwise have to guess.

Output: data/ecosystem-osint.json. It is observation, not curation: analyst fields in ecosystem.json
(section, evidence class, techniques, status) are never touched, and these signals never support attribution.

    python scripts/osint_ecosystem.py                 # collect all entries and write the file
    python scripts/osint_ecosystem.py --only garak    # entries whose owner/name contains the text
    python scripts/osint_ecosystem.py --report out.md # also write a short Markdown summary
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DATA, load_data, write_json  # noqa: E402

DEPS = "https://api.deps.dev"
OSV = "https://api.osv.dev/v1/query"
OSV_ECOSYSTEM = {"PYPI": "PyPI", "NPM": "npm", "GO": "Go", "CARGO": "crates.io", "MAVEN": "Maven", "NUGET": "NuGet", "RUBYGEMS": "RubyGems"}
MAX_PACKAGES = 4
Fetcher = Callable[[str, dict | None], Any]


def fetch(url: str, body: dict | None = None) -> Any:
    """GET (or POST JSON) and decode JSON. Returns None on 404 so a missing project is data, not an error."""
    data = json.dumps(body).encode() if body is not None else None
    headers = {"User-Agent": "LLMInjection-OSINT/1.0", **({"Content-Type": "application/json"} if data else {})}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def project_signals(entry: dict, get: Fetcher) -> dict[str, Any] | None:
    key = urllib.parse.quote(f"github.com/{entry['owner']}/{entry['name']}", safe="")
    project = get(f"{DEPS}/v3/projects/{key}", None)
    if not project:
        return None
    out: dict[str, Any] = {k: project.get(f"{k}Count", project.get(k)) for k in ("stars", "forks")}
    out["open_issues"] = project.get("openIssuesCount")
    versions = (get(f"{DEPS}/v3alpha/projects/{key}:packageversions", None) or {}).get("versions", [])
    packages: dict[tuple[str, str], bool] = {}
    for v in versions:
        k = v["versionKey"]
        if k["system"] in OSV_ECOSYSTEM and v.get("relationType") == "SOURCE_REPO":
            verified = any(a.get("verified") for a in v.get("attestations", []))
            packages[(k["system"], k["name"])] = packages.get((k["system"], k["name"]), False) or verified
    out["slsa_verified"] = any(packages.values())
    out["packages"] = []
    for (system, name), verified in sorted(packages.items())[:MAX_PACKAGES]:
        result = get(OSV, {"package": {"name": name, "ecosystem": OSV_ECOSYSTEM[system]}}) or {}
        vulns = result.get("vulns", [])
        out["packages"].append({
            "system": system, "name": name, "slsa_verified": verified,
            "advisories": len(vulns), "advisory_ids": sorted(v["id"] for v in vulns)[:5],
            "truncated": bool(result.get("next_page_token")),
        })
    return out


def collect(entries: list[dict], get: Fetcher = fetch, today: str | None = None, workers: int = 6) -> dict[str, Any]:
    today = today or datetime.now(UTC).date().isoformat()

    errors: list[str] = []

    def one(entry: dict) -> tuple[str, dict | None]:
        try:
            return entry["id"], project_signals(entry, get)
        except (urllib.error.URLError, TimeoutError, ValueError):
            errors.append(entry["id"])  # a network failure is not the same as "deps.dev does not know this project"
            return entry["id"], None

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(one, entries))
    return {
        "schema_version": "1.0",
        "collected": today,
        "method": "deps.dev v3/v3alpha project and package-version endpoints; OSV.dev v1 package query. Keyless. Observation only.",
        "entries": {eid: {**sig, "checked": today} for eid, sig in results if sig is not None},
        "not_found": sorted(eid for eid, sig in results if sig is None and eid not in errors),
        "errors": sorted(errors),
    }


def report(model: dict, entries: list[dict]) -> str:
    names = {e["id"]: f"{e['owner']}/{e['name']}" for e in entries}
    got = model["entries"]
    lines = [f"# Ecosystem signals, {model['collected']}", "", f"{len(got)} of {len(entries)} entries answered; {len(model['not_found'])} not known to deps.dev (often because the repository publishes no package); {len(model['errors'])} failed with a network error.", ""]
    top = sorted(got.items(), key=lambda kv: -(kv[1].get("stars") or 0))[:10]
    lines += ["## Most starred", ""] + [f"- {names[k]}: {v.get('stars')} stars" for k, v in top]
    with_adv = [(names[k], p["name"], p["advisories"]) for k, v in got.items() for p in v["packages"] if p["advisories"]]
    lines += ["", "## Packages with published advisories (patched or not)", ""] + ([f"- {n}: `{pkg}` has {c} advisory(ies)" for n, pkg, c in sorted(with_adv, key=lambda x: -x[2])] or ["- none found"])
    slsa = sorted(names[k] for k, v in got.items() if v.get("slsa_verified"))
    lines += ["", "## Verified SLSA provenance on a release", ""] + ([f"- {n}" for n in slsa] or ["- none found"])
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="")
    ap.add_argument("--report")
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    entries = [e for e in load_data("ecosystem") if args.only.lower() in f"{e['owner']}/{e['name']}".lower()]
    model = collect(entries)
    print(f"collected {len(model['entries'])} of {len(entries)}; not known: {len(model['not_found'])}; errors: {len(model['errors'])}")
    if args.report:
        Path(args.report).write_text(report(model, entries), encoding="utf-8")
    if not args.no_write and not args.only:
        write_json(DATA / "ecosystem-osint.json", model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
