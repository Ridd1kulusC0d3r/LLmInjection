#!/usr/bin/env python3
"""Map the AI-security skills of a third-party skills catalogue to LLMInjection, and check what can be trusted (stdlib only).

Source: mukul975/anthropic-cybersecurity-skills (Apache-2.0, an independent community project, not affiliated with
Anthropic). It holds 800+ "skills": procedures an AI agent can read and carry out. LLMInjection does not copy them. It
links to them by name and records which of its own techniques each one helps with, so an analyst who needs the "how to"
behind a technique knows where a procedure exists.

What the script establishes from a clone of that repository:

  * the skills whose `subdomain` is `ai-security` (the only ones this repository maps), with version and licence;
  * whether each ATLAS ID they declare exists in ATLAS (clone of mitre-atlas/atlas-data, optional);
  * how many other skills carry ATLAS tags, and how many of those tags point at LLMInjection techniques although the
    skill is not about AI (an audit of the catalogue's tagging, not a mapping).

The mapping to LLMInjection techniques is analyst judgement, kept in CURATED below and reviewed by hand against each
skill's description. It is never derived from ATLAS tags: on the non-AI skills those tags are not meaningful.

    git clone --depth 1 https://github.com/mukul975/anthropic-cybersecurity-skills.git /tmp/skills
    git clone --depth 1 https://github.com/mitre-atlas/atlas-data.git /tmp/atlas
    python scripts/skills_catalog_check.py --skills /tmp/skills --atlas /tmp/atlas --write

Cloned content is untrusted: it is read as text and never executed.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from atr_atlas_check import parse_atlas  # noqa: E402
from common import ROOT, load_data, write_json  # noqa: E402

OUT = ROOT / "references" / "crosswalks" / "anthropic-cybersecurity-skills.json"
REPO = "mukul975/anthropic-cybersecurity-skills"
URL = f"https://github.com/{REPO}/tree/main/skills/"

# Analyst judgement, read against each skill's description: which LLMInjection techniques the procedure helps a defender with.
CURATED: dict[str, dict[str, Any]] = {
    "assessing-vector-and-embedding-weaknesses": {"techniques": ["LLMI-T007", "LLMI-T004"], "role": "assess", "note": "vector-store isolation, embedding inversion and poisoning"},
    "auditing-mcp-servers-for-tool-poisoning": {"techniques": ["LLMI-T021", "LLMI-T011"], "role": "audit", "note": "tool poisoning, shadowing and rug pulls with an MCP scanner"},
    "continuous-llm-red-teaming-with-promptfoo": {"techniques": ["LLMI-T001", "LLMI-T002", "LLMI-T003"], "role": "test", "note": "red-team regression gate in CI"},
    "defending-llms-with-guardrails": {"techniques": ["LLMI-T001", "LLMI-T003"], "role": "defend", "note": "runtime classifiers and rails in front of the model"},
    "detecting-ai-model-prompt-injection-attacks": {"techniques": ["LLMI-T001", "LLMI-T002"], "role": "detect", "note": "signature, heuristic and classifier detection of injection"},
    "detecting-data-and-model-poisoning": {"techniques": ["LLMI-T006"], "role": "detect", "note": "poisoned training data and backdoored models"},
    "detecting-indirect-prompt-injection": {"techniques": ["LLMI-T002", "LLMI-T017", "LLMI-T025"], "role": "detect", "note": "hidden and obfuscated content in documents, pages and images"},
    "detecting-model-extraction-attacks": {"techniques": ["LLMI-T005", "LLMI-T019"], "role": "detect", "note": "per-principal query monitoring on inference APIs"},
    "implementing-llm-guardrails-for-security": {"techniques": ["LLMI-T001", "LLMI-T003", "LLMI-T004"], "role": "defend", "note": "input and output validation, PII and schema checks"},
    "orchestrating-llm-attacks-with-pyrit": {"techniques": ["LLMI-T001", "LLMI-T003"], "role": "test", "note": "multi-turn adversarial testing in an authorised lab"},
    "red-teaming-llms-with-garak": {"techniques": ["LLMI-T001", "LLMI-T003", "LLMI-T004"], "role": "test", "note": "probe suites and hit-rate triage"},
    "securing-agentic-ai-tool-invocation": {"techniques": ["LLMI-T008"], "role": "defend", "note": "allowlist, identity binding, approval and audit at the tool boundary"},
    "testing-for-system-prompt-leakage": {"techniques": ["LLMI-T004"], "role": "test", "note": "system-prompt and embedded-secret leakage"},
    "testing-prompt-injection-in-rag-pipelines": {"techniques": ["LLMI-T002", "LLMI-T007"], "role": "test", "note": "poisoned retrieved documents and embedding manipulation"},
}

# Names that mark offensive or dual-use procedures. Used to count and to describe the tier, never to select anything.
OFFENSIVE = re.compile(r"^(exploiting|abusing|attacking|cracking|bypassing|crafting|poisoning|conducting-.*(pentest|penetration|social-engineering|red-team)|performing-.*(attack|exploit|escalation|injection))")


def frontmatter(text: str) -> dict[str, Any]:
    """Top-level keys of a SKILL.md frontmatter: scalars as strings, `- item` lists as lists."""
    block = re.match(r"^---\n(.*?)\n---", text, re.S)
    out: dict[str, Any] = {}
    key = ""
    for line in (block.group(1) if block else "").splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            out[key] = m.group(2).strip().strip("'\"") if m.group(2).strip() else []
        elif line.startswith("- ") and isinstance(out.get(key), list):
            out[key].append(line[2:].strip().strip("'\""))
    return out


def read_skills(root: Path) -> list[dict[str, Any]]:
    skills = []
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        fm = frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
        skills.append({
            "name": path.parent.name, "subdomain": str(fm.get("subdomain", "")), "version": str(fm.get("version", "")),
            "license": str(fm.get("license", "")), "atlas": sorted(set(re.findall(r"AML\.T\d{4}(?:\.\d{3})?", " ".join(fm.get("atlas_techniques", []) or [])))),
        })
    return skills


def ours_by_atlas() -> dict[str, set[str]]:
    out: dict[str, set[str]] = defaultdict(set)
    for t in load_data("techniques"):
        for m in t.get("external_mappings", []):
            if m["framework"] == "MITRE ATLAS":
                out[m["id"]].add(t["id"])
    return out


def build(skills: list[dict[str, Any]], atlas: dict[str, dict[str, str]] | None, commit: dict[str, str]) -> dict[str, Any]:
    known_techniques = {t["id"] for t in load_data("techniques")}
    by_name = {s["name"]: s for s in skills}
    ai = [s for s in skills if s["subdomain"] == "ai-security"]
    missing = sorted(set(CURATED) - set(by_name))
    unmapped = sorted(s["name"] for s in ai if s["name"] not in CURATED)
    ours = ours_by_atlas()
    others = [s for s in skills if s["subdomain"] != "ai-security" and s["atlas"]]
    overlapping = [s for s in others if any(i in ours for i in s["atlas"])]
    entries = []
    for name in sorted(CURATED):
        s = by_name.get(name)
        cur = CURATED[name]
        bad = [t for t in cur["techniques"] if t not in known_techniques]
        entries.append({
            "name": name, "url": URL + name, "role": cur["role"], "note": cur["note"], "llminjection_techniques": cur["techniques"],
            "version": s["version"] if s else None, "license": s["license"] if s else None, "atlas_declared": s["atlas"] if s else [],
            "atlas_unknown": sorted(i for i in (s["atlas"] if s else []) if atlas is not None and i not in atlas),
            **({"unknown_llminjection_ids": bad} if bad else {}),
        })
    return {
        "schema_version": "1.0",
        "note": "Pointers only. LLMInjection links to these procedures and maps them to its own techniques by analyst judgement; it does not copy their content. An independent community project, not affiliated with Anthropic. Not evidence of any threat.",
        "source": {"repo": REPO, "license": "Apache-2.0", **commit, "skills_total": len(skills)},
        "tiers": {
            "ai-security": {"count": len(ai), "policy": "mapped by name to LLMInjection techniques, link only"},
            "other-skills-with-atlas-tags": {"count": len(others), "policy": "not mapped: the ATLAS tags are not meaningful outside AI"},
            "of-which-point-at-llminjection-techniques": len(overlapping),
            "offensive-or-dual-use-by-name": {"count": sum(1 for s in skills if OFFENSIVE.match(s["name"])), "policy": "not mapped; revisit only through ATT&CK IDs and an explicit analyst decision"},
        },
        "audit": {
            "curated_skills_missing_from_catalogue": missing, "ai_security_skills_not_curated": unmapped,
            "examples_of_non_ai_skills_with_atlas_tags": [{"name": s["name"], "subdomain": s["subdomain"], "atlas": s["atlas"][:3]} for s in overlapping[:6]],
        },
        "skills": entries,
    }


def git_head(path: Path) -> dict[str, str]:
    def run(*args: str) -> str:
        return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True).stdout.strip()

    return {"commit": run("rev-parse", "HEAD"), "date": run("log", "-1", "--format=%cs")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skills", required=True, help="clone of mukul975/anthropic-cybersecurity-skills")
    ap.add_argument("--atlas", help="clone of mitre-atlas/atlas-data, to check the ATLAS IDs the skills declare")
    ap.add_argument("--write", action="store_true", help=f"write {OUT.relative_to(ROOT)}")
    args = ap.parse_args()

    root = Path(args.skills)
    atlas = parse_atlas(Path(args.atlas) / "dist" / "v6" / "ATLAS-latest.yaml")[1] if args.atlas else None
    report = build(read_skills(root), atlas, git_head(root))
    t = report["tiers"]
    print(f"{report['source']['skills_total']} skills; ai-security {t['ai-security']['count']}; other skills with ATLAS tags "
          f"{t['other-skills-with-atlas-tags']['count']} ({t['of-which-point-at-llminjection-techniques']} point at our techniques); "
          f"offensive by name {t['offensive-or-dual-use-by-name']['count']}")
    for key in ("curated_skills_missing_from_catalogue", "ai_security_skills_not_curated"):
        if report["audit"][key]:
            print(f"  {key}: {report['audit'][key]}")
    if args.write:
        write_json(OUT, report)
        print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
