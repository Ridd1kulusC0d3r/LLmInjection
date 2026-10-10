# Agent runtime, identity and observable threat behavior

This document is a defensive **design** and not a claim of live telemetry collection.

## Minimal semantic mapping

| Normalized field | OpenTelemetry GenAI / MCP reference | Use |
| --- | --- | --- |
| operation | gen_ai.operation.name | chat, invoke_agent, execute_tool |
| model | gen_ai.request.model | model context and version |
| provider | gen_ai.provider.name | inference provider context |
| agent | gen_ai.agent.name | agent/workflow identity |
| tool | gen_ai.tool.name | authorized tool classification |
| MCP method | mcp.method.name | protocol operation |
| error | error.type | denied/failed operation |
| trace | trace_id / span_id | sequencing and correlations |

Source: https://github.com/open-telemetry/semantic-conventions-genai

## Detection logic

Every hypothesis needs required telemetry, authorization context, expected false positives and safe validation. A tool call by itself is **not** an incident. Correlate role, approval outcome, model/runtime version, surrounding actions and asset inventory. Use synthetic fixtures to validate first.

## Confidentiality

Default to excluding raw prompts, responses, retrieved records, credentials, and tool arguments. Traces can contain private data. Apply retention limits, minimization, redaction, RBAC and explicit authorization. Version semantic conventions because several GenAI/MCP attributes are under development.

## Data graph links

AI component → versioned package → OSV/CVE → mitigation. Authorized agent → tool call → policy decision → sanitized telemetry → detection hypothesis. No inferred attribution or exploit claim without direct evidence.
