#!/usr/bin/env python3
"""Assemble the static Explorer into a directory (stdlib only): the same files the Pages workflow publishes.

    python scripts/build_site.py                 # build into _site/
    python scripts/build_site.py --out /tmp/x    # build elsewhere, for a local preview

It runs the generators that feed the Explorer (graph, snapshot and diff, static API, Navigator layers, coverage
model) and then copies site/ and their outputs side by side, so a local preview matches what GitHub serves.
Preview with:  python -m http.server --directory _site
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(*args: str) -> None:
    subprocess.run([PY, *args], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)


def build(out: Path) -> None:
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    run("scripts/build_graph.py")
    snapshots = sorted((ROOT / "data" / "snapshots").glob("*.json"))
    run("scripts/build_snapshot.py", "--output", "dist/current-snapshot.json")
    run("scripts/diff_intelligence.py", "--baseline", str(snapshots[-1]), "--current", "dist/current-snapshot.json",
        "--output", "dist/intelligence-diff.json", "--markdown", "dist/intelligence-diff.md")
    run("scripts/build_api.py")
    run("scripts/build_navigator.py")
    run("scripts/coverage_model.py")
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ROOT / "site", out)
    for src, name in [
        ("dist/graph.json", "graph.json"), ("dist/graph.graphml", "graph.graphml"),
        ("dist/llminjection-stix.json", "llminjection-stix.json"), ("data/threat-landscape-2026.json", "landscape.json"),
        ("data/ecosystem.json", "ecosystem.json"), ("dist/coverage.json", "coverage.json"),
        ("dist/current-snapshot.json", "current-snapshot.json"), ("dist/intelligence-diff.json", "intelligence-diff.json"),
        ("dist/intelligence-diff.md", "intelligence-diff.md"),
    ]:
        shutil.copy(ROOT / src, out / name)
    shutil.copytree(dist / "api", out / "api")
    shutil.copytree(dist / "navigator", out / "navigator")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="_site")
    args = ap.parse_args()
    out = Path(args.out)
    build(out if out.is_absolute() else ROOT / out)
    print(f"built {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
