# Detection Coverage

LLMInjection separates **intelligence**, **test coverage** and **production detection**. A safe test demonstrates a security boundary; a detection hypothesis describes telemetry that could reveal the same behavior in operations.

## Detection catalog

| ID | Detection | Primary telemetry | Test coverage |
|---|---|---|---|
| DET-AI-001 | Unexpected LLM Provider Egress | DNS, proxy, flow, workload identity | TC-NET-012 |
| DET-AI-002 | Unauthorized Local LLM Runtime | Process, port, file, inventory | TC-RUN-011 |
| DET-AI-003 | Agent Privilege Boundary Crossing | Agent plan, tool request, authorization, call | TC-AG-005 / 006 / AUTO-015 |
| DET-AI-004 | RAG or Memory Integrity Drift | Vector-store writes, memory writes, identity | TC-RAG-004 / MEM-007 |
| DET-AI-005 | Model Artifact Provenance Drift | Digest, registry, publisher, deployment gate | TC-SC-009 |
| DET-AI-006 | AI Gateway Credential Anomaly | Secret access, cloud audit, provider auth | TC-GW-020 |
| DET-AI-007 | New or Changed MCP Capability | Server inventory, capability list, config | TC-MCP-010 |
| DET-AI-008 | Agent Loop or Budget Exhaustion | Iterations, calls, tokens, cost | TC-COST-014 |
| DET-AI-009 | Automated Dependency Admission Without Review | Package manager, CI, review state | TC-SC-008 |
| DET-AI-010 | Sensitive Canary in Model Output | Response classification, canary hit | TC-DL-003 |
| DET-AI-011 | Assistant or IDE Config Written by Non-Editor Process | File events, process lineage, git diff, hook registration | TC-WS-017 |
| DET-AI-012 | CI Token Read From Runner Process Memory | Process access, runner process tree, token mint, cloud audit | gap |
| DET-AI-013 | Systematic Prompt Harvesting Pattern | API request log, account linkage, template similarity | TC-DIST-018 |
| DET-AI-014 | Scanner Verdict Despite Refusal | Scanner verdict, refusal flag, admission decision | TC-SCAN-016 |

## Detection-as-code starter pack

```text
detections/
├── sigma/        DET-AI-002, DET-AI-011
├── sentinel/
├── splunk/
├── elastic/
└── google-secops/
```

The starter rules deliberately target **observable behavior**, not attempts to classify arbitrary text as “AI generated”.

## Coverage model

```text
Threat behavior
    ↓
Required telemetry
    ↓
Detection hypothesis
    ↓
Vendor implementation
    ↓
Safe simulation / test
    ↓
Coverage result
```

A production deployment should maintain allowlists and inventory externally. The repository examples intentionally do not pretend that a universal list of approved AI providers, agent binaries or MCP servers exists.
