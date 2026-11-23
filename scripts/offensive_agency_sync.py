#!/usr/bin/env python3
"""Daily snapshot of offensive.agency, the passive tracker of offensive AI agents exposed on the Internet (stdlib only).

offensive.agency (data by ONYPHE, categories ctiscan and ctiurl) fingerprints the web consoles of 11 offensive AI
agents (ARTEX, CyberStrikeAI, PentAGI, Cairn, RedAmon, Strix, CyberStrike, Xalgorix, BugTraceAI, HexStrike AI,
Pentest-Swarm-AI) and publishes, once a day, which IPs answer, on which hoster, with which domains and what else runs
on the same box. The tracker is passive: it reads ONYPHE data and never connects to a listed host. Neither does this
script: it only reads the tracker's public exports.

What lands in the repository is the aggregate, not the IP list:

  data/exposure/offensive-agency.json          latest snapshot: totals, per agent (mapped to TOOL-* records),
                                               countries (Brazil and Latin America in full), network type, C2
                                               frameworks seen on the same IP, agents sharing an IP, clusters, series
  data/exposure/offensive-agency-history.csv   one row per agent per collection day, so the trend survives the
                                               tracker's own 30-day window
  docs/EXPOSURE-OFFENSIVE-AGENCY.md            the same snapshot as a readable page, with method and limits

The IP and domain lists stay at the source, which refreshes them daily and carries the caveats (CDN fronts, cloud IPs
that change owner, researchers and students among the operators). `--export DIR` downloads them for a SIEM or
blocklist, with CDN-front IPs split out because blocking those would hit unrelated sites.

    python scripts/offensive_agency_sync.py                 # refresh the snapshot (keeps the old one on failure)
    python scripts/offensive_agency_sync.py --strict        # fail instead of keeping the old snapshot
    python scripts/offensive_agency_sync.py --export /tmp/oa  # also write ips/domains for detection

Everything read from the tracker is treated as untrusted data: numbers are coerced, strings are length-capped, agent
slugs must match a fixed pattern, and nothing is rendered as HTML.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://offensive.agency"
OUT = ROOT / "data" / "exposure" / "offensive-agency.json"
HISTORY = ROOT / "data" / "exposure" / "offensive-agency-history.csv"
DOC = ROOT / "docs" / "EXPOSURE-OFFENSIVE-AGENCY.md"
SOURCE_ID = "SRC-OFFENSIVE-AGENCY-TRACKER"
UA = "LLmInjection-exposure-sync/1.0 (+https://github.com/Ridd1kulusC0d3r/LLmInjection)"

# Tracker slug -> tool record in data/tools.json (None: the agent has no record in the graph yet).
TOOLS = {
    "artex": "TOOL-ARTEX", "cyberstrikeai": "TOOL-CYBERSTRIKEAI", "pentagi": "TOOL-PENTAGI", "cairn": "TOOL-CAIRN",
    "strix": "TOOL-STRIX", "hexstrike": "TOOL-HEXSTRIKE-AI", "redamon": None, "cyberstrike": None, "xalgorix": None,
    "bugtraceai": None, "pentestswarm": None,
}
CLUSTERS = {"antifox": "TOOL-ANTIFOX", "bob-research-labs": None}
LATAM = {"AR", "BO", "BR", "CL", "CO", "CR", "CU", "DO", "EC", "GT", "HN", "MX", "NI", "PA", "PE", "PY", "SV", "UY", "VE"}
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,40}$")
DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EXPORTS = {name: f"{BASE}/api/{name}" for name in ("ips.txt", "domains.txt", "hosts.csv", "hosts.json", "stats.json")}


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json, text/plain, */*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 (fixed https host)
        return r.read()


def _int(v: Any) -> int:
    try:
        return max(0, int(v))
    except (TypeError, ValueError):
        return 0


def _str(v: Any, n: int = 120) -> str:
    return re.sub(r"[\x00-\x1f<>]", "", str(v or ""))[:n]


def _pairs(v: Any, n: int = 40) -> list[list]:
    return [[_str(a), _int(b)] for a, b in (x for x in (v or []) if isinstance(x, (list, tuple)) and len(x) == 2)][:n]


FP = re.compile(r'\b([a-z][a-z0-9_.]{2,40}):("[^"<>]{1,120}"|[0-9a-f]{32})')
REPO_LINK = re.compile(r'href="(https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/?"')


def parse_agent_page(page: str) -> dict:
    """Pull the ONYPHE fingerprint queries and the project link from an agent page (text only, nothing rendered)."""
    text = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style|svg)\b.*?</\1>", "", page, flags=re.S))
    text = text.replace("&#34;", '"').replace("&quot;", '"').replace("&amp;", "&")
    seg = text.split("How it is detected", 1)[-1].split("Hosts", 1)[0] if "How it is detected" in text else ""
    fps = list(dict.fromkeys(f"{k}:{v}" for k, v in FP.findall(seg) if not k.startswith("category")))[:20]
    repo = next(iter(REPO_LINK.findall(page)), "")
    return {"fingerprints": fps, "project": repo}


def summarise(stats: dict, hosts: list[dict], fetched_at: str, pages: dict[str, str] | None = None) -> dict:
    """Turn the tracker's stats.json and hosts.json (and, if given, its agent pages) into the repository snapshot."""
    pages = pages or {}
    days = [d for d in stats.get("days", []) if isinstance(d, str) and DAY.match(d)]
    agents = []
    for slug, a in sorted((stats.get("tools") or {}).items(), key=lambda kv: -_int(kv[1].get("active"))):
        if not SLUG.match(slug) or not isinstance(a, dict):
            continue
        series = [_int(x) for x in (stats.get("series") or {}).get(slug, [])][-len(days):] if days else []
        ports = _pairs(a.get("ports"), 5)
        agents.append({
            "slug": slug, "name": _str(a.get("name") or slug, 60), "tool_id": TOOLS.get(slug),
            "active": _int(a.get("active")), "confirmed": _int(a.get("confirmed")),
            "probable": max(0, _int(a.get("active")) - _int(a.get("confirmed"))), "new": _int(a.get("new")),
            "all_time": _int(a.get("total")), "main_port": ports[0][0] if ports else "", "ports": ports,
            "countries": _pairs(a.get("countries"), 10), "hosters": _pairs(a.get("orgs"), 5), "series": series,
            "tracker_url": f"{BASE}/agent/{slug}", **parse_agent_page(pages.get(slug, "")),
        })
    # The country table in stats.json stops at 15; hosts.json (active hosts) gives the long tail, Latin America included.
    countries: dict[str, int] = {}
    per_agent_latam: dict[str, dict[str, int]] = {}
    cdn_ips = 0
    for h in hosts:
        if not isinstance(h, dict):
            continue
        c = _str(h.get("country"), 2).upper()
        countries[c] = countries.get(c, 0) + 1
        cdn_ips += h.get("kind") == "cdn"
        if c in LATAM:
            for slug in (h.get("tools") or {}):
                if SLUG.match(str(slug)):
                    per_agent_latam.setdefault(c, {}).setdefault(slug, 0)
                    per_agent_latam[c][slug] += 1
    latam = sorted(((c, n) for c, n in countries.items() if c in LATAM), key=lambda x: -x[1])
    return {
        "meta": {
            "source_id": SOURCE_ID, "tracker": BASE, "data_by": "ONYPHE (category:ctiscan for IPs, category:ctiurl for domains)",
            "method": "Passive. The tracker reads ONYPHE scan data and never connects to a listed host; this repository only reads "
                      "the tracker's public exports. Two independent fingerprint families on one IP make it confirmed, one makes "
                      "it probable. Honeypots and IPs answering on 150 ports or more are dropped. Active = seen in the last 7 days.",
            "caveat": "A listed IP runs an exposed instance; that says nothing about who runs it or why (researchers, students, "
                      "penetration testers and attackers all appear). A CDN-front IP is shared by unrelated sites: search the "
                      "domain instead. A cloud IP can change owner within minutes: compare log dates with first and last seen. "
                      "Counts are IPs, not machines. Clusters are a shared build detail, not an attribution.",
            "ref_day": _str(stats.get("ref_day"), 10), "active_since": _str(stats.get("active_since"), 10),
            "fetched_at": fetched_at, "exports": EXPORTS,
        },
        "totals": {
            "active_ips": _int(stats.get("active")), "all_time_ips": _int(stats.get("total")), "new_ips": _int(stats.get("new")),
            "multi_agent_ips": _int(stats.get("multi")), "ips_with_c2": _int(stats.get("with_c2")),
            "domains": _int(stats.get("domains")), "domains_behind_cdn": _int(stats.get("domains_cdn")),
            "network": {k: _int(v) for k, v in (stats.get("kinds") or {}).items() if SLUG.match(str(k))},
            "cdn_front_ips_in_hosts": cdn_ips, "agents": len(agents),
        },
        "agents": agents,
        "countries": sorted(([c, n] for c, n in countries.items() if c), key=lambda x: -x[1])[:40] or _pairs(stats.get("countries")),
        "latam": {"total": sum(n for _, n in latam), "countries": [[c, n] for c, n in latam],
                  "by_agent": {c: dict(sorted(v.items(), key=lambda kv: -kv[1])) for c, v in sorted(per_agent_latam.items())}},
        "hosters": _pairs(stats.get("orgs"), 15),
        "c2_same_ip": _pairs(stats.get("c2"), 20),
        "agent_pairs": _pairs(stats.get("pairs"), 15),
        "clusters": [{"slug": k, "hosts": _int(v), "tool_id": CLUSTERS.get(k), "tracker_url": f"{BASE}/cluster/{k}"}
                     for k, v in sorted((stats.get("clusters") or {}).items()) if SLUG.match(str(k))],
        "days": days,
    }


