# Intelligence Changelog

This changelog records material changes to attribution, confidence, external mappings and structured intelligence. Ordinary prose edits do not belong here.

## 2026-10-09 — Coverage depth and benchmark sources

### Added

- `scripts/coverage_model.py` derives, from the datasets and the files in `detections/`: per-detection implementation (rule file or specification), distinct publishers and best grade per technique, newest evidence date with a stale flag, mapped benchmarks, actors reached through campaigns, and a priority score with a documented formula;
- Explorer Coverage tab: sortable columns, eight filters, row drill-down to the linked records, an actor-by-technique view, URL state (`sort`, `dir`, `show`, `view`) and a richer CSV;
- coverage matrix SVG: a benchmark column, a marker for techniques that have a detection rule file, and a summary line stating that only 3 of 45 detections are rule files;
- eight ecosystem entries (InjecAgent, PurpleLlama, Inspect Evals, SORRY-Bench, StrongREJECT, CTIBench, Cybench, WildTeaming), each cloned and read; three release feeds (PurpleLlama, Inspect Evals, promptfoo); [docs/BENCHMARKS.md](BENCHMARKS.md).

- `scripts/osint_ecosystem.py` and `data/ecosystem-osint.json`: for 64 of the 114 ecosystem entries, stars, forks, open issues, the packages published from the repository, OSV advisories per package and whether a release carries verified SLSA provenance (deps.dev and OSV.dev, no token). 50 entries are unknown to deps.dev. Summary: [docs/ECOSYSTEM-SIGNALS.md](ECOSYSTEM-SIGNALS.md).

### Changed

- the matrix headline now reads "covered by design" instead of "fully covered", because a detection that is a specification counted the same as a working rule.

### Confidence notes

- The new ecosystem entries are grade D and map to techniques only where the project's README states the attack class. CTIBench measures AI for CTI tasks and Cybench measures agent capability; neither is evidence of attacker behaviour.
- The reference date for freshness is the newest day-precision date in the evidence (a bare year such as "2026" is ignored for that purpose).

## 2026-10-08 — Explorer languages and accessibility

### Added

- Explorer interface in English, Portuguese, Spanish, Simplified Chinese and Russian (`site/i18n/*.json`, runtime in `site/i18n.js`), a language selector in the masthead, `#lang=<code>` links, and a Languages tab listing what is and is not translated;
- READMEs in Spanish, Simplified Chinese and Russian, the Latin America regional overview in Spanish, and `docs/TRANSLATIONS.md` with a glossary generated from the Explorer dictionaries;
- tests for dictionary parity, placeholders, used-versus-defined keys, Chinese punctuation, WCAG contrast of the colour tokens, the translation manifest and the README language bars.

### Fixed in the Explorer

- keyboard access: tabs now follow the ARIA tab pattern with arrow keys, the 287 graph nodes are one tab stop with arrow-key movement, coverage rows and cards open with Enter, the record drawer takes and returns focus and traps Tab, and a skip link was added;
- phones: Landscape, Coverage, Ecosystem and Timeline overflowed horizontally (up to 274 px); tables now scroll inside their container;
- search ignores accents and case; CSV exports start with a byte-order mark so Excel reads accents and non-Latin text;
- contrast: the small grey labels and the mid heat-map cells were below 4.5:1 in the light theme, and the small grey labels were below it in the dark theme;
- the changes panel showed "vulnerabilitie" for vulnerability records;
- the Ecosystem tab still said repository state was not independently verified, which stopped being true after the ecosystem sweep.

### Confidence notes

- Every translation is machine-assisted and awaiting native-speaker review. Record content (names, summaries, source titles) stays in English by design.

## 2026-10-07 — Merge with the ecosystem sweep

The ecosystem sweep (107 repositories read, ATLAS 2026.09 crosswalk) and this branch were developed in parallel and both created techniques T020 to T023 and detections DET-AI-015 to DET-AI-020. Resolution:

- the sweep's IDs are kept as published; this branch's equivalents were unified where they meant the same thing (improper output handling is T020, resource exhaustion and cost harvesting is T022) and renumbered where they did not: unsanctioned AI runtime is now LLMI-T027, AI-assisted tooling development LLMI-T028, detections DET-AI-040 to DET-AI-045 and tests TC-JB-035 to TC-TOOL-040;
- maturity was recomputed for all 28 techniques from the merged graph;
- the two ecosystem verifiers were reconciled: `scripts/verify_ecosystem.py` (git, no token) records reachability, last commit and licence; `scripts/check_ecosystem.py` (API) adds only the archive flag and renames to the same `verification` block.

