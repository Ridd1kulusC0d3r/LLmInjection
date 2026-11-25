#!/usr/bin/env python3
"""Redact secrets from an agent tool's OUTPUT before it reaches the model's context (stdlib only).

Daily-digest defence of 2026-11-25. Two cases motivate it: Amazon ECS MCP Server < 0.1.36 returned task-definition
environment variables and secret references unredacted (CVE-2026-135614, AWS bulletin 2026-200), and Dragos showed
that secrets inside prompts sent to inference providers were later reused by third parties (OpenRouter ZDR removals).
Whatever an MCP tool returns becomes prompt text, so redact at the tool boundary.

Heuristic layer, not a complete control: it misses secrets with no recognisable name or shape. Not tested in production.
    echo '{"environment":[{"name":"DB_PASSWORD","value":"x"}]}' | python examples/tool_output_redactor.py
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

MASK = "[REDACTED]"
SENSITIVE_NAME = re.compile(r"pass(word)?|secret|token|api[_-]?key|private[_-]?key|credential|dsn", re.I)
SECRET_SHAPES = re.compile("|".join((
    r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",               # AWS access key id
    r"\bsk-[A-Za-z0-9_-]{20,}\b",                   # OpenAI/OpenRouter-style keys
    r"\bgh[pousr]_[A-Za-z0-9]{30,}\b",              # GitHub tokens
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",          # PEM private key header
    r"\b[a-z][a-z0-9+.-]*://[^\s:/@]+:[^\s@]+@",    # URL carrying user:password
)))


def redact(node: Any, key: str = "") -> tuple[Any, int]:
    """Return (clean copy, number of redactions). Understands the ECS shape {"name": NAME, "value"|"valueFrom": V}."""
    if isinstance(node, dict):
        name, count, out = str(node.get("name", key)), 0, {}
        for k, v in node.items():
            sensitive = (k in ("value", "valueFrom") and SENSITIVE_NAME.search(name)) or (SENSITIVE_NAME.search(k) and isinstance(v, str))
            out[k], n = (MASK, 1) if sensitive else redact(v, k)
            count += n
        return out, count
    if isinstance(node, list):
        pairs = [redact(x, key) for x in node]
        return [p[0] for p in pairs], sum(p[1] for p in pairs)
    if isinstance(node, str):
        return SECRET_SHAPES.subn(MASK, node)
    return node, 0


def main() -> int:
    clean, count = redact(json.load(sys.stdin))
    print(json.dumps(clean, ensure_ascii=False))
    print(f"[redactor] {count} value(s) redacted", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
