#!/usr/bin/env python3
"""Compare two LLMInjection intelligence snapshots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def render_markdown(result: dict) -> str:
    summary = result["summary"]
    lines = [
        "# Intelligence Diff",
        "",
        f"- Baseline: {result['baseline']}",
        f"- Current: {result['current']}",
        f"- Added objects: **{summary['added']}**",
        f"- Removed objects: **{summary['removed']}**",
        f"- Changed objects: **{summary['changed']}**",
        "",
        "## Dataset changes",
        "",
        "| Dataset | Added | Removed | Changed |",
        "|---|---:|---:|---:|",
    ]
    for name, change in result["datasets"].items():
        lines.append(
            f"| {name} | {len(change['added'])} | {len(change['removed'])} | {len(change['changed'])} |"
        )

    for name, change in result["datasets"].items():
        if not any(change[key] for key in ("added", "removed", "changed")):
            continue
        lines.extend(["", f"## {name}", ""])
        for key in ("added", "removed", "changed"):
            if change[key]:
                lines.append(f"### {key.title()}")
                lines.append("")
                lines.extend(f"- {value}" for value in change[key])
                lines.append("")

    if summary["added"] == summary["removed"] == summary["changed"] == 0:
        lines.extend(["", "No structured-intelligence changes were detected.", ""])

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--current", required=True)
    parser.add_argument("--output", default="dist/intelligence-diff.json")
    parser.add_argument("--markdown", default="dist/intelligence-diff.md")
    args = parser.parse_args()

    baseline = load(Path(args.baseline))
    current = load(Path(args.current))
    names = sorted(set(baseline.get("datasets", {})) | set(current.get("datasets", {})))

    result = {
        "schema_version": "1.0",
        "baseline": baseline.get("generated_at") or baseline.get("snapshot_date"),
        "current": current.get("generated_at") or current.get("snapshot_date"),
        "summary": {"added": 0, "removed": 0, "changed": 0},
        "datasets": {},
    }

    for name in names:
        before = baseline.get("datasets", {}).get(name, {})
        after = current.get("datasets", {}).get(name, {})
        before_ids = set(before.get("ids", []))
        after_ids = set(after.get("ids", []))
        added = sorted(after_ids - before_ids)
        removed = sorted(before_ids - after_ids)

        changed: list[str] = []
        before_fp = before.get("fingerprints", {})
        after_fp = after.get("fingerprints", {})
        if before_fp and after_fp:
            changed = sorted(
                rid
                for rid in before_ids & after_ids
                if before_fp.get(rid) != after_fp.get(rid)
            )

        result["datasets"][name] = {
            "added": added,
            "removed": removed,
            "changed": changed,
            "before_count": before.get("count", 0),
            "after_count": after.get("count", 0),
        }
        result["summary"]["added"] += len(added)
        result["summary"]["removed"] += len(removed)
        result["summary"]["changed"] += len(changed)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    markdown = Path(args.markdown)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(render_markdown(result), encoding="utf-8")

    print(
        "Intelligence diff: "
        f"added={result['summary']['added']}, "
        f"removed={result['summary']['removed']}, "
        f"changed={result['summary']['changed']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
