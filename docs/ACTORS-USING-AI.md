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

## Expansion rule

The target is not to collect every APT name.

The target is to maintain the strongest evidence-backed catalog of **how real threat actors are using, abusing or targeting AI systems**.
