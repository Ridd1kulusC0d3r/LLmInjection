# LLMI-T010: Model Source Tampering

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | supply-chain |
| Maturity | **observed in the wild** |
| Priority | 6 of 16 (maturity weight times the layers still missing) |
| Frameworks | [LLM04:2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) OWASP LLM Top 10 2026 (related), [AML.T0010.003](https://atlas.mitre.org/techniques/AML.T0010.003) ATLAS (exact), [AML.T0115.001](https://atlas.mitre.org/techniques/AML.T0115.001) ATLAS (related), [AML.T0011.000](https://atlas.mitre.org/techniques/AML.T0011.000) ATLAS (related), [AML.T0076](https://atlas.mitre.org/techniques/AML.T0076) ATLAS (related) |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 1 record(s), 1 publisher(s), best grade A, newest 2025-02-25 |
| Safe tests | 1 |
| Detections | 0 rule file(s), 3 specification(s) |
| Controls | 2 |
| Benchmarks | 0 |

**Next step:** Turn DET-AI-022 (Unsafe Deserialization Import in Model Artifact) from a specification into a rule file, starting with the telemetry listed in section 3.

## 1. Understand it

Model code, weights or serving artifacts are replaced or modified without authorization.

What the repository links to it:

- 2025-02-25 · [Malicious Models on Hugging Face (AML.CS0031)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0031) (atlas-incident, high)

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-SC-009 · Model Artifact Provenance Drift

- **Goal:** Verify detection when a model artifact digest differs from the approved manifest.
- **Stimulus:** A test manifest is changed to reference a mismatched synthetic digest.
- **Expected:** Promotion/deployment is blocked and the provenance mismatch is recorded.
- **Telemetry to capture:** `artifact-digest`, `expected-digest`, `publisher`, `deployment-gate`
- **Controls it exercises:** digest pinning, signatures, trusted registries

```bash
python scripts/query_intel.py coverage LLMI-T010
python scripts/run_safe_lab.py --profile supply-chain   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

## 3. Detect it

### DET-AI-005 · Model Artifact Provenance Drift

- **Severity:** high
- **Hypothesis:** A model or serving artifact digest differs from the approved manifest or trusted publisher record.
- **Telemetry:** `artifact-digest`, `registry-event`, `deployment-gate`, `publisher`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-022 · Unsafe Deserialization Import in Model Artifact

- **Severity:** critical
- **Hypothesis:** A model artifact whose pickle stream or Keras/TF graph references process, network or code-execution globals or file-I/O ops indicates a weaponised model file that executes on load.
- **Telemetry:** `model file hash and format`, `pickle opcode GLOBAL/STACK_GLOBAL module.name list`, `Keras Lambda layer presence`, `TF SavedModel op list (ReadFile/WriteFile)`, `model registry download events`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-023 · Model Load Followed by Unexpected Child Process or Egress

- **Severity:** high
- **Hypothesis:** A training or inference process that spawns a shell or opens a new outbound connection within seconds of loading a model file indicates load-time code execution from a malicious artifact.
- **Telemetry:** `file open events on model extensions (.pt, .pth, .bin, .ckpt, .pkl, .joblib, .h5, .keras)`, `process creation with parent = python/ML runtime`, `network connections from ML runtime`, `model file hash`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

## 4. Prevent it

- **Artifact Digest Pinning** (`CTRL-ARTIFACT-PINNING`): Pin model, package and deployment artifacts to approved immutable digests.
- **Artifact Signature Verification** (`CTRL-SIGNATURE-VERIFICATION`): Verify trusted publisher identity and artifact integrity before promotion or execution.

## 5. Close the loop

- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.
- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.
- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.
- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.
- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.

## 6. Limits of this page

- All the evidence comes from one publisher (MITRE). Treat it as one voice until a second source confirms it.
- The newest evidence (2025-02-25) is more than 365 days older than the newest in the dataset.
- 3 of 3 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- No benchmark maps to it, so there is no public yardstick for how well a defence performs.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Tools and projects:** [Tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard), [protectai/modelscan](https://github.com/protectai/modelscan), [perplext/LLMrecon](https://github.com/perplext/LLMrecon)
- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T010)
