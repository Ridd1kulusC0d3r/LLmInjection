# LLMI-T028: AI-Assisted Tooling Development

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | offensive-enablement |
| Maturity | **observed in the wild** |
| Priority | 6 of 16 (maturity weight times the layers still missing) |
| Frameworks | none mapped |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 4 record(s), 5 publisher(s), best grade A, newest 2026 |
| Safe tests | 1 |
| Detections | 0 rule file(s), 1 specification(s) |
| Controls | 1 |
| Benchmarks | 0 |

**Next step:** Turn DET-AI-045 (Rapid Iterative Script Variants on One Host) from a specification into a rule file, starting with the telemetry listed in section 3.

## 1. Understand it

Operators use LLMs to generate or iterate on reconnaissance, exploitation, credential-validation and deployment scripts or malware, compressing development time without changing the underlying attack paths.

What the repository links to it:

- 2026 · [BREEZE COMET payment-system fraud in Brazil](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-BREEZE-COMET-PAYMENTS) (campaign, confirmed)
- 2026 · [CL-CRI-1131 LLM-assisted intrusions in Mexico and Ecuador](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CL-CRI-1131) (campaign, medium)
- 2026 · [SHADOW-AETHER-040 agentic intrusions against Latin American governments](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-SHADOW-AETHER-040) (campaign, high)
- 2026 · [VoidLink AI-assisted malware engineering case](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-VOIDLINK) (observed-research-case, confirmed)

Actors whose campaigns use it: BREEZE COMET. Vendor labels are kept as published and never merged without evidence.

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-TOOL-040 · Iterative Script Trial-and-Error Detection

- **Goal:** Verify that rapid iteration of near-identical scripts on one host is detected by behavior, independent of who or what wrote them.
- **Stimulus:** A sandbox host runs a series of benign, numbered script variants in a short window, with failures followed by small corrections, from a user-writable path.
- **Expected:** The execution policy blocks unknown scripts from the user-writable path, and the iteration pattern raises an alert with the script hashes and exit codes.
- **Telemetry to capture:** `process-creation`, `script-content-hash`, `file-naming-pattern`, `exit-code`
- **Controls it exercises:** execution allowlisting, behavioral detection, script logging

```bash
python scripts/query_intel.py coverage LLMI-T028
python scripts/run_safe_lab.py --profile detection   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

**Recorded results:** none. These cases are designed, not tested.

## 3. Detect it

### DET-AI-045 · Rapid Iterative Script Variants on One Host

- **Severity:** medium
- **Hypothesis:** A host runs a series of near-identical scripts with incrementally changed names or content, failures followed by corrections, in a short window from a user-writable path. Unit 42 describes this trial-and-error pattern in the CL-CRI-1131 intrusions.
- **Telemetry:** `process-creation`, `script-content-hash`, `file-naming-pattern`, `exit-code`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

## 4. Prevent it

- **Script and Unknown Binary Execution Policy** (`CTRL-EXEC-POLICY`): Restrict execution of unsigned or unknown scripts and binaries from user-writable paths, so attacker tooling is stopped by behavior and provenance regardless of how it was written.

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

- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T028)
