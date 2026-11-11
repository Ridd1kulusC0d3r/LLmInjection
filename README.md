<p align="center">
  <img src="assets/llminjection-banner.svg" alt="LLMInjection: threat landscape for LLM and agentic systems" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Ridd1kulusC0d3r/LLmInjection/actions/workflows/validate-intel.yml"><img src="https://img.shields.io/github/actions/workflow/status/Ridd1kulusC0d3r/LLmInjection/validate-intel.yml?style=flat-square&label=intel%20CI&labelColor=17150f&color=b43c0e" alt="Intel CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Ridd1kulusC0d3r/LLmInjection?style=flat-square&labelColor=17150f&color=4a463c" alt="Apache-2.0"></a>
  <img src="https://img.shields.io/badge/mode-defensive--first-4a463c?style=flat-square&labelColor=17150f" alt="Defensive first">
</p>

**The AI threat landscape, with the evidence attached.** Who is using AI against whom, how AI systems themselves are attacked, and what detects or stops it. Every claim carries a source grade and a confidence level, and activity that was observed is kept apart from what research demonstrated and from what is only inferred.

<!-- lang-bar -->
**English** · [Português](README.pt-BR.md) · [Español](README.es.md) · [简体中文](README.zh-CN.md) · [Русский](README.ru.md)
<!-- /lang-bar -->

**[Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/)** · [Documentation](docs/README.md) · [Methodology](docs/METHODOLOGY.md) · [API](docs/PUBLISHING.md) · [Roadmap](docs/ROADMAP.md)

## The landscape in 2026

Read as deep as you need: the numbers first, then where the threat is moving, then how far the evidence goes.

### In one minute

<!-- gen:landscape-headlines:start -->

