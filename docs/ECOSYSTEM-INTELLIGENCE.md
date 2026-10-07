# Ecosystem intelligence sweep, 2026-10-07

What 107 related repositories actually contain, read from shallow clones on 2026-10-07, and what that changed in LLMInjection. Machine-readable versions of every table live in [`references/crosswalks/`](../references/crosswalks/).

> **Evidence rule.** Nothing on this page is in-the-wild evidence. Tools, rules and benchmarks inform tests, detections, controls and taxonomy. Incidents added in this sweep come from MITRE ATLAS case studies (grade A), not from the repositories.

## 1. How the sweep was run

| Step | What happened |
|---|---|
| Inputs | Four research lists supplied by the maintainer: 109 distinct GitHub references after de-duplication |
| Verification | `git clone --depth 1` of every repository (no API token). 107 cloned; `mlcommons/jailbreak` does not exist (auth prompt on a public host); `tencent/AI-Infra-Guard` is the same repository as `Tencent/AI-Infra-Guard` |
| Metadata | Last commit date and licence family read from each clone and stored in `ecosystem[].verification` |
| Mining | Rule sets, probe modules, taxonomies, test catalogues, benchmark suites and scanner checks were enumerated by name only. No payload text was copied and no repository code was executed |
| Re-run | `python scripts/verify_ecosystem.py [--write]` repeats the verification step with git alone |

Claims from the input lists that did **not** hold up: `mlcommons/jailbreak` is not a public repository; "llm-guard archived in mid-2026" is consistent with the clone (last commit 2026-07-09, deprecation notice in README) but GitHub's archive flag cannot be read by git, so `archived-reported` stays as reported; `llm-threatintel.com` and the Hugging Face dataset are not GitHub repositories and stay out of `ecosystem.json`.

## 2. What changed in the datasets

| Dataset | Before | After | Source of the additions |
|---|---:|---:|---|
| Techniques | 19 | 26 | ATLAS 2026.09 techniques with no LLMInjection equivalent (T020–T026) |
| ATLAS mappings on techniques | 18 | 78 | ATLAS crosswalk; T017–T019 had none |
| Test cases | 20 | 34 | Red-team tool module families with no test (TC-OBF-021 … TC-EXP-034) |
| Detections | 14 | 39 | Agent Threat Rules, agent/MCP/skill scanners, ATLAS case studies |
| Controls | 20 | 31 | tl;dr sec defence catalogue, CaMeL, MCP tool pinning |
| Incidents | 7 | 29 | ATLAS case studies (13 incidents, 9 research exercises) |
| Relationships | 75 | 174 | Every new record is linked to a technique |
| Sources | 40 | 50 | Repositories now cited as evidence for detections and controls |
| Ecosystem | 75 | 106 | 31 verified additions; all entries now carry verification and technique tags |
| Research queue | 0 | 47 | Repositories cited by three or more curated lists, not yet verified |

### New techniques

| ID | Name | ATLAS anchor | Why it earned its own ID |
|---|---|---|---|
| `LLMI-T020` | Improper Output Handling and Rendering Exfiltration | `AML.T0077` | Distinct telemetry (renderer, egress); EchoLeak, Lenovo chatbot XSS |
| `LLMI-T021` | Agent Tool Poisoning and Rug Pull | `AML.T0110`, `AML.T0109` | 113 ATR tool-poisoning rules; Postmark MCP incident |
| `LLMI-T022` | Agentic Resource Consumption and Cost Harvesting | `AML.T0034.002` | OWASP AITG-INF-02 and TC-COST-014 had no technique |
| `LLMI-T023` | Crafted AI Assistant Links and Recommendation Poisoning | `AML.T0131` | ATLAS incident CS0072: 31 companies, 14 industries |
| `LLMI-T024` | Exposed or Misconfigured AI Services | `AML.T0132` | Langflow/n8n exploitation (CS0070), ShadowRay |
| `LLMI-T025` | Multimodal Instruction Triggers | `AML.T0129` | Image-scaling and audio injection research; 18 related case studies |
| `LLMI-T026` | Inter-Agent Instruction Propagation | `AML.T0118`, `AML.T0061` | Morris II, multi-agent Taiwan intrusion (CS0071) |

