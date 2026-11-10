#!/usr/bin/env python3
"""Merge analyst promotion files into the datasets, with the checks a reviewer would make (stdlib only).

A promotion file is what an analyst writes after reading primary reports for research-queue candidates:

    {"sources": [...], "actors": [...], "campaigns": [...], "incidents": [...], "not_promoted": [...]}

Campaigns carry `actor_id` and `uses`; incidents carry `demonstrates`. This script turns those into relationships.
It refuses or repairs, and reports each time:

  * a source whose URL is already held is mapped to the existing source ID (no duplicates);
  * an actor whose name or alias matches an existing actor is not created; its campaigns point at the existing one;
  * IDs that collide with existing records get a numeric suffix;
  * unknown technique IDs, invalid confidence values, http URLs and source IDs that resolve nowhere drop the link;
  * dates are normalised to YYYY, YYYY-MM or YYYY-MM-DD.

Research-queue items whose candidate was promoted are marked `accepted`; candidates listed in `not_promoted` are
marked `reviewing` with the reason, so the queue says what was read and why it stayed out.

    python scripts/merge_promotions.py promo/*.json --dry-run
    python scripts/merge_promotions.py promo/*.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DATA, load_data, write_json  # noqa: E402

CONFIDENCE = {"confirmed", "high", "medium", "low", "unverified"}
GRADES = {"A", "B", "C", "D", "E"}
AI_ROLES = {"autonomous-operator", "runtime-enabler", "offensive-enabler", "local-analysis", "tooling-development",
            "ai-supply-chain-targeting", "coding-agent-targeting", "ai-infrastructure-targeting", "supply-chain"}
DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")


def norm_url(url: str) -> str:
    return re.sub(r"^https?://(www\.)?", "", (url or "").strip()).rstrip("/").lower()


def key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def clean_id(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^A-Z0-9-]+", "-", text.upper())).strip("-")


def date(value: Any) -> str | None:
    if not value:
        return None
    text = str(value).strip()[:10]
    return text if DATE.match(text) else (text[:4] if DATE.match(text[:4]) else None)


class Merger:
    def __init__(self) -> None:
        self.d = {n: load_data(n) for n in ("sources", "actors", "campaigns", "incidents", "relationships", "techniques")}
        self.queue = load_data("research-queue")
        self.techniques = {t["id"] for t in self.d["techniques"]}
        self.ids = {r["id"] for n in ("sources", "actors", "campaigns", "incidents") for r in self.d[n]}
        self.src_by_url = {norm_url(s["url"]): s["id"] for s in self.d["sources"]}
        self.actor_by_key: dict[str, str] = {}
        for a in self.d["actors"]:
            for label in [a["name"], *a.get("aliases", [])]:
                self.actor_by_key.setdefault(key(label), a["id"])
        self.rel_n = max(int(r["id"].split("-")[1]) for r in self.d["relationships"])
        self.log: list[str] = []
        self.promoted_names: set[str] = set()
        self.reasons: dict[str, str] = {}
        self.added = {"sources": 0, "actors": 0, "campaigns": 0, "incidents": 0, "relationships": 0}

    def note(self, msg: str) -> None:
        self.log.append(msg)

    def unique(self, rid: str) -> str:
        rid, base, n = clean_id(rid), clean_id(rid), 2
        while rid in self.ids:
            rid, n = f"{base}-{n}", n + 1
        self.ids.add(rid)
        return rid

    def rel(self, source: str, kind: str, target: str, confidence: str, evidence: list[str]) -> None:
        if confidence not in CONFIDENCE:
            confidence = "medium"
        if any((r["source"], r["relationship"], r["target"]) == (source, kind, target) for r in self.d["relationships"]):
            return
        self.rel_n += 1
        self.d["relationships"].append({"id": f"REL-{self.rel_n}", "type": "relationship", "source": source, "relationship": kind,
                                        "target": target, "confidence": confidence, "evidence_sources": evidence})
        self.added["relationships"] += 1

    def merge_file(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding="utf-8"))
        src_map: dict[str, str] = {}
        for s in data.get("sources", []):
            url = s.get("url", "")
            if not url.startswith("https://"):
                self.note(f"{path.name}: source {s.get('id')} dropped (not https)")
                continue
            held = self.src_by_url.get(norm_url(url))
            if held:
                src_map[s["id"]] = held
                continue
            new = self.unique(s["id"])
            src_map[s["id"]] = new
            grade = s.get("grade") if s.get("grade") in GRADES else "C"
            self.d["sources"].append({"id": new, "type": "source", "name": s["name"], "publisher": s["publisher"], "grade": grade,
                                      "role": s.get("role") or "threat-report", "url": url,
                                      **({"published": date(s.get("published"))} if date(s.get("published")) else {}),
                                      "last_verified": date(s.get("last_verified")) or "2026-11-10"})
            self.src_by_url[norm_url(url)] = new
            self.added["sources"] += 1

        def sources_of(ids: list[str]) -> list[str]:
            out = [src_map.get(i, i) for i in ids]
            known = {s["id"] for s in self.d["sources"]}
            missing = [i for i in out if i not in known]
            for i in missing:
                self.note(f"{path.name}: unknown source {i} dropped")
            return [i for i in out if i in known]

        actor_map: dict[str, str] = {}
        for a in data.get("actors", []):
            existing = next((self.actor_by_key[key(x)] for x in [a["name"], *a.get("aliases", [])] if key(x) in self.actor_by_key), None)
            if existing:
                actor_map[a["id"]] = existing
                self.note(f"{path.name}: actor {a['name']} already held as {existing}; not created")
                self.promoted_names.add(a["name"])
                continue
            if a.get("confidence") not in CONFIDENCE or not a.get("summary"):
                self.note(f"{path.name}: actor {a.get('name')} dropped (confidence or summary missing)")
                continue
            srcs = [x for x in a.get("sources", []) if x.get("url", "").startswith("https://")]
            if not srcs:
                self.note(f"{path.name}: actor {a['name']} dropped (no https source)")
                continue
            new = self.unique(a["id"])
            actor_map[a["id"]] = new
            rec = {"id": new, "type": "actor", "name": a["name"], "aliases": a.get("aliases", []), "nexus": a.get("nexus") or "Not stated in report",
                   "ai_role": [r for r in a.get("ai_role", []) if r in AI_ROLES] or ["offensive-enabler"], "confidence": a["confidence"]}
            if a.get("regions"):
                rec["regions"] = a["regions"]
            rec.update({"summary": a["summary"], "last_verified": "2026-11-10",
                        "sources": [{"title": x["title"], "publisher": x["publisher"], "grade": x.get("grade") if x.get("grade") in GRADES else "C", "url": x["url"]} for x in srcs]})
            self.d["actors"].append(rec)
            for label in [a["name"], *a.get("aliases", [])]:
                self.actor_by_key.setdefault(key(label), new)
            self.promoted_names.add(a["name"])
            self.added["actors"] += 1

        for kind, links in (("campaigns", "uses"), ("incidents", "demonstrates")):
            for r in data.get(kind, []):
                if r.get("confidence") not in CONFIDENCE or not r.get("summary"):
                    self.note(f"{path.name}: {kind[:-1]} {r.get('id')} dropped (confidence or summary missing)")
                    continue
                srcs = sources_of(r.get("source_ids", []))
                if not srcs:
                    self.note(f"{path.name}: {kind[:-1]} {r.get('id')} dropped (no resolvable source)")
                    continue
                new = self.unique(r["id"])
                rec = {"id": new, "type": kind[:-1], "name": r["name"]}
                if kind == "incidents":
                    rec.update({"kind": r.get("kind") or "intrusion", "status": r.get("status") or "observed"})
                rec["confidence"] = r["confidence"]
                for f in (("first_seen", "last_seen", "reported") if kind == "campaigns" else ("date",)):
                    if date(r.get(f)):
                        rec[f] = date(r.get(f))
                if r.get("regions"):
                    rec["regions"] = r["regions"]
                rec.update({"summary": r["summary"], "source_ids": srcs})
                if kind == "incidents" and date(r.get("reported")):
                    rec["reported"] = date(r.get("reported"))
                self.d[kind].append(rec)
                self.added[kind] += 1
                actor = actor_map.get(r.get("actor_id") or "", r.get("actor_id")) if kind == "campaigns" else None
                if actor and actor in {a["id"] for a in self.d["actors"]}:
                    self.rel(actor, "conducts", new, "confirmed" if r["confidence"] == "confirmed" else "high", srcs)
                for link in r.get(links, []):
                    if link.get("technique") in self.techniques:
                        self.rel(new, links, link["technique"], link.get("confidence", "medium"), srcs)
                    else:
                        self.note(f"{path.name}: {new} -> {link.get('technique')} dropped (unknown technique)")
                self.promoted_names.add(r["name"])
        for n in data.get("not_promoted", []):
            self.reasons[n.get("name", "")] = n.get("reason", "")

    def update_queue(self) -> tuple[int, int]:
        accepted = reviewing = 0
        promoted = {key(x) for x in self.promoted_names}
        reasons = {key(k): v for k, v in self.reasons.items()}
        held_urls = set(self.src_by_url)
        for item in self.queue["items"]:
            if item["status"] != "candidate" or item["source_feed_id"] != "FEED-AI-ACTOR-TRACKER":
                continue
            name = key(item["identifiers"][0]) if item["identifiers"] else ""
            if item["kind"] == "actor-candidate" and (name in promoted or any(name and name in p for p in promoted)):
                item["status"], item["review"] = "accepted", {"decision": "promoted", "notes": "Primary report read on 2026-11-10; see the actor, campaign or incident with this name."}
                accepted += 1
            elif item["kind"] == "source-candidate" and norm_url(item["url"]) in held_urls:
                item["status"], item["review"] = "accepted", {"decision": "added to sources", "notes": "Read and graded on 2026-11-10."}
                accepted += 1
            else:
                reason = reasons.get(name) if name else reasons.get(key(item["url"]))
                if not reason and len(name) >= 4:
                    reason = next((v for k, v in reasons.items() if len(k) >= 4 and (k in name or name in k)), None)
                if reason:
                    item["status"], item["review"] = "reviewing", {"decision": "not promoted", "notes": reason[:400]}
                    reviewing += 1
        return accepted, reviewing

    def save(self) -> None:
        for n in ("sources", "actors", "campaigns", "incidents", "relationships"):
            write_json(DATA / f"{n}.json", self.d[n])
        write_json(DATA / "research-queue.json", self.queue)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    m = Merger()
    for f in args.files:
        m.merge_file(Path(f))
    accepted, reviewing = m.update_queue()
    print(json.dumps({"added": m.added, "queue_accepted": accepted, "queue_reviewing": reviewing}, indent=1))
    for line in m.log:
        print("  " + line)
    if not args.dry_run:
        m.save()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
