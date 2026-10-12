"""The safe-lab test cases of playbook LLMI-T008, as executable assertions against examples/agent_tool_gate.py."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))

import agent_tool_gate as g  # noqa: E402

ACCOUNTS = {"acct-1": "alice", "acct-2": "bob"}


def make_gate(base: Path, approve: bool = False) -> g.Gate:
    return g.Gate(
        tools={
            "calc": g.Tool("calc", lambda expression: g.arithmetic_only(expression), validate=lambda p: g.arithmetic_only(str(p.get("expression", "")))),
            "read_note": g.Tool("read_note", lambda path: (base / path).name, validate=g.inside(base)),
            "fetch": g.Tool("fetch", lambda url: "ok", side_effect=True, validate=g.public_https_host({"example.org"})),
            "pay": g.Tool("pay", lambda from_account, amount: "sent", side_effect=True, high_impact=True,
                          owner_of=lambda p: ACCOUNTS.get(p.get("from_account")), params=frozenset({"from_account", "amount"})),
        },
        approver=lambda tool, params: approve,
    )


class AgentToolGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.gate = make_gate(self.base)
        self.alice = g.Caller("alice")

    def tearDown(self):
        self.tmp.cleanup()

    def test_tc_mcp_010_a_capability_nobody_registered_does_not_exist(self):
        d = self.gate.call(self.alice, "shell", {"cmd": "id"})
        self.assertEqual((d.allowed, d.reason), (False, "not-allowlisted"))

    def test_tc_ag_005_untrusted_content_cannot_trigger_a_side_effect(self):
        d = self.gate.call(self.alice, "fetch", {"url": "https://example.org/x"}, origin=g.UNTRUSTED)
        self.assertEqual((d.allowed, d.reason), (False, "side-effect-from-untrusted-origin"))
        self.assertTrue(self.gate.call(self.alice, "fetch", {"url": "https://example.org/x"}, origin=g.USER_TURN).allowed)

    def test_tc_param_019_model_supplied_parameters_are_rejected_before_use(self):
        bad_expr = self.gate.call(self.alice, "calc", {"expression": "__import__('os').system('id')"})
        bad_path = self.gate.call(self.alice, "read_note", {"path": "../../etc/passwd"})
        self.assertTrue(bad_expr.reason.startswith("invalid-parameters"))
        self.assertTrue(bad_path.reason.startswith("invalid-parameters"))
        self.assertEqual(self.gate.call(self.alice, "calc", {"expression": "2 * (3 + 4)"}).result, 14)
        smuggled = self.gate.call(self.alice, "pay", {"from_account": "acct-1", "amount": 1, "approved": True})   # an undeclared parameter
        self.assertTrue(smuggled.reason.startswith("invalid-parameters"))

    def test_tc_authz_029_the_caller_identity_decides_not_the_models_claim(self):
        params = {"from_account": "acct-2", "amount": 5}          # alice names bob's account
        self.assertEqual(self.gate.call(self.alice, "pay", params).reason, "object-owner-mismatch")
        admin = g.Caller("carol", frozenset({"admin"}))
        self.assertEqual(self.gate.call(admin, "pay", params).reason, "pending-human-approval")  # allowed to ask, still needs a person

    def test_tc_tool_030_private_and_link_local_destinations_are_refused(self):
        for url in ("https://169.254.169.254/latest", "https://127.0.0.1/admin", "https://10.0.0.5/", "http://example.org/", "https://evil.example/"):
            d = self.gate.call(self.alice, "fetch", {"url": url})
            self.assertFalse(d.allowed, url)

    def test_tc_ag_006_a_high_impact_action_parks_until_a_person_approves(self):
        params = {"from_account": "acct-1", "amount": 100}
        self.assertEqual(self.gate.call(self.alice, "pay", params).reason, "pending-human-approval")
        approved = make_gate(self.base, approve=True)
        self.assertTrue(approved.call(self.alice, "pay", params).allowed)

    def test_every_decision_is_audited_with_the_fields_the_test_cases_name(self):
        self.gate.call(self.alice, "shell", {})
        self.gate.call(self.alice, "calc", {"expression": "1+1"})
        self.assertEqual(len(self.gate.audit), 2)
        for row in self.gate.audit:
            self.assertEqual({"tool-request", "caller-identity", "authorization-result", "reason", "tool-result"}, set(row))
        self.assertIsNone(self.gate.audit[0]["tool-result"])
        json.dumps(self.gate.audit)  # serialisable, so it can go to a log pipeline

    def test_the_test_cases_this_example_covers_exist_in_the_dataset(self):
        ids = {c["id"] for c in json.loads((ROOT / "data" / "test-cases.json").read_text(encoding="utf-8"))}
        self.assertLessEqual({"TC-MCP-010", "TC-AG-005", "TC-PARAM-019", "TC-AUTHZ-029", "TC-TOOL-030", "TC-AG-006"}, ids)


if __name__ == "__main__":
    unittest.main()
