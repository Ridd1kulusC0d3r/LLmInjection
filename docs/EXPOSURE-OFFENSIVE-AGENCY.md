# Agentes ofensivos de IA expostos na Internet (offensive.agency)

> Gerado por `scripts/offensive_agency_sync.py` a partir do [offensive.agency](https://offensive.agency) (dados da ONYPHE). Dia de referência **2026-11-22**, janela ativa desde 2026-11-16. Atualizado todo dia pelo workflow `exposure-daily.yml`.

## Resumo

- **5.005 IPs ativos** (vistos nos últimos 7 dias), 8.087 no histórico do rastreador; 1.373 novos na janela.
- **444 IPs rodam mais de um agente**; **27 também hospedam um C2**.
- Rede: hosting 4.644, cloud 294, cdn 67. 203 domínios, 46 atrás de CDN.
- Brasil e América Latina: **38 IPs** (BR 29, MX 5, CO 2, BO 1, AR 1).

## Por agente

| Agente | Registro no grafo | Ativos | Confirmados | Novos | Histórico | Porta mais vista |
|---|---|--:|--:|--:|--:|--:|
| [ARTEX](https://offensive.agency/agent/artex) | `TOOL-ARTEX` | 3.617 | 3.437 | 1.058 | 5.870 | 8787 |
| [CyberStrikeAI](https://offensive.agency/agent/cyberstrikeai) | `TOOL-CYBERSTRIKEAI` | 1.029 | 1.018 | 145 | 1.574 | 8080 |
| [PentAGI](https://offensive.agency/agent/pentagi) | `TOOL-PENTAGI` | 664 | 648 | 149 | 950 | 8443 |
| [RedAmon](https://offensive.agency/agent/redamon) | sem registro | 45 | 42 | 11 | 69 | 3000 |
| [Cairn](https://offensive.agency/agent/cairn) | `TOOL-CAIRN` | 43 | 40 | 6 | 97 | 8000 |
| [Strix](https://offensive.agency/agent/strix) | `TOOL-STRIX` | 25 | 25 | 4 | 42 | 8080 |
| [CyberStrike](https://offensive.agency/agent/cyberstrike) | sem registro | 15 | 14 | 5 | 26 | 4096 |
| [HexStrike AI](https://offensive.agency/agent/hexstrike) | `TOOL-HEXSTRIKE-AI` | 11 | 0 | 5 | 14 | 443 |
| [Xalgorix](https://offensive.agency/agent/xalgorix) | sem registro | 9 | 6 | 1 | 11 | 443 |
| [BugTraceAI](https://offensive.agency/agent/bugtraceai) | sem registro | 3 | 3 | 1 | 5 | 8000 |
| [Pentest-Swarm-AI](https://offensive.agency/agent/pentestswarm) | sem registro | 1 | 0 | 1 | 1 | 8777 |

## Como cada agente é reconhecido (consultas ONYPHE publicadas pelo rastreador)

Servem para caçar o console no seu próprio perímetro ou numa varredura autorizada: título da página, hash MD5 do favicon, texto da resposta. Indicadores da mesma família não são independentes.

- **ARTEX** · projeto: <https://github.com/BaaRai/ARTEX>
  - `app.device:"offensive agent"`
  - `favicon.data.md5:cd3ebd16437d6d3963592f7365dd3980`
  - `favicon.data.md5:885700bddad47ba6c1e891db12ad6640`
  - `html.title.raw:"ARTEX — 自主渗透测试控制台"`
  - `html.title.text:"ARTEX"`
  - `html.title.text:"Autonomous Penetration Testing Console"`
  - `html.title.text:"自主渗透测试控制台"`
  - `html.title.text:"자율 침투 테스트 콘솔"`
  - `html.title.text:"自律型ペネトレーションテストコンソール"`
  - `app.data.text:"LLM 驱动的自主渗透测试系统控制台"`
  - `app.data.text:"Console for the LLM-driven autonomous penetration testing system"`
  - `app.data.text:"An LLM-driven system console for autonomous penetration testing"`
  - `app.data.text:"LLM 기반으로 자율 침투 테스트를 수행하는 시스템 콘솔"`
  - `app.data.text:"Una consola de sistema impulsada por LLM para pruebas de penetración autónomas"`
  - `app.data.text:"LLM を活用して自律的にペネトレーションテストを行うシステムコンソール"`
  - `app.data.text:"AI 驱动的自主渗透测试平台"`
  - `app.data.text:"We are coming to root your server"`
- **CyberStrikeAI** · projeto: <https://github.com/AIPentest/CyberStrikeAI>
  - `app.device:"offensive agent"`
  - `html.title.raw:"CyberStrikeAI"`
  - `extract.url:"https://github.com/Ed1s0nZ/CyberStrikeAI"`
  - `app.data.text:"CyberStrikeAI Logo"`
  - `favicon.data.md5:7d794e98f48497b767fceb032ef28e3e`
  - `favicon.data.md5:8675aef8c3ffdbe15bb2638291887954`
- **PentAGI** · projeto: <https://github.com/vxcontrol/pentagi>
  - `html.title.text:"PentAGI"`
  - `cert.issuer.o:"PentAGI"`
  - `cert.issuer.cn:"PentAGI CA"`
  - `cert.subject.an:"pentagi.local"`
  - `favicon.data.md5:c7bf380529c43568d4bcad5e52c90c32`
- **RedAmon** · projeto: <https://github.com/samugit83/redamon>
  - `html.title.raw:"RedAmon"`
  - `favicon.data.md5:620b55364a1b370943ceeab58e1f49a3`
  - `favicon.data.md5:dca9c654ddce6aa63d1187c509a89345`
  - `app.data.text:"Security reconnaissance and vulnerability assessment dashboard"`
- **Cairn** · projeto: <https://github.com/oritera/Cairn>
  - `favicon.data.md5:46f7bbdd5796a334ba2f6999f0c6798a`
  - `app.data.text:"reasonBeaconPulse"`
  - `app.data.text:"/static/favicon.svg"`
  - `app.data.text:"cytoscape-elk.js"`
  - `html.title.raw:"Cairn"`
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
- **BugTraceAI** · projeto: <https://github.com/BugTraceAI/BugTraceAI>
  - `app.data.text:"BugTraceAI API"`
  - `html.title.raw:"BugTraceAI"`
- **Pentest-Swarm-AI** · projeto: <https://github.com/Armur-Ai/Pentest-Swarm-AI>
  - `html.title.text:"pentestswarm"`
  - `app.data.text:"pentestswarm"`

## C2 no mesmo IP

| Framework | IPs |
|---|--:|
| Vshell | 12 |
| Sliver | 6 |
| Mythic | 3 |
| Cobalt Strike | 3 |
| AdaptixC2 | 2 |
| Havoc | 1 |
| Supershell | 1 |
| Metasploit | 1 |

## Agentes no mesmo IP

| Par | IPs |
|---|--:|
| CyberStrikeAI + PentAGI | 249 |
| ARTEX + CyberStrikeAI | 147 |
| ARTEX + PentAGI | 37 |
| ARTEX + Strix | 7 |
| ARTEX + RedAmon | 5 |
| ARTEX + Cairn | 4 |
| PentAGI + Strix | 3 |
| CyberStrike + CyberStrikeAI | 3 |
| RedAmon + Strix | 2 |
| CyberStrikeAI + Xalgorix | 2 |

## Clusters (detalhe de build compartilhado, não atribuição)

| Cluster | Hosts | Registro |
|---|--:|---|
| [antifox](https://offensive.agency/cluster/antifox) | 494 | `TOOL-ANTIFOX` |
| [bob-research-labs](https://offensive.agency/cluster/bob-research-labs) | 154 | – |

## Países

| País | IPs |
|---|--:|
| US | 1771 |
| HK | 1012 |
| CN | 793 |
| SG | 207 |
| JP | 186 |
| FR | 158 |
| DE | 139 |
| IT | 112 |
| NL | 98 |
| KR | 81 |
| ID | 39 |
| FI | 33 |
| CA | 33 |
| GB | 30 |
| BR | 29 |
| IN | 27 |
| MY | 27 |
| TH | 26 |
| VN | 24 |
| PL | 18 |

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
