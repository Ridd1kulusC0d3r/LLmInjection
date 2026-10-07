# Roadmap

The goal is a **living AI cyber threat-intelligence platform**, not a static awesome-list.

## v0.1 — Intelligence foundation ✅

- [x] evidence model and source grading
- [x] framework crosswalk
- [x] actor tracker
- [x] AI threat model
- [x] model security matrix
- [x] structured data and CI

## v0.15 — AI / LLM Threat Landscape ✅

- [x] evidence-driven 2026 landscape
- [x] sourced metrics with population/time-window context
- [x] sector signals and notable-case status
- [x] OWASP LLM 2026 with 2025 historical preservation
- [x] curated ecosystem and reference library
- [x] weekly source-freshness workflow
- [x] monthly snapshot automation
- [x] automated entity-level trend/delta reports

## v0.2 — Structured intelligence ✅ foundation

- [x] campaigns, incidents, controls, detections and source registry
- [x] explicit relationship graph with confidence/evidence
- [x] STIX 2.1 export
- [x] canonical source IDs
- [x] referential-integrity CI
- [x] exact/related MITRE ATLAS + ATT&CK + OWASP IDs where defensible
- [x] initial CVE/GHSA/OSV enrichment for applicable AI/supply-chain incidents
- [x] attribution/confidence changelog

## v0.3 — Threat graph ✅ foundation

- [x] Graph JSON export
- [x] GraphML export
- [x] interactive GitHub Pages explorer
- [x] actor / campaign / technique / model / source navigation
- [x] computed technique coverage view
- [x] timeline view
- [x] evidence detail drawer
- [ ] larger-graph clustering and layout optimization
- [x] snapshot-to-snapshot landscape comparison foundation

## v0.4 — Detection engineering 🟡 starter pack

- [x] vendor-neutral detection catalog
- [x] Sigma starter analytic
- [x] Sentinel KQL starter analytic
- [x] Splunk SPL starter analytic
- [x] Elastic ES|QL starter analytic
- [x] Google SecOps YARA-L starter analytic
- [x] detection-to-test coverage matrix
- [ ] implementation for all detection IDs across all engines
- [ ] sample normalized telemetry fixtures

## v0.5 — Evaluation lab 🟡 safe foundation

- [x] safe local test runner
- [x] prompt / RAG / agent / MCP / supply-chain / detection profiles
- [x] result schema
- [x] deterministic mock-secure and mock-insecure adapters for CI plumbing
- [ ] PyRIT adapter
- [ ] garak adapter
- [ ] JailbreakBench-style adapter
- [ ] local model endpoint adapter
- [ ] defense effectiveness reporting across system versions

## v0.6 — AI supply-chain intelligence 🟡 foundation

- [x] supply-chain incident objects
- [x] AI gateway and malicious-package threat relationships
- [x] model/data provenance guidance
- [x] AI/ML-BOM guidance
- [x] artifact pinning/signature/dependency controls
- [x] CycloneDX and Sigstore references
- [x] review-gated GitHub advisory / malicious-package intake
- [x] provenance-attested release archives with SHA-256
- [ ] generated AI/ML-BOM for LLMInjection releases

## v1.0 — Community CTI platform

- [x] API-friendly JSON datasets
- [x] versioned static JSON API builder
- [x] graph/STIX/GraphML generation
- [x] interactive public explorer workflow
- [x] source freshness checks
- [x] versioned dataset manifest
- [x] provenance-attested tagged data-release pipeline
- [x] contributor attribution ledger
- [x] public methodology
- [ ] promote schema from beta to stable guarantee
- [ ] TAXII publishing endpoint

## v1.1 — Living intelligence pipeline ✅ foundation

- [x] allow-listed machine-readable source registry
- [x] daily MITRE ATLAS / OWASP / MCP / GitHub Advisory / CISA KEV intake
- [x] research queue with deduplication and review state
- [x] transparent relevance scoring
- [x] ATLAS release-note extraction for new techniques, mitigations and case studies
- [x] monthly deterministic snapshots
- [x] entity-level added / removed / changed diff
- [x] monthly threat-landscape report generator
- [x] review-only automation PRs; no auto-promotion
- [x] Explorer What's New view
- [x] current MITRE ATLAS v2026.09 source tracking
- [x] LLMI-T015 → AML.T0124 Autonomous Attack Orchestration exact mapping
- [ ] RSS / Atom vendor-threat-research feed adapters
- [ ] automated duplicate clustering across vendor naming
- [ ] analyst promotion helper that generates candidate object patches
- [ ] stateful TAXII service
- [x] read-only MCP v2 intelligence server

## North star

An analyst should be able to start from:

```text
Actor / Model / Prompt Injection / MCP / OWASP risk / Supply-chain incident
                              ↓
Evidence → Campaign → Technique → Test → Detection → Control → Framework
```

…and move through the chain without leaving the project.

## Proposed next (2026-10-07)

1. **Close the coverage gaps** reported by `python scripts/audit_graph.py`, starting with the priority gaps: a safe test for CI identity-token theft (LLMI-T011) and detections for agentic attack orchestration (LLMI-T015).
2. **Add a maturity field to techniques** (`observed-in-the-wild`, `incident`, `research-demonstrated`, `theoretical`) so the data model carries the same distinction the ecosystem map enforces.
3. **Verify the ecosystem automatically**: a scheduled job that checks each listed repository's archived flag and last activity through the GitHub API, plus release feeds for the start-here tools.
4. **Export an ATT&CK Navigator and ATLAS layer** from the coverage data so SOC teams can overlay it on their own view.
5. **Fill external mappings** for LLMI-T017 to T022 from the primary ATLAS and OWASP data.
6. **Brazil and LATAM lens**: a regional view of AI-enabled activity, in Portuguese, linked to the existing actor and campaign records.

