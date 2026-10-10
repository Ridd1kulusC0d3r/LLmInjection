#!/usr/bin/env python3
"""Discover bounded metadata from allow-listed AI threat sources for human review."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "ai-source-registry.json"
QUEUE = ROOT / "data" / "enrichment-review-queue.json"
HOSTS = {"api.github.com", "raw.githubusercontent.com",
         "registry.modelcontextprotocol.io", "api.osv.dev"}
ID_RE = re.compile(r"^(CVE-\d{4}-\d{4,}|GHSA-[a-z0-9-]{10,})$", re.I)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def checked_url(url):
    parts = urllib.parse.urlsplit(url)
    if (parts.scheme != "https" or parts.hostname not in HOSTS
            or parts.username or parts.password or parts.port not in (None, 443)):
        raise ValueError("non-allow-listed intelligence endpoint")
    return url


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        checked_url(newurl)
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def fetch(url):
    checked_url(url)
    headers = {"User-Agent": "LLMInjection-Enrichment/1.0", "Accept": "application/json"}
    if os.environ.get("GITHUB_TOKEN") and urllib.parse.urlsplit(url).hostname == "api.github.com":
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    client = urllib.request.build_opener(SafeRedirect())
    with client.open(urllib.request.Request(url, headers=headers), timeout=20) as result:
        checked_url(result.geturl())
        if int(result.headers.get("Content-Length", "0")) > 8_000_000:
            raise ValueError("oversized feed response")
        raw = result.read(8_000_001)
        if len(raw) > 8_000_000:
            raise ValueError("oversized feed response")
        return json.loads(raw.decode("utf-8"))


def short(value, limit=280):
    return " ".join(str(value or "").split())[:limit]


def candidates_from(source, data, limit, known_vulns=(), fetcher=fetch):
    adapter = source["adapter"]
    if adapter == "avid-list":
        files = sorted((r for r in data if r.get("type") == "file"
                        and r.get("name", "").endswith(".json")),
                       key=lambda r: r.get("name", ""), reverse=True)
        for record in files[:limit]:
            yield {"key": record["path"], "title": record["name"],
                   "url": record["html_url"], "kind": "report-discovery",
                   "summary": "AVID research record; content and real-world status unverified."}
    elif adapter == "veris-json":
        for record in data.get("incidents", [])[:limit]:
            key = str(record.get("id", ""))
            if not key:
                continue
            yield {"key": key, "title": short(record.get("title") or key),
                   "url": "https://github.com/DavidFarago/ai_security_incidents_2026/blob/main/incidents/all_2026_ai_software_security_incidents.json",
                   "kind": "secondary-incident-discovery",
                   "summary": "Secondary VERIS compilation; validate original report, dates and rights."}
    elif adapter == "mcp-list":
        for record in data.get("servers", [])[:limit]:
            server = record.get("server", record)
            key = str(server.get("name", "")).strip()
            if not key:
                continue
            repo = server.get("repository") or {}
            url = repo.get("url", "") if isinstance(repo, dict) else ""
            if not isinstance(url, str) or not url.startswith("https://"):
                url = "https://registry.modelcontextprotocol.io/"
            yield {"key": key, "title": short(key), "url": url,
                   "kind": "mcp-inventory", "summary": "Registry listing, not a security approval."}
    elif adapter == "git-commits":
        for record in data[:limit]:
            sha = str(record.get("sha", ""))
            if not re.fullmatch("[0-9a-f]{40}", sha):
                continue
            yield {"key": sha,
                   "title": short(record.get("commit", {}).get("message", "").split("\n")[0]),
                   "url": record["html_url"], "kind": "repository-change",
                   "summary": "Upstream commit only; not evidence of an AI incident."}
    elif adapter == "osv-local":
        seen = set()
        for item in known_vulns:
            for identifier in item.get("identifiers", []):
                if len(seen) >= limit:
                    return
                if not ID_RE.fullmatch(identifier) or identifier in seen:
                    continue
                seen.add(identifier)
                try:
                    value = data.get(identifier) if isinstance(data, dict) else None
                    if value is None:
                        value = fetcher(checked_url(
                            "https://api.osv.dev/v1/vulns/"
                            + urllib.parse.quote(identifier, safe="-")))
                except (urllib.error.URLError, ValueError, KeyError, json.JSONDecodeError):
                    continue
                if not isinstance(value, dict) or not value.get("id"):
                    continue
                record_id = str(value["id"])
                yield {"key": record_id, "title": short(value.get("summary") or identifier),
                       "url": "https://osv.dev/vulnerability/" + urllib.parse.quote(record_id, safe="-"),
                       "kind": "vulnerability-enrichment",
                       "summary": "Enrichment for already tracked identifier: " + identifier,
                       "identifiers": [identifier, record_id]}
    else:
        raise ValueError("unsupported source adapter: " + adapter)


def candidate(source, item, timestamp):
    identity = (source["id"] + "|" + str(item["key"])).encode("utf-8")
    content = json.dumps(item, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return {"id": "RQ-AI-" + hashlib.sha256(identity).hexdigest()[:16].upper(),
            "status": "candidate", "source_feed_id": source["id"],
            "source_grade": source["source_grade"], "kind": item["kind"],
            "external_id": item["key"], "title": short(item["title"]),
            "url": item["url"], "summary": short(item["summary"], 450),
            "identifiers": item.get("identifiers", []),
            "evidence_sha256": hashlib.sha256(content).hexdigest(),
            "observed_at": timestamp, "review": {"decision": None, "notes": None}}


def merge(existing, incoming):
    index = {entry["id"]: entry for entry in existing["items"]}
    added = changed = 0
    for item in incoming:
        old = index.get(item["id"])
        if old is None:
            index[item["id"]] = item
            added += 1
        elif item["evidence_sha256"] != old["evidence_sha256"]:
            item["status"] = old.get("status", "candidate")
            item["review"] = old.get("review", item["review"])
            item["observed_at"] = old.get("observed_at", item["observed_at"])
            index[item["id"]] = item
            changed += 1
    return {**existing, "items": sorted(index.values(), key=lambda r: r["id"])}, added, changed


def collect(sources, *, fixtures=None, limit=20, known_vulns=(), fetcher=fetch):
    now = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    found, errors = [], []
    for source in sources:
        if not source.get("enabled"):
            continue
        try:
            if source["adapter"] == "osv-local":
                data = fixtures.get(source["id"], {}) if fixtures is not None else {}
            else:
                data = fixtures[source["id"]] if fixtures is not None else fetcher(
                    checked_url(source["url"]))
            def offline(url):
                raise KeyError("not in offline fixtures")
            reader = offline if fixtures is not None else fetcher
            for item in candidates_from(source, data, limit, known_vulns, fetcher=reader):
                if item["url"].startswith("https://"):
                    found.append(candidate(source, item, now))
        except (KeyError, ValueError, TypeError, urllib.error.URLError, json.JSONDecodeError) as exc:
            errors.append({"source": source["id"], "error": short(exc, 200)})
    return found, errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max-per-source", type=int, default=20)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--queue", type=Path, default=QUEUE)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--summary-json", type=Path)
    args = parser.parse_args(argv)
    if not args.live and args.fixture is None:
        parser.error("explicitly choose --live or --fixture")
    if not 1 <= args.max_per_source <= 50:
        parser.error("--max-per-source must be 1..50")
    registry = load(args.registry)
    fixture = load(args.fixture) if args.fixture else None
    vulns = load(ROOT / "data" / "vulnerabilities.json")
    found, errors = collect(registry["sources"], fixtures=fixture,
                            limit=args.max_per_source, known_vulns=vulns)
    queue = load(args.queue) if args.queue.exists() else {"meta": {}, "items": []}
    result, additions, changes = merge(queue, found)
    if (additions or changes) and not args.dry_run:
        result["meta"]["last_run"] = datetime.now(UTC).isoformat()
        dump(args.queue, result)
    summary = {"candidate_count": len(found), "new_count": additions,
               "updated_count": changes, "failure_count": len(errors),
               "errors": errors, "promoted_count": 0}
    if args.summary_json:
        dump(args.summary_json, summary)
    if args.report:
        lines = ["# AI source discovery report", "", "Review only: no official CTI promotion.",
                 "", "New: " + str(additions), "Updated: " + str(changes),
                 "Failed: " + str(len(errors))]
        lines.extend("- " + e["source"] + ": " + e["error"] for e in errors)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
