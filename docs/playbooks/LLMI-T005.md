# LLMI-T005: Model Extraction / Theft

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | model |
| Maturity | **observed in the wild** |
| Priority | 10 of 16 (maturity weight times the layers still missing) |
| Frameworks | [AML.T0044](https://atlas.mitre.org/techniques/AML.T0044) ATLAS (related) |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 1 record(s), 1 publisher(s), best grade A, newest 2026 |
| Safe tests | 1 |
| Detections | 0 rule file(s), 2 specification(s) |
| Controls | 0 |
| Benchmarks | 0 |

**Next step:** Turn DET-AI-026 (Systematic Decision-Boundary Probing via Inference API) from a specification into a rule file, starting with the telemetry listed in section 3.

## 1. Understand it

Adversary attempts to recover model behavior, intellectual property or weights.

What the repository links to it:

- 2026 · [Model distillation campaigns against Google models](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-GTIG-DISTILLATION) (model-extraction, confirmed)

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-DIST-018 · Systematic Prompt Harvest Alert

- **Goal:** Verify that high-volume, templated prompting against a model endpoint is detected and rate-limited.
- **Stimulus:** A lab client sends a synthetic, templated prompt sweep to a mock endpoint at a rate well above the account baseline, across several linked test accounts.
- **Expected:** The abuse monitor raises an alert, throttles the accounts, and records the account linkage and template similarity.
- **Telemetry to capture:** `request-rate`, `prompt-template-similarity`, `account-linkage`, `throttle-decision`
- **Controls it exercises:** rate and budget limits, abuse monitoring, account linkage review

```bash
python scripts/query_intel.py coverage LLMI-T005
python scripts/run_safe_lab.py --profile prompt   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

## 3. Detect it

### DET-AI-013 · Systematic Prompt Harvesting Pattern

- **Severity:** medium
- **Hypothesis:** Linked accounts send templated, high-volume prompts that cover a model's capability space far beyond the baseline for that account class.
- **Telemetry:** `api-request-log`, `account-linkage`, `prompt-template-similarity`, `request-rate`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-026 · Systematic Decision-Boundary Probing via Inference API

- **Severity:** critical
- **Hypothesis:** If an identity issues high volumes of near-duplicate prompts varying a single attribute or requesting confidence scores, it is likely attempting model extraction.
- **Telemetry:** `inference-api-request-log`, `requested-logprobs-or-parameters`, `per-identity-query-cadence`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

## 4. Prevent it

No control is linked yet.

## 5. Close the loop

- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.
- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.
- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.
- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.
- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.

## 6. Limits of this page

- All the evidence comes from one publisher (Google Threat Intelligence Group). Treat it as one voice until a second source confirms it.
- 2 of 2 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- No control is linked to this technique yet.
- No benchmark maps to it, so there is no public yardstick for how well a defence performs.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Tools and projects:** [NVIDIA/garak](https://github.com/NVIDIA/garak), [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo), [regaan/basilisk](https://github.com/regaan/basilisk), [perplext/LLMrecon](https://github.com/perplext/LLMrecon), [mukul975/anthropic-cybersecurity-skills](https://github.com/mukul975/anthropic-cybersecurity-skills)
- **Third-party procedures (not ours, link only):** [detecting-model-extraction-attacks](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/detecting-model-extraction-attacks) (detect: per-principal query monitoring on inference APIs). Independent community project, Apache-2.0, not affiliated with Anthropic; see the [knowledge strategy](../KNOWLEDGE-STRATEGY.md).
- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T005)
