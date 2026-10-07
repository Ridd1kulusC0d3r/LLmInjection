# Ecosystem map

Seventy-five related GitHub projects, curated from a research pass on 2026-10-07 and organised by what each can honestly support.

**Provenance.** The list was supplied by the maintainer's own research. Descriptions summarise each project's declared scope. Repository state, including the archived flags, is recorded as reported and has not been independently verified, and nothing here measures a tool's effectiveness.

## The rule that governs this page

LLMInjection keeps three kinds of evidence apart:

1. **Observed incidents:** something happened, with a primary report.
2. **Demonstrated techniques:** something worked in research or a lab, not necessarily in the wild.
3. **Lab examples:** material for training and test design.

A repository listed here can inform test cases, detections, controls and taxonomy. It can **never** create an actor, a campaign or an incident record, and it cannot support attribution. The validator rejects an entry that claims otherwise. A jailbreak collection can enrich the test catalog; it cannot show that a named actor used the technique.

## Evidence classes

<!-- gen:eco-classes:start -->
| Evidence class | What it is | Can support | Cannot support | Entries |
|---|---|---|---|---|
| `framework-data` | Taxonomies and knowledge bases | Technique definitions and framework mappings | Observed activity | 6 |
| `incident-data` | Incident databases | Incident references, citing the primary report | Actor attribution or cyber campaigns (scope is broader than cybersecurity) | 1 |
| `detection-content` | Community detection rules | Detection ideas and telemetry requirements | Proof of in-the-wild behavior | 1 |
| `curated-list` | Curated lists | Discovering sources and tools | Any claim on their own | 16 |
| `assessment-tool` | Scanners and red-team tools | Test design and control evaluation | Effectiveness against current models | 18 |
| `benchmark` | Benchmarks and environments | Reproducible tests and coverage measurement | Real-world prevalence | 8 |
| `research-technique` | Attack research code | Techniques demonstrated in research | Use in the wild | 12 |
| `defence-tool` | Defences and guardrails | Control design and comparison | Proven protection | 7 |
| `lab-exercise` | Training labs | Analyst training and onboarding | Threat intelligence | 4 |
| `prompt-corpus` | Prompt corpora and datasets | Test inspiration and measurement | Threat intelligence or attribution | 2 |
<!-- gen:eco-classes:end -->

## Start here

Ten entries chosen as the highest-value inputs for taxonomy, evidence, tests and controls.

