<p align="center">
  <img src="assets/llminjection-banner.svg" alt="LLMInjection: panorama de ameaças a LLMs e sistemas agentivos" width="100%">
</p>

<!-- lang-bar -->
[English](README.md) · **Português** · [Español](README.es.md) · [简体中文](README.zh-CN.md) · [Русский](README.ru.md)
<!-- /lang-bar -->

> Tradução assistida por IA, ainda sem revisão de falante nativo. A versão em inglês é a referência. Para corrigir, veja [docs/TRANSLATIONS.md](docs/TRANSLATIONS.md).

Inteligência de ameaças aberta para sistemas de IA, LLMs e agentes: atores, campanhas, técnicas de ataque, casos de teste seguros, detecções e controles, ligados à evidência que sustenta cada afirmação.

**[Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/)** · [Documentação](docs/README.md) · [Panorama Brasil e América Latina](docs/pt-BR/PANORAMA-BRASIL-LATAM.md) · [Metodologia](docs/METHODOLOGY.md)

---

## Em números

<!-- gen:stats-pt:start -->
| Atores | Campanhas | Incidentes | Vulnerabilidades | Técnicas | Fontes |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **8** | **10** | **30** | **9** | **28** | **54** |

| Casos de teste | Detecções | Controles | Frameworks | Famílias de modelos | Relações | Projetos do ecossistema |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **40** | **45** | **32** | **19** | **12** | **215** | **106** |
<!-- gen:stats-pt:end -->

O LLMInjection **não é um repositório de prompts**. Cada afirmação relevante traz nota da fonte, nível de confiança, data de verificação, contexto de frameworks e um ângulo defensivo.

## O que há aqui

| Camada | O que contém | Comece por |
|---|---|---|
| **Atores e campanhas** | Operadores estatais e criminosos que usam IA, com os rótulos dos fornecedores mantidos como publicados | [`data/actors.json`](data/actors.json) |
| **Brasil e América Latina** | Uso de IA contra organizações da região, separando o que o relatório afirma do que ele não afirma | [Panorama](docs/pt-BR/PANORAMA-BRASIL-LATAM.md) |
| **Panorama de ameaças** | Métricas citadas, domínios e pistas de pesquisa de 2026 | [Landscape 2026](docs/THREAT-LANDSCAPE-2026.md) |
| **Técnicas e frameworks** | Técnicas mapeadas para ATLAS, OWASP, NIST, SAIF e MAESTRO, com nível de maturidade | [Frameworks](docs/FRAMEWORKS.md) |
| **Laboratório seguro** | Casos de teste defensivos para prompt, RAG, agentes, MCP e cadeia de suprimentos | [Casos de teste](docs/TEST-CASES.md) |
| **Detecção** | Hipóteses de detecção e regras Sigma de partida | [Engenharia de detecção](docs/DETECTION-ENGINEERING.md) |
| **Ecossistema** | Projetos relacionados, classificados pelo que cada um pode sustentar | [Mapa do ecossistema](docs/ECOSYSTEM.md) |

## Princípios

1. **Incidente observado, técnica demonstrada em pesquisa e exemplo de laboratório não se misturam.** Um repositório de jailbreaks pode inspirar um teste; nunca prova que um ator usou a técnica.
2. **Inferência não é confirmação.** Quando o uso de IA é deduzido de artefatos, o registro diz isso.
3. **Rótulos de fornecedores não são fundidos** em apelidos universais sem evidência.
4. **Maturidade vem do grafo.** Cada técnica é classificada como observada em campo, vulnerabilidade divulgada, demonstrada em pesquisa ou sem evidência ligada, e a validação impede que o campo se afaste dos dados.

## Início rápido

```bash
make check         # lint, testes, validação dos dados e auditoria do grafo
make build         # grafo, STIX, API estática, camadas do Navigator e gráficos
python scripts/query_intel.py search "prompt injection"
python scripts/osint_ioc.py relatorio.md --enrich    # extrai IOCs; enriquece CVEs com CISA KEV e EPSS
```

Python 3.12, somente biblioteca padrão.

## Contribuir

Contribuições úteis acrescentam **evidência, relações, testes, detecções ou correções**, não exagero. Leia [CONTRIBUTING.md](CONTRIBUTING.md), prefira fontes primárias, preserve a incerteza e rode `make check` antes de abrir um pull request.

## Licença

Apache-2.0. Veja [LICENSE](LICENSE).
