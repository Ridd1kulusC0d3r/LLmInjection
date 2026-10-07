# Intelligence Changelog

This changelog records material changes to attribution, confidence, external mappings and structured intelligence. Ordinary prose edits do not belong here.

## 2026-10-07 — Latin America, closed coverage gaps and technique maturity

### Added

- Latin America: actor BREEZE COMET; campaigns BREEZE-COMET-PAYMENTS, SHADOW-AETHER-040 and CL-CRI-1131 from Google/Mandiant, Trend Micro and Unit 42 primary reports; four sources; technique LLMI-T023 (AI-assisted tooling development); control CTRL-EXEC-POLICY; landscape domain and four research-queue leads; `regions` field; Portuguese regional document and README;
- coverage: tests TC-JB-021 to TC-TOOL-026 and detections DET-AI-015 to DET-AI-020, so every technique now has a test and a detection; INCIDENT-GTIG-DISTILLATION links the distillation technique to observed activity;
- technique `maturity` field, derived from the graph by `scripts/maturity.py` and enforced by the validator; level `no-linked-evidence` replaces the misleading word theoretical;
- dates: `published` on sources, `reported` on campaigns and incidents; the validator checks `reported` equals the earliest source date and rejects a record first seen after its primary report;
- ATT&CK Navigator layer export, ecosystem verification script and weekly workflow, release feeds for garak, PyRIT and AgentDojo, T018 external mappings.

### Corrected

- CAMPAIGN-GTG1002-AI-ESPIONAGE first_seen set to 2025-09: Anthropic reports detection in mid-September 2025 and published on 2025-11-13, not in 2026;
- CAMPAIGN-APT28-PROMPTSTEAL first_seen set to 2025: GTIG reported it on 2025-11-05.

### Confidence notes

- In all three Latin America campaigns the AI use is inferred or reported by one vendor; the records say so and no model is asserted except where Trend reports it with high confidence from leaked conversations.
- Press-reported overlaps (for example CL-CRI-1163 with BREEZE COMET) are noted in summaries, not merged as aliases. Google's own reported overlaps (Plump Spider, SHADOW-AETHER-064) are likewise not merged.
- Not done: external ATLAS and OWASP IDs for T017 and T019 to T023. The ATLAS technique pages were unreachable (HTTP 404) from this environment, so those mappings are left empty rather than guessed. The ecosystem verification script was tested with fixtures but not run against GitHub from this environment.

## 2026-10-07 — Graph audit, taxonomy completion and Explorer dashboard

### Added

- techniques LLMI-T020 (improper output handling), LLMI-T021 (resource exhaustion and cost abuse), LLMI-T022 (unsanctioned AI runtime), covering risks that existing tests and detections already addressed but the taxonomy did not name;
- seventeen relationships linking six previously unlinked test cases, five detections and four controls to techniques;
- `scripts/audit_graph.py`: fails CI on test cases, detections or controls linked to nothing, and lists techniques without a test or detection;
- charts: coverage matrix extended with evidence and tool columns and a priority-gap flag; new framework-mapping and ecosystem-map charts;
- Explorer: dashboard on the main screen, ecosystem tab, extended coverage table and structured record view;
- repository tooling: ruff configuration, `make check`, dependabot, CODEOWNERS and two issue forms.

### Confidence notes

- The new relationships are the maintainer's analytic links. They use medium or high confidence and cite the nearest supporting source; none asserts observed activity.
- LLMI-T020 to T022 carry no external framework mapping yet. IDs will be added from the primary framework data rather than guessed.

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