## 2026-10-07 — Latin America, closed coverage gaps and technique maturity

### Added

- Latin America: actor BREEZE COMET; campaigns BREEZE-COMET-PAYMENTS, SHADOW-AETHER-040 and CL-CRI-1131 from Google/Mandiant, Trend Micro and Unit 42 primary reports; four sources; technique LLMI-T028 (AI-assisted tooling development); control CTRL-EXEC-POLICY; landscape domain and four research-queue leads; `regions` field; Portuguese regional document and README;
- coverage: tests TC-JB-035 to TC-TOOL-040 and detections DET-AI-040 to DET-AI-045, so every technique now has a test and a detection; INCIDENT-GTIG-DISTILLATION links the distillation technique to observed activity;
- technique `maturity` field, derived from the graph by `scripts/maturity.py` and enforced by the validator; level `no-linked-evidence` replaces the misleading word theoretical;
- dates: `published` on sources, `reported` on campaigns and incidents; the validator checks `reported` equals the earliest source date and rejects a record first seen after its primary report;
- ATT&CK Navigator layer export, ecosystem verification script and weekly workflow, release feeds for garak, PyRIT and AgentDojo, T018 external mappings.

### Corrected

- CAMPAIGN-GTG1002-AI-ESPIONAGE first_seen set to 2025-09: Anthropic reports detection in mid-September 2025 and published on 2025-11-13, not in 2026;
- CAMPAIGN-APT28-PROMPTSTEAL first_seen set to 2025: GTIG reported it on 2025-11-05.

### Confidence notes

- In all three Latin America campaigns the AI use is inferred or reported by one vendor; the records say so and no model is asserted except where Trend reports it with high confidence from leaked conversations.
- Press-reported overlaps (for example CL-CRI-1163 with BREEZE COMET) are noted in summaries, not merged as aliases. Google's own reported overlaps (Plump Spider, SHADOW-AETHER-064) are likewise not merged.
- Not done: external ATLAS and OWASP IDs for LLMI-T027 and LLMI-T028. The ATLAS technique pages were unreachable (HTTP 404) from this environment, so those mappings are left empty rather than guessed. The ecosystem verification script was tested with fixtures but not run against GitHub from this environment.

## 2026-10-07 — Graph audit, taxonomy completion and Explorer dashboard

### Added

- technique LLMI-T027 (unsanctioned AI runtime), and links tying existing tests and detections for improper output handling and resource exhaustion to the techniques now named LLMI-T020 and LLMI-T022, so those risks have a taxonomy home;
- seventeen relationships linking six previously unlinked test cases, five detections and four controls to techniques;
- `scripts/audit_graph.py`: fails CI on test cases, detections or controls linked to nothing, and lists techniques without a test or detection;
- charts: coverage matrix extended with evidence and tool columns and a priority-gap flag; new framework-mapping and ecosystem-map charts;
- Explorer: dashboard on the main screen, ecosystem tab, extended coverage table and structured record view;
- repository tooling: ruff configuration, `make check`, dependabot, CODEOWNERS and two issue forms.

### Confidence notes

- The new relationships are the maintainer's analytic links. They use medium or high confidence and cite the nearest supporting source; none asserts observed activity.
- LLMI-T027 carries no external framework mapping yet. IDs will be added from the primary framework data rather than guessed.

## 2026-10-07 — Ecosystem map

### Added

- `data/ecosystem.json`: 75 related GitHub projects with an evidence class, section, priority and technique mapping, plus a schema and validator rules;
- `docs/ECOSYSTEM.md`: generated tables by section, evidence-class definitions and the rule that these entries never support attribution or campaign claims;
- ten entries flagged `start-here` (ATLAS Data, Arcanum taxonomy, PLOT4ai, Agent Threat Rules, prompt-injection-defenses, AgentDojo, PyRIT, garak, AIID, awesome-llm-supply-chain-security).

### Confidence notes

