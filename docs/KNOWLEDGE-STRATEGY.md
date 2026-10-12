# Knowledge strategy: what we hold, what we link, what we leave out

LLMInjection holds **what is known** (evidence, techniques, graded sources) and **what to check** (safe tests, detections, controls). It has been thin on **how to do it**: a test case is a specification, and the lab runner has plan and mock adapters only. This page says how the repository closes that gap without turning into a copy of other people's work, and why it maps some third-party material and not the rest.

## Three layers of "how to"

| Layer | Where | Rule |
|---|---|---|
| **Ours, generated** | [`docs/playbooks/`](playbooks/README.md): one page per technique, built from the datasets by `scripts/build_playbooks.py` | Cannot drift from the data. States what is missing instead of hiding it. |
| **Ours, executable** | [`examples/`](../examples/): small code that turns test cases into assertions, with tests under `tests/` | Offline, standard library, no network. First one: [`agent_tool_gate.py`](../examples/agent_tool_gate.py) for `LLMI-T008`. |
| **Theirs, linked** | The AI-security skills below, and the [ecosystem map](ECOSYSTEM.md) | Link only. Nothing is copied, nothing is evidence. |

Playbook pages end with a "Go deeper" section that points at the third layer, so a defender who needs the full procedure gets there in one click and knows which parts are ours.

## Third-party AI-security skills (Tier 1)

`mukul975/anthropic-cybersecurity-skills` (Apache-2.0, an independent community project, not affiliated with Anthropic) is a catalogue of procedure-style skills. Its `ai-security` subdomain has 14 skills that read as defensive procedures for the same problems LLMInjection tracks. They are mapped by name and technique, by analyst judgement, in [`references/crosswalks/anthropic-cybersecurity-skills.json`](../references/crosswalks/anthropic-cybersecurity-skills.json), regenerated with `scripts/skills_catalog_check.py`.

<!-- gen:skills-crosswalk:start -->

| Skill (third party, link only) | Role | Our techniques | What it is for |
|---|---|---|---|
| [`continuous-llm-red-teaming-with-promptfoo`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/continuous-llm-red-teaming-with-promptfoo) | test | [LLMI-T001](playbooks/LLMI-T001.md), [LLMI-T002](playbooks/LLMI-T002.md), [LLMI-T003](playbooks/LLMI-T003.md) | red-team regression gate in CI |
| [`defending-llms-with-guardrails`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/defending-llms-with-guardrails) | defend | [LLMI-T001](playbooks/LLMI-T001.md), [LLMI-T003](playbooks/LLMI-T003.md) | runtime classifiers and rails in front of the model |
| [`detecting-ai-model-prompt-injection-attacks`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/detecting-ai-model-prompt-injection-attacks) | detect | [LLMI-T001](playbooks/LLMI-T001.md), [LLMI-T002](playbooks/LLMI-T002.md) | signature, heuristic and classifier detection of injection |
| [`implementing-llm-guardrails-for-security`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/implementing-llm-guardrails-for-security) | defend | [LLMI-T001](playbooks/LLMI-T001.md), [LLMI-T003](playbooks/LLMI-T003.md), [LLMI-T004](playbooks/LLMI-T004.md) | input and output validation, PII and schema checks |
| [`orchestrating-llm-attacks-with-pyrit`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/orchestrating-llm-attacks-with-pyrit) | test | [LLMI-T001](playbooks/LLMI-T001.md), [LLMI-T003](playbooks/LLMI-T003.md) | multi-turn adversarial testing in an authorised lab |
| [`red-teaming-llms-with-garak`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/red-teaming-llms-with-garak) | test | [LLMI-T001](playbooks/LLMI-T001.md), [LLMI-T003](playbooks/LLMI-T003.md), [LLMI-T004](playbooks/LLMI-T004.md) | probe suites and hit-rate triage |
| [`detecting-indirect-prompt-injection`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/detecting-indirect-prompt-injection) | detect | [LLMI-T002](playbooks/LLMI-T002.md), [LLMI-T017](playbooks/LLMI-T017.md), [LLMI-T025](playbooks/LLMI-T025.md) | hidden and obfuscated content in documents, pages and images |
| [`testing-prompt-injection-in-rag-pipelines`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/testing-prompt-injection-in-rag-pipelines) | test | [LLMI-T002](playbooks/LLMI-T002.md), [LLMI-T007](playbooks/LLMI-T007.md) | poisoned retrieved documents and embedding manipulation |
| [`testing-for-system-prompt-leakage`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/testing-for-system-prompt-leakage) | test | [LLMI-T004](playbooks/LLMI-T004.md) | system-prompt and embedded-secret leakage |
| [`detecting-model-extraction-attacks`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/detecting-model-extraction-attacks) | detect | [LLMI-T005](playbooks/LLMI-T005.md), [LLMI-T019](playbooks/LLMI-T019.md) | per-principal query monitoring on inference APIs |
| [`detecting-data-and-model-poisoning`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/detecting-data-and-model-poisoning) | detect | [LLMI-T006](playbooks/LLMI-T006.md) | poisoned training data and backdoored models |
| [`assessing-vector-and-embedding-weaknesses`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/assessing-vector-and-embedding-weaknesses) | assess | [LLMI-T007](playbooks/LLMI-T007.md), [LLMI-T004](playbooks/LLMI-T004.md) | vector-store isolation, embedding inversion and poisoning |
| [`securing-agentic-ai-tool-invocation`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/securing-agentic-ai-tool-invocation) | defend | [LLMI-T008](playbooks/LLMI-T008.md) | allowlist, identity binding, approval and audit at the tool boundary |
| [`auditing-mcp-servers-for-tool-poisoning`](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/auditing-mcp-servers-for-tool-poisoning) | audit | [LLMI-T021](playbooks/LLMI-T021.md), [LLMI-T011](playbooks/LLMI-T011.md) | tool poisoning, shadowing and rug pulls with an MCP scanner |

