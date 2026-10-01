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
- [ ] quarterly snapshot automation
- [ ] automated trend-delta reports

## v0.2 — Structured intelligence ✅ foundation

- [x] campaigns, incidents, controls, detections and source registry
- [x] explicit relationship graph with confidence/evidence
- [x] STIX 2.1 export
- [x] canonical source IDs
- [x] referential-integrity CI
- [ ] exact MITRE ATLAS + ATT&CK IDs for every defensible technique
- [ ] CVE/GHSA/OSV enrichment for applicable supply-chain incidents
- [ ] attribution/confidence changelog

## v0.3 — Threat graph ✅ foundation

- [x] Graph JSON export
- [x] GraphML export
- [x] interactive GitHub Pages explorer
- [x] actor / campaign / technique / model / source navigation
- [x] computed technique coverage view
- [x] timeline view
- [x] evidence detail drawer
- [ ] larger-graph clustering and layout optimization
- [ ] quarter-over-quarter landscape comparison

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
- [ ] automated OSV/GHSA enrichment
- [ ] signed release manifests
- [ ] generated AI/ML-BOM for LLMInjection releases

## v1.0 — Community CTI platform

- [x] API-friendly JSON datasets
- [x] graph/STIX/GraphML generation
- [x] interactive public explorer workflow
- [x] source freshness checks
- [ ] versioned signed data releases
- [ ] stable schema guarantee
- [ ] contributor attribution ledger
- [ ] TAXII publishing endpoint
- [ ] public methodology paper

## North star

An analyst should be able to start from:

```text
Actor / Model / Prompt Injection / MCP / OWASP risk / Supply-chain incident
                              ↓
Evidence → Campaign → Technique → Test → Detection → Control → Framework
```

…and move through the chain without leaving the project.
