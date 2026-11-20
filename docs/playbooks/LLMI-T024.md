# LLMI-T024: Exposed or Misconfigured AI Services

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | infrastructure |
| Maturity | **observed in the wild** |
| Priority | 4 of 16 (maturity weight times the layers still missing) |
| Frameworks | [AML.T0132](https://atlas.mitre.org/techniques/AML.T0132) ATLAS (exact), [AML.T0006.002](https://atlas.mitre.org/techniques/AML.T0006.002) ATLAS (related), [AML.T0006](https://atlas.mitre.org/techniques/AML.T0006) ATLAS (related), [AML.T0049](https://atlas.mitre.org/techniques/AML.T0049) ATLAS (related) |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 23 record(s), 7 publisher(s), best grade A, newest 2026 |
| Safe tests | 1 |
| Detections | 2 rule file(s), 3 specification(s) |
| Controls | 2 |
| Benchmarks | 0 |

**Next step:** No public benchmark maps to this technique. Check the ecosystem for one, or measure it with your own regression tests.

## 1. Understand it

Model-serving endpoints, agent builders, vector stores or MCP servers are reachable without adequate authentication and are scanned for and abused.

What the repository links to it:

- 2026 · [JADEPUFFER agentic database extortion](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-JADEPUFFER-AGENTIC-EXTORTION) (campaign, high)
- 2026-07 · [knaithe autonomous exploitation with DeepSeek and Hermes Agent](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-KNAITHE-HERMES-AUTONOMOUS) (campaign, confirmed)
- 2026-05-07 · [Threat Actor Uses a DeepSeek-Powered Hermes Agent in Langflow and n8n Exploitation Attempts (AML.CS0070)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0070) (atlas-incident, high)
- 2026-04-15 · [Exploitation attempts against LiteLLM's guardrail tester (CVE-2026-40217)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-LITELLM-GUARDRAIL-TESTER-EXPLOITATION) (exploitation, high)
- 2024-08-27 · [Flowise 1.8.2 authentication bypass](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-FLOWISE-CVE-2024-8181) (authentication-bypass, confirmed)
- 2025-09-22 · [Flowise CustomMCP remote code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-FLOWISE-CVE-2025-59528) (remote-code-execution, confirmed)
- 2025-08-14 · [Flowise Custom MCP OS command execution without authentication](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-FLOWISE-CVE-2025-8943) (remote-code-execution, confirmed)
- 2025-04-07 · [Langflow unauthenticated code injection in /api/v1/validate/code](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LANGFLOW-CVE-2025-3248) (code-injection, confirmed)
- 2025-12-05 · [Langflow CORS and refresh-cookie chain to account takeover and code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LANGFLOW-CVE-2025-34291) (cors-misconfiguration, confirmed)
- 2026-01-23 · [Langflow exec_globals inclusion leads to unauthenticated code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LANGFLOW-CVE-2026-0770) (code-injection, confirmed)
- 2026-03-20 · [Langflow public flow build endpoint runs attacker-supplied flow data](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LANGFLOW-CVE-2026-33017) (code-injection, confirmed)
- 2026-06-23 · [Langflow /api/v1/responses IDOR runs another user's flow](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LANGFLOW-CVE-2026-55255) (idor, confirmed)
- 2026-07-17 · [IBM Langflow OSS auto_login and validate/code chain to unauthenticated code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LANGFLOW-CVE-2026-9198) (missing-authentication, confirmed)
- 2026-04-10 · [LiteLLM guardrail tester sandbox escape to code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LITELLM-CVE-2026-40217) (sandbox-escape, confirmed)
- 2026-05-08 · [LiteLLM proxy command injection in two endpoints](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LITELLM-CVE-2026-42271) (command-injection, confirmed)
- 2025-06-13 · [MCP Inspector unauthenticated proxy remote code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-MCP-INSPECTOR-CVE-2025-49596) (remote-code-execution, confirmed)
- 2023-03-24 · [MLflow path traversal](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-MLFLOW-CVE-2023-1177) (path-traversal, confirmed)
- 2026-08-17 · [MLflow webhook test endpoint follows redirects past URL validation (SSRF)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-MLFLOW-CVE-2026-64849) (ssrf, confirmed)
- 2025-12-19 · [n8n workflow expression evaluation escapes to code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-N8N-CVE-2025-68613) (code-injection, confirmed)
- 2026-03-30 · [nginx-ui MCP integration exposed without authentication](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-NGINX-UI-CVE-2026-33032) (missing-authentication, confirmed)
- 2023-11-16 · [Ray log API local file inclusion](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-RAY-CVE-2023-6021) (path-traversal, confirmed)
- 2025-11-26 · [Ray dashboard browser-origin guard bypass to code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-RAY-CVE-2025-62593) (csrf, confirmed)
- 2026-05-26 · [Starlette Host header desynchronises request.url from the routed path (BadHost)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-STARLETTE-CVE-2026-48710) (request-smuggling, confirmed)

Actors whose campaigns use it: JADEPUFFER, knaithe. Vendor labels are kept as published and never merged without evidence.

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

**Recorded results:** none. These cases are designed, not tested.

## 3. Detect it

### DET-AI-036 · Inbound Scan of AI Service Ports

- **Severity:** medium
- **Hypothesis:** External sources probe model-serving, agent-builder or MCP endpoints, for example requesting model lists or agent flow APIs, across several hosts in a short window.
- **Telemetry:** `network-flow`, `http-request`, `service-inventory`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-053 · AI Service or Gateway Process Spawns a Shell or Network Utility

- **Severity:** critical
- **Hypothesis:** A self-hosted AI service (LiteLLM, Flowise, Langflow, MLflow, Ray, n8n, nginx-ui) or the Python/Node server hosting it (python, uvicorn, gunicorn, node) starts sh, bash, curl, wget, nc, npx or pip: post-exploitation of an exposed or vulnerable AI service. This widens the artex-detections web-service-spawns-shell rule, which lists Flowise only, to the AI infrastructure exploited in 2026 (KEV entries for LiteLLM, Langflow, MLflow, Ray, n8n).
- **Telemetry:** `EDR or auditd process creation with parent command line`, `container runtime process events`
- **Implementation:** rule file(s): [sentinel](../../detections/sentinel/det-ai-053-ai-service-spawns-shell.kql), [sigma](../../detections/sigma/det-ai-053-ai-service-spawns-shell.yml). Experimental and not run against real telemetry.

### DET-AI-055 · Malformed Host Header Reaching a Starlette or FastAPI AI Service

- **Severity:** high
- **Hypothesis:** A request to an AI service built on Starlette or FastAPI (LiteLLM, MCP servers, model APIs) carries a Host header containing /, ? or # or not matching the expected names: an attempt to desynchronise request.url from the routed path (CVE-2026-48710, BadHost) to bypass path-based authorisation.
- **Telemetry:** `reverse proxy or WAF logs with the raw Host header`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-056 · Unauthenticated or Unexpected Call to an AI Platform Admin, Test or Code Endpoint

- **Severity:** high
- **Hypothesis:** A request without an authenticated session, or outside a change window, reaches an AI platform route that runs code or reaches tools: LiteLLM /mcp-rest/test/*, /guardrails/test_custom_code and key/role changes; Flowise customMCP node load; Langflow public flow build, /api/v1/validate/code, /api/v1/auto_login and /api/v1/responses; nginx-ui /mcp_message and /api/backup. These are the routes behind the 2026 KEV entries for these products.
- **Telemetry:** `reverse proxy or WAF logs`, `AI gateway audit log`
- **Implementation:** rule file(s): [sigma](../../detections/sigma/det-ai-056-ai-platform-sensitive-endpoint.yml). Experimental and not run against real telemetry.

### DET-AI-057 · MLflow Webhook Test Followed by Egress to Metadata or Internal Address

- **Severity:** critical
- **Hypothesis:** An MLflow webhook test call is followed within seconds by an outbound connection from the MLflow host to 169.254.169.254, an equivalent metadata address or an internal range: server-side request forgery through redirect following (CVE-2026-64849).
- **Telemetry:** `MLflow server logs`, `host or VPC flow logs`, `cloud audit logs for instance credential use`
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

- 3 of 5 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- No benchmark maps to it, so there is no public yardstick for how well a defence performs.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Tools and projects:** [TiaMEOWS/mcp-sentinel](https://github.com/TiaMEOWS/mcp-sentinel), [BerkantACUN/guardmcp](https://github.com/BerkantACUN/guardmcp)
- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T024)
