#!/usr/bin/env python3
"""Render each analyst report (reports/intel, reports/dossiers) as a standalone web page in the site's identity.

Stdlib only. The Markdown subset is the one the reports use: front matter, headings, paragraphs, pipe tables,
ordered and unordered lists, fenced code, block quotes, raw HTML blocks (with markdown="1" inside), inline code,
bold, italic and links. CVE IDs held in data/vulnerabilities.json link to their record in the Explorer.

Optional front matter keys:
    kpis: "13|AI entries in CISA KEV in 2026; 36 h|advisory to exploitation"   (value|label pairs)
    kev_chart: true                                                            (timeline of AI KEV entries)

    python scripts/build_report_pages.py --out _site/relatorios
"""

from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/Ridd1kulusC0d3r/LLmInjection/blob/main/"
DIRS = ("intel", "dossiers")
TAGS = {"EXP": "exploração", "SC": "cadeia de suprimentos", "PI": "injeção de prompt", "OFF": "uso ofensivo",
        "AUT": "agente sem adversário", "ID": "identidade", "EXPO": "exposição"}
CVE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b")
KEV_DATE = re.compile(r"KEV (?:on|since) (\d{4}-\d{2}-\d{2})")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", re.sub(r"<[^>]+>", "", s)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    return "s-" + (re.sub(r"[\s_]+", "-", s).strip("-")[:56] or "sec")


class Linker:
    """Links CVE IDs to Explorer records, outside existing links and code."""

    def __init__(self, vulns: list[dict]):
        self.by_cve = {i: v for v in vulns for i in v["identifiers"] if i.startswith("CVE-")}
        self.seen: set[str] = set()

    def __call__(self, h: str) -> str:
        out, in_a, in_code = [], 0, 0
        for part in re.split(r"(<[^>]+>)", h):
            if part.startswith("<"):
                low = part.lower()
                in_a += 1 if low.startswith("<a ") else -1 if low.startswith("</a") else 0
                in_code += 1 if low.startswith("<code") else -1 if low.startswith("</code") else 0
                out.append(part)
            elif in_a or in_code:
                out.append(part)
            else:
                out.append(CVE.sub(self.link, part))
        return "".join(out)

    def link(self, m: re.Match) -> str:
        v = self.by_cve.get(m.group(0))
        if not v:
            return m.group(0)
        self.seen.add(v["id"])
        kev = " kev" if "SRC-CISA-KEV-CATALOG" in v.get("source_ids", []) else ""
        return f'<a class="cve{kev}" href="../#node={esc(v["id"])}" title="{esc(v["name"])}">{m.group(0)}</a>'


