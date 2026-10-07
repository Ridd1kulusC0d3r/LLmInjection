# Benchmarks, Evaluation & Research Tools

This index focuses on reproducible **security evaluation**. A verified comparison of 12 benchmarks (suites, metrics, last commit, techniques) is in the [ecosystem intelligence sweep](ECOSYSTEM-INTELLIGENCE.md#7-benchmarks). Inclusion is not an endorsement and does not imply that a tool covers the full AI threat model.

## LLM / GenAI security evaluation

### JailbreakBench
Open robustness benchmark for jailbreaking language models, including behaviors, attacks, defenses and judges.

- Repository: https://github.com/JailbreakBench/jailbreakbench
- Use in LLMInjection: benchmark metadata, defense comparison, robustness research.

### NVIDIA garak
Generative AI red-teaming and assessment toolkit covering prompt injection, data leakage, jailbreaks and other failure modes.

- Repository: https://github.com/NVIDIA/garak
- Use in LLMInjection: repeatable defensive evaluation and regression testing.

### Microsoft PyRIT
Python Risk Identification Tool for generative AI red teaming.

- Repository: https://github.com/Azure/PyRIT
- Use in LLMInjection: orchestration of authorized red-team evaluations, result capture and test repeatability.

## Adversarial ML / NLP

### Adversarial Robustness Toolbox (ART)
LF AI & Data project for evaluating and defending ML systems against evasion, poisoning, extraction and inference attacks.

- Repository: https://github.com/Trusted-AI/adversarial-robustness-toolbox

### TextAttack
Framework for adversarial attacks, data augmentation and model training in NLP.

- Repository: https://github.com/QData/TextAttack

## Academic attack research

### LLM Attacks / GCG
Official research repository for *Universal and Transferable Adversarial Attacks on Aligned Language Models*.

- Repository: https://github.com/llm-attacks/llm-attacks

LLMInjection indexes the research and evaluation context; it does not mirror operational jailbreak strings into the core threat-intelligence dataset.

## What to measure

A useful security benchmark should report more than "attack succeeded".

Recommended dimensions:

- attack success rate;
- false-positive / false-refusal rate;
- task utility after defense;
- model/version;
- system prompt/application version;
- tool/RAG availability;
- attack budget / attempts;
- deterministic vs stochastic settings;
- evaluator/judge model;
- reproducibility seed/config;
- latency and cost impact;
- defense bypass rate over time.

## Regression testing

Security evaluation should be versioned like software testing.

A model/application release should record:

```text
model + system policy + tools + RAG corpus + gateway policy
                    ↓
              security suite
                    ↓
     results + deltas + failed controls
```

A benchmark result without the surrounding system configuration is often impossible to interpret later.
