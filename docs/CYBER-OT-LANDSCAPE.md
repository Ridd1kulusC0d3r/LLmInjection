# AI × Cyber OT / ICS threat landscape

**Status: defensive research domain. Updated 2026-10-09.**

This domain connects *AI-system threats* to *industrial operational contexts* while
keeping hypotheses separate from observed incidents. The primary LLMInjection
datasets remain authoritative for actors, campaigns, detections, sources, techniques
and relationships. This domain contributes complementary contextual records.

## Scope: four different questions

1. **AI as a target in industrial environments:** integrity of industrial RAG,
   maintenance copilot knowledge, models and software supply chains.
2. **AI used as an adversary enabler:** review primary reports before claiming
   industrial targeting or identifying the model or operator.
3. **AI adjacent to OT processes:** authority boundaries between recommendations,
   engineering approvals, enterprise tools and OT components.
4. **AI as a defender:** whether monitoring models generalize across process
   modes, datasets and sites, with measured false alarms and human escalation.

**Not in scope:** interacting with live PLCs, network probing, equipment commands,
exploit payloads, production system testing, real-time plant inventory, predictive
physical impact claims or linking ordinary ICS ransomware to AI without evidence.

## Initial datasets and machine-readable assets

| File | Status | Role |
| --- | --- | --- |
| [OT sources](../data/ot-source-registry.json) | 14 curated references, 2 enabled passive metadata adapters | Controlled provenance and ingestion registry |
| [OT scenarios](../data/ot-scenarios.json) | 6 **hypothetical** scenarios | Risk/telemetry/control hypotheses, not incident records |
| [OT datasets](../data/ot-datasets.json) | 5 references | License-aware experimental discovery, **no raw datasets** |
| [OT research queue](../data/ot-review-queue.json) | Candidate-only | Metadata and human review decisions |
| [Offline fixture](../tests/fixtures/ot-feeds.json) | Synthetic | Tests without industrial access |

The scenario list is intentionally separate from `data/incidents.json`, which
must contain supported claims. Sources in the OT registry are *sources to review*,
not `data/sources.json` citations already promoted into intelligence.

## Priority data sources

| Provider | Exact integration boundary | Evidence limitation |
| --- | --- | --- |
| [MITRE ATT&CK ICS STIX 2.1](https://github.com/mitre-attack/attack-stix-data) | Listed versioned `ics-attack/*.json` files | Knowledge base, not proof a scenario occurred |
| [CISA CSAF](https://github.com/cisagov/CSAF) | 2026 OT advisory **filenames and blob metadata** | No automatic CVE/product/exploitation claims |
| [CISA KEV](https://github.com/cisagov/kev-data) | Existing core enrichment | KEV is not AI/OT attribution |
| [CISA Vulnrichment](https://github.com/cisagov/vulnrichment) | Future SSVC enrichment | Context still requires asset inventory |
| [OTCAD](https://github.com/bvcyber/OTCAD) | Secondary historical OT discovery | Map legacy ATT&CK versions before using |
| [MISP ICS Taxonomies](https://github.com/MISP/misp-taxonomies) | Vocabulary | Taxonomy does not equal observation |
| [IPAL datasets](https://github.com/ipal-ids/ipal_datasets) | Offline dataset converters | Does not include raw datasets |
| [HAI](https://github.com/icsdataset/hai) | Offline time-series benchmark | Verify dataset license and distribution terms |
| [Malcolm](https://github.com/cisagov/Malcolm) | Passive telemetry architecture reference | Not installed, not scanning |
| [CSET](https://github.com/cisagov/cset) | Industrial risk-assessment guidance | Control reference, not incident CTI |

Further authoritative guidance:
- [CISA and partners, Principles for the Secure Integration of Artificial Intelligence in OT, 2025-12-03](https://www.cisa.gov/resources-tools/resources/principles-secure-integration-artificial-intelligence-operational-technology)
- [NIST SP 800-82 Rev. 3, final](https://csrc.nist.gov/pubs/sp/800/82/r3/final)
- [NIST SP 800-82 Rev. 4, initial public draft](https://csrc.nist.gov/pubs/sp/800/82/r4/ipd)
- [MITRE ATT&CK ICS](https://attack.mitre.org/matrices/ics/)
- [MITRE ATLAS](https://atlas.mitre.org/)

NIST Rev. 4 is a draft as of this update. Do not describe it as a final
standard. IEC 62443 may be referenced by scope, but its paid text must not
be redistributed without permission.

## Source and confidence invariants

- *Source grade* assesses provenance; *claim confidence* is independent.
- A vendor advisory does not establish that a vulnerable asset exists at
  a specific site, is exposed, or has been exploited.
- A generic OT attack is not AI-powered unless a primary source shows that link.
- A simulated industrial anomaly is not an observed criminal campaign.
- AI involvement is stored as `design-hypothesis` for these scenarios, never
  `observed-in-the-wild`.
- MITRE ATLAS, Enterprise ATT&CK and ICS ATT&CK mappings are versioned and
  reviewed at the **specific technique** level when exact relationships exist.
- Operational safety and reliability take priority: AI-generated output is
  never treated as sufficient authorization to change physical processes.

## Run, without connecting to OT networks

```bash
python3 scripts/validate_ot.py
python3 -m unittest tests/test_ot.py
python3 scripts/ot_intake.py --fixture tests/fixtures/ot-feeds.json --dry-run
# Public GitHub metadata only; needs network and explicit opt-in:
python3 scripts/ot_intake.py --live --dry-run
```

When `--dry-run` is omitted, the script only updates the review-queue JSON.
It never writes incidents or source-of-truth intelligence. No source code
from discovered projects is executed. The fixed 2026 CSAF directory must be
rotated/reviewed for subsequent years; this initial adapter does not claim
complete historical coverage.

## Roadmap

1. Review-gated ingestion of CSAF **document content** with product-tree and
   revision-history validation, using offline fixtures and no asset discovery.
2. Versioned ATT&CK ICS crosswalk into ATLAS/Enterprise, preserving the
   provenance and avoiding invented 1:1 relations.
3. Optional analyst-approved export of the validated OT registry to STIX
   / API and versioned source-diff reporting.
4. Evidence-backed AI-in-OT case studies **only after** primary reporting
   documents the AI connection.
5. Explorer UI for OT sectors, boundary controls, evidence classes, dataset
   license status and remaining detection coverage gaps.

No bullet above should be marked complete until its tests and provenance
checks are delivered.
