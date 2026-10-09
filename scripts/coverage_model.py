#!/usr/bin/env python3
"""Derive the coverage model behind the Explorer's Coverage tab (stdlib only).

Counting links says a technique has "1 detection". It does not say whether that detection is a
paragraph or a query somebody can run. This script adds the depth dimensions, all derived from the
datasets and the files in detections/, never typed by hand:

  implementation   per detection: "rule-file" when detections/<platform>/<det-id>-*.* exists, else "specification"
  platforms        which rule languages exist for the detection (sigma, sentinel, splunk, elastic, google-secops)
  publishers       distinct publishers behind a technique's evidence (one vendor repeated is one voice)
  best_grade       strongest source grade behind that evidence
  newest_evidence  most recent evidence date, and whether it is older than STALE_DAYS before the dataset's latest date
  benchmarks       ecosystem projects of evidence class "benchmark" that map to the technique
  actors           actors reached through campaigns that use the technique
  priority         maturity weight x unimplemented layers (see FORMULA)

Output: dist/coverage.json (the Explorer loads it as coverage.json).

    python scripts/coverage_model.py            # write dist/coverage.json and print a summary
    python scripts/coverage_model.py --check    # exit 1 if the model cannot be built
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, load_data  # noqa: E402

STALE_DAYS = 365
MATURITY_WEIGHT = {"observed-in-the-wild": 4, "disclosed-vulnerability": 3, "research-demonstrated": 2, "no-linked-evidence": 1}
GRADE_ORDER = "ABCDE"
EVIDENCE_PREFIXES = ("CAMPAIGN-", "INCIDENT-", "VULN-")
FORMULA = (
    "priority = maturity_weight x (4 - layers). maturity_weight: observed 4, disclosed vulnerability 3, "
    "research 2, none 1. layers (0-4) = test(1 if any) + detection(1 if a rule file exists, 0.5 if only a "
    "specification) + control(1 if any) + benchmark(1 if any). Higher means more urgent."
)


def rule_files(root: Path = ROOT) -> dict[str, list[str]]:
    """Map detection id (DET-AI-001) to the platforms that have a rule file for it."""
    found: dict[str, set[str]] = {}
    base = root / "detections"
    if base.is_dir():
        for path in base.glob("*/*"):
            if path.is_file() and path.name.lower().startswith("det-"):
                det_id = "-".join(path.name.split("-")[:3]).upper()
                found.setdefault(det_id, set()).add(path.parent.name)
    return {k: sorted(v) for k, v in found.items()}


def record_date(rec: dict) -> str:
    """Best event date for an evidence record, ISO string or empty."""
    return str(rec.get("date") or rec.get("last_seen") or rec.get("published") or rec.get("first_seen") or rec.get("reported") or "")[:10]  # YYYY[-MM[-DD]]


def latest_day(value: str) -> date:
    """Parse YYYY, YYYY-MM or YYYY-MM-DD; a partial date counts as the last day of its period (the freshest it could be)."""
    parts = [int(p) for p in value.split("-")]
    year, month = parts[0], parts[1] if len(parts) > 1 else 12
    if len(parts) > 2:
        return date(year, month, parts[2])
    nxt = date(year + (month == 12), month % 12 + 1, 1)
    return date.fromordinal(nxt.toordinal() - 1)


def days_between(newer: str, older: str) -> int:
    return (latest_day(newer) - latest_day(older)).days


def peer(rel: dict, tid: str) -> str:
    """The other end of a relationship."""
    return rel["target"] if rel["source"] == tid else rel["source"]


def build(root: Path = ROOT) -> dict:
    techniques, rels, eco = load_data("techniques"), load_data("relationships"), load_data("ecosystem")
    records = {r["id"]: r for name in ("incidents", "campaigns", "vulnerabilities") for r in load_data(name)}
    sources = {s["id"]: s for s in load_data("sources")}
    actors = {a["id"]: a for a in load_data("actors")}
    detections = {d["id"]: d for d in load_data("detections")}
    files = rule_files(root)
    # reference date = newest day-precision date in the data; a bare year such as "2026" must not push it into the future
    as_of = max((d for d in map(record_date, records.values()) if len(d) == 10), default="")

    conducts: dict[str, set[str]] = {}
    for r in rels:
        if r["relationship"] == "conducts":
            conducts.setdefault(r["target"], set()).add(r["source"])

    rows, matrix = [], []
    for t in techniques:
        tid = t["id"]
        linked = [r for r in rels if tid in (r["source"], r["target"])]
        evidence = sorted({o for o in (peer(r, tid) for r in linked) if o.startswith(EVIDENCE_PREFIXES)})
        src_ids = sorted({s for e in evidence for s in records.get(e, {}).get("source_ids", []) if s in sources})
        publishers = sorted({sources[s]["publisher"] for s in src_ids})
        grades = [sources[s]["grade"] for s in src_ids]
        dates = sorted((d for d in (record_date(records[e]) for e in evidence if e in records) if d), key=latest_day)
        newest = dates[-1] if dates else ""
        stale = bool(newest and as_of and days_between(as_of, newest) > STALE_DAYS)
        det_ids = sorted(peer(r, tid) for r in linked if r["relationship"] == "detects")
        dets = [{"id": d, "name": detections.get(d, {}).get("name", d), "implementation": "rule-file" if d in files else "specification", "platforms": files.get(d, [])} for d in det_ids]
        tests = sorted(peer(r, tid) for r in linked if r["relationship"] == "validates")
        controls = sorted(peer(r, tid) for r in linked if r["relationship"] == "mitigated-by")
        tools = sorted(e["id"] for e in eco if tid in e.get("techniques", []))
        benches = sorted(e["id"] for e in eco if tid in e.get("techniques", []) and e["evidence_class"] == "benchmark")
        who = sorted({a for e in evidence if e.startswith("CAMPAIGN-") for a in conducts.get(e, ())})
        det_layer = 1 if any(d["implementation"] == "rule-file" for d in dets) else (0.5 if dets else 0)
        layers = (1 if tests else 0) + det_layer + (1 if controls else 0) + (1 if benches else 0)
        maturity = t.get("maturity", "no-linked-evidence")
        rows.append({
            "id": tid, "name": t["name"], "category": t.get("category", ""), "maturity": maturity,
            "evidence": evidence, "publishers": publishers, "best_grade": min(grades, key=GRADE_ORDER.index) if grades else "",
            "newest_evidence": newest, "stale": stale,
            "tests": tests, "detections": dets, "controls": controls, "tools": tools, "benchmarks": benches, "actors": who,
            "layers": layers, "priority": round(MATURITY_WEIGHT.get(maturity, 1) * (4 - layers), 1),
        })
        matrix += [{"actor": a, "technique": tid, "via": sorted(e for e in evidence if e.startswith("CAMPAIGN-") and a in conducts.get(e, ()))} for a in who]

    n = len(rows)
    dets_all = [d for r in rows for d in r["detections"]]
    summary = {
        "techniques": n,
        "with_rule_file": sum(1 for r in rows if any(d["implementation"] == "rule-file" for d in r["detections"])),
        "specification_only": sum(1 for r in rows if r["detections"] and not any(d["implementation"] == "rule-file" for d in r["detections"])),
        "no_detection": sum(1 for r in rows if not r["detections"]),
        "with_benchmark": sum(1 for r in rows if r["benchmarks"]),
        "single_publisher": sum(1 for r in rows if len(r["publishers"]) == 1),
        "stale_evidence": sum(1 for r in rows if r["stale"]),
        "detections_total": len({d["id"] for d in dets_all}),
        "detections_with_rule_file": len({d["id"] for d in dets_all if d["implementation"] == "rule-file"}),
    }
    return {
        "schema_version": "1.0", "as_of": as_of, "stale_days": STALE_DAYS, "formula": FORMULA,
        "summary": summary,
        "techniques": rows,
        "actors": [{"id": a, "name": actors[a]["name"]} for a in sorted({m["actor"] for m in matrix}) if a in actors],
        "matrix": matrix,
    }


def main() -> int:
    model = build()
    out = ROOT / "dist" / "coverage.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(model, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}: {json.dumps(model['summary'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
