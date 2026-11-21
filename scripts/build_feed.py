#!/usr/bin/env python3
"""Publish the site's subscription feeds: Atom (feed.xml) and JSON Feed 1.1 (feed.json). Stdlib only.

Entries: every analyst report (intel, dossiers, weekly trends, monthly landscape) and the evidence records
reported in the last 60 days (incidents, campaigns, new CISA KEV entries). Feed readers and RSS-to-email
services (Buttondown, follow.it, Mailchimp RSS campaigns) read feed.xml; nothing else is needed on the site.

    python scripts/build_feed.py --out _site --reports _site/reports.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://ridd1kulusc0d3r.github.io/LLmInjection/"
TITLE = "LLMInjection · Ameaças a sistemas de IA"
SUBTITLE = "Relatórios, tendências semanais e novos registros de incidentes, campanhas e vulnerabilidades em IA, LLM e agentes."
KIND_PT = {"intel": "Relatório", "dossier": "Dossiê", "trends": "Tendências da semana", "landscape": "Threat Landscape mensal", "platform": "Relatório da plataforma"}


def _date(s: str) -> str:
    s = (s or "")[:10]
    if len(s) == 7:
        s += "-01"
    if len(s) == 4:
        s += "-01-01"
    try:
        dt.date.fromisoformat(s)
    except ValueError:
        s = dt.date.today().isoformat()
    return s + "T09:00:00-03:00"


def entries(reports: list[dict], days: int = 60) -> list[dict]:
    out = []
    for r in reports:
        if r.get("kind") in ("template", "intake") or r.get("path", "").endswith("-diff.md"):
            continue
        link = SITE + r["page"] if r.get("page") else SITE + "#tab=reports&report=" + r["path"].replace("/", "%2F")
        label = KIND_PT.get(r.get("kind"), "Relatório")
        title = r["title"] if r["title"].lower().startswith(label.lower().split()[0]) else f"{label}: {r['title']}"
        out.append({"id": SITE + r["path"], "title": title, "url": link,
                    "date": _date(r.get("date", "")), "summary": f"{KIND_PT.get(r.get('kind'), 'Relatório')} publicado no LLMInjection."
                    + (f" PDF: {SITE}{r['pdf']}" if r.get("pdf") else ""), "tags": [r.get("kind", "report")]})
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    data = {n: json.loads((ROOT / "data" / f"{n}.json").read_text(encoding="utf-8")) for n in ("incidents", "campaigns", "vulnerabilities")}
    for kind, rows in (("incidente", data["incidents"]), ("campanha", data["campaigns"])):
        for r in rows:
            w = str(r.get("reported") or r.get("date") or r.get("first_seen") or "")
            if w[:10] >= since[: len(w[:10])] and w.startswith("20"):
                out.append({"id": SITE + "#node=" + r["id"], "title": f"Novo {kind}: {r['name']}", "url": SITE + "#node=" + r["id"],
                            "date": _date(w), "summary": r.get("summary", ""), "tags": [kind, r.get("confidence", "")]})
    for v in data["vulnerabilities"]:
        if v.get("kev_added", "") >= since:
            out.append({"id": SITE + "#node=" + v["id"] + "#kev", "title": f"CISA KEV: {v['identifiers'][0]} · {v['package']}",
                        "url": SITE + "#node=" + v["id"], "date": _date(v["kev_added"]), "summary": v.get("summary", ""), "tags": ["kev", v.get("severity", "")]})
    out.sort(key=lambda e: e["date"], reverse=True)
    return out[:60]


def atom(items: list[dict]) -> str:
    updated = items[0]["date"] if items else _date("")
    parts = ['<?xml version="1.0" encoding="utf-8"?>', '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="pt-BR">',
             f"<title>{escape(TITLE)}</title>", f"<subtitle>{escape(SUBTITLE)}</subtitle>",
             f'<link href="{SITE}feed.xml" rel="self" type="application/atom+xml"/>', f'<link href="{SITE}"/>',
             f"<id>{SITE}</id>", f"<updated>{updated}</updated>", "<author><name>LLMInjection</name></author>"]
    for e in items:
        parts.append("<entry>" + f"<title>{escape(e['title'])}</title>" + f'<link href="{escape(e["url"])}"/>' + f"<id>{escape(e['id'])}</id>"
                     + f"<updated>{e['date']}</updated>" + f"<summary>{escape(e['summary'][:600])}</summary>"
                     + "".join(f'<category term="{escape(t)}"/>' for t in e["tags"] if t) + "</entry>")
    parts.append("</feed>")
    return "\n".join(parts) + "\n"


def jsonfeed(items: list[dict]) -> str:
    return json.dumps({"version": "https://jsonfeed.org/version/1.1", "title": TITLE, "description": SUBTITLE, "home_page_url": SITE,
                       "feed_url": SITE + "feed.json", "language": "pt-BR",
                       "items": [{"id": e["id"], "url": e["url"], "title": e["title"], "summary": e["summary"][:600],
                                  "date_published": e["date"], "tags": [t for t in e["tags"] if t]} for e in items]}, ensure_ascii=False, indent=1)


def build(out: Path, reports: list[dict]) -> int:
    items = entries(reports)
    (out / "feed.xml").write_text(atom(items), encoding="utf-8")
    (out / "feed.json").write_text(jsonfeed(items), encoding="utf-8")
    return len(items)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--reports", type=Path, required=True)
    a = ap.parse_args()
    n = build(a.out, json.loads(a.reports.read_text(encoding="utf-8"))["reports"])
    print(f"feed: {n} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
