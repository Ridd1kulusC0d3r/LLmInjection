#!/usr/bin/env python3
"""A tool-invocation gate for an AI agent: the model asks, deterministic code decides (stdlib only).

This is the worked example of playbook LLMI-T008 (Agent Tool Misuse). It turns six LLMInjection safe-lab test cases into
code you can read, run and adapt. The model never authorises anything: its output is a *request*, and this gate answers it
from configuration and from the caller's identity.

    TC-MCP-010   a tool description cannot grant itself authority      -> tools exist only if code registered them
    TC-AG-005    untrusted content cannot trigger a privileged tool    -> side effects need a user-turn origin
    TC-PARAM-019 model-supplied parameters are validated outside it    -> per-tool validators, default deny
    TC-AUTHZ-029 object-level authorisation uses the caller identity   -> the app looks the owner up; the model only names the object
    TC-TOOL-030  fetch tools enforce destination allowlists            -> private and link-local targets are refused
    TC-AG-006    high-impact actions need a human checkpoint           -> the call parks until an approver says yes

It is a teaching sketch, not a product: no sandboxing, no network, no persistence. Run it:  python examples/agent_tool_gate.py
"""

from __future__ import annotations

import ast
import ipaddress
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

USER_TURN, UNTRUSTED = "user-turn", "untrusted"  # where the request came from: a person's turn, or content the agent read


@dataclass(frozen=True)
class Caller:
    """Who is asking. Built by the application from the authenticated session, never from model output."""

    user_id: str
    roles: frozenset[str] = frozenset()


@dataclass
class Tool:
    name: str
    handler: Callable[..., Any]
    side_effect: bool = False                                  # anything that changes state or leaves the system
    high_impact: bool = False                                  # irreversible or costly: needs a human checkpoint
    validate: Callable[[dict], None] = lambda params: None     # raises ValueError on a bad parameter
    owner_of: Callable[[dict], str | None] = lambda params: None  # who owns the object this call touches, looked up by the app
    params: frozenset[str] | None = None                       # the only parameter names the tool accepts; None means unchecked


@dataclass
class Decision:
    allowed: bool
    reason: str
    result: Any = None


@dataclass
class Gate:
    tools: dict[str, Tool]
    approver: Callable[[str, dict], bool] = lambda tool, params: False   # default: nobody approves
    audit: list[dict] = field(default_factory=list)

    def call(self, caller: Caller, tool: str, params: dict, origin: str = USER_TURN) -> Decision:
        decision = self._decide(caller, tool, params, origin)
        # The telemetry fields the test cases ask for: request, caller identity, authorisation result, tool result or reason.
        self.audit.append({"tool-request": {"tool": tool, "params": params, "origin": origin}, "caller-identity": caller.user_id,
                           "authorization-result": "allow" if decision.allowed else "deny", "reason": decision.reason,
                           "tool-result": decision.result if decision.allowed else None})
        return decision

    def _decide(self, caller: Caller, name: str, params: dict, origin: str) -> Decision:
        spec = self.tools.get(name)
        if spec is None:                                       # TC-MCP-010: the model cannot add or rename capabilities
            return Decision(False, "not-allowlisted")
        if spec.side_effect and origin != USER_TURN:           # TC-AG-005: retrieved or tool-returned text is data, not authority
            return Decision(False, "side-effect-from-untrusted-origin")
        try:
            if spec.params is not None and set(params) - spec.params:
                raise ValueError(f"unexpected parameters {sorted(set(params) - spec.params)}")   # default deny for anything undeclared
            spec.validate(params)                              # TC-PARAM-019: deterministic validation, outside the model
        except ValueError as exc:
            return Decision(False, f"invalid-parameters: {exc}")
        owner = spec.owner_of(params)
        if owner is not None and owner != caller.user_id and "admin" not in caller.roles:   # TC-AUTHZ-029
            return Decision(False, "object-owner-mismatch")
        if spec.high_impact and not self.approver(name, params):                            # TC-AG-006
            return Decision(False, "pending-human-approval")
        return Decision(True, "allowed", spec.handler(**params))


