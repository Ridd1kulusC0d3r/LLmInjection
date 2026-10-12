#!/usr/bin/env python3
"""Turn the CVEs cited by Agent Threat Rules into research-queue candidates (stdlib only).

ATR (Agent-Threat-Rule/agent-threat-rules, MIT) rules cite the CVEs and GHSA advisories their patterns were written
from. Those citations are leads for LLMInjection's vulnerability dataset, nothing more: an ATR citation says a rule
author read the advisory, not that the vulnerability matters, was exploited, or belongs to an AI system.

This script lists the cited CVEs that LLMInjection does not yet hold (neither in data/vulnerabilities.json nor in the
research queue), optionally adds CISA KEV membership and FIRST EPSS from the public APIs (no key), ranks them with a
documented score and can append the top ones to data/research-queue.json as `candidate` items. Nothing is promoted
into a dataset: that stays a human decision.

    git clone --depth 1 https://github.com/Agent-Threat-Rule/agent-threat-rules.git /tmp/atr
    python scripts/atr_cve_candidates.py --atr /tmp/atr --enrich --report atr-cve.md
    python scripts/atr_cve_candidates.py --atr /tmp/atr --enrich --queue --top 25

Score (0 to 100): 20, plus 10 per citing rule up to 30, plus 30 when the CVE is in CISA KEV, plus 40 x EPSS.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DATA, load_data, write_json  # noqa: E402
from osint_ioc import enrich_cves  # noqa: E402

FEED_ID = "FEED-ATR-RULE-COMMITS"
CVE = re.compile(r"\bCVE-\d{4}-\d{4,8}\b", re.I)
GHSA = re.compile(r"\bGHSA(?:-[2-9cfghjmpqrvwx]{4}){3}\b", re.I)


def reference_sections(text: str) -> dict[str, str]:
    """The `references:` block of an ATR rule split into its two-space-indented keys (cve, ghsa, cwe, ...)."""
    block = re.search(r"^references:\n((?:[ \t]+.*\n|\n)+)", text, re.M)
    if not block:
        return {}
    sections: dict[str, list[str]] = {}
    key = ""
    for line in block.group(1).splitlines():
        m = re.match(r"^  ([a-z_]+):(.*)$", line)
        if m:
            key = m.group(1)
            sections[key] = [m.group(2)]
        elif key:
            sections[key].append(line)
    return {k: "\n".join(v) for k, v in sections.items()}


def parse_rule(text: str, category: str) -> dict[str, Any] | None:
    rid = re.search(r"^id: (ATR-[\w-]+)", text, re.M)
    if not rid:
        return None
    title = re.search(r'^title: "?(.*?)"?\s*$', text, re.M)
    status = re.search(r'^status: "?([\w-]+)"?', text, re.M)
    sections = reference_sections(text)
    return {
        "id": rid.group(1), "title": title.group(1) if title else "", "status": status.group(1) if status else "", "category": category,
        "cve": sorted({c.upper() for c in CVE.findall(sections.get("cve", ""))}),
        "ghsa": sorted({g.lower().replace("ghsa", "GHSA", 1) for g in GHSA.findall(sections.get("ghsa", "") + sections.get("external", ""))}),
    }


def collect(root: Path) -> list[dict[str, Any]]:
    rules = []
    for path in sorted((root / "rules").rglob("*.yaml")):
        rule = parse_rule(path.read_text(encoding="utf-8", errors="ignore"), path.relative_to(root / "rules").parts[0])
        if rule and (rule["cve"] or rule["ghsa"]):
            rules.append(rule)
    return rules


def known_identifiers() -> set[str]:
    """CVE and GHSA identifiers already in the vulnerability dataset or in the research queue."""
    known = {i.upper() for v in load_data("vulnerabilities") for i in v.get("identifiers", [])}
    for item in load_data("research-queue")["items"]:
        known |= {i.upper() for i in item.get("identifiers", [])}
        known |= {c.upper() for c in CVE.findall(item.get("title", ""))}
    return known


def group_by_cve(rules: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    cited: dict[str, dict[str, Any]] = defaultdict(lambda: {"rules": [], "categories": set(), "titles": [], "ghsa": set()})
    for rule in rules:
        for cve in rule["cve"]:
            row = cited[cve]
            row["rules"].append(rule["id"])
            row["categories"].add(rule["category"])
            row["titles"].append(rule["title"])
            row["ghsa"].update(rule["ghsa"])
    return cited


def enrich_chunked(cves: list[str], size: int = 40) -> dict[str, dict[str, Any]]:
    """The EPSS API fails on very long CVE lists, so ask for a few dozen at a time."""
    out: dict[str, dict[str, Any]] = {}
    for i in range(0, len(cves), size):
        out.update(enrich_cves(cves[i : i + size]))
    return out


def score(rules: int, enrichment: dict[str, Any]) -> int:
    kev = 30 if enrichment.get("in_cisa_kev") else 0
    return min(100, 20 + 10 * min(rules, 3) + kev + int(40 * enrichment.get("epss", 0.0)))


def candidates(cited: dict[str, dict[str, Any]], known: set[str], enrichment: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for cve, row in cited.items():
        if cve in known or any(g.upper() in known for g in row["ghsa"]):
            continue
        extra = enrichment.get(cve, {})
        rows.append({
            "cve": cve, "rules": sorted(row["rules"]), "categories": sorted(row["categories"]), "ghsa": sorted(row["ghsa"]),
            "atr_title": row["titles"][0], "enrichment": extra, "score": score(len(row["rules"]), extra),
        })
    return sorted(rows, key=lambda r: (-r["score"], r["cve"]))


def summary_text(row: dict[str, Any]) -> str:
    parts = [f"Cited by {len(row['rules'])} Agent Threat Rule(s) in {', '.join(row['categories'])}; first rule title: {row['atr_title']!r}."]
    e = row["enrichment"]
    if "in_cisa_kev" in e:
        parts.append("In CISA KEV." if e["in_cisa_kev"] else "Not in CISA KEV.")
    if "epss" in e:
        parts.append(f"EPSS {e['epss']:.3f}.")
    parts.append("An ATR citation is a lead, not evidence of exploitation or of an AI system.")
    return " ".join(parts)


def queue_item(row: dict[str, Any], now: str) -> dict[str, Any]:
    return {
        "id": f"RQ-ATR-{row['cve']}", "status": "candidate", "source_feed_id": FEED_ID, "source_grade": "D", "kind": "vulnerability-candidate",
        "title": f"{row['cve']} (cited by Agent Threat Rules)", "url": f"https://nvd.nist.gov/vuln/detail/{row['cve']}", "published": None,
        "observed_at": now, "relevance_score": row["score"], "matched_terms": row["categories"], "summary": summary_text(row),
        "identifiers": [row["cve"], *row["ghsa"]],
        "review": {"decision": None, "notes": "Read the NVD or vendor advisory. Add a vulnerability record only if the product is an AI framework, agent, MCP server or model tool, and link it to a technique from evidence in the advisory."},
    }


def report(rows: list[dict[str, Any]], total_cited: int, rules: int, limit: int) -> str:
    kev = sum(1 for r in rows if r["enrichment"].get("in_cisa_kev"))
    lines = [
        "# CVEs cited by Agent Threat Rules and not yet in LLMInjection", "",
        f"{rules} ATR rules cite {total_cited} distinct CVEs; {len(rows)} are not in the vulnerability dataset or the research queue ({kev} in CISA KEV).", "",
        "A citation is a lead, not evidence. Score = 20 + 10 per citing rule (max 30) + 30 if in KEV + 40 x EPSS.", "",
        "| CVE | Score | Rules | Categories | EPSS | KEV |", "|---|---|---|---|---|---|",
    ]
    for r in rows[:limit]:
        e = r["enrichment"]
        lines.append(f"| {r['cve']} | {r['score']} | {len(r['rules'])} | {', '.join(r['categories'])} | {e.get('epss', ''):} | {'yes' if e.get('in_cisa_kev') else ('no' if 'in_cisa_kev' in e else '')} |")
    return "\n".join(lines) + "\n"


def ensure_feed() -> None:
    path = DATA / "source-feeds.json"
    data = load_data("source-feeds")
    if any(f["id"] == FEED_ID for f in data["feeds"]):
        return
    data["feeds"].append({
        "id": FEED_ID, "name": "Agent Threat Rules: CVEs cited by rules (read from a clone by scripts/atr_cve_candidates.py)",
        "kind": "github-commits", "url": "https://api.github.com/repos/Agent-Threat-Rule/agent-threat-rules/commits?per_page=10",
        "source_grade": "D", "enabled": False, "max_items": 1, "relevance_mode": "all",
    })
    write_json(path, data)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--atr", required=True, help="clone of Agent-Threat-Rule/agent-threat-rules")
    ap.add_argument("--enrich", action="store_true", help="add CISA KEV and EPSS (public APIs)")
    ap.add_argument("--report", help="write a Markdown report to this path")
    ap.add_argument("--queue", action="store_true", help="append the top candidates to data/research-queue.json")
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    rules = collect(Path(args.atr))
    cited = group_by_cve(rules)
    enrichment = enrich_chunked(sorted(cited)) if args.enrich else {}
    rows = candidates(cited, known_identifiers(), enrichment)
    print(f"{len(rules)} rules cite {len(cited)} CVEs; {len(rows)} are new to LLMInjection")
    for r in rows[: args.top]:
        print(f"  {r['score']:3} {r['cve']:16} {len(r['rules'])} rule(s) {','.join(r['categories'])}")
    if args.report:
        Path(args.report).write_text(report(rows, len(cited), len(rules), len(rows)), encoding="utf-8")
    if args.queue:
        queue = load_data("research-queue")
        have = {i["id"] for i in queue["items"]}
        now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        new = [queue_item(r, now) for r in rows[: args.top] if f"RQ-ATR-{r['cve']}" not in have]
        queue["items"].extend(new)
        write_json(DATA / "research-queue.json", queue)
        ensure_feed()
        print(f"appended {len(new)} candidate(s) to data/research-queue.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
