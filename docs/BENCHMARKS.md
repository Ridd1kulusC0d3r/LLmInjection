# Benchmarks and evaluation sources

Benchmarks measure how a model, an agent or a defence behaves under a fixed set of attacks. That makes them useful for LLMInjection in two ways, and useless in a third.

| Use | Allowed |
| --- | --- |
| Design a safe test or a detection from the attack the benchmark describes | yes |
| Show that a technique is **research-demonstrated** (the maturity level in the coverage matrix) | yes |
| Show that an actor used a technique, or that a campaign happened | **never** |

The validator already rejects any ecosystem entry that claims to support attribution. A benchmark number such as "attack success rate 40%" describes the benchmark's test set, not the world.

## Added on 2026-10-09

Each project below was cloned with `git clone --depth 1`, its README read, and its last commit and licence recorded in `data/ecosystem.json`. They are all grade D (a maintainer's project, not an independent source).

| Project | Measures | Techniques | Licence | Last commit | Note |
| --- | --- | --- | --- | --- | --- |
| [InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent) | Indirect prompt injection against tool-integrated agents: 1,054 test cases, 17 user tools, 62 attacker tools | T002, T008 | MIT | 2024-07-02 | Stale: no commit for more than 540 days |
| [PurpleLlama](https://github.com/meta-llama/PurpleLlama) | CyberSecEval cybersecurity evals, plus Llama Guard, Prompt Guard, LlamaFirewall and CodeShield | T001, T002 | other (see repository) | 2026-09-29 | Mixes evals and defensive tools |
| [Inspect Evals](https://github.com/UKGovernmentBEIS/inspect_evals) | A library of evaluations on Inspect AI, including agentdojo, agentharm, cybench and cve_bench | none mapped | MIT | 2026-10-09 | A runner for other benchmarks; map individual evals when used |
| [SORRY-Bench](https://github.com/SORRY-Bench/sorry-bench) | Safety refusal behaviour, with 20 linguistic mutations of each request | T003 | MIT | 2025-03-01 | |
| [StrongREJECT](https://github.com/dsbowen/strong_reject) | Forbidden-prompt dataset and an autograder for jailbreak responses | T003 | MIT | 2025-07-07 | Successor of `alexandrasouly/strongreject`, which its README marks as deprecated |
| [CTIBench](https://github.com/xashru/cti-bench) | LLM performance on CTI tasks: CTI knowledge, CVE/CWE mapping, CVSS scoring, ATT&CK technique extraction, threat actor attribution | none mapped | CC-BY-NC | 2026-05-07 | Measures **AI for CTI**, not attacks on AI. Non-commercial licence |
| [Cybench](https://github.com/andyzorigin/cybench) | Agent capability on 40 CTF tasks from four competitions | T015 | Apache-2.0 | 2026-09-24 | A capability measure, not evidence that attackers use agents this way |
| [WildTeaming](https://github.com/allenai/wildteaming) | Mines in-the-wild user-chatbot interactions for jailbreak tactics; releases the WildJailbreak data | T003 | none found | 2024-08-10 | Research technique, not a benchmark in the strict sense |

The eight benchmarks that were already in the ecosystem (AgentDojo, BIPIA, Open-Prompt-Injection, JailbreakBench, HarmBench, ASB, PINT and PromptInject) are listed in [ECOSYSTEM.md](ECOSYSTEM.md).

## What the coverage matrix does with them

`scripts/coverage_model.py` counts, per technique, the ecosystem projects of class `benchmark` that map to it. The result is the **BENCH** column of the matrix and the "No benchmark" filter in the Explorer. A technique with no benchmark is not unsafe; it has no public yardstick yet. Today 8 of 28 techniques have one, and most supply-chain techniques have none.

## Consuming results

The repository does not copy benchmark datasets or scores. It records where a benchmark exists and which techniques it covers. To bring a result in:

1. Run the benchmark yourself, against a model or defence you are authorised to test.
2. Record the outcome in the `lab-result` shape (`schemas/lab-result.schema.json`): the `test_case` it informs, the `adapter` used, the `result` and the `timestamp`.
3. Keep the benchmark's name, version and the model tested in `observations`. A score without the model, version and date is not comparable.

## Feeds that watch these projects

`data/source-feeds.json` holds the release feeds that `scripts/intel_intake.py` reads: garak, PyRIT and AgentDojo (existing), plus PurpleLlama, Inspect Evals and promptfoo (added 2026-10-09). A new release becomes a research-queue **candidate**; nothing is promoted into the official datasets without review.

## Not yet verified

These came up while researching and could not be confirmed from the authoring environment, so they are **not** in the datasets:

- `microsoft/llmail-inject` and `CTIBench/CTIBench`: the repository URLs tried returned an authentication prompt, which for a public repository means the path is wrong, moved or removed. A maintainer who knows the current location is welcome to open an issue.
