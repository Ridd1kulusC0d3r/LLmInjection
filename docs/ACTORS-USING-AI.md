# Actors Using AI

This view focuses on **documented threat-actor use of, targeting of, or operational dependence on AI systems**.

It is intentionally smaller than a conventional APT encyclopedia. Inclusion requires evidence that AI materially appears in the activity being tracked.

## Current tracked actors

| Actor / cluster | Nexus | AI role | Campaign / activity | Confidence |
|---|---|---|---|---|
| GTG-1002 | China | autonomous operator · offensive enabler | AI-orchestrated espionage using Claude Code | confirmed |
| APT28 / FROZENLAKE | Russia | runtime enabler | PROMPTSTEAL / LAMEHUG runtime LLM command generation | confirmed |
| APT42 | Iran | offensive enabler | Gemini-assisted reconnaissance, target research and content generation | confirmed |
| UNC2970 | North Korea nexus | offensive enabler | Gemini-assisted OSINT synthesis and target profiling | confirmed |
| Kimsuky | North Korea | local analysis · offensive enabler | local LLM environments and RAG-related capability integration | high |
| Famous Chollima / Shifty Corsair | North Korea | AI supply-chain targeting · coding-agent targeting | PromptMink dependency-selection manipulation reporting | high |
| TeamPCP | Unattributed | AI infrastructure targeting · supply chain | LiteLLM and related software supply-chain activity | confirmed |

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

The tracker lists **141** actors or clusters that use AI in cyber operations (plus 17 deepfake-fraud entries). LLMInjection holds **9** of them. **107** reported in 2025 or later are in the research queue as `actor-candidate`, and **92** report URLs we do not cite (69 from vendors or governments) as `source-candidate`. Its 78 ATT&CK IDs were checked against Enterprise ATT&CK 20.1: 2 are retired there, 0 unknown.

Top candidates by score (recency, number of references, vendor or government reporting). None is verified yet.

| Candidate | Reported | References | Vendor or government |
|---|---|---|---|
| APT45 | May 2026 | 2 | yes |
| Earth Krahang | Jul 2026 | 2 | yes |
| Earth Naga | Jul 2026 | 2 | yes |
| LAUNDRY BEAR | Jul 2026 | 2 | yes |
| Sapphire Sleet | Mar 2026 | 2 | yes |
| ShinyHunters | Sep 2026 | 2 | yes |
| Temp.HEX | Feb 2026 (updated Sep 2026) | 2 | yes |
| UnSub (ARTEX agentic pentest, South Korean finance) — CrowdStrike | Oct 2026 | 2 | yes |
| UnSub (FortiGate campaign) — Amazon Threat Intelligence | Feb 2026 | 2 | yes |
| UnSub (Mexican government campaign) — Gambit Security | Apr 2026 | 2 | yes |
| UnSub (PaperCut NG/MF agentic exploitation campaign) — GreyNoise/Blackpoint | Sep 2026 | 2 | yes |
| UnSub (possibly Earth Lamia) — Trend Micro | Jul 2026 | 2 | yes |
| UnSub (suspected China-nexus) — Hunt.io | Jul 2026 | 2 | yes |
| UNC1069 | Nov 2025 (updated Sep 2026) | 3 | yes |
| APT31 | Feb 2026 | 1 | yes |

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
