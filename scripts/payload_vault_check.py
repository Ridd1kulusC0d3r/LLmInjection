#!/usr/bin/env python3
"""Cross-reference the LLM Red Team Payload Vault with LLMInjection's techniques and safe tests (stdlib only).

The vault (crazywifi/Redteam_LLM_Injection_payloads) is a set of single-page HTML libraries holding about a
thousand prompt-injection payloads, sorted into categories that follow the OWASP Top 10 for LLM Applications.
The repository declares no licence, so nothing of it is copied here: the crosswalk keeps, per payload, the
vault's own ID, the short technique label it gives, its category and a SHA-256 of the payload text. That is
enough to count coverage, find duplicates across libraries and pick payloads by ID from the vault when an
authorised test needs them.

    git clone --depth 1 https://github.com/crazywifi/Redteam_LLM_Injection_payloads.git /tmp/vault
    python scripts/payload_vault_check.py --vault /tmp/vault            # report
    python scripts/payload_vault_check.py --vault /tmp/vault --write    # references/crosswalks/payload-vault.json

The HTML is untrusted input: it is read as text and its script blocks are parsed, never executed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import load_data  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "references" / "crosswalks" / "payload-vault.json"
REPO = "https://github.com/crazywifi/Redteam_LLM_Injection_payloads"

LIBRARIES = {  # file -> (library name, JavaScript variable holding {category: [payloads]})
    "Redteam_LLM_Injection_payloads.html": ("core", "library"),
    "Enterprise&Corporate_LLM_Prompt_injection_Test_Library.html": ("enterprise", "DATA"),
    "Financial&Banking_LLM_Prompt_injection_Test_Library.html": ("financial", "ALL_DATA"),
    "Medical&Healthcare_LLM_Prompt_injection_Test_Library.html": ("medical", "DATA"),
}

# vault category -> (OWASP LLM Top 10 2025 IDs, LLMInjection techniques). Analyst mapping, kept in one place.
CATEGORY_MAP: dict[str, tuple[list[str], list[str]]] = {
    "instruction override": (["LLM01"], ["LLMI-T001"]),
    "system prompt extraction": (["LLM07"], ["LLMI-T004"]),
    "prompt leakage": (["LLM07"], ["LLMI-T004"]),
    "roleplay / jailbreak": (["LLM01"], ["LLMI-T003"]),
    "jailbreak": (["LLM01"], ["LLMI-T003"]),
    "indirect injection (rag)": (["LLM01", "LLM08"], ["LLMI-T002", "LLMI-T007"]),
    "indirect injection": (["LLM01"], ["LLMI-T002"]),
    "rag": (["LLM08"], ["LLMI-T007"]),
    "encoding attacks": (["LLM01"], ["LLMI-T001"]),
    "obfuscation": (["LLM01"], ["LLMI-T001"]),
    "advanced mutations": (["LLM01"], ["LLMI-T001"]),
    "social engineering": (["LLM01"], ["LLMI-T003"]),
    "data exfiltration": (["LLM02"], ["LLMI-T004", "LLMI-T020"]),
    "tool / agent exploitation": (["LLM06"], ["LLMI-T008", "LLMI-T021"]),
    "tool": (["LLM06"], ["LLMI-T008"]),
    "multi-turn attacks": (["LLM01"], ["LLMI-T003"]),
    "multi-turn": (["LLM01"], ["LLMI-T003"]),
    "sql & code injection": (["LLM05"], ["LLMI-T020", "LLMI-T013"]),
    "code injection": (["LLM05"], ["LLMI-T020"]),
    "debug / audit": (["LLM07"], ["LLMI-T004"]),
    "cross-modal injection": (["LLM01"], ["LLMI-T025"]),
    "cross-modal": (["LLM01"], ["LLMI-T025"]),
    "persistent injection": (["LLM01"], ["LLMI-T009"]),
    "privilege escalation": (["LLM06"], ["LLMI-T008"]),
    "token smuggling": (["LLM01"], ["LLMI-T001"]),
    "sensitive": (["LLM02"], ["LLMI-T004"]),
}


def js_object(text: str, var: str) -> tuple[int, str] | None:
    """Offset and source of the object literal assigned to `const <var> = {`, up to the first line that closes it."""
    m = re.search(rf"const\s+{re.escape(var)}\s*=\s*\{{", text)
    if not m:
        return None
    end = text.find("\n};", m.end())
    return (m.end() - 1, text[m.end() - 1 : end + 2]) if end != -1 else None


STRING = r'"((?:[^"\\]|\\.)*)"'


def parse(text: str, var: str) -> list[dict]:
    """Payload records from one library: category, vault ID, short label and SHA-256 of the payload text."""
    found = js_object(text, var)
    if not found:
        return []
    _, src = found
    cats = [(m.start(), m.group(1)) for m in re.finditer(STRING + r"\s*:\s*\[", src)]
    rows = []
    for k, (start, cat) in enumerate(cats):
        block = src[start : cats[k + 1][0] if k + 1 < len(cats) else len(src)]
        objects = list(re.finditer(r"\{[^{}]*?\bid\s*:\s*" + STRING + r"[^{}]*\}", block, re.S))
        if objects:  # sector libraries: {id:"…", role:"…", technique:"…", text:"…"}
            for o in objects:
                body = o.group(0)
                text_m = re.search(r"\btext\s*:\s*" + STRING, body, re.S)
                tech_m = re.search(r"\btechnique\s*:\s*" + STRING, body)
                payload = text_m.group(1) if text_m else body
                rows.append({"id": o.group(1), "category": cat, "label": (tech_m.group(1) if tech_m else "")[:60], "payload": payload})
        else:  # core library: "IO-001: Label - payload text", or a bare payload string
            for n, s in enumerate(re.finditer(STRING, block[block.index("[") :]), 1):
                value = s.group(1)
                m = re.match(r"([A-Z]+(?:-[A-Z]+)*-\d+)\s*:\s*(.*)", value, re.S)
                if m:
                    label, _, payload = m.group(2).partition(" - ")
                    rows.append({"id": m.group(1), "category": cat, "label": label.strip()[:60] if payload else "", "payload": payload or label})
                else:
                    rows.append({"id": f"CORE-{k + 1:02d}-{n:03d}", "category": cat, "label": "", "payload": value})
    for r in rows:
        r["sha256"] = hashlib.sha256(r.pop("payload").encode("utf-8")).hexdigest()
    return rows


def mapping(category: str) -> tuple[list[str], list[str]]:
    key = category.lower().strip()
    if key in CATEGORY_MAP:
        return CATEGORY_MAP[key]
    for k, v in CATEGORY_MAP.items():
        if k in key:
            return v
    return [], []


def build(vault: Path) -> dict:
    items = []
    for name, (library, var) in LIBRARIES.items():
        path = vault / name
        if path.is_file():
            for r in parse(path.read_text(encoding="utf-8", errors="replace"), var):
                items.append({"library": library, **r})
    tests_by_tech = defaultdict(list)
    for rel in load_data("relationships"):
        if rel["relationship"] == "validates":
            tests_by_tech[rel["target"]].append(rel["source"])
    techniques = {t["id"]: t["name"] for t in load_data("techniques")}
    cats = defaultdict(lambda: Counter())
    for it in items:
        cats[it["category"]][it["library"]] += 1
    categories = []
    for cat, counts in sorted(cats.items(), key=lambda kv: -sum(kv[1].values())):
        owasp, techs = mapping(cat)
        techs = [t for t in techs if t in techniques]
        categories.append({"category": cat, "owasp": owasp, "techniques": techs,
                           "test_cases": sorted({tc for t in techs for tc in tests_by_tech[t]}),
                           "payloads": dict(counts), "total": sum(counts.values())})
    by_hash = Counter(it["sha256"] for it in items)
    per_tech = Counter()
    for c in categories:
        for t in c["techniques"]:
            per_tech[t] += c["total"]
    try:
        commit = subprocess.run(["git", "-C", str(vault), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except OSError:
        commit = ""
    return {
        "meta": {"source": REPO, "commit": commit, "read": datetime.now(UTC).strftime("%Y-%m-%d"),
                 "licence": "none declared", "policy": "IDs, short labels, categories and SHA-256 only; no payload text is held",
                 "mapping": "category to OWASP and LLMInjection technique is an analyst mapping (scripts/payload_vault_check.py)"},
        "summary": {"payloads": len(items), "unique_texts": len(by_hash),
                    "libraries": dict(Counter(it["library"] for it in items)),
                    "unmapped_categories": [c["category"] for c in categories if not c["techniques"]],
                    "per_technique": dict(per_tech.most_common()),
                    "techniques_without_payloads": sorted(set(techniques) - set(per_tech))},
        "categories": categories,
        "items": sorted(items, key=lambda r: (r["library"], r["id"])),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--vault", type=Path, required=True, help="a clone of crazywifi/Redteam_LLM_Injection_payloads")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    data = build(a.vault)
    s = data["summary"]
    print(f"payloads {s['payloads']} · unique texts {s['unique_texts']} · libraries {s['libraries']}")
    for c in data["categories"]:
        print(f"  {c['total']:4}  {c['category'][:34]:34}  {','.join(c['owasp']) or '-':10}  {','.join(c['techniques']) or 'UNMAPPED'}")
    print("techniques without payloads:", ", ".join(s["techniques_without_payloads"]))
    if a.write:
        OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
