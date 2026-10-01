# Intelligence Changelog

This changelog records material changes to attribution, confidence, external mappings and structured intelligence. Ordinary prose edits do not belong here.

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
