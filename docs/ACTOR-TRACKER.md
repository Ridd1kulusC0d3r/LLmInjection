# AI / LLM Threat Actor Tracker

Last reviewed: **2026-09-30**

This page summarizes public reporting where AI materially intersects with real-world threat activity. It does not assume that every actor using an LLM has suddenly become "AI-native".

## Tracker

| Actor / cluster | Nexus | AI role | Publicly reported behavior | Confidence |
|---|---|---|---|---|
| GTG-1002 | China | AI as autonomous operator | Anthropic assessed with high confidence that a Chinese state-sponsored group used Claude Code to conduct a largely AI-orchestrated espionage campaign against ~30 targets; AI executed 80–90% of tactical operations | confirmed |
| APT28 / FROZENLAKE | Russia | AI as runtime enabler | GTIG reported PROMPTSTEAL (CERT-UA: LAMEHUG) querying Qwen2.5-Coder-32B-Instruct via Hugging Face to generate commands during live operations | confirmed |
| APT42 | Iran | AI as offensive enabler | GTIG observed Gemini use for reconnaissance, target research, phishing content and localization | confirmed |
| UNC2970 | North Korea nexus | AI as offensive enabler | GTIG reported Gemini use to synthesize OSINT and profile high-value targets | confirmed |
| Kimsuky | North Korea | AI as local analysis/enabler | Genians reported Ollama, GPT4All, Msty and RAG-related artifacts in infrastructure linked to Kimsuky; reporting describes this as capability accumulation/integration | high |
| Famous Chollima / PromptMink | North Korea | AI supply-chain / coding-agent targeting | 2026 reporting describes malicious npm packages optimized to influence AI coding-agent dependency selection; CSA summarizes ReversingLabs' attribution to Famous Chollima | high |
| TeamPCP | Unattributed / criminal reporting | AI infrastructure as target | 2026 campaign compromised software supply-chain components and resulted in malicious LiteLLM releases, exposing the strategic value of AI gateways and CI secrets | confirmed |

## From actor intelligence to defensive tests

The actor tracker is not meant to end at attribution. Where the public behavior translates cleanly into a defensive hypothesis, LLMInjection links it to a safe lab case.

| Intelligence example | Defensive question | Related safe test |
|---|---|---|
| GTG-1002 / AI-orchestrated campaign | Where must an autonomous workflow stop and return control to policy or a human? | [TC-AUTO-015](TEST-CASES.md#tc-auto-015--autonomous-multi-step-chain-gate), [TC-AG-006](TEST-CASES.md#tc-ag-006--high-impact-action-confirmation) |
| APT28 / runtime LLM command generation | Can defenders identify AI-provider traffic from workloads that should not use AI? | [TC-NET-012](TEST-CASES.md#tc-net-012--unexpected-llm-provider-egress) |
| Kimsuky / local LLM stack reporting | Can unauthorized local model runtimes and unexpected RAG artifacts be inventoried? | [TC-RUN-011](TEST-CASES.md#tc-run-011--unauthorized-local-llm-runtime), [TC-RAG-004](TEST-CASES.md#tc-rag-004--rag-provenance-conflict) |
| Famous Chollima / PromptMink reporting | Can coding agents recommend or install dependencies without package provenance controls? | [TC-SC-008](TEST-CASES.md#tc-sc-008--coding-agent-dependency-manipulation) |
| TeamPCP / LiteLLM supply-chain compromise | Will provenance drift block a modified AI component before trusted deployment? | [TC-SC-009](TEST-CASES.md#tc-sc-009--model-artifact-provenance-drift) |

Not every observed use of AI maps to a prompt-injection test. APT42 and UNC2970, for example, are primarily useful here as evidence of **AI as an offensive enabler** for reconnaissance and target research, not as proof of a new vulnerability class.

---

## Important corrections and caveats

### Famous Chollima is not automatically APT37

Some secondary reporting collapses Famous Chollima, Lazarus-lineage names and APT37/Reaper into one alias set. LLMInjection does **not** do that without a source explicitly establishing the equivalence.

### "AI-generated malware" requires evidence

A codebase containing stylistic artifacts associated with LLM output is not the same as proving end-to-end AI authorship. Keep the source's exact confidence and wording.

### TeamPCP is an AI-security case, not necessarily an AI-native actor

The relevance is the compromise of AI supply-chain infrastructure (including LiteLLM), not evidence that the actor itself depends on LLMs.

## Primary / strong sources

### GTG-1002
- Anthropic, *Disrupting the first reported AI-orchestrated cyber espionage campaign*, 2025-11-13  
  https://www.anthropic.com/news/disrupting-AI-espionage
- Anthropic, *Mapping AI-enabled cyber threats*, 2026  
  https://www.anthropic.com/research/attack-navigator

### APT28 / PROMPTSTEAL / LAMEHUG
- Google Threat Intelligence Group, *GTIG AI Threat Tracker: Advances in Threat Actor Usage of AI Tools*  
  https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools

### APT42 and UNC2970
- Google Threat Intelligence Group, *Adversarial Misuse of Generative AI*  
  https://cloud.google.com/blog/topics/threat-intelligence/adversarial-misuse-generative-ai
- GTIG, *Distillation, Experimentation, and (Continued) Integration of AI for Adversarial Use*  
  https://cloud.google.com/blog/topics/threat-intelligence/distillation-experimentation-integration-ai-adversarial-use

### Kimsuky
- Genians Security Center, *Kimsuky Integrates AI into Attack Operations, From AI-Generated Decoy Documents to a Local LLM*, 2026-08-10  
  https://www.genians.co.kr/blog/threat_intelligence/kimsuky_ai_llm
- Reuters coverage notes the Genians findings had not been independently verified.

### PromptMink
- Cloud Security Alliance research note, *PromptMink: AI-Optimized DPRK Supply Chain Attack*, 2026  
  https://labs.cloudsecurityalliance.org/research/csa-research-note-promptmink-dprk-ai-generated-supply-chain/

### TeamPCP / LiteLLM
- Endor Labs, *TeamPCP Isn't Done... LiteLLM*, 2026-03-24  
  https://www.endorlabs.com/learn/teampcp-isnt-done
- Wiz, *TeamPCP trojanizes LiteLLM*, 2026-03-24  
  https://www.wiz.io/blog/threes-a-crowd-teampcp-trojanizes-litellm-in-continuation-of-campaign

## Research queue

The following claims should remain outside the confirmed tracker until primary-source validation is attached:

- GTG-20006 / APT29 "detect-rewrite-reexecute" loop;
- exact attribution/alias chains that collapse unrelated DPRK tracking names;
- precise victim/download/exfiltration counts repeated only by secondary sources;
- CL-CRI-1163 AI-use claims without a strong primary report.

The point is not to be timid. It is to keep the dataset usable by analysts who expect evidence.
