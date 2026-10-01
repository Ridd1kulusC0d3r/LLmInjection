#!/usr/bin/env python3
"""Collect metadata from allow-listed AI security sources into a human-review research queue.

This script never promotes candidates into official CTI datasets. It collects metadata,
deduplicates candidates, assigns a transparent relevance score, and preserves review state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FEEDS = ROOT / "data" / "source-feeds.json"
DEFAULT_QUEUE = ROOT / "data" / "research-queue.json"

IDENTIFIER_RE = re.compile(
    r"\b(?:CVE-\d{4}-\d{4,8}|GHSA-[0-9a-z-]{10,}|MAL-\d{4}-\d+|AML\.T\d{4}(?:\.\d{3})?|LLM\d{2}:\d{4}|ASI\d{2}:\d{4})\b",
    re.IGNORECASE,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fetch_json(url: str) -> Any:
    headers = {
        "Accept": "application/vnd.github+json, application/json",
        "User-Agent": "LLMInjection-Living-Intelligence/1.0",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2026-03-10"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return json.loads(response.read().decode(charset))


def compact(text: Any, limit: int = 1200) -> str:
    if text is None:
        return ""
    value = re.sub(r"\s+", " ", str(text)).strip()
    return value[:limit]


def matched_terms(text: str, keywords: list[str]) -> list[str]:
    text_l = text.lower()
    hits: list[str] = []
    for keyword in keywords:
        term = keyword.lower().strip()
        if not term:
            continue
        if len(term) <= 3 and term.isalnum():
            if re.search(rf"\b{re.escape(term)}\b", text_l):
                hits.append(keyword)
        elif term in text_l:
            hits.append(keyword)
    return sorted(set(hits), key=str.lower)


def identifiers(text: str) -> list[str]:
    return sorted({m.group(0).upper() for m in IDENTIFIER_RE.finditer(text)})


def relevance(feed: dict, text: str, ids: list[str]) -> tuple[int, list[str]]:
    if feed.get("relevance_mode") == "all":
        return 100, []
    hits = matched_terms(text, feed.get("keywords", []))
    if not hits:
        return 0, []
    score = 35 + min(48, len(hits) * 12) + (10 if ids else 0)
    return min(100, score), hits


def candidate_id(feed_id: str, url: str, title: str, kind: str) -> str:
    material = "|".join((feed_id, url.strip().lower(), title.strip().lower(), kind))
    return "RQ-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:16].upper()


def make_candidate(
    feed: dict,
    *,
    kind: str,
    title: str,
    url: str,
    published: str | None,
    summary: str,
    extra_text: str = "",
) -> dict | None:
    search_text = " ".join((title, summary, extra_text))
    ids = identifiers(search_text)
    score, hits = relevance(feed, search_text, ids)
    if feed.get("relevance_mode") == "keywords" and not hits:
        return None
    return {
        "id": candidate_id(feed["id"], url, title, kind),
        "status": "candidate",
        "source_feed_id": feed["id"],
        "source_grade": feed["source_grade"],
        "kind": kind,
        "title": compact(title, 300),
        "url": url,
        "published": published,
        "observed_at": utc_now(),
        "relevance_score": score,
        "matched_terms": hits,
        "summary": compact(summary),
        "identifiers": ids,
        "review": {"decision": None, "notes": None},
    }


def parse_atlas_added_items(body: str) -> list[tuple[str, str]]:
    mapping = {
        "added new techniques": "atlas-technique",
        "added new mitigations": "atlas-mitigation",
        "added new case studies": "atlas-case-study",
        "added new tactics": "atlas-tactic",
    }
    current: str | None = None
    found: list[tuple[str, str]] = []

    for raw in body.splitlines():
        line = raw.strip()
        lower = line.lower()
        if line.startswith("#"):
            current = None
            continue
        matched_header = False
        for heading, kind in mapping.items():
            if heading in lower:
                current = kind
                matched_header = True
                break
        if matched_header:
            continue
        if current and (
            "updated existing" in lower
            or "removed " in lower
            or "renamed " in lower
            or lower.startswith("assets")
        ):
            current = None
            continue
        if current and line.startswith(("* ", "- ")):
            title = line[2:].strip()
            if title and not title.lower().startswith(("added ", "updated ", "removed ")):
                found.append((current, title))
    return found


def candidates_from_feed(feed: dict, payload: Any) -> list[dict]:
    kind = feed["kind"]
    limit = int(feed.get("max_items", 100))
    out: list[dict] = []

    if kind in {"github-releases", "atlas-releases"}:
        for release in (payload or [])[:limit]:
            title = release.get("name") or release.get("tag_name") or "GitHub release"
            url = release.get("html_url") or feed["url"]
            body = release.get("body") or ""
            candidate = make_candidate(
                feed,
                kind="framework-release" if kind == "atlas-releases" else "project-release",
                title=title,
                url=url,
                published=release.get("published_at") or release.get("created_at"),
                summary=body or f"Release {title}",
            )
            if candidate:
                out.append(candidate)

            if kind == "atlas-releases":
                for item_kind, item_title in parse_atlas_added_items(body):
                    item = make_candidate(
                        feed,
                        kind=item_kind,
                        title=item_title,
                        url=url,
                        published=release.get("published_at") or release.get("created_at"),
                        summary=f"MITRE ATLAS release {title} added: {item_title}.",
                        extra_text=body[:2000],
                    )
                    if item:
                        out.append(item)

    elif kind == "github-commits":
        for commit in (payload or [])[:limit]:
            data = commit.get("commit", {})
            message = (data.get("message") or "Repository update").splitlines()[0]
            commit_date = (data.get("committer") or {}).get("date") or (data.get("author") or {}).get("date")
            candidate = make_candidate(
                feed,
                kind="canonical-repository-change",
                title=message,
                url=commit.get("html_url") or feed["url"],
                published=commit_date,
                summary=data.get("message") or message,
            )
            if candidate:
                out.append(candidate)

    elif kind == "github-advisories":
        for advisory in (payload or [])[:limit]:
            packages = []
            for vuln in advisory.get("vulnerabilities") or []:
                package = (vuln.get("package") or {}).get("name")
                ecosystem = (vuln.get("package") or {}).get("ecosystem")
                if package:
                    packages.append(f"{ecosystem or 'unknown'}:{package}")
            id_text = " ".join(
                value for value in [advisory.get("ghsa_id"), advisory.get("cve_id")] if value
            )
            title = advisory.get("summary") or id_text or "GitHub advisory"
            summary = advisory.get("description") or title
            candidate = make_candidate(
                feed,
                kind="malware-advisory" if advisory.get("type") == "malware" else "security-advisory",
                title=title,
                url=advisory.get("html_url") or feed["url"],
                published=advisory.get("published_at") or advisory.get("updated_at"),
                summary=summary,
                extra_text=" ".join(packages + [id_text]),
            )
            if candidate:
                out.append(candidate)

    elif kind == "cisa-kev":
        vulnerabilities = (payload or {}).get("vulnerabilities", [])
        for vuln in vulnerabilities[:limit]:
            title = vuln.get("vulnerabilityName") or vuln.get("cveID") or "CISA KEV entry"
            summary = vuln.get("shortDescription") or title
            extra = " ".join(
                str(vuln.get(key) or "")
                for key in ("vendorProject", "product", "requiredAction", "cveID")
            )
            candidate = make_candidate(
                feed,
                kind="known-exploited-vulnerability",
                title=title,
                url="https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                published=vuln.get("dateAdded"),
                summary=summary,
                extra_text=extra,
            )
            if candidate:
                out.append(candidate)

    else:
        raise ValueError(f"unsupported feed kind: {kind}")

    return out


def render_report(feeds: list[dict], new_items: list[dict], queue: dict, failures: list[str]) -> str:
    active = sum(1 for feed in feeds if feed.get("enabled"))
    lines = [
        "# Living Intelligence Intake",
        "",
        f"- Run: {queue['meta']['last_run']}",
        f"- Enabled feeds: **{active}**",
        f"- New candidates: **{len(new_items)}**",
        f"- Queue size: **{len(queue['items'])}**",
        f"- Feed failures: **{len(failures)}**",
        "",
        "## New candidates",
        "",
    ]
    if not new_items:
        lines.append("No new candidates were discovered.")
    else:
        for item in sorted(new_items, key=lambda value: (-value["relevance_score"], value["title"].lower()))[:50]:
            ids = ", ".join(item["identifiers"]) or "none"
            terms = ", ".join(item["matched_terms"]) or "canonical feed"
            lines.extend(
                [
                    f"### {item['title']}",
                    "",
                    f"- Queue ID: {item['id']}",
                    f"- Kind: {item['kind']}",
                    f"- Source: {item['source_feed_id']} / grade {item['source_grade']}",
                    f"- Relevance: **{item['relevance_score']}**",
                    f"- Matched terms: {terms}",
                    f"- Identifiers: {ids}",
                    f"- Published: {item['published']}",
                    f"- URL: {item['url']}",
                    "",
                    item["summary"],
                    "",
                ]
            )
    if failures:
        lines.extend(["## Feed failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")
    lines.extend(
        [
            "## Promotion policy",
            "",
            "Collection is automated. Promotion into actors, campaigns, incidents, techniques, vulnerabilities, relationships or landscape metrics requires review under docs/METHODOLOGY.md.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feeds", default=str(DEFAULT_FEEDS))
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--report", default=str(ROOT / "reports" / "intake" / "latest.md"))
    parser.add_argument("--fixture", help="JSON object keyed by feed ID; disables network fetching")
    parser.add_argument("--dry-run", action="store_true", help="Do not overwrite the queue")
    args = parser.parse_args()

    feeds_doc = load_json(Path(args.feeds))
    queue_path = Path(args.queue)
    queue = load_json(queue_path)
    fixture = load_json(Path(args.fixture)) if args.fixture else None

    existing = {item["id"]: item for item in queue.get("items", [])}
    new_items: list[dict] = []
    failures: list[str] = []

    for feed in feeds_doc.get("feeds", []):
        if not feed.get("enabled"):
            continue
        try:
            payload = fixture.get(feed["id"], []) if fixture is not None else fetch_json(feed["url"])
            for candidate in candidates_from_feed(feed, payload):
                if candidate["id"] in existing:
                    continue
                existing[candidate["id"]] = candidate
                new_items.append(candidate)
        except Exception as exc:
            failures.append(f"{feed['id']}: {type(exc).__name__}: {exc}")

    queue["meta"]["last_run"] = utc_now()
    queue["items"] = sorted(
        existing.values(),
        key=lambda item: (
            0 if item["status"] in {"candidate", "reviewing"} else 1,
            -int(item.get("relevance_score", 0)),
            str(item.get("published") or ""),
            item["id"],
        ),
    )

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(feeds_doc["feeds"], new_items, queue, failures), encoding="utf-8")

    if not args.dry_run:
        write_json(queue_path, queue)

    print(
        f"Living intelligence intake complete: feeds={len(feeds_doc['feeds'])}, "
        f"new={len(new_items)}, queue={len(queue['items'])}, failures={len(failures)}"
    )
    return 0 if not failures or fixture is not None else 2


if __name__ == "__main__":
    sys.exit(main())
