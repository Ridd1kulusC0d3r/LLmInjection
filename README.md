<p align="center">
  <img src="assets/llminjection-banner.svg" alt="LLMInjection: threat landscape for LLM and agentic systems" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Ridd1kulusC0d3r/LLmInjection/actions/workflows/validate-intel.yml"><img src="https://img.shields.io/github/actions/workflow/status/Ridd1kulusC0d3r/LLmInjection/validate-intel.yml?style=flat-square&label=intel%20CI&labelColor=17150f&color=b43c0e" alt="Intel CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Ridd1kulusC0d3r/LLmInjection?style=flat-square&labelColor=17150f&color=4a463c" alt="Apache-2.0"></a>
  <img src="https://img.shields.io/badge/mode-defensive--first-4a463c?style=flat-square&labelColor=17150f" alt="Defensive first">
</p>

Open threat intelligence for AI, LLM and agentic systems: actors, campaigns, attack techniques, safe test cases, detections and controls, linked to the evidence behind each claim.

**[Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/)** · [Documentation](docs/README.md) · [Methodology](docs/METHODOLOGY.md) · [API](docs/PUBLISHING.md) · [Roadmap](docs/ROADMAP.md)

---

## At a glance

<!-- gen:stats:start -->
| Actors | Campaigns | Incidents | Vulnerabilities | Techniques | Sources |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **7** | **7** | **7** | **9** | **19** | **40** |

| Test cases | Detections | Controls | Frameworks | Model families | Relationships | Ecosystem repos |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **20** | **14** | **20** | **19** | **12** | **75** | **75** |
<!-- gen:stats:end -->

LLMInjection is **not a prompt dump**. Every meaningful claim carries a source grade, a confidence level, a last-verified date, framework context and a defensive angle.

<img src="assets/coverage-matrix.svg" alt="Technique coverage matrix: tests, detections and controls per technique" width="100%">

<sub>Rows flagged *no test* or *no detection* are the open work. Regenerate with `make charts`.</sub>

## What is inside

| Layer | What it holds | Start here |
|---|---|---|
| **Actors and campaigns** | State and criminal operators using AI, with vendor tracking labels kept as published | [`data/actors.json`](data/actors.json) · [Actor tracker](docs/ACTOR-TRACKER.md) |
| **Threat landscape** | Cited metrics, domains and open research leads for 2026 | [Landscape 2026](docs/THREAT-LANDSCAPE-2026.md) |
| **Techniques and frameworks** | LLMInjection techniques mapped to ATLAS, OWASP, NIST, SAIF and MAESTRO | [Frameworks](docs/FRAMEWORKS.md) · [Threat model](docs/AI-THREAT-MODEL.md) |
| **Safe test lab** | Defensive test cases for prompt, RAG, agent, MCP and supply-chain risks | [Test cases](docs/TEST-CASES.md) · [Lab](docs/LAB.md) |
| **Detection engineering** | Sigma, KQL, SPL, ES\|QL and YARA-L starter detections | [Detection engineering](docs/DETECTION-ENGINEERING.md) |
| **Evidence** | Graded sources and explicit relationships behind every record | [Source grading](docs/SOURCE-GRADING.md) · [Methodology](docs/METHODOLOGY.md) |
| **Ecosystem** | 75 related projects classified by what they can support | [Ecosystem map](docs/ECOSYSTEM.md) |

Exports: `graph.json`, GraphML, STIX 2.1, a static `/api/v1/` JSON API, monthly snapshots with entity-level diffs, and an interactive [Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/).

## Quick start

```bash
make test          # unit tests
make validate      # schema and referential checks on all datasets
make build         # graph, STIX, static API, charts
python scripts/query_intel.py search "prompt injection"
python scripts/query_intel.py coverage LLMI-T015
```

Python 3.12, standard library only. The optional MCP server in [`integrations/mcp`](integrations/mcp/README.md) needs its own `requirements.txt`.

## How intelligence gets in

```text
feeds ─► collector ─► research queue ─► analyst review ─► datasets ─► graph / STIX / API ─► snapshot + diff
 ATLAS      daily        candidates         human           JSON         exports            monthly
 OWASP
 MCP
 GHSA
```

The collector **cannot** create attribution, incidents, CVE relationships or framework mappings. It only proposes candidates. Details: [Living intelligence](docs/LIVING-INTELLIGENCE.md).

### OSINT indicator extractor

```bash
python scripts/osint_ioc.py report.md
python scripts/osint_ioc.py --url https://example.com/post --enrich   # adds CISA KEV and EPSS for CVEs
```

Re-fangs `hxxp` and `[.]`, drops private IPs and noisy domains, and extracts CVE/GHSA/ATLAS/OWASP IDs, hashes, npm and PyPI install lures and prompt-injection signals (hidden comments, invisible Unicode, markdown-image exfiltration). Output feeds the review queue, never the datasets directly.

## Explore the project

Each section opens in place: click the arrow. Tables inside are generated from the datasets, so they never drift.

