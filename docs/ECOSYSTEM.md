# Ecosystem map

A hundred and six related GitHub projects, curated from research passes on 2026-10-07 and organised by what each can honestly support. What they contain, and what it changed here, is in the [ecosystem intelligence sweep](ECOSYSTEM-INTELLIGENCE.md).

**Provenance.** The list was supplied by the maintainer's own research and every entry was cross-checked by shallow clone on 2026-10-07: the *Last commit · License* column comes from the repository itself. GitHub's archive flag is not visible to git, so archived markers remain *as reported*. Re-run the check with `python scripts/verify_ecosystem.py`. Nothing here measures a tool's effectiveness.

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
| `framework-data` | Taxonomies and knowledge bases | Technique definitions and framework mappings | Observed activity | 7 |
| `incident-data` | Incident databases | Incident references, citing the primary report | Actor attribution or cyber campaigns (scope is broader than cybersecurity) | 1 |
| `detection-content` | Community detection rules | Detection ideas and telemetry requirements | Proof of in-the-wild behavior | 4 |
| `curated-list` | Curated lists | Discovering sources and tools | Any claim on their own | 22 |
| `assessment-tool` | Scanners and red-team tools | Test design and control evaluation | Effectiveness against current models | 28 |
| `benchmark` | Benchmarks and environments | Reproducible tests and coverage measurement | Real-world prevalence | 13 |
| `research-technique` | Attack research code | Techniques demonstrated in research | Use in the wild | 16 |
| `defence-tool` | Defences and guardrails | Control design and comparison | Proven protection | 10 |
| `lab-exercise` | Training labs | Analyst training and onboarding | Threat intelligence | 7 |
| `prompt-corpus` | Prompt corpora and datasets | Test inspiration and measurement | Threat intelligence or attribution | 7 |
<!-- gen:eco-classes:end -->

## Start here

Ten entries chosen as the highest-value inputs for taxonomy, evidence, tests and controls.

