# LLMInjection AI Threat Model

LLMInjection models AI cyber risk across **role**, **surface**, **trust boundary**, **adversary objective** and **observable behavior**.

## Axis 1 — Role of AI

### AI as Target
The attacker targets the model, data, retrieval layer, agent, tools, supply chain or serving infrastructure.

Examples of threat families:
- prompt injection and indirect prompt injection;
- jailbreak/safety-boundary manipulation;
- data/model poisoning;
- model theft and extraction;
- malicious model or dependency substitution;
- RAG knowledge-base poisoning;
- agent tool abuse;
- memory/context poisoning;
- model gateway and CI/CD compromise.

### AI as Offensive Enabler
The attacker uses AI to accelerate a mostly human-directed operation.

Common use cases:
- reconnaissance and OSINT synthesis;
- social-engineering content generation/localization;
- code translation, debugging and malware development;
- vulnerability research;
- data triage and document analysis.

### AI as Autonomous Operator
AI executes meaningful parts of the attack loop with limited human intervention.

Track separately from ordinary "AI assistance" because autonomy changes:
- speed;
- scale;
- task chaining;
- error modes;
- detection windows;
- human decision points.

### AI as Defensive Control Plane
AI is used by defenders for detection, triage, policy, response, evaluation or threat hunting. These systems become security-critical assets and need their own threat model.

## Axis 2 — Attack Surface

| Surface | Representative risks |
|---|---|
| Data | poisoning, unauthorized data, leakage, provenance failures |
| Model | evasion, extraction, backdoors, unsafe behavior |
| Prompt/context | direct/indirect injection, instruction collision, context poisoning |
| RAG/knowledge | malicious documents, retrieval manipulation, stale or untrusted corpora |
| Agent/orchestrator | goal hijack, memory abuse, planning failures, excessive autonomy |
| Tools/plugins | confused deputy, privilege abuse, unsafe arguments, tool substitution |
| Protocols | MCP/A2A trust, identity, message integrity, capability discovery |
| Application | output handling, authz gaps, insecure integration |
| Supply chain | model/package/dataset compromise, malicious release, compromised CI |
| Infrastructure | model serving, GPU/cloud, secret storage, observability gaps |

## Axis 3 — Trust Boundaries

Every AI system should explicitly map boundaries between:

1. user and application;
2. application and model;
3. model and retrieved content;
4. model and tools;
5. agent and agent;
6. orchestration layer and credentials;
7. build pipeline and model/package registries;
8. AI gateway and external providers;
9. telemetry and security control plane.

The key design assumption is simple: **content is not authority**. A document, web page, tool response or retrieved chunk may contain instructions but must not automatically gain the privileges of the system prompt, application policy or human operator.

## Axis 4 — Adversary Objectives

- influence model behavior;
- disclose sensitive information;
- gain unauthorized action;
- persist in memory or knowledge;
- steal model/data/IP;
- compromise the AI supply chain;
- degrade availability or economics;
- evade detection;
- accelerate a broader cyber operation.

## Axis 5 — Observable Behavior

Intelligence is useful only if it can lead to observation or control.

For each threat family, record:

- **entry point**;
- **preconditions**;
- **affected component**;
- **security consequence**;
- **telemetry**;
- **detection hypothesis**;
- **preventive control**;
- **containment control**;
- **framework mappings**.

## Defensive principle

Treat LLM output as untrusted data until policy and context authorize an action. For agents, the decisive security boundary is usually not the model's text response but the transition from **text to capability**: API call, shell/tool invocation, file write, message send, credential use or state change.
