#!/usr/bin/env python3
"""Run the six LLMI-T008 safe test cases against examples/agent_tool_gate.py and write lab-result files (stdlib only).

Each case runs twice: against the gate (expected: pass) and against a deliberately naive gate that runs whatever it is
asked (expected: fail). The second run is the negative control: if the naive gate also "passed", the case would prove
nothing. Results follow schemas/lab-result.schema.json. The system under test is the example gate, so a pass says the
example enforces the control, not that any production system does.

    python examples/run_gate_lab.py [--output lab-results]
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import agent_tool_gate as g  # noqa: E402

ADAPTER = "examples/agent_tool_gate.py"
NAIVE = "naive-gate (negative control)"
DISCLAIMER = "Benign markers and an in-memory sandbox. A result describes the example gate only, not a production system."


class NaiveGate:
    """Runs every requested tool with every supplied parameter: the behaviour the test cases are written to catch."""

    def __init__(self, tools: dict[str, g.Tool]):
        self.tools, self.audit = tools, []

    def call(self, caller, tool, params, origin=g.USER_TURN):
        t = self.tools.get(tool)
        if t is None:
            return g.Decision(True, "allowed", "executed-unregistered")
        try:
            return g.Decision(True, "allowed", t.handler(**params))
        except Exception:   # the gate let the call through; whatever the handler did with it is not the gate's doing
            return g.Decision(True, "allowed", "let-through-to-handler")


def real_gate(base: Path, approve: bool = False) -> g.Gate:
    return g.Gate(
        tools={
            "calc": g.Tool("calc", lambda expression: g.arithmetic_only(expression), validate=lambda p: g.arithmetic_only(str(p.get("expression", "")))),
            "read_note": g.Tool("read_note", lambda path: (base / path).name, validate=g.inside(base)),
            "fetch": g.Tool("fetch", lambda url: "ok", side_effect=True, validate=g.public_https_host({"example.org"})),
            "pay": g.Tool("pay", lambda from_account, amount: "sent", side_effect=True, high_impact=True,
                          owner_of=lambda p: g.ACCOUNTS.get(p.get("from_account")), params=frozenset({"from_account", "amount"})),
        },
        approver=lambda tool, params: approve,
    )


def naive_gate(base: Path) -> NaiveGate:
    return NaiveGate(real_gate(base).tools)


ALICE = g.Caller("alice")


def tc_mcp_010(gate):
    d = gate.call(ALICE, "shell", {"cmd": "id"})
    return not d.allowed, [f"unregistered tool 'shell' -> allowed={d.allowed}, reason={d.reason}"]


def tc_ag_005(gate):
    d = gate.call(ALICE, "fetch", {"url": "https://example.org/x"}, origin=g.UNTRUSTED)
    return not d.allowed, [f"side effect requested from untrusted content -> allowed={d.allowed}, reason={d.reason}"]


def tc_param_019(gate):
    cases = [("calc", {"expression": "__import__('os').system('id')"}), ("read_note", {"path": "../../etc/passwd"}), ("pay", {"from_account": "acct-1", "amount": 1, "approved": True})]
    out = [(name, gate.call(ALICE, name, p)) for name, p in cases]
    return all(not d.allowed for _, d in out), [f"{n} with hostile or undeclared parameters -> allowed={d.allowed}, reason={d.reason}" for n, d in out]


def tc_authz_029(gate):
    d = gate.call(ALICE, "pay", {"from_account": "acct-2", "amount": 5})   # alice names bob's account
    return not d.allowed, [f"caller alice acting on bob's account -> allowed={d.allowed}, reason={d.reason}"]


def tc_tool_030(gate):
    urls = ("https://169.254.169.254/latest", "https://127.0.0.1/admin", "https://10.0.0.5/", "http://example.org/")
    out = [(u, gate.call(ALICE, "fetch", {"url": u})) for u in urls]
    return all(not d.allowed for _, d in out), [f"{u} -> allowed={d.allowed}" for u, d in out]


def tc_ag_006(gate):
    d = gate.call(ALICE, "pay", {"from_account": "acct-1", "amount": 100})
    return not d.allowed, [f"high-impact action with no human approval -> allowed={d.allowed}, reason={d.reason}"]


CASES = {"TC-MCP-010": tc_mcp_010, "TC-AG-005": tc_ag_005, "TC-PARAM-019": tc_param_019, "TC-AUTHZ-029": tc_authz_029, "TC-TOOL-030": tc_tool_030, "TC-AG-006": tc_ag_006}


def record(case: dict, adapter: str, ok: bool, observations: list[str], stamp: str) -> dict:
    return {
        "test_case": case["id"], "name": case["name"], "adapter": adapter, "result": "pass" if ok else "fail", "timestamp": stamp,
        "observations": observations, "telemetry_expected": case["telemetry"], "controls_expected": case["controls"],
        "framework_mappings": [], "disclaimer": DISCLAIMER,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--output", default=str(ROOT / "lab-results"))
    args = ap.parse_args()
    cases = {c["id"]: c for c in json.loads((ROOT / "data" / "test-cases.json").read_text(encoding="utf-8"))}
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    results, controls_ok = [], True
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        for tid, fn in CASES.items():
            ok, obs = fn(real_gate(base))
            bad_ok, bad_obs = fn(naive_gate(base))
            results.append(record(cases[tid], ADAPTER, ok, obs, stamp))
            results.append(record(cases[tid], NAIVE, bad_ok, bad_obs, stamp))
            controls_ok &= (not bad_ok)  # the naive gate must fail every case, or the case does not discriminate
            print(f"{tid:14} gate={'pass' if ok else 'FAIL':4}  naive={'pass (case proves nothing!)' if bad_ok else 'fail (expected)'}")
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / "llmi-t008-gate.json").write_text(json.dumps({"technique": "LLMI-T008", "system_under_test": ADAPTER, "results": results}, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out / 'llmi-t008-gate.json'}")
    return 0 if controls_ok and all(r["result"] == "pass" for r in results if r["adapter"] == ADAPTER) else 1


if __name__ == "__main__":
    raise SystemExit(main())
