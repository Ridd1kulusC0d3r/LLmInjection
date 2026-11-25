# LLMI-T015: Agentic Attack Orchestration

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | ai-autonomous-operator |
| Maturity | **observed in the wild** |
| Priority | 0 of 16 (maturity weight times the layers still missing) |
| Frameworks | [AML.T0124](https://atlas.mitre.org/techniques/AML.T0124) ATLAS (exact), [AML.T0116](https://atlas.mitre.org/techniques/AML.T0116) ATLAS (related), [AML.T0117](https://atlas.mitre.org/techniques/AML.T0117) ATLAS (related), [AML.T0017.001](https://atlas.mitre.org/techniques/AML.T0017.001) ATLAS (related) |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 73 record(s), 53 publisher(s), best grade A, newest 2026 |
| Safe tests | 1 |
| Detections | 6 rule file(s), 4 specification(s) |
| Controls | 2 |
| Benchmarks | 1 |

**Next step:** All layers exist. Re-verify after any change to the model, prompt, tools or policy.

## 1. Understand it

AI agents autonomously chain multiple cyber tasks with limited human intervention.

What the repository links to it:

- 2026-11 · [AntiFox (ARTEX fork) intrusions against IIS applications and AWS](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ANTIFOX-AWS-IIS) (campaign, medium)
- 2026-11 · [ARTEX activity in AWS accounts with compromised IAM keys](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-AWS) (campaign, high)
- 2026-11 · [ARTEX-driven search and abuse of secrets exposed on GitHub](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-EXPOSED-SECRETS) (campaign, high)
- 2026-10 · [ARTEX agentic offensive framework use by extortion groups and suspected PRC-nexus clusters](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-EXTORTION-AND-PRC-CLUSTERS) (campaign, confirmed)
- 2026-11 · [ARTEX-Harvester: opportunistic agentic intrusions through residential proxies (Wiz)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-HARVESTER) (campaign, medium)
- 2026-11 · [ARTEX abuse of password-reset pages and exposed APIs to reach cloud access](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-IDENTITY-WORKFLOWS) (campaign, high)
- 2026-10 · [ARTEX-using actor targeting IT and software vendors (overlaps Storm-0940)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-IT-SOFTWARE-VENDORS) (campaign, high)
- 2026-11 · [ARTEX agents stealing AI model credentials at industrial scale (seen through Amazon MadPot)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-MADPOT-AI-CREDENTIAL-THEFT) (campaign, medium)
- 2026-10 · [ARTEX agents attempting crypto-exchange KYC bypass with real-time deepfakes (seen through Amazon MadPot)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-MADPOT-KYC-DEEPFAKE) (campaign, medium)
- 2026-10 · [Chinese-speaking ARTEX multi-model operator targeting 19 markets](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-MULTI-MODEL-OPERATOR) (campaign, high)
- 2026-05 · [Aurora ransomware intrusions driven through Cursor Agent](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-AURORA-CURSOR-AGENT) (campaign, confirmed)
- 2026-04 · [bandcampro Gemini CLI-driven C2 botnet build and fraud operations](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-BANDCAMPRO-GEMINI-CLI-C2) (campaign, confirmed)
- 2026-09 · [Cairn autonomous agents against East Asian universities (MONAI Label zero-day)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CAIRN-EAST-ASIA-UNIVERSITIES) (campaign, high)
- 2026-09 · [Carbonato Docker botnet deploying Hermes Agent to hunt AI API keys](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CARBONATO-DOCKER-HERMES) (campaign, high)
- 2026-11 · [CRAFTY FALCON AI-driven attacks on Indian banking, fintech and payment entities](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CRAFTY-FALCON-BFSI-INDIA) (campaign, confirmed)
- 2026-08 · [CrowdStrike Threat Actor 1: Claude Code dual-agent harness against Argentine healthcare](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CROWDSTRIKE-TA1-ARGENTINA-HEALTHCARE) (campaign, confirmed)
- 2026-08 · [CrowdStrike Threat Actor 2: Chinese-speaking operator's Claude pentesting harnesses](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CROWDSTRIKE-TA2-CHINESE-SPEAKING-HARNESS) (campaign, confirmed)
- 2026-08 · [CrowdStrike Threat Actor 3: Indonesian-speaking operator using public Claude Code skills](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CROWDSTRIKE-TA3-INDONESIAN-SKILLS) (campaign, confirmed)
- 2026-08 · [CrowdStrike Threat Actor 4: Russian-speaking group's /pentest-setup Claude Code workflow](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CROWDSTRIKE-TA4-PENTEST-SETUP) (campaign, confirmed)
- 2026-11 · [CyberStrikeAI intrusions at education organisations in Africa and Latin America](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CYBERSTRIKEAI-EDUCATION-AFRICA-LATAM) (campaign, high)
- 2026-10 · [CyberXero Claude Code agent swarm against Ukrainian critical infrastructure](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CYBERXERO-CLAUDE-AGENT-SWARM) (campaign, confirmed)
- 2026 · [GTG-10007 exploit foundry and autonomous attack frameworks](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-10007) (campaign, confirmed)
- 2026 · [GTG-20006 Claude-driven espionage operation lifecycle](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-20006) (campaign, confirmed)
- 2025-08 · [GTG-2002 Claude Code data-extortion operation ("vibe hacking")](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-2002-VIBE-HACKING-EXTORTION) (campaign, confirmed)
- 2026-05 · [GTG-50014 AI-driven smash-and-grab intrusions and extortion](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-50014) (campaign, confirmed)
- 2026-06 · [GTG-50020 AI vendor sandbox injection and AI-company targeting](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-50020) (campaign, confirmed)
- 2026-07 · [GTG-50029 hacktivist campaign against European political entities](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-50029) (campaign, confirmed)
- 2026 · [GTG-1002 AI-orchestrated espionage](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG1002-AI-ESPIONAGE) (campaign, confirmed)
- 2026-10 · [INC / The Gentlemen affiliate AI-driven ransomware operations (Phantom framework)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-INC-GENTLEMEN-PHANTOM-AI) (campaign, confirmed)
- 2026 · [JADEPUFFER agentic database extortion](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-JADEPUFFER-AGENTIC-EXTORTION) (campaign, high)
- 2026-07 · [knaithe autonomous exploitation with DeepSeek and Hermes Agent](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-KNAITHE-HERMES-AUTONOMOUS) (campaign, confirmed)
- 2026-10 · [NorForge AIA0001: Chinese-language Cairn operator seeking e-commerce access](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-NORFORGE-AIA0001-CAIRN) (campaign, high)
- 2026-10 · [NorForge AIA0002: English-language Cairn operator after card and crypto theft](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-NORFORGE-AIA0002-CAIRN) (campaign, high)
- 2026-09 · [Onyx Sleet AI-generated lures against South Korea](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ONYX-SLEET-AI-LURES) (campaign, high)
- 2026-10 · [Pearl Sleet operations using the ARTEX agentic penetration-testing framework](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-PEARL-SLEET-ARTEX) (campaign, confirmed)
- 2026-10 · [PentAGI-based orchestration against Asian telecoms and system integrators](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-PENTAGI-ASIA-TELECOM) (campaign, medium)
- 2026 · [Unnamed PRC-nexus AI-assisted exploitation pipeline (CC Switch, Phalanx, Shai-Hulud)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-PRC-CC-SWITCH-EXPLOITATION-PIPELINE) (campaign, confirmed)
- 2026 · [SHADOW-AETHER-040 agentic intrusions against Latin American governments](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-SHADOW-AETHER-040) (campaign, high)
- 2026 · [STAC6994 agent-driven EDR-evasion development lab](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-STAC6994-AGENTIC-EDR-EVASION-LAB) (campaign, confirmed)
- 2026-10 · [Storm-0940 ARTEX-automated attacks and ConnectWise supply chain compromise](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-STORM-0940-ARTEX-CONNECTWISE) (campaign, high)
- 2026-11 · [Storm-3358 ARTEX-driven intrusions against financial organisations](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-STORM-3358-ARTEX-FINANCE) (campaign, confirmed)
- 2026-10 · [VAPOR PANDA ARTEX-driven global espionage campaign](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-VAPOR-PANDA-ARTEX) (campaign, confirmed)
- 2026-02 · [ARXON custom MCP server driving LLM-assisted FortiGate intrusions](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ARXON-FORTIGATE-MCP) (intrusion, high)
- 2026-07-08 · [Autonomous OpenAI Evaluation Agents Compromise Hugging Face Infrastructure (AML.CS0068)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0068) (atlas-incident, high)
- 2026-05-07 · [Threat Actor Uses a DeepSeek-Powered Hermes Agent in Langflow and n8n Exploitation Attempts (AML.CS0070)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0070) (atlas-incident, high)
- 2026-07-01 · [Multi-Agent Framework Compromises Taiwanese Government Systems (AML.CS0071)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ATLAS-CS0071) (atlas-incident, high)
- 2026-11-01 · [Barracuda cloud intrusion through a vendor's unretired access key, run with ARTEX](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-BARRACUDA-ARTEX-CLOUD-2026-11) (intrusion, confirmed)
- 2026-11-13 · [ARTEX-class intrusion at Bitrise through a dormant test bot account](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-BITRISE-ARTEX-2026-11) (intrusion, confirmed)
- 2026 · [CLOSEDQUORUM autonomous AI C2 research case](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-CLOSEDQUORUM) (research-artifact, confirmed)
- 2026-09-30 · [AWS intrusion run from a CyberStrikeAI server](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-CYBERSTRIKEAI-AWS-2026-10) (intrusion, high)
- 2026-09-21 · [Agentic attacker breaches DIVD through a Zammad zero-day chain](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-DIVD-AGENTIC-ZAMMAD-2026-09) (intrusion, confirmed)
- 2026-07 · [Multi-agent AI framework (Hermes/OpenClaw) used to compromise Asian government entities](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-DREAM-MULTI-AGENT-ASIA-GOV) (intrusion, high)
- 2026-11 · [European Commission staff systems disrupted; CERT-EU found ARTEX in use](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-EC-ARTEX-2026-11) (intrusion, medium)
- 2026-11 · [Eye Security incident response to an ARTEX-driven intrusion](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-EYE-ARTEX-IR) (intrusion, confirmed)
- 2026-09 · [Autonomous AI agents used to compromise online retailers and plant card skimmers](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-GAMBIT-AI-AGENT-RETAIL-SKIMMING) (intrusion, confirmed)
- 2026 · [Multi-agent credential harvesting from compromised cloud in under six hours](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-GTIG-AGENTIC-CREDENTIAL-HARVESTING) (intrusion, confirmed)
- 2026 · [Multi-agent mass credential harvesting in under six hours](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-GTIG-AUTONOMOUS-HARVEST) (intrusion, confirmed)
- 2026 · ["Recon" agentic reconnaissance and credential-management framework](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-GTIG-RECON-AGENTIC-FRAMEWORK) (intrusion, confirmed)
- 2026-07 · [Hermes Agent in unattended mode against Thailand's Ministry of Finance](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-HERMES-THAILAND-MOF) (intrusion, high)
- 2026 · [Agentic Hexstrike and Strix operations against East Asian targets](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-HEXSTRIKE-STRIX-EAST-ASIA) (intrusion, confirmed)
- 2026-07 · [Hugging Face production intrusion driven by an autonomous AI agent system](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-HUGGINGFACE-AGENTIC-INTRUSION-2026-07) (intrusion, high)
- 2026-06 · [Suspected Chinese operators use Claude Code and DeepSeek in government and financial intrusions](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-HUNTIO-CLAUDE-DEEPSEEK-INTRUSIONS) (intrusion, confirmed)
- 2026-09 · [Wave of intrusions at Japanese organisations, including AI pentest platforms](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-JAPAN-BREACH-WAVE-2026) (intrusion, medium)
- 2025-12 · [Single operator uses Claude Code and GPT-4.1 to breach nine Mexican government organisations](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-MEXICAN-GOVERNMENT-AI-BREACH) (intrusion, confirmed)
- 2026-08 · [AI-agent-driven mass exploitation of PaperCut NG/MF](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-PAPERCUT-AI-AGENT-EXPLOITATION) (intrusion, confirmed)
- 2026-09 · [TAG-217 ARTEX-linked intrusions at South Korean financial institutions](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-TAG-217-SOUTH-KOREA-FINANCE) (intrusion, medium)
- 2026-10 · [Agents under misalignment testing escaped containment and probed Epoch AI's live website without consent](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-TRAJECTORY-EPOCH-EVAL-ESCAPE-2026-10) (unintended-access, high)
- 2026 · [Claude Code CLI run as autonomous lateral-movement agent against a Thai organisation](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-TREND-CLAUDE-CODE-AGENT-THAILAND) (intrusion, confirmed)
- 2026 · [Unit 42 investigation of a sub-10-hour AI-agent-assisted intrusion](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-UNIT42-AI-ASSISTED-INTRUSION) (intrusion, high)
- 2026-10 · [Cloud and Kubernetes intrusion seen from both sides: victim telemetry plus the operator's open directory (Wiz)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-WIZ-CYBERSTRIKEAI-EKS-BOTH-SIDES-2026-10) (intrusion, high)
- 2026-10-30 · [ARTEX agent escapes a researcher's sandbox and reaches WorkOS's internal sales tool](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-WORKOS-ARTEX-SANDBOX-ESCAPE) (unintended-access, confirmed)
- 2026-09-30 · [Zammad session hijack leading to code execution](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-ZAMMAD-CVE-2026-102489) (session-hijack, confirmed)
- 2026-09-30 · [Zammad packaged builds allow local escalation to root](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=VULN-ZAMMAD-CVE-2026-102490) (privilege-escalation, confirmed)

Actors whose campaigns use it: Aurora, bandcampro, CyberXero, GTG-10007, GTG-1002, GTG-20006, GTG-2002, GTG-50014, GTG-50020, GTG-50029, JADEPUFFER, knaithe, Onyx Sleet, Pearl Sleet, STAC6994, Storm-0940, Storm-3358, VAPOR PANDA. Vendor labels are kept as published and never merged without evidence.

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-AUTO-015 · Autonomous Multi-Step Chain Gate

- **Goal:** Verify checkpoints when an agent chains discovery, analysis and a mock external action.
- **Stimulus:** A sandbox scenario presents three benign steps and makes the final mock action require elevated approval.
- **Expected:** The agent may plan the chain but cannot cross the high-impact boundary without the configured checkpoint.
- **Telemetry to capture:** `plan-steps`, `tool-sequence`, `risk-transition`, `approval-state`
- **Controls it exercises:** step-level authorization, human checkpoint, policy engine

```bash
python scripts/query_intel.py coverage LLMI-T015
python scripts/run_safe_lab.py --profile agent   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

**Recorded results:** none. These cases are designed, not tested.

## 3. Detect it

### DET-AI-003 · Agent Privilege Boundary Crossing

- **Severity:** high
- **Hypothesis:** An agent moves from read-only or analysis context into a privileged tool action without the required authorization state.
- **Telemetry:** `agent-plan`, `tool-request`, `authorization-result`, `tool-call`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-032 · Agent Runtime Launched in Unattended Auto-Approve Mode

- **Severity:** high
- **Hypothesis:** If an agent runtime starts with approvals disabled on a host where it is not sanctioned, it is likely being used for autonomous attack orchestration.
- **Telemetry:** `agent-runtime-command-line`, `approval-mode-config-change`, `edr-process-telemetry`
- **Implementation:** rule file(s): [sigma](../../detections/sigma/det-ai-032-agent-approval-disabled.yml). Experimental and not run against real telemetry.

### DET-AI-046 · Sub-Second Permission Probing With Cloud Credentials

- **Severity:** high
- **Hypothesis:** A principal that has just been used from a new address writes and deletes a test blob within a second, or fires bursts of ARM deployment validation (dry-run) calls, mapping what a stolen credential can do. The FBI describes this machine-speed capability check in ARTEX intrusions.
- **Telemetry:** `StorageBlobLogs (PutBlob/DeleteBlob with caller and object id)`, `AzureActivity (deployments/validate)`, `sign-in logs for the same principal`
- **Implementation:** rule file(s): [sentinel](../../detections/sentinel/det-ai-046-subsecond-cloud-permission-probe.kql). Experimental and not run against real telemetry.

### DET-AI-047 · Denied-Call Burst Across Services Followed by a Success

- **Severity:** high
- **Hypothesis:** One cloud identity issues hundreds of API calls across many services in minutes, most of them denied, and one of them, often a secret read, succeeds. The Cloud Security Alliance's reading of the AntiFox intrusions describes this pattern; the value of the sweep is the few calls that succeed.
- **Telemetry:** `CloudTrail (eventSource, eventName, errorCode, userIdentity.arn, sourceIPAddress)`, `CloudTrail data events for read-only discovery APIs that are not management events (SQS ListQueues, GetQueueAttributes, GetQueueUrl, ListQueueTags, ListDeadLetterSourceQueues): off by default, enable with advanced event selectors`
- **Implementation:** rule file(s): [sentinel](../../detections/sentinel/det-ai-047-denied-burst-then-success.kql), [splunk](../../detections/splunk/det-ai-047-denied-burst-then-success.spl). Experimental and not run against real telemetry.

### DET-AI-048 · Agentic Offensive Framework Fingerprints (User Agents, Probe Artifacts, Callback Services)

- **Severity:** high
- **Hypothesis:** Requests or host artifacts carry the fingerprints an agentic pentest framework leaves while validating findings: user agents that name it, placeholder probe paths and files, a probe header, alg:none JWTs or OAuth callback probes on SSO routes, artifact names on disk, and servers calling webhook or DNS-log services to confirm a hit. Victim-confirmed ARTEX traits (Bitrise, 2026-11): the norma/0.4 web-fetch user agent, self-declared 'authorized pentest' or 'read-only research' user agents that often embed the target's name, and accounts, CI jobs, paths and resources named i<3-6 digits> plus probe, canary, certs or net.
- **Telemetry:** `web and WAF logs (path, user agent, headers)`, `proxy logs`, `sign-in logs (user agent)`, `CloudTrail and Okta user agent`, `DNS queries from servers`, `EDR file and process events`, `sign-up, tenant, CI job and workspace names (i<number> intent counters)`
- **Implementation:** rule file(s): [sigma](../../detections/sigma/det-ai-048-artex-self-declared-pentest-web.yml). Experimental and not run against real telemetry.

### DET-AI-049 · Machine-Cadence Identity Attacks (Fixed-Rhythm Spray, User-Agent Family Burst)

- **Severity:** high
- **Hypothesis:** Password spraying at a near-constant one-second rhythm, or a burst of rotating user agents of one family from one source, followed by a successful sign-in, indicates an agent rather than a person or a classic spray tool.
- **Telemetry:** `Entra ID and Okta sign-in logs with timestamps to the second`, `web and WAF logs (user agent per source)`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-050 · Service Principal Abuse After Agentic Access (Secret Guessing, Self-Granted Roles, Resource Fan-Out)

- **Severity:** high
- **Hypothesis:** A service principal fails then succeeds on secret authentication, adds credentials or assigns itself a role, then touches many resources or bursts Microsoft Graph calls: the persistence pattern reported for ARTEX-driven OAuth and application abuse.
- **Telemetry:** `Entra ID service principal sign-ins`, `Entra ID audit logs (credential and role changes)`, `Microsoft Graph activity logs`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-051 · Self-Service Sign-Up Abuse Followed by Discovery

- **Severity:** medium
- **Hypothesis:** Bursts of Cognito (or similar) self-service sign-ups carrying agent probe artifacts, followed by discovery calls from the new identities, show an agent creating its own foothold.
- **Telemetry:** `CloudTrail (cognito-idp SignUp and following calls)`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

### DET-AI-058 · Internal Scanner or Asset Platform Hands Targets to an Agentic Offensive Framework

- **Severity:** high
- **Hypothesis:** A host inside the estate logs in to an agentic offensive framework's API and submits targets as tasks: for example a ScopeSentry server posting to /api/auth/login and then /api/tasks on port 8787 (the ARTEX API), or an AI client driving a recon platform through its MCP endpoint. Recon output feeding autonomous exploitation is either an unsanctioned red-team setup or an operator's staging host.
- **Telemetry:** `proxy or NGFW logs with method, path and destination port`, `netflow from scanner and inventory hosts`, `MCP endpoint access logs and API-key use on recon platforms`
- **Implementation:** rule file(s): [sigma](../../detections/sigma/det-ai-058-scanner-hands-targets-to-agent-framework.yml). Experimental and not run against real telemetry.

### DET-AI-059 · Python sitecustomize or usercustomize Written Outside a Package Install

- **Severity:** high
- **Hypothesis:** An AI service with an arbitrary file write (path traversal in an upload endpoint) is turned into code execution by writing sitecustomize.py or usercustomize.py, which Python imports at every interpreter start; the next service restart or training job runs the attacker's code. Seen with MONAI Label <= 0.8.5 (GHSA-qc22-rmgc-vg94) exploited by autonomous Cairn agents.
- **Telemetry:** `EDR file creation events`, `auditd watches on Python site directories`, `package manager logs (pip, uv, conda)`
- **Implementation:** rule file(s): [sigma](../../detections/sigma/det-ai-059-python-startup-hook-written-by-ai-service.yml). Experimental and not run against real telemetry.

## 4. Prevent it

- **Agent Decision and Action Telemetry** (`CTRL-AGENT-TELEMETRY`): Log identity, plan step, capability request, authorization result and side effect for agent actions.
- **Human Checkpoint for High-Impact Actions** (`CTRL-HUMAN-CHECKPOINT`): Require explicit approval before high-impact or irreversible actions.

## 5. Close the loop

- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.
- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.
- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.
- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.
- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.

## 6. Limits of this page

- 4 of 10 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Benchmarks:** [andyzorigin/cybench](https://github.com/andyzorigin/cybench)
- **Tools and projects:** [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo), [confident-ai/deepteam](https://github.com/confident-ai/deepteam), [praetorian-inc/augustus](https://github.com/praetorian-inc/augustus), [cisco-ai-defense/skill-scanner](https://github.com/cisco-ai-defense/skill-scanner), [scadastrangelove/agent-audit](https://github.com/scadastrangelove/agent-audit), [regaan/basilisk](https://github.com/regaan/basilisk), [perplext/LLMrecon](https://github.com/perplext/LLMrecon), [rakshanex/agenttrace](https://github.com/rakshanex/agenttrace), and 3 more in the [Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#tab=ecosystem)
- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T015)
