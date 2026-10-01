# AI Security Frameworks & Taxonomies

MITRE ATLAS is essential, but it is only one lens. LLMInjection deliberately uses several frameworks because adversarial AI spans classic intrusion behavior, ML-specific attacks, application security, agent autonomy, governance and threat intelligence.

## Crosswalk

| Resource | Type | Primary question | Best use in LLMInjection |
|---|---|---|---|
| MITRE ATLAS | Adversary knowledge base | How do adversaries attack AI-enabled systems? | Technique mapping and campaign behavior |
| MITRE ATT&CK | Adversary knowledge base | How do intrusions operate across enterprise/cloud? | Classic TTPs around AI-enabled campaigns |
| OWASP Top 10 for LLM Apps 2025 | AppSec risk list | What fails in LLM/GenAI applications? | Prompt injection, disclosure, supply chain, poisoning, output handling |
| OWASP Top 10 for Agentic Apps 2026 | Agentic risk list | What fails when AI can plan and act? | Agent identity, tools, autonomy, memory and orchestration risks |
| NIST AI 100-2e2025 | AML taxonomy | How should adversarial ML attacks and mitigations be described? | Canonical AML terminology |
| NIST AI RMF 1.0 + AI 600-1 | Risk framework/profile | How should organizations govern AI risk? | Governance, lifecycle and assurance mapping |
| Google SAIF | Secure-AI framework | Where are AI risks introduced/exposed/mitigated? | Lifecycle controls across data, infrastructure, model and application |
| CSA MAESTRO | Threat-modeling framework | How do we model multi-agent/agentic systems? | Seven-layer agentic threat models |
| CSA AI Controls Matrix | Control framework | Which security controls apply to AI systems? | Control mapping and assurance |
| ENISA CTL Methodology 2025 | Threat-landscape methodology | How should cyber threat intelligence be structured? | Source-driven threat landscape and reporting |
| STRIDE | Threat modeling | Which classic technical threat classes exist? | Baseline component threat modeling |
| PASTA | Risk-centric threat modeling | How do business impact and attack paths connect? | Scenario-driven AI threat models |
| LINDDUN | Privacy threat modeling | Which privacy harms can the system introduce? | Privacy analysis for data/RAG/model flows |

## Why a multi-framework approach

No single framework spans the whole system.

A prompt-injection incident in an enterprise agent may involve:

- an **OWASP LLM/Agentic** application risk;
- a **MITRE ATLAS** AI attack technique;
- **MITRE ATT&CK** credential, cloud or lateral-movement behavior;
- a **MAESTRO** cross-layer trust failure;
- a **SAIF** risk and control gap;
- a **NIST AI 100-2e2025** adversarial-ML concept;
- a **NIST AI RMF** governance failure.

LLMInjection keeps those mappings separate, then links them through data records rather than forcing a fake one-to-one equivalence.

## Framework notes

### MITRE ATLAS

Use for adversary tactics and techniques targeting AI systems. ATLAS is the closest analogue to ATT&CK for adversarial AI, but real intrusions still need ATT&CK mappings for the surrounding infrastructure.

Source: https://atlas.mitre.org/

### OWASP Top 10 for LLM Applications 2025

The 2025 list includes Prompt Injection, Sensitive Information Disclosure, Supply Chain, Data and Model Poisoning, Improper Output Handling and other application-level risks.

Source: https://genai.owasp.org/llm-top-10/

### OWASP Top 10 for Agentic Applications 2026

A peer-reviewed OWASP GenAI framework focused on autonomous and agentic AI systems that plan, act and use tools across workflows.

Source: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

### NIST AI 100-2e2025

NIST's 2025 adversarial machine learning taxonomy organizes attacks by lifecycle stage, attacker goals, capabilities and knowledge, and pairs them with mitigation concepts.

Source: https://doi.org/10.6028/NIST.AI.100-2e2025

### NIST AI RMF + Generative AI Profile

The AI RMF provides the Govern, Map, Measure and Manage risk functions. NIST AI 600-1 adds GenAI-specific risk considerations.

Sources:
- https://www.nist.gov/itl/ai-risk-management-framework
- https://doi.org/10.6028/NIST.AI.600-1

### Google SAIF

SAIF maps risks and controls across Data, Infrastructure, Model and Application components. Its current risk map includes prompt injection, data poisoning, model source tampering, model exfiltration, insecure integrated components, sensitive-data disclosure and rogue actions.

Source: https://saif.google/

### CSA MAESTRO

MAESTRO (Multi-Agent Environment, Security, Threat, Risk, and Outcome) is a seven-layer threat-modeling approach for agentic AI. It explicitly extends classic methods such as STRIDE, PASTA and LINDDUN with AI-specific and multi-agent considerations.

Source: https://labs.cloudsecurityalliance.org/maestro/

### ENISA Cybersecurity Threat Landscape Methodology 2025

Useful for the *intelligence process* rather than AI-specific attack techniques: consistent threat landscape production, evidence handling and contextualization.

Source: https://www.enisa.europa.eu/publications/enisa-cybersecurity-threat-landscape-methodology

## LLMInjection mapping rule

A record may map to many frameworks, but a mapping must be defensible. If an exact technique/control identifier is unknown, map only at framework-family level and leave the identifier blank rather than inventing one.
