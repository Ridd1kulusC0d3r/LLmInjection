# LLMInjection

> **AI / LLM Cyber Threat Intelligence, adversarial research and defensive engineering.**

LLMInjection is an open cybersecurity knowledge base for tracking how large language models, generative AI and agentic systems change the threat landscape.

This project is **not a prompt dump**. It connects threat actors, campaigns, AI attack surfaces, prompt injection, jailbreak research, adversarial ML, model supply-chain compromise, agentic abuse, detections, mitigations, benchmarks and security frameworks in one evidence-driven repository.

## Why this exists

AI security is fragmented across model-security papers, vendor threat reports, jailbreak repositories, OWASP guidance, MITRE ATLAS, adversarial ML research, incident reports and classic threat-modeling methods. LLMInjection turns that fragmentation into a usable intelligence layer.

The repository models four distinct questions:

1. **AI as a target** — prompt injection, poisoning, model theft, supply-chain compromise, malicious dependencies and agent/tool abuse.
2. **AI as an offensive enabler** — reconnaissance, social engineering, malware development, data analysis and attack automation.
3. **AI as an autonomous operator** — agentic execution, orchestration and machine-speed attack chains.
4. **AI as a defensive control plane** — detection, evaluation, policy enforcement, monitoring and threat hunting.

## Intelligence map

| Layer | What we track |
|---|---|
| Threat actors | APTs, financially motivated actors, unattributed clusters |
| Campaigns | Real-world AI-enabled or AI-targeting operations |
| Techniques | Prompt injection, jailbreaks, poisoning, model extraction, RAG abuse, agent/tool misuse |
| Models & runtimes | Frontier APIs, open-weight models, local runtimes and agent frameworks |
| Supply chain | Models, datasets, packages, gateways, plugins, MCP/A2A components and CI/CD |
| Detection | Telemetry, behaviors, analytics, hunting hypotheses and control points |
| Frameworks | MITRE ATLAS, OWASP, NIST, Google SAIF, CSA MAESTRO, ENISA and classic threat modeling |
| Evidence | Source quality, confidence, attribution and verification date |

## Frameworks beyond MITRE ATLAS

LLMInjection treats frameworks according to what they actually do instead of pretending every standards document is a threat framework.

- **MITRE ATLAS** — adversary behaviors against AI-enabled systems.
- **OWASP Top 10 for LLM Applications 2025** — application-layer GenAI risks.
- **OWASP Top 10 for Agentic Applications 2026** — autonomous-agent security risks.
- **NIST AI 100-2e2025** — adversarial machine learning taxonomy and terminology.
- **NIST AI RMF + Generative AI Profile (AI 600-1)** — AI risk governance and lifecycle controls.
- **Google Secure AI Framework (SAIF)** — AI lifecycle risks and mapped controls.
- **CSA MAESTRO** — threat modeling for multi-agent and agentic AI systems.
- **ENISA Cybersecurity Threat Landscape Methodology 2025** — structured threat-landscape methodology.
- **STRIDE / PASTA / LINDDUN** — foundational threat-modeling lenses reused where they still fit.

See [docs/FRAMEWORKS.md](docs/FRAMEWORKS.md) for the crosswalk.

## Current threat-intelligence watchlist

The repository tracks confirmed or well-sourced cases including:

- **GTG-1002** — Anthropic assessed with high confidence that a Chinese state-sponsored group used Claude Code in a largely AI-orchestrated espionage campaign against roughly 30 targets; Anthropic reported AI performing 80–90% of tactical operations.
- **APT28 / FROZENLAKE** — Google Threat Intelligence documented PROMPTSTEAL/LAMEHUG querying an LLM to generate commands during live operations.
- **APT42** — Google documented Gemini use for reconnaissance, target research, phishing content and localization.
- **UNC2970** — Google documented Gemini use to synthesize OSINT and profile high-value targets.
- **Kimsuky** — Genians reported local LLM infrastructure including Ollama, GPT4All and Msty plus RAG-related artifacts in infrastructure linked to the group.
- **Famous Chollima / PromptMink** — public 2026 reporting describes AI-optimized malicious package activity aimed at coding-agent dependency selection.
- **TeamPCP** — 2026 supply-chain activity affected Trivy/KICS and malicious LiteLLM releases, demonstrating that AI infrastructure and gateways are high-value targets.

Every actor record includes a source list, confidence level and last-verification date. We deliberately separate **confirmed fact**, **vendor assessment**, **community reporting** and **unverified claims**.

## Repository structure

```text
LLmInjection/
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── docs/
│   ├── FRAMEWORKS.md
│   ├── AI-THREAT-MODEL.md
│   ├── ACTOR-TRACKER.md
│   ├── DETECTION-ENGINEERING.md
│   ├── MODEL-SECURITY-MATRIX.md
│   ├── BENCHMARKS.md
│   ├── SOURCE-GRADING.md
│   └── ROADMAP.md
├── data/
│   ├── frameworks.json
│   ├── actors.json
│   └── techniques.json
├── references/
│   └── community-corpora.md
├── schemas/
│   └── intel.schema.json
└── scripts/
    └── validate_intel.py
```

## Evidence model

Every intelligence item should answer:

- **What happened?**
- **Who says so?**
- **What is directly observed vs assessed?**
- **How confident are we?**
- **When was it last verified?**
- **Which framework techniques/risks does it map to?**
- **What defensive telemetry or control is relevant?**

Confidence values:

| Value | Meaning |
|---|---|
| `confirmed` | Primary or authoritative reporting directly supports the claim |
| `high` | Multiple credible sources or a strong named-vendor assessment |
| `medium` | Plausible reporting with material gaps |
| `low` | Weak, indirect or single-source reporting |
| `unverified` | Interesting claim retained for research but not treated as fact |

## Core sources

- MITRE ATLAS: https://atlas.mitre.org/
- OWASP GenAI Security Project: https://genai.owasp.org/
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI 100-2e2025: https://doi.org/10.6028/NIST.AI.100-2e2025
- Google SAIF: https://saif.google/
- CSA MAESTRO: https://labs.cloudsecurityalliance.org/maestro/
- ENISA Threat Landscape methodology: https://www.enisa.europa.eu/publications/enisa-cybersecurity-threat-landscape-methodology
- Anthropic threat research: https://www.anthropic.com/research
- Google Threat Intelligence: https://cloud.google.com/blog/topics/threat-intelligence

## Research posture

LLMInjection is built for **defenders, threat analysts, AI red teams, detection engineers, researchers and security architects**. Offensive techniques are documented to support threat modeling and authorized evaluation; the project prioritizes reproducible evidence, mitigations, detections and safe lab research over turnkey abuse.

## Contributing

The fastest way to make this repository useful is to contribute **new evidence**, not hype.

Read [CONTRIBUTING.md](CONTRIBUTING.md), include primary sources whenever possible, and mark uncertain attribution explicitly.

## License

Apache-2.0. See [LICENSE](LICENSE).
