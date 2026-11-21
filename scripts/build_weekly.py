#!/usr/bin/env python3
"""Draft the weekly trends report (Tendências da semana) from the datasets and the week's daily digests. Stdlib only.

The draft holds everything that can be counted: the week's numbers, every signal with its source and seal,
the techniques that moved, new KEV entries and a short LinkedIn version. The analytic parts (the thesis, the
counterpoint, the defender's Monday, Camada 8) are marked for the analyst or the scheduled task to write from
the signals, never from memory. Window: the seven days ending on --end (default: yesterday).

    python scripts/build_weekly.py                    # week ending yesterday
    python scripts/build_weekly.py --end 2026-11-20   # explicit window
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "trends"
SITE = "https://ridd1kulusc0d3r.github.io/LLmInjection/"
CONF = {"confirmed": "confirmada", "high": "alta", "medium": "média", "low": "baixa", "unverified": "não verificada"}
SEAL = {"original": "lido no original", "secondary": "secundária", "unconfirmed": "não confirmado"}
SKIP_KINDS = {"atlas-exercise", "research-artifact", "research-framework", "defensive-research", "observed-research-case"}
TODO = "<!-- A PREENCHER: escrever a partir dos sinais acima, sem fato novo que não esteja numa fonte listada -->"


def data(name: str):
    return json.loads((ROOT / "data" / f"{name}.json").read_text(encoding="utf-8"))


def cell(s: str) -> str:
    return str(s or "").replace("|", "/").replace("\n", " ").strip()


def in_window(w: str, start: str, end: str) -> bool:
    w = (w or "")[:10]
    return len(w) == 10 and start <= w <= end


def draft(end: dt.date) -> tuple[Path, str]:
    start = end - dt.timedelta(days=6)
    year, week, _ = end.isocalendar()
    tag = f"{year}-W{week:02d}"
    s, e = start.isoformat(), end.isoformat()
    inc, cam, vul, rel = data("incidents"), data("campaigns"), data("vulnerabilities"), data("relationships")
    src = {x["id"]: x for x in data("sources")}
    tech = {t["id"]: t["name"] for t in data("techniques")}
    tools = {t["id"]: t["name"] for t in data("tools")}

    def best(r):
        ss = sorted((src[i] for i in r.get("source_ids", []) if i in src and src[i].get("url", "").startswith("https://")), key=lambda x: x.get("grade", "Z"))
        return (f"[{cell(ss[0].get('publisher') or ss[0]['name'])}]({ss[0]['url']})", ss[0].get("grade", "")) if ss else ("—", "")

    signals = []
    for kind, rows in (("incidente", inc), ("campanha", cam)):
        for r in rows:
            w = str(r.get("reported") or r.get("date") or r.get("first_seen") or "")
            if in_window(w, s, e) and r.get("kind") not in SKIP_KINDS:
                link, g = best(r)
                signals.append((w[:10], kind, r["name"], link, f"`{r['id']}`", f"registro do repositório · {CONF.get(r.get('confidence'), '')}", r["id"], g))
    for v in vul:
        if in_window(v.get("kev_added", ""), s, e):
            link, g = best(v)
            signals.append((v["kev_added"], "KEV", f"{v['identifiers'][0]} · {v['package']}: {v['name']}", link, f"`{v['id']}`", "catálogo CISA KEV", v["id"], g))
        elif in_window(v.get("published", ""), s, e):
            link, g = best(v)
            signals.append((v["published"], "vulnerabilidade", f"{v['identifiers'][0]} · {v['package']}", link, f"`{v['id']}`", "NVD / aviso", v["id"], g))
    digests, seen_items = [], set()
    for p in sorted((ROOT / "intake" / "digests").glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not in_window(d.get("date", ""), s, e) or d.get("digest_id", "").endswith(("REPORT", "SPECTRUM")):
            continue
        digests.append(d["date"])
        for it in d.get("items", []):
            # An expanded edition (e.g. YYYY-MM-DD-ampliado.json) repeats the daily items: count each item once.
            if it.get("id") in seen_items:
                continue
            seen_items.add(it.get("id"))
            signals.append((d["date"], "digest", it["title"], f"[fonte]({it['url']})", f"`{it['id']}`", SEAL.get(it.get("seal"), it.get("seal", "")), None, it.get("source_grade", "")))
    signals.sort(key=lambda x: (x[0], x[7] or "Z"), reverse=True)

    ids = {x[6] for x in signals if x[6]}
    techs, used = Counter(), Counter()
    for r in rel:
        if r["source"] in ids and r["relationship"] in ("uses", "demonstrates") and r["target"] in tech:
            techs[r["target"]] += 1
        if r["source"] in ids and r["relationship"] == "uses-tool":
            used[tools.get(r["target"], r["target"])] += 1
    kev = [x for x in signals if x[1] == "KEV"]
    top_t = techs.most_common(6)
    lead = signals[0][2] if signals else "semana sem registros novos nos datasets"
    agent_share = sum(1 for x in signals if x[6] and any(r["source"] == x[6] and r["relationship"] == "uses-tool" for r in rel))

    L = [f'---\ntitle: "Tendências da semana · {tag}"\n---\n', "![Masthead](../../assets/reports/masthead-trends.svg)\n",
         f'<p class="rpt-head"><span>LLMI-TS-{tag}</span><span class="tlp">TLP:CLEAR</span><span>Corte {e} · janela {s} a {e}</span></p>\n',
         '<div class="injected" markdown="1">\n'
         f"Rascunho gerado por `scripts/build_weekly.py` a partir dos datasets e de {len(digests)} digest(s) diário(s) da janela. "
         "Os números e a lista de sinais são contados; as seções analíticas são escritas a partir desses sinais.\n</div>\n",
         '<div class="bluf" markdown="1">\n' + TODO + f"\n\n{len(signals)} sinais na semana; destaque: {cell(lead)}.\n</div>\n",
         "## Números da semana\n",
         "| Medida | Valor |\n|---|---|\n"
         f"| Sinais (registros, KEV, digests) | {len(signals)} |\n"
         f"| Incidentes e campanhas novos nos datasets | {sum(1 for x in signals if x[1] in ('incidente', 'campanha'))} |\n"
         f"| Com framework ofensivo agêntico | {agent_share} |\n"
         f"| Entradas novas no CISA KEV | {len(kev)} |\n"
         f"| Itens de digest diário | {sum(1 for x in signals if x[1] == 'digest')} |\n",
         "## Sinais\n", "| # | Data | Tipo | Sinal | Fonte | Item | Selo |\n|---|---|---|---|---|---|---|"]
    for i, x in enumerate(signals, 1):
        L.append(f"| {i} | {x[0]} | {x[1]} | {cell(x[2])} | {x[3]} | {x[4]} | {cell(x[5])} |")
    L.append("\n## Técnicas e ferramentas que se mexeram\n")
    if top_t:
        L.append("| Técnica | Sinais na semana |\n|---|---|\n" + "\n".join(f"| `{t}` {cell(tech[t])} | {n} |" for t, n in top_t))
    if used:
        L.append("\n**Ferramentas agênticas citadas:** " + ", ".join(f"{k} ({n})" for k, n in used.most_common()) + ".")
    if kev:
        L.append("\n**Novas no KEV:** " + "; ".join(f"{cell(x[2])} ({x[0]})" for x in kev) + ".")
    L += ["\n## O contraponto\n" + TODO, "\n## Segunda-feira do defensor\n" + TODO + "\n- **Uma detecção:**\n- **Um controle:**\n- **Uma hipótese de hunting:**",
          "\n## Camada 8\n" + TODO, "\n## Brasil e América Latina\n" + TODO, "\n## Para acompanhar\n" + TODO, "\n---\n", "## Versão curta (LinkedIn)\n"]
    bullets = "\n".join(f"- {cell(x[2])[:140]}" for x in signals[:3]) or "- Semana sem sinais novos nos datasets."
    L.append(f"{len(signals)} sinais de ameaça a sistemas de IA na semana de {start:%d/%m} a {end:%d/%m}.\n\n{bullets}\n\n"
             f"Relatório completo, fontes e grau de cada uma: {SITE}#tab=reports\n\n#CTI #SegurançaDeIA #ThreatIntel")
    path = OUT / f"{tag}.md"
    return path, "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--end", type=dt.date.fromisoformat, default=dt.date.today() - dt.timedelta(days=1))
    ap.add_argument("--stdout", action="store_true")
    a = ap.parse_args()
    path, text = draft(a.end)
    if a.stdout:
        print(text)
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
