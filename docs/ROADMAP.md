# Roadmap

The goal is to make LLMInjection a **living AI cyber threat-intelligence platform**, not a static awesome-list.

## v0.1 — Intelligence foundation

- [x] evidence model and source grading;
- [x] framework crosswalk beyond MITRE ATLAS;
- [x] initial AI/APT threat actor tracker;
- [x] AI threat model;
- [x] model/architecture security matrix;
- [x] machine-readable actor/framework/technique data;
- [x] CI validation.

## v0.15 — AI / LLM Threat Landscape

- [x] 2026 evidence-driven threat landscape;
- [x] key-metric dataset with source/population/time-window context;
- [x] landscape domains: operator, enabler, prompt injection, agentic, supply chain, data exposure, cloud/identity, ransomware, model integrity;
- [x] sector signals;
- [x] notable-case status model (observed vs research vs unverified);
- [x] OWASP LLM Top 10 2026 update while preserving 2025 historical mappings;
- [x] curated AI-security GitHub ecosystem;
- [x] JSON schema and CI validation;
- [ ] recurring source-freshness checks;
- [ ] quarterly landscape snapshots / changelog;
- [ ] trend deltas between landscape releases.

## v0.2 — Structured intelligence

- [ ] STIX 2.1 export;
- [ ] relationships: actor → campaign → technique → model/tool → control;
- [ ] MITRE ATLAS + ATT&CK identifiers where defensible;
- [ ] CVE/GHSA/OSV references for AI supply-chain incidents;
- [ ] source deduplication and canonical URLs;
- [ ] changelog of confidence/attribution changes.

## v0.3 — Threat graph

- [ ] GraphML/JSON graph export;
- [ ] interactive GitHub Pages explorer;
- [ ] filters by actor, country/nexus, technique, model, framework and confidence;
- [ ] timeline view;
- [ ] source-evidence panel;
- [ ] "AI as target / enabler / operator / defense" graph layers.

## v0.4 — Detection engineering

- [ ] vendor-neutral analytics specification;
- [ ] Sigma;
- [ ] Sentinel KQL;
- [ ] Splunk SPL;
- [ ] Elastic ES|QL;
- [ ] Google SecOps YARA-L;
- [ ] detection-to-intel coverage matrix.

## v0.5 — Evaluation lab

- [ ] safe local test harness;
- [ ] benchmark adapters for garak / PyRIT / JailbreakBench;
- [ ] regression result schema;
- [ ] model/system version tracking;
- [ ] defense effectiveness matrix;
- [ ] agent/RAG/MCP test profiles.

## v0.6 — AI supply-chain intelligence

- [ ] model registry/hub incidents;
- [ ] malicious packages and gateways;
- [ ] CI/CD compromise cases;
- [ ] model/data provenance guidance;
- [ ] SBOM / AI-BOM mapping;
- [ ] OpenSSF / SLSA integration notes.

## v1.0 — Community CTI platform

- [ ] documented release process;
- [ ] signed data releases;
- [ ] contributor attribution;
- [ ] automated source freshness checks;
- [ ] stable schema;
- [ ] API-friendly published dataset;
- [ ] public methodology paper.

## North star

A security analyst should be able to start from any one of these:

- an APT;
- an AI model/runtime;
- a prompt-injection class;
- an OWASP risk;
- a MITRE technique;
- a supply-chain incident;

…and navigate to **evidence, related behaviors, controls and detections** without leaving the repository.
