#!/usr/bin/env python3
"""Build the print edition of the 2026 AI threat report: a designed A4 document, not a site export.

Writes three HTML files (cover, body, back cover) under the output folder. scripts/render_print_report.js turns
them into one PDF with a two-pass table of contents (page numbers read back from the first render).

    python scripts/build_print_report.py --out dist/print [--toc toc.json]

Content: the authored report in reports/intel (prose sections) plus sections generated from data/: actor map,
incident and leak timeline, AI-software KEV entries, AI model mapping, detection matrix, controls by layer and the
appendices. Illustrations come from assets/report-art.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import build_report_pages as brp

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "intel" / "2026-11-20-vulnerabilidades-e-incidentes-ia.md"
ART = ROOT / "assets" / "report-art"
CUT = "2026-11-20"
CODE = "LLMI-RI-2026-11-20"
TITLE = "Ameaças a sistemas de IA"
SUB = "Vulnerabilidades, incidentes e operações com agentes em 2026"
AGENT_TOOLS = {"TOOL-ARTEX", "TOOL-ANTIFOX", "TOOL-PENTAGI", "TOOL-CAIRN", "TOOL-CYBERSTRIKEAI", "TOOL-HEXSTRIKE-AI", "TOOL-STRIX", "TOOL-SCOPESENTRY"}
NEXUS_COLOR = {"China": "#f0885a", "North Korea": "#c9a227", "Russia": "#e05a5a", "Iran": "#3fae8c", "Pakistan": "#7aa6e0", "Financially motivated": "#b98cf0"}
MODEL_TERMS = {"MODEL-FAMILY-OPENAI-GPT": ["GPT", "OpenAI", "ChatGPT", "Codex"], "MODEL-FAMILY-ANTHROPIC-CLAUDE": ["Claude", "Anthropic"],
               "MODEL-FAMILY-GOOGLE-GEMINI": ["Gemini"], "MODEL-FAMILY-META-LLAMA": ["Llama"], "MODEL-FAMILY-DEEPSEEK": ["DeepSeek"],
               "MODEL-FAMILY-QWEN": ["Qwen"], "MODEL-FAMILY-MISTRAL": ["Mistral"], "MODEL-FAMILY-XAI-GROK": ["Grok"],
               "MODEL-FAMILY-MOONSHOT-KIMI": ["Kimi"], "MODEL-FAMILY-ZHIPU-GLM": ["GLM"], "MODEL-FAMILY-MICROSOFT-PHI": ["Phi-"],
               "MODEL-FAMILY-OLLAMA-LOCAL": ["Ollama", "local LLM", "local model"]}

CONF = {"confirmed": "confirmada", "high": "alta", "medium": "média", "low": "baixa", "unverified": "não verificada"}

GLOSSARY = [
    ("Agente de IA", "Sistema em que um modelo de linguagem escolhe e executa ações (chamar ferramentas, rodar comandos, ler e escrever arquivos) para cumprir um objetivo, com pouca ou nenhuma intervenção humana a cada passo."),
    ("ARTEX", "Framework open-source de pentest multiagente guiado por LLM, publicado em julho de 2026 e usado em intrusões reais desde agosto. Um agente planejador escolhe o próximo passo e agentes executores rodam ferramentas comuns."),
    ("BLUF", "Bottom line up front: a conclusão principal vem primeiro, antes da argumentação."),
    ("CISA KEV", "Catálogo de vulnerabilidades sabidamente exploradas da agência americana CISA. Estar no KEV é a evidência pública mais forte de exploração em campo."),
    ("Confiança", "Quanto o repositório confia numa afirmação: confirmada, alta, média, baixa ou não verificada. É diferente do grau da fonte."),
    ("CVE / CVSS / CWE", "Identificador público de uma vulnerabilidade; nota de severidade de 0 a 10; e a classe de fraqueza de software a que a falha pertence."),
    ("Destilação", "Treinar um modelo copiando as respostas de outro em larga escala, em geral sem autorização. Motiva o roubo de chaves de provedores de IA."),
    ("EPSS", "Probabilidade estimada de exploração de um CVE nos próximos 30 dias, publicada pela FIRST. Muda diariamente."),
    ("Exfiltração", "Retirada de dados do ambiente da vítima pelo atacante."),
    ("Fronteira de confiança", "Ponto em que dados ou comandos passam de uma zona menos confiável para uma mais confiável (por exemplo, um e-mail lido por um agente com acesso ao shell)."),
    ("Gateway LLM", "Proxy entre aplicações e provedores de modelo (LiteLLM é o exemplo central). Concentra chaves de todos os provedores e, por isso, é alvo preferido."),
    ("Grau da fonte (A–E)", "Qualidade da fonte: A primária ou confirmada, B fornecedor de segurança reconhecido, C imprensa ou fonte única, D agregador, E não avaliada."),
    ("Guardrail", "Controle que restringe o que o modelo ou o agente pode fazer em tempo de execução: filtros de entrada e saída, listas de ferramentas permitidas, aprovação humana."),
    ("Harness", "A estrutura em volta do modelo: ferramentas, permissões, memória, sandbox, registro e limites. Quem decide o que o agente consegue tocar é o harness, não o modelo."),
    ("Hardening", "Endurecimento da infraestrutura: versões corrigidas, menor exposição, menor privilégio, segredos fora do alcance."),
    ("Hunting (caça)", "Busca ativa por sinais de comprometimento que não dispararam alerta, a partir de uma hipótese."),
    ("Injeção de prompt direta", "O usuário escreve instruções para desviar o modelo das regras."),
    ("Injeção de prompt indireta", "A instrução hostil chega escondida num dado que o agente lê (página, e-mail, issue, evento de erro) e é executada com as permissões do usuário."),
    ("IOC", "Indicador de comprometimento: IP, domínio, hash ou artefato observado numa intrusão. Tem vida curta."),
    ("Jailbreak", "Técnica para fazer o modelo ignorar suas políticas de segurança."),
    ("KEV (data de entrada)", "Data em que a CISA incluiu a falha no catálogo; usada aqui para medir a velocidade da exploração."),
    ("LLM", "Large language model, o modelo de linguagem por trás de assistentes e agentes."),
    ("MCP", "Model Context Protocol: padrão para ligar agentes a ferramentas e dados. Servidores MCP expõem ferramentas; clientes MCP (agentes, IDEs) as chamam."),
    ("MITRE ATLAS / ATT&CK", "Bases de táticas e técnicas: ATLAS para ataques a sistemas de IA, ATT&CK para intrusões em geral."),
    ("n-day", "Vulnerabilidade já divulgada e corrigida, mas ainda explorável onde não houve atualização."),
    ("Orquestração agêntica", "Uso de vários agentes coordenados para executar uma operação ofensiva inteira em velocidade de máquina (técnica LLMI-T015)."),
    ("PoC", "Prova de conceito que demonstra que uma falha é explorável."),
    ("RAG", "Retrieval-augmented generation: o modelo consulta uma base de documentos antes de responder. Envenenar essa base é um vetor de ataque."),
    ("RCE", "Execução remota de código."),
    ("Sandbox", "Ambiente isolado onde o agente ou o código roda com acesso limitado."),
    ("Sigma", "Formato aberto de regras de detecção, convertível para SIEMs como Sentinel, Splunk e Elastic."),
    ("SSRF", "Falha em que o servidor é levado a fazer requisições para destinos escolhidos pelo atacante, como o serviço de metadados da nuvem."),
    ("STDIO (MCP)", "Modo em que o cliente MCP inicia o servidor como processo local; um servidor malicioso vira execução de comando na máquina."),
    ("Supply chain (cadeia de suprimentos)", "Comprometer um componente de terceiros (pacote, imagem, plugin, extensão) para atingir quem o usa."),
    ("TLP", "Traffic Light Protocol: regra de compartilhamento. TLP:CLEAR permite distribuição pública."),
    ("Tool poisoning / rug pull", "Ferramenta MCP que traz instruções escondidas na descrição, ou que muda de comportamento depois de aprovada."),
    ("TTP", "Táticas, técnicas e procedimentos: o modo de operar de um atacante."),
    ("Zero-day", "Vulnerabilidade explorada antes de existir correção pública."),
]


def esc(s: object) -> str:
    return html.escape(str(s if s is not None else ""), quote=True)


def data(name: str):
    return json.loads((ROOT / "data" / f"{name}.json").read_text(encoding="utf-8"))


def art(name: str, cls: str = "art") -> str:
    svg = (ART / f"{name}.svg").read_text(encoding="utf-8")
    return f'<div class="{cls}">{svg}</div>'


def md_section(md: str, number: str) -> str:
    """The body of '## {number}. …' without its heading, up to the next '## '."""
    m = re.search(rf"^## {re.escape(number)}\.\s.*$", md, re.M)
    if not m:
        return ""
    rest = md[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def md_sub(md: str, title: str) -> str:
    m = re.search(rf"^### {re.escape(title)}\s*$", md, re.M)
    if not m:
        return ""
    rest = md[m.end():]
    nxt = re.search(r"^##+ ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


class Doc:
    def __init__(self, vulns: list[dict]):
        self.link = brp.Linker(vulns)
        self.toc: list[tuple[str, str, str]] = []
        self.n = 0

    def render(self, md: str) -> str:
        out, _ = brp.render(md, self.link)
        out = re.sub(r'<h2 id="([^"]+)">', r'<h3 class="h2" id="\1">', out).replace("</h2>", "</h3>")
        return out

    def opener(self, key: str, num: str, title: str, lead: str, monster: str | None = None, inline: bool = False) -> str:
        if num.isdigit():
            self.n += 1
            num = f"{self.n:02d}"
        self.toc.append((key, num, title))
        mon = ""  # section openers stay clean; illustrations live on the covers only
        return (f'<section class="opener{" inline" if inline else ""}" id="{key}"><span class="mk">@@{key}@@</span>{mon}<div class="onum">{esc(num)}</div>'
                f'<h1>{esc(title)}</h1><p class="lead">{lead}</p><div class="orule"></div></section>')


KIND_PT = {"intrusion": "intrusão", "fraud": "fraude", "malware": "malware", "supply-chain": "cadeia de suprimentos", "atlas-incident": "incidente (ATLAS)",
           "unintended-access": "acesso não intencional", "exploitation": "exploração", "model-extraction": "extração de modelo", "exploit-development": "desenvolvimento de exploit"}
SKIP_KINDS = {"atlas-exercise", "research-artifact", "research-framework", "defensive-research", "observed-research-case"}
LEAK = re.compile(r"(?i)exfiltrat|stole|stolen|theft|leak|exposed|dump|personal data|card")


def when(r: dict) -> str:
    return str(r.get("reported") or r.get("date") or r.get("first_seen") or "")


def events(inc, cam, rel, src, tools):
    used = defaultdict(list)
    for r in rel:
        if r["relationship"] == "uses-tool":
            used[r["source"]].append(tools.get(r["target"], r["target"]))
    agent = {r["source"] for r in rel if (r["relationship"] == "uses-tool" and r["target"] in AGENT_TOOLS)
             or (r["target"] == "LLMI-T015" and r["relationship"] in ("demonstrates", "uses"))}
    out = []
    for r in inc + cam:
        w = when(r)
        if not w.startswith("2026") or r.get("kind") in SKIP_KINDS:
            continue
        ss = sorted((src[i] for i in r.get("source_ids", []) if i in src and src[i].get("url", "").startswith("https://")), key=lambda x: x.get("grade", "Z"))
        best = f"[{ss[0].get('publisher') or ss[0]['name']}]({ss[0]['url']}) ({ss[0].get('grade', '?')})" if ss else ""
        flags = [f for f, ok in (("vazamento", bool(LEAK.search(r.get("summary", "")))), ("agente de IA", r["id"] in agent)) if ok]
        out.append((w, r, KIND_PT.get(r.get("kind", ""), "campanha"), flags, ", ".join(used.get(r["id"], [])), best.replace("|", "/")))
    out.sort(key=lambda x: x[0], reverse=True)
    return out


def ev_table(rows) -> str:
    return ("| Data | Registro | Tipo | Conf. | Sinais | Ferramentas | Fonte principal |\n| --- | --- | --- | --- | --- | --- | --- |\n"
            + "\n".join(f"| {w} | {r['name'].replace('|', '/')} | {k} | {CONF.get(r.get('confidence'), '')} | {', '.join(f)} | {t} | {b} |" for w, r, k, f, t, b in rows))


def kpis(vul, inc, cam) -> list[tuple[str, str]]:
    kev26 = [v for v in vul if str(v.get("kev_added", "")).startswith("2026") and v.get("ai_relation", "ai-software") == "ai-software"]
    rel = data("relationships")
    agent = {r["source"] for r in rel if r["relationship"] == "uses-tool" and r["target"] in AGENT_TOOLS}
    ev26 = [r for r in inc + cam if str(r.get("reported") or r.get("date") or r.get("first_seen") or "").startswith("2026")]
    return [(str(len(kev26)), "falhas em software de IA entraram no CISA KEV em 2026"),
            (str(len([r for r in ev26 if r["id"] in agent])), "incidentes e campanhas de 2026 com framework ofensivo agêntico"),
            ("~36 h", "do aviso à exploração do LiteLLM CVE-2026-42208"),
            ("50%", "das falhas achadas por IA levam a execução remota de código (GTIG)")]


def nexus_pt(n: str) -> str:
    n = n or ""
    base = n.split(" (")[0].strip()
    m = {"China": "China", "North Korea": "Coreia do Norte", "North Korea nexus": "Coreia do Norte", "Russia": "Rússia", "Iran": "Irã",
         "Mali": "Mali", "Pakistan": "Paquistão", "Not stated in report": "não declarado", "Unattributed": "não atribuído",
         "Unattributed, financially motivated": "crime financeiro", "Unattributed, financially motivated, Brazil-focused": "crime financeiro (foco no Brasil)",
         "Cambodia-based, financially motivated": "crime financeiro (Camboja)"}
    return m.get(base, base)


def nexus_key(n: str) -> str:
    n = n or ""
    for k in ("China", "North Korea", "Russia", "Iran", "Pakistan"):
        if n.startswith(k):
            return k
    return "Financially motivated" if "financially" in n else ""


def actor_map(actors, cam, inc, rel, tools, w=1000, h=760, dark=True, limit=26):
    """Constellation: agentic tools in the centre, actors around them, coloured by nexus."""
    by = {r["id"]: r for r in cam + inc}
    conducts = defaultdict(set)
    for r in rel:
        if r["relationship"] == "conducts":
            conducts[r["source"]].add(r["target"])
    uses = defaultdict(set)
    for r in rel:
        if r["relationship"] == "uses-tool":
            uses[r["source"]].add(r["target"])
    links, act_nodes = defaultdict(set), []
    for a in actors:
        camps = [c for c in conducts.get(a["id"], ()) if c in by and str(by[c].get("first_seen") or by[c].get("reported") or "").startswith("2026")]
        if not camps:
            continue
        ts = {t for c in camps for t in uses.get(c, ())}
        act_nodes.append((a, len(camps), ts))
        for t in ts:
            links[a["id"]].add(t)
    act_nodes.sort(key=lambda x: (-len(x[2]), -x[1], x[0]["name"]))
    with_tools = [x for x in act_nodes if x[2]]
    others = [x for x in act_nodes if not x[2] and not x[0]["name"].startswith("GTG-")]
    act_nodes = (with_tools + others)[:limit]
    # alternate nexus groups around the ring so colours spread instead of clumping
    act_nodes.sort(key=lambda x: (x[0].get("nexus") or "zz", x[0]["name"]))
    used_tools = sorted({t for _, _, ts in act_nodes for t in ts} | {"TOOL-ARTEX"}, key=lambda t: t != "TOOL-ARTEX")
    import math
    cx, cy = w / 2, h / 2 + 10
    tpos = {}
    for i, t in enumerate(used_tools):
        ang = -math.pi / 2 + 2 * math.pi * i / max(1, len(used_tools))
        r = 0 if t == "TOOL-ARTEX" else 105
        tpos[t] = (cx + r * math.cos(ang), cy + r * math.sin(ang))
    apos = {}
    for i, (a, _n, _ts) in enumerate(act_nodes):
        ang = -math.pi / 2 + 2 * math.pi * i / max(1, len(act_nodes))
        k = 1 + (i % 2) * 0.12
        apos[a["id"]] = (cx + w * 0.33 * k * math.cos(ang), cy + h * 0.38 * k * math.sin(ang), ang)
    ink, paper, faint = ("#f3f0e8", "#15140f", "rgba(243,240,232,.16)") if dark else ("#15140f", "#f6f5f1", "rgba(21,20,15,.14)")
    g = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" class="amap">']
    for i in range(1, 6):
        g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{i * 78 * 1.18:.0f}" ry="{i * 78 * .86:.0f}" fill="none" stroke="{faint}" stroke-width="1"/>')
    for a, _n, ts in act_nodes:
        x, y, _ = apos[a["id"]]
        col = NEXUS_COLOR.get(nexus_key(a.get("nexus")), "#9a958a")
        for t in ts:
            tx, ty = tpos[t]
            g.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" stroke="{col}" stroke-opacity=".45" stroke-width="1.4"/>')
        if not ts:
            g.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{cx:.0f}" y2="{cy:.0f}" stroke="{faint}" stroke-width="1" stroke-dasharray="3 5"/>')
    for t in used_tools:
        x, y = tpos[t]
        big = t == "TOOL-ARTEX"
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{50 if big else 30}" fill="{"#b43c0e" if big else "#2a2823" if dark else "#15140f"}" stroke="{"#f0885a" if big else ink}" stroke-width="{4 if big else 1.5}"/>')
        g.append(f'<text x="{x:.0f}" y="{y + 4:.0f}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="{16 if big else 9}" fill="#fff">{esc(tools.get(t, t)[:11])}</text>')
    for a, n, _ts in act_nodes:
        x, y, ang = apos[a["id"]]
        col = NEXUS_COLOR.get(nexus_key(a.get("nexus")), "#9a958a")
        rr = 5 + min(n, 6) * 1.6
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="{col}" stroke="{paper}" stroke-width="2"/>')
        right = math.cos(ang) >= 0
        g.append(f'<text x="{x + (rr + 6) * (1 if right else -1):.0f}" y="{y + 4:.0f}" text-anchor="{"start" if right else "end"}" font-family="Inter" font-weight="600" font-size="12.5" fill="{ink}">{esc(a["name"])}</text>')
    lx = 24
    for name, col in NEXUS_COLOR.items():
        label = {"China": "China", "North Korea": "Coreia do Norte", "Russia": "Rússia", "Iran": "Irã", "Pakistan": "Paquistão", "Financially motivated": "Crime financeiro"}[name]
        g.append(f'<circle cx="{lx + 6}" cy="{h - 22}" r="6" fill="{col}"/><text x="{lx + 16}" y="{h - 18}" font-family="Inter" font-size="12" fill="{ink}">{label}</text>')
        lx += 22 + len(label) * 7.2
    g.append("</svg>")
    return "".join(g), act_nodes


def back_cover(css: str, K, code: str, version: str) -> str:
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body class="back">
<div class="cv-grid"></div>
<div class="bk-monsters">{''.join(art(n, "bk-m") for n in ("enxame", "mimico", "parasita", "devorador", "espelho", "rastreador"))}</div>
<div class="bk-names"><span>O Enxame<br><i>agentes ofensivos</i></span><span>O Mímico<br><i>injeção de prompt</i></span><span>O Parasita<br><i>cadeia de suprimentos</i></span><span>O Devorador<br><i>chaves e gateways</i></span><span>O Espelho<br><i>destilação</i></span><span>O Rastreador<br><i>reconhecimento</i></span></div>
<div class="bk-body"><h2>Evidência acima de exagero.</h2>
<p>LLMInjection é inteligência aberta sobre ameaças a sistemas de IA, LLM e agentes. Cada afirmação traz o grau da fonte e o nível de confiança, e cada registro deste relatório pode ser aberto, conferido e reutilizado no Explorer e no repositório.</p>
<div class="bk-kpis">{''.join(f'<div><b>{esc(v)}</b><span>{esc(lbl)}</span></div>' for v, lbl in K[:3])}</div>
<div class="bk-links"><div><span>Explorer</span>ridd1kulusc0d3r.github.io/LLmInjection</div><div><span>Repositório</span>github.com/Ridd1kulusC0d3r/LLmInjection</div><div><span>Dados</span>STIX 2.1 · GraphML · API JSON</div></div></div>
<footer class="cv-foot"><div><b>{code}</b> · {version} · TLP:CLEAR</div><div>Corte {CUT} · gerado {dt.date.today().isoformat()}</div></footer>
</body></html>"""


