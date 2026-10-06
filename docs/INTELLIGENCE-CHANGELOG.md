# Intelligence Changelog

This changelog records material changes to attribution, confidence, external mappings and structured intelligence. Ordinary prose edits do not belong here.

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
