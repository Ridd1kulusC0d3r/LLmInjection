<p align="center">
  <img src="assets/llminjection-banner.svg" alt="LLMInjection: threat landscape for LLM and agentic systems" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Ridd1kulusC0d3r/LLmInjection/actions/workflows/validate-intel.yml"><img src="https://img.shields.io/github/actions/workflow/status/Ridd1kulusC0d3r/LLmInjection/validate-intel.yml?style=flat-square&label=intel%20CI&labelColor=17150f&color=b43c0e" alt="Intel CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Ridd1kulusC0d3r/LLmInjection?style=flat-square&labelColor=17150f&color=4a463c" alt="Apache-2.0"></a>
  <img src="https://img.shields.io/badge/mode-defensive--first-4a463c?style=flat-square&labelColor=17150f" alt="Defensive first">
</p>

Open threat intelligence for AI, LLM and agentic systems: actors, campaigns, attack techniques, safe test cases, detections and controls, linked to the evidence behind each claim.

**[Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/)** · [Documentation](docs/README.md) · [Methodology](docs/METHODOLOGY.md) · [API](docs/PUBLISHING.md) · [Roadmap](docs/ROADMAP.md)

---

## At a glance

<!-- stats:start -->
| Actors | Campaigns | Incidents | Vulnerabilities | Techniques | Sources |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **7** | **7** | **7** | **9** | **19** | **40** |

| Test cases | Detections | Controls | Frameworks | Model families | Relationships |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **15** | **10** | **20** | **19** | **12** | **64** |
<!-- stats:end -->

LLMInjection is **not a prompt dump**. Every meaningful claim carries a source grade, a confidence level, a last-verified date, framework context and a defensive angle.

<img src="assets/coverage-matrix.svg" alt="Technique coverage matrix: tests, detections and controls per technique" width="100%">

<sub>Rows flagged *no test* or *no detection* are the open work. Regenerate with `make charts`.</sub>

## What is inside

| Layer | What it holds | Start here |
|---|---|---|
| **Actors and campaigns** | State and criminal operators using AI, with vendor tracking labels kept as published | [`data/actors.json`](data/actors.json) · [Actor tracker](docs/ACTOR-TRACKER.md) |
| **Threat landscape** | Cited metrics, domains and open research leads for 2026 | [Landscape 2026](docs/THREAT-LANDSCAPE-2026.md) |
| **Techniques and frameworks** | LLMInjection techniques mapped to ATLAS, OWASP, NIST, SAIF and MAESTRO | [Frameworks](docs/FRAMEWORKS.md) · [Threat model](docs/AI-THREAT-MODEL.md) |
| **Safe test lab** | Defensive test cases for prompt, RAG, agent, MCP and supply-chain risks | [Test cases](docs/TEST-CASES.md) · [Lab](docs/LAB.md) |
| **Detection engineering** | Sigma, KQL, SPL, ES\|QL and YARA-L starter detections | [Detection engineering](docs/DETECTION-ENGINEERING.md) |
| **Evidence** | Graded sources and explicit relationships behind every record | [Source grading](docs/SOURCE-GRADING.md) · [Methodology](docs/METHODOLOGY.md) |

Exports: `graph.json`, GraphML, STIX 2.1, a static `/api/v1/` JSON API, monthly snapshots with entity-level diffs, and an interactive [Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/).

## Quick start

```bash
make test          # unit tests
make validate      # schema and referential checks on all datasets
make build         # graph, STIX, static API, charts
python scripts/query_intel.py search "prompt injection"
python scripts/query_intel.py coverage LLMI-T015
```

Python 3.12, standard library only. The optional MCP server in [`integrations/mcp`](integrations/mcp/README.md) needs its own `requirements.txt`.

## How intelligence gets in

```text
feeds ─► collector ─► research queue ─► analyst review ─► datasets ─► graph / STIX / API ─► snapshot + diff
 ATLAS      daily        candidates         human           JSON         exports            monthly
 OWASP
 MCP
 GHSA
```

The collector **cannot** create attribution, incidents, CVE relationships or framework mappings. It only proposes candidates. Details: [Living intelligence](docs/LIVING-INTELLIGENCE.md).

### OSINT indicator extractor

```bash
python scripts/osint_ioc.py report.md
python scripts/osint_ioc.py --url https://example.com/post --enrich   # adds CISA KEV and EPSS for CVEs
```

Re-fangs `hxxp` and `[.]`, drops private IPs and noisy domains, and extracts CVE/GHSA/ATLAS/OWASP IDs, hashes, npm and PyPI install lures and prompt-injection signals (hidden comments, invisible Unicode, markdown-image exfiltration). Output feeds the review queue, never the datasets directly.

## Repository layout

```text
data/          structured intelligence (JSON), monthly snapshots
schemas/       JSON Schemas for every dataset
scripts/       validation, graph/API/STIX builds, intake, queries, safe lab
detections/    Sigma, KQL, SPL, ES|QL and YARA-L rules
docs/          methodology, handbooks and the full overview (docs/README.md is the index)
site/          Explorer (GitHub Pages)
integrations/  read-only MCP server
references/    curated external reading and tooling
tests/         unit tests and fixtures
assets/        banner and generated charts
```

## Documentation

Full index in **[docs/README.md](docs/README.md)**. The long-form tour that used to live in this file is [docs/OVERVIEW.md](docs/OVERVIEW.md).

## Contributing

Useful contributions add **evidence, relationships, tests, detections or corrections**, not hype. Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [methodology](docs/METHODOLOGY.md), prefer primary sources, preserve uncertainty, and run `make test validate` before opening a pull request.

LLMInjection is built for defenders, threat analysts, AI red teams, detection engineers and security architects. Offensive behavior is documented to support threat modeling and authorized evaluation, not turnkey abuse. Security reports: [SECURITY.md](SECURITY.md).

## License

Apache-2.0. See [LICENSE](LICENSE). Citation metadata: [CITATION.cff](CITATION.cff).

<p align="center"><sub><strong>Evidence over hype. Behavior over branding. Controls over vibes.</strong></sub></p>