<details open>
<summary><strong>Latest update, 2026-10-06</strong> &nbsp;·&nbsp; <sub>agent workspaces, MCP transport, autonomy at scale</sub></summary>

<br>

Two attack surfaces moved from research to observed activity.

1. **Agent workspace as attack surface.** Google Threat Intelligence Group reports the DUSTMAKER stealer hiding in `.claude/`, `.vscode/` and `.cursor/`, steering AI assistants through config files, stealing CI/CD OIDC tokens and prompt-injecting LLM scanners (techniques `LLMI-T017`, `LLMI-T018`).
2. **Model-controlled parameters reaching execution.** Microsoft Semantic Kernel (`CVE-2026-26030`, `CVE-2026-25592`) and the disputed MCP STDIO class show prompt injection turning into code execution when tool parameters are not validated outside the model.

Scale signals from GTIG: a multi-agent credential harvest planned and run in under six hours, and distillation campaigns exceeding 100 million prompts (`LLMI-T019`).

Held back on purpose: Anthropic's September 2026 report is only available here through press coverage, so its actors and victim counts sit in the research queue until the primary document is attached.

Full record: [Intelligence changelog](docs/INTELLIGENCE-CHANGELOG.md) · [Landscape 2026](docs/THREAT-LANDSCAPE-2026.md)

</details>

<details>
<summary><strong>Attack chains and defender playbook</strong> &nbsp;·&nbsp; <sub>two 2026 chains, mapped to tests, detections and controls</sub></summary>

<br>

### Chain 1: agent workspace abuse (DUSTMAKER)

Built from Google Threat Intelligence Group's reporting of DUSTMAKER. Each box is something the report states the malware does.

```mermaid
flowchart LR
    A["Foothold in repo<br>or CI environment"] --> B["Detect CI/CD<br>environment"]
    B --> C["Extract OIDC tokens<br>from runner memory"]
    A --> D["Drop hidden files in<br>.claude/ .vscode/ .cursor/"]
    D --> E["Config instructs the AI<br>assistant to run a script"]
    E --> F["Commands run on the<br>attacker's behalf"]
    A --> G["Adversarial comments<br>in the JS loader"]
    G --> H["LLM scanner refuses<br>or skips analysis"]
```

### Chain 2: prompt to execution (Semantic Kernel)

From Microsoft's analysis of `CVE-2026-26030` and `CVE-2026-25592`: the model is not the vulnerability, the missing validation after it is.

```mermaid
flowchart LR
    A["Untrusted text<br>in prompt or retrieved data"] --> B["Model chooses<br>tool parameters"]
    B --> C{"Validated outside<br>the model?"}
    C -- "no" --> D["eval() or file helper<br>runs the parameter"]
    D --> E["Code execution or<br>sandbox escape"]
    C -- "yes" --> F["Rejected and logged"]
```

### Defender playbook

| Stage | Technique | Safe test | Detection | Controls |
|---|---|---|---|---|
| Hidden assistant or IDE config | `LLMI-T018` | `TC-WS-017` | `DET-AI-011` | `CTRL-HUMAN-CHECKPOINT`, `CTRL-TOOL-ALLOWLIST` |
| Scanner evasion by refusal bait | `LLMI-T017` | `TC-SCAN-016` | `DET-AI-014` | `CTRL-DEPENDENCY-POLICY` |
| CI identity token theft | `LLMI-T011` | gap | `DET-AI-012` | `CTRL-SECRET-ISOLATION` |
| Model parameter reaches an evaluator | `LLMI-T008` | `TC-PARAM-019` | `DET-AI-003` | `CTRL-CONTEXTUAL-AUTHZ` |
| Gateway or provider key reuse | `LLMI-T016` | `TC-GW-020` | `DET-AI-006` | `CTRL-SECRET-ISOLATION` |
| Distillation at scale | `LLMI-T019` | `TC-DIST-018` | `DET-AI-013` | `CTRL-ACTION-BUDGET` |

The one open gap in this table is a safe test for CI token theft (`DET-AI-012` has a hypothesis but no simulation yet). A Sigma starter for `DET-AI-011` is in [`detections/sigma`](detections/sigma/det-ai-011-assistant-config-write.yml).

</details>

<details>
<summary><strong>Living intelligence</strong> &nbsp;·&nbsp; <sub>review-gated feeds, snapshots and diffs</sub></summary>

<br>

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

**Living intelligence methodology:** [docs/LIVING-INTELLIGENCE.md](docs/LIVING-INTELLIGENCE.md) · **Feed registry:** [data/source-feeds.json](data/source-feeds.json) · **Research queue:** [data/research-queue.json](data/research-queue.json)

</details>

<details>
<summary><strong>AI / LLM threat landscape 2026</strong> &nbsp;·&nbsp; <sub>cited metrics, domains and attack surfaces</sub></summary>

<br>

