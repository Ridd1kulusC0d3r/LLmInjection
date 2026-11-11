# Actors Using AI

This view focuses on **documented threat-actor use of, targeting of, or operational dependence on AI systems**.

It is intentionally smaller than a conventional APT encyclopedia. Inclusion requires evidence that AI materially appears in the activity being tracked.

## Current tracked actors

Generated from `data/actors.json`; every row cites at least one source.

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

## AI-role taxonomy

### Autonomous operator

AI materially participates in multi-step execution or orchestration rather than only preparing content.

Current tracked example: **GTG-1002**.

### Runtime enabler

An AI/LLM capability is invoked during live operations to generate or adapt commands or actions.

Current tracked example: **APT28 / PROMPTSTEAL**.

### Offensive enabler

AI supports reconnaissance, research, social engineering, translation, synthesis, development or other attack preparation.

Current tracked examples: **APT42**, **UNC2970**, **Kimsuky**.

### Local AI capability

The actor operates self-hosted or local model tooling as part of its working environment.

Current tracked example: **Kimsuky**.

### AI supply-chain / coding-agent targeting

The activity targets trust placed in AI software, model gateways, coding agents or dependency-selection workflows.

Current tracked examples: **Famous Chollima / PromptMink**, **TeamPCP**.

## What this page does not claim

- Use of an AI service does not automatically imply autonomous intrusion.
- Code that merely looks AI-generated is not accepted as evidence of AI-assisted malware development.
- Vendor actor labels are not automatically merged into universal aliases.
- Shared national nexus does not imply two clusters are the same actor.
- A research demonstration is not converted into an actor campaign.

## Querying the dataset

Local CLI:

```bash
python scripts/query_intel.py search "Gemini" --type campaign
python scripts/query_intel.py get ACTOR-APT28
python scripts/query_intel.py neighbors ACTOR-GTG-1002
python scripts/query_intel.py recent --limit 20
```

MCP exposes equivalent read-only queries through [integrations/mcp/](../integrations/mcp/).

## Intelligence path

```text
Actor
  ↓ conducts
Campaign
  ↓ uses
Technique
  ↓ external mapping
ATLAS / ATT&CK / OWASP
  ↓
Test / Detection / Control
  ↓
Evidence source
```

## Candidate pipeline

LLMInjection tracks both halves of the problem: attacks **against** AI systems and adversaries **using** AI in their operations. The second half grows through a candidate pipeline, never by bulk import. A community tracker is compared with the datasets by `scripts/ai_actor_tracker_check.py`; what is missing goes to the research queue, and an analyst promotes a candidate only after reading the primary report.

<!-- gen:actor-tracker-gap:start -->

The tracker lists **141** actors or clusters that use AI in cyber operations (plus 17 deepfake-fraud entries). LLMInjection holds **68** of them. **48** reported in 2025 or later are in the research queue as `actor-candidate`, and **31** report URLs we do not cite (18 from vendors or governments) as `source-candidate`. Its 78 ATT&CK IDs were checked against Enterprise ATT&CK 20.1: 2 are retired there, 0 unknown.

Top candidates by score (recency, number of references, vendor or government reporting). None is verified yet.

| Candidate | Reported | References | Vendor or government |
|---|---|---|---|
| UnSub (ARTEX agentic pentest, South Korean finance) — CrowdStrike | Oct 2026 | 2 | yes |
| UnSub (FortiGate campaign) — Amazon Threat Intelligence | Feb 2026 | 2 | yes |
| UnSub (Mexican government campaign) — Gambit Security | Apr 2026 | 2 | yes |
| UnSub (PaperCut NG/MF agentic exploitation campaign) — GreyNoise/Blackpoint | Sep 2026 | 2 | yes |
| UnSub (possibly Earth Lamia) — Trend Micro | Jul 2026 | 2 | yes |
| UnSub (suspected China-nexus) — Hunt.io | Jul 2026 | 2 | yes |
| CRAFTY FALCON | Nov 2026 | 1 | yes |
| EvilTokens | Sep 2026 | 1 | yes |
| GTG-17001 | Sep 2026 | 1 | yes |
| Multiple UnSub (DPRK) — GTIG | Sep 2026 | 1 | yes |
| Multiple UnSub — CrowdStrike | Feb 2026 | 1 | yes |
| PROMPTSPY | May 2026 | 1 | yes |
| Storm-1747 | Apr 2026 | 1 | yes |
| Storm-2945 (CaptiveCrunch) | Jul 2026 | 1 | yes |
| UnSub ("Recon" agentic infostealer framework) — GTIG | Sep 2026 | 1 | yes |

Snapshot of `cybershujin/Threat-Actors-use-of-Artifical-Intelligence` at `6aba8f0a0c` (2026-11-09); licence: none declared. Regenerate with `scripts/ai_actor_tracker_check.py`.

<!-- gen:actor-tracker-gap:end -->

Promotion checklist for an `actor-candidate`:

1. Read the vendor or government report, not the tracker's summary or press coverage.
2. Record the vendor's own label and nexus wording. Do not merge it with an existing actor unless the report says they are the same.
3. Pick the AI role from the taxonomy above from what the report shows, not from what it speculates.
4. Grade the source and set confidence separately (see [Methodology](METHODOLOGY.md)).
5. Link the campaign to techniques only where the report describes the behaviour.

## Expansion rule

The target is not to collect every APT name.

The target is to maintain the strongest evidence-backed catalog of **how real threat actors are using, abusing or targeting AI systems**.
