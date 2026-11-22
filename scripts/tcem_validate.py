#!/usr/bin/env python3
"""Validate the TCEM cases in tcem/cases (stdlib only).

TCEM, the Threat Context Engineering Method (github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling, v0.5.1,
same author as this repository), validates a detection specification by replaying a fixture of defensive events
against its `validation_logic`. This module ports that evaluator (single-event, threshold and ordered-sequence
patterns, operators eq, neq, in, exists and contains) so the cases here can be checked without installing the
toolkit, and adds the structural checks this repository needs: the fields TCEM's schemas require, unique ids,
references that resolve inside the case, and LLMInjection ids (DET-AI, CTRL, LLMI-T, sources) that exist.

    python scripts/tcem_validate.py              # every case
    python scripts/tcem_validate.py CASE-ARTEX-STORM-0940

The same cases load in the TCEM toolkit itself: `tce validate tcem/cases/<case>`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tcem" / "cases"

# Required fields per TCEM entity kind (schemas/*.schema.json in the TCEM repository, v0.5.1).
REQUIRED = {
    "case": ["id", "name", "mission", "status"],
    "intelligence_requirements": ["id", "question", "decision_supported", "priority"],
    "crown_jewels": ["id", "name", "rationale"],
    "architectures": ["id", "name", "nodes"],
    "evidence_items": ["id", "claim", "evidence_state"],
    "hypotheses": ["id", "statement", "confidence", "status"],
    "threat_contexts": ["id", "name", "lens_id", "relevance", "status"],
    "scenarios": ["id", "title", "objective", "target_crown_jewels", "priority", "confidence"],
    "telemetry_contracts": ["id", "behavior", "observable", "status"],
    "detection_specifications": ["id", "title", "scenario_ids", "telemetry_contract_ids", "analytic_concept", "validation_logic", "implementations", "status"],
    "validations": ["id", "method", "status"],
    "intelligence_gaps": ["id", "question", "priority", "status"],
    "decisions": ["id", "title", "statement", "status"],
}
# Enumerations in TCEM's schemas that the cases here use.
ENUMS = {("scenarios", "priority.band"): {"", "P0", "P1", "P2", "P3"},
         ("detection_specifications", "status"): {"draft", "ready", "implemented", "validated", "production", "retired"},
         ("validations", "status"): {"passed", "partial", "failed", "not-tested"}}
PRIORITY_KEYS = ["crown_jewel_criticality", "threat_relevance", "attack_path_feasibility", "exposure", "control_weakness", "detection_gap"]


def _value(event: dict[str, Any], field: str):
    if field in event:
        return event[field]
    current: Any = event
    for part in field.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _predicate(event: dict[str, Any], clause: dict[str, Any]) -> bool:
    actual, op = _value(event, clause.get("field", "")), clause.get("op", "eq")
    if op == "exists":
        return actual is not None
    if op == "eq":
        return actual == clause.get("value")
    if op == "neq":
        return actual != clause.get("value")
    if op == "in":
        return actual in (clause.get("values") or [])
    if op == "contains":
        needle = clause.get("value")
        if isinstance(actual, (list, tuple, set)):
            return needle in actual
        return isinstance(actual, str) and str(needle) in actual
    raise ValueError(f"unsupported validation operator: {op}")


def _stage(event: dict[str, Any], stage: dict[str, Any]) -> bool:
    return all(_predicate(event, c) for c in stage.get("all", []) or [])


def evaluate_logic(logic: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    """Same semantics as tce.validation_harness.evaluate_logic."""
    pattern, stages, group_by = logic.get("pattern", "single-event"), logic.get("stages") or [], logic.get("group_by") or []
    key = lambda e: tuple(_value(e, f) for f in group_by)  # noqa: E731
    if not stages:
        return {"matches": 0, "groups": []}
    if pattern == "single-event":
        idx = [i for i, e in enumerate(events) if _stage(e, stages[0])]
        return {"matches": len(idx), "groups": [[i] for i in idx]}
    if pattern == "threshold":
        groups: dict[tuple, list[int]] = {}
        for i, e in enumerate(events):
            if _stage(e, stages[0]):
                groups.setdefault(key(e), []).append(i)
        hit = [v for v in groups.values() if len(v) >= int(logic.get("threshold", 1))]
        return {"matches": len(hit), "groups": hit}
    if pattern == "ordered-sequence":
        matches = []
        for start, e in enumerate(events):
            if not _stage(e, stages[0]):
                continue
            k, idx, cursor, ok = key(e), [start], start + 1, True
            for stage in stages[1:]:
                found = None
                while cursor < len(events):
                    c = events[cursor]
                    cursor += 1
                    if key(c) == k and _stage(c, stage):
                        found = cursor - 1
                        break
                if found is None:
                    ok = False
                    break
                idx.append(found)
            if ok:
                matches.append(idx)
        return {"matches": len(matches), "groups": matches}
    raise ValueError(f"unsupported validation pattern: {pattern}")


def load_case(case_dir: Path) -> dict:
    return json.loads((case_dir / "case.json").read_text(encoding="utf-8"))


def load_events(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def run_validations(case: dict, case_dir: Path) -> list[dict]:
    specs = {s["id"]: s for s in case.get("detection_specifications", [])}
    out = []
    for v in case.get("validations", []):
        events = load_events(case_dir / v["fixture"])
        for sid in v.get("detection_specification_ids", []):
            r = evaluate_logic(specs[sid]["validation_logic"], events)
            exp = v.get("expected") or {}
            lo, hi = int(exp.get("min_matches", 1)), exp.get("max_matches")
            out.append({"validation": v["id"], "spec": sid, "matches": r["matches"], "groups": r["groups"],
                        "passed": r["matches"] >= lo and (hi is None or r["matches"] <= int(hi))})
    return out


def _known_ids() -> set[str]:
    ids: set[str] = set()
    for name in ("detections", "controls", "techniques", "sources", "actors", "campaigns", "incidents", "tools"):
        ids |= {x["id"] for x in json.loads((ROOT / "data" / f"{name}.json").read_text(encoding="utf-8"))}
    return ids


def check_case(case: dict, known: set[str]) -> list[str]:
    errs, ids = [], set()
    if not str(case.get("case", {}).get("id", "")).startswith("CASE-"):
        errs.append("case.id must start with CASE-")
    for key, fields in REQUIRED.items():
        items = [case.get(key, {})] if key == "case" else case.get(key, [])
        for it in items:
            for f in fields:
                if it.get(f) in (None, "", []):
                    errs.append(f"{key} {it.get('id')}: missing {f}")
            if key != "case":
                if it["id"] in ids:
                    errs.append(f"duplicate id {it['id']}")
                ids.add(it["id"])
    for s in case.get("scenarios", []):
        missing = [k for k in PRIORITY_KEYS if k not in s.get("priority", {})]
        if missing:
            errs.append(f"{s['id']}: priority lacks {missing}")
    for (key, path), allowed in ENUMS.items():
        for it in case.get(key, []):
            v = it
            for part in path.split("."):
                v = v.get(part) if isinstance(v, dict) else None
            if v not in allowed:
                errs.append(f"{it['id']}.{path}: {v!r} is not a TCEM value")
    refs = ("scenario_ids", "telemetry_contract_ids", "detection_specification_ids", "validation_ids", "hypothesis_ids",
            "evidence_ids", "crown_jewel_ids", "target_crown_jewels", "intelligence_requirement_ids", "intelligence_gap_ids",
            "supports", "supporting_evidence", "telemetry_requirements", "threat_context_ids", "architecture_ids")
    for key in REQUIRED:
        for it in ([] if key == "case" else case.get(key, [])):
            for r in refs:
                for target in it.get(r, []) or []:
                    if target not in ids:
                        errs.append(f"{it['id']}.{r}: {target} is not in the case")
    llmi = case.get("x_llminjection", {})
    for ref in llmi.get("refs", []):
        if ref not in known:
            errs.append(f"x_llminjection: {ref} is not in data/")
    return errs


def main(argv: list[str]) -> int:
    known, bad = _known_ids(), 0
    dirs = [CASES / a for a in argv] if argv else sorted(p for p in CASES.iterdir() if (p / "case.json").exists())
    for d in dirs:
        case = load_case(d)
        errs = check_case(case, known)
        res = run_validations(case, d)
        errs += [f"{r['validation']} / {r['spec']}: {r['matches']} matches, expected otherwise" for r in res if not r["passed"]]
        print(f"{d.name}: {'ok' if not errs else 'FAILED'} ({len(res)} validations)")
        for e in errs:
            print("  -", e)
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