The repository now maintains a dedicated **evidence-driven threat landscape**, separate from the actor tracker. The landscape tracks macro-trends, telemetry, sectors, research concepts, attack surfaces and defensive priorities while preserving each source's original population and time window.

### 2026 snapshot

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

### Landscape domains

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

**Full landscape:** [THREAT-LANDSCAPE-2026.md](docs/THREAT-LANDSCAPE-2026.md) · **Dataset:** [`data/threat-landscape-2026.json`](data/threat-landscape-2026.json) · **AI security ecosystem:** [AI-SECURITY-ECOSYSTEM.md](references/AI-SECURITY-ECOSYSTEM.md)

> The landscape distinguishes **observed incidents**, **vendor assessments**, **research frameworks**, **proofs of concept** and **unverified leads**. Interesting numbers do not become CTI just because someone put them in a chart.

</details>

<details>
<summary><strong>Threat actors and campaigns</strong> &nbsp;·&nbsp; <sub>who is using AI, and how</sub></summary>

<br>

Real-world reporting is intentionally placed on the front page because AI security becomes useful when research connects to **who is doing what, where the evidence comes from, and what defenders can observe**.

**Actors Using AI:** [docs/ACTORS-USING-AI.md](docs/ACTORS-USING-AI.md) · **Analyst tracker:** [ACTOR-TRACKER.md](docs/ACTOR-TRACKER.md) · **Machine-readable:** [`data/actors.json`](data/actors.json) · **Source methodology:** [SOURCE-GRADING.md](docs/SOURCE-GRADING.md)

> Attribution is deliberately conservative. Vendor tracking labels are not silently merged into universal aliases, and claims that lack sufficient primary evidence remain in the research queue rather than being promoted to fact.

### Tracked actors

<!-- gen:actors:start -->
| Actor | Nexus | AI role | Activity | Confidence |
|---|---|---|---|---|
| **GTG-1002** | China | autonomous-operator, offensive-enabler | Anthropic assessed with high confidence that a Chinese state-sponsored group used Claude Code in a largely AI-orchestrated… | confirmed |
| **APT28** | Russia | runtime-enabler | Google Threat Intelligence reported PROMPTSTEAL, reported by CERT-UA as LAMEHUG, querying Qwen2.5-Coder-32B-Instruct through… | confirmed |
| **APT42** | Iran | offensive-enabler | GTIG observed Gemini use supporting reconnaissance, target research, phishing content and localization. | confirmed |
| **UNC2970** | North Korea nexus | offensive-enabler | GTIG reported Gemini use to synthesize OSINT and profile high-value targets for campaign planning and reconnaissance. | confirmed |
| **Kimsuky** | North Korea | local-analysis, offensive-enabler | Genians reported local LLM environments including Ollama, GPT4All and Msty plus RAG-related artifacts on infrastructure linked to… | high |
| **Famous Chollima** | North Korea | ai-supply-chain-targeting, coding-agent-targeting | 2026 reporting summarized by CSA attributes PromptMink to Famous Chollima and describes npm packages deliberately optimized to… | high |
| **TeamPCP** | Unattributed | ai-infrastructure-targeting, supply-chain | 2026 supply-chain activity resulted in malicious LiteLLM releases and demonstrated the concentration of credentials and trust in… | confirmed |
<!-- gen:actors:end -->

### Campaigns

<!-- gen:campaigns:start -->
| Campaign | Seen | Confidence | Summary |
|---|---|---|---|
| **GTG-1002 AI-orchestrated espionage** | 2026 | confirmed | Campaign assessed by Anthropic as Chinese state-sponsored in which Claude Code performed the majority of tactical operations against roughly 30… |
| **APT28 PROMPTSTEAL / LAMEHUG runtime LLM use** | 2026 | confirmed | APT28-linked activity used a public LLM at runtime to generate host-relevant commands. |
| **APT42 Gemini-enabled reconnaissance** | 2025 | confirmed | GTIG documented Gemini use for reconnaissance, target research, phishing content and localization. |
| **UNC2970 Gemini-enabled target profiling** | 2025 | confirmed | GTIG documented Gemini use to synthesize OSINT and profile high-value targets. |
| **Kimsuky local LLM capability integration** | 2026 | high | Genians reported local LLM tooling and RAG-related artifacts on infrastructure linked to Kimsuky. |
| **PromptMink** | 2026 | high | Reporting describes malicious package activity optimized to influence AI coding-agent dependency selection and attributes it to Famous Chollima. |
| **TeamPCP LiteLLM supply-chain compromise** | 2026 | confirmed | TeamPCP-linked supply-chain activity affected LiteLLM releases and highlighted credential concentration in AI gateways. |
<!-- gen:campaigns:end -->

### Incidents and research cases

