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

## v1.2 — Ecosystem intelligence 🟡 sweep 2026-10-07

- [x] Clone-verify every ecosystem repository; record last commit and licence (`scripts/verify_ecosystem.py`)
- [x] MITRE ATLAS 2026.09 crosswalk with gap list (`references/crosswalks/atlas-crosswalk.json`)
- [x] Seven techniques (T020–T026), 14 tests, 25 detections, 11 controls, 22 ATLAS case studies
- [ ] Promote research-queue candidates (47) after clone-and-classify review
- [ ] Re-verify OWASP `LLMxx:2026` and `ASIxx` IDs against `GenAI-Security-Project/GenAI-LLM-Top10`
- [ ] Test cases for training-data exposure, fine-tune poisoning and dev-time model theft (OWASP AITG DAT-01, INF-05, INF-06)
- [ ] Decide on held-back technique candidates: approval-gate subversion, tool-argument injection, MCP protocol abuse
- [ ] Write rule files (Sigma / KQL) for the highest-severity new specifications (DET-AI-022, 027, 028, 029, 031)

## North star

An analyst should be able to start from:

```text
Actor / Model / Prompt Injection / MCP / OWASP risk / Supply-chain incident
                              ↓
Evidence → Campaign → Technique → Test → Detection → Control → Framework
```

…and move through the chain without leaving the project.

## v1.3 — Evidence levels, regional lens and tooling 🟡 2026-10-07

- [x] Close every technique coverage gap: each technique has a safe test and a detection; `scripts/audit_graph.py` keeps it that way
- [x] Derived `maturity` field on techniques, enforced by the validator
- [x] Weekly ecosystem verification workflow combining the git check and the GitHub API check (not yet run on GitHub)
- [x] ATT&CK Navigator layer export (`scripts/build_navigator.py`)
- [x] Brazil and Latin America lens in Portuguese, linked to actor and campaign records
- [x] Source `published` and record `reported` dates, with validator checks
- [x] Explorer: deep links, CSV export, region filter, maturity and dashboard
- [ ] External ATLAS and OWASP IDs for LLMI-T027 and LLMI-T028 (the ATLAS technique pages were unreachable from the authoring environment)
- [ ] Link observed prompt-injection incidents to LLMI-T001 and LLMI-T002 so their maturity reflects the evidence
- [ ] Verify the Navigator layer's ATLAS `domain` value against an ATLAS-aware Navigator build
- [ ] Primary reports for the Brazil leads in the research queue (Zscaler, Serasa, Banco Central)
- [ ] Evaluate SHADOW-AETHER-064 as its own record once the overlap with BREEZE COMET is resolved

## v1.4 — Languages 🟡 2026-10-08

- [x] Explorer interface in English, Portuguese, Spanish, Simplified Chinese and Russian
- [x] READMEs in the four additional languages; regional overview in Spanish and Portuguese
- [x] Keyboard, focus, contrast and phone-layout fixes found in an audit of the Explorer
- [ ] Native-speaker review of the Portuguese, Spanish, Chinese and Russian translations
- [ ] Regional overview in Chinese and Russian (not planned until there is regional evidence relevant to those readers)
- [ ] Right-to-left layout, if an Arabic or Hebrew translation is contributed
- [ ] Automate the Explorer preview image (it is a manual screenshot today and goes stale)


## v1.5 — Coverage depth 🟡 2026-10-09

- [x] Derived coverage model (`scripts/coverage_model.py`): rule-file versus specification, distinct publishers, best grade, evidence freshness, benchmarks, actors, explicit priority formula
- [x] Explorer Coverage tab: sortable, filterable, drill-down to the linked records, actor-by-technique view, state in the URL, CSV with the new columns
- [x] Coverage matrix SVG with a benchmark column and a marker for rule files; the README image links to the live tab
- [x] Eight verified benchmark and evaluation projects; three new release feeds ([BENCHMARKS.md](BENCHMARKS.md))
- [x] Keyless OSINT signals for the ecosystem (`scripts/osint_ecosystem.py`): stars, published packages, OSV advisories and verified SLSA provenance, weekly in the verification workflow
- [ ] Show the signals in the Explorer's Ecosystem tab
- [ ] OpenSSF Scorecard scores (deps.dev returned none for the projects tried, and the Scorecard API returned 404)
- [x] First Sigma drafts through Feedly's `create-sigma-rule` method: DET-AI-032 and DET-AI-029 ([SIGMA-DRAFTS.md](SIGMA-DRAFTS.md))
- [ ] Rule files for the 40 detections that are still specifications; most have no Sigma logsource (agent and model-pipeline telemetry)
- [ ] A safe test for DET-AI-029, which has none
- [ ] Execute safe tests and record `lab-result` files, so a cell can say "tested" and not only "designed"
- [ ] Link observed prompt-injection incidents to LLMI-T001 (it has no linked evidence today)
- [ ] More than one publisher for the 14 techniques that rest on a single one
- [ ] Per-technique history (how coverage changed between snapshots)
