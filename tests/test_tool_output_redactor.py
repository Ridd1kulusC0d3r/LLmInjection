"""Assertions for examples/tool_output_redactor.py and the IPv6 gap fix in examples/agent_tool_gate.py (digest 2026-11-25)."""

import ipaddress
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))

import agent_tool_gate as gate  # noqa: E402
import tool_output_redactor as r  # noqa: E402

TASK_DEF = {"containerDefinitions": [{"name": "web",
    "environment": [{"name": "DB_PASSWORD", "value": "hunter2"}, {"name": "REGION", "value": "sa-east-1"},
                    {"name": "NOTE", "value": "key AKIAABCDEFGHIJKLMNOP and postgres://app:pw@db:5432/x"}],
    "secrets": [{"name": "API_TOKEN", "valueFrom": "arn:aws:ssm:sa-east-1:111122223333:parameter/tok"}]}]}


class RedactorTests(unittest.TestCase):
    def test_ecs_task_definition_secrets_are_masked(self):
        clean, count = r.redact(TASK_DEF)
        env = clean["containerDefinitions"][0]["environment"]
        self.assertEqual(env[0]["value"], r.MASK)
        self.assertEqual(env[1]["value"], "sa-east-1")
        self.assertNotIn("AKIA", env[2]["value"])
        self.assertNotIn("app:pw@", env[2]["value"])
        self.assertEqual(clean["containerDefinitions"][0]["secrets"][0]["valueFrom"], r.MASK)
        self.assertEqual(count, 4)

    def test_benign_output_is_unchanged(self):
        data = {"name": "service", "status": "RUNNING", "tasks": [1, 2], "url": "https://example.org/a"}
        self.assertEqual(r.redact(data), (data, 0))

    def test_secret_named_keys_and_shapes(self):
        clean, count = r.redact(["ok", {"token": "abc"}, "ghp_" + "A" * 36])
        self.assertEqual(clean, ["ok", {"token": r.MASK}, r.MASK])
        self.assertEqual(count, 2)


class FetchGuardIPv6Tests(unittest.TestCase):
    """GHSA-3rxj-6jhw-qfv7: ipaddress calls fec0::/10 and ::ffff:0:0:0/96 global; the gate must not."""

    def test_non_public_addresses_are_refused(self):
        for a in ("fec0::1", "::ffff:0:a00:1", "::ffff:10.0.0.1", "169.254.169.254", "fd00::1", "::1"):
            self.assertTrue(gate.non_public(ipaddress.ip_address(a)), a)

    def test_public_addresses_pass(self):
        for a in ("8.8.8.8", "2606:4700::1", "::ffff:8.8.8.8"):
            self.assertFalse(gate.non_public(ipaddress.ip_address(a)), a)

    def test_fetch_validator_rejects_site_local_literal(self):
        check = gate.public_https_host({"example.org"})
        with self.assertRaisesRegex(ValueError, "private"):
            check({"url": "https://[fec0::1]/latest/meta-data/"})


if __name__ == "__main__":
    unittest.main()
