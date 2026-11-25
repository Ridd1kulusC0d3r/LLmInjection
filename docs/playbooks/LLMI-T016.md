# LLMI-T016: AI Gateway Credential Compromise

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | supply-chain |
| Maturity | **observed in the wild** |
| Priority | 4 of 16 (maturity weight times the layers still missing) |
| Frameworks | [ASI03:2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) OWASP Agentic Top 10 2026 (related), [AML.T0083](https://atlas.mitre.org/techniques/AML.T0083) ATLAS (related), [T1552](https://attack.mitre.org/techniques/T1552/) ATT&CK (related), [AML.T0098](https://atlas.mitre.org/techniques/AML.T0098) ATLAS (related), [AML.T0040](https://atlas.mitre.org/techniques/AML.T0040) ATLAS (related), [AML.T0055](https://atlas.mitre.org/techniques/AML.T0055) ATLAS (related) |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 14 record(s), 13 publisher(s), best grade A, newest 2026 |
| Safe tests | 1 |
| Detections | 4 rule file(s), 1 specification(s) |
| Controls | 1 |
| Benchmarks | 0 |

**Next step:** No public benchmark maps to this technique. Check the ecosystem for one, or measure it with your own regression tests.

## 1. Understand it

An AI gateway or proxy is compromised to access concentrated upstream model-provider credentials.

What the repository links to it:

- 2026-11 · [ARTEX-driven search and abuse of secrets exposed on GitHub](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-EXPOSED-SECRETS) (campaign, high)
- 2026-11 · [ARTEX-Harvester: opportunistic agentic intrusions through residential proxies (Wiz)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-HARVESTER) (campaign, medium)
- 2026-11 · [ARTEX agents stealing AI model credentials at industrial scale (seen through Amazon MadPot)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-MADPOT-AI-CREDENTIAL-THEFT) (campaign, medium)
- 2026-09 · [Carbonato Docker botnet deploying Hermes Agent to hunt AI API keys](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CARBONATO-DOCKER-HERMES) (campaign, high)
- 2026 · [TeamPCP LiteLLM supply-chain compromise](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-TEAMPCP-LITELLM) (campaign, confirmed)
- 2024-05-06 · [LLM Jacking (AML.CS0030)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0030) (atlas-incident, high)
- 2024-12-01 · [Storm-2139 Azure OpenAI Guardrail Bypass (AML.CS0057)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0057) (atlas-incident, high)
- 2026-11-01 · [Barracuda cloud intrusion through a vendor's unretired access key, run with ARTEX](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-BARRACUDA-ARTEX-CLOUD-2026-11) (intrusion, confirmed)
- 2026-11-13 · [ARTEX-class intrusion at Bitrise through a dormant test bot account](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-BITRISE-ARTEX-2026-11) (intrusion, confirmed)
- 2026-04-15 · [Exploitation attempts against LiteLLM's guardrail tester (CVE-2026-40217)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-LITELLM-GUARDRAIL-TESTER-EXPLOITATION) (exploitation, high)
- 2026-10 · [Cloud and Kubernetes intrusion seen from both sides: victim telemetry plus the operator's open directory (Wiz)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-WIZ-CYBERSTRIKEAI-EKS-BOTH-SIDES-2026-10) (intrusion, high)
- 2025-12-05 · [Langflow CORS and refresh-cookie chain to account takeover and code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LANGFLOW-CVE-2025-34291) (cors-misconfiguration, confirmed)
- 2026-05-08 · [LiteLLM proxy SQL injection via authorization header](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LITELLM-CVE-2026-42208) (sql-injection, confirmed)
- 2026-05-08 · [LiteLLM proxy command injection in two endpoints](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-LITELLM-CVE-2026-42271) (command-injection, confirmed)

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

**Recorded results:** none. These cases are designed, not tested.

## 3. Detect it

### DET-AI-006 · AI Gateway Credential Anomaly

- **Severity:** high
- **Hypothesis:** An AI gateway identity accesses, exports or uses provider credentials outside its normal administrative pattern.
- **Telemetry:** `secret-access`, `gateway-admin`, `cloud-audit`, `provider-auth`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-047 · Denied-Call Burst Across Services Followed by a Success

- **Severity:** high
- **Hypothesis:** One cloud identity issues hundreds of API calls across many services in minutes, most of them denied, and one of them, often a secret read, succeeds. The Cloud Security Alliance's reading of the AntiFox intrusions describes this pattern; the value of the sweep is the few calls that succeed.
- **Telemetry:** `CloudTrail (eventSource, eventName, errorCode, userIdentity.arn, sourceIPAddress)`, `CloudTrail data events for read-only discovery APIs that are not management events (SQS ListQueues, GetQueueAttributes, GetQueueUrl, ListQueueTags, ListDeadLetterSourceQueues): off by default, enable with advanced event selectors`
- **Implementation:** rule file(s): [sentinel](../../detections/sentinel/det-ai-047-denied-burst-then-success.kql), [splunk](../../detections/splunk/det-ai-047-denied-burst-then-success.spl). Experimental and not run against real telemetry.

### DET-AI-053 · AI Service or Gateway Process Spawns a Shell or Network Utility

- **Severity:** critical
- **Hypothesis:** A self-hosted AI service (LiteLLM, Flowise, Langflow, MLflow, Ray, n8n, nginx-ui) or the Python/Node server hosting it (python, uvicorn, gunicorn, node) starts sh, bash, curl, wget, nc, npx or pip: post-exploitation of an exposed or vulnerable AI service. This widens the artex-detections web-service-spawns-shell rule, which lists Flowise only, to the AI infrastructure exploited in 2026 (KEV entries for LiteLLM, Langflow, MLflow, Ray, n8n).
- **Telemetry:** `EDR or auditd process creation with parent command line`, `container runtime process events`
- **Implementation:** rule file(s): [sentinel](../../detections/sentinel/det-ai-053-ai-service-spawns-shell.kql), [sigma](../../detections/sigma/det-ai-053-ai-service-spawns-shell.yml). Experimental and not run against real telemetry.

### DET-AI-056 · Unauthenticated or Unexpected Call to an AI Platform Admin, Test or Code Endpoint

- **Severity:** high
- **Hypothesis:** A request without an authenticated session, or outside a change window, reaches an AI platform route that runs code or reaches tools: LiteLLM /mcp-rest/test/*, /guardrails/test_custom_code and key/role changes; Flowise customMCP node load; Langflow public flow build, /api/v1/validate/code, /api/v1/auto_login and /api/v1/responses; nginx-ui /mcp_message and /api/backup. These are the routes behind the 2026 KEV entries for these products.
- **Telemetry:** `reverse proxy or WAF logs`, `AI gateway audit log`
- **Implementation:** rule file(s): [sigma](../../detections/sigma/det-ai-056-ai-platform-sensitive-endpoint.yml). Experimental and not run against real telemetry.

### DET-AI-060 · Canary Credential That Only Ever Lived in LLM Prompts Is Used

- **Severity:** critical
- **Hypothesis:** Prompt content sent to an AI gateway or third-party inference provider is logged, retained or resold despite no-retention terms, and secrets found in it are reused. A per-provider canary access key planted only in prompts turns any later use into proof of leakage and identifies the route. Dragos observed planted AWS keys used by third parties (OpenRouter ZDR removals, 2026-11-22); agent tools that return secrets into context (CVE-2026-135614) create the same exposure.
- **Telemetry:** `AWS CloudTrail (userIdentity.accessKeyId, sourceIPAddress, userAgent)`, `AI gateway request logs mapping canary IDs to provider routes`, `canary-token service callbacks (URLs, DNS)`
- **Implementation:** rule file(s): [sigma](../../detections/sigma/det-ai-060-prompt-only-canary-credential-used.yml). Experimental and not run against real telemetry.

## 4. Prevent it

- **Secret Isolation** (`CTRL-SECRET-ISOLATION`): Keep model/provider credentials outside prompts and minimize which agents can access them.

## 5. Close the loop

- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.
- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.
- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.
- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.
- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.

## 6. Limits of this page

- 1 of 5 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- No benchmark maps to it, so there is no public yardstick for how well a defence performs.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Tools and projects:** [NVIDIA/garak](https://github.com/NVIDIA/garak), [Tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard), [praetorian-inc/augustus](https://github.com/praetorian-inc/augustus), [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector), [garagon/aguara](https://github.com/garagon/aguara), [ThreatDefence/agentic-attack-detections](https://github.com/ThreatDefence/agentic-attack-detections)
- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T016)
