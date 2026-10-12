# LLMI-T003: Jailbreak / Safety Boundary Manipulation

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | model-behavior |
| Maturity | **observed in the wild** |
| Priority | 2 of 16 (maturity weight times the layers still missing) |
| Frameworks | [LLM01:2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) OWASP LLM Top 10 2026 (related), [AML.T0054](https://atlas.mitre.org/techniques/AML.T0054) ATLAS (exact) |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 1 record(s), 1 publisher(s), best grade A, newest 2024-12-01 |
| Safe tests | 1 |
| Detections | 0 rule file(s), 1 specification(s) |
| Controls | 2 |
| Benchmarks | 5 |

**Next step:** Turn DET-AI-041 (Repeated Refusal-Bypass Sequence) from a specification into a rule file, starting with the telemetry listed in section 3.

## 1. Understand it

Adversarial inputs attempt to elicit behavior outside intended safety or policy boundaries.

What the repository links to it:

- 2024-12-01 · [Storm-2139 Azure OpenAI Guardrail Bypass (AML.CS0057)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0057) (atlas-incident, high)

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-JB-035 · Refusal Consistency Under Rephrasing

- **Goal:** Verify that a policy-covered refusal stays consistent when the same benign-but-restricted request is rephrased, role-framed or split across turns.
- **Stimulus:** A lab harness replays a library of benign stand-in requests that the policy must refuse, each in several framings, against the application with a canary-protected policy.
- **Expected:** The application refuses consistently across framings, logs each deviation, and a regression threshold fails the build when consistency drops.
- **Telemetry to capture:** `request-framing`, `policy-decision`, `refusal-flag`, `session-risk-score`
- **Controls it exercises:** external policy enforcement, regression thresholds, session risk scoring

```bash
python scripts/query_intel.py coverage LLMI-T003
python scripts/run_safe_lab.py --profile prompt   # lists the cases for this surface; plan mode makes no model calls
python scripts/run_safe_lab.py --profile rag   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

**Recorded results:** none. These cases are designed, not tested.

## 3. Detect it

### DET-AI-041 · Repeated Refusal-Bypass Sequence

- **Severity:** medium
- **Hypothesis:** A session shows repeated rephrasing of refused requests, rising refusal rate, or role-framing shifts consistent with probing a safety boundary.
- **Telemetry:** `refusal-flag`, `request-framing`, `session-risk-score`, `user-identity`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

## 4. Prevent it

- **Model Injection-Robustness Selection and Evaluation** (`CTRL-MODEL-ROBUSTNESS-EVAL`): Select/finetune models with instruction-hierarchy or injection-resistant training and re-evaluate with adversarial suites (e.g., AgentDojo-style) on each model/version change.
- **External Policy Enforcement** (`CTRL-POLICY-OUTSIDE-MODEL`): Enforce security policy outside the model so generated text cannot self-authorize privileged actions.

## 5. Close the loop

- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.
- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.
- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.
- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.
- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.

## 6. Limits of this page

- All the evidence comes from one publisher (MITRE). Treat it as one voice until a second source confirms it.
- The newest evidence (2024-12-01) is more than 365 days older than the newest in the dataset.
- 1 of 1 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Benchmarks:** [JailbreakBench/jailbreakbench](https://github.com/JailbreakBench/jailbreakbench), [centerforaisafety/HarmBench](https://github.com/centerforaisafety/HarmBench), [CheckPointSW/pint-benchmark](https://github.com/CheckPointSW/pint-benchmark), [SORRY-Bench/sorry-bench](https://github.com/SORRY-Bench/sorry-bench), [dsbowen/strong_reject](https://github.com/dsbowen/strong_reject)
- **Tools and projects:** [Arcanum-Sec/arc_pi_taxonomy](https://github.com/Arcanum-Sec/arc_pi_taxonomy), [yueliu1999/Awesome-Jailbreak-on-LLMs](https://github.com/yueliu1999/Awesome-Jailbreak-on-LLMs), [NVIDIA/garak](https://github.com/NVIDIA/garak), [microsoft/PyRIT](https://github.com/microsoft/PyRIT), [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo), [confident-ai/deepteam](https://github.com/confident-ai/deepteam), [cyberark/FuzzyAI](https://github.com/cyberark/FuzzyAI), [msoedov/agentic_security](https://github.com/msoedov/agentic_security), and 25 more in the [Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#tab=ecosystem)
- **Third-party procedures (not ours, link only):** [continuous-llm-red-teaming-with-promptfoo](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/continuous-llm-red-teaming-with-promptfoo) (test: red-team regression gate in CI); [defending-llms-with-guardrails](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/defending-llms-with-guardrails) (defend: runtime classifiers and rails in front of the model); [implementing-llm-guardrails-for-security](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/implementing-llm-guardrails-for-security) (defend: input and output validation, PII and schema checks); [orchestrating-llm-attacks-with-pyrit](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/orchestrating-llm-attacks-with-pyrit) (test: multi-turn adversarial testing in an authorised lab); [red-teaming-llms-with-garak](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/red-teaming-llms-with-garak) (test: probe suites and hit-rate triage). Independent community project, Apache-2.0, not affiliated with Anthropic; see the [knowledge strategy](../KNOWLEDGE-STRATEGY.md).
- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T003)