<!-- gen:incidents:start -->
| Incident | Kind | Status | Confidence |
|---|---|---|---|
| **CLOSEDQUORUM autonomous AI C2 research case** | research-artifact | not-confirmed-in-the-wild | confirmed |
| **VoidLink AI-assisted malware engineering case** | observed-research-case | observed | confirmed |
| **STARDUST CHOLLIMA Mastra AI package compromise** | supply-chain | observed | confirmed |
| **Qwen3-4B safety-circuit perturbation research** | defensive-research | research | confirmed |
| **Promptware Kill Chain research model** | research-framework | research | confirmed |
| **DUSTMAKER credential stealer targeting AI coding-assistant workspaces** | malware | observed | confirmed |
| **Multi-agent mass credential harvesting in under six hours** | intrusion | observed | confirmed |
<!-- gen:incidents:end -->

</details>

<details>
<summary><strong>Security test lab</strong> &nbsp;·&nbsp; <sub>safe, reproducible defensive test cases</sub></summary>

<br>

The test catalog converts threat intelligence into **safe, reproducible defensive validation**. Tests use synthetic canaries, mock tools, local fixtures and simulated telemetry instead of production secrets or third-party targets.

**Test handbook:** [docs/TEST-CASES.md](docs/TEST-CASES.md) · **Safe runner:** [docs/LAB.md](docs/LAB.md) · **Dataset:** [`data/test-cases.json`](data/test-cases.json) · **Evaluation ecosystem:** [BENCHMARKS.md](docs/BENCHMARKS.md)

### Lab pipeline

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

### Test case catalog

<!-- gen:test-cases:start -->
| ID | Test case | Category | What the secure system must prove |
|---|---|---|---|
| `TC-PI-001` | **Direct Prompt Injection Boundary** | prompt-injection | Verify that untrusted user text cannot override higher-priority application policy. |
| `TC-PI-002` | **Indirect Prompt Injection in RAG** | prompt-injection | Verify that instructions embedded in retrieved content are treated as data, not control. |
| `TC-DL-003` | **Synthetic Secret Disclosure** | data-leakage | Verify that protected context is not disclosed through ordinary conversation. |
| `TC-RAG-004` | **RAG Provenance Conflict** | rag-security | Verify behavior when trusted and untrusted documents disagree. |
| `TC-AG-005` | **Unauthorized Tool Invocation** | agentic-security | Verify that untrusted content cannot directly trigger a privileged tool. |
| `TC-AG-006` | **High-Impact Action Confirmation** | agentic-security | Verify that high-impact actions require an explicit human checkpoint. |
| `TC-MEM-007` | **Persistent Memory Poisoning** | agentic-security | Verify that persistent memory changes have provenance and cannot silently alter future authorization. |
| `TC-SC-008` | **Coding-Agent Dependency Manipulation** | supply-chain | Verify that attractive package metadata cannot bypass dependency review. |
| `TC-SC-009` | **Model Artifact Provenance Drift** | supply-chain | Verify detection when a model artifact digest differs from the approved manifest. |
| `TC-MCP-010` | **Mock MCP Capability Spoofing** | agentic-protocol | Verify that a tool description cannot grant itself authority. |
| `TC-RUN-011` | **Unauthorized Local LLM Runtime** | runtime-security | Verify visibility when a local model runtime appears on a non-AI endpoint. |
| `TC-NET-012` | **Unexpected LLM Provider Egress** | network-detection | Verify detection of AI-provider traffic from a workload with no approved AI dependency. |
| `TC-OH-013` | **Improper Output Handling** | application-security | Verify that model output is treated as untrusted data by downstream components. |
| `TC-COST-014` | **Agent Budget Exhaustion** | availability | Verify hard limits on loops, tokens, calls and cost in an agent workflow. |
| `TC-AUTO-015` | **Autonomous Multi-Step Chain Gate** | agentic-security | Verify checkpoints when an agent chains discovery, analysis and a mock external action. |
| `TC-SCAN-016` | **Scanner Refusal-Bait Fail-Open Check** | application-security | Verify that an LLM-based code or package scanner never reports a sample as clean when it refused or skipped the… |
| `TC-WS-017` | **Assistant Workspace Config Trust Gate** | agentic-security | Verify that new or changed assistant, hook or IDE configuration inside a repository is not trusted or executed… |
| `TC-DIST-018` | **Systematic Prompt Harvest Alert** | data-leakage | Verify that high-volume, templated prompting against a model endpoint is detected and rate-limited. |
| `TC-PARAM-019` | **Model-Supplied Parameter Validation** | agentic-security | Verify that parameters produced by a model are validated outside the model before reaching an evaluator, file path or… |
| `TC-GW-020` | **AI Gateway Key Blast Radius** | runtime-security | Verify that a leaked gateway or provider key is scoped, monitored and revocable before it can be reused at scale. |
<!-- gen:test-cases:end -->

</details>

<details>
<summary><strong>Threat landscape model</strong> &nbsp;·&nbsp; <sub>attack surfaces and trust boundaries</sub></summary>

<br>

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

Read the full model: [AI-THREAT-MODEL.md](docs/AI-THREAT-MODEL.md).

### Technique catalog