- The list is the maintainer's own research. Repository state, including three entries recorded as archived (BIPIA, rebuff, llm-guard), is as reported and was not independently verified.
- Source grades follow the publisher: A for the MITRE and OWASP projects, D for everything else. A grade describes the repository as a source of claims, not the quality of the tool.
- Technique mappings are made only where the project's stated scope clearly matches; many entries have none.

## 2026-10-07 — Defensive coverage for the 2026-10-06 techniques

### Added

- five safe test cases: TC-SCAN-016, TC-WS-017, TC-DIST-018, TC-PARAM-019, TC-GW-020;
- four detection hypotheses: DET-AI-011 to DET-AI-014, plus a Sigma starter rule for DET-AI-011;
- DET-AI-006 (AI gateway credential anomaly) now has a test, TC-GW-020, closing a documented gap;
- eleven relationships linking the new tests and detections to techniques;
- README attack-chain diagrams and a defender playbook.

### Open gaps

- DET-AI-012 (CI token read from runner memory) has a hypothesis but no safe simulation yet.
- The new tests and detections are specifications. None has been exercised against a production telemetry source.

## 2026-10-06 — Agent workspace, MCP transport and autonomy update

### Added

- GTIG "From Prompting to Autonomy" (2026-09-08): DUSTMAKER incident, sub-six-hour multi-agent credential harvest incident, three landscape metrics (6 h, 100M+ distillation prompts, 23,800+ secrets);
- Microsoft Semantic Kernel CVE-2026-26030 and CVE-2026-25592 (prompt injection reaching eval() and file helpers);
- OX Security MCP STDIO command-injection record (only CVE-2026-30623 and CVE-2026-30615 listed; vendor dispute noted);
- techniques LLMI-T017 (prompt injection against AI security scanners), LLMI-T018 (AI coding-assistant workspace abuse), LLMI-T019 (model distillation campaign);
- landscape domains LANDSCAPE-DEVTOOL-WORKSPACE and LANDSCAPE-MCP-TRANSPORT; 12 new evidence-backed relationships.

### Confidence notes

- Anthropic's September 2026 report is held in the research queue (grade C press coverage only) until the primary document is attached; no new actors were promoted from it.
- OX Security's remaining CVE identifiers were not cross-checked and are queued as unverified.
- New techniques carry no external framework mapping yet rather than an unsupported one.

## 2026-09-30 — Initial structured baseline

### Added

- AI / LLM Threat Landscape 2026 baseline;
- seven tracked actor records;
- seven normalized campaign records;
- five incident / research-case records;
- sixteen LLMInjection techniques;
- exact/related MITRE ATLAS, ATT&CK and OWASP external mappings where defensible;
- six CVE/GHSA/malicious-package vulnerability records;
- ten detection hypotheses;
- twenty defensive controls;
- canonical source registry;
- evidence-backed relationship graph;
- safe adversarial test catalog.

### Attribution notes

- GTG-1002 remains the vendor tracking label used by Anthropic in the cited campaign reporting.
- APT28 / FROZENLAKE is mapped only where the cited Google reporting supports the relationship.
- Famous Chollima / Shifty Corsair is not silently merged with unrelated DPRK tracking labels.
- TeamPCP remains unattributed in the actor dataset.

### Confidence notes

- CLOSEDQUORUM is preserved as a research-significant autonomous AI C2 artifact, **not** a confirmed in-the-wild deployment.
- Promptware Kill Chain is represented as a research framework, not an observed campaign.
- Claims without sufficient primary sourcing remain in the threat-landscape research queue rather than being promoted.

### Framework/version notes

- OWASP LLM Top 10 2026 is the current application-risk reference.
- OWASP LLM Top 10 2025 is preserved for historical mapping.
- External technique mappings distinguish `exact` from `related`.
- MCP Security Best Practices, OWASP ACS, CSA AICM v1.1, CycloneDX AI/ML-BOM and SLSA v1.2 were added to the reference/control stack.

## Change policy

Future entries should record any change that affects how a consumer interprets the data, especially:

- actor alias or nexus change;
- campaign attribution change;
- confidence increase/decrease;
- source replacement or retraction;
- external technique-ID change;
- vulnerability affected/fixed-version correction;
- schema-breaking change.

Historical assessments should be corrected transparently rather than silently rewritten.
