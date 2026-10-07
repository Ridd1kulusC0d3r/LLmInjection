#!/usr/bin/env python3
"""Build a deterministic intelligence snapshot for change detection."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def flatten_document(filename: str, value: Any) -> list[dict]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]

    if filename == "threat-landscape-2026.json" and isinstance(value, dict):
        rows: list[dict] = []
        for section in ("key_metrics", "domains", "sector_signals", "notable_cases", "research_queue"):
            for index, item in enumerate(value.get(section, [])):
                if not isinstance(item, dict):
                    continue
                copy = dict(item)
                copy.setdefault("id", f"{section}:{index}")
                copy["_snapshot_section"] = section
                rows.append(copy)
        return rows

    if isinstance(value, dict):
        copy = dict(value)
        copy.setdefault("id", "__document__")
        return [copy]

    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(DATA / "dataset-manifest.json"))
    parser.add_argument("--output", default=str(ROOT / "dist" / "current-snapshot.json"))
    args = parser.parse_args()

    manifest = load(Path(args.manifest))
    datasets: dict[str, dict] = {}
    total_records = 0

    for filename in manifest.get("datasets", []):
        path = DATA / filename
        value = load(path)
        records = flatten_document(filename, value)
        ids: list[str] = []
        fingerprints: dict[str, str] = {}

        for index, record in enumerate(records):
            rid = str(record.get("id") or f"row:{index}")
            ids.append(rid)
            fingerprints[rid] = fingerprint(record)

        datasets[filename] = {
            "count": len(records),
            "ids": sorted(ids),
            "fingerprints": dict(sorted(fingerprints.items())),
            "document_sha256": fingerprint(value),
        }
        total_records += len(records)

    output = {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "snapshot_date": manifest.get("snapshot"),
        "dataset_schema_version": manifest.get("schema_version"),
        "status": manifest.get("status"),
        "total_records": total_records,
        "datasets": datasets,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built intelligence snapshot: datasets={len(datasets)}, records={total_records}, output={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
