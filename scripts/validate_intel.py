#!/usr/bin/env python3
"""Minimal dependency-free validation for LLMInjection structured intelligence."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIDENCE = {"confirmed", "high", "medium", "low", "unverified"}
GRADES = {"A", "B", "C", "D", "E"}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def valid_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def check_https(value: str) -> bool:
    return isinstance(value, str) and value.startswith("https://")


def validate():
    errors: list[str] = []
    seen: set[str] = set()

    frameworks = load_json(ROOT / "data" / "frameworks.json")
    actors = load_json(ROOT / "data" / "actors.json")
    techniques = load_json(ROOT / "data" / "techniques.json")
    models = load_json(ROOT / "data" / "models.json")
    test_cases = load_json(ROOT / "data" / "test-cases.json")
    landscape = load_json(ROOT / "data" / "threat-landscape-2026.json")

    for dataset_name, records in (
        ("frameworks", frameworks),
        ("actors", actors),
        ("techniques", techniques),
        ("models", models),
        ("test-cases", test_cases),
    ):
        if not isinstance(records, list):
            errors.append(f"{dataset_name}: root must be a JSON array")
            continue

        for index, record in enumerate(records):
            prefix = f"{dataset_name}[{index}]"
            if not isinstance(record, dict):
                errors.append(f"{prefix}: record must be an object")
                continue

            record_id = record.get("id")
            if not record_id:
                errors.append(f"{prefix}: missing id")
            elif record_id in seen:
                errors.append(f"{prefix}: duplicate id {record_id}")
            else:
                seen.add(record_id)

            if not record.get("name"):
                errors.append(f"{prefix}: missing name")

    for index, actor in enumerate(actors):
        prefix = f"actors[{index}]"
        if actor.get("type") != "actor":
            errors.append(f"{prefix}: type must be actor")
        if actor.get("confidence") not in CONFIDENCE:
            errors.append(f"{prefix}: invalid confidence")
        if not valid_date(actor.get("last_verified")):
            errors.append(f"{prefix}: invalid last_verified date")
        sources = actor.get("sources")
        if not sources:
            errors.append(f"{prefix}: at least one source is required")
            continue
        for sidx, source in enumerate(sources):
            sp = f"{prefix}.sources[{sidx}]"
            if source.get("grade") not in GRADES:
                errors.append(f"{sp}: invalid source grade")
            if not check_https(source.get("url")):
                errors.append(f"{sp}: source URL must use https")

    for index, technique in enumerate(techniques):
        prefix = f"techniques[{index}]"
        if technique.get("type") != "technique":
            errors.append(f"{prefix}: type must be technique")
        if not technique.get("summary"):
            errors.append(f"{prefix}: missing summary")
        if not technique.get("mappings"):
            errors.append(f"{prefix}: at least one framework mapping is required")

    for index, test_case in enumerate(test_cases):
        prefix = f"test-cases[{index}]"
        if test_case.get("mode") not in {"safe-lab", "detection-simulation"}:
            errors.append(f"{prefix}: invalid mode")
        if not test_case.get("category"):
            errors.append(f"{prefix}: missing category")
        if not test_case.get("goal"):
            errors.append(f"{prefix}: missing goal")
        if not test_case.get("stimulus"):
            errors.append(f"{prefix}: missing stimulus")
        if not test_case.get("expected"):
            errors.append(f"{prefix}: missing expected behavior")
        if not test_case.get("telemetry"):
            errors.append(f"{prefix}: telemetry must not be empty")
        if not test_case.get("controls"):
            errors.append(f"{prefix}: controls must not be empty")
        if not test_case.get("mappings"):
            errors.append(f"{prefix}: mappings must not be empty")

    if not isinstance(landscape, dict):
        errors.append("threat-landscape-2026: root must be a JSON object")
    else:
        meta = landscape.get("meta", {})
        if meta.get("as_of") and not valid_date(meta.get("as_of")):
            errors.append("threat-landscape-2026.meta.as_of: invalid date")
        metrics = landscape.get("key_metrics", [])
        domains = landscape.get("domains", [])
        cases = landscape.get("notable_cases", [])
        if not metrics:
            errors.append("threat-landscape-2026: key_metrics must not be empty")
        if not domains:
            errors.append("threat-landscape-2026: domains must not be empty")
        for index, metric in enumerate(metrics):
            prefix = f"threat-landscape-2026.key_metrics[{index}]"
            if metric.get("confidence") not in CONFIDENCE:
                errors.append(f"{prefix}: invalid confidence")
            source = metric.get("source", {})
            if source.get("grade") not in GRADES:
                errors.append(f"{prefix}.source: invalid grade")
            if not check_https(source.get("url")):
                errors.append(f"{prefix}.source: URL must use https")
        for index, domain in enumerate(domains):
            prefix = f"threat-landscape-2026.domains[{index}]"
            if domain.get("confidence") not in CONFIDENCE:
                errors.append(f"{prefix}: invalid confidence")
            if not domain.get("defensive_focus"):
                errors.append(f"{prefix}: defensive_focus must not be empty")
        for index, case in enumerate(cases):
            prefix = f"threat-landscape-2026.notable_cases[{index}]"
            if case.get("confidence") not in CONFIDENCE:
                errors.append(f"{prefix}: invalid confidence")
            source = case.get("source", {})
            if source.get("grade") not in GRADES:
                errors.append(f"{prefix}.source: invalid grade")
            if not check_https(source.get("url")):
                errors.append(f"{prefix}.source: URL must use https")

    for index, model in enumerate(models):
        prefix = f"models[{index}]"
        if not model.get("provider"):
            errors.append(f"{prefix}: missing provider")
        if not model.get("deployment"):
            errors.append(f"{prefix}: missing deployment")
        if not check_https(model.get("official")):
            errors.append(f"{prefix}: official URL must use https")

    for index, framework in enumerate(frameworks):
        prefix = f"frameworks[{index}]"
        if not check_https(framework.get("url")):
            errors.append(f"{prefix}: URL must use https")
        if not framework.get("category"):
            errors.append(f"{prefix}: missing category")

    if errors:
        print("LLMInjection intelligence validation FAILED")
        for error in errors:
            print(f" - {error}")
        return 1

    print(
        "LLMInjection intelligence validation OK: "
        f"{len(frameworks)} frameworks, "
        f"{len(actors)} actors, "
        f"{len(techniques)} techniques, "
        f"{len(models)} model families, "
        f"{len(test_cases)} test cases, "
        f"{len(landscape.get('key_metrics', [])) if isinstance(landscape, dict) else 0} landscape metrics"
    )
    return 0


if __name__ == "__main__":
    sys.exit(validate())
