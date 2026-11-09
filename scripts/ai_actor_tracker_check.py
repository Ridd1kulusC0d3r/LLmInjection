#!/usr/bin/env python3
"""Compare a community tracker of threat-actor use of AI with LLMInjection and queue what is missing (stdlib only).

Source: cybershujin/Threat-Actors-use-of-Artifical-Intelligence, a one-person curation of public reporting on threat
actors that use AI in their operations. It declares no licence, so nothing is copied: its descriptions and its IOC
files stay there. What this script takes are facts that point elsewhere: actor names as the reporting vendors use
them, the URLs of the reports, the reporting dates and the ATT&CK IDs the curator assigned.

From a clone it establishes:

  * which tracked actors LLMInjection already holds (by name or alias) and which it does not;
  * which report URLs are not in any LLMInjection dataset;
  * which ATT&CK IDs the tracker uses, checked against an ATT&CK release (optional), as a work list for our own mapping.

With --queue it appends `actor-candidate` and `source-candidate` items to data/research-queue.json. Nothing is
promoted into actors.json or sources.json: that needs the primary report read by an analyst.

    git clone --depth 1 https://github.com/cybershujin/Threat-Actors-use-of-Artifical-Intelligence.git /tmp/ait
    python scripts/ai_actor_tracker_check.py --tracker /tmp/ait --attack enterprise-attack.json --write
    python scripts/ai_actor_tracker_check.py --tracker /tmp/ait --queue

Actor score (0 to 100): 20, plus 30 if reported in 2026 or 15 if in 2025, plus 10 per reference up to 30, plus 20 when
at least one reference is a vendor or government publication rather than press.

Cloned content is untrusted: it is read as text and JSON and never executed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DATA, ROOT, load_data, write_json  # noqa: E402

REPO = "cybershujin/Threat-Actors-use-of-Artifical-Intelligence"
FEED_ID = "FEED-AI-ACTOR-TRACKER"
OUT = ROOT / "references" / "crosswalks" / "ai-actor-tracker.json"
STIX = "stix/threat-actors-ai-stix2.1.json"
ATTACK_ID = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")
URL = re.compile(r"https?://[^\s)<>\"\]|]+")
# Domains of vendors and governments that publish primary reporting. Anything else is treated as press or other.
PRIMARY_DOMAINS = {
    "anthropic.com", "openai.com", "microsoft.com", "blogs.microsoft.com", "cloud.google.com", "blog.google",
    "unit42.paloaltonetworks.com", "crowdstrike.com", "cisa.gov", "ic3.gov", "fbi.gov", "ncsc.gov.uk", "cert-in.org.in",
    "securelist.com", "kaspersky.com", "proofpoint.com", "trendmicro.com", "sysdig.com", "huntress.com", "sophos.com",
    "bitdefender.com", "welivesecurity.com", "eset.com", "recordedfuture.com", "group-ib.com", "zscaler.com",
    "security.com", "symantec-enterprise-blogs.security.com", "aws.amazon.com", "mandiant.com", "checkpoint.com",
    "research.checkpoint.com", "gambit.security", "sygnia.co", "hunt.io", "socradar.io", "resecurity.com", "greynoise.io",
    "slashnext.com", "abnormalsecurity.com", "intezer.com", "sentinelone.com", "volexity.com", "huggingface.co",
}


def norm_url(url: str) -> str:
    return re.sub(r"^https?://(www\.)?", "", url.strip()).rstrip("/.,)").lower()


def domain(url: str) -> str:
    return norm_url(url).split("/")[0]


def is_primary(url: str) -> bool:
    d = domain(url)
    return any(d == p or d.endswith("." + p) for p in PRIMARY_DOMAINS)


def key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def year(text: str) -> int | None:
    found = re.findall(r"20\d\d", text or "")
    return int(found[0]) if found else None


def read_tracker(root: Path) -> list[dict[str, Any]]:
    """Tracker entries joined to the references of the matching STIX intrusion-set (by name)."""
    entries = json.loads((root / "tracker.json").read_text(encoding="utf-8"))["entries"]
    refs: dict[str, list[dict[str, str]]] = {}
    stix_path = root / STIX
    if stix_path.exists():
        for obj in json.loads(stix_path.read_text(encoding="utf-8"))["objects"]:
            if obj.get("type") == "intrusion-set":
                refs[key(obj["name"])] = [{"source": r.get("source_name", ""), "url": r["url"]} for r in obj.get("external_references", []) if r.get("url")]
    out = []
    for e in entries:
        links = refs.get(key(e["name"]), [])
        out.append({
            "name": e["name"].strip(), "akas": e.get("akas", "").strip(), "table": e.get("table", ""),
            "reported": e.get("reported", "").strip(), "activity": e.get("activity", "").strip(),
            "attack_ids": sorted(set(ATTACK_ID.findall(e.get("ttp_md", "")))), "references": links,
        })
    return out


def report_urls(root: Path) -> dict[str, dict[str, str]]:
    """Every report URL the tracker cites (Sources.md and STIX reports), with a publisher label when known."""
    urls: dict[str, dict[str, str]] = {}
    sources = root / "Sources.md"
    if sources.exists():
        for u in URL.findall(sources.read_text(encoding="utf-8")):
            urls.setdefault(norm_url(u), {"url": u.rstrip(".,)"), "publisher": domain(u), "title": ""})
    stix_path = root / STIX
    if stix_path.exists():
        objs = json.loads(stix_path.read_text(encoding="utf-8"))["objects"]
        names = {o["id"]: o.get("name", "") for o in objs if o.get("type") == "identity"}
        for o in objs:
            if o.get("type") != "report":
                continue
            for r in o.get("external_references", []):
                if r.get("url"):
                    urls[norm_url(r["url"])] = {"url": r["url"], "publisher": names.get(o.get("created_by_ref", ""), r.get("source_name", "")) or domain(r["url"]),
                                                "title": o.get("name", ""), "published": o.get("published", "")[:10]}
    # the tracker's own pages are not reports, and the datasets accept https only
    return {k: v for k, v in urls.items() if not k.startswith("github.com/cybershujin") and v["url"].startswith("https://")}


def our_actor_keys() -> dict[str, str]:
    out = {}
    for a in load_data("actors"):
        for label in [a["name"], *a.get("aliases", [])]:
            out[key(label)] = a["id"]
    return out


def match_actor(entry: dict[str, Any], ours: dict[str, str]) -> tuple[str, str] | None:
    """(our actor ID, the tracker label that matched it), so a match through an alias stays visible."""
    labels = [entry["name"], *re.split(r"[,;/()]| aka ", entry["akas"])]
    for label in labels:
        k = key(label)
        if len(k) >= 4 and k in ours:
            return ours[k], label.strip()
    return None


def our_urls() -> set[str]:
    """Every URL that appears in the datasets; queues hold leads, not holdings, so they are skipped."""
    found = set()
    for path in DATA.glob("*.json"):
        if "queue" in path.name:
            continue
        found |= {norm_url(u) for u in URL.findall(path.read_text(encoding="utf-8"))}
    return found


def attack_names(bundle: Path) -> dict[str, dict[str, Any]]:
    out = {}
    for o in json.loads(bundle.read_text(encoding="utf-8"))["objects"]:
        if o.get("type") != "attack-pattern":
            continue
        ref = next((r for r in o.get("external_references", []) if r.get("source_name") == "mitre-attack"), None)
        if ref:
            out[ref["external_id"]] = {"name": o["name"], "retired": bool(o.get("revoked") or o.get("x_mitre_deprecated"))}
    return out


def score(entry: dict[str, Any]) -> int:
    y = year(entry["reported"]) or 0
    recency = 30 if y >= 2026 else 15 if y == 2025 else 0
    primary = 20 if any(is_primary(r["url"]) for r in entry["references"]) else 0
    return min(100, 20 + recency + 10 * min(len(entry["references"]), 3) + primary)


def build(entries: list[dict[str, Any]], reports: dict[str, dict[str, str]], attack: dict[str, dict[str, Any]] | None, head: dict[str, str]) -> dict[str, Any]:
    ours, have = our_actor_keys(), our_urls()
    actors = []
    for e in entries:
        hit = match_actor(e, ours)
        actors.append({**e, "llminjection_actor": hit[0] if hit else None, **({"matched_label": hit[1]} if hit else {}), "score": score(e),
                       "has_primary_reference": any(is_primary(r["url"]) for r in e["references"])})
    ids = Counter(i for e in entries for i in e["attack_ids"])
    attack_rows = [{"id": i, "entries": n, **({"attack_name": attack[i]["name"], "status": "retired" if attack[i]["retired"] else "ok"} if attack and i in attack else
                                             {"status": "unknown-id"} if attack else {})} for i, n in ids.most_common()]
    new_sources = sorted((v for k, v in reports.items() if k not in have), key=lambda v: (not is_primary(v["url"]), v["publisher"].lower(), v["url"]))
    for s in new_sources:
        s["primary"] = is_primary(s["url"])
    main = [a for a in actors if a["table"] == "main"]
    return {
        "schema_version": "1.0",
        "note": "Work list, not intelligence. A community tracker of threat-actor use of AI (no licence declared): names, report URLs, dates and ATT&CK IDs only; no description or IOC is copied. Every candidate needs its primary report read before promotion.",
        "source": {"repo": REPO, "license": "none declared", **head, "entries": len(entries)},
        "attack_release": attack and "checked" or "not checked",
        "summary": {
            "entries_main": len(main), "entries_deepfake": len(actors) - len(main),
            "already_held": sum(1 for a in actors if a["llminjection_actor"]),
            "new_main_2025_or_later": sum(1 for a in main if not a["llminjection_actor"] and (year(a["reported"]) or 0) >= 2025),
            "report_urls": len(reports), "report_urls_not_held": len(new_sources),
            "report_urls_not_held_primary": sum(1 for s in new_sources if s["primary"]),
            "attack_ids": len(ids), **({"attack_ids_unknown": sum(1 for r in attack_rows if r.get("status") == "unknown-id"),
                                        "attack_ids_retired": sum(1 for r in attack_rows if r.get("status") == "retired")} if attack else {}),
        },
        "attack_ids": attack_rows,
        "actors": sorted(actors, key=lambda a: (a["llminjection_actor"] is not None, -a["score"], a["name"].lower())),
        "sources_not_held": new_sources,
    }


def slug(text: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "-", text.upper()).strip("-")[:40] or hashlib.sha1(text.encode()).hexdigest()[:8].upper()


def actor_item(a: dict[str, Any], now: str) -> dict[str, Any]:
    ref = next((r for r in a["references"] if is_primary(r["url"])), a["references"][0] if a["references"] else None)
    parts = [f"Listed by a community tracker of threat-actor use of AI as {a['name']!r}" + (f" (also: {a['akas']})" if a["akas"] and a["akas"].lower() not in ("unknown", "unsub") else "") + "."]
    if a["reported"]:
        parts.append(f"Reported {a['reported']}.")
    parts.append(f"{len(a['references'])} reference(s), {'at least one' if a['has_primary_reference'] else 'none'} from a vendor or government.")
    if a["attack_ids"]:
        parts.append(f"Curator's ATT&CK IDs: {', '.join(a['attack_ids'][:8])}.")
    parts.append("Not verified by LLMInjection.")
    return {
        "id": f"RQ-AIT-ACTOR-{slug(a['name'])}", "status": "candidate", "source_feed_id": FEED_ID, "source_grade": "D", "kind": "actor-candidate",
        "title": f"{a['name']} (threat-actor use of AI)", "url": ref["url"] if ref else f"https://github.com/{REPO}", "published": None,
        "observed_at": now, "relevance_score": a["score"], "matched_terms": ["adversary-use-of-ai", a["table"]], "summary": " ".join(parts),
        "identifiers": [a["name"]],
        "review": {"decision": None, "notes": "Read the primary report. Promote only what it states: the vendor's label, nexus wording, the AI role (see docs/ACTORS-USING-AI.md) and confidence. Never merge with an existing actor without evidence."},
    }


def source_item(s: dict[str, Any], now: str) -> dict[str, Any]:
    return {
        "id": f"RQ-AIT-SRC-{hashlib.sha1(norm_url(s['url']).encode()).hexdigest()[:10].upper()}", "status": "candidate", "source_feed_id": FEED_ID,
        "source_grade": "D", "kind": "source-candidate", "title": s.get("title") or s["url"], "url": s["url"], "published": s.get("published") or None,
        "observed_at": now, "relevance_score": 60 if s["primary"] else 30, "matched_terms": ["adversary-use-of-ai", "primary" if s["primary"] else "press-or-other"],
        "summary": f"Report cited by a community tracker of threat-actor use of AI ({s['publisher']}). Not in any LLMInjection dataset. {'Vendor or government publication.' if s['primary'] else 'Press or other secondary publication: look for the primary report it cites.'}",
        "identifiers": [],
        "review": {"decision": None, "notes": "Read it and grade it (docs/SOURCE-GRADING.md) before adding it to data/sources.json."},
    }


def ensure_feed() -> None:
    data = load_data("source-feeds")
    if any(f["id"] == FEED_ID for f in data["feeds"]):
        return
    data["feeds"].append({
        "id": FEED_ID, "name": "Community tracker of threat-actor use of AI (read from a clone by scripts/ai_actor_tracker_check.py)",
        "kind": "github-commits", "url": f"https://api.github.com/repos/{REPO}/commits?per_page=10",
        "source_grade": "D", "enabled": False, "max_items": 1, "relevance_mode": "all",
    })
    write_json(DATA / "source-feeds.json", data)


def queue(report: dict[str, Any], min_year: int) -> int:
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    q = load_data("research-queue")
    have = {i["id"] for i in q["items"]}
    new = [actor_item(a, now) for a in report["actors"]
           if a["table"] == "main" and not a["llminjection_actor"] and (year(a["reported"]) or 0) >= min_year]
    new += [source_item(s, now) for s in report["sources_not_held"]]
    seen, added = set(have), []
    for item in new:
        if item["id"] not in seen:
            seen.add(item["id"])
            added.append(item)
    q["items"].extend(added)
    write_json(DATA / "research-queue.json", q)
    ensure_feed()
    return len(added)


def git_head(path: Path) -> dict[str, str]:
    def run(*args: str) -> str:
        return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True).stdout.strip()

    return {"commit": run("rev-parse", "HEAD"), "date": run("log", "-1", "--format=%cs")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tracker", required=True, help=f"clone of {REPO}")
    ap.add_argument("--attack", help="enterprise-attack.json from mitre-attack/attack-stix-data (optional)")
    ap.add_argument("--write", action="store_true", help=f"write {OUT.relative_to(ROOT)}")
    ap.add_argument("--queue", action="store_true", help="append actor and source candidates to data/research-queue.json")
    ap.add_argument("--min-year", type=int, default=2025, help="queue only actors reported in or after this year")
    args = ap.parse_args()
    root = Path(args.tracker)
    report = build(read_tracker(root), report_urls(root), attack_names(Path(args.attack)) if args.attack else None, git_head(root))
    if args.attack:
        collection = next((o for o in json.loads(Path(args.attack).read_text(encoding="utf-8"))["objects"] if o.get("type") == "x-mitre-collection"), {})
        report["attack_release"] = f"Enterprise ATT&CK {collection.get('x_mitre_version', '?')}"
    print(json.dumps(report["summary"], indent=1))
    if args.write:
        write_json(OUT, report)
        print(f"wrote {OUT.relative_to(ROOT)}")
    if args.queue:
        print(f"appended {queue(report, args.min_year)} candidate(s) to data/research-queue.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