Candidates held back for review (raised by ATR and the tool sweep, not yet distinct enough): human-approval gate subversion, model-supplied tool-argument injection (today covered by TC-PARAM-019), MCP protocol abuse (sampling, DNS rebinding), AI content provenance stripping.

## 3. MITRE ATLAS crosswalk

ATLAS 2026.09 has 208 techniques and sub-techniques, 73 case studies and 40 mitigations. Of the 139 that apply to generative or agentic AI, LLMInjection now covers **109 (78%)**, up from 73 (52%). The 23 uncovered ones are mostly resource development and impact categories (Obtain Capabilities, External Harms, Verify Attack), which describe adversary logistics rather than attack techniques against AI systems.

| Technique | ATLAS IDs | ATLAS case studies |
|---|---|---|
| `LLMI-T001` Direct Prompt Injection | `AML.T0051.000`, `AML.T0068`, `AML.T0093`, `AML.T0065` | CS0016, CS0020, CS0021, CS0024, CS0026, CS0029, CS0035, CS0036 +23 |
| `LLMI-T002` Indirect Prompt Injection | `AML.T0051.001`, `AML.T0051.002`, `AML.T0066` | CS0020, CS0021, CS0024, CS0026, CS0029, CS0035, CS0037, CS0038 +14 |
| `LLMI-T003` Jailbreak / Safety Boundary Manipulation | `AML.T0054` | CS0041, CS0046, CS0051, CS0052, CS0057, CS0063, CS0066, CS0067 +1 |
| `LLMI-T004` Sensitive Information Disclosure | `AML.T0057`, `AML.T0056`, `AML.T0069`, `AML.T0085` | CS0024, CS0067 |
| `LLMI-T005` Model Extraction / Theft | `AML.T0044` | CS0013, CS0027, CS0028, CS0058 |
| `LLMI-T006` Data or Model Poisoning | `AML.T0020`, `AML.T0018`, `AML.T0115.000`, `AML.T0059` | CS0002, CS0009, CS0025 |
| `LLMI-T007` RAG Knowledge Poisoning | `AML.T0070`, `AML.T0071`, `AML.T0082`, `AML.T0064` | CS0026, CS0035, CS0059 |
| `LLMI-T008` Agent Tool Misuse | `AML.T0053`, `AML.T0086`, `AML.T0101`, `AML.T0100`, `AML.T0085.001` | CS0016, CS0021, CS0024, CS0026, CS0037, CS0038, CS0039, CS0045 +15 |
| `LLMI-T009` Memory / Context Poisoning | `AML.T0080`, `AML.T0094`, `AML.T0080.000`, `AML.T0092` | CS0036, CS0038, CS0040, CS0048, CS0063, CS0066, CS0072 |
| `LLMI-T010` Model Source Tampering | `AML.T0010.003`, `AML.T0115.001`, `AML.T0011.000`, `AML.T0076` | CS0013, CS0019, CS0023, CS0027, CS0031, CS0064, CS0065 |
| `LLMI-T011` AI Software Supply Chain Compromise | `AML.T0010`, `AML.T0010.001` | CS0015, CS0018, CS0022, CS0031, CS0041, CS0047 |
| `LLMI-T012` Coding-Agent Dependency Manipulation | `AML.T0111`, `AML.T0060`, `AML.T0062` | CS0022, CS0049 |
| `LLMI-T013` Runtime LLM Command Generation | `AML.T0102`, `AML.T0096` | CS0042, CS0044, CS0068, CS0070 |
| `LLMI-T014` AI-Assisted Reconnaissance and Social Engineering | `AML.T0052.000` | CS0020 |
| `LLMI-T015` Agentic Attack Orchestration | `AML.T0124`, `AML.T0116`, `AML.T0117`, `AML.T0017.001` | CS0068, CS0069, CS0070, CS0071 |
| `LLMI-T016` AI Gateway Credential Compromise | `AML.T0083`, `AML.T0098`, `AML.T0040` | CS0005, CS0010, CS0011, CS0012, CS0022, CS0024, CS0045, CS0048 +6 |
| `LLMI-T017` Prompt Injection Against AI Security Scanners | `AML.T0051.001`, `AML.T0015`, `AML.T0134` | CS0000, CS0001, CS0003, CS0004, CS0005, CS0008, CS0010, CS0011 +28 |
| `LLMI-T018` AI Coding-Assistant Workspace Abuse | `AML.T0081`, `AML.T0084`, `AML.T0112.000`, `AML.T0002.002` | CS0041, CS0050, CS0051, CS0052, CS0055, CS0063 |
| `LLMI-T019` Model Distillation Campaign | `AML.T0024.002`, `AML.T0005` | CS0000, CS0012, CS0014, CS0056 |
| `LLMI-T020` Improper Output Handling and Rendering Exfiltration | `AML.T0077`, `AML.T0067` | CS0021, CS0029, CS0035, CS0041, CS0059, CS0060, CS0064 |
| `LLMI-T021` Agent Tool Poisoning and Rug Pull | `AML.T0110`, `AML.T0011.002`, `AML.T0010.005`, `AML.T0109`, `AML.T0115.002` | CS0049, CS0053, CS0054 |
| `LLMI-T022` Agentic Resource Consumption and Cost Harvesting | `AML.T0034.002`, `AML.T0034`, `AML.T0029` | CS0016, CS0036 |
| `LLMI-T023` Crafted AI Assistant Links and Recommendation Poisoning | `AML.T0131`, `AML.T0130`, `AML.T0080.000` | CS0036, CS0040, CS0066, CS0072 |
| `LLMI-T024` Exposed or Misconfigured AI Services | `AML.T0132`, `AML.T0006.002`, `AML.T0006` | CS0023, CS0048, CS0063, CS0069, CS0070, CS0071 |
| `LLMI-T025` Multimodal Instruction Triggers | `AML.T0129`, `AML.T0051.001` | CS0020, CS0021, CS0026, CS0029, CS0035, CS0038, CS0039, CS0040 +10 |
| `LLMI-T026` Inter-Agent Instruction Propagation | `AML.T0118`, `AML.T0061` | CS0024 |


