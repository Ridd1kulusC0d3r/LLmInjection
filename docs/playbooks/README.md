# Defender playbooks

One page per technique, generated from the datasets, in the order a defender works: understand it, test it, detect it, prevent it, close the loop, know the limits. Each page says what exists and what does not, and ends with where to go for the hands-on detail. Read the [knowledge strategy](../KNOWLEDGE-STRATEGY.md) for how this fits with the rest of the repository.

Sorted by priority, the techniques with the most missing defence first. `E` evidence records, `T` safe tests, `R` rule files, `S` specifications, `C` controls, `B` benchmarks.

| Technique | Maturity | Priority | E | T | R | S | C | B |
|---|---|---|---|---|---|---|---|---|
| [LLMI-T005](LLMI-T005.md) Model Extraction / Theft | observed in the wild | 10 | 1 | 1 | 0 | 2 | 0 | 0 |
| [LLMI-T013](LLMI-T013.md) Runtime LLM Command Generation | observed in the wild | 8 | 2 | 1 | 1 | 0 | 0 | 0 |
| [LLMI-T010](LLMI-T010.md) Model Source Tampering | observed in the wild | 6 | 1 | 1 | 0 | 3 | 2 | 0 |
| [LLMI-T012](LLMI-T012.md) Coding-Agent Dependency Manipulation | observed in the wild | 6 | 1 | 2 | 0 | 2 | 1 | 0 |
| [LLMI-T014](LLMI-T014.md) AI-Assisted Reconnaissance and Social Engineering | observed in the wild | 6 | 2 | 1 | 0 | 1 | 1 | 0 |
| [LLMI-T016](LLMI-T016.md) AI Gateway Credential Compromise | observed in the wild | 6 | 3 | 1 | 0 | 1 | 1 | 0 |
| [LLMI-T017](LLMI-T017.md) Prompt Injection Against AI Security Scanners | observed in the wild | 6 | 2 | 1 | 0 | 2 | 2 | 0 |
| [LLMI-T019](LLMI-T019.md) Model Distillation Campaign | observed in the wild | 6 | 2 | 1 | 0 | 1 | 1 | 0 |
| [LLMI-T021](LLMI-T021.md) Agent Tool Poisoning and Rug Pull | observed in the wild | 6 | 2 | 1 | 0 | 2 | 3 | 0 |
| [LLMI-T023](LLMI-T023.md) Crafted AI Assistant Links and Recommendation Poisoning | observed in the wild | 6 | 1 | 1 | 0 | 1 | 2 | 0 |
| [LLMI-T024](LLMI-T024.md) Exposed or Misconfigured AI Services | observed in the wild | 6 | 1 | 1 | 0 | 1 | 2 | 0 |
| [LLMI-T026](LLMI-T026.md) Inter-Agent Instruction Propagation | observed in the wild | 6 | 2 | 1 | 0 | 1 | 3 | 0 |
| [LLMI-T028](LLMI-T028.md) AI-Assisted Tooling Development | observed in the wild | 6 | 4 | 1 | 0 | 1 | 1 | 0 |
| [LLMI-T007](LLMI-T007.md) RAG Knowledge Poisoning | demonstrated in research | 5 | 1 | 1 | 0 | 1 | 0 | 0 |
| [LLMI-T011](LLMI-T011.md) AI Software Supply Chain Compromise | observed in the wild | 4 | 6 | 2 | 1 | 4 | 1 | 0 |
| [LLMI-T018](LLMI-T018.md) AI Coding-Assistant Workspace Abuse | observed in the wild | 4 | 2 | 1 | 1 | 5 | 2 | 0 |
| [LLMI-T006](LLMI-T006.md) Data or Model Poisoning | demonstrated in research | 3 | 0 | 1 | 0 | 1 | 0 | 1 |
| [LLMI-T020](LLMI-T020.md) Improper Output Handling and Rendering Exfiltration | demonstrated in research | 3 | 2 | 3 | 0 | 2 | 3 | 0 |
| [LLMI-T025](LLMI-T025.md) Multimodal Instruction Triggers | demonstrated in research | 3 | 0 | 2 | 0 | 1 | 2 | 0 |
| [LLMI-T003](LLMI-T003.md) Jailbreak / Safety Boundary Manipulation | observed in the wild | 2 | 1 | 1 | 0 | 1 | 2 | 5 |
| [LLMI-T008](LLMI-T008.md) Agent Tool Misuse | observed in the wild | 2 | 8 | 6 | 0 | 3 | 2 | 3 |
| [LLMI-T022](LLMI-T022.md) Agentic Resource Consumption and Cost Harvesting | no linked evidence yet | 1.5 | 0 | 2 | 0 | 2 | 1 | 0 |
| [LLMI-T001](LLMI-T001.md) Direct Prompt Injection | demonstrated in research | 1 | 0 | 2 | 0 | 2 | 2 | 6 |
| [LLMI-T002](LLMI-T002.md) Indirect Prompt Injection | demonstrated in research | 1 | 4 | 1 | 0 | 2 | 3 | 6 |
| [LLMI-T004](LLMI-T004.md) Sensitive Information Disclosure | demonstrated in research | 1 | 1 | 2 | 0 | 1 | 1 | 3 |
| [LLMI-T009](LLMI-T009.md) Memory / Context Poisoning | demonstrated in research | 1 | 2 | 1 | 0 | 2 | 1 | 1 |
| [LLMI-T027](LLMI-T027.md) Unsanctioned AI Runtime (Shadow AI) | no linked evidence yet | 1 | 0 | 2 | 2 | 0 | 2 | 0 |
| [LLMI-T015](LLMI-T015.md) Agentic Attack Orchestration | observed in the wild | 0 | 7 | 1 | 1 | 1 | 2 | 1 |

Pages with a worked example or hand-written notes: [LLMI-T008](LLMI-T008.md).
