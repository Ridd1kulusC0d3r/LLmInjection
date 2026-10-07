# Project overview

The long-form tour of LLMInjection: pipeline, landscape, actors, lab, graph, frameworks, models, detection and architecture. This was the body of the repository README; the README now carries only the short version.

- [Living Intelligence](#living-intelligence)
- [AI / LLM Threat Landscape 2026](#ai--llm-threat-landscape-2026)
- [Threat Actors & Campaigns](#threat-actors--campaigns)
- [Security Test Lab](#security-test-lab)
- [Threat Landscape Model](#threat-landscape-model)
- [Intelligence Graph & Explorer](#intelligence-graph--explorer)
- [Framework Stack](#framework-stack)
- [Model & Runtime Intelligence](#model--runtime-intelligence)
- [Detection Engineering](#detection-engineering)
- [Intelligence Architecture](#intelligence-architecture)
- [Research & Evaluation Ecosystem](#research--evaluation-ecosystem)
- [Roadmap](#roadmap)

---

## Living Intelligence

LLMInjection now has a **review-gated living-intelligence pipeline** instead of depending on occasional manual bulk updates.

```text
MITRE ATLAS · OWASP · MCP · GitHub Advisories · CISA KEV
                         ↓
                 automated collection
                         ↓
                 research-queue.json
                         ↓
                    analyst review
                         ↓
              structured intelligence
                         ↓
                Graph / STIX / API
                         ↓
                monthly snapshot
                         ↓
                entity-level diff
                         ↓
             Explorer · What's New
```

The daily collectors **cannot auto-create attribution, incidents, CVE relationships or framework mappings**. It only creates review candidates. Monthly automation produces deterministic snapshots and added/removed/changed diffs.

**Living intelligence methodology:** [docs/LIVING-INTELLIGENCE.md](LIVING-INTELLIGENCE.md) · **Feed registry:** [data/source-feeds.json](../data/source-feeds.json) · **Research queue:** [data/research-queue.json](../data/research-queue.json)

---

## AI / LLM Threat Landscape 2026

The repository now maintains a dedicated **evidence-driven threat landscape**, separate from the actor tracker. The landscape tracks macro-trends, telemetry, sectors, research concepts, attack surfaces and defensive priorities while preserving each source's original population and time window.

#### 2026 snapshot

| Signal | Verified value | Source |
|---|---:|---|
| Leaders expecting AI to be the biggest force shaping cybersecurity in 2026 | **94%** | World Economic Forum |
| Respondents identifying AI-related vulnerabilities as fastest-growing cyber risk | **87%** | World Economic Forum |
| Average attacks per organization per week | **1,968** | Check Point |
| AI-agent-triggered detection leads vs human-triggered growth | **2.5×** | CrowdStrike |
| Cloud-conscious eCrime activity | **+171%** | CrowdStrike |
| Registry threats involving malicious npm packages | **87%** | CrowdStrike |
| Confirmed ransomware victims in Fortinet dataset | **7,831 / +389% YoY** | Fortinet |
| Ransomware-associated data theft | **896.2 TB** | Zscaler ThreatLabz |
| Blockchain transactions associated with ransomware payments | **US$328M** | Zscaler ThreatLabz |
| High-risk GenAI prompts | **2% → 4%** | Check Point Research |
| Longer malicious prompt-injection payload detections | **~5×** | Check Point Research |
| Major supply-chain / third-party incidents since 2020 | **nearly 4×** | IBM X-Force |

#### Landscape domains

```mermaid
flowchart LR
    TL["AI / LLM Threat Landscape 2026"]
    TL --> O["AI as Operator"]
    TL --> E["AI as Offensive Enabler"]
    TL --> P["Prompt Injection / Promptware"]
    TL --> A["Agentic / MCP / Tool Risk"]
    TL --> S["AI Supply Chain"]
    TL --> D["Data Exposure / Shadow AI"]
    TL --> I["Cloud / Identity"]
    TL --> R["Ransomware / Extortion"]
    TL --> M["Model Integrity"]
```

**Full landscape:** [THREAT-LANDSCAPE-2026.md](THREAT-LANDSCAPE-2026.md) · **Dataset:** [`data/threat-landscape-2026.json`](../data/threat-landscape-2026.json) · **AI security ecosystem:** [AI-SECURITY-ECOSYSTEM.md](../references/AI-SECURITY-ECOSYSTEM.md)

> The landscape distinguishes **observed incidents**, **vendor assessments**, **research frameworks**, **proofs of concept** and **unverified leads**. Interesting numbers do not become CTI just because someone put them in a chart.

---

## Threat Actors & Campaigns

Real-world reporting is intentionally placed on the front page because AI security becomes useful when research connects to **who is doing what, where the evidence comes from, and what defenders can observe**.

| Actor / cluster | Nexus | AI role | Documented activity | Confidence |
|---|---|---|---|:---:|
| **GTG-1002** | China | Autonomous operator | Claude Code used in a largely AI-orchestrated espionage campaign against ~30 targets; Anthropic reported AI performing 80–90% of tactical operations | 🟢 Confirmed |
| **APT28 / FROZENLAKE** | Russia | Runtime enabler | PROMPTSTEAL / LAMEHUG queried an LLM to generate commands during live operations | 🟢 Confirmed |
| **APT42** | Iran | Offensive enabler | Gemini used for reconnaissance, target research, phishing content and localization | 🟢 Confirmed |
| **UNC2970** | North Korea nexus | Offensive enabler | Gemini used to synthesize OSINT and profile high-value targets | 🟢 Confirmed |
| **Kimsuky** | North Korea | Local AI stack | Reporting identified Ollama, GPT4All, Msty and RAG-related artifacts in infrastructure linked to the group | 🟡 High |
| **Famous Chollima / PromptMink** | North Korea | Coding-agent / supply chain | Reporting describes malicious package activity designed to influence AI coding-agent dependency selection | 🟡 High |
| **TeamPCP** | Unattributed | AI infrastructure target | 2026 software supply-chain activity included malicious LiteLLM releases, exposing AI gateways and CI/CD trust | 🟢 Confirmed |

**Actors Using AI:** [docs/ACTORS-USING-AI.md](ACTORS-USING-AI.md) · **Analyst tracker:** [ACTOR-TRACKER.md](ACTOR-TRACKER.md) · **Machine-readable:** [`data/actors.json`](../data/actors.json) · **Source methodology:** [SOURCE-GRADING.md](SOURCE-GRADING.md)

> Attribution is deliberately conservative. Vendor tracking labels are not silently merged into universal aliases, and claims that lack sufficient primary evidence remain in the research queue rather than being promoted to fact.

---

## Security Test Lab

The test catalog converts threat intelligence into **safe, reproducible defensive validation**. Tests use synthetic canaries, mock tools, local fixtures and simulated telemetry instead of production secrets or third-party targets.

| ID | Test case | Surface | What the secure system must prove |
|---|---|---|---|
| [`TC-PI-001`](TEST-CASES.md#tc-pi-001--direct-prompt-injection-boundary) | Direct Prompt Injection Boundary | Prompt | User text cannot become higher-priority policy |
| [`TC-PI-002`](TEST-CASES.md#tc-pi-002--indirect-prompt-injection-in-rag) | Indirect Prompt Injection in RAG | RAG | Retrieved instructions remain untrusted content |
| [`TC-DL-003`](TEST-CASES.md#tc-dl-003--synthetic-secret-disclosure) | Synthetic Secret Disclosure | Context | Protected canaries are not disclosed |
| [`TC-RAG-004`](TEST-CASES.md#tc-rag-004--rag-provenance-conflict) | RAG Provenance Conflict | Knowledge | Trusted/untrusted source provenance survives retrieval |
| [`TC-AG-005`](TEST-CASES.md#tc-ag-005--unauthorized-tool-invocation) | Unauthorized Tool Invocation | Agent tools | Content cannot trigger privileged side effects |
| [`TC-AG-006`](TEST-CASES.md#tc-ag-006--high-impact-action-confirmation) | High-Impact Action Confirmation | Agent tools | High-impact action stops at a human/policy checkpoint |
| [`TC-MEM-007`](TEST-CASES.md#tc-mem-007--persistent-memory-poisoning) | Persistent Memory Poisoning | Memory | Memory cannot silently grant future authority |
| [`TC-SC-008`](TEST-CASES.md#tc-sc-008--coding-agent-dependency-manipulation) | Coding-Agent Dependency Manipulation | Supply chain | Attractive metadata cannot bypass dependency policy |
| [`TC-SC-009`](TEST-CASES.md#tc-sc-009--model-artifact-provenance-drift) | Model Artifact Provenance Drift | Model supply chain | Digest/provenance mismatch blocks deployment |
| [`TC-MCP-010`](TEST-CASES.md#tc-mcp-010--mock-mcp-capability-spoofing) | Mock MCP Capability Spoofing | MCP / tools | Tool descriptions cannot self-grant privilege |
| [`TC-RUN-011`](TEST-CASES.md#tc-run-011--unauthorized-local-llm-runtime) | Unauthorized Local LLM Runtime | Endpoint | Shadow AI is inventoried and investigated |
| [`TC-NET-012`](TEST-CASES.md#tc-net-012--unexpected-llm-provider-egress) | Unexpected LLM Provider Egress | Network | AI egress from an unapproved workload is surfaced |
| [`TC-OH-013`](TEST-CASES.md#tc-oh-013--improper-output-handling) | Improper Output Handling | Application | Model output remains untrusted data |
| [`TC-COST-014`](TEST-CASES.md#tc-cost-014--agent-budget-exhaustion) | Agent Budget Exhaustion | Availability | Token/call/cost budgets terminate loops |
| [`TC-AUTO-015`](TEST-CASES.md#tc-auto-015--autonomous-multi-step-chain-gate) | Autonomous Multi-Step Chain Gate | Orchestration | Autonomous chains stop at privilege boundaries |

**Test handbook:** [docs/TEST-CASES.md](TEST-CASES.md) · **Safe runner:** [docs/LAB.md](LAB.md) · **Dataset:** [`data/test-cases.json`](../data/test-cases.json) · **Evaluation ecosystem:** [BENCHMARKS.md](BENCHMARKS.md)

#### Lab pipeline

```mermaid
flowchart LR
    A["Threat / CTI hypothesis"] --> B["Safe test case"]
    B --> C["Synthetic stimulus"]
    C --> D["System under test"]
    D --> E{"Security boundary"}
    E -->|Held| F["PASS"]
    E -->|Crossed| G["FAIL / investigate"]
    F --> H["Telemetry + evidence"]
    G --> H
    H --> I["Framework + control mapping"]
```

The roadmap includes adapters for **Microsoft PyRIT, NVIDIA garak, JailbreakBench-style evaluation, local models, mock RAG stores and mock MCP/tool servers**.

---

## Threat Landscape Model

LLMInjection separates four roles that are often carelessly mixed together under the phrase “AI cyber threat”.

```mermaid
flowchart TB
    CTI["LLMInjection Intelligence Layer"]

    CTI --> TARGET["AI as Target"]
    CTI --> ENABLER["AI as Offensive Enabler"]
    CTI --> OPERATOR["AI as Autonomous Operator"]
    CTI --> DEFENSE["AI as Defensive Control Plane"]

    TARGET --> T1["Prompt / indirect injection"]
    TARGET --> T2["RAG & memory poisoning"]
    TARGET --> T3["Model / data theft & poisoning"]
    TARGET --> T4["Agent / MCP / tool abuse"]
    TARGET --> T5["AI supply-chain compromise"]

    ENABLER --> E1["Recon & OSINT synthesis"]
    ENABLER --> E2["Social engineering"]
    ENABLER --> E3["Code / malware assistance"]
    ENABLER --> E4["Data triage"]

    OPERATOR --> O1["Task chaining"]
    OPERATOR --> O2["Autonomous tool use"]
    OPERATOR --> O3["Machine-speed iteration"]

    DEFENSE --> D1["Evaluation"]
    DEFENSE --> D2["Detection engineering"]
    DEFENSE --> D3["Policy enforcement"]
    DEFENSE --> D4["Threat hunting"]
```

The important boundary is usually not the text generated by the model. It is the transition from **text to capability**: API call, tool execution, file write, credential use, message send, package install or other state change.

Read the full model: [AI-THREAT-MODEL.md](AI-THREAT-MODEL.md).

---

## Intelligence Graph & Explorer

The CTI core is now relational rather than list-based:

```text
Source → Actor → Campaign → Technique → Model
                         ↓
                      Test Case
                         ↓
                      Detection
                         ↓
                       Control
                         ↓
                      Framework
```

Run locally:

```bash
python scripts/validate_intel.py
python scripts/build_graph.py
python scripts/run_safe_lab.py --profile all
```

Generated outputs are written to `dist/graph.json`, `dist/graph.graphml` and `dist/llminjection-stix.json`. Vulnerability nodes retain CVE/GHSA/OSV identifiers as STIX external references.

#### Read-only intelligence interfaces

```bash
python scripts/query_intel.py search "prompt injection"
python scripts/query_intel.py get ACTOR-APT28
python scripts/query_intel.py coverage LLMI-T015
```

An optional **MCP v2 read-only server** exposes search, object lookup, graph traversal, recent activity, defensive coverage and latest-diff queries without modifying the dataset.

**MCP:** [integrations/mcp/README.md](../integrations/mcp/README.md)

**Explorer:** https://ridd1kulusc0d3r.github.io/LLmInjection/ · **Static API:** `https://ridd1kulusc0d3r.github.io/LLmInjection/api/v1/index.json` · **Graph model:** [INTELLIGENCE-GRAPH.md](INTELLIGENCE-GRAPH.md) · **Methodology:** [METHODOLOGY.md](METHODOLOGY.md) · **Vulnerabilities:** [`data/vulnerabilities.json`](../data/vulnerabilities.json) · **Reference library:** [REFERENCE-LIBRARY.md](../references/REFERENCE-LIBRARY.md)

---

## Framework Stack

MITRE ATLAS is essential, but it does not cover the whole AI system. LLMInjection uses a multi-framework crosswalk rather than pretending every taxonomy is interchangeable.

| Layer | Frameworks / taxonomies | Purpose |
|---|---|---|
| Adversary behavior | **MITRE ATLAS · MITRE ATT&CK** | AI-specific and surrounding intrusion TTPs |
| LLM application risk | **OWASP Top 10 for LLM Applications 2026** | Current prompt, disclosure, agency, supply-chain, poisoning, consumption, context and output risks |
| Agentic security | **OWASP Top 10 for Agentic Applications 2026 · CSA MAESTRO** | Autonomy, tools, memory, identity and multi-agent trust |
| Adversarial ML | **NIST AI 100-2e2025** | AML terminology, attacker goals/capabilities and mitigations |
| AI risk governance | **NIST AI RMF · NIST AI 600-1** | Govern, Map, Measure and Manage GenAI risk |
| Secure AI architecture | **Google SAIF** | Data, infrastructure, model and application controls |
| Threat intelligence | **ENISA CTL Methodology 2025** | Evidence-driven threat-landscape methodology |
| Classic modeling | **STRIDE · PASTA · LINDDUN** | Technical, risk-centric and privacy threat modeling |

**Full crosswalk:** [docs/FRAMEWORKS.md](FRAMEWORKS.md) · **Dataset:** [`data/frameworks.json`](../data/frameworks.json)

---

## Model & Runtime Intelligence

A model name is not a security posture. Deployment architecture, tool authority, RAG, memory, identity, network access and provenance often matter more than the base model alone.

**Tracked families:**  
`GPT` · `gpt-oss` · `Claude` · `Gemini` · `Gemma` · `Llama` · `Qwen` · `DeepSeek` · `Mistral` · `Grok` · `Kimi` · `GLM`

| Deployment class | Main security questions |
|---|---|
| Managed API | Identity, API keys, gateway policy, data handling, tool authorization |
| Open-weight / self-hosted | Model provenance, serving stack, dependencies, runtime isolation |
| RAG application | Ingestion trust, indirect injection, corpus poisoning, citation provenance |
| Coding agent | Repository trust, dependency policy, secret isolation, shell/tool permissions |
| Tool-using agent | Capability boundaries, contextual authorization, side effects |
| Multi-agent system | Agent identity, delegation, message integrity, trust propagation |
| AI gateway | Credential concentration, routing integrity, CI/CD and admin control |

**Catalog:** [MODEL-CATALOG.md](MODEL-CATALOG.md) · **Security matrix:** [MODEL-SECURITY-MATRIX.md](MODEL-SECURITY-MATRIX.md) · **Data:** [`data/models.json`](../data/models.json)

---

## Detection Engineering

LLMInjection focuses on behaviors and trust-boundary crossings rather than trying to detect the string “AI”.

#### High-value detection hypotheses

- **Unexpected AI egress** from workloads with no approved AI dependency.
- **Local model runtimes** appearing on non-AI endpoints.
- **Agent capability transitions** from text/read-only context to privileged action.
- **RAG or memory integrity changes** originating from untrusted sources.
- **Model/package provenance drift** before deployment.
- **AI gateway credential access** inconsistent with normal administration.
- **Autonomous chains** crossing action-risk tiers without required approval.

```text
untrusted content
      ↓
model / agent interpretation
      ↓
capability request
      ↓
policy + identity decision
      ↓
tool / API / state change
      ↓
telemetry + detection
```

**Detection guide:** [docs/DETECTION-ENGINEERING.md](DETECTION-ENGINEERING.md) · **Coverage:** [docs/DETECTION-COVERAGE.md](DETECTION-COVERAGE.md) · **Starter rules:** [detections/](../detections/)

---

## Intelligence Architecture

```mermaid
flowchart LR
    S["Sources"] --> I["Evidence & confidence"]
    I --> A["Actors / campaigns"]
    I --> T["Techniques"]
    I --> M["Models / runtimes"]
    I --> F["Framework mappings"]

    A --> R["Relationships"]
    T --> R
    M --> R
    F --> R

    R --> TC["Safe test cases"]
    R --> DE["Detection engineering"]
    R --> TH["Threat hunting"]
    R --> CT["Controls / mitigations"]

    TC --> OUT["JSON · Graph · STIX · Pages"]
    DE --> OUT
    TH --> OUT
    CT --> OUT
```

#### Evidence model

Every intelligence item should answer:

1. **What happened?**
2. **Who says so?**
3. **What is directly observed vs assessed?**
4. **How confident are we?**
5. **When was it last verified?**
6. **Which frameworks does it map to?**
7. **What telemetry, test or control is relevant?**

| Confidence | Meaning |
|---|---|
| 🟢 `confirmed` | Primary or authoritative reporting directly supports the claim |
| 🟡 `high` | Strong named-vendor assessment or multiple credible sources |
| 🟠 `medium` | Plausible and partially supported, with material gaps |
| 🔴 `low` | Limited support or meaningful conflicting evidence |
| ⚪ `unverified` | Research lead retained without promotion to fact |

---

## Research & Evaluation Ecosystem

LLMInjection indexes external projects for discovery and reproducible evaluation while keeping its CTI dataset evidence-driven.

| Area | Projects |
|---|---|
| GenAI red teaming | Microsoft **PyRIT**, NVIDIA **garak** |
| Jailbreak robustness | **JailbreakBench**, GCG / LLM Attacks |
| Adversarial ML | **Adversarial Robustness Toolbox**, TextAttack |
| Community corpora | jailbreak and prompt-security collections indexed as research sources |
| Standards | MITRE, OWASP, NIST, CSA, Google SAIF, ENISA |

Community corpora are discovery sources, **not self-authenticating intelligence**. Claims are promoted only after evidence review.

See [REFERENCE-LIBRARY.md](../references/REFERENCE-LIBRARY.md), [BENCHMARKS.md](BENCHMARKS.md), [AI-SUPPLY-CHAIN.md](AI-SUPPLY-CHAIN.md) and [community-corpora.md](../references/community-corpora.md).

---

## Roadmap

```text
v0.1  Intelligence foundation                    ✅
v0.2  Relationships + STIX 2.1                    ✅ foundation
v0.3  Threat graph + interactive GitHub Pages     ✅ foundation
v0.4  Sigma / KQL / SPL / ES|QL / YARA-L         🟡 starter pack
v0.5  Reproducible AI security evaluation lab     🟡 safe foundation
v0.6  AI supply-chain intelligence + AI/ML-BOM    🟡 foundation
v1.0  Community CTI platform                      🟡 beta
v1.1  Living Intelligence Pipeline                ✅ foundation
```

The north star is simple:

> Start with an **actor, model, prompt-injection class, OWASP risk, MITRE technique or supply-chain incident** and navigate directly to **evidence → related behavior → test case → telemetry → detection → control**.

Full roadmap: [docs/ROADMAP.md](ROADMAP.md) · [Intelligence changelog](INTELLIGENCE-CHANGELOG.md) · [Publishing & releases](PUBLISHING.md)