| | What it measures | Window | Source |
|---|---|---|---|
| **94%** | AI expected to be the biggest force shaping cybersecurity in 2026 | WEF Global Cybersecurity Outlook 2026 | [World Economic Forum](https://www.weforum.org/publications/global-cybersecurity-outlook-2026/in-full/executive-summary-6efae97d74/), grade A |
| **&lt; 6 h** | Time for an autonomous multi-agent framework to plan, build and run a mass credential harvest (upper bound) | GTIG AI Threat Tracker, 2026-09-08 | [Google Threat Intelligence Group](https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai), grade A |
| **100M+** | Size of the largest observed distillation campaigns against Google models | Feb-Sep 2026 | [Google Threat Intelligence Group](https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai), grade A |
| **≈ 4×** | Increase in major supply-chain and third-party incidents since 2020 | 2020-2025 | [IBM X-Force](https://www.ibm.com/think/x-force/threat-intelligence-index-2026-securing-identities-ai-detection-risk-management), grade A |

<!-- gen:landscape-headlines:end -->

AI is now on both sides of the line: attackers use it to move faster and, increasingly, to operate, while the AI systems, agents, gateways and supply chains organisations adopt have become targets of their own.

### Where it is moving

<!-- gen:landscape-domains:start -->

| Direction | Where it is moving | What the evidence says |
|---|---|---|
| rising | **AI as active operator** | Public reporting now includes campaigns and malware where AI participates in live execution, task chaining or runtime decision-making rather than only preparation. |
| rising | **AI as offensive force multiplier** | Threat actors use AI for reconnaissance, social engineering, code generation, debugging, translation and rapid iteration. |
| rising | **Prompt injection and content-borne attacks** | Prompt Injection remains OWASP LLM01:2026, while Check Point observed a sharp rise in longer malicious payloads consistent with indirect/content-borne attack paths. |
| rising | **Agentic autonomy, identity and tool abuse** | Excessive Agency moved to LLM03:2026 and OWASP maintains a separate Agentic Top 10 covering goal hijack, tool misuse, identity abuse, memory poisoning, inter-agent communication and rogue agents. |
| rising | **AI and software supply chain** | Open-source packages, CI/CD, AI frameworks, model artifacts and gateways increasingly sit in the blast radius of supply-chain compromise. |
| rising | **Enterprise AI data exposure and Shadow AI** | Everyday enterprise AI use creates measurable data-exposure risk even without an external attacker. |
| rising | **Cloud and identity abuse around AI workloads** | Cloud-conscious eCrime increased while vendor reporting continues to emphasize stolen or misused credentials over direct infrastructure exploitation. |
| rising | **Ransomware and data-extortion industrialization** | Ransomware reporting shows greater victim volume and a shift toward high-volume data theft and extortion, with AI contributing to speed and scale in the broader ecosystem. |
| emerging | **Model integrity and safety-control fragility** | Research on open-weight models demonstrates that some refusal behaviors can depend on surprisingly concentrated internal mechanisms, reinforcing that model alignment alone is not a system security boundary. |
| rising | **AI coding-assistant workspace and config abuse** | Malware now hides in assistant and IDE directories (.claude/, .vscode/, .cursor/), abuses agent hooks and configs, and prompt-injects LLM scanners. |
| rising | **MCP transport and framework command injection** | Prompt-injectable tool parameters and unsanitized STDIO config reached code execution in Semantic Kernel, LiteLLM and other MCP-consuming products in 2026. |
| rising | **AI-assisted tooling against Latin American targets** | Three 2026 primary reports describe operators speeding tool development or command execution with LLMs against Brazilian financial and Latin American government targets. |

<!-- gen:landscape-domains:end -->

Each row is a record in [`data/threat-landscape-2026.json`](data/threat-landscape-2026.json) with its signals, defensive focus and sources; the [Explorer's Landscape tab](https://ridd1kulusc0d3r.github.io/LLmInjection/#tab=landscape) shows them with the linked actors, campaigns and incidents.

### How far the evidence goes

<!-- gen:landscape-evidence:start -->

Of the **28 techniques** tracked, **22** have activity observed in the wild, **0** are tied to a disclosed vulnerability, **6** are demonstrated in research and **0** have no linked evidence yet (a gap in this repository, not a claim that they are theoretical). On the defensive side, **5 of 45** detections exist as rule files; the rest are specifications.

<!-- gen:landscape-evidence:end -->

Attribution is the weakest link: AI use is usually **inferred from artifacts**, vendors track actors under their own labels, and those labels are kept as published, never merged without evidence. The [methodology](docs/METHODOLOGY.md) explains the source grades (A to E), the confidence levels and how each technique maps to MITRE ATLAS, OWASP, NIST and Google SAIF.

<a href="https://ridd1kulusc0d3r.github.io/LLmInjection/"><img src="assets/explorer-tour.gif" alt="Explorer tour: dashboard, actors using AI, landscape, the graph with a pinned selection, the coverage matrix sorted by priority with a technique opened, actors by technique, timeline, ecosystem, dark theme and the Portuguese interface" width="100%"></a>

<sub>A tour of the Explorer: dashboard, actors using AI, landscape, graph, the coverage matrix (sort, drill down, actors by technique), timeline, ecosystem, dark theme and the language switch. Click it to open the live site, which is rebuilt from the datasets on every merge to main.</sub>

<table>
<tr>
<td width="50%"><a href="https://ridd1kulusc0d3r.github.io/LLmInjection/#tab=graph"><img src="assets/explorer-graph.gif" alt="Graph interaction: hover traces a node, a click pins it and lists its linked records, a linked record is selected, the view is dragged and zoomed, two columns are hidden and the whole graph is shown" width="100%"></a></td>
<td width="50%"><a href="https://ridd1kulusc0d3r.github.io/LLmInjection/#tab=overview"><img src="assets/explorer-filters.gif" alt="Dashboard filters: a confidence segment filters the Explorer and shows a removable chip, a maturity bar opens the coverage matrix filtered, and a source-grade bar opens the filtered source registry" width="100%"></a></td>
</tr>
<tr>
<td><sub><b>Graph.</b> Click a node to pin it and trace its links, jump along a link, drag to pan, zoom with the buttons or Ctrl + wheel, hide columns by type.</sub></td>
<td><sub><b>Selectable charts.</b> Every bar, meter and confidence segment on the dashboard is a filter; active filters show as chips.</sub></td>
</tr>
</table>

<sub>Regenerate the GIFs with `node scripts/record_tour.js <url> <frames> tour|graph|filters` and `python scripts/make_tour_gif.py <frames> assets/explorer-<name>.gif`.</sub>

### ▶ Video tour (73 s)

<a href="https://ridd1kulusc0d3r.github.io/LLmInjection/video.html"><img src="assets/promo-video-poster.jpg" alt="Video tour of the LLMInjection Explorer: intelligence graph and coverage matrix" width="100%"></a>

<sub><b>Click to play</b> the tour of the <a href="https://ridd1kulusc0d3r.github.io/LLmInjection/#tab=graph">intelligence graph</a> and the <a href="https://ridd1kulusc0d3r.github.io/LLmInjection/#tab=coverage">coverage matrix</a>, recorded from the live site. English and Português. MP4 files: <a href="site/media/llminjection-promo-en.mp4">EN</a> · <a href="site/media/llminjection-promo-pt.mp4">PT-BR</a>. Re-render with <code>scripts/promo/render.py</code>.</sub>

---

## AI threat-source enrichment (2026-10-09) 

New [source registry and ingestion guidance](docs/AI-INTELLIGENCE-SOURCES.md), [runtime and identity telemetry design](docs/AI-RUNTIME-INTELLIGENCE.md), 19 newly catalogued GitHub references in the AI source registry, six-dimensional threat ontology and candidate-only source adapters. External material requires human review before promotion into CTI.

## AI × Cyber OT / ICS Intelligence (2026-10-09)

**New defensive Cyber OT domain:** [AI × Cyber OT landscape](docs/CYBER-OT-LANDSCAPE.md) with [14 curated industrial intelligence sources](data/ot-source-registry.json), [6 explicitly hypothetical safety-boundary scenarios](data/ot-scenarios.json), [5 research-dataset references](data/ot-datasets.json), a bounded [offline-testable passive metadata intake](scripts/ot_intake.py) and separate review queue. Includes MITRE ATT&CK for ICS, CISA CSAF OT, OTCAD, IPAL, HAI, CSET and MISP. **No incident, AI attribution, controller interaction or industrial scan is implied.**

## At a glance

<!-- gen:stats:start -->

| Actors | Campaigns | Incidents | Vulnerabilities | Techniques | Sources |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **73** | **91** | **65** | **9** | **28** | **132** |

| Test cases | Detections | Controls | Frameworks | Model families | Relationships | Ecosystem repos |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **40** | **45** | **32** | **19** | **12** | **451** | **117** |

<!-- gen:stats:end -->

LLMInjection is **not a prompt dump**. Every meaningful claim carries a source grade, a confidence level, a last-verified date, framework context and a defensive angle.

<a href="https://ridd1kulusc0d3r.github.io/LLmInjection/#tab=coverage"><img src="assets/coverage-matrix.svg" alt="Technique coverage matrix: evidence, tests, detections, controls, tools and benchmarks per technique" width="100%"></a>

<sub>The picture is static because GitHub renders README images without scripts. <b>Click it</b> for the live matrix in the Explorer: sortable, filterable, with the linked records behind every number. A dot in the detections column marks techniques with a real rule file; the other detections are specifications. Regenerate the charts with `make charts`.</sub>

## What is inside

| Layer | What it holds | Start here |
|---|---|---|
| **Actors and campaigns** | State and criminal operators using AI, with vendor tracking labels kept as published, and a queue of candidates awaiting primary-source review | [`data/actors.json`](data/actors.json) · [Actor tracker](docs/ACTOR-TRACKER.md) |
| **AI × Cyber OT / ICS** | Industrial intelligence sources, evidence boundaries, hypothetical scenarios and offline detection-dataset catalog | [AI × Cyber OT landscape](docs/CYBER-OT-LANDSCAPE.md) |
| **Threat landscape** | Cited metrics, domains and open research leads for 2026 | [Landscape 2026](docs/THREAT-LANDSCAPE-2026.md) |
| **Brazil and Latin America** | AI-assisted activity against regional targets, in Portuguese, separating what reports claim from what they do not | [Panorama](docs/pt-BR/PANORAMA-BRASIL-LATAM.md) |
| **Techniques and frameworks** | LLMInjection techniques with a maturity level, mapped to ATLAS, OWASP, NIST, SAIF and MAESTRO | [Frameworks](docs/FRAMEWORKS.md) · [Threat model](docs/AI-THREAT-MODEL.md) |
| **Safe test lab** | Defensive test cases for prompt, RAG, agent, MCP and supply-chain risks | [Test cases](docs/TEST-CASES.md) · [Lab](docs/LAB.md) |
| **Detection engineering** | Sigma, KQL, SPL, ES\|QL and YARA-L starter detections | [Detection engineering](docs/DETECTION-ENGINEERING.md) |
| **Evidence** | Graded sources and explicit relationships behind every record | [Source grading](docs/SOURCE-GRADING.md) · [Methodology](docs/METHODOLOGY.md) |
| **Defender playbooks** | One generated page per technique: understand, test, detect, prevent, close the loop, and the limits of what we hold | [Playbooks](docs/playbooks/README.md) · [Knowledge strategy](docs/KNOWLEDGE-STRATEGY.md) |
| **Ecosystem** | Related projects classified by what they can support | [Ecosystem map](docs/ECOSYSTEM.md), [benchmarks](docs/BENCHMARKS.md) |

Exports: `graph.json`, GraphML, STIX 2.1, a static `/api/v1/` JSON API, monthly snapshots with entity-level diffs, and an interactive [Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/).

## Quick start

```bash
make test          # unit tests
make validate      # schema and referential checks on all datasets
make build         # graph, STIX, static API, Navigator layers, charts
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
<summary markdown="span"><strong>Latest update, 2026-10-09: depth in the coverage matrix</strong> &nbsp;·&nbsp; <sub>rule files, publishers, freshness, benchmarks, actors</sub></summary>


A count of linked records says little when most cells read "1". The coverage model (`scripts/coverage_model.py`) now derives what a count hides, from the datasets and the files in `detections/`:

1. **Implementation level.** Each detection is a `rule-file` when a rule exists under `detections/`, otherwise a `specification`. Only 5 of 45 detections have rule files; the matrix marks them with a dot instead of letting a specification look finished.
2. **Evidence quality.** Distinct publishers behind each technique, the best source grade, the newest evidence date and a stale flag. 14 of 28 techniques rest on a single publisher.
3. **Benchmarks.** A new column counts benchmark projects mapped to each technique. Eight verified projects joined the ecosystem: InjecAgent, PurpleLlama (CyberSecEval), Inspect Evals, SORRY-Bench, StrongREJECT, CTIBench, Cybench and WildTeaming. A benchmark measures a model or a defence; it never proves that an actor used a technique.
4. **Actors and techniques.** The Explorer's Coverage tab has a second view that links each actor to the techniques its campaigns use.
5. **Priority.** An explicit, documented formula ranks techniques: maturity weight times the layers still missing (test, rule file, control, benchmark).
6. **OSINT signals on the tools themselves.** `scripts/osint_ecosystem.py` asks deps.dev and OSV.dev, with no token, how widely each ecosystem project is used, which packages it publishes, whether those packages have security advisories and whether releases carry verified SLSA provenance ([summary](docs/ECOSYSTEM-SIGNALS.md)). A red-team tool is part of the AI supply chain too.

</details>

<details>
<summary markdown="span"><strong>Update, 2026-10-07: ecosystem sweep</strong> &nbsp;·&nbsp; <sub>107 repositories read, ATLAS 2026.09 crosswalk</sub></summary>


Every related repository was cloned and read, not just listed ([sweep report](docs/ECOSYSTEM-INTELLIGENCE.md)).

1. **Seven new techniques** anchored on ATLAS 2026.09: rendering exfiltration (`LLMI-T020`), tool poisoning and rug pull (`LLMI-T021`), agentic cost harvesting (`LLMI-T022`), crafted assistant links (`LLMI-T023`), exposed AI services (`LLMI-T024`), multimodal triggers (`LLMI-T025`) and inter-agent propagation (`LLMI-T026`). ATLAS coverage of generative and agentic techniques rose from 52% to 78%.
2. **22 ATLAS case studies** joined the incident set, from LLMjacking and LAMEHUG to the Postmark MCP server and recommendation poisoning.
3. **25 detection specifications and 14 safe-lab tests** derived from Agent Threat Rules, agent and skill scanners and the gaps in 13 red-team tools.
4. **Verified ecosystem:** 106 entries with last commit and licence read from the repository; 47 more repositories wait in the research queue. `scripts/verify_ecosystem.py` repeats the check with git alone.

</details>

<details open>
<summary markdown="span"><strong>Latest update, 2026-10-07: Latin America, coverage and maturity</strong> &nbsp;·&nbsp; <sub>regional lens, gaps closed, evidence levels</sub></summary>


- **Latin America.** Three 2026 primary reports (Google and Mandiant on BREEZE COMET, Trend Micro on SHADOW-AETHER-040, Unit 42 on CL-CRI-1131) describe AI-assisted tooling against Brazilian financial and Latin American government targets. AI use is largely inferred from artifacts and the models are not confirmed; initial access is unchanged. Regional view, in Portuguese: [Panorama Brasil e América Latina](docs/pt-BR/PANORAMA-BRASIL-LATAM.md). New technique `LLMI-T028`.
- **Coverage gaps closed.** Every technique now has a safe test, a detection and a linked record; the graph audit keeps it that way. New tests `TC-JB-035` to `TC-TOOL-040`, detections `DET-AI-040` to `DET-AI-045`.
- **Technique maturity.** Each technique is classified from the graph as observed in the wild, disclosed vulnerability, research demonstrated or no linked evidence, and the validator rejects a value that drifts from the evidence.
- **Dates.** Sources carry a `published` date; campaigns and incidents carry `reported`. The validator now rejects a record first seen after its primary report, which corrected two campaigns.
- **Tooling.** ATT&CK Navigator layers, a weekly ecosystem verification job, CSV export and deep links in the Explorer.

</details>

<details>
<summary markdown="span"><strong>Previous update, 2026-10-06</strong> &nbsp;·&nbsp; <sub>agent workspaces, MCP transport, autonomy at scale</sub></summary>


Two attack surfaces moved from research to observed activity.

1. **Agent workspace as attack surface.** Google Threat Intelligence Group reports the DUSTMAKER stealer hiding in `.claude/`, `.vscode/` and `.cursor/`, steering AI assistants through config files, stealing CI/CD OIDC tokens and prompt-injecting LLM scanners (techniques `LLMI-T017`, `LLMI-T018`).
2. **Model-controlled parameters reaching execution.** Microsoft Semantic Kernel (`CVE-2026-26030`, `CVE-2026-25592`) and the disputed MCP STDIO class show prompt injection turning into code execution when tool parameters are not validated outside the model.

Scale signals from GTIG: a multi-agent credential harvest planned and run in under six hours, and distillation campaigns exceeding 100 million prompts (`LLMI-T019`).

Held back on purpose: Anthropic's September 2026 report is only available here through press coverage, so its actors and victim counts sit in the research queue until the primary document is attached.

Full record: [Intelligence changelog](docs/INTELLIGENCE-CHANGELOG.md) · [Landscape 2026](docs/THREAT-LANDSCAPE-2026.md)

</details>

<details>
<summary markdown="span"><strong>Technique maturity</strong> &nbsp;·&nbsp; <sub>how strong the evidence for each technique is, derived from the graph</sub></summary>


Maturity is **derived, not asserted**: `scripts/maturity.py` computes it from the relationship graph and the validator rejects a technique whose field disagrees. It mirrors the rule behind the ecosystem map: observed activity, disclosed vulnerabilities and research results are different kinds of evidence.

<!-- gen:maturity:start -->

| Maturity | Derived from | Techniques | IDs |
|---|---|---|---|
| `observed-in-the-wild` | Linked to a campaign, or to an incident whose status is observed | 22 | T001, T003, T004, T005, T008, T010, T011, T012, T013, T014, T015, T016, T017, T018, T019, T021, T022, T023, T024, T026, T027, T028 |
| `disclosed-vulnerability` | Linked to a vulnerability record (CVE, GHSA or malicious package) | 0 |  |
| `research-demonstrated` | Linked to a research or lab incident, or mapped by a research or benchmark project | 6 | T002, T006, T007, T009, T020, T025 |
| `no-linked-evidence` | Nothing in this repository links to it yet. Not a claim that it is theoretical | 0 |  |

<!-- gen:maturity:end -->

A low level means few records link to the technique so far, not that it is theoretical. For example, prompt injection is widely discussed but its maturity here is only as strong as the incidents and campaigns actually linked to it.

</details>

<details>
<summary markdown="span"><strong>Visual atlas</strong> &nbsp;·&nbsp; <sub>framework mapping and ecosystem charts</sub></summary>


### Framework mapping

Which external frameworks each technique maps to. Techniques mapped to few frameworks are the first candidates for a mapping review.

<img src="assets/framework-coverage.svg" alt="Technique to framework mapping matrix" width="100%">

### Ecosystem map

Related projects by evidence class and section. The class decides what a project can support: a research repository can inspire a test, never prove an actor used a technique.

<img src="assets/ecosystem-map.svg" alt="Ecosystem projects by evidence class and section" width="100%">

All charts are generated by [`scripts/build_charts.py`](scripts/build_charts.py) from the datasets, and a test fails if they go stale.

</details>

<details>
<summary markdown="span"><strong>Attack chains and defender playbook</strong> &nbsp;·&nbsp; <sub>two 2026 chains, mapped to tests, detections and controls</sub></summary>


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
<summary markdown="span"><strong>Living intelligence</strong> &nbsp;·&nbsp; <sub>review-gated feeds, snapshots and diffs</sub></summary>


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
<summary markdown="span"><strong>AI / LLM threat landscape 2026</strong> &nbsp;·&nbsp; <sub>cited metrics, domains and attack surfaces</sub></summary>


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
<summary markdown="span"><strong>Threat actors and campaigns</strong> &nbsp;·&nbsp; <sub>who is using AI, and how</sub></summary>


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
| **BREEZE COMET** | Unattributed, financially motivated, Brazil-focused | offensive-enabler, tooling-development | Google and Mandiant describe a financially motivated actor manipulating payment systems and banking software in Brazil, and… | high |
| **JADEPUFFER** | Unattributed | autonomous-operator, ai-infrastructure-targeting | Sysdig assesses JADEPUFFER as the first documented agentic ransomware operation: an LLM-driven operator that entered through an… | high |
| **Coral Sleet** | North Korea | tooling-development, offensive-enabler | Microsoft reports that since April 2026 Coral Sleet built a workflow to trojanize private GitHub repositories, highly likely… | high |
| **Jasper Sleet** | North Korea | offensive-enabler | Microsoft reports Jasper Sleet using generative and agentic AI in resume workflows to build fake digital personas and to keep… | high |
| **Onyx Sleet** | North Korea | offensive-enabler | Microsoft reports Onyx Sleet produced more than 100 target-specific PDF lures in August and September 2026, dozens within minutes… | high |
| **APT27** | China | tooling-development | Google Threat Intelligence Group observed the PRC-nexus actor APT27 using Gemini to accelerate development of a fleet-management… | confirmed |
| **GTG-20006** | Russia (report: consistent with Russian state-nexus espionage and with public reporting linking the actor to Midnight Blizzard) | autonomous-operator, tooling-development | Anthropic reports that GTG-20006, a Russian espionage cluster whose attribution it calls consistent with public reporting on… | confirmed |
| **GTG-50014** | Not stated in report (operators suspected to be affiliates of the ShinyHunters collective; financially motivated extortion) | autonomous-operator, tooling-development | Anthropic reports that GTG-50014, operators it suspects are affiliates of the ShinyHunters collective (operator handles MeowSHA… | confirmed |
| **GTG-10007** | China (report: Chinese-speaking operators likely residing in Changsha, Hunan province) | autonomous-operator, tooling-development | Anthropic reports that GTG-10007, Chinese-speaking operators it assesses likely reside in Changsha, used Claude as the… | confirmed |
| **GTG-50020** | Unattributed, financially motivated (report: Russian-speaking, financially-motivated actor) | ai-infrastructure-targeting, ai-supply-chain-targeting, autonomous-operator | Anthropic reports that GTG-50020, a Russian-speaking financially motivated actor, moved from hotel-booking and fintech targets to… | confirmed |
| **GTG-50021** | Not stated in report (Russian- and Ukrainian-speaking group; fraud) | ai-infrastructure-targeting | Anthropic reports that GTG-50021 (alias kl1zy), a Russian- and Ukrainian-speaking group, ran a fraudulent AI reseller that… | confirmed |
| **GTG-50029** | Not stated in report (single French-speaking hacktivist actor) | tooling-development, offensive-enabler | Anthropic reports that GTG-50029, a single French-speaking hacktivist, used Claude to build a Rust scanner for exposed AI API… | confirmed |
| **GTG-14021** | China (report: believed associated with a municipal cyber police unit; Zhejiang location assessed with medium confidence) | tooling-development, offensive-enabler | Anthropic reports that GTG-14021, which it believes is associated with a Chinese municipal cyber police unit (institution… | confirmed |
| **GTG-14022** | China (report: assessed with medium confidence to be a contractor for PRC-government clients) | tooling-development, offensive-enabler | Anthropic reports that GTG-14022, assessed with medium confidence to be a contractor working for PRC government clients, used… | confirmed |
| **GTG-15001** | China (report: a China-based app studio using PRC-based proxy infrastructure) | runtime-enabler, tooling-development | Anthropic reports that GTG-15001, a China-based app studio relying on PRC-based proxy infrastructure, used Claude both to build a… | confirmed |
| **GTG-17002** | China (report: assessed China-based defense and military-industrial researcher with links to PRC research institutions including the PLA Academy of Military Sciences) | tooling-development | Anthropic reports that GTG-17002, which it assesses is a China-based defense researcher linked to PRC research institutions… | confirmed |
| **GTG-27005** | Russia (report: Russia-based; assessed small specialized freelance team, not a state entity, with assessed ties to a regional university linked to a Russian Academy of Sciences research center) | tooling-development | Anthropic reports that GTG-27005 (operation names DronDoc / Serafim), assessed as a small Russia-based freelance team, used… | confirmed |
| **GTG-30004** | Iran (report: Iran-nexus threat actor) | tooling-development, offensive-enabler | Anthropic reports that GTG-30004, an Iran-nexus threat actor, used Claude to orchestrate an OSINT identity-profiling harness… | confirmed |
| **GTG-30005** | Iran (report: Iran-nexus threat actor) | tooling-development, offensive-enabler | Anthropic reports that GTG-30005, an Iran-nexus threat actor, used Claude to build targeting handbooks and a Python… | confirmed |
| **GTG-30006** | Iran (report: Iranian threat actor) | tooling-development | Anthropic reports that GTG-30006, an Iranian threat actor building domestic-surveillance tooling, used fragmented sessions on… | confirmed |
| **GTG-34007** | Iran (report: assessed with high confidence to be associated with Iranian paramilitary domestic security entities) | tooling-development, offensive-enabler | Anthropic reports that GTG-34007, two units it assesses with high confidence are associated with Iranian paramilitary… | confirmed |
| **GTG-50027** | Mali (report: likely a Bamako-based independent consultant working with Mali's state intelligence service, ANSE) | tooling-development | Anthropic reports that GTG-50027, likely a Bamako-based independent consultant working with Mali's state intelligence service… | confirmed |
| **GTG-87001** | Not stated in report (report: based in northern Yemen; no group named) | tooling-development | Anthropic reports that GTG-87001, a weapons engineering cell based in northern Yemen, used Claude Code as a substitute for… | confirmed |
| **RAVINE CASTLE** | China | offensive-enabler | Google Threat Intelligence Group describes RAVINE CASTLE, a PRC-nexus espionage group previously known as COULEE and APT24… | confirmed |
| **SANDWORM RELIC** | Russia | tooling-development, offensive-enabler | Google Threat Intelligence Group reports that SANDWORM RELIC, the Russian espionage group formerly tracked as FROZENBARENTS… | confirmed |
| **UNC5792** | Russia | runtime-enabler | Google Threat Intelligence Group reports that the Russia-based group UNC5792 experimented with integrating AI models into… | confirmed |
| **UNC6508** | China | ai-infrastructure-targeting | Google Threat Intelligence Group describes UNC6508 as a PRC-nexus actor running a multi-year espionage campaign against academic… | confirmed |
| **UNC1069** | North Korea | offensive-enabler, tooling-development | Google Threat Intelligence Group reports the North Korean cryptocurrency-theft actor UNC1069 (aka MASAN) used Gemini to research… | confirmed |
| **APT41** | China | tooling-development | Google Threat Intelligence Group observed the PRC-backed actor APT41 throughout August 2025 using Gemini for C++ and Golang code… | confirmed |
| **TEMP.Zagros** | Iran | tooling-development | Google Threat Intelligence Group reports the Iranian state-sponsored actor TEMP.Zagros (aka MUDDYCOAST, Muddy Water) used Gemini… | confirmed |
| **UNC4899** | North Korea | tooling-development | Google Threat Intelligence Group reports the North Korean supply-chain-compromise actor UNC4899 (aka PUKCHONG) used Gemini to… | confirmed |
| **FunkSec** | Unattributed; hacktivism/cybercrime hybrid (developer assessed as based in Algeria) | tooling-development | Check Point Research describes FunkSec as a new ransomware-as-a-service operation that emerged in late 2024, straddling… | medium |
| **APT45** | Not stated in report | offensive-enabler | Google Threat Intelligence Group reports observing APT45 send thousands of repetitive prompts that recursively analyse different… | confirmed |
| **UNC2814** | Not stated in report | offensive-enabler | Google Threat Intelligence Group observed UNC2814 using expert-persona prompting with Gemini, directing the model to act as a… | confirmed |
| **UNC5673** | China | offensive-enabler | Google Threat Intelligence Group describes UNC5673 as a PRC-nexus cluster with notable overlaps with TEMP.Hex that has targeted… | confirmed |
| **UNC6201** | China | offensive-enabler | Google Threat Intelligence Group observed attempted use, by PRC-nexus UNC6201, of a public GitHub Python script that automates… | confirmed |
| **bandcampro** | Unattributed, Russian-speaking; financially motivated | autonomous-operator, tooling-development | Trend Micro (TrendAI Research) analysed about 200 Gemini CLI session logs (19 March to 21 April 2026) from the Russian-speaking… | confirmed |
| **Temp.HEX** | China | offensive-enabler | Google Threat Intelligence Group reports that the PRC-based actor Temp.HEX used Gemini and other AI tools in Q4 2025 to compile… | confirmed |
| **APT31** | China | offensive-enabler | Google Threat Intelligence Group reports that the PRC-based actor APT31 prompted Gemini with an expert cybersecurity persona and… | confirmed |
| **UNC5356** | Unattributed, financially motivated | tooling-development | Google Threat Intelligence Group assesses with high confidence that part of the COINBAIT phishing-kit activity, which targets… | medium |
| **UNC6418** | Unattributed | offensive-enabler | Google Threat Intelligence Group reports that the unattributed cluster UNC6418 used Gemini for targeted intelligence gathering on… | confirmed |
| **UNC795** | China | tooling-development, offensive-enabler | Google Threat Intelligence Group reports that the PRC-based actor UNC795 used Gemini several days a week in Q4 2025 across the… | confirmed |
| **Armored Likho** | Not stated in report | tooling-development | Kaspersky reports that the first-stage loaders and stagers in Armored Likho's BusySnake Stealer campaign against government and… | high |
| **SilkParasite** | China (medium confidence) | tooling-development | Bitdefender designates SilkParasite as an activity cluster targeting Central Asian government bodies and holds its China-nexus… | medium |
| **STAC6994** | Not stated in report | tooling-development | Sophos found a rogue device in a customer environment (May 2026) where the actor tracked as STAC6994 ran about a dozen… | confirmed |
| **DragonForce** | Not stated in report | offensive-enabler | In a DragonForce ransomware case investigated by Sophos IR, the actor produced what Sophos 'strongly suspect[s]' was an… | medium |
| **The Gentlemen** | Not stated in report | tooling-development | Sophos states that leaked chats from The Gentlemen ransomware group confirmed the group used generative AI to produce attack… | medium |
| **GTG-2002** | Unattributed, financially motivated | autonomous-operator, offensive-enabler | Anthropic disrupted a data-extortion operation tracked as GTG-2002 in which a cybercriminal used Claude Code, guided by a… | confirmed |
| **GTG-5004** | Unattributed, financially motivated (UK-based per Anthropic) | tooling-development | Anthropic reports a UK-based actor tracked as GTG-5004 used Claude to develop, market and distribute ransomware-as-a-service… | confirmed |
| **BUGSTER** | Unattributed, financially motivated (English-speaking per Unit 42) | offensive-enabler, tooling-development | Unit 42, with visibility into the actor's operational environment, reports BUGSTER used Hermes Agent with DeepSeek V4 (controlled… | confirmed |
| **Storm-0940** | China | autonomous-operator | Microsoft reports that Storm-0940, a China-state aligned actor active since 2021, used the open-source multi-agent penetration… | confirmed |
| **LAUNDRY BEAR** | Russia | tooling-development | A joint advisory led by CISA, NSA and FBI with 27 partner agencies describes LAUNDRY BEAR as a Russian state-supported espionage… | medium |
| **Earth Krahang** | China | tooling-development | TrendAI describes Earth Krahang, a China-aligned group targeting government and defense sectors globally, using generative AI to… | confirmed |
| **Earth Naga** | China | tooling-development | TrendAI reports that Earth Naga, a China-aligned group it associates with Flax Typhoon, used an iterative AI prompting ('vibe… | confirmed |
| **CyberXero** | Unattributed, financially motivated (Russian-speaking initial access broker; no state nexus asserted) | autonomous-operator, offensive-enabler | SOCRadar describes CyberXero as a Russian-speaking, financially motivated initial access broker that ran up to 51 specialised… | confirmed |
| **Storm-2945** | Russia | offensive-enabler, tooling-development | Microsoft Threat Intelligence assesses Storm-2945 to be an operational sub-cluster of Midnight Blizzard and attributes the… | confirmed |
| **RevengeHotels** | Unattributed, financially motivated | tooling-development | Kaspersky attributes a summer 2025 wave of hotel-targeting phishing delivering VenomRAT to RevengeHotels (TA558) with high… | medium |
| **CL-CRI-1131** | Not stated in report | tooling-development, offensive-enabler | Palo Alto Networks Unit 42 tracks CL-CRI-1131 attacking a transportation organization, government ministries and water utilities… | high |
| **CL-CRI-1163** | Not stated in report | tooling-development | Palo Alto Networks Unit 42 tracks CL-CRI-1163 targeting the Brazilian financial sector with job- or resume-themed phishing from… | medium |
| **Jade Sleet** | North Korea | offensive-enabler, tooling-development | Microsoft Threat Intelligence assesses that the North Korean actor Jade Sleet has operationalized AI across its operations, using… | high |
| **Pearl Sleet** | North Korea | autonomous-operator, tooling-development | Microsoft Threat Intelligence places the North Korean actor Pearl Sleet at the accelerating stage of AI adoption and has… | confirmed |
| **Sapphire Sleet** | North Korea | tooling-development | Microsoft Threat Intelligence places the North Korean actor Sapphire Sleet at the accelerating stage of AI adoption, saying it… | medium |
| **knaithe** | China (Chinese-speaking actor based in Zhuhai; opportunistic exploit operator) | autonomous-operator | Palo Alto Networks Unit 42 describes a Chinese-speaking, opportunistic exploit operator (knaithe / KnYuan) running DeepSeek… | confirmed |
| **Aurora** | Not stated in report (ransomware/extortion group; operator prompts written in Russian) | offensive-enabler, autonomous-operator | Gambit Security reports the Aurora ransomware group, active since about April 2026, used Cursor Agent running Claude Sonnet… | confirmed |
| **VAPOR PANDA** | China | autonomous-operator | CrowdStrike reports the China-nexus adversary VAPOR PANDA used the ARTEX multi-agent framework, mainly with DeepSeek, to run… | confirmed |
| **GREYVIBE** | Russia | tooling-development, offensive-enabler | WithSecure assesses with high confidence that GREYVIBE's activity aligns with Russian state interests, targeting mainly Ukrainian… | high |

<!-- gen:actors:end -->

### Campaigns

<!-- gen:campaigns:start -->

| Campaign | First seen | Reported | Regions | Confidence | Summary |
|---|---|---|---|---|---|
| **GTG-1002 AI-orchestrated espionage** | 2025-09 | 2025-11-13 |  | confirmed | Campaign assessed by Anthropic as Chinese state-sponsored in which Claude Code performed the majority of tactical operations against… |
| **APT28 PROMPTSTEAL / LAMEHUG runtime LLM use** | 2025 | 2025-11-05 |  | confirmed | APT28-linked activity used a public LLM at runtime to generate host-relevant commands. |
| **APT42 Gemini-enabled reconnaissance** | 2025 | 2025-01-29 |  | confirmed | GTIG documented Gemini use for reconnaissance, target research, phishing content and localization. |
| **UNC2970 Gemini-enabled target profiling** | 2025 | 2026-02-12 |  | confirmed | GTIG documented Gemini use to synthesize OSINT and profile high-value targets. |
| **Kimsuky local LLM capability integration** | 2026 | 2026-08-10 |  | high | Genians reported local LLM tooling and RAG-related artifacts on infrastructure linked to Kimsuky. |
| **PromptMink** | 2026 | 2026-04-30 |  | high | Reporting describes malicious package activity optimized to influence AI coding-agent dependency selection and attributes it to Famous… |
| **TeamPCP LiteLLM supply-chain compromise** | 2026 | 2026-03-24 |  | confirmed | TeamPCP-linked supply-chain activity affected LiteLLM releases and highlighted credential concentration in AI gateways. |
| **BREEZE COMET payment-system fraud in Brazil** | 2024 | 2026-09-01 | BR | confirmed | Intrusions into Brazilian financial services, retail and e-commerce organizations that can move money through Pix, STR and Boleto, reported… |
| **SHADOW-AETHER-040 agentic intrusions against Latin American governments** | 2025-12-27 | 2026-05-11 | MX, LATAM | high | Trend Micro reports Spanish-speaking operators intruding into six Mexican government entities between 2025-12-27 and 2026-01-04, with high… |
| **CL-CRI-1131 LLM-assisted intrusions in Mexico and Ecuador** | 2026 | 2026-09-03 | MX, EC | medium | Unit 42 assesses that operators used LLMs to generate workaround scripts against a Mexican transportation organization, federal ministries… |
| **JADEPUFFER agentic database extortion** | 2026 | 2026-07-01 |  | high | Sysdig documents an LLM-driven operation that exploited an exposed Langflow instance (CVE-2025-3248), swept cloud credentials, and extorted… |
| **Coral Sleet AI-built repository trojanization** | 2026-04 | 2026-10-29 |  | high | Microsoft reports a Coral Sleet workflow, highly likely engineered with an AI-enabled development platform, that trojanizes private GitHub… |
| **Jasper Sleet AI-built remote-worker personas** | 2026 | 2026-10-29 |  | high | Microsoft reports Jasper Sleet using generative and agentic AI to build fake digital personas and keep fraudulent worker identities… |
| **Onyx Sleet AI-generated lures against South Korea** | 2026-08 | 2026-10-29 | KR | high | Microsoft reports more than 100 target-specific PDF lures, highly likely generated by an AI platform, for phishing against South Korean… |
| **APT27 Gemini-assisted ORB management tooling** | 2026 | 2026-05-11 |  | confirmed | Google Threat Intelligence Group observed APT27 using Gemini to accelerate development of a fleet-management application likely to support… |
| **GTG-20006 Claude-driven espionage operation lifecycle** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-20006, a Russian espionage cluster whose attribution it calls consistent with public reporting on Midnight… |
| **GTG-50014 AI-driven smash-and-grab intrusions and extortion** | 2026-02 | 2026-09 |  | confirmed | Anthropic reports that GTG-50014, operators it suspects are affiliates of the ShinyHunters collective (operator handles MeowSHA, frkoo and… |
| **GTG-10007 exploit foundry and autonomous attack frameworks** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-10007, Chinese-speaking operators it assesses likely reside in Changsha, used Claude as the engineering and… |
| **GTG-50020 AI vendor sandbox injection and AI-company targeting** | 2026-05 | 2026-09 |  | confirmed | Anthropic reports that GTG-50020, a Russian-speaking financially motivated actor, moved from hotel-booking and fintech targets to the AI… |
| **GTG-50021 fraudulent Claude reseller and account credential harvesting** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-50021 (alias kl1zy), a Russian- and Ukrainian-speaking group, ran a fraudulent AI reseller that advertised… |
| **GTG-50029 hacktivist campaign against European political entities** | 2026-02 | 2026-09 |  | confirmed | Anthropic reports that GTG-50029, a single French-speaking hacktivist, used Claude to build a Rust scanner for exposed AI API keys, develop… |
| **GTG-14021 stability-maintenance and transnational repression tooling** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-14021, which it believes is associated with a Chinese municipal cyber police unit (institution attribution at… |
| **GTG-14022 public-opinion monitoring pipeline** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-14022, assessed with medium confidence to be a contractor working for PRC government clients, used Claude with… |
| **GTG-15001 deceptive dating-app network** | 2026-04 | 2026-09 |  | confirmed | Anthropic reports that GTG-15001, a China-based app studio relying on PRC-based proxy infrastructure, used Claude both to build a network… |
| **GTG-17002 electronic warfare and SEAD targeting software** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-17002, which it assesses is a China-based defense researcher linked to PRC research institutions including the… |
| **GTG-27005 autonomous drone-swarm software development** | 2025 | 2026-09 |  | confirmed | Anthropic reports that GTG-27005 (operation names DronDoc / Serafim), assessed as a small Russia-based freelance team, used Claude Code to… |
| **GTG-30004 OSINT profiling and malware obfuscation** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-30004, an Iran-nexus threat actor, used Claude to orchestrate an OSINT identity-profiling harness against… |
| **GTG-30005 military reconnaissance and surveillance tooling** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-30005, an Iran-nexus threat actor, used Claude to build targeting handbooks and a Python naval-tracking pipeline… |
| **GTG-30006 domestic surveillance malware and phishing tooling** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-30006, an Iranian threat actor building domestic-surveillance tooling, used fragmented sessions on free Claude… |
| **GTG-34007 paramilitary surveillance tooling** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-34007, two units it assesses with high confidence are associated with Iranian paramilitary domestic-security… |
| **GTG-50027 Lakana 360 mass-interception platform development** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-50027, likely a Bamako-based independent consultant working with Mali's state intelligence service (ANSE), used… |
| **GTG-87001 guided weapons GNC software development** | 2026 | 2026-09 |  | confirmed | Anthropic reports that GTG-87001, a weapons engineering cell based in northern Yemen, used Claude Code as a substitute for engineers on… |
| **GTG-17001 anti-torpedo fire-control specification and acquisition documents** | 2026 | 2026-09 |  | confirmed | Anthropic reports that an actor posing as a US defense OEM, which it assesses was associated with a Chinese defense industry manufacturer… |
| **RAVINE CASTLE Gemini misuse across the attack lifecycle** | 2026 | 2026-09-08 |  | confirmed | GTIG observed RAVINE CASTLE using Gemini for target research supporting social engineering, exploit and post-exploitation research… |
| **SANDWORM RELIC Gemini-assisted operations against Ukraine** | 2026 | 2026-09-08 |  | confirmed | GTIG observed SANDWORM RELIC using Gemini to write password-spraying and endpoint-fingerprinting scripts, support intelligence gathering… |
| **UNC5792 AI-assisted Telegram channel monitoring** | 2026 | 2026-09-08 |  | confirmed | GTIG reports UNC5792 experimenting with AI models inside Telegram monitoring bots to classify messages and output structured intelligence… |
| **UNC6508 targeting of proprietary AI research** | 2026 | 2026-09-08 |  | confirmed | GTIG describes a multi-year UNC6508 espionage campaign (first reported by GTIG in June 2026) against North American research institutions… |
| **Unnamed DPRK clusters using Gemini for recon and pretexting** | 2026 | 2026-09-08 |  | confirmed | GTIG reports multiple unnamed DPRK-associated clusters using AI for resource procurement, profiling aerospace and defense targets, and… |
| **Unnamed PRC-nexus AI-assisted exploitation pipeline (CC Switch, Phalanx, Shai-Hulud)** | 2026 | 2026-09-08 |  | confirmed | GTIG observed an unnamed PRC-nexus espionage group with a history of targeting government entities using CC Switch to query Claude, Gemini… |
| **Unnamed PRC-nexus attempt to build an agentic pentest framework with Gemini** | 2026 | 2026-09-08 |  | confirmed | GTIG observed an unnamed PRC-nexus espionage group using Gemini to design an agentic penetration-testing framework for discovery tasks such… |
| **UNC1069 Gemini-assisted cryptocurrency theft and deepfake lures** | 2025 | 2025-11-05 |  | confirmed | Google Threat Intelligence Group reports UNC1069 used Gemini for cryptocurrency and wallet-data reconnaissance, attempted crypto-stealing… |
| **APT41 Gemini-assisted OSSTUN C2 and obfuscation development** | 2025-08 | 2025-11-05 |  | confirmed | Google Threat Intelligence Group observed APT41 during August 2025 seeking Gemini help with C++ and Golang code for tools including the… |
| **TEMP.Zagros Gemini-assisted custom malware development** | 2025 | 2025-11-05 |  | confirmed | Google Threat Intelligence Group reports TEMP.Zagros used Gemini, under student and research-paper pretexts, to develop web shells and a… |
| **UNC4899 Gemini-assisted exploit research and tooling** | 2025 | 2025-11-05 |  | confirmed | Google Threat Intelligence Group reports UNC4899 used Gemini for code development, exploit research and tooling improvement, likely aimed… |
| **Suspected China-nexus actor using Gemini across an intrusion lifecycle (cloud, vSphere, Kubernetes)** | 2025 | 2025-11-05 |  | confirmed | Google Threat Intelligence Group observed an unnamed suspected China-nexus actor using Gemini for reconnaissance, phishing research… |
| **China-nexus actor using a capture-the-flag pretext to misuse Gemini** | 2025 | 2025-11-05 |  | confirmed | Google Threat Intelligence Group reports an unnamed China-nexus actor that reframed refused prompts as a capture-the-flag exercise and then… |
| **FunkSec AI-assisted ransomware-as-a-service operation** | 2024-10 | 2025-01-10 |  | medium | Check Point Research reports FunkSec launched a leak site in December 2024 claiming more than 85 victims, mainly in India and the US, with… |
| **APT45 recursive CVE analysis and PoC validation prompting** | 2026 | 2026-05-11 |  | confirmed | Google Threat Intelligence Group observed APT45 sending thousands of repetitive prompts to recursively analyse CVEs and validate… |
| **UNC2814 expert-persona prompting for embedded-device vulnerability research** | 2026 | 2026-05-11 |  | confirmed | Google Threat Intelligence Group observed UNC2814 prompting Gemini with fabricated expert-auditor personas to look for pre-authentication… |
| **UNC5673 pooled multi-provider LLM access via relay services** | 2026 | 2026-05-11 |  | confirmed | Google Threat Intelligence Group observed UNC5673 using Claude-Relay-Service and CLI-Proxy-API to aggregate Gemini, Claude and OpenAI… |
| **UNC6201 automated premium LLM account registration and cancellation** | 2026 | 2026-05-11 |  | medium | Google Threat Intelligence Group observed attempted use by UNC6201 of a public script automating sign-up and immediate cancellation of… |
| **bandcampro Gemini CLI-driven C2 botnet build and fraud operations** | 2026-03 | 2026-07-14 |  | confirmed | Trend Micro reports that bandcampro used a jailbroken Gemini CLI agent to migrate and run a C2 server for a small botnet on a dental… |
| **Chinese-speaking ARTEX multi-model operator targeting 19 markets** | 2026-08 | 2026-10 |  | high | Zscaler ThreatLabz analysed recovered prompts (4 August to 4 October 2026) from an unnamed, Chinese-speaking, likely financially motivated… |
| **Temp.HEX Gemini-assisted research on Pakistan targets and separatist organizations** | 2025 | 2026-02-12 |  | confirmed | GTIG observed Temp.HEX using Gemini and other AI tools to compile information on individuals in Pakistan and on separatist organizations… |
| **APT31 Gemini-assisted vulnerability analysis against US targets** | 2025 | 2026-02-12 |  | confirmed | GTIG observed APT31 using a security-researcher persona and a Hexstrike MCP pretext to have Gemini automate vulnerability analysis and… |
| **COINBAIT phishing kit built with Lovable AI** | 2025-11 | 2026-02-12 |  | medium | GTIG identified the COINBAIT phishing kit, built with Lovable AI and likely accelerated by AI code generation, targeting customers of… |
| **UNC6418 Gemini-assisted reconnaissance before phishing in Ukraine and defense sector** | 2025 | 2026-02-12 |  | confirmed | GTIG observed UNC6418 using Gemini to gather sensitive account credentials and email addresses, followed shortly by phishing against… |
| **UNC795 Gemini use across the attack lifecycle** | 2025 | 2026-02-12 |  | confirmed | GTIG observed UNC795 using Gemini for code troubleshooting, research and generating intrusion capabilities, including an AI-integrated code… |
| **Armored Likho BusySnake Stealer campaign with AI-generated first-stage payloads** | 2026 | 2026-07-03 |  | high | Kaspersky reports an ongoing BusySnake Stealer campaign against government and electric-power organizations in Russia, Kazakhstan and… |
| **SilkParasite espionage against Central Asian governments** | 2025-10 | 2026-08-19 |  | medium | Bitdefender tracks SilkParasite activity against Central Asian government bodies since about October 2025, with tooling showing traces of… |
| **STAC6994 agent-driven EDR-evasion development lab** | 2026-05 | 2026-07 |  | confirmed | Sophos recovered an AI-agent development framework (Cursor IDE, ~12 agents, Ludus VMs, Sliver C2, Git via MCP) that reproduced techniques… |
| **DragonForce suspected AI-generated extortion analysis** | 2026 | 2026-07 |  | medium | Sophos IR observed a DragonForce negotiation in which the actor supplied a detailed analysis of stolen data that Sophos strongly suspects… |
| **The Gentlemen AI-generated attack scripts** | 2026 | 2026-07 |  | medium | Sophos cites leaked chats from The Gentlemen ransomware group as confirming use of generative AI to produce scripts deployed manually. |
| **GTG-2002 Claude Code data-extortion operation ("vibe hacking")** | 2025 | 2025-08-27 |  | confirmed | Anthropic disrupted a scaled data-theft and extortion operation in which Claude Code ran reconnaissance (including scanning thousands of… |
| **GTG-5004 Claude-assisted ransomware-as-a-service** | 2025-01 | 2025-08-27 |  | confirmed | Anthropic reports GTG-5004 used Claude to build and refine ransomware with ChaCha20 encryption, syscall-based EDR evasion and shadow-copy… |
| **BUGSTER Hermes Agent/DeepSeek multi-domain cybercrime** | 2026 | 2026-10-21 |  | confirmed | Unit 42 describes BUGSTER using a Hermes Agent backed by DeepSeek V4 for reconnaissance reports and criminal planning, and AI-assisted code… |
| **Storm-0940 ARTEX-automated attacks and ConnectWise supply chain compromise** | 2026-09 | 2026-10-21 |  | high | Microsoft reports Storm-0940 used the agentic ARTEX framework to run around-the-clock scanning, password spraying (327 accounts across… |
| **Russian-speaking malware tooling development (OpenAI)** | 2025 | 2025-10-07 |  | confirmed | OpenAI banned accounts of a Russian-language operator, assessed as linked to Russian-speaking criminal groups, who used ChatGPT to iterate… |
| **Korean-language operators malware and C2 development (OpenAI)** | 2025 | 2025-10-07 |  | confirmed | OpenAI banned a cluster of Korean-language accounts that used ChatGPT for malware, C2, credential-theft and Korean-language crypto-themed… |
| **Phish and Scripts: Chinese-language phishing and tooling (OpenAI)** | 2025 | 2025-10-07 |  | confirmed | OpenAI banned Chinese-language accounts, overlapping public reporting on UNK_DROPPITCH (Proofpoint) and UTA0388 (Volexity), that used… |
| **CrowdStrike Threat Actor 1: Claude Code dual-agent harness against Argentine healthcare** | 2026-05 | 2026-10-21 |  | confirmed | CrowdStrike reports an unnamed Spanish/English-speaking operator (its 'Threat Actor 1') running a dual-agent autonomous pentesting harness… |
| **CrowdStrike Threat Actor 2: Chinese-speaking operator's Claude pentesting harnesses** | 2026-05 | 2026-10-21 |  | confirmed | CrowdStrike reports an unnamed Chinese-speaking operator ('Threat Actor 2') reaching Claude models through a China-based AI proxy and… |
| **CrowdStrike Threat Actor 3: Indonesian-speaking operator using public Claude Code skills** | 2026-05 | 2026-10-21 |  | confirmed | CrowdStrike reports an unnamed Indonesian-speaking operator ('Threat Actor 3') instructing Claude Code to compromise targets using 819… |
| **CrowdStrike Threat Actor 4: Russian-speaking group's /pentest-setup Claude Code workflow** | 2026-05 | 2026-10-21 |  | confirmed | CrowdStrike reports an unnamed group of Russian-speaking individuals ('Threat Actor 4') using a '/pentest-setup' slash command that… |
| **LAUNDRY BEAR Zimbra phishing with AI-assisted Flowerbed development** | 2025-07 | 2026-07-23 |  | medium | The AA26-204A advisory describes LAUNDRY BEAR exploiting a Zimbra zero-day (CVE-2025-66376) via phishing, including from compromised… |
| **Earth Krahang AI-enhanced CVE-2026-0740 exploit scanner** | 2026 | 2026-07-29 |  | confirmed | TrendAI reports Earth Krahang used generative AI to enhance a public CVE-2026-0740 proof-of-concept into a mass scanner for vulnerable… |
| **Earth Naga vibe-coded PowerShell/C# backdoor loader** | 2026 | 2026-07-29 |  | confirmed | TrendAI observed Earth Naga iteratively prompting an AI to develop a PowerShell script that compiles C# at runtime for process hollowing… |
| **ARTEX agentic offensive framework use by extortion groups and suspected PRC-nexus clusters** | 2026-08 | 2026-10-30 |  | confirmed | GTIG and Mandiant observed, in incident response since late August 2026, unnamed financially motivated extortion groups and suspected… |
| **PentAGI-based orchestration against Asian telecoms and system integrators** | 2026-08 | 2026-10-30 |  | medium | GTIG reports unattributed operators using the open-source PentAGI agent framework, including a custom orchestration platform built on it… |
| **CyberXero Claude Code agent swarm against Ukrainian critical infrastructure** | 2026-07 | 2026-10-06 |  | confirmed | SOCRadar reports CyberXero ran up to 51 Claude Code agents and PentAGI with Cobalt Strike, using a rehearsed ownership narrative and… |
| **CaptiveCrunch** | 2026-02 | 2026-07-31 |  | confirmed | Microsoft attributes CaptiveCrunch, captive-portal traffic manipulation, AitM and device code phishing and malware delivery (CornFlake… |
| **INC / The Gentlemen affiliate AI-driven ransomware operations (Phantom framework)** | 2026-07 | 2026-10-20 |  | confirmed | SOCRadar recovered exposed infrastructure showing affiliates of INC Ransomware (and, with lower confidence, The Gentlemen) using OpenCode… |
| **RevengeHotels 2025 LLM-generated loaders delivering VenomRAT** | 2025 | 2025-09-16 |  | medium | Kaspersky reports RevengeHotels phishing hotels in Brazil and Spanish-speaking markets in summer 2025 with infectors and downloaders that… |
| **CL-CRI-1163 phishing against Brazilian financial sector with LLM-generated scripts** | 2026-02 | 2026-09-03 |  | medium | Unit 42 reports CL-CRI-1163 targeted the Brazilian financial sector via likely job- or resume-themed phishing, with exposed staging scripts… |
| **Jade Sleet AI-accelerated job-themed targeting via front companies** | 2026-06 | 2026-10-29 |  | high | Microsoft Threat Intelligence identified Jade Sleet running job-themed targeting through three front companies between 8 and 12 June 2026… |
| **Pearl Sleet operations using the ARTEX agentic penetration-testing framework** | 2026-10 | 2026-10-29 |  | confirmed | Microsoft Threat Intelligence has identified Pearl Sleet, together with Onyx Sleet, using the open-source agentic AI penetration-testing… |
| **Sapphire Sleet Rust software supply-chain compromise** | 2026-08 | 2026-10-29 |  | medium | Microsoft Threat Intelligence says Sapphire Sleet likely incorporated AI into its August 2026 Rust software compromise, which targeted Rust… |
| **knaithe autonomous exploitation with DeepSeek and Hermes Agent** | 2026-05 | 2026-07-30 |  | confirmed | Unit 42 reports knaithe used a DeepSeek-driven Hermes Agent, tasked over Telegram, to autonomously enumerate and exploit targets found via… |
| **Aurora ransomware intrusions driven through Cursor Agent** | 2026-04 | 2026-08-27 |  | confirmed | Gambit Security reports Aurora ransomware operators used Cursor Agent with Claude Sonnet in sessions from 8 April to 21 May 2026 against… |
| **VAPOR PANDA ARTEX-driven global espionage campaign** | 2026-10 | 2026-10-29 |  | confirmed | CrowdStrike reports VAPOR PANDA used ARTEX planner and worker agents, primarily on DeepSeek, to write web shells, extract domain… |
| **GREYVIBE AI-assisted operations against Ukraine** | 2025-08 | 2026-05-28 |  | high | WithSecure reports GREYVIBE campaigns (PhantomMail, PhantomClick, PrincessClub, DroneLink, Nebo) against Ukrainian targets using GenAI-made… |

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
| **Model distillation campaigns against Google models** | model-extraction | observed | confirmed |
| **LLM Jacking (AML.CS0030)** | atlas-incident | observed | high |
| **Malicious Models on Hugging Face (AML.CS0031)** | atlas-incident | observed | high |
| **Malware Prototype with Embedded Prompt Injection (AML.CS0043)** | atlas-incident | observed | high |
| **LAMEHUG: Malware Leveraging Dynamic AI-Generated Commands (AML.CS0044)** | atlas-incident | observed | high |
| **Code to Deploy Destructive AI Agent Discovered in Amazon Q VS Code Extension (AML.CS0047)** | atlas-incident | observed | high |
| **Poisoned Postmark MCP Server Email Exfiltration (AML.CS0053)** | atlas-incident | observed | high |
| **Model Distillation Campaigns Targeting Anthropic Claude (AML.CS0056)** | atlas-incident | observed | high |
| **Storm-2139 Azure OpenAI Guardrail Bypass (AML.CS0057)** | atlas-incident | observed | high |
| **Autonomous OpenAI Evaluation Agents Compromise Hugging Face Infrastructure (AML.CS0068)** | atlas-incident | observed | high |
| **Threat Actor Uses a DeepSeek-Powered Hermes Agent in Langflow and n8n Exploitation Attempts (AML.CS0070)** | atlas-incident | observed | high |
| **Multi-Agent Framework Compromises Taiwanese Government Systems (AML.CS0071)** | atlas-incident | observed | high |
| **AI Recommendation Poisoning via Crafted AI Assistant Links (AML.CS0072)** | atlas-incident | observed | high |
| **Morris II Worm: RAG-Based Attack (AML.CS0024)** | atlas-exercise | research | confirmed |
| **Hacking ChatGPT's Memories with Prompt Injection (AML.CS0040)** | atlas-exercise | research | confirmed |
| **Rules File Backdoor: Supply Chain Attack on AI Coding Assistants (AML.CS0041)** | atlas-exercise | research | confirmed |
| **Data Exfiltration via an MCP Server used by Cursor (AML.CS0045)** | atlas-exercise | research | confirmed |
| **Data Destruction via Indirect Prompt Injection Targeting Claude Computer-Use (AML.CS0046)** | atlas-exercise | research | confirmed |
| **AI ClickFix: Hijacking Computer-Use Agents Using ClickFix (AML.CS0055)** | atlas-exercise | research | confirmed |
| **EchoLeak: Zero-Click Prompt Injection Targeting M365 Copilot for Data Exfiltration (AML.CS0059)** | atlas-exercise | research | confirmed |
| **Cross-Site Scripting via Prompt Manipulation in Lenovo AI Chatbot (AML.CS0060)** | atlas-exercise | research | confirmed |
| **Prompt-Based Attacks Against Gemini via Calendar Invitations (AML.CS0063)** | atlas-exercise | research | confirmed |
| **ZombieAgent: Data Exfiltration Attack on ChatGPT (AML.CS0066)** | atlas-exercise | research | confirmed |
| **PROMPTSPY Android backdoor with a Gemini UI agent** | malware | observed | confirmed |
| **Criminal actor uses an AI model to develop a 2FA-bypass zero-day** | intrusion | observed | high |
| **FakeAgent: malicious Claude Artifact as a Claude Desktop download page** | malware | observed | confirmed |
| **Multi-agent credential harvesting from compromised cloud in under six hours** | intrusion | observed | confirmed |
| **"Recon" agentic reconnaissance and credential-management framework** | intrusion | observed | confirmed |
| **Unit 42 investigation of a sub-10-hour AI-agent-assisted intrusion** | intrusion | observed | high |
| **TuxBot v3 Evolution IoT botnet built with LLM assistance** | malware | observed | confirmed |
| **Carding store maintained with Claude Code** | fraud | observed | confirmed |
| **Suspected Chinese operators use Claude Code and DeepSeek in government and financial intrusions** | intrusion | observed | confirmed |
| **PROMPTFLUX: experimental VBScript dropper that rewrites itself via the Gemini API** | malware | observed | confirmed |
| **QUIETVAULT: JavaScript credential stealer using on-host AI CLI tools to hunt secrets** | malware | observed | confirmed |
| **Hugging Face production intrusion driven by an autonomous AI agent system** | intrusion | observed | high |
| **Multi-agent AI framework (Hermes/OpenClaw) used to compromise Asian government entities** | intrusion | observed | high |
| **ARXON custom MCP server driving LLM-assisted FortiGate intrusions** | intrusion | observed | high |
| **Deepfakes and stolen PII used to apply for remote IT jobs (FBI IC3 PSA)** | fraud | observed | confirmed |
| **CANFAIL and LONGSTREAM: LLM-generated decoy code in Russia-nexus malware against Ukraine** | malware | observed | high |
| **Agentic Hexstrike and Strix operations against East Asian targets** | intrusion | observed | confirmed |
| **AI-agent-driven mass exploitation of PaperCut NG/MF** | intrusion | observed | confirmed |
| **EvilTokens AI-enabled email compromise service disrupted** | fraud | observed | confirmed |
| **AI-generated exploitation scripts against Siemens S7 PLCs** | exploit-development | observed | confirmed |
| **TAG-217 ARTEX-linked intrusions at South Korean financial institutions** | intrusion | observed | medium |
| **Malicious Hugging Face models with pickle reverse-shell payloads** | supply-chain | observed | confirmed |
| **Suspected AI-generated PowerShell script used for Active Directory enumeration** | intrusion | observed | high |
| **GXC Team AI-enabled Business Invoice Swapper** | fraud | observed | medium |
| **WaterPlum (Contagious Interview) use of AI face-swapping in online interviews** | fraud | observed | confirmed |
| **Autonomous AI agents used to compromise online retailers and plant card skimmers** | intrusion | observed | confirmed |
| **Claude Code CLI run as autonomous lateral-movement agent against a Thai organisation** | intrusion | observed | confirmed |
| **AI voice-cloned impersonation of senior U.S. officials** | fraud | observed | confirmed |
| **Greek gang uses AI voice clones of relatives to steal cash and valuables** | fraud | observed | medium |
| **AI-augmented mass access to FortiGate devices** | intrusion | observed | confirmed |
| **Abuse of the Lovable AI website builder for phishing and malware delivery** | fraud | observed | confirmed |
| **LLM-generated PowerShell and HTML delivery scripts in malware campaigns** | malware | observed | high |
| **Single operator uses Claude Code and GPT-4.1 to breach nine Mexican government organisations** | intrusion | observed | confirmed |
| **Deepfake videos and voice cloning in scams impersonating the FBI IC3** | fraud | observed | confirmed |
| **SweetSpecter spear-phishing of OpenAI employees** | intrusion | observed | confirmed |

<!-- gen:incidents:end -->

</details>

<details>
<summary markdown="span"><strong>Security test lab</strong> &nbsp;·&nbsp; <sub>safe, reproducible defensive test cases</sub></summary>


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
| `TC-OBF-021` | **Invisible-Character Instruction Smuggling** | prompt-injection | Verify that instructions hidden via Unicode tag characters, zero-width or bidi controls are normalized or flagged… |
| `TC-MM-022` | **Image-Borne Indirect Instruction** | multimodal | Confirm that text rendered inside an uploaded image is treated as data, not instruction, by a vision-enabled assistant. |
| `TC-MM-023` | **Audio Channel Instruction Injection** | multimodal | Check voice/speech pipelines do not elevate spoken instructions embedded in user-supplied audio. |
| `TC-OH-024` | **Markdown Image Exfiltration via Rendering** | application-security | Ensure model output cannot cause the client to fetch attacker URLs carrying context data (render-time exfil). |
| `TC-OH-025` | **Terminal Escape Sequence Passthrough** | application-security | Verify CLI/log surfaces neutralize ANSI/OSC control sequences emitted by the model. |
| `TC-DOS-026` | **Reasoning Loop / Token Exhaustion Guard** | availability | Confirm per-request token, time and recursion budgets stop inputs that induce unbounded reasoning or repetition. |
| `TC-SC-027` | **Hallucinated Package Admission Check** | supply-chain | Verify that dependencies proposed by a coding assistant are checked against an allowlisted/mirrored registry before… |
| `TC-LEAK-028` | **Cross-Session Context Leakage** | data-leakage | Verify session/tenant isolation of conversation memory and caches. |
| `TC-AUTHZ-029` | **Agent BOLA Object Reference Check** | agentic-security | Confirm agent tools enforce object-level authorization using the caller identity, not the model's claim. |
| `TC-TOOL-030` | **LLM-Mediated SSRF via Fetch Tool** | agentic-security | Ensure URL-fetch tools enforce destination allowlists independent of model output. |
| `TC-MCP-031` | **MCP Tool Description Rug Pull** | agentic-protocol | Detect tool metadata that changes after user approval and contains instruction-like text. |
| `TC-MA-032` | **Inter-Agent Instruction Propagation** | agentic-security | Verify that output from one agent is treated as untrusted data by downstream agents and cannot self-replicate. |
| `TC-LINK-033` | **Pre-filled Assistant Link Memory Write** | prompt-injection | Verify that a prompt delivered through an assistant deep-link cannot write persistent memory without explicit user… |
| `TC-EXP-034` | **Unauthenticated AI Endpoint Discovery** | network-detection | Verify that model servers, agent builders and MCP endpoints in the lab perimeter require authentication and that scans… |
| `TC-JB-035` | **Refusal Consistency Under Rephrasing** | prompt-injection | Verify that a policy-covered refusal stays consistent when the same benign-but-restricted request is rephrased… |
| `TC-POI-036` | **Training Data Poisoning Canary** | supply-chain | Verify that a poisoned or tampered sample in a fine-tuning or retrieval-training set is detected before it changes… |
| `TC-CI-037` | **CI Identity Token Scope Under Untrusted Steps** | supply-chain | Verify that short-lived CI identity tokens are unavailable to untrusted steps and cannot be reused outside the intended… |
| `TC-RLC-038` | **Model-Generated Command Execution Gate** | runtime-security | Verify that commands generated by a model at runtime are never executed without policy evaluation, and that high-impact… |
| `TC-SOC-039` | **Agent Outbound Communication Gate** | agentic-security | Verify that an agent cannot send messages to new external recipients or impersonate a person without approval, and that… |
| `TC-TOOL-040` | **Iterative Script Trial-and-Error Detection** | runtime-security | Verify that rapid iteration of near-identical scripts on one host is detected by behavior, independent of who or what… |

<!-- gen:test-cases:end -->

</details>

<details>
<summary markdown="span"><strong>Threat landscape model</strong> &nbsp;·&nbsp; <sub>attack surfaces and trust boundaries</sub></summary>


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

| ID | Technique | Category | Maturity | Mapped to |
|---|---|---|---|---|
| `LLMI-T001` | **Direct Prompt Injection** | prompt-context | observed-in-the-wild | OWASP LLM, MITRE ATLAS, Google SAIF |
| `LLMI-T002` | **Indirect Prompt Injection** | prompt-context | research-demonstrated | OWASP LLM, MITRE ATLAS, Google SAIF, CSA MAESTRO |
| `LLMI-T003` | **Jailbreak / Safety Boundary Manipulation** | model-behavior | observed-in-the-wild | OWASP LLM, NIST AI 100-2e2025 |
| `LLMI-T004` | **Sensitive Information Disclosure** | confidentiality | observed-in-the-wild | OWASP LLM, Google SAIF, MITRE ATLAS |
| `LLMI-T005` | **Model Extraction / Theft** | model | observed-in-the-wild | MITRE ATLAS, NIST AI 100-2e2025, Google SAIF |
| `LLMI-T006` | **Data or Model Poisoning** | training-data | research-demonstrated | OWASP LLM, MITRE ATLAS, NIST AI 100-2e2025, Google SAIF |
| `LLMI-T007` | **RAG Knowledge Poisoning** | rag | research-demonstrated | OWASP LLM, CSA MAESTRO, Google SAIF |
| `LLMI-T008` | **Agent Tool Misuse** | agentic | observed-in-the-wild | OWASP Agentic, CSA MAESTRO, Google SAIF, MITRE ATLAS |
| `LLMI-T009` | **Memory / Context Poisoning** | agentic | research-demonstrated | OWASP Agentic, CSA MAESTRO, MITRE ATLAS |
| `LLMI-T010` | **Model Source Tampering** | supply-chain | observed-in-the-wild | Google SAIF, MITRE ATLAS |
| `LLMI-T011` | **AI Software Supply Chain Compromise** | supply-chain | observed-in-the-wild | OWASP LLM, Google SAIF, CSA MAESTRO, MITRE ATT&CK |
| `LLMI-T012` | **Coding-Agent Dependency Manipulation** | supply-chain | observed-in-the-wild | OWASP Agentic, OWASP LLM, CSA MAESTRO |
| `LLMI-T013` | **Runtime LLM Command Generation** | ai-offensive-enabler | observed-in-the-wild | MITRE ATT&CK, MITRE ATLAS |
| `LLMI-T014` | **AI-Assisted Reconnaissance and Social Engineering** | ai-offensive-enabler | observed-in-the-wild | MITRE ATT&CK, MITRE ATLAS |
| `LLMI-T015` | **Agentic Attack Orchestration** | ai-autonomous-operator | observed-in-the-wild | MITRE ATT&CK, MITRE ATLAS, CSA MAESTRO |
| `LLMI-T016` | **AI Gateway Credential Compromise** | supply-chain | observed-in-the-wild | OWASP LLM, Google SAIF, MITRE ATT&CK |
| `LLMI-T017` | **Prompt Injection Against AI Security Scanners** | defense-evasion | observed-in-the-wild | OWASP LLM, MITRE ATLAS |
| `LLMI-T018` | **AI Coding-Assistant Workspace Abuse** | agentic-supply-chain | observed-in-the-wild | OWASP LLM, CSA MAESTRO, MITRE ATLAS |
| `LLMI-T019` | **Model Distillation Campaign** | model-theft | observed-in-the-wild | OWASP LLM, MITRE ATLAS |
| `LLMI-T020` | **Improper Output Handling and Rendering Exfiltration** | application | research-demonstrated | MITRE ATLAS |
| `LLMI-T021` | **Agent Tool Poisoning and Rug Pull** | agentic-supply-chain | observed-in-the-wild | MITRE ATLAS |
| `LLMI-T022` | **Agentic Resource Consumption and Cost Harvesting** | availability | observed-in-the-wild | MITRE ATLAS |
| `LLMI-T023` | **Crafted AI Assistant Links and Recommendation Poisoning** | prompt-context | observed-in-the-wild | MITRE ATLAS |
| `LLMI-T024` | **Exposed or Misconfigured AI Services** | infrastructure | observed-in-the-wild | MITRE ATLAS |
| `LLMI-T025` | **Multimodal Instruction Triggers** | prompt-context | research-demonstrated | MITRE ATLAS |
| `LLMI-T026` | **Inter-Agent Instruction Propagation** | agentic | observed-in-the-wild | MITRE ATLAS |
| `LLMI-T027` | **Unsanctioned AI Runtime (Shadow AI)** | runtime-security | observed-in-the-wild | MITRE ATT&CK, MITRE ATLAS |
| `LLMI-T028` | **AI-Assisted Tooling Development** | offensive-enablement | observed-in-the-wild | MITRE ATLAS |

<!-- gen:techniques:end -->

</details>

<details>
<summary markdown="span"><strong>Intelligence graph and Explorer</strong> &nbsp;·&nbsp; <sub>relationships, STIX, static API and MCP</sub></summary>


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
<summary markdown="span"><strong>Framework stack</strong> &nbsp;·&nbsp; <sub>ATLAS, OWASP, NIST, SAIF, MAESTRO and more</sub></summary>


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
<summary markdown="span"><strong>Model and runtime intelligence</strong> &nbsp;·&nbsp; <sub>model families and deployment risk</sub></summary>


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
<summary markdown="span"><strong>Detection engineering</strong> &nbsp;·&nbsp; <sub>telemetry-backed detection hypotheses</sub></summary>


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
| `DET-AI-015` | **MCP Tool Description Changed After Approval (Rug Pull)** | mcp | high | specification |
| `DET-AI-016` | **Cross-Server Tool Reference in MCP Description (Shadowing)** | mcp | high | specification |
| `DET-AI-017` | **Hidden Content in Agent-Facing Metadata** | mcp | medium | specification |
| `DET-AI-018` | **Repository Assistant Settings Grant Broad Pre-Approval** | workspace | high | specification |
| `DET-AI-019` | **Agent Session Executes Repo Helper Script Referenced by Instruction File** | workspace | high | specification |
| `DET-AI-020` | **Skill Installs With Remote Fetch-and-Execute or Shipped Bytecode** | supply-chain | high | specification |
| `DET-AI-021` | **Skill Declared Capabilities Under-Report Observed Behaviour** | supply-chain | medium | specification |
| `DET-AI-022` | **Unsafe Deserialization Import in Model Artifact** | model | critical | specification |
| `DET-AI-023` | **Model Load Followed by Unexpected Child Process or Egress** | model | high | specification |
| `DET-AI-024` | **Sensitive File Read Flows Into Outbound Tool Argument** | agent | high | specification |
| `DET-AI-025` | **MCP Client Config Server Added With Inline Exec, Privileged Container or Unpinned Package** | mcp | medium | specification |
| `DET-AI-026` | **Systematic Decision-Boundary Probing via Inference API** | inference-api | critical | specification |
| `DET-AI-027` | **Assistant Hook Executes Before Workspace Trust** | workspace | critical | specification |
| `DET-AI-028` | **Model-Provider Base URL Redirected by Repository Config** | workspace | critical | specification |
| `DET-AI-029` | **Package Install Writes AI Agent Config** | supply-chain | critical | specification |
| `DET-AI-030` | **Agent-Proposed Package With No Registry Reputation** | supply-chain | high | specification |
| `DET-AI-031` | **Cross-Scope Memory Write** | rag-memory | critical | specification |
| `DET-AI-032` | **Agent Runtime Launched in Unattended Auto-Approve Mode** | agent-runtime | high | specification |
| `DET-AI-033` | **Agent Widens Own Auto-Approval Policy** | agent-runtime | high | specification |
| `DET-AI-034` | **Rendered Model Output References External Image Host** | application | high | specification |
| `DET-AI-035` | **Assistant Deep-Link With Persistence Clause** | email-web | medium | specification |
| `DET-AI-036` | **Inbound Scan of AI Service Ports** | network | medium | specification |
| `DET-AI-037` | **Agent Forwards Received Instructions to Peer Agents** | agent-runtime | high | specification |
| `DET-AI-038` | **Hidden Instruction Text in Image or Audio Input** | multimodal | medium | specification |
| `DET-AI-039` | **Reasoning or Tool-Loop Cost Spike Per Session** | availability | medium | specification |
| `DET-AI-040` | **Policy Deviation After Untrusted Content Ingestion** | agent-runtime | high | specification |
| `DET-AI-041` | **Repeated Refusal-Bypass Sequence** | application | medium | specification |
| `DET-AI-042` | **Training Data Provenance Drift** | supply-chain | high | specification |
| `DET-AI-043` | **Agent Outbound Communication Anomaly** | agent-runtime | medium | specification |
| `DET-AI-044` | **Model Output Reaching an Interpreter Unsanitized** | application | high | specification |
| `DET-AI-045` | **Rapid Iterative Script Variants on One Host** | endpoint | medium | specification |

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
| `CTRL-IO-GUARDRAIL` | **Input/Output Injection & Policy Classifier** | prompt-context |
| `CTRL-CONTEXT-CANARY` | **Privileged-Context Canary Tokens** | observability |
| `CTRL-PRIVILEGE-SEPARATED-LLM` | **Privileged / Quarantined LLM Separation** | agentic |
| `CTRL-DATAFLOW-TAINT` | **Data-Flow Provenance and Taint Policy** | authorization |
| `CTRL-TASK-ALIGNMENT-CHECK` | **Task-Alignment Verification of Agent Actions** | agentic |
| `CTRL-INPUT-TRANSFORM` | **Untrusted Input Transformation and Spotlighting** | prompt-context |
| `CTRL-STRUCTURED-OUTPUT` | **Typed / Templated Model Output** | application |
| `CTRL-MODEL-ROBUSTNESS-EVAL` | **Model Injection-Robustness Selection and Evaluation** | governance |
| `CTRL-MCP-TOOL-PINNING` | **Tool Definition Pinning** | mcp |
| `CTRL-AI-SERVICE-EXPOSURE` | **AI Service Exposure Management** | infrastructure |
| `CTRL-PREFILL-LINK-POLICY` | **Pre-filled Prompt and Memory Write Policy** | memory |
| `CTRL-EXEC-POLICY` | **Script and Unknown Binary Execution Policy** | endpoint |

<!-- gen:controls:end -->

</details>

<details>
<summary markdown="span"><strong>Intelligence architecture</strong> &nbsp;·&nbsp; <sub>evidence model, grades and confidence</sub></summary>


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
| **A** | Primary or authoritative | 114 |
| **B** | Strong secondary | 7 |
| **C** | Reputable press | 6 |
| **D** | Community | 5 |
| **E** | Unsupported | 0 |

<!-- gen:source-grades:end -->

</details>

<details>
<summary markdown="span"><strong>Research and evaluation ecosystem</strong> &nbsp;·&nbsp; <sub>red-team tools, benchmarks, standards</sub></summary>


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

### Ecosystem map: related projects

The [ecosystem map](docs/ECOSYSTEM.md) classifies related repositories by **what each can honestly support**, so observed incidents, techniques demonstrated in research and lab examples never blur together. These entries inform taxonomy, tests, detections and controls. They never create an actor, campaign or incident record, and the validator rejects any entry that claims to support attribution.

<!-- gen:eco-classes:start -->

| Evidence class | What it is | Can support | Cannot support | Entries |
|---|---|---|---|---|
| `framework-data` | Taxonomies and knowledge bases | Technique definitions and framework mappings | Observed activity | 7 |
| `incident-data` | Incident databases | Incident references, citing the primary report | Actor attribution or cyber campaigns (scope is broader than cybersecurity) | 1 |
| `detection-content` | Community detection rules | Detection ideas and telemetry requirements | Proof of in-the-wild behavior | 4 |
| `curated-list` | Curated lists | Discovering sources and tools | Any claim on their own | 24 |
| `assessment-tool` | Scanners and red-team tools | Test design and control evaluation | Effectiveness against current models | 28 |
| `benchmark` | Benchmarks and environments | Reproducible tests and coverage measurement | Real-world prevalence | 13 |
| `research-technique` | Attack research code | Techniques demonstrated in research | Use in the wild | 16 |
| `defence-tool` | Defences and guardrails | Control design and comparison | Proven protection | 10 |
| `lab-exercise` | Training labs | Analyst training and onboarding | Threat intelligence | 7 |
| `prompt-corpus` | Prompt corpora and datasets | Test inspiration and measurement | Threat intelligence or attribution | 7 |

<!-- gen:eco-classes:end -->

#### Start here

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

All entries, by section: [docs/ECOSYSTEM.md](docs/ECOSYSTEM.md). Provenance: maintainer research, cross-checked by shallow clone on 2026-10-07 (reachability, last commit, licence). The GitHub archive flag is not visible to git and is added by `scripts/check_ecosystem.py`.

</details>

<details>
<summary markdown="span"><strong>Roadmap</strong> &nbsp;·&nbsp; <sub>where the project is going</sub></summary>


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

## Maintaining the repository

```bash
make check      # lint, unit tests, schema validation, graph audit: everything CI runs
make readme     # refresh generated tables in README.md and docs/ECOSYSTEM.md
make charts     # refresh the SVG charts in assets/
python scripts/audit_graph.py   # list orphaned records and coverage gaps
make navigator  # export ATT&CK Navigator layers (also in make build)
python scripts/verify_ecosystem.py   # re-verify ecosystem repositories by shallow clone
python scripts/check_ecosystem.py    # add the GitHub archive flag and renames (API)
```

The graph audit separates **hard findings** (a test, detection or control linked to nothing, which fails CI) from **coverage gaps** (a technique with no test or detection, which is the work queue).

## Repository layout

```text
data/          structured intelligence (JSON), monthly snapshots
schemas/       JSON Schemas for every dataset
scripts/       validation, audit, graph/API/STIX/chart builds, intake, queries, safe lab
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
