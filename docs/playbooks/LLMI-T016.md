# LLMI-T016: AI Gateway Credential Compromise

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | supply-chain |
| Maturity | **observed in the wild** |
| Priority | 6 of 16 (maturity weight times the layers still missing) |
| Frameworks | [ASI03:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) OWASP Agentic Top 10 2026 (related), [AML.T0083](https://atlas.mitre.org/techniques/AML.T0083) ATLAS (related), [T1552](https://attack.mitre.org/techniques/T1552/) ATT&CK (related), [AML.T0098](https://atlas.mitre.org/techniques/AML.T0098) ATLAS (related), [AML.T0040](https://atlas.mitre.org/techniques/AML.T0040) ATLAS (related), [AML.T0055](https://atlas.mitre.org/techniques/AML.T0055) ATLAS (related) |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 3 record(s), 3 publisher(s), best grade A, newest 2026 |
| Safe tests | 1 |
| Detections | 0 rule file(s), 1 specification(s) |
| Controls | 1 |
| Benchmarks | 0 |

**Next step:** Turn DET-AI-006 (AI Gateway Credential Anomaly) from a specification into a rule file, starting with the telemetry listed in section 3.

## 1. Understand it

An AI gateway or proxy is compromised to access concentrated upstream model-provider credentials.

What the repository links to it:

- 2026 · [TeamPCP LiteLLM supply-chain compromise](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-TEAMPCP-LITELLM) (campaign, confirmed)
- 2024-05-06 · [LLM Jacking (AML.CS0030)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0030) (atlas-incident, high)
- 2024-12-01 · [Storm-2139 Azure OpenAI Guardrail Bypass (AML.CS0057)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0057) (atlas-incident, high)

Actors whose campaigns use it: TeamPCP. Vendor labels are kept as published and never merged without evidence.

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-GW-020 · AI Gateway Key Blast Radius

- **Goal:** Verify that a leaked gateway or provider key is scoped, monitored and revocable before it can be reused at scale.
- **Stimulus:** A lab environment issues a synthetic gateway key, then replays it from an unexpected network location and workload identity.
- **Expected:** The key is scope-limited, the anomalous use is flagged, and revocation takes effect without redeploying the gateway.
- **Telemetry to capture:** `key-id`, `source-identity`, `provider-auth-event`, `revocation-state`
- **Controls it exercises:** secret isolation, key scoping, anomaly alerting

```bash
python scripts/query_intel.py coverage LLMI-T016
python scripts/run_safe_lab.py --profile detection   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

## 3. Detect it

### DET-AI-006 · AI Gateway Credential Anomaly

- **Severity:** high
- **Hypothesis:** An AI gateway identity accesses, exports or uses provider credentials outside its normal administrative pattern.
- **Telemetry:** `secret-access`, `gateway-admin`, `cloud-audit`, `provider-auth`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

## 4. Prevent it

- **Secret Isolation** (`CTRL-SECRET-ISOLATION`): Keep model/provider credentials outside prompts and minimize which agents can access them.

## 5. Close the loop

- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.
- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.
- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.
- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.
- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.

## 6. Limits of this page

- 1 of 1 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- No benchmark maps to it, so there is no public yardstick for how well a defence performs.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Tools and projects:** [NVIDIA/garak](https://github.com/NVIDIA/garak), [Tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard), [praetorian-inc/augustus](https://github.com/praetorian-inc/augustus), [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector), [garagon/aguara](https://github.com/garagon/aguara)
- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T016)