def inline(s: str, link: Linker) -> str:
    codes: list[str] = []

    def keep(m: re.Match) -> str:
        codes.append(f"<code>{esc(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    s = re.sub(r"`([^`]+)`", keep, s)
    s = esc(s).replace("&quot;", '"').replace("&#x27;", "'")
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", lambda m: f'<a class="out" href="{m.group(2)}" rel="noopener">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], s)
    return link(s)


def cell(c: str, link: Linker, head: str) -> str:
    raw = c.strip()
    h = head.lower()
    if h.startswith("conf") and raw in {"A", "B", "C", "D", "E"}:
        return f'<span class="wgrade g-{raw}">{raw}</span>'
    if h.startswith("cat") and raw in TAGS:
        return f'<span class="tag t-{raw}" title="{esc(TAGS[raw])}">{raw}</span>'
    if h.startswith("severidade") and raw:
        return f'<span class="sev s-{slug(raw)}">{esc(raw)}</span>'
    return inline(raw, link)


def render(md: str, link: Linker) -> tuple[str, list[tuple[int, str, str]]]:
    lines, out, toc, i = md.split("\n"), [], [], 0
    para: list[str] = []

    def flush() -> None:
        if para:
            out.append(f"<p>{inline(' '.join(para), link)}</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            flush()
            lang, buf = s[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            out.append(f'<div class="code"><span class="lang">{esc(lang or "texto")}</span><button type="button" class="copy" data-copy>Copiar</button><pre><code>{esc(chr(10).join(buf))}</code></pre></div>')
        elif m := re.match(r"^(#{1,4})\s+(.*)$", s):
            flush()
            lvl, text = len(m.group(1)), m.group(2)
            if lvl == 1:
                i += 1
                continue
            sid = slug(text)
            if lvl == 2:
                toc.append((lvl, sid, text))
                num = re.match(r"^(\d+)\.\s+(.*)$", text)
                label = f'<span class="wnum">{num.group(1).zfill(2)}</span>{inline(num.group(2), link)}' if num else inline(text, link)
                out.append(f'<h2 id="{sid}">{label}</h2>')
            else:
                toc.append((lvl, sid, text))
                out.append(f'<h{lvl} id="{sid}">{inline(text, link)}</h{lvl}>')
        elif s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            flush()
            head = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c for c in re.split(r"(?<!\\)\|", lines[i].strip()[1:-1])])
                i += 1
            th = "".join(f"<th>{inline(h, link)}</th>" for h in head)
            tb = "".join("<tr>" + "".join(f'<td data-label="{esc(head[k] if k < len(head) else "")}">{cell(c, link, head[k] if k < len(head) else "")}</td>' for k, c in enumerate(r)) + "</tr>" for r in rows)
            filt = '<input class="tfilter" type="search" placeholder="Filtrar esta tabela" aria-label="Filtrar esta tabela">' if len(rows) >= 10 else ""
            out.append(f'<div class="wtbl">{filt}<div class="tscroll"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div></div>')
            continue
        elif re.match(r"^(\d+)\.\s+", s) or re.match(r"^[-*]\s+", s):
            flush()
            ordered = bool(re.match(r"^\d+\.", s))
            items = []
            while i < len(lines) and (re.match(r"^\s*(\d+\.|[-*])\s+", lines[i])):
                items.append(re.sub(r"^\s*(\d+\.|[-*])\s+", "", lines[i]))
                i += 1
                while i < len(lines) and lines[i].startswith("   ") and lines[i].strip() and not re.match(r"^\s*(\d+\.|[-*])\s+", lines[i]):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x, link)}</li>" for x in items) + f"</{tag}>")
            continue
        elif s.startswith(">"):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(f"<blockquote>{inline(' '.join(buf), link)}</blockquote>")
            continue
        elif s.startswith("<div") or s.startswith("</div") or s.startswith("<p ") or s.startswith("<p>"):
            flush()
            if 'class="rpt-head"' not in s:
                out.append(s.replace(' markdown="1"', ""))
        elif not s:
            flush()
        else:
            para.append(s)
        i += 1
    flush()
    return "\n".join(out), toc


def front_matter(text: str) -> tuple[dict, str]:
    fm: dict[str, str] = {}
    if text.startswith("---\n"):
        end = text.index("\n---", 4)
        for ln in text[4:end].splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
        text = text[end + 4:]
    return fm, text


def kev_chart(vulns: list[dict]) -> str:
    pts = []
    for v in vulns:
        m = KEV_DATE.search(v.get("summary", ""))
        added = v.get("kev_added") or (m.group(1) if m else "")
        if added.startswith("2026") and v.get("ai_relation", "ai-software") == "ai-software" and "SRC-CISA-KEV-CATALOG" in v.get("source_ids", []):
            pts.append((added, v))
    pts.sort(key=lambda x: x[0])
    if not pts:
        return ""
    W, H, L, R, T, B = 1000, 360, 40, 20, 20, 46
    x = lambda d: L + (int(d[5:7]) - 1 + (int(d[8:10]) - 1) / 31) / 12 * (W - L - R)  # noqa: E731
    y = lambda n: H - B - n / max(len(pts), 1) * (H - T - B)  # noqa: E731
    months = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    grid = "".join(f'<line x1="{x(f"2026-{k + 1:02d}-01"):.1f}" x2="{x(f"2026-{k + 1:02d}-01"):.1f}" y1="{T}" y2="{H - B}" class="g"/><text x="{x(f"2026-{k + 1:02d}-01") + 4:.1f}" y="{H - B + 18}" class="m">{months[k]}</text>' for k in range(12))
    step, prev = [f"M{L} {y(0):.1f}"], 0
    for n, (d, _) in enumerate(pts, 1):
        step.append(f"H{x(d):.1f}V{y(n):.1f}")
        prev = n
    step.append(f"H{W - R}")
    dots = "".join(
        f'<a href="../#node={esc(v["id"])}"><g class="pt" transform="translate({x(d):.1f} {y(n):.1f})"><circle r="6"/><title>{esc(d)} · {esc(v["package"])} · {esc(v["identifiers"][0])}</title></g></a>'
        f'<text class="lbl" x="{x(d) + (10 if n % 2 else -10):.1f}" y="{y(n) + 4:.1f}" text-anchor="{"start" if n % 2 else "end"}">{esc(v["package"])} <tspan class="d">{d[8:10]}/{d[5:7]}</tspan></text>'
        for n, (d, v) in enumerate(pts, 1))
    return (f'<figure class="chart"><figcaption><b>{prev}</b> vulnerabilidades de software de IA entraram no catálogo CISA KEV em 2026 '
            f'(acumulado, por data de inclusão). Cada ponto abre o registro no Explorer.</figcaption>'
            f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Entradas de IA no CISA KEV em 2026">{grid}'
            f'<path class="step" d="{"".join(step)}"/>{dots}</svg>'
            f'<p class="csrc">Fonte: feed JSON do CISA KEV, conferido em cada registro de <code>data/vulnerabilities.json</code>.</p></figure>')


def page(path: Path, vulns: list[dict], index: list[dict]) -> tuple[str, dict]:
    fm, body = front_matter(path.read_text(encoding="utf-8"))
    link = Linker(vulns)
    title = fm.get("title") or (re.search(r"^#\s+(.+)$", body, re.M) or [None, path.stem])[1]
    content, toc = render(body, link)
    rel = path.relative_to(ROOT).as_posix()
    kind = "Dossiê" if path.parent.name == "dossiers" else "Relatório de inteligência"
    head = re.search(r'<p class="rpt-head">(.*?)</p>', body)
    meta = re.findall(r"<span[^>]*>(.*?)</span>", head.group(1)) if head else []
    date = re.search(r"\b(20\d\d-\d\d-\d\d)\b", path.stem + " " + body[:800])
    kpis = [k.split("|", 1) for k in fm.get("kpis", "").split(";") if "|" in k]
    toc_html = "".join(f'<a href="#{sid}" class="l{lvl}">{esc(re.sub(r"[*`]", "", text))}</a>' for lvl, sid, text in toc)
    ids = sorted(link.seen)
    graph = f'<a class="btn" href="../report.html#ids={",".join(ids[:40])}&depth=1&lang=pt">Relatório sob demanda dos {len(ids)} CVEs no grafo ↗</a>' if ids else ""
    hero_kpis = "".join(f'<div class="kpi"><b>{esc(v.strip())}</b><span>{esc(lbl.strip())}</span></div>' for v, lbl in kpis)
    chart = kev_chart(vulns) if fm.get("kev_chart") == "true" else ""
    words = len(re.sub(r"<[^>]+>", " ", content).split())
    others = "".join(f'<a href="{esc(Path(r["path"]).stem)}.html">{esc(r["title"])}</a>' for r in index if r["path"] != rel)
    doc = TEMPLATE.format(
        title=esc(title), kind=esc(kind), kind_up=esc(kind.upper()), code=esc(meta[0] if meta else path.stem.upper()),
        date=esc(date.group(1) if date else ""), tlp=esc(meta[1] if len(meta) > 1 else "TLP:CLEAR"),
        minutes=max(1, round(words / 220)), sections=len([t for t in toc if t[0] == 2]), kpis=hero_kpis,
        chart=chart, toc=toc_html, content=content, github=REPO + rel, graph=graph, others=others,
        desc=esc(re.sub(r"<[^>]+>|\s+", " ", content)[:220].strip()))
    return doc, {"path": rel, "title": title}


