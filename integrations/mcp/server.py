#!/usr/bin/env python3
"""Read-only MCP interface for LLMInjection intelligence."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mcp.server.mcpserver import MCPServer

from scripts.query_intel import (
    current_diff,
    get_neighbors,
    get_object,
    recent_activity,
    search_intelligence,
    technique_coverage,
)

mcp = MCPServer("LLMInjection Intelligence")


@mcp.tool()
def search_ai_threat_intelligence(
    query: str,
    object_type: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Search the local, validated LLMInjection intelligence datasets."""
    return search_intelligence(query, object_type, limit)


@mcp.tool()
def get_intelligence_object(object_id: str) -> dict[str, Any] | None:
    """Return one intelligence object by stable LLMInjection ID."""
    return get_object(object_id)


@mcp.tool()
def get_intelligence_neighbors(
    object_id: str,
    relationship: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Traverse evidence-backed graph relationships for one object."""
    return get_neighbors(object_id, relationship, limit)


@mcp.tool()
def get_recent_ai_threat_activity(limit: int = 20) -> list[dict[str, Any]]:
    """Return recent campaign, incident and vulnerability records from local data."""
    return recent_activity(limit)


@mcp.tool()
def get_technique_defensive_coverage(technique_id: str) -> dict[str, Any]:
    """Return tests, detections, controls, evidence and external mappings for a technique."""
    return technique_coverage(technique_id)


@mcp.tool()
def get_intelligence_changes() -> dict[str, Any]:
    """Return the latest generated entity-level intelligence diff when available."""
    return current_diff()


if __name__ == "__main__":
    transport = os.getenv("LLMI_MCP_TRANSPORT", "stdio")
    if transport == "streamable-http":
        host = os.getenv("LLMI_MCP_HOST", "127.0.0.1")
        port = int(os.getenv("LLMI_MCP_PORT", "8000"))
        mcp.run(
            transport="streamable-http",
            host=host,
            port=port,
            stateless_http=True,
            json_response=True,
        )
    else:
        mcp.run()
