#!/usr/bin/env python3
"""Dependency-free validation for LLMInjection structured intelligence."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIDENCE = {"confirmed", "high", "medium", "low", "unverified"}
GRADES = {"A", "B", "C", "D", "E"}
LAB_MODES = {"safe-lab", "detection-simulation"}

LIST_DATASETS = {
    "frameworks": "frameworks.json",
    "actors": "actors.json",
    "campaigns": "campaigns.json",
    "incidents": "incidents.json",
    "techniques": "techniques.json",
    "models": "models.json",
    "test-cases": "test-cases.json",
    "controls": "controls.json",
    "detections": "detections.json",
    "sources": "sources.json",
    "vulnerabilities": "vulnerabilities.json",
    "relationships": "relationships.json",
}

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
    datasets = {name: load_json(ROOT / "data" / filename) for name, filename in LIST_DATASETS.items()}
    landscape = load_json(ROOT / "data" / "threat-landscape-2026.json")
    seen: set[str] = set()
    index: dict[str, tuple[str, dict]] = {}

    for dataset_name, records in datasets.items():
        if not isinstance(records, list):
            errors.append(f"{dataset_name}: root must be a JSON array")
            continue
        for i, record in enumerate(records):
            prefix = f"{dataset_name}[{i}]"
            if not isinstance(record, dict):
                errors.append(f"{prefix}: record must be an object")
                continue
            record_id = record.get("id")
            if not record_id:
                errors.append(f"{prefix}: missing id")
                continue
            if record_id in seen:
                errors.append(f"{prefix}: duplicate id {record_id}")
            else:
                seen.add(record_id)
                index[record_id] = (dataset_name, record)

    for i, actor in enumerate(datasets["actors"]):
        prefix = f"actors[{i}]"
        if actor.get("type") != "actor":
            errors.append(f"{prefix}: type must be actor")
        if actor.get("confidence") not in CONFIDENCE:
            errors.append(f"{prefix}: invalid confidence")
        if not valid_date(actor.get("last_verified")):
            errors.append(f"{prefix}: invalid last_verified date")
        for sidx, source in enumerate(actor.get("sources", [])):
            sp = f"{prefix}.sources[{sidx}]"
            if source.get("grade") not in GRADES:
                errors.append(f"{sp}: invalid source grade")
            if not check_https(source.get("url")):
                errors.append(f"{sp}: source URL must use https")

    for name in ("campaigns", "incidents"):
        for i, record in enumerate(datasets[name]):
            prefix = f"{name}[{i}]"
            if record.get("type") not in {"campaign", "incident"}:
                errors.append(f"{prefix}: invalid type")
            if record.get("confidence") not in CONFIDENCE:
                errors.append(f"{prefix}: invalid confidence")
            if not record.get("summary"):
                errors.append(f"{prefix}: missing summary")

    for i, source in enumerate(datasets["sources"]):
        prefix = f"sources[{i}]"
        if source.get("type") != "source":
            errors.append(f"{prefix}: type must be source")
        if source.get("grade") not in GRADES:
            errors.append(f"{prefix}: invalid grade")
        if not check_https(source.get("url")):
            errors.append(f"{prefix}: URL must use https")
        if not valid_date(source.get("last_verified")):
            errors.append(f"{prefix}: invalid last_verified")

    for dataset_name in ("campaigns", "incidents", "controls", "vulnerabilities"):
        for i, record in enumerate(datasets[dataset_name]):
            for source_id in record.get("source_ids", []):
                if source_id not in index or index[source_id][0] != "sources":
                    errors.append(f"{dataset_name}[{i}]: unknown source_id {source_id}")

    for i, vuln in enumerate(datasets["vulnerabilities"]):
        prefix = f"vulnerabilities[{i}]"
        if vuln.get("type") != "vulnerability":
            errors.append(f"{prefix}: type must be vulnerability")
        if vuln.get("confidence") not in CONFIDENCE:
            errors.append(f"{prefix}: invalid confidence")
        if not vuln.get("identifiers"):
            errors.append(f"{prefix}: identifiers must not be empty")
        if not valid_date(vuln.get("published")):
            errors.append(f"{prefix}: invalid published date")
        if not vuln.get("package") or not vuln.get("summary"):
            errors.append(f"{prefix}: package and summary are required")

    for i, technique in enumerate(datasets["techniques"]):
        prefix = f"techniques[{i}]"
        if technique.get("type") != "technique":
            errors.append(f"{prefix}: type must be technique")
        if not technique.get("summary"):
            errors.append(f"{prefix}: missing summary")
        if not technique.get("mappings"):
            errors.append(f"{prefix}: at least one framework mapping is required")

    for i, test_case in enumerate(datasets["test-cases"]):
        prefix = f"test-cases[{i}]"
        if test_case.get("mode") not in LAB_MODES:
            errors.append(f"{prefix}: invalid mode")
        for field in ("category", "goal", "stimulus", "expected"):
            if not test_case.get(field):
                errors.append(f"{prefix}: missing {field}")
        for field in ("telemetry", "controls", "mappings"):
            if not test_case.get(field):
                errors.append(f"{prefix}: {field} must not be empty")

    for i, detection in enumerate(datasets["detections"]):
        prefix = f"detections[{i}]"
        if detection.get("type") != "detection":
            errors.append(f"{prefix}: type must be detection")
        if not detection.get("hypothesis") or not detection.get("telemetry"):
            errors.append(f"{prefix}: hypothesis and telemetry are required")
        for test_id in detection.get("test_ids", []):
            if test_id not in index or index[test_id][0] != "test-cases":
                errors.append(f"{prefix}: unknown test_id {test_id}")

    for i, model in enumerate(datasets["models"]):
        prefix = f"models[{i}]"
        if not model.get("provider") or not model.get("deployment"):
            errors.append(f"{prefix}: provider and deployment are required")
        if not check_https(model.get("official")):
            errors.append(f"{prefix}: official URL must use https")

    for i, framework in enumerate(datasets["frameworks"]):
        prefix = f"frameworks[{i}]"
        if not check_https(framework.get("url")):
            errors.append(f"{prefix}: URL must use https")
        if not framework.get("category"):
            errors.append(f"{prefix}: missing category")

    for i, rel in enumerate(datasets["relationships"]):
        prefix = f"relationships[{i}]"
        if rel.get("type") != "relationship":
            errors.append(f"{prefix}: type must be relationship")
        if rel.get("confidence") not in CONFIDENCE:
            errors.append(f"{prefix}: invalid confidence")
        for endpoint in ("source", "target"):
            ref = rel.get(endpoint)
            if ref not in index:
                errors.append(f"{prefix}: dangling {endpoint} reference {ref}")
        for source_id in rel.get("evidence_sources", []):
            if source_id not in index or index[source_id][0] != "sources":
                errors.append(f"{prefix}: unknown evidence source {source_id}")

    if not isinstance(landscape, dict):
        errors.append("threat-landscape-2026: root must be a JSON object")
    else:
        meta = landscape.get("meta", {})
        if meta.get("as_of") and not valid_date(meta.get("as_of")):
            errors.append("threat-landscape-2026.meta.as_of: invalid date")
        for i, metric in enumerate(landscape.get("key_metrics", [])):
            prefix = f"threat-landscape-2026.key_metrics[{i}]"
            if metric.get("confidence") not in CONFIDENCE:
                errors.append(f"{prefix}: invalid confidence")
            source = metric.get("source", {})
            if source.get("grade") not in GRADES or not check_https(source.get("url")):
                errors.append(f"{prefix}: invalid source")
        for i, domain in enumerate(landscape.get("domains", [])):
            if domain.get("confidence") not in CONFIDENCE:
                errors.append(f"threat-landscape-2026.domains[{i}]: invalid confidence")

    if errors:
        print("LLMInjection intelligence validation FAILED")
        for error in errors:
            print(f" - {error}")
        return 1

    counts = ", ".join(f"{name}={len(records)}" for name, records in datasets.items())
    landscape_metrics = len(landscape.get("key_metrics", [])) if isinstance(landscape, dict) else 0
    print(f"LLMInjection intelligence validation OK: {counts}, landscape-metrics={landscape_metrics}")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
