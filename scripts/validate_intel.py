#!/usr/bin/env python3
"""Dependency-free validation for LLMInjection structured intelligence."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from maturity import derive_all as derive_maturity  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CONFIDENCE = {"confirmed", "high", "medium", "low", "unverified"}
GRADES = {"A", "B", "C", "D", "E"}
LAB_MODES = {"safe-lab", "detection-simulation"}
MATURITY = {"observed-in-the-wild", "disclosed-vulnerability", "research-demonstrated", "no-linked-evidence"}
ECO_CLASSES = {"framework-data", "incident-data", "detection-content", "curated-list", "assessment-tool",
               "benchmark", "research-technique", "defence-tool", "lab-exercise", "prompt-corpus"}
ECO_SECTIONS = {"knowledge", "catalog", "evaluation", "benchmark", "attack-research", "defence", "agent-security", "lab"}

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
    "ecosystem": "ecosystem.json",
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

def valid_datetime(value: str | None) -> bool:
    if value is None:
        return True
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except (TypeError, ValueError):
        return False

def validate():
    errors: list[str] = []
    datasets = {name: load_json(ROOT / "data" / filename) for name, filename in LIST_DATASETS.items()}
    landscape = load_json(ROOT / "data" / "threat-landscape-2026.json")
    manifest = load_json(ROOT / "data" / "dataset-manifest.json")
    contributors = load_json(ROOT / "data" / "contributors.json")
    source_feeds = load_json(ROOT / "data" / "source-feeds.json")
    research_queue = load_json(ROOT / "data" / "research-queue.json")
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
        for midx, mapping in enumerate(technique.get("external_mappings", [])):
            mp = f"{prefix}.external_mappings[{midx}]"
            if mapping.get("relation") not in {"exact", "related"}:
                errors.append(f"{mp}: relation must be exact or related")
            if not mapping.get("framework") or not mapping.get("id") or not mapping.get("name"):
                errors.append(f"{mp}: framework, id and name are required")
            if not check_https(mapping.get("url")):
                errors.append(f"{mp}: URL must use https")

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

    published = {s["id"]: s.get("published") for s in datasets["sources"]}
    for i, source in enumerate(datasets["sources"]):
        if source.get("published") is not None and not valid_date(source["published"]):
            errors.append(f"sources[{i}]: invalid published date")
    for name in ("campaigns", "incidents"):
        for i, record in enumerate(datasets[name]):
            prefix = f"{name}[{i}]"
            reported = record.get("reported")
            if reported is None:
                continue
            if not valid_date(reported):
                errors.append(f"{prefix}: invalid reported date")
                continue
            dates = [published.get(sid) for sid in record.get("source_ids", [])]
            if dates and all(dates) and reported != min(dates):
                errors.append(f"{prefix}: reported {reported} must equal the earliest source publication date {min(dates)}")
            seen = record.get("first_seen") if name == "campaigns" else record.get("date")
            if seen and str(seen)[:4].isdigit() and str(seen)[:4] > reported[:4]:
                errors.append(f"{prefix}: {seen} is later than the primary report ({reported})")
            if "regions" in record and not all(isinstance(r, str) for r in record["regions"]):
                errors.append(f"{prefix}: regions must be strings")

    derived_maturity = derive_maturity()
    for i, technique in enumerate(datasets["techniques"]):
        level = technique.get("maturity")
        if level not in MATURITY:
            errors.append(f"techniques[{i}]: invalid maturity")
        elif level != derived_maturity.get(technique["id"]):
            errors.append(f"techniques[{i}]: maturity {level} does not match the graph-derived {derived_maturity.get(technique['id'])}")

    eco_urls: set[str] = set()
    for i, entry in enumerate(datasets["ecosystem"]):
        prefix = f"ecosystem[{i}]"
        if entry.get("type") != "ecosystem":
            errors.append(f"{prefix}: type must be ecosystem")
        if entry.get("evidence_class") not in ECO_CLASSES:
            errors.append(f"{prefix}: invalid evidence_class")
        if entry.get("section") not in ECO_SECTIONS:
            errors.append(f"{prefix}: invalid section")
        if entry.get("status") not in {"listed", "archived-reported", "active-verified", "archived-verified", "not-found"}:
            errors.append(f"{prefix}: invalid status")
        if entry.get("verified_at") is not None and not valid_date(entry["verified_at"]):
            errors.append(f"{prefix}: invalid verified_at")
        if entry.get("priority") not in {"start-here", "standard"}:
            errors.append(f"{prefix}: invalid priority")
        if entry.get("source_grade") not in GRADES:
            errors.append(f"{prefix}: invalid source_grade")
        url = entry.get("url", "")
        if not check_https(url) or not url.startswith("https://github.com/"):
            errors.append(f"{prefix}: url must be an https GitHub URL")
        elif url.lower() in eco_urls:
            errors.append(f"{prefix}: duplicate url {url}")
        eco_urls.add(url.lower())
        if not entry.get("summary") or not entry.get("provenance"):
            errors.append(f"{prefix}: summary and provenance are required")
        if not valid_date(entry.get("added")):
            errors.append(f"{prefix}: invalid added date")
        for tid in entry.get("techniques", []):
            if tid not in index or index[tid][0] != "techniques":
                errors.append(f"{prefix}: unknown technique {tid}")
        # Ecosystem entries are discovery and test-design material. They never support attribution or campaign claims.
        if {"attribution", "campaign"} & set(entry.get("supports", [])):
            errors.append(f"{prefix}: ecosystem entries cannot support attribution or campaign claims")

    feed_ids: set[str] = set()
    if not isinstance(source_feeds, dict) or not isinstance(source_feeds.get("feeds"), list):
        errors.append("source-feeds: root must contain a feeds array")
    else:
        for i, feed in enumerate(source_feeds.get("feeds", [])):
            prefix = f"source-feeds.feeds[{i}]"
            feed_id = feed.get("id")
            if not feed_id or not str(feed_id).startswith("FEED-"):
                errors.append(f"{prefix}: invalid feed id")
            elif feed_id in feed_ids:
                errors.append(f"{prefix}: duplicate feed id {feed_id}")
            else:
                feed_ids.add(feed_id)
            if feed.get("source_grade") not in GRADES:
                errors.append(f"{prefix}: invalid source grade")
            if not check_https(feed.get("url")):
                errors.append(f"{prefix}: URL must use https")
            if feed.get("relevance_mode") not in {"all", "keywords"}:
                errors.append(f"{prefix}: invalid relevance_mode")
            if feed.get("relevance_mode") == "keywords" and not feed.get("keywords"):
                errors.append(f"{prefix}: keyword mode requires keywords")

    if not isinstance(research_queue, dict) or not isinstance(research_queue.get("items"), list):
        errors.append("research-queue: root must contain an items array")
    else:
        queue_ids: set[str] = set()
        valid_statuses = {"candidate", "reviewing", "accepted", "rejected", "duplicate"}
        if not valid_datetime(research_queue.get("meta", {}).get("last_run")):
            errors.append("research-queue.meta.last_run: invalid datetime")
        for i, item in enumerate(research_queue.get("items", [])):
            prefix = f"research-queue.items[{i}]"
            item_id = item.get("id")
            if not item_id or not str(item_id).startswith("RQ-"):
                errors.append(f"{prefix}: invalid id")
            elif item_id in queue_ids:
                errors.append(f"{prefix}: duplicate id {item_id}")
            else:
                queue_ids.add(item_id)
            if item.get("status") not in valid_statuses:
                errors.append(f"{prefix}: invalid status")
            if item.get("source_feed_id") not in feed_ids:
                errors.append(f"{prefix}: unknown source_feed_id {item.get('source_feed_id')}")
            if item.get("source_grade") not in GRADES:
                errors.append(f"{prefix}: invalid source grade")
            if not check_https(item.get("url")):
                errors.append(f"{prefix}: URL must use https")
            if not valid_datetime(item.get("observed_at")):
                errors.append(f"{prefix}: invalid observed_at")
            score = item.get("relevance_score")
            if not isinstance(score, int) or not 0 <= score <= 100:
                errors.append(f"{prefix}: relevance_score must be 0..100")

    snapshots_dir = ROOT / "data" / "snapshots"
    if snapshots_dir.exists():
        for snapshot_path in sorted(snapshots_dir.glob("*.json")):
            snapshot = load_json(snapshot_path)
            if not isinstance(snapshot, dict) or snapshot.get("schema_version") != "1.0":
                errors.append(f"{snapshot_path.name}: invalid snapshot schema")
            if not isinstance(snapshot.get("datasets"), dict):
                errors.append(f"{snapshot_path.name}: datasets must be an object")

    if not isinstance(manifest, dict):
        errors.append("dataset-manifest: root must be an object")
    else:
        if not manifest.get("schema_version"):
            errors.append("dataset-manifest: missing schema_version")
        if not valid_date(manifest.get("snapshot")):
            errors.append("dataset-manifest: invalid snapshot date")
        for filename in manifest.get("datasets", []):
            if not (ROOT / "data" / filename).exists():
                errors.append(f"dataset-manifest: missing dataset {filename}")

    if not isinstance(contributors, list) or not contributors:
        errors.append("contributors: root must be a non-empty array")
    else:
        for i, contributor in enumerate(contributors):
            if not contributor.get("github") or not contributor.get("roles"):
                errors.append(f"contributors[{i}]: github and roles are required")

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
    queue_count = len(research_queue.get("items", [])) if isinstance(research_queue, dict) else 0
    feed_count = len(source_feeds.get("feeds", [])) if isinstance(source_feeds, dict) else 0
    print(
        f"LLMInjection intelligence validation OK: {counts}, "
        f"landscape-metrics={landscape_metrics}, feeds={feed_count}, "
        f"research-queue={queue_count}, schema={manifest.get('schema_version', 'unknown')}"
    )
    return 0

if __name__ == "__main__":
    sys.exit(validate())
