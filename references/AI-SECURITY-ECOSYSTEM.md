# AI Security Landscape — Curated GitHub Ecosystem

This page indexes external repositories that are useful for **research discovery, defensive evaluation, threat modeling and dataset enrichment**. Inclusion does not convert a community repository into authoritative threat intelligence.

## Landscape / curated references

| Repository | Role in LLMInjection |
|---|---|
| [8kSec/awesome-ai-security](https://github.com/8kSec/awesome-ai-security) | Broad AI-security discovery and research index |
| [ottosulin/awesome-ai-security](https://github.com/ottosulin/awesome-ai-security) | Frameworks, standards, tools and agent/MCP security discovery |
| [TalEliyahu/Awesome-AI-Security](https://github.com/TalEliyahu/Awesome-AI-Security) | Threat modeling, security research and tooling discovery |
| [cckuailong/awesome-gpt-security](https://github.com/cckuailong/awesome-gpt-security) | LLM/GPT security research and experiments |

## Red teaming / evaluation

| Repository | Role |
|---|---|
| [NVIDIA/garak](https://github.com/NVIDIA/garak) | GenAI vulnerability scanning and regression evaluation |
| [microsoft/PyRIT](https://github.com/microsoft/PyRIT) | GenAI red-team orchestration and evaluation |
| [JailbreakBench/jailbreakbench](https://github.com/JailbreakBench/jailbreakbench) | Jailbreak robustness benchmark |
| [albert-y1n/PIForge](https://github.com/albert-y1n/PIForge) | Prompt-injection research framework; index as research, not production exploit guidance |
| [llm-attacks/llm-attacks](https://github.com/llm-attacks/llm-attacks) | Academic adversarial LLM attack research |

## Datasets / benchmarks

| Repository | Role |
|---|---|
| [VeraaaCUI/SecEval-Dataset](https://github.com/VeraaaCUI/SecEval-Dataset) | Security evaluation dataset discovery |
| [bboylyg/BackdoorLLM](https://github.com/bboylyg/BackdoorLLM) | LLM backdoor benchmark/research |
| [QData/TextAttack](https://github.com/QData/TextAttack) | Adversarial NLP evaluation |
| [Trusted-AI/adversarial-robustness-toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox) | Adversarial ML evaluation and defenses |

## Threat-intelligence discovery

| Repository | Role |
|---|---|
| [mermoddity/ai-security-rss-feed](https://github.com/mermoddity/ai-security-rss-feed) | AI-security source/feed discovery |
| [GenAI-Security-Project/GenAI-LLM-Top10](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10) | Canonical OWASP LLM Top 10 source |
| [mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data) | MITRE ATLAS machine-readable knowledge base |

## Intake discipline

External repositories are classified as one of:

- **canonical source** — official framework/project repository;
- **research implementation** — code accompanying published research;
- **evaluation tool** — defensive/red-team testing software;
- **benchmark/dataset** — evaluation data;
- **community index** — discovery source only.

The workflow is:

```text
external repo
   ↓
discovery
   ↓
primary paper / advisory / canonical project source
   ↓
LLMInjection evidence grading
   ↓
actor / technique / landscape / test / control relationship
```

We do not copy large prompt payload collections into the CTI core. Their useful contribution is metadata: attack family, model/application context, publication provenance, reproducibility and defensive coverage.