Case-study counts include related (not exact) mappings, so broad anchors such as `AML.T0015` inflate T017.

## 4. Red-team tool coverage

Thirteen evaluation tools expose 874 named modules. The matrix shows which tools can automate a test for each technique.

| Technique | Tools | Coverage |
|---|---|---|
| `LLMI-T001` Direct Prompt Injection | garak, PyRIT, promptfoo, deepteam, FuzzyAI, spikee, augustus, agentic_sec, LLAMATOR, basilisk, LLMrecon, AI-Infra-Guard | strong |
| `LLMI-T002` Indirect Prompt Injection | garak, PyRIT, promptfoo, deepteam, spikee, augustus, basilisk, LLMrecon, AI-Infra-Guard | strong |
| `LLMI-T003` Jailbreak / Safety Boundary Manipulation | garak, PyRIT, promptfoo, deepteam, FuzzyAI, spikee, augustus, agentic_sec, LLAMATOR, moonshot, basilisk, LLMrecon, AI-Infra-Guard | strong |
| `LLMI-T004` Sensitive Information Disclosure | garak, PyRIT, promptfoo, deepteam, spikee, augustus, agentic_sec, LLAMATOR, basilisk, LLMrecon, AI-Infra-Guard | strong |
| `LLMI-T005` Model Extraction / Theft | promptfoo, basilisk, LLMrecon, garak | moderate |
| `LLMI-T006` Data or Model Poisoning | promptfoo, LLMrecon, AI-Infra-Guard | weak |
| `LLMI-T007` RAG Knowledge Poisoning | promptfoo, spikee, basilisk, LLMrecon, augustus, deepteam | moderate |
| `LLMI-T008` Agent Tool Misuse | promptfoo, deepteam, augustus, garak, PyRIT, basilisk, LLMrecon, agentic_sec, AI-Infra-Guard | strong |
| `LLMI-T009` Memory / Context Poisoning | promptfoo, deepteam, basilisk, LLMrecon, AI-Infra-Guard | moderate |
| `LLMI-T010` Model Source Tampering | AI-Infra-Guard, LLMrecon | weak |
| `LLMI-T011` AI Software Supply Chain Compromise | LLMrecon, AI-Infra-Guard, augustus | weak |
| `LLMI-T012` Coding-Agent Dependency Manipulation | garak, augustus, promptfoo | weak |
| `LLMI-T013` Runtime LLM Command Generation | garak, augustus, promptfoo, agentic_sec, PyRIT, AI-Infra-Guard | moderate |
| `LLMI-T014` AI-Assisted Reconnaissance and Social Engineering | promptfoo, PyRIT, LLMrecon, garak, deepteam | moderate |
| `LLMI-T015` Agentic Attack Orchestration | LLMrecon, augustus, deepteam, promptfoo, basilisk | moderate |
| `LLMI-T016` AI Gateway Credential Compromise | AI-Infra-Guard, augustus, garak | weak |
| `LLMI-T017` Prompt Injection Against AI Security Scanners | garak, augustus, spikee, promptfoo | moderate |
| `LLMI-T018` AI Coding-Assistant Workspace Abuse | promptfoo, LLMrecon, AI-Infra-Guard | weak |
| `LLMI-T019` Model Distillation Campaign | LLMrecon, basilisk, promptfoo | weak |
**Reading it.** Prompt-level techniques (T001–T004, T008) are saturated with tooling. Infrastructure and supply-chain techniques (T010, T011, T016, T019) are not testable with prompt probes at all; they need artifact hashing, canary credentials and volumetric simulation, which is where LLMInjection's own test cases add value.

