# LLMInjection Methodology

LLMInjection is an evidence-driven AI / LLM cyber threat-intelligence knowledge base. Its purpose is to connect observed behavior, technical research, security controls and reproducible defensive validation without collapsing them into one undifferentiated list.

## 1. Intelligence principles

### Evidence before promotion

A claim moves into the structured intelligence layer only when its source and evidentiary status are explicit.

Source grades:

| Grade | Meaning |
|---|---|
| A | Primary or authoritative source: vendor incident report, standards body, official advisory, original research |
| B | Strong secondary technical reporting with attributable evidence |
| C | Credible secondary reporting with material gaps |
| D | Community / discovery source |
| E | Unsupported or unverifiable claim |

Source grade and analytic confidence are separate. A primary source can still contain an assessment rather than a directly observed fact.

### Analytic confidence

| Value | Meaning |
|---|---|
| confirmed | Primary/authoritative evidence directly supports the structured claim |
| high | Strong named assessment or multiple credible sources |
| medium | Plausible and partially supported, with material gaps |
| low | Weak, indirect or conflicting support |
| unverified | Retained as a research lead, not promoted as fact |

## 2. Object model

The repository keeps different intelligence objects separate:

- **actor**: named vendor cluster, APT, criminal group or unattributed actor;
- **campaign**: bounded activity attributed or linked to an actor;
- **incident**: observed event, research case or explicitly labeled research artifact;
- **technique**: normalized AI/LLM security behavior;
- **model**: model family / deployment context;
- **vulnerability**: CVE, GHSA, OSV or malicious-package intelligence;
- **test-case**: safe defensive validation definition;
- **detection**: observable behavior hypothesis;
- **control**: mitigation / policy / assurance mechanism;
- **framework**: external taxonomy, standard or methodology;
- **source**: canonical evidence record;
- **relationship**: evidence-backed graph edge connecting objects.

A proof of concept is not an incident. A CVE is not an actor. A vendor alias is not automatically a universal alias. These distinctions are enforced because otherwise the graph becomes visually impressive nonsense.

## 3. Relationship rule

Every explicit relationship must:

1. reference two existing object IDs;
2. declare a relationship type;
3. declare analytic confidence;
4. reference one or more evidence-source IDs;
5. pass referential-integrity CI.

Examples:

```text
actor --conducts--> campaign
campaign --uses--> technique
campaign --uses-model-family--> model
test-case --validates--> technique
detection --detects--> technique
technique --mitigated-by--> control
vulnerability --observed-in--> campaign
```

## 4. Framework mapping

External mappings use a two-level semantic relationship:

- **exact**: the LLMInjection technique substantially matches the external technique/risk;
- **related**: meaningful overlap exists, but the concepts are not equivalent.

This prevents false precision when connecting MITRE ATLAS, ATT&CK, OWASP, NIST, SAIF, MAESTRO and other frameworks.

If an exact external identifier cannot be verified, the repository prefers a blank mapping over an invented ID.

## 5. Attribution discipline

LLMInjection does not merge actor aliases solely because two reports discuss the same country, tooling family or objective.

Attribution records should preserve:

- reporting vendor;
- actor/cluster label used by that vendor;
- nexus wording;
- directly observed behavior;
- assessed relationships;
- confidence;
- verification date.

Disputed or uncertain attribution remains explicit.

## 6. Threat-landscape methodology

Landscape metrics retain the original:

- population;
- geography, if any;
- measurement window;
- vendor dataset scope;
- publication date;
- source URL.

A metric from one vendor's telemetry is not rewritten as a universal global statistic.

Landscape objects distinguish:

```text
observed incident
vendor assessment
academic research
proof of concept
emerging concept
unverified research lead
```

## 7. Vulnerability enrichment

Vulnerability records preserve:

- CVE / GHSA / OSV / MAL identifiers;
- package and ecosystem;
- affected versions;
- fixed versions when known;
- publication date;
- severity as published;
- primary advisory sources.

Vulnerabilities are related to campaigns, techniques and controls only when evidence supports the relationship.

## 8. Safe evaluation

The evaluation layer tests system security properties rather than distributing a bypass-payload collection.

Allowed test patterns include:

- synthetic canaries;
- mock tools;
- local fixtures;
- simulated telemetry;
- disposable lab objects;
- explicit authorization checkpoints.

Results must record system/runtime versions and must not be generalized into a universal “model security score”.

## 9. Detection engineering

Detections describe observable hypotheses. They are not considered production-ready merely because a query exists.

A useful detection record identifies:

```text
behavior → required telemetry → analytic logic → expected false positives → safe validation
```

Vendor-specific queries are starter implementations and require field/schema adaptation to the target environment.

## 10. Update cadence

- Living-intelligence intake: daily metadata collection from allow-listed canonical/advisory feeds.
- Research promotion: review-gated; collection never auto-promotes official CTI.
- Actor/source verification: warning after 90 days; CI failure threshold after 180 days.
- Threat landscape: monthly structured snapshots and entity-level diffs, with quarterly synthesis as the longer-form reporting cadence.
- Framework crosswalks: update when canonical upstream versions change.
- CVE/GHSA/OSV: review candidates are collected automatically; official vulnerability/relationship enrichment remains evidence-gated.
- Confidence changes: preserve change history rather than silently rewriting prior assessments.

See docs/LIVING-INTELLIGENCE.md for the collection and review pipeline.

## 11. Reproducibility and provenance

Structured datasets are validated in CI and exported as:

- JSON graph;
- GraphML;
- STIX 2.1;
- versioned static JSON API;
- release archives with SHA-256 digest;
- GitHub artifact provenance attestations for tagged data releases.

## 12. Contribution acceptance

A contribution is strongest when it adds at least one of:

- stronger evidence;
- a defensible relationship;
- a corrected mapping;
- a reproducible safe test;
- useful telemetry;
- a detection hypothesis;
- a mitigation/control;
- a source-quality or confidence correction.

Volume alone is not a quality metric. The internet has already conducted that experiment.
