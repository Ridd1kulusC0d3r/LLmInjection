# Detection Engineering for AI / LLM Systems

The goal is not to detect the word "AI". The goal is to detect **unexpected capability use, trust-boundary crossings and changes in behavior** around AI systems.

## Telemetry map

| Telemetry | What it can reveal |
|---|---|
| Endpoint / EDR | local model runtimes, unexpected agent processes, tool execution, file changes |
| Network / proxy | AI-provider egress, model gateways, unusual destinations, abnormal request patterns |
| Identity / IAM | service-account misuse, token abuse, privilege escalation, unusual tool authorization |
| AI gateway | model/provider, caller, token usage, latency, prompt class metadata, policy decisions |
| Agent runtime | tool calls, capability requests, memory changes, planner/action transitions |
| RAG / vector store | ingestion source, document provenance, index changes, deletion/replacement events |
| CI/CD | package publication, dependency changes, provenance, build-token access, unexpected release path |
| Model registry | model source, digest, signature/provenance, version drift |
| Application | authorization failures, unsafe output handling, policy bypass attempts |
| Cloud | secret access, workload identity, unusual compute/model-serving activity |

## High-value detection hypotheses

### 1. AI egress from the wrong place

**Hypothesis:** a workload with no documented AI dependency begins contacting public model providers or model gateways.

Collect:
- process/workload identity;
- destination/provider;
- request volume;
- first-seen time;
- owning service/team.

Signal quality rises when AI egress appears alongside discovery, credential access, archive creation or unusual scripting.

### 2. Local model runtime where none is expected

**Hypothesis:** local LLM runtimes or model files appear on servers that are not designated AI/ML systems.

Useful evidence:
- newly installed runtime/application;
- new model-weight files;
- new local listening service;
- unexpected GPU/CPU usage;
- process lineage and user identity.

Do not treat the presence of a legitimate runtime alone as malicious. Context determines whether it is expected.

### 3. Agent moves from text to privileged action

**Hypothesis:** an agent requests or executes a tool capability that is inconsistent with the user's intent, the workflow or its normal baseline.

Prioritize transitions such as:
- read-only → write;
- user data → external send;
- low-privilege → privileged API;
- retrieved content → executable action;
- single-agent task → cross-agent delegation.

### 4. RAG or memory integrity change

**Hypothesis:** the knowledge layer receives content from an untrusted or newly introduced source and later drives sensitive actions.

Collect:
- source URI/repository;
- uploader/identity;
- content hash;
- ingestion timestamp;
- retrieval hits;
- downstream tool/action correlation.

### 5. Model or package provenance drift

**Hypothesis:** a model, package, agent extension or gateway release reaches production through an unexpected path.

Watch for:
- unsigned/unverified artifact;
- digest mismatch;
- new publisher identity;
- package version not associated with the project's normal release pipeline;
- dependency added by automation without review;
- CI secrets accessed by security tooling or third-party actions unexpectedly.

### 6. AI gateway credential concentration

AI gateways can hold credentials for many upstream providers. Treat them as high-value identity infrastructure.

Monitor:
- provider key reads;
- configuration exports;
- environment-variable access;
- unexpected admin API calls;
- sudden multi-provider traffic;
- changes to routing or fallback configuration.

## Behavioral chaining

Single events are often weak. Detection improves when chained:

```text
unexpected AI egress
  + host discovery / scripting
  + credential or secret access
  + archive/data staging
  + external transfer
= high-priority investigation
```

Likewise for agentic systems:

```text
untrusted retrieved content
  -> agent interprets instruction
  -> privileged tool request
  -> policy exception
  -> external side effect
= likely trust-boundary failure
```

## Detection content roadmap

Future releases should add vendor-neutral analytic specifications first, followed by mappings for:

- Sigma;
- Microsoft Sentinel KQL;
- Splunk SPL;
- Elastic ES|QL;
- Chronicle / Google SecOps YARA-L;
- cloud-native detections.

Each detection should link back to an intelligence record and framework mapping.
