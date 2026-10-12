# LLMI-T006: Data or Model Poisoning

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | training-data |
| Maturity | **demonstrated in research** |
| Priority | 3 of 16 (maturity weight times the layers still missing) |
| Frameworks | [LLM05:2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) OWASP LLM Top 10 2026 (exact), [AML.T0020](https://atlas.mitre.org/techniques/AML.T0020) ATLAS (exact), [AML.T0018](https://atlas.mitre.org/techniques/AML.T0018) ATLAS (related), [AML.T0115.000](https://atlas.mitre.org/techniques/AML.T0115.000) ATLAS (related), [AML.T0059](https://atlas.mitre.org/techniques/AML.T0059) ATLAS (related), [AML.T0018.000](https://atlas.mitre.org/techniques/AML.T0018.000) ATLAS (related) |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 0 record(s), 0 publisher(s), best grade n/a, newest undated |
| Safe tests | 1 |
| Detections | 0 rule file(s), 1 specification(s) |
| Controls | 0 |
| Benchmarks | 1 |

**Next step:** Turn DET-AI-042 (Training Data Provenance Drift) from a specification into a rule file, starting with the telemetry listed in section 3.

## 1. Understand it

Adversarial changes to data or model artifacts influence future behavior.

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-POI-036 · Training Data Poisoning Canary

- **Goal:** Verify that a poisoned or tampered sample in a fine-tuning or retrieval-training set is detected before it changes model behavior.
- **Stimulus:** A synthetic dataset includes a small set of canary samples with a harmless trigger-and-response pair, submitted through the normal data intake path.
- **Expected:** Provenance checks flag the unreviewed contributor, the canary behavior does not appear in the evaluated model, and the dataset digest change is recorded.
- **Telemetry to capture:** `dataset-digest`, `contributor-identity`, `canary-hit-rate`, `evaluation-delta`
- **Controls it exercises:** dataset provenance, contributor review, canary evaluation

```bash
python scripts/query_intel.py coverage LLMI-T006
python scripts/run_safe_lab.py --profile supply-chain   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

## 3. Detect it

### DET-AI-042 · Training Data Provenance Drift

- **Severity:** high
- **Hypothesis:** A fine-tuning or retrieval-training dataset changes digest, contributor or source mix without an approved review event.
- **Telemetry:** `dataset-digest`, `contributor-identity`, `source-mix`, `review-state`
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

- No incident, campaign or vulnerability in this repository is linked to this technique. That is a gap here, not proof that it has not happened.
- 1 of 1 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- No control is linked to this technique yet.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Benchmarks:** [agiresearch/ASB](https://github.com/agiresearch/ASB)
- **Tools and projects:** [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo), [Tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard), [AI-secure/AgentPoison](https://github.com/AI-secure/AgentPoison), [perplext/LLMrecon](https://github.com/perplext/LLMrecon), [mukul975/anthropic-cybersecurity-skills](https://github.com/mukul975/anthropic-cybersecurity-skills)
- **Third-party procedures (not ours, link only):** [detecting-data-and-model-poisoning](https://github.com/mukul975/anthropic-cybersecurity-skills/tree/main/skills/detecting-data-and-model-poisoning) (detect: poisoned training data and backdoored models). Independent community project, Apache-2.0, not affiliated with Anthropic; see the [knowledge strategy](../KNOWLEDGE-STRATEGY.md).
- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T006)
