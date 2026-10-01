# LLMInjection MCP Server

A **read-only** Model Context Protocol interface over the validated LLMInjection datasets.

The server does not modify intelligence, execute commands, scan targets, or call external model providers.

## Requirements

The current official Python MCP SDK v2 is used:

```bash
python -m pip install -r integrations/mcp/requirements.txt
```

## Run locally with stdio

```bash
python integrations/mcp/server.py
```

Or with the MCP CLI:

```bash
mcp run integrations/mcp/server.py
```

## Streamable HTTP

```bash
LLMI_MCP_TRANSPORT=streamable-http LLMI_MCP_HOST=127.0.0.1 LLMI_MCP_PORT=8000 python integrations/mcp/server.py
```

The server is stateless and JSON-response oriented for HTTP use.

## Tools

- `search_ai_threat_intelligence`
- `get_intelligence_object`
- `get_intelligence_neighbors`
- `get_recent_ai_threat_activity`
- `get_technique_defensive_coverage`
- `get_intelligence_changes`

## Example questions

- Which campaigns are related to runtime LLM command generation?
- What evidence supports `LLMI-T015`?
- Which controls cover indirect prompt injection?
- Which techniques currently have no detection relationship?
- What changed since the latest committed snapshot?

## Trust boundary

MCP exposes the same evidence model as the repository. It does not elevate research-queue candidates into official intelligence.
