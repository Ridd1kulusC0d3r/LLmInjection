# Model Family Catalog

Last reviewed: **2026-09-30**

This catalog tracks model **families and deployment characteristics**, not a leaderboard of which model is easiest to jailbreak. Security behavior changes by release, system policy, host application, tools, retrieval, account tier and provider-side controls.

## Families

| Family | Provider / ecosystem | Typical deployment | Security relevance |
|---|---|---|---|
| GPT / OpenAI API models | OpenAI | managed API | tool use, agentic workflows, API identity, application controls |
| gpt-oss | OpenAI | open-weight / self-hosted | local deployment, fine-tuning, model provenance, runtime security |
| Claude | Anthropic | managed API / agentic coding | coding agents, tool use, MCP ecosystems, agentic security |
| Gemini | Google | managed API / platform | multimodal/agentic applications, provider identity, tool/RAG security |
| Gemma | Google | open-weight / self-hosted | local/open-weight deployment and model provenance |
| Llama | Meta | open-weight / self-hosted / hosted | broad downstream fine-tuning and serving ecosystem |
| Qwen | Alibaba / Qwen | open-weight / hosted ecosystem | coding/reasoning use, self-hosted deployments |
| DeepSeek | DeepSeek | API + open-weight releases | local/hosted reasoning and coding deployments |
| Mistral | Mistral AI | API + open/open-weight models | mixed managed/self-hosted enterprise deployments |
| Grok | xAI | managed/API ecosystem | application and agent security |
| Kimi | Moonshot AI | managed/API ecosystem | long-context/agent-oriented application surface |
| GLM | Zhipu AI ecosystem | API + open ecosystem | coding/agent use and regional deployment ecosystem |

## Why family-level tracking

A statement such as "Model X is vulnerable to prompt injection" is usually too weak to be useful.

A proper security record needs at least:

- exact model/version;
- release or snapshot date;
- provider/runtime;
- system/application policy;
- tools and permissions;
- RAG or memory state;
- attack/evaluation method;
- number of attempts;
- evaluator/judge;
- defense stack;
- date tested.

Without that context, jailbreak claims become screenshots with branding.

## Deployment classes

### Managed API models

Key controls:
- API identity and key lifecycle;
- gateway policy;
- data handling;
- model/version pinning when available;
- request logging and cost anomaly detection;
- tool/action authorization outside the model.

### Open-weight / self-hosted

Key controls:
- source and digest verification;
- model license and provenance;
- serving-stack hardening;
- dependency and container integrity;
- fine-tuning provenance;
- runtime isolation;
- model inventory.

Open-weight systems have a different security model because the organization controls weights and runtime, but also inherits more supply-chain and infrastructure responsibility.

### Coding models / coding agents

Key controls:
- repository trust;
- dependency policy;
- sandboxing;
- secret isolation;
- human review for dependency and workflow changes;
- signed commits/releases;
- tool and package-manager restrictions.

### Multi-agent / tool-using systems

Evaluate the whole control plane:
- agent identity;
- message integrity;
- tool capability;
- delegated authority;
- memory;
- policy enforcement;
- side effects;
- auditability.

## Official reference starting points

- OpenAI open models: https://openai.com/open-models/
- Anthropic Claude docs: https://docs.anthropic.com/
- Google Gemini: https://ai.google.dev/
- Google Gemma: https://ai.google.dev/gemma
- Meta Llama: https://www.llama.com/
- Qwen: https://qwenlm.github.io/
- DeepSeek transparency/model overview: https://www.deepseek.com/en/transparency/
- Mistral docs: https://docs.mistral.ai/
- xAI docs: https://docs.x.ai/
- Moonshot/Kimi platform: https://platform.moonshot.ai/
- Zhipu/GLM ecosystem: https://open.bigmodel.cn/

## Corpus note

The community repository `togg53192-cmd/jailbreaks` includes model-specific artifacts for several of these families. LLMInjection references that repository as a community corpus but does not treat its claimed prompts or model behavior as verified findings without repeatable evaluation.