<!-- gen:eco-start:start -->
| Repository | Evidence class | Techniques | Last commit · License | Scope |
|---|---|---|---|---|
| [mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data) | `framework-data` | none | 2026-09-10 · Apache-2.0 | Data for tactics, techniques and case studies of threats against AI systems. · **start here** |
| [PLOT4ai/plot4ai-library](https://github.com/PLOT4ai/plot4ai-library) | `framework-data` | none | 2025-06-20 · CC | Threat library for AI threat modeling. · **start here** |
| [Arcanum-Sec/arc_pi_taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy) | `framework-data` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003` | 2026-06-29 · CC | Taxonomy specialised in prompt injection. · **start here** |
| [responsible-ai-collaborative/aiid](https://github.com/responsible-ai-collaborative/aiid) | `incident-data` | none | 2026-10-05 · Apache-2.0 | AI Incident Database: incidents and harms involving AI, broader than cybersecurity. · **start here** |
| [Agent-Threat-Rule/agent-threat-rules](https://github.com/Agent-Threat-Rule/agent-threat-rules) | `detection-content` | `LLMI-T001`, `LLMI-T002`, `LLMI-T004`, `LLMI-T008`, `LLMI-T009`, `LLMI-T011`, `LLMI-T018`, `LLMI-T021` | 2026-10-07 · MIT | Detection rules for agent threats, including injection, tools and MCP. · **start here** |
| [tldrsec/prompt-injection-defenses](https://github.com/tldrsec/prompt-injection-defenses) | `curated-list` | `LLMI-T001`, `LLMI-T002` | 2025-02-22 · none-found | Practical and proposed defences against prompt injection. · **start here** |
| [ShenaoW/awesome-llm-supply-chain-security](https://github.com/ShenaoW/awesome-llm-supply-chain-security) | `curated-list` | `LLMI-T011` | 2025-01-20 · CC | LLM supply chain: papers, reports and CVEs. · **start here** |
| [NVIDIA/garak](https://github.com/NVIDIA/garak) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T005`, `LLMI-T008`, `LLMI-T012`, `LLMI-T013`, `LLMI-T014`, `LLMI-T016`, `LLMI-T017` | 2026-10-07 · Apache-2.0 | LLM vulnerability scanner. · **start here** |
| [microsoft/PyRIT](https://github.com/microsoft/PyRIT) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T008`, `LLMI-T013`, `LLMI-T014` | 2026-10-07 · MIT | Framework for identifying risks in generative AI systems. · **start here** |
| [ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo) | `benchmark` | `LLMI-T001`, `LLMI-T002`, `LLMI-T004`, `LLMI-T008` | 2026-06-02 · MIT | Environment for evaluating attacks and defences of LLM agents. · **start here** |
| [OWASP/www-project-ai-testing-guide](https://github.com/OWASP/www-project-ai-testing-guide) | `framework-data` | none | 2026-06-01 · other | OWASP AI Testing Guide: 32 test procedures across application, data, infrastructure and model layers. · **start here** |
<!-- gen:eco-start:end -->

## All entries

### Knowledge bases, taxonomies and incident data

<!-- gen:eco-knowledge:start -->
| Repository | Evidence class | Techniques | Last commit · License | Scope |
|---|---|---|---|---|
| [mitre-atlas/atlas-data](https://github.com/mitre-atlas/atlas-data) | `framework-data` | none | 2026-09-10 · Apache-2.0 | Data for tactics, techniques and case studies of threats against AI systems. · **start here** |
| [mitre-atlas/atlas-website](https://github.com/mitre-atlas/atlas-website) | `framework-data` | none | 2026-09-15 · Apache-2.0 | Implementation of the ATLAS knowledge portal. |
| [OWASP/www-project-top-10-for-large-language-model-applications](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications) | `framework-data` | none | 2026-08-05 · CC | Risk taxonomy and security guidance for LLM applications. |
| [OWASP/www-project-ai-security-and-privacy-guide](https://github.com/OWASP/www-project-ai-security-and-privacy-guide) | `framework-data` | none | 2026-10-07 · none-found | Security and privacy references for AI systems. |
| [PLOT4ai/plot4ai-library](https://github.com/PLOT4ai/plot4ai-library) | `framework-data` | none | 2025-06-20 · CC | Threat library for AI threat modeling. · **start here** |
| [Arcanum-Sec/arc_pi_taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy) | `framework-data` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003` | 2026-06-29 · CC | Taxonomy specialised in prompt injection. · **start here** |
| [responsible-ai-collaborative/aiid](https://github.com/responsible-ai-collaborative/aiid) | `incident-data` | none | 2026-10-05 · Apache-2.0 | AI Incident Database: incidents and harms involving AI, broader than cybersecurity. · **start here** |
| [Agent-Threat-Rule/agent-threat-rules](https://github.com/Agent-Threat-Rule/agent-threat-rules) | `detection-content` | `LLMI-T001`, `LLMI-T002`, `LLMI-T004`, `LLMI-T008`, `LLMI-T009`, `LLMI-T011`, `LLMI-T018`, `LLMI-T021` | 2026-10-07 · MIT | Detection rules for agent threats, including injection, tools and MCP. · **start here** |
| [OWASP/www-project-ai-testing-guide](https://github.com/OWASP/www-project-ai-testing-guide) | `framework-data` | none | 2026-06-01 · other | OWASP AI Testing Guide: 32 test procedures across application, data, infrastructure and model layers. · **start here** |
<!-- gen:eco-knowledge:end -->

### Catalogs and awesome lists

<!-- gen:eco-catalog:start -->
| Repository | Evidence class | Techniques | Last commit · License | Scope |
|---|---|---|---|---|
| [corca-ai/awesome-llm-security](https://github.com/corca-ai/awesome-llm-security) | `curated-list` | none | 2025-08-20 · none-found | Tools, papers and projects on LLM security. |
| [Joe-B-Security/awesome-prompt-injection](https://github.com/Joe-B-Security/awesome-prompt-injection) | `curated-list` | `LLMI-T001`, `LLMI-T002` | 2026-09-11 · CC | Resources on prompt injection. |
| [tldrsec/prompt-injection-defenses](https://github.com/tldrsec/prompt-injection-defenses) | `curated-list` | `LLMI-T001`, `LLMI-T002` | 2025-02-22 · none-found | Practical and proposed defences against prompt injection. · **start here** |
| [user1342/Awesome-LLM-Red-Teaming](https://github.com/user1342/Awesome-LLM-Red-Teaming) | `curated-list` | none | 2025-09-04 · MIT | Training, tools and material for LLM red teaming. |
| [yueliu1999/Awesome-Jailbreak-on-LLMs](https://github.com/yueliu1999/Awesome-Jailbreak-on-LLMs) | `curated-list` | `LLMI-T003` | 2026-10-07 · MIT | Papers, code, datasets and evaluations of jailbreaks. |
| [cckuailong/awesome-gpt-security](https://github.com/cckuailong/awesome-gpt-security) | `curated-list` | none | 2026-07-24 · CC | Tools and experiments on GPT and LLM security. |
| [CryptoAILab/Awesome-LM-SSP](https://github.com/CryptoAILab/Awesome-LM-SSP) | `curated-list` | none | 2026-09-02 · Apache-2.0 | Literature on safety, security and privacy of large models. |
| [wearetyomsmnv/Awesome-LLMSecOps](https://github.com/wearetyomsmnv/Awesome-LLMSecOps) | `curated-list` | none | 2026-09-27 · none-found | Security and operations for LLMs and agents. |
| [wearetyomsmnv/Awesome-LLM-agent-Security](https://github.com/wearetyomsmnv/Awesome-LLM-agent-Security) | `curated-list` | none | 2026-07-11 · other | Vulnerabilities, threats, tools and research on agents. |
| [ucsb-mlsec/Awesome-Agent-Security](https://github.com/ucsb-mlsec/Awesome-Agent-Security) | `curated-list` | none | 2026-06-23 · none-found | Agent security references. |
| [LLMSecurity/awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security) | `curated-list` | `LLMI-T008`, `LLMI-T011` | 2026-10-08 · none-found | Attacks, defences and benchmarks for agent skills and tools. |
| [mcp-security-project/awesome-agentic-mcp-security](https://github.com/mcp-security-project/awesome-agentic-mcp-security) | `curated-list` | `LLMI-T008` | 2026-09-27 · CC0 | Security of agentic systems and MCP. |
| [ShenaoW/awesome-llm-supply-chain-security](https://github.com/ShenaoW/awesome-llm-supply-chain-security) | `curated-list` | `LLMI-T011` | 2025-01-20 · CC | LLM supply chain: papers, reports and CVEs. · **start here** |
| [scadastrangelove/awesome-ai-security-tools](https://github.com/scadastrangelove/awesome-ai-security-tools) | `curated-list` | none | 2026-10-05 · CC0 | Broad catalogue of AI security tools and AI applied to security. |
| [PromptLabs/Prompt-Hacking-Resources](https://github.com/PromptLabs/Prompt-Hacking-Resources) | `curated-list` | none | 2026-07-29 · MIT | References on jailbreak, prompt injection and red teaming. |
| [forcesunseen/llm-hackers-handbook](https://github.com/forcesunseen/llm-hackers-handbook) | `curated-list` | none | 2023-04-14 · none-found | Guide to LLM fundamentals, attacks and defences. |
| [pathakabhi24/LLM-MCP-Security-Field-Guide](https://github.com/pathakabhi24/LLM-MCP-Security-Field-Guide) | `curated-list` | `LLMI-T021` | 2026-04-19 · none-found | Field guide to LLM and MCP security aligned with OWASP. |
| [Puliczek/awesome-mcp-security](https://github.com/Puliczek/awesome-mcp-security) | `curated-list` | `LLMI-T021` | 2026-03-03 · none-found | Curated MCP security resources: specification guidance, audit checklists and scanners. |
| [Shiva108/ai-llm-red-team-handbook](https://github.com/Shiva108/ai-llm-red-team-handbook) | `curated-list` | none | 2026-05-08 · CC | AI/LLM red-team field handbook with methodology and test material. |
| [ydyjya/Awesome-LLM-Safety](https://github.com/ydyjya/Awesome-LLM-Safety) | `curated-list` | none | 2026-07-12 · none-found | Papers, tutorials and talks on LLM safety and alignment. |
| [swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) | `prompt-corpus` | `LLMI-T001`, `LLMI-T002` | 2026-08-27 · MIT | Offensive payload reference; its Prompt Injection section documents direct and indirect vectors. |
| [ubikron/Awesome-AI-OSINT](https://github.com/ubikron/Awesome-AI-OSINT) | `curated-list` | none | 2026-05-05 · none-found | AI tools for OSINT: geolocation, reverse image, dork generation and AI-assisted search. |
| [7WaySecurity/ai_osint](https://github.com/7WaySecurity/ai_osint) | `curated-list` | none | 2026-06-19 · MIT | Resources mixing OSINT and AI, including Sigma rules and threat-intel tooling. |
| [OpenOSINT/OpenOSINT](https://github.com/OpenOSINT/OpenOSINT) | `assessment-tool` | none | 2026-10-06 · MIT | LLM agent and MCP server chaining OSINT collectors with an entity graph; analyst tooling, not threat data. |
<!-- gen:eco-catalog:end -->

### Evaluation tools, scanners and red teaming

<!-- gen:eco-evaluation:start -->
| Repository | Evidence class | Techniques | Last commit · License | Scope |
|---|---|---|---|---|
| [NVIDIA/garak](https://github.com/NVIDIA/garak) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T005`, `LLMI-T008`, `LLMI-T012`, `LLMI-T013`, `LLMI-T014`, `LLMI-T016`, `LLMI-T017` | 2026-10-07 · Apache-2.0 | LLM vulnerability scanner. · **start here** |
| [microsoft/PyRIT](https://github.com/microsoft/PyRIT) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T008`, `LLMI-T013`, `LLMI-T014` | 2026-10-07 · MIT | Framework for identifying risks in generative AI systems. · **start here** |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T005`, `LLMI-T006`, `LLMI-T007`, `LLMI-T008`, `LLMI-T009`, `LLMI-T012`, `LLMI-T013`, `LLMI-T014`, `LLMI-T015`, `LLMI-T017`, `LLMI-T018`, `LLMI-T019` | 2026-10-07 · MIT | Security evaluation and testing of prompts, agents and RAG. |
| [confident-ai/deepteam](https://github.com/confident-ai/deepteam) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T007`, `LLMI-T008`, `LLMI-T009`, `LLMI-T014`, `LLMI-T015` | 2026-10-01 · Apache-2.0 | Red teaming for LLMs and AI agents. |
| [cyberark/FuzzyAI](https://github.com/cyberark/FuzzyAI) | `assessment-tool` | `LLMI-T001`, `LLMI-T003` | 2026-02-06 · Apache-2.0 | Automated fuzzing to find weaknesses and jailbreaks. |
| [msoedov/agentic_security](https://github.com/msoedov/agentic_security) | `assessment-tool` | `LLMI-T001`, `LLMI-T003`, `LLMI-T004`, `LLMI-T008`, `LLMI-T013` | 2026-09-22 · Apache-2.0 | LLM vulnerability scanner and red-teaming kit. |
| [ReversecLabs/spikee](https://github.com/ReversecLabs/spikee) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T007`, `LLMI-T017` | 2026-09-11 · Apache-2.0 | Prompt injection evaluation kit. |
| [Tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T006`, `LLMI-T008`, `LLMI-T009`, `LLMI-T010`, `LLMI-T011`, `LLMI-T013`, `LLMI-T016`, `LLMI-T018` | 2026-10-07 · Apache-2.0 | Assessment of AI infrastructure, agents, skills, MCP and jailbreaks. |
| [LLAMATOR-Core/llamator](https://github.com/LLAMATOR-Core/llamator) | `assessment-tool` | `LLMI-T001`, `LLMI-T003`, `LLMI-T004` | 2026-01-15 · CC | Python framework for testing chatbots and GenAI systems. |
| [aiverify-foundation/moonshot](https://github.com/aiverify-foundation/moonshot) | `assessment-tool` | `LLMI-T003` | 2026-02-05 · Apache-2.0 | Modular evaluation and red teaming of LLM applications. |
| [LLMSecurity/HouYi](https://github.com/LLMSecurity/HouYi) | `research-technique` | `LLMI-T001`, `LLMI-T002` | 2024-09-12 · Apache-2.0 | Research and automation of prompt injection against LLM-integrated applications. |
| [praetorian-inc/augustus](https://github.com/praetorian-inc/augustus) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T007`, `LLMI-T008`, `LLMI-T011`, `LLMI-T012`, `LLMI-T013`, `LLMI-T015`, `LLMI-T016`, `LLMI-T017` | 2026-10-03 · Apache-2.0 | Test framework for injection, jailbreaks and adversarial attacks. |
| [anmolksachan/LLMInjector](https://github.com/anmolksachan/LLMInjector) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T004` | 2026-04-06 · Apache-2.0 | Burp Suite extension that automates prompt-injection tests against HTTP endpoints backed by LLM APIs. |
| [regaan/basilisk](https://github.com/regaan/basilisk) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T005`, `LLMI-T007`, `LLMI-T008`, `LLMI-T009`, `LLMI-T015`, `LLMI-T019` | 2026-10-01 · AGPL-3.0 | AI red-team CLI with direct, indirect and tool-abuse modules and genetic prompt evolution (AGPL-3.0). |
| [perplext/LLMrecon](https://github.com/perplext/LLMrecon) | `assessment-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T005`, `LLMI-T006`, `LLMI-T007`, `LLMI-T008`, `LLMI-T009`, `LLMI-T010`, `LLMI-T011`, `LLMI-T014`, `LLMI-T015`, `LLMI-T018`, `LLMI-T019` | 2026-09-15 · MIT | LLM security testing framework organised around the OWASP LLM Top 10 with a large attack-module library. |
| [Mafifrizi/InjectionForgeProX](https://github.com/Mafifrizi/InjectionForgeProX) | `assessment-tool` | `LLMI-T001`, `LLMI-T004` | 2026-06-21 · MIT | Framework for authorised prompt-injection and sensitive-data-leak testing of chatbots and agents. |
| [byt3n33dl3/thc-BloodMiami](https://github.com/byt3n33dl3/thc-BloodMiami) | `assessment-tool` | `LLMI-T001`, `LLMI-T020` | 2025-11-14 · LGPL | Pentest tool for AI chat interfaces covering prompt injection and classic web injection through the chat channel. |
| [mikeperry-tor/HostileShop](https://github.com/mikeperry-tor/HostileShop) | `assessment-tool` | `LLMI-T002`, `LLMI-T008` | 2025-12-25 · MIT | Adversarial shopping-agent environment that generates injections and evaluates prompt filters against agents. |
| [jasoncobra3/LLM_Sentinel](https://github.com/jasoncobra3/LLM_Sentinel) | `assessment-tool` | `LLMI-T001`, `LLMI-T003` | 2026-03-05 · MIT | Single-turn red-team harness with a library of pre-written test prompts. |
| [meta-llama/PurpleLlama](https://github.com/meta-llama/PurpleLlama) | `assessment-tool` | `LLMI-T001`, `LLMI-T002` | 2026-09-29 · other | Meta umbrella project: CyberSecEval cybersecurity evals plus input/output safeguards (Llama Guard, Prompt Guard, LlamaFirewall, CodeShield). |
| [UKGovernmentBEIS/inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) | `assessment-tool` | none | 2026-10-09 · MIT | Library of evaluations on Inspect AI; includes agent-security and cyber-capability suites such as agentdojo, agentharm, cybench and cve_bench. |
<!-- gen:eco-evaluation:end -->

### Benchmarks, datasets and environments

<!-- gen:eco-benchmark:start -->
| Repository | Evidence class | Techniques | Last commit · License | Scope |
|---|---|---|---|---|
| [ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo) | `benchmark` | `LLMI-T001`, `LLMI-T002`, `LLMI-T004`, `LLMI-T008` | 2026-06-02 · MIT | Environment for evaluating attacks and defences of LLM agents. · **start here** |
| [microsoft/BIPIA](https://github.com/microsoft/BIPIA) | `benchmark` | `LLMI-T002`, `LLMI-T004` | 2024-04-15 · MIT | Benchmark for indirect prompt injection. · archived (as reported) |
| [liu00222/Open-Prompt-Injection](https://github.com/liu00222/Open-Prompt-Injection) | `benchmark` | `LLMI-T001`, `LLMI-T002` | 2026-09-27 · MIT | Benchmark of prompt injection attacks and defences. |
| [JailbreakBench/jailbreakbench](https://github.com/JailbreakBench/jailbreakbench) | `benchmark` | `LLMI-T003` | 2025-03-31 · MIT | Open benchmark of robustness against jailbreaks. |
| [centerforaisafety/HarmBench](https://github.com/centerforaisafety/HarmBench) | `benchmark` | `LLMI-T001`, `LLMI-T003` | 2024-08-05 · MIT | Standardised evaluation of automated red teaming and refusals. |
| [agiresearch/ASB](https://github.com/agiresearch/ASB) | `benchmark` | `LLMI-T001`, `LLMI-T002`, `LLMI-T006`, `LLMI-T008`, `LLMI-T009` | 2026-09-29 · MIT | Agent Security Bench. |
| [CheckPointSW/pint-benchmark](https://github.com/CheckPointSW/pint-benchmark) | `benchmark` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003` | 2026-04-02 · MIT | Benchmark for prompt injection detection systems. |
| [verazuo/jailbreak_llms](https://github.com/verazuo/jailbreak_llms) | `prompt-corpus` | `LLMI-T003` | 2024-12-24 · MIT | Dataset and research on prompts and jailbreaks collected from public sources. |
| [agencyenterprise/PromptInject](https://github.com/agencyenterprise/PromptInject) | `benchmark` | `LLMI-T001`, `LLMI-T004` | 2022-11-18 · MIT | Modular evaluation of LLM robustness to adversarial prompts. |
| [uiuc-kang-lab/InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent) | `benchmark` | `LLMI-T002`, `LLMI-T008` | 2024-07-02 · MIT | Benchmark of 1,054 test cases for indirect prompt injection against tool-integrated LLM agents (17 user tools, 62 attacker tools). |
| [SORRY-Bench/sorry-bench](https://github.com/SORRY-Bench/sorry-bench) | `benchmark` | `LLMI-T003` | 2025-03-01 · MIT | Benchmark of LLM safety refusal behaviour, with 20 linguistic mutations of each request. |
| [dsbowen/strong_reject](https://github.com/dsbowen/strong_reject) | `benchmark` | `LLMI-T003` | 2025-07-07 · MIT | StrongREJECT: forbidden-prompt dataset and autograder for scoring jailbreak responses; successor of alexandrasouly/strongreject, which is deprecated. |
| [xashru/cti-bench](https://github.com/xashru/cti-bench) | `benchmark` | none | 2026-05-07 · CC-BY-NC | CTIBench: evaluates LLMs on cyber threat intelligence tasks (CTI knowledge, CVE/CWE mapping, CVSS scoring, ATT&CK technique extraction, threat actor attribution). |
| [andyzorigin/cybench](https://github.com/andyzorigin/cybench) | `benchmark` | `LLMI-T015` | 2026-09-24 · Apache-2.0 | Cybench: 40 CTF tasks from four competitions for measuring LLM agent cybersecurity capability. A capability measure, not evidence of attacker use. |
<!-- gen:eco-benchmark:end -->

### Attack technique research

<!-- gen:eco-attack-research:start -->
| Repository | Evidence class | Techniques | Last commit · License | Scope |
|---|---|---|---|---|
| [greshake/llm-security](https://github.com/greshake/llm-security) | `research-technique` | `LLMI-T002`, `LLMI-T026` | 2025-07-17 · MIT | Attacks on LLM-integrated applications, including indirect injection. |
| [llm-attacks/llm-attacks](https://github.com/llm-attacks/llm-attacks) | `research-technique` | `LLMI-T003` | 2024-08-01 · MIT | Universal and transferable adversarial attacks on aligned models. |
| [patrickrchao/JailbreakingLLMs](https://github.com/patrickrchao/JailbreakingLLMs) | `research-technique` | `LLMI-T003` | 2024-12-01 · MIT | Research code associated with the PAIR method. |
| [RICommunity/TAP](https://github.com/RICommunity/TAP) | `research-technique` | `LLMI-T003` | 2024-03-08 · MIT | Automated jailbreaking of black-box models. |
| [SaFo-Lab/AutoDAN-Turbo](https://github.com/SaFo-Lab/AutoDAN-Turbo) | `research-technique` | `LLMI-T003` | 2025-10-08 · MIT | Automated exploration of jailbreak strategies. |
| [tml-epfl/llm-adaptive-attacks](https://github.com/tml-epfl/llm-adaptive-attacks) | `research-technique` | `LLMI-T003` | 2025-01-23 · MIT | Adaptive attacks on aligned LLMs. |
| [CHATS-lab/persuasive_jailbreaker](https://github.com/CHATS-lab/persuasive_jailbreaker) | `research-technique` | `LLMI-T003` | 2025-10-17 · Apache-2.0 | Persuasion-based jailbreaks. |
| [uw-nsl/ArtPrompt](https://github.com/uw-nsl/ArtPrompt) | `research-technique` | `LLMI-T003` | 2025-08-14 · MIT | Research on ASCII-art-based attacks. |
| [tmlr-group/DeepInception](https://github.com/tmlr-group/DeepInception) | `research-technique` | `LLMI-T003` | 2024-02-20 · MIT | Research on jailbreaks through scenario construction. |
| [AI-secure/AgentPoison](https://github.com/AI-secure/AgentPoison) | `research-technique` | `LLMI-T006`, `LLMI-T007`, `LLMI-T009` | 2026-10-06 · MIT | Poisoning of agent memory or knowledge bases. |
| [trailofbits/anamorpher](https://github.com/trailofbits/anamorpher) | `research-technique` | `LLMI-T002`, `LLMI-T025` | 2026-02-19 · Apache-2.0 | Multimodal prompt injection through image resizing attacks. |
| [crazywifi/Redteam_LLM_Injection_payloads](https://github.com/crazywifi/Redteam_LLM_Injection_payloads) | `prompt-corpus` | `LLMI-T001`, `LLMI-T002` | 2026-05-11 · none-found | Large categorised prompt-injection corpus; use only as test inspiration, never as intelligence. |
| [nukIeer/AI-Prompt-Injection-Cheatsheet](https://github.com/nukIeer/AI-Prompt-Injection-Cheatsheet) | `prompt-corpus` | `LLMI-T001`, `LLMI-T002`, `LLMI-T007` | 2026-06-04 · none-found | Cheatsheet of injection techniques against reasoning pipelines, tool use and RAG. |
| [2alf/prmptinj](https://github.com/2alf/prmptinj) | `prompt-corpus` | `LLMI-T001` | 2026-01-09 · none-found | Prompt-injection payloads used in public injection challenges. |
| [Insider77Circle/LLM-INJECTION-POC](https://github.com/Insider77Circle/LLM-INJECTION-POC) | `research-technique` | `LLMI-T002`, `LLMI-T025` | 2025-12-10 · none-found | Proof of concept for injection through uploaded files using hidden text and metadata poisoning. |
| [Asstar-X/JailPrompter](https://github.com/Asstar-X/JailPrompter) | `research-technique` | `LLMI-T003` | 2026-01-21 · none-found | Research project on jailbreak structures with attack and defence examples. |
| [allenai/wildteaming](https://github.com/allenai/wildteaming) | `research-technique` | `LLMI-T003` | 2024-08-10 · none-found | WildTeaming: mines in-the-wild user-chatbot interactions to discover jailbreak tactics; releases the WildJailbreak data. |
<!-- gen:eco-attack-research:end -->

### Defences, detection and controls

<!-- gen:eco-defence:start -->
| Repository | Evidence class | Techniques | Last commit · License | Scope |
|---|---|---|---|---|
| [google-research/camel-prompt-injection](https://github.com/google-research/camel-prompt-injection) | `defence-tool` | `LLMI-T002`, `LLMI-T008` | 2025-06-20 · Apache-2.0 | Code for the research 'Defeating Prompt Injections by Design'. |
| [protectai/rebuff](https://github.com/protectai/rebuff) | `defence-tool` | `LLMI-T001`, `LLMI-T002` | 2024-01-25 · Apache-2.0 | Prompt injection detection. · archived (as reported) |
| [protectai/llm-guard](https://github.com/protectai/llm-guard) | `defence-tool` | `LLMI-T001`, `LLMI-T004` | 2026-07-09 · MIT | Security controls for LLM interactions. · archived (as reported) |
| [deadbits/vigil-llm](https://github.com/deadbits/vigil-llm) | `defence-tool` | `LLMI-T001`, `LLMI-T003` | 2024-01-31 · Apache-2.0 | Detection of injections, jailbreaks and risky inputs. |
| [guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails) | `defence-tool` | `LLMI-T020` | 2026-08-26 · Apache-2.0 | Validation and controls for LLM applications. |
| [allenai/wildguard](https://github.com/allenai/wildguard) | `defence-tool` | `LLMI-T003` | 2024-12-02 · Apache-2.0 | Moderation and risk assessment for jailbreaks and refusals. |
| [protectai/modelscan](https://github.com/protectai/modelscan) | `defence-tool` | `LLMI-T010`, `LLMI-T011` | 2026-02-18 · Apache-2.0 | Model inspection against serialization risks. |
| [maheshmakvana/llm-injection-guard](https://github.com/maheshmakvana/llm-injection-guard) | `defence-tool` | `LLMI-T001`, `LLMI-T002` | 2026-04-10 · none-found | Python library for detecting, blocking and auditing prompt-injection attempts in LLM apps and agents. |
| [rana-m-ahmed/Anti-LLM-Injection-Gateway](https://github.com/rana-m-ahmed/Anti-LLM-Injection-Gateway) | `defence-tool` | `LLMI-T001`, `LLMI-T002` | 2026-09-13 · none-found | Lightweight pre-inference gateway applying block, mask or allow decisions to injection indicators. |
| [NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | `defence-tool` | `LLMI-T001`, `LLMI-T002`, `LLMI-T004` | 2026-10-07 · Apache-2.0 | Programmable guardrails toolkit for dialogue rails, PII masking, fact checking and injection blocking. |
| [microsoft/BinaryShield](https://github.com/microsoft/BinaryShield) | `detection-content` | `LLMI-T001`, `LLMI-T003`, `LLMI-T019` | 2026-08-03 · MIT | Research on privacy-preserving sharing of LLM threat fingerprints across services. |
| [OMGstacks/llm-threat-triage](https://github.com/OMGstacks/llm-threat-triage) | `detection-content` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003`, `LLMI-T004`, `LLMI-T008` | 2026-08-17 · MIT | Python and SQL triage toolkit flagging injection, jailbreak and exfiltration mapped to OWASP LLM Top 10. |
| [feedly/skills](https://github.com/feedly/skills) | `detection-content` | none | 2026-10-07 · MIT | Feedly's CTI skills and prompts for Claude (MIT): ATT&CK technique mapping with Navigator 4.5 layers, Sigma rule drafting validated with sigma-cli, intelligence-requirements and risk-reduction reporting. ATT&CK only; no ATLAS content found. |
<!-- gen:eco-defence:end -->

### Agent, skill and MCP security

<!-- gen:eco-agent-security:start -->
| Repository | Evidence class | Techniques | Last commit · License | Scope |
|---|---|---|---|---|
| [snyk/agent-scan](https://github.com/snyk/agent-scan) | `assessment-tool` | `LLMI-T004`, `LLMI-T008`, `LLMI-T011`, `LLMI-T017`, `LLMI-T018` | 2026-10-06 · Apache-2.0 | Scanner for agents, MCP servers and skills. |
| [cisco-ai-defense/mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) | `assessment-tool` | `LLMI-T002`, `LLMI-T004`, `LLMI-T008`, `LLMI-T011`, `LLMI-T018` | 2026-10-07 · Apache-2.0 | Threat and security inspection of MCP servers. |
| [cisco-ai-defense/skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) | `assessment-tool` | `LLMI-T002`, `LLMI-T004`, `LLMI-T008`, `LLMI-T011`, `LLMI-T012`, `LLMI-T015` | 2026-10-05 · Apache-2.0 | Security scanner for agent skills. |
| [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | `assessment-tool` | `LLMI-T002`, `LLMI-T004`, `LLMI-T008`, `LLMI-T009`, `LLMI-T011`, `LLMI-T012`, `LLMI-T016`, `LLMI-T018` | 2026-10-07 · Apache-2.0 | Skill analysis for injection, exfiltration and supply-chain risk. |
| [splx-ai/agentic-radar](https://github.com/splx-ai/agentic-radar) | `assessment-tool` | `LLMI-T002`, `LLMI-T007`, `LLMI-T008`, `LLMI-T011` | 2025-11-27 · Apache-2.0 | Security scanner for agentic workflows. |
| [scadastrangelove/agent-audit](https://github.com/scadastrangelove/agent-audit) | `assessment-tool` | `LLMI-T004`, `LLMI-T008`, `LLMI-T011`, `LLMI-T015`, `LLMI-T017`, `LLMI-T018` | 2026-07-16 · MIT | Forensic audit of local agents, logs, configuration and instructions. |
| [garagon/aguara](https://github.com/garagon/aguara) | `assessment-tool` | `LLMI-T004`, `LLMI-T008`, `LLMI-T011`, `LLMI-T012`, `LLMI-T016`, `LLMI-T017`, `LLMI-T018` | 2026-09-10 · Apache-2.0 | Security analysis of agents and their supply chain. |
| [invariantlabs-ai/mcp-injection-experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments) | `research-technique` | `LLMI-T004`, `LLMI-T008`, `LLMI-T011`, `LLMI-T021` | 2025-04-10 · none-found | Experiments on MCP tool poisoning, shadowing and exfiltration via malicious tool descriptions. |
<!-- gen:eco-agent-security:end -->

### Labs, training and example collections

<!-- gen:eco-lab:start -->
| Repository | Evidence class | Techniques | Last commit · License | Scope |
|---|---|---|---|---|
| [ReversecLabs/damn-vulnerable-llm-agent](https://github.com/ReversecLabs/damn-vulnerable-llm-agent) | `lab-exercise` | `LLMI-T002`, `LLMI-T008` | 2025-06-25 · Apache-2.0 | Deliberately vulnerable agent for training. |
| [dhammon/ai-goat](https://github.com/dhammon/ai-goat) | `lab-exercise` | `LLMI-T001` | 2024-08-21 · GPL | Local LLM security challenges in CTF format. |
| [AISecurityConsortium/AIGoat](https://github.com/AISecurityConsortium/AIGoat) | `lab-exercise` | `LLMI-T001`, `LLMI-T002`, `LLMI-T020` | 2026-04-24 · Apache-2.0 | Security lab with scenarios related to the OWASP LLM Top 10. |
| [jthack/PIPE](https://github.com/jthack/PIPE) | `lab-exercise` | `LLMI-T001`, `LLMI-T002` | 2023-08-25 · none-found | Introduction to prompt injection for engineers. |
| [LouisShark/chatgpt_system_prompt](https://github.com/LouisShark/chatgpt_system_prompt) | `prompt-corpus` | `LLMI-T004` | 2026-09-30 · MIT | Collection of system prompts and material on prompt injection and leakage. |
| [Autonoma-Tools/how-to-test-for-prompt-injection](https://github.com/Autonoma-Tools/how-to-test-for-prompt-injection) | `prompt-corpus` | `LLMI-T001`, `LLMI-T004` | 2026-07-28 · MIT | Test payload guide for jailbreak, system-prompt leakage and data exfiltration checks. |
| [shreyansbhatt/rag-prompt-injection-echoleak](https://github.com/shreyansbhatt/rag-prompt-injection-echoleak) | `lab-exercise` | `LLMI-T002`, `LLMI-T007`, `LLMI-T020` | 2026-06-07 · MIT | Lab reproducing an EchoLeak-style injection and exfiltration against a defended RAG application. |
| [microsoft/AI-Red-Teaming-Playground-Labs](https://github.com/microsoft/AI-Red-Teaming-Playground-Labs) | `lab-exercise` | `LLMI-T001`, `LLMI-T002`, `LLMI-T003` | 2025-10-07 · MIT | Hands-on AI red-teaming challenges used in Microsoft training, including injection scenarios. |
| [Wisdomajoku/ai-redteam-journey](https://github.com/Wisdomajoku/ai-redteam-journey) | `lab-exercise` | `LLMI-T001` | 2026-09-15 · none-found | Learning log for AI red teaming with Burp Suite based LLM testing notes. |
<!-- gen:eco-lab:end -->

## How to add an entry

1. Add a record to [`data/ecosystem.json`](../data/ecosystem.json) with the next `ECO-` id, an evidence class, a section and a one-sentence scope taken from the project's own description.
2. Map `techniques` only where the project's stated scope clearly matches. Leave the list empty otherwise.
3. Record `provenance` honestly: who found it, when, and whether its state was verified.
4. Run `make validate readme` and commit the regenerated tables.