<!-- gen:eco-start:start -->
| Repository | Evidence class | Techniques | Scope |
|---|---|---|---|
| [mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data) | `framework-data` | none | Data for tactics, techniques and case studies of threats against AI systems. · **start here** |
| [PLOT4ai/plot4ai-library](https://github.com/PLOT4ai/plot4ai-library) | `framework-data` | none | Threat library for AI threat modeling. · **start here** |
| [Arcanum-Sec/arc_pi_taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy) | `framework-data` | `LLMI-T001`, `LLMI-T002` | Taxonomy specialised in prompt injection. · **start here** |
| [responsible-ai-collaborative/aiid](https://github.com/responsible-ai-collaborative/aiid) | `incident-data` | none | AI Incident Database: incidents and harms involving AI, broader than cybersecurity. · **start here** |
| [Agent-Threat-Rule/agent-threat-rules](https://github.com/Agent-Threat-Rule/agent-threat-rules) | `detection-content` | `LLMI-T001`, `LLMI-T002`, `LLMI-T008` | Detection rules for agent threats, including injection, tools and MCP. · **start here** |
| [tldrsec/prompt-injection-defenses](https://github.com/tldrsec/prompt-injection-defenses) | `curated-list` | `LLMI-T001`, `LLMI-T002` | Practical and proposed defences against prompt injection. · **start here** |
| [ShenaoW/awesome-llm-supply-chain-security](https://github.com/ShenaoW/awesome-llm-supply-chain-security) | `curated-list` | `LLMI-T011` | LLM supply chain: papers, reports and CVEs. · **start here** |
| [NVIDIA/garak](https://github.com/NVIDIA/garak) | `assessment-tool` | none | LLM vulnerability scanner. · **start here** |
| [microsoft/PyRIT](https://github.com/microsoft/PyRIT) | `assessment-tool` | none | Framework for identifying risks in generative AI systems. · **start here** |
| [ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo) | `benchmark` | `LLMI-T002`, `LLMI-T008` | Environment for evaluating attacks and defences of LLM agents. · **start here** |
<!-- gen:eco-start:end -->

## All entries

### Knowledge bases, taxonomies and incident data

<!-- gen:eco-knowledge:start -->
| Repository | Evidence class | Techniques | Scope |
|---|---|---|---|
| [mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data) | `framework-data` | none | Data for tactics, techniques and case studies of threats against AI systems. · **start here** |
| [mitre-atlas/atlas-website](https://github.com/mitre-atlas/atlas-website) | `framework-data` | none | Implementation of the ATLAS knowledge portal. |
| [OWASP/www-project-top-10-for-large-language-model-applications](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications) | `framework-data` | none | Risk taxonomy and security guidance for LLM applications. |
| [OWASP/www-project-ai-security-and-privacy-guide](https://github.com/OWASP/www-project-ai-security-and-privacy-guide) | `framework-data` | none | Security and privacy references for AI systems. |
| [PLOT4ai/plot4ai-library](https://github.com/PLOT4ai/plot4ai-library) | `framework-data` | none | Threat library for AI threat modeling. · **start here** |
| [Arcanum-Sec/arc_pi_taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy) | `framework-data` | `LLMI-T001`, `LLMI-T002` | Taxonomy specialised in prompt injection. · **start here** |
| [responsible-ai-collaborative/aiid](https://github.com/responsible-ai-collaborative/aiid) | `incident-data` | none | AI Incident Database: incidents and harms involving AI, broader than cybersecurity. · **start here** |
| [Agent-Threat-Rule/agent-threat-rules](https://github.com/Agent-Threat-Rule/agent-threat-rules) | `detection-content` | `LLMI-T001`, `LLMI-T002`, `LLMI-T008` | Detection rules for agent threats, including injection, tools and MCP. · **start here** |
<!-- gen:eco-knowledge:end -->

### Catalogs and awesome lists

<!-- gen:eco-catalog:start -->
| Repository | Evidence class | Techniques | Scope |
|---|---|---|---|
| [corca-ai/awesome-llm-security](https://github.com/corca-ai/awesome-llm-security) | `curated-list` | none | Tools, papers and projects on LLM security. |
| [Joe-B-Security/awesome-prompt-injection](https://github.com/Joe-B-Security/awesome-prompt-injection) | `curated-list` | `LLMI-T001`, `LLMI-T002` | Resources on prompt injection. |
| [tldrsec/prompt-injection-defenses](https://github.com/tldrsec/prompt-injection-defenses) | `curated-list` | `LLMI-T001`, `LLMI-T002` | Practical and proposed defences against prompt injection. · **start here** |
| [user1342/Awesome-LLM-Red-Teaming](https://github.com/user1342/Awesome-LLM-Red-Teaming) | `curated-list` | none | Training, tools and material for LLM red teaming. |
| [yueliu1999/Awesome-Jailbreak-on-LLMs](https://github.com/yueliu1999/Awesome-Jailbreak-on-LLMs) | `curated-list` | `LLMI-T003` | Papers, code, datasets and evaluations of jailbreaks. |
| [cckuailong/awesome-gpt-security](https://github.com/cckuailong/awesome-gpt-security) | `curated-list` | none | Tools and experiments on GPT and LLM security. |
| [CryptoAILab/Awesome-LM-SSP](https://github.com/CryptoAILab/Awesome-LM-SSP) | `curated-list` | none | Literature on safety, security and privacy of large models. |
| [wearetyomsmnv/Awesome-LLMSecOps](https://github.com/wearetyomsmnv/Awesome-LLMSecOps) | `curated-list` | none | Security and operations for LLMs and agents. |
| [wearetyomsmnv/Awesome-LLM-agent-Security](https://github.com/wearetyomsmnv/Awesome-LLM-agent-Security) | `curated-list` | none | Vulnerabilities, threats, tools and research on agents. |
| [ucsb-mlsec/Awesome-Agent-Security](https://github.com/ucsb-mlsec/Awesome-Agent-Security) | `curated-list` | none | Agent security references. |
| [LLMSecurity/awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security) | `curated-list` | `LLMI-T008`, `LLMI-T011` | Attacks, defences and benchmarks for agent skills and tools. |
| [mcp-security-project/awesome-agentic-mcp-security](https://github.com/mcp-security-project/awesome-agentic-mcp-security) | `curated-list` | `LLMI-T008` | Security of agentic systems and MCP. |
| [ShenaoW/awesome-llm-supply-chain-security](https://github.com/ShenaoW/awesome-llm-supply-chain-security) | `curated-list` | `LLMI-T011` | LLM supply chain: papers, reports and CVEs. · **start here** |
| [scadastrangelove/awesome-ai-security-tools](https://github.com/scadastrangelove/awesome-ai-security-tools) | `curated-list` | none | Broad catalogue of AI security tools and AI applied to security. |
| [PromptLabs/Prompt-Hacking-Resources](https://github.com/PromptLabs/Prompt-Hacking-Resources) | `curated-list` | none | References on jailbreak, prompt injection and red teaming. |
| [forcesunseen/llm-hackers-handbook](https://github.com/forcesunseen/llm-hackers-handbook) | `curated-list` | none | Guide to LLM fundamentals, attacks and defences. |
<!-- gen:eco-catalog:end -->

### Evaluation tools, scanners and red teaming

<!-- gen:eco-evaluation:start -->
| Repository | Evidence class | Techniques | Scope |
|---|---|---|---|
| [NVIDIA/garak](https://github.com/NVIDIA/garak) | `assessment-tool` | none | LLM vulnerability scanner. · **start here** |
| [microsoft/PyRIT](https://github.com/microsoft/PyRIT) | `assessment-tool` | none | Framework for identifying risks in generative AI systems. · **start here** |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | `assessment-tool` | none | Security evaluation and testing of prompts, agents and RAG. |
| [confident-ai/deepteam](https://github.com/confident-ai/deepteam) | `assessment-tool` | none | Red teaming for LLMs and AI agents. |
| [cyberark/FuzzyAI](https://github.com/cyberark/FuzzyAI) | `assessment-tool` | `LLMI-T003` | Automated fuzzing to find weaknesses and jailbreaks. |
| [msoedov/agentic_security](https://github.com/msoedov/agentic_security) | `assessment-tool` | none | LLM vulnerability scanner and red-teaming kit. |
| [ReversecLabs/spikee](https://github.com/ReversecLabs/spikee) | `assessment-tool` | `LLMI-T001`, `LLMI-T002` | Prompt injection evaluation kit. |
| [Tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) | `assessment-tool` | `LLMI-T008` | Assessment of AI infrastructure, agents, skills, MCP and jailbreaks. |
| [LLAMATOR-Core/llamator](https://github.com/LLAMATOR-Core/llamator) | `assessment-tool` | none | Python framework for testing chatbots and GenAI systems. |
| [aiverify-foundation/moonshot](https://github.com/aiverify-foundation/moonshot) | `assessment-tool` | none | Modular evaluation and red teaming of LLM applications. |
| [LLMSecurity/HouYi](https://github.com/LLMSecurity/HouYi) | `research-technique` | `LLMI-T001`, `LLMI-T002` | Research and automation of prompt injection against LLM-integrated applications. |
| [praetorian-inc/augustus](https://github.com/praetorian-inc/augustus) | `assessment-tool` | `LLMI-T001`, `LLMI-T003` | Test framework for injection, jailbreaks and adversarial attacks. |
<!-- gen:eco-evaluation:end -->

### Benchmarks, datasets and environments

<!-- gen:eco-benchmark:start -->
| Repository | Evidence class | Techniques | Scope |
|---|---|---|---|
| [ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo) | `benchmark` | `LLMI-T002`, `LLMI-T008` | Environment for evaluating attacks and defences of LLM agents. · **start here** |
| [microsoft/BIPIA](https://github.com/microsoft/BIPIA) | `benchmark` | `LLMI-T002` | Benchmark for indirect prompt injection. · archived (as reported) |
| [liu00222/Open-Prompt-Injection](https://github.com/liu00222/Open-Prompt-Injection) | `benchmark` | `LLMI-T001`, `LLMI-T002` | Benchmark of prompt injection attacks and defences. |
| [JailbreakBench/jailbreakbench](https://github.com/JailbreakBench/jailbreakbench) | `benchmark` | `LLMI-T003` | Open benchmark of robustness against jailbreaks. |
| [centerforaisafety/HarmBench](https://github.com/centerforaisafety/HarmBench) | `benchmark` | `LLMI-T003` | Standardised evaluation of automated red teaming and refusals. |
| [agiresearch/ASB](https://github.com/agiresearch/ASB) | `benchmark` | `LLMI-T008` | Agent Security Bench. |
| [CheckPointSW/pint-benchmark](https://github.com/CheckPointSW/pint-benchmark) | `benchmark` | `LLMI-T001`, `LLMI-T002` | Benchmark for prompt injection detection systems. |
| [verazuo/jailbreak_llms](https://github.com/verazuo/jailbreak_llms) | `prompt-corpus` | `LLMI-T003` | Dataset and research on prompts and jailbreaks collected from public sources. |
| [agencyenterprise/PromptInject](https://github.com/agencyenterprise/PromptInject) | `benchmark` | `LLMI-T001` | Modular evaluation of LLM robustness to adversarial prompts. |
<!-- gen:eco-benchmark:end -->

### Attack technique research

<!-- gen:eco-attack-research:start -->
| Repository | Evidence class | Techniques | Scope |
|---|---|---|---|
| [greshake/llm-security](https://github.com/greshake/llm-security) | `research-technique` | `LLMI-T002` | Attacks on LLM-integrated applications, including indirect injection. |
| [llm-attacks/llm-attacks](https://github.com/llm-attacks/llm-attacks) | `research-technique` | `LLMI-T003` | Universal and transferable adversarial attacks on aligned models. |
| [patrickrchao/JailbreakingLLMs](https://github.com/patrickrchao/JailbreakingLLMs) | `research-technique` | `LLMI-T003` | Research code associated with the PAIR method. |
| [RICommunity/TAP](https://github.com/RICommunity/TAP) | `research-technique` | `LLMI-T003` | Automated jailbreaking of black-box models. |
| [SaFo-Lab/AutoDAN-Turbo](https://github.com/SaFo-Lab/AutoDAN-Turbo) | `research-technique` | `LLMI-T003` | Automated exploration of jailbreak strategies. |
| [tml-epfl/llm-adaptive-attacks](https://github.com/tml-epfl/llm-adaptive-attacks) | `research-technique` | `LLMI-T003` | Adaptive attacks on aligned LLMs. |
| [CHATS-lab/persuasive_jailbreaker](https://github.com/CHATS-lab/persuasive_jailbreaker) | `research-technique` | `LLMI-T003` | Persuasion-based jailbreaks. |
| [uw-nsl/ArtPrompt](https://github.com/uw-nsl/ArtPrompt) | `research-technique` | `LLMI-T003` | Research on ASCII-art-based attacks. |
| [tmlr-group/DeepInception](https://github.com/tmlr-group/DeepInception) | `research-technique` | `LLMI-T003` | Research on jailbreaks through scenario construction. |
| [AI-secure/AgentPoison](https://github.com/AI-secure/AgentPoison) | `research-technique` | `LLMI-T007`, `LLMI-T009` | Poisoning of agent memory or knowledge bases. |
| [trailofbits/anamorpher](https://github.com/trailofbits/anamorpher) | `research-technique` | `LLMI-T002` | Multimodal prompt injection through image resizing attacks. |
<!-- gen:eco-attack-research:end -->

### Defences, detection and controls

<!-- gen:eco-defence:start -->
| Repository | Evidence class | Techniques | Scope |
|---|---|---|---|
| [google-research/camel-prompt-injection](https://github.com/google-research/camel-prompt-injection) | `defence-tool` | `LLMI-T002`, `LLMI-T008` | Code for the research 'Defeating Prompt Injections by Design'. |
| [protectai/rebuff](https://github.com/protectai/rebuff) | `defence-tool` | `LLMI-T001`, `LLMI-T002` | Prompt injection detection. · archived (as reported) |
| [protectai/llm-guard](https://github.com/protectai/llm-guard) | `defence-tool` | `LLMI-T001`, `LLMI-T004` | Security controls for LLM interactions. · archived (as reported) |
| [deadbits/vigil-llm](https://github.com/deadbits/vigil-llm) | `defence-tool` | `LLMI-T001`, `LLMI-T003` | Detection of injections, jailbreaks and risky inputs. |
| [guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails) | `defence-tool` | none | Validation and controls for LLM applications. |
| [allenai/wildguard](https://github.com/allenai/wildguard) | `defence-tool` | `LLMI-T003` | Moderation and risk assessment for jailbreaks and refusals. |
| [protectai/modelscan](https://github.com/protectai/modelscan) | `defence-tool` | `LLMI-T010`, `LLMI-T011` | Model inspection against serialization risks. |
<!-- gen:eco-defence:end -->

### Agent, skill and MCP security

<!-- gen:eco-agent-security:start -->
| Repository | Evidence class | Techniques | Scope |
|---|---|---|---|
| [snyk/agent-scan](https://github.com/snyk/agent-scan) | `assessment-tool` | `LLMI-T008`, `LLMI-T011` | Scanner for agents, MCP servers and skills. |
| [cisco-ai-defense/mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) | `assessment-tool` | `LLMI-T008` | Threat and security inspection of MCP servers. |
| [cisco-ai-defense/skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) | `assessment-tool` | `LLMI-T008`, `LLMI-T011` | Security scanner for agent skills. |
| [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | `assessment-tool` | `LLMI-T002`, `LLMI-T004`, `LLMI-T011` | Skill analysis for injection, exfiltration and supply-chain risk. |
| [splx-ai/agentic-radar](https://github.com/splx-ai/agentic-radar) | `assessment-tool` | `LLMI-T008` | Security scanner for agentic workflows. |
| [scadastrangelove/agent-audit](https://github.com/scadastrangelove/agent-audit) | `assessment-tool` | none | Forensic audit of local agents, logs, configuration and instructions. |
| [garagon/aguara](https://github.com/garagon/aguara) | `assessment-tool` | `LLMI-T011` | Security analysis of agents and their supply chain. |
<!-- gen:eco-agent-security:end -->

### Labs, training and example collections

<!-- gen:eco-lab:start -->
| Repository | Evidence class | Techniques | Scope |
|---|---|---|---|
| [ReversecLabs/damn-vulnerable-llm-agent](https://github.com/ReversecLabs/damn-vulnerable-llm-agent) | `lab-exercise` | `LLMI-T008` | Deliberately vulnerable agent for training. |
| [dhammon/ai-goat](https://github.com/dhammon/ai-goat) | `lab-exercise` | none | Local LLM security challenges in CTF format. |
| [AISecurityConsortium/AIGoat](https://github.com/AISecurityConsortium/AIGoat) | `lab-exercise` | none | Security lab with scenarios related to the OWASP LLM Top 10. |
| [jthack/PIPE](https://github.com/jthack/PIPE) | `lab-exercise` | `LLMI-T001`, `LLMI-T002` | Introduction to prompt injection for engineers. |
| [LouisShark/chatgpt_system_prompt](https://github.com/LouisShark/chatgpt_system_prompt) | `prompt-corpus` | `LLMI-T004` | Collection of system prompts and material on prompt injection and leakage. |
<!-- gen:eco-lab:end -->

## How to add an entry

1. Add a record to [`data/ecosystem.json`](../data/ecosystem.json) with the next `ECO-` id, an evidence class, a section and a one-sentence scope taken from the project's own description.
2. Map `techniques` only where the project's stated scope clearly matches. Leave the list empty otherwise.
3. Record `provenance` honestly: who found it, when, and whether its state was verified.
4. Run `make validate readme` and commit the regenerated tables.
