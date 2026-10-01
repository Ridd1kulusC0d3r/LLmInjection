# Reference Library

This library prioritizes **canonical standards, primary threat reports, maintained evaluation projects and original research**. Community lists remain useful for discovery, but they do not outrank primary evidence simply because their README has many emoji.

## Standards and canonical guidance

| Resource | Why it matters |
|---|---|
| [MITRE ATLAS](https://atlas.mitre.org/) | Adversary behavior against AI-enabled systems |
| [MITRE ATLAS data](https://github.com/mitre-atlas/atlas-data) | Machine-readable ATLAS knowledge base |
| [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | Current LLM application-risk reference |
| [OWASP Agentic Top 10 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Agent autonomy, identity, tools and memory risk |
| [OWASP Agent Control Standard](https://genai.owasp.org/resource/agent-control-standard-acs/) | Runtime inspection and portable agent policy controls |
| [OWASP GenAI framework crosswalk](https://genai.owasp.org/resource-item/tools/) | Cross-framework control mapping |
| [NIST AI 100-2e2025](https://www.nist.gov/publications/adversarial-machine-learning-taxonomy-and-terminology-attacks-and-mitigations-0) | Canonical AML taxonomy and terminology |
| [Google SAIF](https://saif.google/) | AI lifecycle threat/control architecture |
| [CSA MAESTRO](https://labs.cloudsecurityalliance.org/maestro/) | Multi-agent and agentic threat modeling |
| [CSA AI Controls Matrix v1.1](https://cloudsecurityalliance.org/blog/2026/07/14/ai-controls-matrix-v1-1-strengthening-the-foundation-for-trustworthy-ai) | AI control framework with dedicated model-security coverage |
| [MCP specification and security guidance](https://github.com/modelcontextprotocol/modelcontextprotocol) | Protocol trust boundaries, authorization and security best practices |
| [CycloneDX AI/ML-BOM](https://www.cyclonedx.org/capabilities/mlbom/) | Model/dataset/dependency supply-chain transparency |\n| [SLSA v1.2](https://slsa.dev/spec/v1.2/) | Build/source provenance and supply-chain assurance |\n| [Sigstore / Cosign](https://docs.sigstore.dev/quickstart/quickstart-cosign/) | Artifact signing, identity and verification |\n| [OpenSSF Malicious Packages](https://github.com/ossf/malicious-packages) | OSV-formatted malicious package intelligence |
| [STIX 2.1](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html) | CTI interchange format |

## Defensive evaluation tooling

| Project | Role |
|---|---|
| [microsoft/PyRIT](https://github.com/microsoft/PyRIT) | GenAI red-team orchestration and evaluation |
| [NVIDIA/garak](https://github.com/NVIDIA/garak) | GenAI vulnerability scanning and regression testing |
| [JailbreakBench](https://github.com/JailbreakBench/jailbreakbench) | Jailbreak robustness benchmark |
| [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox) | Adversarial ML evaluation |
| [TextAttack](https://github.com/QData/TextAttack) | Adversarial NLP experimentation |
| [Model Context Protocol Inspector](https://github.com/modelcontextprotocol/inspector) | Protocol inspection and development support |\n| [Purple Llama / CyberSecEval](https://github.com/meta-llama/PurpleLlama) | Cybersecurity, prompt-injection and autonomous-operation evaluation suites |
| [Sigstore Cosign](https://github.com/sigstore/cosign) | Artifact signing and verification |

## Primary threat and landscape sources

- Anthropic threat research and GTG-1002 reporting;
- Google Threat Intelligence Group AI-threat reporting;
- CrowdStrike Threat Hunting Report 2026;
- Check Point AI Security Report 2026;
- Fortinet Global Threat Landscape 2026;
- Zscaler ThreatLabz ransomware research;
- IBM X-Force Threat Intelligence Index 2026;
- Cisco Talos CLOSEDQUORUM research;
- Palo Alto Networks Unit 42 model-safety research.

## Research worth tracking

- *The Promptware Kill Chain*;
- indirect prompt-injection and agent security research;
- model integrity / safety-circuit research;
- coding-agent dependency selection and package ecosystem research;
- agent identity and runtime-policy enforcement.

## Source intake rule

A reference enters one of four roles:

1. **canonical** — standard/specification/official knowledge base;
2. **primary evidence** — original incident or threat report;
3. **research** — original paper or implementation;
4. **discovery** — community index used to find stronger evidence.

Claims promoted into actors, campaigns, incidents or landscape metrics should normally resolve to category 1–3 sources.