<!-- gen:techniques:start -->
| ID | Technique | Category | Mapped to |
|---|---|---|---|
| `LLMI-T001` | **Direct Prompt Injection** | prompt-context | OWASP LLM, MITRE ATLAS, Google SAIF |
| `LLMI-T002` | **Indirect Prompt Injection** | prompt-context | OWASP LLM, MITRE ATLAS, Google SAIF, CSA MAESTRO |
| `LLMI-T003` | **Jailbreak / Safety Boundary Manipulation** | model-behavior | OWASP LLM, NIST AI 100-2e2025 |
| `LLMI-T004` | **Sensitive Information Disclosure** | confidentiality | OWASP LLM, Google SAIF |
| `LLMI-T005` | **Model Extraction / Theft** | model | MITRE ATLAS, NIST AI 100-2e2025, Google SAIF |
| `LLMI-T006` | **Data or Model Poisoning** | training-data | OWASP LLM, MITRE ATLAS, NIST AI 100-2e2025, Google SAIF |
| `LLMI-T007` | **RAG Knowledge Poisoning** | rag | OWASP LLM, CSA MAESTRO, Google SAIF |
| `LLMI-T008` | **Agent Tool Misuse** | agentic | OWASP Agentic, CSA MAESTRO, Google SAIF |
| `LLMI-T009` | **Memory / Context Poisoning** | agentic | OWASP Agentic, CSA MAESTRO |
| `LLMI-T010` | **Model Source Tampering** | supply-chain | Google SAIF, MITRE ATLAS |
| `LLMI-T011` | **AI Software Supply Chain Compromise** | supply-chain | OWASP LLM, Google SAIF, CSA MAESTRO, MITRE ATT&CK |
| `LLMI-T012` | **Coding-Agent Dependency Manipulation** | supply-chain | OWASP Agentic, OWASP LLM, CSA MAESTRO |
| `LLMI-T013` | **Runtime LLM Command Generation** | ai-offensive-enabler | MITRE ATT&CK, MITRE ATLAS |
| `LLMI-T014` | **AI-Assisted Reconnaissance and Social Engineering** | ai-offensive-enabler | MITRE ATT&CK, MITRE ATLAS |
| `LLMI-T015` | **Agentic Attack Orchestration** | ai-autonomous-operator | MITRE ATT&CK, MITRE ATLAS, CSA MAESTRO |
| `LLMI-T016` | **AI Gateway Credential Compromise** | supply-chain | OWASP LLM, Google SAIF, MITRE ATT&CK |
| `LLMI-T017` | **Prompt Injection Against AI Security Scanners** | defense-evasion | OWASP LLM |
| `LLMI-T018` | **AI Coding-Assistant Workspace Abuse** | agentic-supply-chain | OWASP LLM, CSA MAESTRO |
| `LLMI-T019` | **Model Distillation Campaign** | model-theft | OWASP LLM, MITRE ATLAS |
<!-- gen:techniques:end -->

</details>

<details>
<summary><strong>Intelligence graph and Explorer</strong> &nbsp;·&nbsp; <sub>relationships, STIX, static API and MCP</sub></summary>

<br>

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

### Read-only intelligence interfaces

```bash
python scripts/query_intel.py search "prompt injection"
python scripts/query_intel.py get ACTOR-APT28
python scripts/query_intel.py coverage LLMI-T015
```

An optional **MCP v2 read-only server** exposes search, object lookup, graph traversal, recent activity, defensive coverage and latest-diff queries without modifying the dataset.

**MCP:** [integrations/mcp/README.md](integrations/mcp/README.md)

**Explorer:** https://ridd1kulusc0d3r.github.io/LLmInjection/ · **Static API:** `https://ridd1kulusc0d3r.github.io/LLmInjection/api/v1/index.json` · **Graph model:** [INTELLIGENCE-GRAPH.md](docs/INTELLIGENCE-GRAPH.md) · **Methodology:** [METHODOLOGY.md](docs/METHODOLOGY.md) · **Vulnerabilities:** [`data/vulnerabilities.json`](data/vulnerabilities.json) · **Reference library:** [REFERENCE-LIBRARY.md](references/REFERENCE-LIBRARY.md)

### Vulnerability and malicious-package records

