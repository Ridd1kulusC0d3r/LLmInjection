# AI Security Frameworks & Taxonomies

MITRE ATLAS is essential, but it is only one lens. LLMInjection combines adversary behavior, application risk, agent runtime control, protocol security, supply-chain transparency, governance and CTI methodology.

## Crosswalk

| Resource | Type | Primary question | Best use in LLMInjection |
|---|---|---|---|
| MITRE ATLAS | Adversary knowledge base | How do adversaries attack AI-enabled systems? | AI-specific technique and campaign mapping |
| MITRE ATT&CK | Adversary knowledge base | How do surrounding intrusions operate? | Enterprise/cloud TTPs around AI-enabled campaigns |
| OWASP LLM Top 10 2026 | AppSec risk list | What fails in LLM/GenAI applications? | Current LLM application-risk mapping |
| OWASP LLM Top 10 2025 | Historical risk list | How were risks numbered before 2026? | Preserve legacy evidence mappings |
| OWASP Agentic Top 10 2026 | Agentic risk list | What fails when AI plans and acts? | Identity, tools, memory, delegation and autonomy |
| OWASP Agent Control Standard | Runtime-control standard | How can agent behavior be inspected and controlled? | Runtime policy and agent observability |
| OWASP GenAI Industry Crosswalk | Framework crosswalk | How do GenAI risks map across major standards? | Cross-framework analysis |
| NIST AI 100-2e2025 | AML taxonomy | How should adversarial ML be described? | Canonical attack terminology |
| NIST AI RMF + AI 600-1 | Risk framework/profile | How should organizations govern AI risk? | Governance and lifecycle assurance |
| Google SAIF | Secure-AI framework | Where are AI risks introduced and mitigated? | Risk-to-control architecture |
| CSA MAESTRO | Threat-modeling framework | How do we model multi-agent systems? | Layered agentic threat modeling |
| CSA AI Controls Matrix v1.1 | Control framework | Which controls apply to AI systems? | Assurance and model-security controls |
| MCP Security Best Practices 2026-07-28 | Protocol security | What trust failures exist in MCP? | Authorization, consent, token and local-server controls |
| CycloneDX AI/ML-BOM | Supply-chain transparency | What AI assets and dependencies exist? | Model/dataset/dependency provenance |
| ENISA CTL Methodology 2025 | CTI methodology | How should a threat landscape be produced? | Evidence handling and landscape structure |
| STRIDE | Threat modeling | Which classic technical threats exist? | Baseline component analysis |
| PASTA | Risk-centric threat modeling | How do impact and attack paths connect? | Scenario-driven threat models |
| LINDDUN | Privacy threat modeling | Which privacy harms exist? | Data/RAG/model privacy analysis |

## Why multiple frameworks

A single agentic prompt-injection incident may simultaneously involve:

- **OWASP LLM** application risk;
- **OWASP Agentic** tool, memory or identity risk;
- **OWASP ACS** runtime control;
- **MCP** authorization or consent requirements;
- **MITRE ATLAS** AI attack behavior;
- **MITRE ATT&CK** surrounding credential/cloud behavior;
- **MAESTRO** cross-layer trust failure;
- **SAIF / AICM** control gaps;
- **NIST AML / AI RMF** taxonomy and governance.

LLMInjection preserves those distinctions, then links them through graph relationships rather than inventing fake one-to-one mappings.

## Current additions that matter

### OWASP Agent Control Standard

ACS provides a model for inspectable, traceable agents and portable runtime policy enforcement. It is especially relevant to LLMInjection controls around tool authorization, human checkpoints and action telemetry.

Source: https://genai.owasp.org/resource/agent-control-standard-acs/

### CSA AI Controls Matrix v1.1

AICM v1.1 adds dedicated model-security coverage and maps controls to major governance frameworks. LLMInjection uses it as a control/assurance source rather than as an attack taxonomy.

Source: https://cloudsecurityalliance.org/blog/2026/07/14/ai-controls-matrix-v1-1-strengthening-the-foundation-for-trustworthy-ai

### MCP Security Best Practices

The official MCP guidance covers protocol-specific risks including confused-deputy behavior, state-handle authorization, local server compromise, user consent, token audience validation and mix-up attacks.

Source: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/2026-07-28/tutorials/security/security_best_practices.mdx

### CycloneDX AI/ML-BOM

CycloneDX can represent models, datasets, configurations and dependencies. LLMInjection uses this as the supply-chain transparency layer behind AI/ML-BOM controls.

Source: https://www.cyclonedx.org/capabilities/mlbom/

## Existing core references

- MITRE ATLAS: https://atlas.mitre.org/
- OWASP LLM Top 10 2026: https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- OWASP Agentic Top 10 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- NIST AI 100-2e2025: https://doi.org/10.6028/NIST.AI.100-2e2025
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- Google SAIF: https://saif.google/
- CSA MAESTRO: https://labs.cloudsecurityalliance.org/maestro/
- ENISA CTL Methodology: https://www.enisa.europa.eu/publications/enisa-cybersecurity-threat-landscape-methodology

## Mapping rule

A mapping must be defensible. When an exact technique/control identifier has not been verified, LLMInjection maps only at framework-family level rather than manufacturing precision.
