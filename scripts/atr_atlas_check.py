#!/usr/bin/env python3
"""Check the MITRE ATLAS technique IDs cited by Agent Threat Rules against the ATLAS data (stdlib only).

ATR (Agent-Threat-Rule/agent-threat-rules, MIT) tags every rule with ATLAS techniques. Before LLMInjection extends its own
mappings from them, each cited ID is checked against a clone of mitre-atlas/atlas-data:

  unknown-id        the ID is not in the current ATLAS release; the report says in which release it was last seen
  renamed           ATR labels the ID with a name that is not the current ATLAS name (stale after a rename)
  ok                the ID exists and ATR's label is the current name, or the same name with a parent prefix
  case-study        the ID is an ATLAS case study (AML.CS...), which is evidence, not a technique

It also reports which cited IDs LLMInjection already maps (`already_mapped_by`) and which it does not. It never edits
data/techniques.json: the report is a work list for an analyst, not a mapping.

    git clone --depth 1 https://github.com/Agent-Threat-Rule/agent-threat-rules.git /tmp/atr
    git clone --depth 1 https://github.com/mitre-atlas/atlas-data.git /tmp/atlas
    python scripts/atr_atlas_check.py --atr /tmp/atr --atlas /tmp/atlas --write

Cloned content is untrusted: both trees are only read as text, never executed.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import ROOT, load_data, write_json  # noqa: E402

OUT = ROOT / "references" / "crosswalks" / "atr-atlas.json"


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def parse_atlas(path: Path) -> tuple[str, dict[str, dict[str, str]]]:
    """ID -> {name, maturity} for techniques and case studies of an ATLAS v6 YAML file, with a line scanner (no YAML library)."""
    version, entries, current, in_block = "", {}, None, False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("  version:") and not version:
            version = raw.split(":", 1)[1].strip().strip("'\"")
        if raw and not raw.startswith(" "):  # top-level key: only techniques and case studies are read
            in_block, current = raw in ("techniques:", "case-studies:"), None
            continue
        if not in_block:
            continue
        m = re.match(r"^  (AML\.(?:T\d{4}(?:\.\d{3})?|CS\d{4})):$", raw)
        if m:
            current = entries.setdefault(m.group(1), {})
        elif current is not None:
            f = re.match(r"^    (name|maturity): (.*)$", raw)
            if f:
                current[f.group(1)] = f.group(2).strip().strip("'\"")
    return version, entries


def release_key(path: Path) -> tuple[int, ...]:
    return tuple(int(p) for p in re.findall(r"\d+", path.stem))


def last_seen(atlas_root: Path, ids: set[str]) -> dict[str, dict[str, str]]:
    """For IDs missing from the current release: the newest older release that still had them, and the name used there."""
    found: dict[str, dict[str, str]] = {}
    for path in sorted((atlas_root / "dist" / "v6").glob("ATLAS-20*.yaml"), key=release_key):
        text = path.read_text(encoding="utf-8")
        for ident in ids:
            m = re.search(rf"^  {re.escape(ident)}:\n(?:    .*\n)*?    name: (.*)$", text, re.M)
            if m:
                found[ident] = {"release": path.stem.removeprefix("ATLAS-"), "name": m.group(1).strip().strip("'\"")}
    return found


def parse_atr_rule(text: str) -> dict[str, Any] | None:
    """Rule id, status and the ATLAS references (id + ATR's own label) of one ATR rule file."""
    rid = re.search(r"^id: (ATR-[\w-]+)", text, re.M)
    if not rid:
        return None
    status = re.search(r'^status: "?([\w-]+)"?', text, re.M)
    refs: list[tuple[str, str]] = []
    block = re.search(r"^  mitre_atlas:\n((?:    - .*\n)+)", text, re.M)
    if block:
        for line in block.group(1).splitlines():
            value = line.strip()[2:].strip().strip("\"'")
            ident, _, label = value.partition(" - ")
            refs.append((ident.strip(), label.strip()))
    return {"id": rid.group(1), "status": status.group(1) if status else "", "atlas": refs}


def collect_atr(root: Path) -> list[dict[str, Any]]:
    rules = []
    for path in sorted((root / "rules").rglob("*.yaml")):
        rule = parse_atr_rule(path.read_text(encoding="utf-8", errors="ignore"))
        if rule:
            rule["category"] = path.relative_to(root / "rules").parts[0]
            rules.append(rule)
    return rules


def mapped_by_llmi() -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for t in load_data("techniques"):
        for m in t.get("external_mappings", []):
            if m["framework"] == "MITRE ATLAS":
                out[m["id"]].append(t["id"])
    return out


def analyse(rules: list[dict[str, Any]], atlas: dict[str, dict[str, str]], history: dict[str, dict[str, str]] | None = None) -> list[dict[str, Any]]:
    cited: dict[str, dict[str, Any]] = {}
    for rule in rules:
        for ident, label in rule["atlas"]:
            row = cited.setdefault(ident, {"rules": 0, "categories": Counter(), "labels": Counter()})
            row["rules"] += 1
            row["categories"][rule["category"]] += 1
            row["labels"][label or "(no label)"] += 1
    ours = mapped_by_llmi()
    rows = []
    for ident, row in sorted(cited.items(), key=lambda kv: (-kv[1]["rules"], kv[0])):
        current = atlas.get(ident)
        labels = [k for k in row["labels"] if k != "(no label)"]
        if current is None:
            status = "unknown-id"
        elif ident.startswith("AML.CS"):
            status = "case-study"
        elif any(not norm(label).endswith(norm(current["name"])) for label in labels):
            status = "renamed"  # an ATR label is neither the current name nor "<parent>: <current name>"
        else:
            status = "ok"
        rows.append({
            "atlas_id": ident,
            "atlas_name": current["name"] if current else None,
            "atlas_maturity": current.get("maturity") if current else None,
            "status": status,
            "atr_rules": row["rules"],
            "atr_categories": dict(row["categories"].most_common()),
            "atr_labels": dict(row["labels"].most_common()),
            "already_mapped_by": ours.get(ident, []),
            **({"last_seen": (history or {})[ident]} if status == "unknown-id" and ident in (history or {}) else {}),
        })
    return rows


def check_ours(atlas: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    """LLMInjection's own ATLAS mappings that are missing from, or named differently in, the ATLAS release."""
    problems = []
    for t in load_data("techniques"):
        for m in t.get("external_mappings", []):
            if m["framework"] != "MITRE ATLAS":
                continue
            current = atlas.get(m["id"])
            if current is None:
                problems.append({"technique": t["id"], "atlas_id": m["id"], "problem": "missing-in-atlas", "ours": m["name"]})
            elif not norm(m["name"]).endswith(norm(current["name"])):
                problems.append({"technique": t["id"], "atlas_id": m["id"], "problem": "name-differs", "ours": m["name"], "atlas": current["name"]})
    return problems


def git_head(path: Path) -> dict[str, str]:
    def run(*args: str) -> str:
        return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True).stdout.strip()

    return {"commit": run("rev-parse", "HEAD"), "date": run("log", "-1", "--format=%cs")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--atr", required=True, help="clone of Agent-Threat-Rule/agent-threat-rules")
    ap.add_argument("--atlas", required=True, help="clone of mitre-atlas/atlas-data")
    ap.add_argument("--write", action="store_true", help=f"write {OUT.relative_to(ROOT)}")
    args = ap.parse_args()

    atr, atlas_root = Path(args.atr), Path(args.atlas)
    version, atlas = parse_atlas(atlas_root / "dist" / "v6" / "ATLAS-latest.yaml")
    rules = collect_atr(atr)
    cited = {i for r in rules for i, _ in r["atlas"]}
    rows = analyse(rules, atlas, last_seen(atlas_root, {i for i in cited if i not in atlas}))
    counts = Counter(r["status"] for r in rows)
    report = {
        "schema_version": "1.0",
        "note": "Work list, not a mapping. ATLAS IDs cited by Agent Threat Rules, checked against the ATLAS data. Discovery and test-design material; ATR rules are hypotheses, never evidence of attribution or campaigns.",
        "atr": {"repo": "Agent-Threat-Rule/agent-threat-rules", "license": "MIT", **git_head(atr), "rules": len(rules)},
        "atlas": {"repo": "mitre-atlas/atlas-data", "license": "Apache-2.0", "version": version, **git_head(atlas_root), "techniques": sum(1 for i in atlas if ".T" in i)},
        "summary": {"cited_ids": len(rows), **dict(counts), "not_yet_mapped": sum(1 for r in rows if not r["already_mapped_by"] and r["status"] != "unknown-id")},
        "llminjection_mappings_to_fix": check_ours(atlas),
        "ids": rows,
    }
    print(f"ATR rules {len(rules)} · ATLAS {version} ({len(atlas)} techniques) · cited IDs {len(rows)}: {dict(counts)}")
    for r in rows:
        if r["status"] not in ("ok", "case-study"):
            print(f"  {r['status']:10} {r['atlas_id']:15} ATLAS: {r['atlas_name']!s:42} ATR: {list(r['atr_labels'])[:2]} {r.get('last_seen', '')}")
    for p in report["llminjection_mappings_to_fix"]:
        print(f"  OURS {p['problem']}: {p['technique']} {p['atlas_id']} {p['ours']!r}" + (f" -> {p['atlas']!r}" if "atlas" in p else ""))
    if args.write:
        write_json(OUT, report)
        print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