def append_history(snap: dict, path: Path = HISTORY) -> int:
    """Add one row per agent for the snapshot's day; a day already present is replaced, not duplicated."""
    day = snap["meta"]["ref_day"]
    rows = []
    if path.exists():
        rows = [r for r in csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))) if r["day"] != day]
    rows += [{"day": day, "agent": a["slug"], "active": a["active"], "confirmed": a["confirmed"], "new": a["new"],
              "all_time": a["all_time"]} for a in snap["agents"]]
    rows.sort(key=lambda r: (r["day"], r["agent"]))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["day", "agent", "active", "confirmed", "new", "all_time"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")
    return len(rows)


def render_doc(snap: dict) -> str:
    m, t = snap["meta"], snap["totals"]
    n = lambda x: f"{x:,}".replace(",", ".")  # noqa: E731
    lines = [
        "# Agentes ofensivos de IA expostos na Internet (offensive.agency)", "",
        f"> Gerado por `scripts/offensive_agency_sync.py` a partir do [offensive.agency]({m['tracker']}) "
        f"(dados da ONYPHE). Dia de referência **{m['ref_day']}**, janela ativa desde {m['active_since']}. "
        "Atualizado todo dia pelo workflow `exposure-daily.yml`.", "",
        "## Resumo", "",
        f"- **{n(t['active_ips'])} IPs ativos** (vistos nos últimos 7 dias), {n(t['all_time_ips'])} no histórico do rastreador; "
        f"{n(t['new_ips'])} novos na janela.",
        f"- **{n(t['multi_agent_ips'])} IPs rodam mais de um agente**; **{n(t['ips_with_c2'])} também hospedam um C2**.",
        f"- Rede: {', '.join(f'{k} {n(v)}' for k, v in sorted(t['network'].items(), key=lambda kv: -kv[1]))}. "
        f"{n(t['domains'])} domínios, {n(t['domains_behind_cdn'])} atrás de CDN.",
        f"- Brasil e América Latina: **{n(snap['latam']['total'])} IPs** "
        f"({', '.join(f'{c} {v}' for c, v in snap['latam']['countries']) or 'nenhum'}).", "",
        "## Por agente", "",
        "| Agente | Registro no grafo | Ativos | Confirmados | Novos | Histórico | Porta mais vista |",
        "|---|---|--:|--:|--:|--:|--:|",
    ]
    for a in snap["agents"]:
        lines.append(f"| [{a['name']}]({a['tracker_url']}) | {('`' + a['tool_id'] + '`') if a['tool_id'] else 'sem registro'} | "
                     f"{n(a['active'])} | {n(a['confirmed'])} | {n(a['new'])} | {n(a['all_time'])} | {a['main_port']} |")
    lines += ["", "## Como cada agente é reconhecido (consultas ONYPHE publicadas pelo rastreador)", "",
              "Servem para caçar o console no seu próprio perímetro ou numa varredura autorizada: título da página, hash MD5 do "
              "favicon, texto da resposta. Indicadores da mesma família não são independentes.", ""]
    for a in snap["agents"]:
        proj = f" · projeto: <{a['project']}>" if a.get("project") else ""
        lines.append(f"- **{a['name']}**{proj}")
        lines += [f"  - `{f}`" for f in a.get("fingerprints", [])] or ["  - (sem consulta publicada)"]
    lines += ["", "## C2 no mesmo IP", "", "| Framework | IPs |", "|---|--:|"]
    lines += [f"| {k} | {v} |" for k, v in snap["c2_same_ip"]]
    lines += ["", "## Agentes no mesmo IP", "", "| Par | IPs |", "|---|--:|"]
    lines += [f"| {k} | {v} |" for k, v in snap["agent_pairs"]]
    lines += ["", "## Clusters (detalhe de build compartilhado, não atribuição)", "", "| Cluster | Hosts | Registro |", "|---|--:|---|"]
    lines += [f"| [{c['slug']}]({c['tracker_url']}) | {c['hosts']} | {('`' + c['tool_id'] + '`') if c['tool_id'] else '–'} |"
              for c in snap["clusters"]]
    lines += ["", "## Países", "", "| País | IPs |", "|---|--:|"] + [f"| {c} | {v} |" for c, v in snap["countries"][:20]]
    lines += ["", "## Como usar na detecção", "",
              "As listas ficam na fonte, que as refaz todo dia. Baixe com "
              "`python scripts/offensive_agency_sync.py --export <pasta>`, que separa os IPs de frente de CDN:", ""]
    lines += [f"- `{k}`: <{v}>" for k, v in m["exports"].items()]
    lines += ["", "Parâmetros aceitos pela API do rastreador: `tool` (slug do agente), `scope=all`, `country`, `level`, "
              "`kind` (hosting, cloud, cdn), `domain=1`, `c2=1`, `multi=1`.", "",
              "## Método e limites", "", m["method"], "", m["caveat"], "",
              "Só a página inicial das portas varridas é visível: um agente em porta não varrida, ou que só responde num caminho "
              "de API, fica de fora. O histórico do rastreador começa em 2026-10-21; o deste repositório, no arquivo "
              "`data/exposure/offensive-agency-history.csv`.", "",
              "## Referências", "",
              f"- offensive.agency, rastreador passivo de agentes ofensivos de IA expostos: <{m['tracker']}> (método em <{m['tracker']}/about>).",
              "- ONYPHE, dados de varredura da Internet (ctiscan, ctiurl): <https://www.onyphe.io/>.",
              f"- Registro de fonte: `{m['source_id']}` em `data/sources.json`.", ""]
    return "\n".join(lines)


def export(dest: Path) -> dict[str, int]:
    """Download the tracker's lists for local detection; CDN-front IPs go to a separate file."""
    dest.mkdir(parents=True, exist_ok=True)
    hosts = json.loads(fetch(EXPORTS["hosts.json"]))
    direct = sorted({h["ip"] for h in hosts if h.get("kind") != "cdn" and isinstance(h.get("ip"), str)})
    cdn = sorted({h["ip"] for h in hosts if h.get("kind") == "cdn" and isinstance(h.get("ip"), str)})
    (dest / "ips-direct.txt").write_text("\n".join(direct) + "\n", encoding="utf-8")
    (dest / "ips-cdn-front-do-not-block.txt").write_text("\n".join(cdn) + "\n", encoding="utf-8")
    (dest / "domains.txt").write_bytes(fetch(EXPORTS["domains.txt"]))
    (dest / "hosts.csv").write_bytes(fetch(EXPORTS["hosts.csv"]))
    return {"ips_direct": len(direct), "ips_cdn_front": len(cdn)}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true", help="exit 1 if the tracker cannot be read")
    ap.add_argument("--export", type=Path, help="also download IP and domain lists into this folder")
    ap.add_argument("--stats", type=Path, help="read stats.json from a file instead of the network")
    ap.add_argument("--hosts", type=Path, help="read hosts.json from a file instead of the network")
    ap.add_argument("--pages", type=Path, help="read agent-<slug>.html pages from this folder instead of the network")
    args = ap.parse_args(argv)
    try:
        stats = json.loads(args.stats.read_bytes() if args.stats else fetch(EXPORTS["stats.json"]))
        hosts = json.loads(args.hosts.read_bytes() if args.hosts else fetch(EXPORTS["hosts.json"]))
        if not isinstance(stats, dict) or not isinstance(hosts, list) or not stats.get("tools"):
            raise ValueError("unexpected export layout")
    except Exception as e:  # noqa: BLE001 (network or layout: keep the previous snapshot)
        print(f"offensive.agency unavailable ({e}); keeping {OUT.relative_to(ROOT)}", file=sys.stderr)
        return 1 if args.strict else 0
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    known = {a["slug"]: a for a in old.get("agents", [])}
    pages: dict[str, str] = {}
    for slug in stats["tools"]:
        if not SLUG.match(slug):
            continue
        try:
            pages[slug] = (args.pages / f"agent-{slug}.html").read_text(encoding="utf-8") if args.pages else \
                fetch(f"{BASE}/agent/{slug}", 30).decode("utf-8", "replace")
        except Exception:  # noqa: BLE001 (an agent page is optional: fingerprints fall back to the last snapshot)
            pages[slug] = ""
    snap = summarise(stats, hosts, datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"), pages)
    for a in snap["agents"]:
        prev = known.get(a["slug"], {})
        a["fingerprints"] = a["fingerprints"] or prev.get("fingerprints", [])
        a["project"] = a["project"] or prev.get("project", "")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if old.get("meta", {}).get("ref_day") == snap["meta"]["ref_day"] and {k: v for k, v in old.items() if k != "meta"} == \
            {k: v for k, v in snap.items() if k != "meta"}:
        snap["meta"]["fetched_at"] = old["meta"]["fetched_at"]  # nothing new: no diff, no commit
    OUT.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = append_history(snap)
    DOC.write_text(render_doc(snap), encoding="utf-8")
    print(f"offensive.agency {snap['meta']['ref_day']}: {snap['totals']['active_ips']} active IPs, "
          f"{len(snap['agents'])} agents, history {rows} rows")
    if args.export:
        print("export:", export(args.export))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
