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
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(*args: str) -> None:
    subprocess.run([PY, *args], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)


REPO = "https://github.com/Ridd1kulusC0d3r/LLmInjection/blob/main/"
KIND_BY_DIR = {"dossiers": "dossier", "intel": "intel", "trends": "trends", "templates": "template", "intake": "intake"}


def report_index(platform: dict) -> list[dict]:
    """Every Markdown report under reports/, newest first, plus the report the platform generates on each build."""
    rows = [platform]
    for path in sorted((ROOT / "reports").rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if path.name == "README.md" and path.parent.name == "reports":
            continue
        text = path.read_text(encoding="utf-8")
        title = re.search(r'^title:\s*"?(.+?)"?\s*$', text, re.M) or re.search(r"^#\s+(.+)$", text, re.M)
        kind = KIND_BY_DIR.get(path.parent.name, "landscape" if re.fullmatch(r"\d{4}-\d{2}(-diff)?", path.stem) else "report")
        date = re.search(r"\b(20\d\d-\d\d(?:-\d\d)?)\b", path.stem + " " + text[:600])
        pdf = re.search(r"^pdf:\s*(\S+)\s*$", text[:600], re.M)
        if pdf and (ROOT / pdf.group(1)).exists():
            extra = {"pdf": pdf.group(1)}
        else:
            extra = {}
        rows.append({**extra, "path": rel, "title": title.group(1) if title else path.stem, "kind": kind,
                     "date": date.group(1) if date else "", "github": REPO + rel})
    authored = sorted(rows[1:], key=lambda r: r["date"], reverse=True)
    return [rows[0], *[r for r in authored if r["kind"] != "template"], *[r for r in authored if r["kind"] == "template"]]


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
    period = json.loads((dist / "current-snapshot.json").read_text(encoding="utf-8")).get("generated_at", "")[:7] or "current"
    run("scripts/generate_landscape_report.py", "--snapshot", "dist/current-snapshot.json", "--diff", "dist/intelligence-diff.json",
        "--output", "dist/platform-report.md", "--period", period)
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
    shutil.copytree(ROOT / "reports", out / "reports")
    shutil.copytree(ROOT / "assets" / "reports", out / "assets" / "reports")
    shutil.copy(dist / "platform-report.md", out / "reports" / "platform-report.md")
    platform = {"path": "reports/platform-report.md", "title": "Platform report", "kind": "platform", "date": period,
                "github": REPO + "scripts/generate_landscape_report.py"}
    sys.path.insert(0, str(ROOT / "scripts"))
    from coverage_model import rule_files  # noqa: PLC0415
    rules = {p.relative_to(ROOT).as_posix(): None for p in (ROOT / "detections").glob("*/*") if p.is_file()}
    by_det: dict[str, list[str]] = {}
    for rel in rules:
        det = "-".join(Path(rel).name.split("-")[:3]).upper()
        if det.startswith("DET-"):
            by_det.setdefault(det, []).append(rel)
    assert set(by_det) >= set(rule_files())
    vault = json.loads((ROOT / "references" / "crosswalks" / "payload-vault.json").read_text(encoding="utf-8"))
    (out / "payload-vault.json").write_text(json.dumps({k: vault[k] for k in ("meta", "summary", "categories")}, ensure_ascii=False),
                                            encoding="utf-8")
    external = json.loads((ROOT / "references" / "crosswalks" / "artex-detections.json").read_text(encoding="utf-8"))["detection_links"]
    from build_report_pages import build as build_pages  # noqa: PLC0415
    pages = {r["path"]: r["page"] for r in build_pages(out / "relatorios")}
    index = [{**r, "page": pages[r["path"]]} if r["path"] in pages else r for r in report_index(platform)]
    (out / "reports.json").write_text(json.dumps({"repo": REPO, "reports": index, "rule_files": by_det,
                                                  "external_rules": {k: {"publisher": "ThreatDefence", "urls": v} for k, v in external.items()}},
                                                 ensure_ascii=False, indent=1), encoding="utf-8")
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