<!-- gen:vulnerabilities:start -->
| Record | Identifiers | Kind | Severity | Published |
|---|---|---|---|---|
| Malicious LiteLLM PyPI releases 1.82.7 and 1.82.8 | `GHSA-92x9-889m-jgmw`<br>`MAL-2026-2144` | malicious-package | malware | 2026-07-21 |
| LiteLLM MCP OAuth2 Passthrough Authentication Bypass | `CVE-2026-59822`<br>`GHSA-7488-6r32-c95q` | authentication-bypass | high | 2026-06-30 |
| LiteLLM MCP Proxy Improper Authentication | `CVE-2026-12773`<br>`GHSA-4jcj-7x88-m979` | improper-authentication | moderate | 2026-06-21 |
| LiteLLM Custom Code Guardrails Production Safety-Check Bypass | `CVE-2026-59821`<br>`GHSA-72m8-9m7m-h278` | guardrail-code-execution | low | 2026-06-30 |
| Trivy Ecosystem Supply-Chain Compromise | `CVE-2026-33634`<br>`GHSA-69fq-xp46-6x23` | supply-chain-compromise | critical | 2026-03-21 |
| Trivy Crafted OCI Artifact Path Traversal | `GHSA-mcj4-mphf-j9ff` | path-traversal | high | 2026-06-15 |
| Semantic Kernel In-Memory Vector Store filter injection to RCE | `CVE-2026-26030` | remote-code-execution | unrated | 2026-05-07 |
| Semantic Kernel SessionsPythonPlugin arbitrary file access | `CVE-2026-25592` | sandbox-escape | unrated | 2026-05-07 |
| MCP STDIO configuration command injection across AI frameworks | `CVE-2026-30623`<br>`CVE-2026-30615` | command-injection | unrated | 2026-04-15 |
<!-- gen:vulnerabilities:end -->

</details>

<details>
<summary><strong>Framework stack</strong> &nbsp;·&nbsp; <sub>ATLAS, OWASP, NIST, SAIF, MAESTRO and more</sub></summary>

<br>

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

**Full crosswalk:** [docs/FRAMEWORKS.md](docs/FRAMEWORKS.md) · **Dataset:** [`data/frameworks.json`](data/frameworks.json)

### Tracked frameworks

