# Intelligence Graph

LLMInjection models AI-security intelligence as a graph rather than a collection of disconnected lists.

## Core objects

```text
Source
  ↓
Actor → Campaign → Technique → Model
                    ↓
                 Test Case
                    ↓
                 Detection
                    ↓
                  Control
                    ↓
                Framework
```

Additional `incident` objects represent observed incidents, research artifacts and defensive research cases. Status is preserved so a proof of concept is not silently presented as an active intrusion.

## Datasets

| Dataset | Purpose |
|---|---|
| `actors.json` | Threat actors and tracked clusters |
| `campaigns.json` | AI-enabled or AI-targeting campaigns |
| `incidents.json` | Observed incidents and research cases |
| `techniques.json` | LLMInjection behavior taxonomy |
| `models.json` | Model-family and deployment context |
| `test-cases.json` | Safe defensive validation cases |
| `detections.json` | Vendor-neutral detection hypotheses |
| `controls.json` | Defensive and governance controls |
| `frameworks.json` | Standards, taxonomies and frameworks |
| `sources.json` | Canonical source registry |
| `relationships.json` | Explicit graph edges |

## Relationship semantics

Current relationships include:

- `conducts`: actor → campaign;
- `uses`: campaign/incident → technique;
- `uses-model-family`: campaign → model family;
- `demonstrates`: incident/research case → technique;
- `validates`: test case → technique;
- `detects`: detection → technique;
- `mitigated-by`: technique → control;
- `supported-by`: test/detection → control;
- `sourced-by`: generated evidence link → source.

Every explicit relationship carries confidence and one or more evidence-source IDs.

## Build outputs

Run:

```bash
python scripts/validate_intel.py
python scripts/build_graph.py
```

Outputs:

```text
dist/
├── graph.json
├── graph.graphml
└── llminjection-stix.json
```

`graph.json` powers the web explorer. GraphML supports graph tools such as Gephi. The STIX 2.1 export maps native CTI objects to standard SDOs and uses custom `x-llminjection-*` objects for AI-specific concepts that do not have a clean STIX equivalent.

## Data-quality rule

A graph edge is an analytic claim. It is accepted only when:

1. both endpoints exist;
2. confidence is explicit;
3. evidence-source IDs resolve;
4. the source grade is known;
5. CI finds no dangling references.

That sounds basic. Astonishingly, doing the basic things already eliminates a large percentage of threat-intelligence sludge.