Licence watch: LLAMATOR is CC-BY-NC-SA-4.0 (no commercial use); basilisk is AGPL-3.0.

## 5. Agent Threat Rules (ATR)

829 YAML rules (MIT, commit of 2026-10-07): prompt-injection 252, context-exfiltration 135, tool-poisoning 113, agent-manipulation 108, privilege-escalation 76, skill-compromise 52, model-abuse 41, excessive-autonomy 39, data-poisoning 9, model-security 4. 790 are regex pattern rules and 763 are `experimental`; the project has withdrawn its published false-positive rates. LLMInjection therefore uses ATR as a **source of hypotheses**: eight rules became detection specifications DET-AI-026 to DET-AI-033, written as hypothesis plus telemetry, not copied patterns.

No ATR coverage: T013 (runtime command generation) and T017 (injection against AI scanners).

## 6. Agent, MCP, skill and model scanners

| Scanner | Scans | Output | Main techniques |
|---|---|---|---|
| cisco-ai-defense/mcp-scanner | Live MCP servers, client configs, tool JSON, source | JSON, tables | T008, T011, T021, T018 |
| cisco-ai-defense/skill-scanner | Skill bundles (784 YAML rules + LLM judge) | SARIF, JSON, HTML | T011, T008, T004 |
| snyk/agent-scan | Agents, MCP servers, skills, client configs | JSON | T008, T011, T018 |
| NVIDIA/SkillSpector | Skills (~71 patterns, 17 categories) | SARIF, JSON | T002, T004, T011 |
| garagon/aguara | Agents and supply chain (258 checks incl. AGENTCFG_*, RUGPULL_001) | SARIF, JSON | T018, T021, T011 |
| splx-ai/agentic-radar | Agentic workflow code | HTML, JSON | T008 |
| scadastrangelove/agent-audit | Local agent logs, configs, instructions (forensics) | JSON bundle | T018, T008 |
| Tencent/AI-Infra-Guard | AI infra CVEs, MCP, agents, jailbreak eval | JSON, UI | T010, T011, T016, T024 |
| protectai/modelscan | Model files (pickle, Keras, SavedModel) | JSON | T010 |

Cisco's own figures are the clearest warning in the sweep: static rules alone caught 7.7% of malicious skills; adding an LLM judge raised it to 66.7% at 15.4% false positives. Detections DET-AI-015 to DET-AI-025 therefore pair content checks with behaviour (process, egress, config diff).

## 7. Benchmarks