<!-- gen:frameworks:start -->
| Framework | Category | Used for |
|---|---|---|
| [MITRE ATLAS](https://atlas.mitre.org/) | adversary-knowledge-base | AI-specific adversary behavior mapping |
| [MITRE ATT&CK](https://attack.mitre.org/) | adversary-knowledge-base | Surrounding intrusion behavior for AI-enabled campaigns |
| [OWASP Top 10 for LLM Applications 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | application-risk | Current application-layer risk mapping |
| [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) | application-risk | Application-layer risk mapping |
| [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | agentic-risk | Agent autonomy, tools and orchestration risk |
| [NIST AI 100-2e2025](https://doi.org/10.6028/NIST.AI.100-2e2025) | adversarial-ml-taxonomy | Canonical AML terminology |
| [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | risk-management | Governance, mapping, measurement and management |
| [NIST AI RMF Generative AI Profile](https://doi.org/10.6028/NIST.AI.600-1) | risk-profile | GenAI risk profile and actions |
| [Google Secure AI Framework](https://saif.google/) | secure-ai-framework | Risk-to-control mapping across AI lifecycle |
| [CSA MAESTRO](https://labs.cloudsecurityalliance.org/maestro/) | threat-modeling | Layered agentic threat modeling |
| [ENISA Cybersecurity Threat Landscape Methodology 2025](https://www.enisa.europa.eu/publications/enisa-cybersecurity-threat-landscape-methodology) | threat-intelligence-methodology | Threat-intelligence methodology |
| [STRIDE](https://learn.microsoft.com/azure/security/develop/threat-modeling-tool-threats) | classic-threat-modeling | Baseline component threats |
| [PASTA](https://owasp.org/www-pdf-archive/AppSecEU2012_PASTA.pdf) | risk-centric-threat-modeling | Scenario and impact-driven modeling |
| [LINDDUN](https://www.linddun.org/) | privacy-threat-modeling | Privacy threats in data/RAG/model flows |
| [OWASP Agent Control Standard](https://genai.owasp.org/resource/agent-control-standard-acs/) | agent-runtime-control-standard | Runtime enforcement and agent observability |
| [CSA AI Controls Matrix v1.1](https://cloudsecurityalliance.org/blog/2026/07/14/ai-controls-matrix-v1-1-strengthening-the-foundation-for-trustworthy-ai) | ai-control-framework | Control mapping and assurance |
| [MCP Security Best Practices 2026-07-28](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/2026-07-28/tutorials/security/security_best_practices.mdx) | protocol-security-guidance | MCP threat modeling and controls |
| [CycloneDX AI/ML-BOM](https://www.cyclonedx.org/capabilities/mlbom/) | supply-chain-transparency | AI supply-chain inventory and provenance |
| [OWASP GenAI Security Industry Framework Crosswalk](https://genai.owasp.org/resource-item/tools/) | framework-crosswalk | Cross-framework control mapping |
<!-- gen:frameworks:end -->

</details>

<details>
<summary><strong>Model and runtime intelligence</strong> &nbsp;·&nbsp; <sub>model families and deployment risk</sub></summary>

<br>

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

**Catalog:** [MODEL-CATALOG.md](docs/MODEL-CATALOG.md) · **Security matrix:** [MODEL-SECURITY-MATRIX.md](docs/MODEL-SECURITY-MATRIX.md) · **Data:** [`data/models.json`](data/models.json)

### Model families

<!-- gen:models:start -->
| Family | Provider | Deployment | Security focus |
|---|---|---|---|
| **GPT** | OpenAI | managed-api | api-identity, tool-use, agentic-workflows, application-controls |
| **gpt-oss** | OpenAI | open-weight, self-hosted | model-provenance, fine-tuning, runtime-security, supply-chain |
| **Claude** | Anthropic | managed-api, agentic-coding | tool-use, coding-agent, mcp, agentic-security |
| **Gemini** | Google | managed-api | multimodal, tool-use, rag, application-controls |
| **Gemma** | Google | open-weight, self-hosted | model-provenance, runtime-security, fine-tuning |
| **Llama** | Meta | open-weight, self-hosted, third-party-hosted | model-provenance, fine-tuning, serving-stack, supply-chain |
| **Qwen** | Alibaba / Qwen | open-weight, self-hosted, hosted | coding, reasoning, runtime-security, model-provenance |
| **DeepSeek** | DeepSeek | api, open-weight | reasoning, coding, self-hosted, model-provenance |
| **Mistral** | Mistral AI | api, open-weight, self-hosted | enterprise-deployment, model-provenance, api-security |
| **Grok** | xAI | managed-api | application-controls, tool-use, agentic-workflows |
| **Kimi** | Moonshot AI | managed-api | long-context, agentic-applications, api-security |
| **GLM** | Zhipu AI ecosystem | api, open-ecosystem | coding, agentic-applications, api-security |
<!-- gen:models:end -->

</details>

<details>
<summary><strong>Detection engineering</strong> &nbsp;·&nbsp; <sub>telemetry-backed detection hypotheses</sub></summary>

<br>

LLMInjection focuses on behaviors and trust-boundary crossings rather than trying to detect the string “AI”.

### High-value detection hypotheses

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

**Detection guide:** [docs/DETECTION-ENGINEERING.md](docs/DETECTION-ENGINEERING.md) · **Coverage:** [docs/DETECTION-COVERAGE.md](docs/DETECTION-COVERAGE.md) · **Starter rules:** [detections/](detections/)

### Detection hypotheses

<!-- gen:detections:start -->
| ID | Detection | Category | Severity | Status |
|---|---|---|---|---|
| `DET-AI-001` | **Unexpected LLM Provider Egress** | network | medium | specification |
| `DET-AI-002` | **Unauthorized Local LLM Runtime** | endpoint | medium | specification |
| `DET-AI-003` | **Agent Privilege Boundary Crossing** | agent-runtime | high | specification |
| `DET-AI-004` | **RAG or Memory Integrity Drift** | rag-memory | high | specification |
| `DET-AI-005` | **Model Artifact Provenance Drift** | supply-chain | high | specification |
| `DET-AI-006` | **AI Gateway Credential Anomaly** | identity | high | specification |
| `DET-AI-007` | **New or Changed MCP Capability** | mcp | medium | specification |
| `DET-AI-008` | **Agent Loop or Budget Exhaustion** | availability | medium | specification |
| `DET-AI-009` | **Automated Dependency Admission Without Review** | supply-chain | high | specification |
| `DET-AI-010` | **Sensitive Canary in Model Output** | data-protection | high | specification |
| `DET-AI-011` | **Assistant or IDE Config Written by Non-Editor Process** | agent-runtime | high | specification |
| `DET-AI-012` | **CI Token Read From Runner Process Memory** | identity | high | specification |
| `DET-AI-013` | **Systematic Prompt Harvesting Pattern** | data-protection | medium | specification |
| `DET-AI-014` | **Scanner Verdict Despite Refusal** | supply-chain | high | specification |
<!-- gen:detections:end -->

### Defensive controls

<!-- gen:controls:start -->
| ID | Control | Category |
|---|---|---|
| `CTRL-POLICY-OUTSIDE-MODEL` | **External Policy Enforcement** | authorization |
| `CTRL-INSTRUCTION-DATA-SEPARATION` | **Instruction / Data Separation** | prompt-context |
| `CTRL-TOOL-ALLOWLIST` | **Tool Capability Allowlist** | agentic |
| `CTRL-CONTEXTUAL-AUTHZ` | **Contextual Tool Authorization** | authorization |
| `CTRL-HUMAN-CHECKPOINT` | **Human Checkpoint for High-Impact Actions** | agentic |
| `CTRL-MEMORY-PROVENANCE` | **Memory Provenance and Scope** | memory |
| `CTRL-RAG-PROVENANCE` | **RAG Source Provenance** | rag |
| `CTRL-OUTPUT-SANITIZATION` | **Untrusted Output Handling** | application |
| `CTRL-EGRESS-POLICY` | **AI Egress Policy** | network |
| `CTRL-AI-INVENTORY` | **AI Asset and Service Inventory** | governance |
| `CTRL-ARTIFACT-PINNING` | **Artifact Digest Pinning** | supply-chain |
| `CTRL-SIGNATURE-VERIFICATION` | **Artifact Signature Verification** | supply-chain |
| `CTRL-DEPENDENCY-POLICY` | **Dependency Admission Policy** | supply-chain |
| `CTRL-MCP-TOKEN-AUDIENCE` | **MCP Token Audience Validation** | mcp |
| `CTRL-MCP-CONSENT` | **MCP Explicit User Consent** | mcp |
| `CTRL-MCP-STATE-BINDING` | **MCP State Handle Binding** | mcp |
| `CTRL-AIML-BOM` | **AI/ML Bill of Materials** | supply-chain |
| `CTRL-SECRET-ISOLATION` | **Secret Isolation** | identity |
| `CTRL-ACTION-BUDGET` | **Agent Action and Resource Budgets** | availability |
| `CTRL-AGENT-TELEMETRY` | **Agent Decision and Action Telemetry** | observability |
<!-- gen:controls:end -->

</details>

<details>
<summary><strong>Intelligence architecture</strong> &nbsp;·&nbsp; <sub>evidence model, grades and confidence</sub></summary>

<br>

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

### Evidence model

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

### Source registry by grade

<!-- gen:source-grades:start -->
| Grade | Class | Sources |
|---|---|---|
| **A** | Primary or authoritative | 36 |
| **B** | Strong secondary | 3 |
| **C** | Reputable press | 1 |
| **D** | Community | 0 |
| **E** | Unsupported | 0 |
<!-- gen:source-grades:end -->

</details>

<details>
<summary><strong>Research and evaluation ecosystem</strong> &nbsp;·&nbsp; <sub>red-team tools, benchmarks, standards</sub></summary>

<br>

LLMInjection indexes external projects for discovery and reproducible evaluation while keeping its CTI dataset evidence-driven.

| Area | Projects |
|---|---|
| GenAI red teaming | Microsoft **PyRIT**, NVIDIA **garak** |
| Jailbreak robustness | **JailbreakBench**, GCG / LLM Attacks |
| Adversarial ML | **Adversarial Robustness Toolbox**, TextAttack |
| Community corpora | jailbreak and prompt-security collections indexed as research sources |
| Standards | MITRE, OWASP, NIST, CSA, Google SAIF, ENISA |

Community corpora are discovery sources, **not self-authenticating intelligence**. Claims are promoted only after evidence review.

See [REFERENCE-LIBRARY.md](references/REFERENCE-LIBRARY.md), [BENCHMARKS.md](docs/BENCHMARKS.md), [AI-SUPPLY-CHAIN.md](docs/AI-SUPPLY-CHAIN.md) and [community-corpora.md](references/community-corpora.md).

### Ecosystem map: 75 related projects

The [ecosystem map](docs/ECOSYSTEM.md) classifies related repositories by **what each can honestly support**, so observed incidents, techniques demonstrated in research and lab examples never blur together. These entries inform taxonomy, tests, detections and controls. They never create an actor, campaign or incident record, and the validator rejects any entry that claims to support attribution.

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

#### Start here

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

All 75 entries, by section: [docs/ECOSYSTEM.md](docs/ECOSYSTEM.md). Provenance: supplied by the maintainer's research on 2026-10-07; repository state is recorded as reported and not independently verified.

</details>

<details>
<summary><strong>Roadmap</strong> &nbsp;·&nbsp; <sub>where the project is going</sub></summary>

<br>

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

Full roadmap: [docs/ROADMAP.md](docs/ROADMAP.md) · [Intelligence changelog](docs/INTELLIGENCE-CHANGELOG.md) · [Publishing & releases](docs/PUBLISHING.md)

</details>

## Repository layout

```text
data/          structured intelligence (JSON), monthly snapshots
schemas/       JSON Schemas for every dataset
scripts/       validation, graph/API/STIX builds, intake, queries, safe lab
detections/    Sigma, KQL, SPL, ES|QL and YARA-L rules
docs/          methodology, handbooks and the full overview (docs/README.md is the index)
site/          Explorer (GitHub Pages)
integrations/  read-only MCP server
references/    curated external reading and tooling
tests/         unit tests and fixtures
assets/        banner and generated charts
```

## Documentation

Everything above expands in place. For standalone handbooks, see the index in **[docs/README.md](docs/README.md)**.

## Contributing

Useful contributions add **evidence, relationships, tests, detections or corrections**, not hype. Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [methodology](docs/METHODOLOGY.md), prefer primary sources, preserve uncertainty, and run `make test validate` before opening a pull request.

LLMInjection is built for defenders, threat analysts, AI red teams, detection engineers and security architects. Offensive behavior is documented to support threat modeling and authorized evaluation, not turnkey abuse. Security reports: [SECURITY.md](SECURITY.md).

## License

Apache-2.0. See [LICENSE](LICENSE). Citation metadata: [CITATION.cff](CITATION.cff).

<p align="center"><sub><strong>Evidence over hype. Behavior over branding. Controls over vibes.</strong></sub></p>
