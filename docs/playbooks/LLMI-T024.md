# LLMI-T024: Exposed or Misconfigured AI Services

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | infrastructure |
| Maturity | **observed in the wild** |
| Priority | 6 of 16 (maturity weight times the layers still missing) |
| Frameworks | [AML.T0132](https://atlas.mitre.org/techniques/AML.T0132) ATLAS (exact), [AML.T0006.002](https://atlas.mitre.org/techniques/AML.T0006.002) ATLAS (related), [AML.T0006](https://atlas.mitre.org/techniques/AML.T0006) ATLAS (related), [AML.T0049](https://atlas.mitre.org/techniques/AML.T0049) ATLAS (related) |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 1 record(s), 1 publisher(s), best grade A, newest 2026-05-07 |
| Safe tests | 1 |
| Detections | 0 rule file(s), 1 specification(s) |
| Controls | 2 |
| Benchmarks | 0 |

**Next step:** Turn DET-AI-036 (Inbound Scan of AI Service Ports) from a specification into a rule file, starting with the telemetry listed in section 3.

## 1. Understand it

Model-serving endpoints, agent builders, vector stores or MCP servers are reachable without adequate authentication and are scanned for and abused.

What the repository links to it:

- 2026-05-07 · [Threat Actor Uses a DeepSeek-Powered Hermes Agent in Langflow and n8n Exploitation Attempts (AML.CS0070)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0070) (atlas-incident, high)

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-EXP-034 · Unauthenticated AI Endpoint Discovery

- **Goal:** Verify that model servers, agent builders and MCP endpoints in the lab perimeter require authentication and that scans against them are detected.
- **Stimulus:** A lab scanner enumerates common model-serving and agent-builder ports and requests the model list with header X-LLMI-Probe: LLMI_EXPOSE_034.
- **Expected:** Every endpoint rejects unauthenticated requests and the probe is alerted on with the marker header recorded.
- **Telemetry to capture:** `network-flow`, `http-request`, `service-inventory`, `auth-decision`
- **Controls it exercises:** CTRL-AI-SERVICE-EXPOSURE, CTRL-AI-INVENTORY

```bash
python scripts/query_intel.py coverage LLMI-T024
python scripts/run_safe_lab.py --profile detection   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

## 3. Detect it

### DET-AI-036 · Inbound Scan of AI Service Ports

- **Severity:** medium
- **Hypothesis:** External sources probe model-serving, agent-builder or MCP endpoints, for example requesting model lists or agent flow APIs, across several hosts in a short window.
- **Telemetry:** `network-flow`, `http-request`, `service-inventory`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

## 4. Prevent it

- **AI Asset and Service Inventory** (`CTRL-AI-INVENTORY`): Maintain inventory of models, runtimes, agents, gateways, MCP servers and external providers.
- **AI Service Exposure Management** (`CTRL-AI-SERVICE-EXPOSURE`): Inventory model servers, agent builders, vector stores and MCP endpoints, require authentication on every one and scan the external perimeter for them.

## 5. Close the loop

- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.
- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.
- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.
- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.
- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.

## 6. Limits of this page

- All the evidence comes from one publisher (MITRE). Treat it as one voice until a second source confirms it.
- 1 of 1 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- No benchmark maps to it, so there is no public yardstick for how well a defence performs.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T024)
