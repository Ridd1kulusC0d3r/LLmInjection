# LLMI-T027: Unsanctioned AI Runtime (Shadow AI)

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | runtime-security |
| Maturity | **no linked evidence yet** |
| Priority | 1 of 16 (maturity weight times the layers still missing) |
| Frameworks | none mapped |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 0 record(s), 0 publisher(s), best grade n/a, newest undated |
| Safe tests | 2 |
| Detections | 2 rule file(s), 0 specification(s) |
| Controls | 2 |
| Benchmarks | 0 |

**Next step:** No public benchmark maps to this technique. Check the ecosystem for one, or measure it with your own regression tests.

## 1. Understand it

AI runtimes, local models or provider endpoints are used outside the approved inventory, hiding data flows and capability from security teams.

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-NET-012 · Unexpected LLM Provider Egress

- **Goal:** Verify detection of AI-provider traffic from a workload with no approved AI dependency.
- **Stimulus:** Synthetic proxy logs show a test service contacting an AI provider endpoint for the first time.
- **Expected:** The event is correlated with workload identity and compared against the approved dependency inventory.
- **Telemetry to capture:** `destination`, `workload-identity`, `first-seen`, `request-volume`
- **Controls it exercises:** egress policy, AI service inventory, network monitoring

### TC-RUN-011 · Unauthorized Local LLM Runtime

- **Goal:** Verify visibility when a local model runtime appears on a non-AI endpoint.
- **Stimulus:** Synthetic endpoint telemetry reports a local LLM process, model file and listening socket on a test host.
- **Expected:** The detection pipeline raises an inventory/policy event and enriches it with process and owner context.
- **Telemetry to capture:** `process`, `model-file`, `listening-port`, `host-owner`
- **Controls it exercises:** software inventory, EDR visibility, approved-runtime policy

```bash
python scripts/query_intel.py coverage LLMI-T027
python scripts/run_safe_lab.py --profile detection   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

**Recorded results:** none. These cases are designed, not tested.

## 3. Detect it

### DET-AI-001 · Unexpected LLM Provider Egress

- **Severity:** medium
- **Hypothesis:** A workload with no approved AI dependency contacts an LLM provider or AI gateway.
- **Telemetry:** `dns`, `proxy`, `network-flow`, `workload-identity`
- **Implementation:** rule file(s): [sentinel](../../detections/sentinel/det-ai-001-unexpected-llm-egress.kql), [splunk](../../detections/splunk/det-ai-001-unexpected-llm-egress.spl). Experimental and not run against real telemetry.

### DET-AI-002 · Unauthorized Local LLM Runtime

- **Severity:** medium
- **Hypothesis:** A local LLM runtime or model-serving process appears on a host outside the approved AI inventory.
- **Telemetry:** `process`, `listening-port`, `file`, `host-inventory`
- **Implementation:** rule file(s): [elastic](../../detections/elastic/det-ai-002-local-llm-runtime.esql), [google-secops](../../detections/google-secops/det-ai-002-local-llm-runtime.yaral), [sigma](../../detections/sigma/det-ai-002-local-llm-runtime.yml). Experimental and not run against real telemetry.

## 4. Prevent it

- **AI Asset and Service Inventory** (`CTRL-AI-INVENTORY`): Maintain inventory of models, runtimes, agents, gateways, MCP servers and external providers.
- **AI Egress Policy** (`CTRL-EGRESS-POLICY`): Restrict and monitor network access to model providers and AI gateways by workload identity.

## 5. Close the loop

- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.
- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.
- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.
- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.
- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.

## 6. Limits of this page

- No incident, campaign or vulnerability in this repository is linked to this technique. That is a gap here, not proof that it has not happened.
- No benchmark maps to it, so there is no public yardstick for how well a defence performs.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T027)