Catalogue snapshot: `mukul975/anthropic-cybersecurity-skills` at commit `54a798831d` (2026-08-31), 818 skills, Apache-2.0.

<!-- gen:skills-crosswalk:end -->

A skill is a procedure someone wrote, not an observation of a threat. It never supports a record in the evidence datasets, an attribution, or a maturity level.

## What is not mapped, and why

| Group | Count | Decision | Why |
|---|---|---|---|
| Other skills carrying ATLAS tags | 79 | Not mapped | The tags are not meaningful outside AI: a DNS-exfiltration log skill is tagged with ML supply-chain techniques. 66 of them point at our technique IDs only by accident, so a link derived from the tags would be wrong. |
| Offensive or dual-use by name (exploitation, C2, evasion, credential attacks) | 70 | **Not mapped** | They teach attack procedure for general IT, not for AI systems. Our own mapping to ATT&CK is a single technique (T1552), so there is no shared key to link on honestly. Listing them would add dual-use material with no defender value and no evidence value. |
| Everything else | the rest | Out of scope | General cybersecurity, not AI. |

**Criteria to revisit the offensive group.** Reconsider only if all of these hold: we have a real ATT&CK crosswalk for a technique, so the link is by ID and not by tag; an analyst reads the skill and records why it helps a defender test or detect that technique; and the entry stays link-only with a dual-use note. Until then the answer is no.

## Why the generated playbooks are better than copying procedures

- They are built from graded evidence, so each page says whether a technique is observed, demonstrated or only specified, and how many independent publishers say so.
- They list the gaps (no rule file, no control, one publisher, stale evidence) as part of the page. A borrowed procedure never tells you what the surrounding repository lacks.
- They are tested: `tests/test_playbooks.py` fails when a page is stale, when a test case or detection is missing from a page, or when a page makes a claim the data does not.
- Hands-on judgement goes in hand-written notes under `docs/playbooks/notes/` and in `examples/`, so the generated part stays honest and the human part stays visible.

## What still needs doing

- More worked examples: the next candidates are the techniques with the most missing defence at the top of the [playbook index](playbooks/README.md).
- Rule files for the detections that are still specifications. A playbook says so, but a rule is what a defender needs.
- Run the safe test cases against real systems and record results in the `lab-result` schema, so a playbook can say "this passed on this setup" and not only "this is what to check".