| Benchmark | Measures | Metrics | Last commit | Techniques |
|---|---|---|---|---|
| AgentDojo | Injection robustness of tool-using agents; 97 user × 27 injection tasks | Benign utility, utility under attack, targeted ASR | 2026-06-02 | T002, T008, T004 |
| ASB | 10 scenarios, 400 attack tools, 13 backbones | ASR, refusal rate, PNA | 2026-09-29 | T001, T002, T008, T009 |
| AgentPoison | Memory and knowledge-base backdoors in RAG agents | ASR-r/a/t, accuracy | 2026-10-06 | T007, T009 |
| PINT | Injection detector accuracy, 4,314 inputs with hard negatives | Balanced accuracy | 2026-04-02 | T001, T002 |
| Open-Prompt-Injection | Target × injected task matrix, detection and localisation | ASV, MR, PNA | 2026-09-27 | T001, T002 |
| BIPIA (archived as reported) | Indirect injection in email, web, table, code apps | ASR, task quality | 2024-04-15 | T002 |
| HarmBench | 510 behaviours, 18 red-team methods | Judged ASR | 2024-08-05 | T003 |
| JailbreakBench | 100 harmful + 100 benign behaviours | ASR, benign refusal | 2025-03-31 | T003 |

Results are reproducible only against the dated model snapshots each paper used; several (gpt-4o-2024-05-13, PaLM 2) are retired. Treat cross-paper ASR comparisons as indicative.

## 8. Taxonomy crosswalks

- **Arcanum PI taxonomy 1.6.1:** 172 nodes (27 intents, 70 techniques, 63 evasions, 12 inputs). Evasions are encoding layers on top of a technique and matter for detection normalisation; see [`arcanum-pi-taxonomy.json`](../references/crosswalks/arcanum-pi-taxonomy.json).
- **PLOT4ai:** 138 threats in 8 categories; 46 are security-relevant to LLMs and agents and are mapped in [`plot4ai.json`](../references/crosswalks/plot4ai.json).
- **OWASP Top 10 check:** the OWASP repository in the sweep is a legacy archive holding the 2025 list and the Agentic draft; the 2026 list lives in `GenAI-Security-Project/GenAI-LLM-Top10`. The `LLMxx:2026` IDs used here could not be re-verified from it, and the draft names ASI01 "Agent Behaviour Hijack" where LLMInjection uses "Goal Hijack". Open item in the roadmap.

### OWASP AI Testing Guide (32 tests)

Mapping made against the 20 original test cases. The new TC-SC-027 now covers AITG-APP-11 and TC-DOS-026 covers AITG-INF-02.

