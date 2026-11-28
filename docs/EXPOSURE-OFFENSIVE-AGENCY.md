# Agentes ofensivos de IA expostos na Internet (offensive.agency)

> Gerado por `scripts/offensive_agency_sync.py` a partir do [offensive.agency](https://offensive.agency) (dados da ONYPHE). Dia de referência **2026-11-27**, janela ativa desde 2026-11-21. Atualizado todo dia pelo workflow `exposure-daily.yml`.

## Resumo

- **6.892 IPs ativos** (vistos nos últimos 7 dias), 12.284 no histórico do rastreador; 2.781 novos na janela.
- **431 IPs rodam mais de um agente**; **82 também hospedam um C2**.
- Rede: hosting 6.306, cloud 380, cdn 206. 702 domínios, 167 atrás de CDN.
- Brasil e América Latina: **142 IPs** (BR 129, MX 4, CO 3, AR 3, DO 1, CL 1, PE 1).

## Por agente

| Agente | Registro no grafo | Ativos | Confirmados | Novos | Histórico | Porta mais vista |
|---|---|--:|--:|--:|--:|--:|
| [ARTEX](https://offensive.agency/agent/artex) | `TOOL-ARTEX` | 4.917 | 4.143 | 2.413 | 8.634 | 8787 |
| [CyberStrikeAI](https://offensive.agency/agent/cyberstrikeai) | `TOOL-CYBERSTRIKEAI` | 1.093 | 1.028 | 228 | 1.839 | 8080 |
| [PentAGI](https://offensive.agency/agent/pentagi) | `TOOL-PENTAGI` | 510 | 493 | 50 | 1.002 | 8443 |
| [Hermes Agent](https://offensive.agency/agent/hermes-agent) | sem registro | 326 | 0 | 62 | 743 | 9119 |
| [AutoCVE](https://offensive.agency/agent/autocve) | sem registro | 246 | 245 | 1 | 257 | 3000 |
| [DeepAudit](https://offensive.agency/agent/deepaudit) | sem registro | 74 | 70 | 3 | 92 | 3000 |
| [Cairn](https://offensive.agency/agent/cairn) | `TOOL-CAIRN` | 48 | 44 | 9 | 113 | 8000 |
| [RedAmon](https://offensive.agency/agent/redamon) | sem registro | 39 | 35 | 7 | 76 | 3000 |
| [Strix](https://offensive.agency/agent/strix) | `TOOL-STRIX` | 24 | 22 | 4 | 45 | 8080 |
| [CyberStrike](https://offensive.agency/agent/cyberstrike) | sem registro | 11 | 9 | 1 | 27 | 4096 |
| [HexStrike AI](https://offensive.agency/agent/hexstrike) | `TOOL-HEXSTRIKE-AI` | 10 | 1 | 3 | 17 | 443 |
| [Xalgorix](https://offensive.agency/agent/xalgorix) | sem registro | 10 | 8 | 4 | 14 | 443 |
| [Z3r0](https://offensive.agency/agent/z3r0) | sem registro | 6 | 5 | 2 | 7 | 8000 |
| [AIDA](https://offensive.agency/agent/aida) | sem registro | 5 | 4 | 0 | 10 | 31337 |
| [BugTraceAI](https://offensive.agency/agent/bugtraceai) | sem registro | 3 | 3 | 0 | 5 | 8000 |
| [AIRecon](https://offensive.agency/agent/airecon) | sem registro | 2 | 0 | 0 | 2 | 8080 |
| [Decepticon](https://offensive.agency/agent/decepticon) | sem registro | 2 | 1 | 0 | 5 | 3000 |
| [open-kritt](https://offensive.agency/agent/open-kritt) | sem registro | 2 | 2 | 0 | 3 | 80 |
| [Pentest-Swarm-AI](https://offensive.agency/agent/pentestswarm) | sem registro | 2 | 0 | 1 | 2 | 6666 |
| [T3MP3ST](https://offensive.agency/agent/t3mp3st) | sem registro | 2 | 0 | 1 | 2 | 3333 |
| [LuaN1aoAgent](https://offensive.agency/agent/luan1aoagent) | sem registro | 1 | 0 | 0 | 1 | 8787 |
| [REDCELL](https://offensive.agency/agent/redcell) | sem registro | 1 | 1 | 0 | 3 | 80 |
| [sapper-v2](https://offensive.agency/agent/sapper-v2) | sem registro | 1 | 0 | 0 | 4 | 2333 |
| [Vulnerator AI](https://offensive.agency/agent/vulnerator-ai) | sem registro | 1 | 1 | 0 | 110 | 9100 |
| [WormXGPT](https://offensive.agency/agent/wormxgpt) | sem registro | 1 | 1 | 0 | 3 | 3005 |
| [ARTEX-CC](https://offensive.agency/agent/artex-cc) | sem registro | 0 | 0 | 0 | 0 |  |
| [NeuroSploit](https://offensive.agency/agent/neurosploit) | sem registro | 0 | 0 | 0 | 1 |  |
| [NyxStrike](https://offensive.agency/agent/nyxstrike) | sem registro | 0 | 0 | 0 | 1 |  |
| [PentestCode](https://offensive.agency/agent/pentestcode) | sem registro | 0 | 0 | 0 | 0 |  |

## Como cada agente é reconhecido (consultas ONYPHE publicadas pelo rastreador)

Servem para caçar o console no seu próprio perímetro ou numa varredura autorizada: título da página, hash MD5 do favicon, texto da resposta. Indicadores da mesma família não são independentes.

- **ARTEX** · projeto: <https://github.com/BaaRai/ARTEX>
  - `app.device:"offensive agent"`
  - `favicon.data.md5:cd3ebd16437d6d3963592f7365dd3980`
  - `favicon.data.md5:e14fa4f2f1f6dfdd606c7267877fb72e`
  - `favicon.data.md5:16bf6c5653291854e8c56c8eff7ca20d`
  - `favicon.data.md5:885700bddad47ba6c1e891db12ad6640`
  - `html.title.raw:"ARTEX — 自主渗透测试控制台"`
  - `html.title.text:"ARTEX"`
  - `html.title.text:"Autonomous Penetration Testing Console"`
  - `html.title.text:"自主渗透测试控制台"`
  - `html.title.text:"자율 침투 테스트 콘솔"`
  - `html.title.text:"自律型ペネトレーションテストコンソール"`
  - `html.title.text:"Otonom Sızma Testi Konsolu"`
  - `app.data.text:"LLM 驱动的自主渗透测试系统控制台"`
  - `app.data.text:"Console for the LLM-driven autonomous penetration testing system"`
  - `app.data.text:"An LLM-driven system console for autonomous penetration testing"`
  - `app.data.text:"LLM 기반으로 자율 침투 테스트를 수행하는 시스템 콘솔"`
  - `app.data.text:"Una consola de sistema impulsada por LLM para pruebas de penetración autónomas"`
  - `app.data.text:"LLM を活用して自律的にペネトレーションテストを行うシステムコンソール"`
  - `app.data.text:"LLM güdümlü otonom sızma testi sistemi için konsol"`
  - `app.data.text:"AI 驱动的自主渗透测试平台"`
- **CyberStrikeAI** · projeto: <https://github.com/AIPentest/CyberStrikeAI>
  - `app.device:"offensive agent"`
  - `html.title.raw:"CyberStrikeAI"`
  - `extract.url:"https://github.com/Ed1s0nZ/CyberStrikeAI"`
  - `app.data.text:"CyberStrikeAI Logo"`
  - `favicon.data.md5:7d794e98f48497b767fceb032ef28e3e`
  - `favicon.data.md5:8675aef8c3ffdbe15bb2638291887954`
  - `app.data.text:"brand-wordmark__ai"`
- **PentAGI** · projeto: <https://github.com/vxcontrol/pentagi>
  - `html.title.text:"PentAGI"`
  - `cert.issuer.o:"PentAGI"`
  - `cert.issuer.cn:"PentAGI CA"`
  - `cert.subject.an:"pentagi.local"`
  - `favicon.data.md5:c7bf380529c43568d4bcad5e52c90c32`
  - `favicon.data.md5:d2fbb03231198e21b2e866363272a3d4`
  - `favicon.data.md5:bcfaddafe9133ff84ed893bb71d385a9`
- **Hermes Agent** · projeto: <https://github.com/NousResearch/hermes-agent>
  - `html.title.text:"Hermes Agent - Dashboard"`
- **AutoCVE** · projeto: <https://github.com/larlarua/AutoCVE>
  - `html.title.text:"AutoCVE"`
  - `favicon.data.md5:f20edcc49f7b035d4ff0b7dd62d67eae`
- **DeepAudit** · projeto: <https://github.com/lintsinghua/DeepAudit>
  - `html.title.raw:"DeepAudit"`
  - `favicon.data.md5:c0e1513d2d79dda98209cde3885b5f47`
- **Cairn** · projeto: <https://github.com/oritera/Cairn>
  - `favicon.data.md5:46f7bbdd5796a334ba2f6999f0c6798a`
  - `app.data.text:"reasonBeaconPulse"`
  - `app.data.text:"/static/favicon.svg"`
  - `app.data.text:"cytoscape-elk.js"`
  - `html.title.raw:"Cairn"`
  - `cert.subject.cn:"Cairn auto-generated TLS certificate"`
  - `cert.subject.o:"Cairn Platform"`
  - `html.title.text:"衍迹 · 自主探索工作台"`
  - `html.title.text:"衍迹 · 意图驱动推理工作台"`
- **RedAmon** · projeto: <https://github.com/samugit83/redamon>
  - `html.title.raw:"RedAmon"`
  - `favicon.data.md5:620b55364a1b370943ceeab58e1f49a3`
  - `favicon.data.md5:dca9c654ddce6aa63d1187c509a89345`
  - `app.data.text:"Security reconnaissance and vulnerability assessment dashboard"`
- **Strix** · projeto: <https://github.com/usestrix/strix>
  - `html.title.raw:"Strix Results"`
  - `favicon.data.md5:c25fd702de374ec0f0c95d737f50c277`
  - `app.data.text:"StrixViewer"`
- **CyberStrike** · projeto: <https://github.com/CyberStrikeus/cyberstrike>
  - `html.title.raw:"CyberStrike"`
  - `favicon.data.md5:dd4b4494c75b328270a4e63e592c400b`
  - `app.data.text:"x-cyberstrike-directory"`
  - `app.data.text:"cyberstrike-capture"`
  - `app.data.text:"Autonomous offensive security agent"`
- **HexStrike AI** · projeto: <https://github.com/0x4m4/hexstrike-ai>
  - `html.title.text:"HexStrike"`
  - `app.data.text:"hexstrike-ai"`
  - `app.data.text:".hexstrike_api_key"`
  - `app.data.text:"HexStrike AI Tools API Server"`
- **Xalgorix** · projeto: <https://github.com/xalgorix/xalgorix>
  - `html.title.text:"Xalgorix"`
  - `favicon.data.md5:7ce3d0eeae5c13ad1cf02ed0062c99b9`
  - `favicon.data.md5:152b1831875335f7fa32473e5edcd414`
  - `favicon.data.md5:27835995c192828ab5401a58242701ed`
  - `favicon.data.md5:64c97a7738b2e2b00760ccd6d276e97b`
  - `app.data.text:".xalgorix.env"`
  - `app.data.text:"xalgorix-linux-amd64"`
- **Z3r0** · projeto: <https://github.com/yv1ing/Z3r0>
  - `html.title.text:"Z3r0 Console"`
  - `favicon.data.md5:0f2b5d1d65422072b373cbc3e720dd80`
- **AIDA** · projeto: <https://github.com/Vasco0x4/AIDA>
  - `html.title.text:"AIDA - AI-Driven Security Assessment"`
  - `favicon.data.md5:d4be6f9e5330cbc5606bd101256e94fa`
  - `app.data.text:"AIDA API"`
  - `app.data.text:"tagline"`
- **BugTraceAI** · projeto: <https://github.com/BugTraceAI/BugTraceAI>
  - `app.data.text:"BugTraceAI API"`
  - `html.title.raw:"BugTraceAI"`
- **AIRecon** · projeto: <https://github.com/pikpikcu/airecon>
  - `html.title.text:"AIRecon Search"`
- **Decepticon** · projeto: <https://github.com/BitterSecurity/Decepticon>
  - `html.title.text:"Decepticon"`
  - `html.title.text:"Autonomous Red Team Platform"`
  - `favicon.data.md5:0d9eb87ab032844a4bed864085981964`
- **open-kritt** · projeto: <https://github.com/Kritt-ai/open-kritt>
  - `favicon.data.md5:2df232e29387b904996ae39123f79362`
  - `html.title.text:"kritt"`
- **Pentest-Swarm-AI** · projeto: <https://github.com/Armur-Ai/Pentest-Swarm-AI>
  - `html.title.text:"pentestswarm"`
  - `app.data.text:"pentestswarm"`
- **T3MP3ST** · projeto: <https://github.com/elder-plinius/T3MP3ST>
  - `html.title.text:"T3MP3ST"`
  - `html.title.text:"Dashboard"`
- **LuaN1aoAgent** · projeto: <https://github.com/SanMuzZzZz/LuaN1aoAgent>
  - `html.title.text:"鸾鸟渗透智能体"`
- **REDCELL** · projeto: <https://github.com/martian56/redcell>
  - `app.data.text:"apple-mobile-web-app-title"`
  - `app.data.text:"REDCELL"`
  - `favicon.data.md5:82d9011327979643168e73a45a394420`
- **sapper-v2** · projeto: <https://github.com/N1nEmAn/sapper-v2>
  - `html.title.text:"sapper"`
  - `html.title.text:"engagement graph"`
- **Vulnerator AI** · projeto: <https://github.com/irraz/vulnerator-ai>
  - `html.title.text:"Vulnerator Console"`
  - `favicon.data.md5:f27e45fa2a7d35d46111f1ca15f27c43`
- **WormXGPT** · projeto: <https://github.com/gaur-avvv/wormxgpt>
  - `html.title.text:"WormGPT Red Terminal"`
  - `html.title.text:"WormGPT Terminal"`
  - `favicon.data.md5:5be0a3173f6fc54a7862dda9fe1d223f`
- **ARTEX-CC** · projeto: <https://github.com/SREsAreHumanToo/ARTEX-CC>
  - `html.title.text:"ARTEX-CC"`
  - `favicon.data.md5:eddd4f1af798717d69460adc5084a8f9`
  - `favicon.data.md5:317c4c1d070cd9aa15ff7723fb7631eb`
- **NeuroSploit** · projeto: <https://github.com/JoasASantos/NeuroSploit>
  - `html.title.text:"NeuroSploit"`
  - `favicon.data.md5:f8fb482e183c10bb03aaf940dde7b18c`
- **NyxStrike** · projeto: <https://github.com/CommonHuman-Lab/nyxstrike>
  - `html.title.text:"NyxStrike"`
- **PentestCode** · projeto: <https://github.com/s0ld13rr/pentestcode>
  - `html.title.raw:"PentestCode"`

## C2 no mesmo IP

| Framework | IPs |
|---|--:|
| Sliver | 52 |
| Vshell | 17 |
| AdaptixC2 | 4 |
| Cobalt Strike | 3 |
| Mythic | 2 |
| Supershell | 2 |
| Havoc | 1 |
| Hak5 Cloud | 1 |
| Villain | 1 |
| Metasploit | 1 |

## Agentes no mesmo IP

| Par | IPs |
|---|--:|
| CyberStrikeAI + PentAGI | 215 |
| ARTEX + CyberStrikeAI | 153 |
| ARTEX + PentAGI | 43 |
| ARTEX + DeepAudit | 8 |
| ARTEX + Strix | 8 |
| ARTEX + Cairn | 7 |
| ARTEX + RedAmon | 3 |
| CyberStrikeAI + DeepAudit | 2 |
| CyberStrikeAI + RedAmon | 2 |
| ARTEX + AutoCVE | 2 |

## Clusters (detalhe de build compartilhado, não atribuição)

| Cluster | Hosts | Registro |
|---|--:|---|
| [antifox](https://offensive.agency/cluster/antifox) | 940 | `TOOL-ANTIFOX` |
| [artex-ruoji6-basic](https://offensive.agency/cluster/artex-ruoji6-basic) | 650 | – |
| [bob-research-labs](https://offensive.agency/cluster/bob-research-labs) | 158 | – |
| [forang](https://offensive.agency/cluster/forang) | 2 | – |
| [pojun](https://offensive.agency/cluster/pojun) | 193 | – |
| [scopeweaver](https://offensive.agency/cluster/scopeweaver) | 270 | – |
| [yueluo](https://offensive.agency/cluster/yueluo) | 8 | – |

## Países

| País | IPs |
|---|--:|
| US | 2003 |
| HK | 1286 |
| CN | 1163 |
| JP | 345 |
| SG | 287 |
| DE | 272 |
| NL | 230 |
| FR | 216 |
| KR | 174 |
| BR | 129 |
| CA | 119 |
| TH | 111 |
| ID | 86 |
| FI | 47 |
| LT | 41 |
| GB | 38 |
| MY | 33 |
| IN | 33 |
| VN | 30 |
| PL | 23 |

## Como usar na detecção

As listas ficam na fonte, que as refaz todo dia. Baixe com `python scripts/offensive_agency_sync.py --export <pasta>`, que separa os IPs de frente de CDN:

- `ips.txt`: <https://offensive.agency/api/ips.txt>
- `domains.txt`: <https://offensive.agency/api/domains.txt>
- `hosts.csv`: <https://offensive.agency/api/hosts.csv>
- `hosts.json`: <https://offensive.agency/api/hosts.json>
- `stats.json`: <https://offensive.agency/api/stats.json>

Parâmetros aceitos pela API do rastreador: `tool` (slug do agente), `scope=all`, `country`, `level`, `kind` (hosting, cloud, cdn), `domain=1`, `c2=1`, `multi=1`.

## Método e limites

Passive. The tracker reads ONYPHE scan data and never connects to a listed host; this repository only reads the tracker's public exports. Two independent fingerprint families on one IP make it confirmed, one makes it probable. Honeypots and IPs answering on 150 ports or more are dropped. Active = seen in the last 7 days.

A listed IP runs an exposed instance; that says nothing about who runs it or why (researchers, students, penetration testers and attackers all appear). A CDN-front IP is shared by unrelated sites: search the domain instead. A cloud IP can change owner within minutes: compare log dates with first and last seen. Counts are IPs, not machines. Clusters are a shared build detail, not an attribution.

Só a página inicial das portas varridas é visível: um agente em porta não varrida, ou que só responde num caminho de API, fica de fora. O histórico do rastreador começa em 2026-10-21; o deste repositório, no arquivo `data/exposure/offensive-agency-history.csv`.

## Referências

- offensive.agency, rastreador passivo de agentes ofensivos de IA expostos: <https://offensive.agency> (método em <https://offensive.agency/about>).
- ONYPHE, dados de varredura da Internet (ctiscan, ctiurl): <https://www.onyphe.io/>.
- Registro de fonte: `SRC-OFFENSIVE-AGENCY-TRACKER` em `data/sources.json`.