TEMPLATE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · LLMInjection</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="article">
<link rel="stylesheet" href="../style.css">
<style>
:root{{--w:1240px}}
body{{background:var(--paper)}}
.progress{{position:fixed;top:0;left:0;height:3px;width:0;background:var(--signal);z-index:20}}
.top{{position:sticky;top:0;z-index:10;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px max(16px,calc((100% - var(--w))/2));background:color-mix(in srgb,var(--paper) 86%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--rule-2);font:600 11px var(--mono);letter-spacing:.12em;text-transform:uppercase}}
.top a{{color:var(--ink-2);text-decoration:none}}.top a:hover{{color:var(--signal)}}
.top .acts{{display:flex;gap:6px;flex-wrap:wrap}}
.top button,.btn{{font:600 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--ink);background:var(--card);border:1px solid var(--rule);padding:8px 13px;border-radius:var(--pill);cursor:pointer;text-decoration:none;display:inline-block}}
.top button:hover,.btn:hover{{border-color:var(--ink)}}
.btn.primary{{background:var(--signal);color:var(--signal-ink);border-color:var(--signal)}}
.hero{{position:relative;overflow:hidden;background:#15140f;color:#f3f0e8;padding:64px max(16px,calc((100% - var(--w))/2)) 44px}}
.hero:before{{content:"";position:absolute;inset:0;background:radial-gradient(900px 420px at 88% -10%,rgba(240,136,90,.35),transparent 65%),repeating-linear-gradient(90deg,rgba(255,255,255,.04) 0 1px,transparent 1px 80px),repeating-linear-gradient(0deg,rgba(255,255,255,.04) 0 1px,transparent 1px 80px);pointer-events:none}}
.hero>*{{position:relative}}
.hero .wbar{{display:flex;justify-content:space-between;gap:12px;font:700 12px var(--mono);letter-spacing:.18em;border-bottom:1px solid rgba(243,240,232,.35);padding-bottom:12px;color:#cfc9ba}}
.hero .wbar .tlp{{color:#f0885a}}
.hero h1{{font:700 clamp(34px,5.6vw,68px)/1.04 Georgia,"Times New Roman",serif;letter-spacing:-.025em;margin:28px 0 16px;max-width:20ch}}
.hero .meta{{display:flex;flex-wrap:wrap;gap:8px 22px;font:12px var(--mono);color:#bdb8aa}}
.hero .meta b{{color:#f3f0e8;font-weight:600}}
.hero .ctas{{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}}
.hero .btn{{background:transparent;color:#f3f0e8;border-color:rgba(243,240,232,.4)}}.hero .btn:hover{{border-color:#f0885a;color:#f0885a}}
.hero .btn.primary{{background:#f0885a;color:#131210;border-color:#f0885a}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1px;margin-top:36px;background:rgba(243,240,232,.18);border:1px solid rgba(243,240,232,.18);border-radius:14px;overflow:hidden}}
.kpi{{background:#1c1b17;padding:20px 22px}}
.kpi b{{display:block;font:700 clamp(30px,3.6vw,44px)/1 var(--display);letter-spacing:-.03em;color:#f0885a}}
.kpi span{{display:block;margin-top:8px;font-size:13.5px;color:#cfc9ba;line-height:1.4}}
.layout{{display:grid;grid-template-columns:250px minmax(0,1fr);gap:48px;max-width:var(--w);margin:0 auto;padding:40px 16px 80px}}
nav.toc{{position:sticky;top:64px;align-self:start;max-height:calc(100vh - 84px);overflow:auto;font-size:13px;border-left:1px solid var(--rule)}}
nav.toc .h{{font:700 11px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);padding:0 0 8px 14px}}
nav.toc a{{display:block;padding:5px 10px 5px 14px;margin-left:-1px;border-left:2px solid transparent;color:var(--ink-2);text-decoration:none;line-height:1.35}}
nav.toc a.l3{{padding-left:26px;font-size:12px;color:var(--ink-3)}}
nav.toc a.on{{border-left-color:var(--signal);color:var(--ink);font-weight:600}}
nav.toc a:hover{{color:var(--signal)}}
article{{min-width:0;font-size:16.5px;line-height:1.7}}
article h2{{display:flex;align-items:baseline;gap:14px;font:700 clamp(26px,3vw,34px)/1.15 Georgia,serif;letter-spacing:-.015em;margin:72px 0 18px;padding-top:18px;border-top:2px solid var(--ink);scroll-margin-top:70px}}
article h2:first-of-type{{margin-top:0}}
article h2 .wnum{{font:700 13px var(--mono);color:var(--signal);letter-spacing:.08em}}
article h3{{font:700 20px/1.3 var(--display);margin:40px 0 10px;scroll-margin-top:70px}}
article h4{{font:600 13px var(--mono);letter-spacing:.08em;text-transform:uppercase;margin:28px 0 8px}}
article p,article li{{color:var(--ink-2)}}article strong{{color:var(--ink)}}
article ol,article ul{{padding-left:22px}}article li{{margin:8px 0}}
article ol li::marker{{font:700 14px var(--mono);color:var(--signal)}}
article code{{font:13.5px var(--mono);background:var(--paper-2);padding:1px 6px;border-radius:5px;overflow-wrap:anywhere}}
.injected{{font-family:var(--sans)!important;border:1px solid var(--signal);background:var(--signal-soft);border-radius:12px;padding:6px 22px;margin:0 0 32px;font-size:15px}}
.injected *{{font-family:inherit}}.injected code,.injected a.cve{{font-family:var(--mono)}}.injected:before{{content:"PROVENIÊNCIA E VERIFICAÇÃO";display:block;font:700 11px var(--mono);letter-spacing:.14em;color:var(--signal);margin:12px 0 -4px}}
.bluf{{border-left:4px solid var(--signal);padding:4px 20px;margin:0 0 28px;font-size:18px}}
blockquote{{margin:20px 0;padding:14px 20px;border-left:4px solid var(--signal);background:var(--card);border-radius:0 10px 10px 0}}
.wtbl{{margin:20px 0 28px}}
.tscroll{{overflow:auto;max-height:78vh;border:1px solid var(--rule-2);border-radius:12px;background:var(--card);box-shadow:var(--shadow-1)}}
table{{border-collapse:collapse;width:100%;font-size:14px;line-height:1.5}}
thead th{{position:sticky;top:0;z-index:1;background:var(--paper-2);font:600 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3);text-align:left;padding:11px 14px;border-bottom:1px solid var(--rule)}}
td{{padding:11px 14px;border-bottom:1px solid var(--rule-2);vertical-align:top;color:var(--ink-2);overflow-wrap:anywhere}}
tbody tr:hover td{{background:var(--paper)}}
tbody tr:last-child td{{border-bottom:0}}
.tfilter{{width:100%;max-width:340px;margin:0 0 10px;padding:9px 14px;border:1px solid var(--rule);border-radius:var(--pill);background:var(--card);color:var(--ink);font:14px var(--sans)}}
.wgrade,.tag,.sev{{display:inline-block;font:700 11px var(--mono);padding:2px 8px;border-radius:5px;letter-spacing:.04em;white-space:nowrap}}
.wgrade.g-A{{background:var(--ink);color:var(--paper)}}.wgrade.g-B{{background:var(--paper-2);color:var(--ink);border:1px solid var(--ink-3)}}.wgrade.g-C{{border:1px dashed var(--ink-3);color:var(--ink-2)}}
.tag{{background:var(--paper-2);color:var(--ink)}}.tag.t-EXP{{background:var(--signal);color:var(--signal-ink)}}.tag.t-SC{{background:#6b4fbb;color:#fff}}.tag.t-PI{{background:#1f6f8b;color:#fff}}.tag.t-OFF{{background:#15140f;color:#f3f0e8}}.tag.t-AUT{{background:#7a6a2a;color:#fff}}.tag.t-ID{{background:#2f7a4f;color:#fff}}
.sev.s-crítica{{background:var(--signal);color:var(--signal-ink)}}.sev.s-alta{{background:var(--ink);color:var(--paper)}}
a.cve{{font:600 .92em var(--mono);text-decoration:none;border-bottom:1.5px solid var(--rule);white-space:nowrap}}
a.cve:hover{{border-color:var(--signal);color:var(--signal)}}
a.cve.kev:after{{content:"KEV";font:700 9px var(--mono);margin-left:4px;padding:1px 4px;border-radius:3px;background:var(--signal);color:var(--signal-ink);vertical-align:2px}}
.code{{position:relative;margin:18px 0 26px;border-radius:12px;background:#15140f;color:#e8e4d8;overflow:hidden}}
.code pre{{margin:0;padding:38px 18px 18px;overflow:auto;font:13px/1.6 var(--mono)}}
.code code{{background:none;padding:0;color:inherit}}
.code .lang{{position:absolute;top:10px;left:16px;font:700 10px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:#f0885a}}
.code .copy{{position:absolute;top:8px;right:10px;font:600 10px var(--mono);text-transform:uppercase;letter-spacing:.08em;background:transparent;color:#cfc9ba;border:1px solid #45423a;border-radius:6px;padding:4px 8px;cursor:pointer}}
.chart{{margin:0 0 40px;padding:22px 24px 14px;background:var(--card);border:1px solid var(--rule-2);border-radius:14px;box-shadow:var(--shadow-1)}}
.chart figcaption{{font-size:15px;color:var(--ink-2)}}.chart figcaption b{{font:700 26px var(--display);color:var(--signal);margin-right:6px}}
.chart svg{{width:100%;height:auto;margin-top:8px}}
.chart .g{{stroke:var(--rule-2)}}.chart .m{{font:11px var(--mono);fill:var(--ink-3);text-transform:uppercase}}
.chart .step{{fill:none;stroke:var(--signal);stroke-width:2.5}}
.chart .pt circle{{fill:var(--card);stroke:var(--signal);stroke-width:2.5}}.chart .pt:hover circle{{fill:var(--signal)}}
.chart .lbl{{font:600 11.5px var(--mono);fill:var(--ink);paint-order:stroke;stroke:var(--card);stroke-width:4px}}.chart .lbl .d{{fill:var(--ink-3);font-weight:400}}
.chart .csrc{{font-size:12px;color:var(--ink-3);margin:4px 0 0}}
.end{{margin-top:80px;padding:28px;border:1px solid var(--rule);border-radius:14px;background:var(--card)}}
.end h3{{margin:0 0 10px;font:700 18px var(--display)}}.end .others a{{display:block;margin:6px 0}}
@media (max-width:980px){{.layout{{grid-template-columns:1fr;gap:0}}nav.toc{{position:static;max-height:none;border:1px solid var(--rule-2);border-radius:12px;padding:12px 0;margin-bottom:28px;background:var(--card)}}
  .top .acts button:not(.keep){{display:none}}}}
@media (max-width:640px){{thead{{display:none}}table,tbody,tr,td{{display:block}}tr{{padding:10px 0;border-bottom:1px solid var(--rule)}}td{{border:0;padding:4px 14px}}td:before{{content:attr(data-label);display:block;font:600 10px var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--ink-3)}}.tscroll{{max-height:none}}}}
@media print{{.top,.progress,nav.toc,.ctas,.tfilter,.copy,.end .others{{display:none!important}}.layout{{display:block;padding:0}}.hero{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}.tscroll{{max-height:none;overflow:visible;box-shadow:none}}article h2{{break-before:page}}tr,.code,.chart{{break-inside:avoid}}a.out:after{{content:" (" attr(href) ")";font-size:10px;color:#666;word-break:break-all}}}}
</style>
</head>
<body>
<div class="progress" id="progress"></div>
<header class="top"><a href="../#tab=reports">← LLMInjection · Relatórios</a><div class="acts"><button type="button" onclick="print()">PDF</button><button type="button" class="keep" id="share">Copiar link</button><button type="button" id="theme">Tema</button></div></header>
<section class="hero">
  <div class="wbar"><span>LLMINJECTION / {kind_up}</span><span class="tlp">{tlp}</span></div>
  <h1>{title}</h1>
  <div class="meta"><span><b>{code}</b></span><span>Corte <b>{date}</b></span><span><b>{sections}</b> seções</span><span>Leitura de <b>{minutes} min</b></span></div>
  <div class="ctas"><a class="btn primary" href="#conteudo">Ler o relatório</a>{graph}<a class="btn" href="{github}" rel="noopener">Markdown no GitHub ↗</a></div>
  <div class="kpis">{kpis}</div>
</section>
<div class="layout"><nav class="toc" aria-label="Sumário"><div class="h">Sumário</div>{toc}</nav>
<article id="conteudo">{chart}{content}
<section class="end"><h3>Como ler este material</h3><p>Graus de fonte A a E e níveis de confiança seguem a metodologia do repositório. CVEs sublinhados abrem o registro no Explorer; o selo KEV indica entrada confirmada no catálogo da CISA. Nenhuma seção traz payload ou cadeia de exploração reproduzível.</p><div class="others"><h3>Outros produtos</h3>{others}</div></section>
</article></div>
<script>
(function(){{
var p=document.getElementById("progress"),links=[].slice.call(document.querySelectorAll("nav.toc a")),heads=links.map(function(a){{return document.getElementById(a.getAttribute("href").slice(1))}});
function onScroll(){{var h=document.documentElement,max=h.scrollHeight-h.clientHeight;p.style.width=(max>0?h.scrollTop/max*100:0)+"%";var cur=0;heads.forEach(function(el,i){{if(el&&el.getBoundingClientRect().top<120)cur=i}});links.forEach(function(a,i){{a.classList.toggle("on",i===cur)}})}}
addEventListener("scroll",onScroll,{{passive:true}});onScroll();
document.querySelectorAll(".tfilter").forEach(function(f){{f.addEventListener("input",function(){{var q=f.value.toLowerCase();f.parentNode.querySelectorAll("tbody tr").forEach(function(r){{r.hidden=q&&r.textContent.toLowerCase().indexOf(q)<0}})}})}});
document.querySelectorAll("[data-copy]").forEach(function(b){{b.addEventListener("click",function(){{navigator.clipboard&&navigator.clipboard.writeText(b.parentNode.querySelector("code").textContent).then(function(){{b.textContent="Copiado"}})}})}});
document.getElementById("share").onclick=function(e){{navigator.clipboard&&navigator.clipboard.writeText(location.href).then(function(){{e.target.textContent="Copiado"}})}};
var root=document.documentElement;try{{var s=localStorage.getItem("llmi-theme");if(s)root.dataset.theme=s}}catch(_){{}}
document.getElementById("theme").onclick=function(){{var d=root.dataset.theme==="dark"||(!root.dataset.theme&&matchMedia("(prefers-color-scheme:dark)").matches);root.dataset.theme=d?"light":"dark";try{{localStorage.setItem("llmi-theme",root.dataset.theme)}}catch(_){{}}}};
}})();
</script>
</body>
</html>
"""


def reports() -> list[Path]:
    return sorted(p for d in DIRS for p in (ROOT / "reports" / d).glob("*.md"))


def build(out: Path) -> list[dict]:
    vulns = json.loads((ROOT / "data" / "vulnerabilities.json").read_text(encoding="utf-8"))
    out.mkdir(parents=True, exist_ok=True)
    paths = reports()
    index = []
    for p in paths:
        fm, body = front_matter(p.read_text(encoding="utf-8"))
        index.append({"path": p.relative_to(ROOT).as_posix(), "title": fm.get("title", p.stem)})
    made = []
    for p in paths:
        doc, row = page(p, vulns, index)
        (out / f"{p.stem}.html").write_text(doc, encoding="utf-8")
        made.append({**row, "page": f"relatorios/{p.stem}.html"})
    return made


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=ROOT / "dist" / "relatorios")
    a = ap.parse_args()
    for r in build(a.out):
        print(r["page"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