| AITG test | Title | LLMI | Test case | Match |
|---|---|---|---|---|
| `AITG-APP-01` | Testing for Prompt Injection | LLMI-T001, LLMI-T003 | TC-PI-001 | exact |
| `AITG-APP-02` | Testing for Indirect Prompt Injection | LLMI-T002 | TC-PI-002 | exact |
| `AITG-APP-03` | Testing for Sensitive Data Leak | LLMI-T004 | TC-DL-003 | exact |
| `AITG-APP-04` | Testing for Input Leakage | LLMI-T004, LLMI-T009 | TC-DL-003 | partial |
| `AITG-APP-05` | Testing for Unsafe Outputs | LLMI-T003 | TC-OH-013 | partial |
| `AITG-APP-06` | Testing for Agentic Behavior Limits | LLMI-T008, LLMI-T015 | TC-AG-005, TC-AG-006, TC-AUTO-015, TC-COST-014, TC-PARAM-019 | exact |
| `AITG-APP-07` | Testing for Prompt Disclosure | LLMI-T004 | TC-DL-003 | partial |
| `AITG-APP-08` | Testing for Embedding Manipulation | LLMI-T007 | TC-RAG-004 | exact |
| `AITG-APP-09` | Testing for Model Extraction | LLMI-T005, LLMI-T019 | TC-DIST-018 | partial |
| `AITG-APP-10` | Testing for Content Bias | — | — | none |
| `AITG-APP-11` | Testing for Hallucinations | LLMI-T012 | — | none |
| `AITG-APP-12` | Testing for Toxic Output | LLMI-T003 | — | none |
| `AITG-APP-13` | Testing for Over-Reliance on AI | — | — | none |
| `AITG-APP-14` | Testing for Explainability and Interpretability | — | — | none |
| `AITG-DAT-01` | Testing for Training Data Exposure | LLMI-T004 | — | none |
| `AITG-DAT-02` | Testing for Runtime Exfiltration | LLMI-T004, LLMI-T002 | TC-DL-003, TC-GW-020 | partial |
| `AITG-DAT-03` | Testing for Dataset Diversity & Coverage | — | — | none |
| `AITG-DAT-04` | Testing for Harmful Content in Data | LLMI-T006 | — | none |
| `AITG-DAT-05` | Testing for Data Minimization & Consent | LLMI-T004 | — | none |
| `AITG-INF-01` | Testing for Supply Chain Tampering | LLMI-T010, LLMI-T011, LLMI-T012 | TC-SC-009, TC-SC-008 | exact |
| `AITG-INF-02` | Testing for Resource Exhaustion | — | TC-COST-014 | exact-test-no-technique |
| `AITG-INF-03` | Testing for Plugin Boundary Violations | LLMI-T008, LLMI-T011 | TC-MCP-010, TC-AG-005, TC-PARAM-019 | exact |
| `AITG-INF-04` | Testing for Capability Misuse | LLMI-T008, LLMI-T013, LLMI-T014 | TC-AG-005 | partial |
| `AITG-INF-05` | Testing for Fine-tuning Poisoning | LLMI-T006 | — | none |
| `AITG-INF-06` | Testing for Dev-Time Model Theft | LLMI-T005, LLMI-T010 | — | none |
| `AITG-MOD-01` | Testing for Evasion Attacks | LLMI-T003 | — | none |
| `AITG-MOD-02` | Testing for Runtime Model Poisoning | LLMI-T006, LLMI-T009 | TC-MEM-007 | partial |
| `AITG-MOD-03` | Testing for Poisoned Training Sets | LLMI-T006 | — | none |
| `AITG-MOD-04` | Testing for Membership Inference | LLMI-T004 | — | none |
| `AITG-MOD-05` | Testing for Inversion Attacks | LLMI-T004, LLMI-T005 | — | none |
| `AITG-MOD-06` | Testing for Robustness to New Data | — | — | none |
| `AITG-MOD-07` | Testing for Goal Alignment | LLMI-T015 | — | none |

Still without a test case: training-data exposure and membership inference (DAT-01, MOD-04, MOD-05), fine-tune poisoning (INF-05, MOD-03, DAT-04), dev-time model theft (INF-06).

## 9. Discovery queue

`data/research-queue.json` now holds the 47 repositories cited by three or more of the 20 curated lists that are not yet in the ecosystem. Top of the queue: ArmorerLabs/Armorer-Guard, meta-llama/PurpleLlama, OWASP agent-memory-guard (six lists each), EasyJailbreak, GPTFuzz, CipherChat, image-hijacks, LLMs-Finetuning-Safety. Each needs the same clone-and-classify pass before promotion. The 40 papers cited by three or more lists are in [`discovery.json`](../references/crosswalks/discovery.json); the most cited are 2302.12173 (indirect prompt injection, 8 lists) and 2504.03767 (MCP Safety Audit, 7).

## 10. OSINT angle

For analysts building collection around this landscape, the sweep surfaced AI-assisted OSINT tooling worth tracking (full list in `discovery.json`): Taranis AI (open-source OSINT and CTI pipeline with NLP enrichment), Robin (LLM-assisted dark-web search), osintgpt, MCP servers wrapping maigret and dnstwist, and leaked-key monitors (KeyLeak Detector, KeySentry). They are analyst tools, not threat data, and sit outside the ecosystem dataset on purpose.

AIID (AI Incident Database) does not ship its corpus in the repository; it is MongoDB-backed. Usable entry points found in the code: weekly snapshots at `https://incidentdatabase.ai/research/snapshots/`, RSS at `https://incidentdatabase.ai/rss.xml`, and a GraphQL API that now requires an account token. The MIT risk taxonomy's "Privacy & Security" and "4.2 Cyberattacks" classes are the filter to apply before anything reaches the research queue.

## 11. Attribution and licences

Rule IDs, module names and test IDs are cited, not copied. ATR (MIT) requests citation; tl;dr sec prompt-injection-defenses and invariantlabs mcp-injection-experiments have no licence file and are linked only. Full licence per repository: `ecosystem[].verification.license`.