def build(out: Path, toc_pages: dict[str, int] | None = None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    fm, md = brp.front_matter(REPORT.read_text(encoding="utf-8"))
    vul, inc, cam, rel = data("vulnerabilities"), data("incidents"), data("campaigns"), data("relationships")
    actors, tech, det, ctr, models = data("actors"), data("techniques"), data("detections"), data("controls"), data("models")
    src = {s["id"]: s for s in data("sources")}
    tools = {t["id"]: t["name"] for t in data("tools")}
    doc = Doc(vul)
    K = kpis(vul, inc, cam)
    css = (ROOT / "scripts" / "print_report.css").read_text(encoding="utf-8")
    amap_dark, act_nodes = actor_map(actors, cam, inc, rel, tools, dark=True)
    amap_light, _ = actor_map(actors, cam, inc, rel, tools, dark=False)

    # ---------- cover ----------
    cover = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body class="cover">
<div class="cv-grid"></div><div class="cv-map">{amap_dark}</div>
<header class="cv-top"><span>LLMINJECTION · INTELIGÊNCIA DE AMEAÇAS</span><span class="tlp">TLP:CLEAR</span></header>
<div class="cv-title"><div class="cv-kicker">Relatório de inteligência de ameaças · 2026</div><h1>{TITLE}</h1><p>{SUB}</p></div>
{art("enxame", "cv-monster")}
<footer class="cv-foot"><div><b>{CODE}</b> · v2.0</div><div>Corte {CUT}</div><div>Mapa: atores com campanhas em 2026 e as ferramentas agênticas que usaram</div></footer>
</body></html>"""
    (out / "cover.html").write_text(cover, encoding="utf-8")

    # ---------- body ----------
    B: list[str] = []
    B.append(f"""<section class="page front">
<div class="fm-head"><span class="eyebrow">Ficha do relatório</span><h2>{TITLE}</h2><p class="lead">{SUB}</p></div>
<dl class="fm">
<dt>Código</dt><dd>{CODE} · versão 2.0</dd><dt>Data de corte</dt><dd>{CUT}</dd><dt>Classificação</dt><dd><span class="tlpb">TLP:CLEAR</span> distribuição pública</dd>
<dt>Produzido por</dt><dd>LLMInjection, inteligência aberta de ameaças a sistemas de IA, LLM e agentes</dd>
<dt>Base</dt><dd>Relatório autoral de 20/11/2026 (156 fontes) somado aos datasets do repositório: {len(vul)} vulnerabilidades, {len(inc)} incidentes, {len(cam)} campanhas, {len(actors)} atores, {len(det)} detecções, {len(ctr)} controles</dd>
<dt>Edição web</dt><dd>ridd1kulusc0d3r.github.io/LLmInjection</dd></dl>
<div class="howto"><h3>Como ler</h3><div class="howgrid">
<div><b>Grau da fonte</b><p><span class="g A">A</span> primária ou confirmada · <span class="g B">B</span> fornecedor reconhecido · <span class="g C">C</span> imprensa ou fonte única · <span class="g D">D</span> agregador</p></div>
<div><b>Confiança</b><p>confirmada · alta · média · baixa · não verificada. Grau mede a fonte; confiança mede a afirmação.</p></div>
<div><b>Selos</b><p><span class="kevb">KEV</span> falha no catálogo de exploradas da CISA · CVEs sublinhados têm registro no Explorer.</p></div>
<div><b>Escopo</b><p>Nenhuma seção traz payload ou cadeia de exploração reproduzível. Indicadores ficam nas fontes.</p></div></div></div>
</section>""")
    B.append('<section class="page toc"><span class="mk">@@toc@@</span><span class="eyebrow">Sumário</span><h2 class="toc-h">O que está neste relatório</h2><ol class="tocl">@@TOCLIST@@</ol></section>')

    # 01 summary
    s1 = md_section(md, "1")
    finds = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*\s*(.+)$", s1, re.M)
    prio = re.search(r"\*\*Prioridades imediatas:\*\*\s*(.+)", s1)
    upd = re.search(r"\*\*Atualização v1\.1:\*\*([\s\S]+?)\n\n\*\*Prioridades", s1)
    B.append(doc.opener("s01", "01", "Sumário executivo", "O que mudou em 2026, em sete julgamentos, e o que fazer primeiro.", "devorador"))
    B.append('<div class="kpis">' + "".join(f'<div class="kpi"><b>{esc(v)}</b><span>{esc(lbl)}</span></div>' for v, lbl in K) + "</div>")
    B.append('<div class="bluf"><span>BLUF</span>' + esc(re.sub(r"\s+", " ", s1.strip().split("\n\n")[0])) + "</div>")
    B.append('<div class="finds">' + "".join(f'<div class="find"><i>{i:02d}</i><h4>{doc.render(t)[3:-4]}</h4><p>{doc.render(d)[3:-4]}</p></div>' for i, (t, d) in enumerate(finds, 1)) + "</div>")
    if upd:
        B.append('<div class="callout">' + doc.render(upd.group(1).strip()) + "</div>")
    if prio:
        B.append('<div class="prio"><h4>Prioridades imediatas</h4>' + doc.render(prio.group(1)) + "</div>")

    # hot: last 30 days
    evs = events(inc, cam, rel, src, tools)
    since = (dt.date.fromisoformat(CUT) - dt.timedelta(days=30)).isoformat()
    hot = [e for e in evs if e[0][:10] >= since[:len(e[0][:10])]]
    kev_new = sorted((v for v in vul if v.get("kev_added", "") >= since), key=lambda v: v["kev_added"], reverse=True)
    B.append(doc.opener("shot", "02", "O mais quente agora", f"O que foi divulgado nos 30 dias até {CUT}: {len(hot)} incidentes e campanhas e {len(kev_new)} entrada(s) nova(s) no CISA KEV."))
    B.append(doc.render("Gerado dos datasets do repositório na data de corte. Os títulos ficam em inglês, como nos registros; a fonte principal é a de melhor grau. \"Vazamento\" marca registros cujo resumo descreve exfiltração, roubo ou exposição de dados; \"agente de IA\" marca uso de framework ofensivo agêntico.\n\n" + ev_table(hot)))
    if kev_new:
        B.append(doc.render("**Entradas novas no KEV no período:** " + "; ".join(f"{v['identifiers'][0]} ({v['package']}, {v['kev_added']})" for v in kev_new) + "."))

    # scope, method and verification notes
    B.append(doc.opener("sscope", "03", "Escopo, metodologia e confiança", "O que entra, o que fica de fora, como cada afirmação foi conferida e o que mudou entre as versões."))
    B.append(doc.render(md_section(md, "2")))
    inj = re.search(r'<div class="injected" markdown="1">([\s\S]+?)</div>', md)
    if inj:
        B.append(doc.render("### Notas de versão e verificação\n\n" + inj.group(1).strip()))

    # 02 landscape
    B.append(doc.opener("s02", "02", "Panorama de ameaças", "Onde a exploração de 2026 se concentrou, e a velocidade com que aconteceu.", "parasita"))
    B.append(brp.kev_chart(vul).replace('href="../#node=', 'href="https://ridd1kulusc0d3r.github.io/LLmInjection/#node='))
    B.append(doc.render(md_section(md, "3")))

    # 03 actor map
    B.append(doc.opener("s03", "03", "Mapeamento de atores de ameaças", "Quem usou IA contra quem em 2026, e com quais ferramentas agênticas.", "rastreador"))
    B.append(f'<figure class="amapfig">{amap_light}<figcaption>Atores com campanhas em 2026 nos datasets. Ligações mostram o uso de framework ofensivo agêntico; o tamanho do ponto, o número de campanhas. Usar a mesma ferramenta não liga atores entre si.</figcaption></figure>')
    rows = []
    roles_pt = {"tooling-development": "desenvolvimento de ferramentas", "ai-infrastructure-targeting": "alvo: infraestrutura de IA", "runtime-enabler": "apoio em execução",
                "ai-supply-chain-targeting": "alvo: cadeia de IA", "local-analysis": "análise local", "coding-agent-targeting": "alvo: agentes de código", "supply-chain": "cadeia de suprimentos",
                "autonomous-operator": "operador autônomo", "offensive-enabler": "apoio ofensivo", "influence-operations": "operações de influência",
                "malware-development": "desenvolvimento de malware", "social-engineering": "engenharia social", "reconnaissance": "reconhecimento",
                "model-abuse": "abuso de modelo", "fraud": "fraude", "vulnerability-research": "pesquisa de falhas", "target": "alvo"}
    for a, n, ts in act_nodes:
        rows.append(f"| {esc(a['name'])} | {esc(nexus_pt(a.get('nexus')))} | {esc(', '.join(roles_pt.get(x, x) for x in a.get('ai_role', [])))} | {n} | {esc(', '.join(tools.get(t, t) for t in sorted(ts)) or '—')} | {CONF.get(a.get('confidence'), a.get('confidence', ''))} |")
    B.append(doc.render("| Ator | Nexo | Papel da IA | Campanhas 2026 | Ferramentas agênticas | Confiança |\n| --- | --- | --- | --- | --- | --- |\n" + "\n".join(rows)))
    B.append(doc.render(md_section(md, "6")))

    # 04 timeline
    B.append(doc.opener("s04", "04", "Linha do tempo de incidentes e vazamentos", "Os casos de 2026 com impacto confirmado, exploração ativa ou técnica nova.", "enxame"))
    tl = md_section(md, "5")
    intro = tl.strip().split("\n\n")[0]
    B.append(doc.render(intro))
    trows = re.findall(r"^\| (?!Data|---)(.+?) \| (.+?) \| (\w+) \| (.+?) \|$", tl, re.M)
    cat_pt = {"EXP": "Exploração", "SC": "Cadeia de suprimentos", "PI": "Injeção de prompt", "OFF": "IA ofensiva", "AUT": "Agente sem adversário", "ID": "Identidade", "EXPO": "Exposição"}
    items = []
    for d, name, catg, what in trows:
        items.append(f'<div class="tli c-{catg}"><div class="tld">{esc(d)}</div><div class="tlb"><span class="tag t-{catg}">{esc(cat_pt.get(catg, catg))}</span>'
                     f'<h4>{doc.render(name.replace(" *v1.1*", ""))[3:-4]}</h4><p>{doc.render(what)[3:-4]}</p></div></div>')
    B.append('<div class="tline">' + "".join(items) + "</div>")
    tail = tl.strip().split("\n\n")[-1]
    if not tail.startswith("|"):
        B.append(doc.render(tail))

    # 05 vulnerabilities
    B.append(doc.opener("s05", "05", "Vulnerabilidades documentadas", "Os CVEs que importam, o que o KEV confirma e o que agentes de IA já encontram.", "devorador"))
    s4 = md_section(md, "4")
    B.append(doc.render(s4.split("### LiteLLM")[0]))
    B.append(doc.render("### Vulnerabilidades encontradas por IA\n" + md_sub(md, "Vulnerabilidades encontradas por IA")))
    for sub in ("LiteLLM: o caso mais grave da tabela", "Flowise", "Família MCP", "Agentes de código e copilots", "CrewAI", "Rejeitados: Rails, Adminer e Achievo"):
        body = md_sub(md, sub)
        if body:
            B.append(doc.render(f"### {sub}\n{body}"))

    # 06 models
    B.append(doc.opener("s06", "06", "Mapeamento de modelos de IA", "Quais famílias de modelo aparecem em operações ofensivas, e onde ficam os controles de cada uma.", "espelho"))
    ev = [r for r in inc + cam if str(r.get("reported") or r.get("date") or r.get("first_seen") or "").startswith("2026")]
    mrows = []
    for m in models:
        terms = MODEL_TERMS.get(m["id"], [m["name"]])
        hits = [r for r in ev if any(re.search(rf"\b{re.escape(tm)}", r.get("summary", "") + " " + r.get("name", "")) for tm in terms)]
        famrel = [r for r in rel if r["relationship"] == "uses-model-family" and r["target"] == m["id"]]
        ex = "; ".join(esc(h["name"][:60]) for h in hits[:3])
        mrows.append((len(hits) + len(famrel), f"| {esc(m['name'])} | {esc(m.get('provider', ''))} | {esc(', '.join(m.get('deployment', [])))} | {len(hits)} | {ex or '—'} | {esc(', '.join(x.replace('-', ' ') for x in m.get('security_focus', [])[:3]))} |"))
    mrows.sort(key=lambda x: -x[0])
    B.append(doc.render("Contagem de incidentes e campanhas de 2026 cujo registro cita a família de modelo pelo nome. Citação não é atribuição: muitos casos usam vários modelos e o provedor costuma ser a vítima do abuso, não o atacante.\n\n"
                        "| Família | Provedor | Implantação | Casos em 2026 | Exemplos | Foco de controle |\n| --- | --- | --- | --- | --- | --- |\n" + "\n".join(r for _, r in mrows)))
    B.append(doc.render("**Leitura para o defensor.** Os frameworks agênticos não trazem modelo próprio: ARTEX e afins chamam APIs de terceiros (DeepSeek domina nas instâncias de atacantes analisadas pelo FBI), o que faz da chave de API do provedor o ativo que o atacante precisa e da telemetria do provedor uma fonte de detecção. Modelos locais (Ollama e similares) tiram essa telemetria do caminho e aparecem como runtime não autorizado (`DET-AI-002`)."))

    # ARTEX dossier
    dfm, dmd = brp.front_matter((ROOT / "reports" / "dossiers" / "artex.md").read_text(encoding="utf-8"))
    B.append(doc.opener("sartex", "09", "Dossiê ARTEX", "O framework ofensivo agêntico que mais apareceu em intrusões de 2026: quem usa, como opera, como detectar e o que não se pode afirmar."))
    dbody = dmd[dmd.find("<div class=\"bluf\""):] if "<div class=\"bluf\"" in dmd else dmd
    dbody = re.sub(r"<span class=\"conf conf-\w+\">(.*?)</span>", r"\1", dbody)
    B.append(doc.render(dbody))

    # 07 threat modeling
    B.append(doc.opener("s07", "07", "Modelagem de ameaças", "Ativos, fronteiras de confiança e os cenários de abuso que mais se repetem em stacks de IA.", "mimico"))
    B.append(doc.render(md_section(md, "7")))

    # 08 detection matrix
    B.append(doc.opener("s08", "08", "Matriz de detecção", "Cada técnica, o que a detecta, o que já tem regra pronta e o que a testa.", "rastreador"))
    rule = defaultdict(list)
    for p in (ROOT / "detections").glob("*/det-ai-*"):
        rule["-".join(p.name.split("-")[:3]).upper()].append(p.parent.name)
    detects, mitig, valid, evid = defaultdict(set), defaultdict(set), defaultdict(set), Counter()
    for r in rel:
        if r["relationship"] == "detects":
            detects[r["target"]].add(r["source"])
        elif r["relationship"] == "mitigated-by":
            mitig[r["source"]].add(r["target"])
        elif r["relationship"] == "validates":
            valid[r["target"]].add(r["source"])
        elif r["relationship"] in ("uses", "demonstrates"):
            evid[r["target"]] += 1
    layer = {c["id"]: c.get("layer") for c in ctr}
    mat_pt = {"observed-in-the-wild": "em campo", "disclosed-vulnerability": "falha divulgada", "research-demonstrated": "pesquisa", "no-linked-evidence": "sem evidência"}
    hdr = '<table class="dmx"><thead><tr><th>Técnica</th><th>Maturidade</th><th>Evidências</th><th>Detecções</th><th>Com regra</th><th>Testes</th><th>Guardrail</th><th>Hardening</th><th>Monitor.</th></tr></thead><tbody>'
    cells = []

    def heat(n: int, hi: int) -> str:
        lvl = 0 if n == 0 else 1 if n < hi / 3 else 2 if n < 2 * hi / 3 else 3
        return f'<td class="h{lvl}">{n}</td>'
    for t in tech:
        ds = detects.get(t["id"], set())
        wr = [d for d in ds if rule.get(d)]
        cs = mitig.get(t["id"], set())
        cells.append(f'<tr><th><span class="tid">{t["id"][5:]}</span>{esc(t["name"])}</th><td class="mat m-{t.get("maturity", "")}">{mat_pt.get(t.get("maturity", ""), "")}</td>'
                     + heat(evid[t["id"]], 20) + heat(len(ds), 6) + heat(len(wr), 3) + heat(len(valid.get(t["id"], ())), 3)
                     + heat(sum(1 for c in cs if layer.get(c) == "guardrail"), 3) + heat(sum(1 for c in cs if layer.get(c) == "hardening"), 3)
                     + heat(sum(1 for c in cs if layer.get(c) == "monitoring"), 2) + "</tr>")
    B.append('<p class="note">Células mais escuras indicam mais cobertura. "Com regra" conta detecções que têm arquivo Sigma, KQL, SPL, ES|QL ou YARA-L no repositório; as demais são especificação. Zeros, em laranja, são as lacunas para priorizar.</p>')
    B.append(hdr + "".join(cells) + "</tbody></table>")
    drows = []
    for d in det:
        if rule.get(d["id"]):
            covers = sorted(r["target"] for r in rel if r["source"] == d["id"] and r["relationship"] == "detects")
            drows.append(f"| {d['id']} | {esc(d['name'])} | {esc(', '.join(sorted(set(rule[d['id']]))))} | {esc(', '.join(c.replace('LLMI-', '') for c in covers))} |")
    B.append(doc.render("### Detecções com regra pronta\n\n| ID | Detecção | Formatos | Cobre |\n| --- | --- | --- | --- |\n" + "\n".join(drows)))
    B.append(doc.render(md_section(md, "8")))
    B.append(doc.render("### Oportunidades no repositório artex-detections\n" + md_section(md, "13")))

    # 09 hunting
    B.append(doc.opener("s09", "09", "Threat hunting", "Doze hipóteses, as consultas de partida e o que fazer quando uma delas confirma.", "enxame"))
    B.append(doc.render(md_section(md, "9")))

    # 10 harness/guardrails/hardening
    B.append(doc.opener("s10", "10", "Harness, guardrails e hardening", "Corrigir resolve o CVE da semana; reduzir exposição e privilégio resolve o próximo.", "parasita"))
    B.append(doc.render(md_section(md, "11")))
    B.append(doc.render(md_section(md, "10")))
    lay_pt = {"guardrail": "Guardrail", "hardening": "Hardening", "monitoring": "Monitoramento"}
    crow = []
    for c in sorted(ctr, key=lambda c: (c.get("layer", ""), c["name"])):
        ts = sorted(t for t, cs in mitig.items() if c["id"] in cs and t.startswith("LLMI-"))
        crow.append(f"| {lay_pt.get(c.get('layer'), c.get('layer'))} | {esc(c['name'])} | {esc((c.get('description') or '')[:170])} | {esc(', '.join(t.replace('LLMI-', '') for t in ts))} |")
    B.append(doc.render("### Controles do repositório por camada\n\n| Camada | Controle | O que faz | Técnicas |\n| --- | --- | --- | --- |\n" + "\n".join(crow)))

    # 11 plan
    B.append(doc.opener("s11", "11", "Plano de ação 30/60/90", "Conter, estruturar e sustentar, com indicadores para acompanhar.", "devorador"))
    B.append(doc.render(md_section(md, "12")))

    # glossary
    B.append(doc.opener("s12", "12", "Glossário", "Os termos deste relatório, em uma linha cada.", "mimico"))
    B.append('<dl class="gloss">' + "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in GLOSSARY) + "</dl>")

    # references
    B.append(doc.opener("s13", "13", "Referências", "As fontes consultadas, com o endereço completo para conferência.", "espelho"))
    used_src = set()
    for r in inc + cam + vul:
        if str(r.get("reported") or r.get("date") or r.get("first_seen") or r.get("published") or "").startswith("2026"):
            used_src.update(r.get("source_ids", []))
    refs = sorted((src[s] for s in used_src if s in src and src[s].get("url", "").startswith("https://")), key=lambda s: (s.get("grade", "Z"), s.get("publisher", ""), s["name"]))
    B.append('<p class="note">Fontes que sustentam os registros de 2026 citados neste relatório, ordenadas por grau. A lista completa do relatório autoral segue depois.</p>')
    B.append('<ol class="refs">' + "".join(f'<li><span class="g {esc(s.get("grade", ""))}">{esc(s.get("grade", ""))}</span> <b>{esc(s.get("publisher", ""))}.</b> {esc(s["name"])}. <a href="{esc(s["url"])}">{esc(s["url"])}</a></li>' for s in refs) + "</ol>")
    B.append(doc.render("### Fontes do relatório autoral\n" + md_section(md, "14")))

    # appendices
    B.append(doc.opener("sappA", "A", "Apêndice A: linha do tempo de incidentes e vazamentos de 2026", f"Todos os incidentes e campanhas de 2026 nos datasets ({len(evs)} registros), sem exercícios e artefatos de pesquisa."))
    B.append(doc.render(ev_table(evs)))
    B.append(doc.opener("s14", "B", "Apêndice B: CVEs documentadas", "Todas as vulnerabilidades com CVE nos datasets, conferidas em NVD, GHSA ou aviso do fornecedor.", None))
    rel_pt = {"ai-software": "software de IA", "ai-discovered": "encontrada por IA", "exploited-by-ai-agent": "usada por agente"}
    cves = sorted((v for v in vul if any(i.startswith("CVE-") for i in v["identifiers"])), key=lambda v: (v.get("kev_added", ""), v["published"]), reverse=True)
    B.append(doc.render("| CVE | Produto | Falha | Sev. | Corrigida em | KEV | Relação com IA |\n| --- | --- | --- | --- | --- | --- | --- |\n" + "\n".join(
        f"| {', '.join(i for i in v['identifiers'] if i.startswith('CVE-'))} | {brp._cell(v['package']) if hasattr(brp, '_cell') else v['package']} | {v['name'].replace('|', '/')} | {v.get('severity', '')} | {(', '.join(v.get('patched') or []) or '—').replace('|', '/')} | {v.get('kev_added', '')} | {rel_pt.get(v.get('ai_relation', 'ai-software'))} |" for v in cves)))

    body = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body class="doc">{''.join(B)}</body></html>"""
    pages = toc_pages or {}
    toc = "".join(f'<li><span class="tn">{esc(n)}</span><span class="tt">{esc(t)}</span><span class="dots"></span><span class="tp">{pages.get(k, "")}</span></li>' for k, n, t in doc.toc)
    body = body.replace("@@TOCLIST@@", toc)
    (out / "body.html").write_text(body, encoding="utf-8")
    (out / "toc-keys.json").write_text(json.dumps([k for k, _, _ in doc.toc]), encoding="utf-8")

    # ---------- back cover ----------
    (out / "back.html").write_text(back_cover(css, K, CODE, "v2.0"), encoding="utf-8")


def build_dossier(md_path: Path, out: Path, toc_pages: dict[str, int] | None = None) -> None:
    """Same design for a dossier: cover with the actor map, sheet, numbered contents, one opener per section."""
    out.mkdir(parents=True, exist_ok=True)
    fm, md = brp.front_matter(md_path.read_text(encoding="utf-8"))
    vul, inc, cam, rel = data("vulnerabilities"), data("incidents"), data("campaigns"), data("relationships")
    actors = data("actors")
    tools = {t["id"]: t["name"] for t in data("tools")}
    css = (ROOT / "scripts" / "print_report.css").read_text(encoding="utf-8")
    head = re.search(r'<p class="rpt-head">(.*?)</p>', md)
    meta = re.findall(r"<span[^>]*>(.*?)</span>", head.group(1)) if head else []
    code_v = (meta[0] if meta else md_path.stem).split(" · ")
    code, version = code_v[0], (code_v[1] if len(code_v) > 1 else "v1")
    cut = (re.search(r"Corte (\d{4}-\d{2}-\d{2})", md) or [None, CUT])[1]
    full = fm.get("title", md_path.stem)
    after = full.split(":", 1)[1].strip() if ":" in full else full
    title, _, sub = after.partition(",")
    sub = sub.strip()
    amap_dark, _ = actor_map(actors, cam, inc, rel, tools, dark=True)
    (out / "cover.html").write_text(f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body class="cover">
<div class="cv-grid"></div><div class="cv-map">{amap_dark}</div>
<header class="cv-top"><span>LLMINJECTION · INTELIGÊNCIA DE AMEAÇAS</span><span class="tlp">TLP:CLEAR</span></header>
<div class="cv-title"><div class="cv-kicker">Dossiê de ameaça · 2026</div><h1>{esc(title)}</h1><p>{esc(sub[:1].upper() + sub[1:])}</p></div>
{art("enxame", "cv-monster")}
<footer class="cv-foot"><div><b>{esc(code)}</b> · {esc(version)}</div><div>Corte {esc(cut)}</div><div>Mapa: atores com campanhas em 2026 e as ferramentas agênticas que usaram</div></footer>
</body></html>""", encoding="utf-8")
    doc = Doc(vul)
    B = [f"""<section class="page front"><div class="fm-head"><span class="eyebrow">Ficha do dossiê</span><h2>{esc(title)}</h2><p class="lead">{esc(sub)}</p></div>
<dl class="fm"><dt>Código</dt><dd>{esc(code)} · {esc(version)}</dd><dt>Data de corte</dt><dd>{esc(cut)}</dd><dt>Classificação</dt><dd><span class="tlpb">TLP:CLEAR</span> distribuição pública</dd>
<dt>Produzido por</dt><dd>LLMInjection, inteligência aberta de ameaças a sistemas de IA, LLM e agentes</dd><dt>Edição web</dt><dd>ridd1kulusc0d3r.github.io/LLmInjection</dd></dl>
<div class="howto"><h3>Como ler</h3><div class="howgrid">
<div><b>Grau da fonte</b><p><span class="g A">A</span> primária ou confirmada · <span class="g B">B</span> fornecedor reconhecido · <span class="g C">C</span> imprensa ou fonte única</p></div>
<div><b>Confiança</b><p>alta · média · baixa. Grau mede a fonte; confiança mede a afirmação.</p></div>
<div><b>Identificadores</b><p>IDs como <code>SRC-…</code>, <code>TOOL-…</code> e <code>DET-AI-…</code> abrem o registro no Explorer.</p></div>
<div><b>Escopo</b><p>Nenhuma seção traz payload. Indicadores ficam nas fontes e nos pacotes citados.</p></div></div></div></section>""",
         '<section class="page toc"><span class="mk">@@toc@@</span><span class="eyebrow">Sumário</span><h2 class="toc-h">O que está neste dossiê</h2><ol class="tocl">@@TOCLIST@@</ol></section>']
    bluf = re.search(r'<div class="bluf" markdown="1">([\s\S]+?)</div>', md)
    inj = re.search(r'<div class="injected" markdown="1">([\s\S]+?)</div>', md)
    parts = re.split(r"^## (\d+(?:\.\d+)?)\.\s+(.+)$", md, flags=re.M)
    first = True
    for k in range(1, len(parts), 3):
        _, name, body = parts[k], parts[k + 1].strip(), parts[k + 2]
        B.append(doc.opener(f"d{k}", "01", name, "", inline=not first))
        if first:
            if bluf:
                B.append('<div class="bluf"><span>BLUF</span>' + doc.render(bluf.group(1).strip())[3:-4] + "</div>")
            if inj:
                B.append('<div class="callout"><b>Notas de versão</b>' + doc.render(inj.group(1).strip()) + "</div>")
            first = False
        body = re.sub(r"<span class=\"conf conf-\w+\">(.*?)</span>", r"\1", body)
        B.append(doc.render(body))
    B.append(doc.opener("dgl", "01", "Glossário", "Os termos deste dossiê, em uma linha cada."))
    B.append('<dl class="gloss">' + "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in GLOSSARY) + "</dl>")
    pages = toc_pages or {}
    toc = "".join(f'<li><span class="tn">{esc(n)}</span><span class="tt">{esc(t)}</span><span class="dots"></span><span class="tp">{pages.get(k, "")}</span></li>' for k, n, t in doc.toc)
    (out / "body.html").write_text(f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body class="doc">{''.join(B)}</body></html>""".replace("@@TOCLIST@@", toc), encoding="utf-8")
    (out / "toc-keys.json").write_text(json.dumps([k for k, _, _ in doc.toc]), encoding="utf-8")
    (out / "back.html").write_text(back_cover(css, kpis(vul, inc, cam), code, version), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=ROOT / "dist" / "print")
    ap.add_argument("--toc", type=Path, help="JSON {section key: page number} from the first render")
    ap.add_argument("--dossier", type=Path, help="build this dossier (reports/dossiers/*.md) instead of the 2026 report")
    a = ap.parse_args()
    toc = json.loads(a.toc.read_text(encoding="utf-8")) if a.toc and a.toc.exists() else None
    if a.dossier:
        build_dossier(a.dossier if a.dossier.is_absolute() else ROOT / a.dossier, a.out, toc)
    else:
        build(a.out, toc)
    print(a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
