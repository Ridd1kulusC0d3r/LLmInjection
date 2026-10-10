# AI Threat Intelligence: data enrichment

Updated 2026-10-09. **These are complementary sources, not 32 newly validated incident feeds.**

## Added

- 19 additional previously uncatalogued public repositories in `data/ai-source-registry.json`; the core `data/ecosystem.json` is preserved until repository commit and licence verification.
- 32 source records in `data/ai-source-registry.json` with integration states, evidence classes and review requirements.
- An ontology of six overlapping AI threat dimensions: target, enabler, operator, supply chain, runtime identity, autonomous failure.
- A bounded, candidate-only enrichment pipeline (see `scripts/enrich_ai_sources.py`), separate from authoritative CTI data.

## Live adapter scope

| Adapter | What is imported | What is not claimed |
| --- | --- | --- |
| AVID reports | Path/URL metadata for JSON reports | Independent incident verification |
| Independent VERIS collection | Secondary report ID and title | Primary-source evidence or confirmed breach |
| MCP Registry | Published server listing metadata | Server safety, maliciousness or actual deployment |
| OSV local | OSV records for CVE/GHSA identifiers already present | New confirmed impact on an unknown version |
| CVE repository changes | Latest official repository commit IDs | That a changed commit is AI-specific |
| Inspect Evals changes | New research repository commits | Real-world attack incidence |

AIID GraphQL, VCDB, NVD, EPSS, vendor reports, full CVE deltas and telemetry are **catalogued for later connectors**, not silently scraped.

## Evidence policy

The pipeline writes only `data/enrichment-review-queue.json`. Human review is required to promote candidates into `data/incidents.json`, `data/vulnerabilities.json` or other canonical datasets. Preserve source identifier, URL, discovered date, original publication and occurrence dates separately, evidence fingerprint, source grade and analytic confidence. Resolve aliases without collapsing distinct events. Review rights and licenses before copying upstream records. 

## Run

Offline: `python scripts/enrich_ai_sources.py --fixture tests/fixtures/ai-source-responses.json --dry-run`

Live: `python scripts/enrich_ai_sources.py --live --max-per-source 20`

No external source code is executed. The collector uses explicit HTTPS allow-listed hosts, bounded responses and review-only output. The scheduled workflow opens a review PR but cannot create actors, incidents, relations or vulnerability records.

## Documentation and primary sources

- AVID: https://github.com/avidml/avid-db
- OSV: https://google.github.io/osv.dev/post-v1-query/
- CVE JSON 5: https://github.com/CVEProject/cvelistV5
- MCP Registry: https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/openapi.yaml
- OpenTelemetry GenAI: https://github.com/open-telemetry/semantic-conventions-genai
- FIRST EPSS: https://www.first.org/epss/

## Next engineering gates

Real AIID GraphQL pagination, CVE JSON records with package/version inventory, incremental MCP cursors, EPSS time series, sanitized OpenTelemetry trace ingestion, rights-aware vendor RSS, benchmark adapters, interactive Explorer views, and crosswalks into the official evidence graph remain follow-on deliverables. These must be tested with source fixtures and cannot be treated as completed merely because the source has been catalogued.