# --- validators: small, strict and boring on purpose -----------------------------------------------------------------

def arithmetic_only(expression: str) -> float:
    """Evaluate +, -, *, / and parentheses over numbers. Anything else, including names and calls, is rejected."""
    allowed = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub, ast.UAdd)
    tree = ast.parse(expression, mode="eval")
    if not all(isinstance(node, allowed) for node in ast.walk(tree)) or not all(
            isinstance(n.value, (int, float)) for n in ast.walk(tree) if isinstance(n, ast.Constant)):
        raise ValueError("only arithmetic is allowed")
    return eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}})  # noqa: S307  (the tree was whitelisted above)


def inside(base: Path) -> Callable[[dict], None]:
    """Validator factory: the `path` parameter must resolve to somewhere under `base` (blocks ../ and absolute paths)."""
    def check(params: dict) -> None:
        target = (base / str(params.get("path", ""))).resolve()
        if base.resolve() not in (target, *target.parents):
            raise ValueError("path leaves the allowed directory")
    return check


def public_https_host(allowed_hosts: set[str]) -> Callable[[dict], None]:
    """Validator factory for a fetch tool: https only, an allowlisted host, never a private or link-local address."""
    def check(params: dict) -> None:
        url = urlparse(str(params.get("url", "")))
        host = url.hostname or ""
        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            ip = None                                          # a name, not an address literal
        if ip is not None and (ip.is_private or ip.is_link_local or ip.is_loopback or ip.is_reserved):
            raise ValueError("private or link-local address")
        if url.scheme != "https" or host not in allowed_hosts:
            raise ValueError("destination is not allowlisted")
    return check


ACCOUNTS = {"acct-1": "alice", "acct-2": "bob"}   # the application's own records: the model only ever names an object, never its owner


def demo() -> None:
    base = Path(__file__).resolve().parent
    gate = Gate(
        tools={
            "calc": Tool("calc", lambda expression: arithmetic_only(expression), validate=lambda p: arithmetic_only(str(p.get("expression", "")))),
            "read_note": Tool("read_note", lambda path: (base / path).name, validate=inside(base)),
            "fetch": Tool("fetch", lambda url: f"(would fetch {url})", side_effect=True, validate=public_https_host({"example.org"})),
            "send_payment": Tool("send_payment", lambda from_account, amount: f"sent {amount} from {from_account}", side_effect=True, high_impact=True,
                                 owner_of=lambda p: ACCOUNTS.get(p.get("from_account")), params=frozenset({"from_account", "amount"})),
        },
    )
    alice = Caller("alice")
    cases = [
        ("calc", {"expression": "2 * (3 + 4)"}, USER_TURN),
        ("calc", {"expression": "__import__('os').system('id')"}, USER_TURN),
        ("read_note", {"path": "../../etc/passwd"}, USER_TURN),
        ("fetch", {"url": "https://169.254.169.254/latest/meta-data"}, USER_TURN),
        ("fetch", {"url": "https://example.org/page"}, UNTRUSTED),
        ("send_payment", {"from_account": "acct-2", "amount": 100}, USER_TURN),
        ("send_payment", {"from_account": "acct-1", "amount": 100}, USER_TURN),
        ("send_payment", {"from_account": "acct-1", "amount": 100, "approved": True}, USER_TURN),
        ("shell", {"cmd": "id"}, USER_TURN),
    ]
    for tool, params, origin in cases:
        d = gate.call(alice, tool, params, origin)
        print(f"{'ALLOW' if d.allowed else 'DENY ':5} {tool:13} {origin:10} {d.reason}")
    print(json.dumps(gate.audit[1], indent=2)[:400])


if __name__ == "__main__":
    demo()
