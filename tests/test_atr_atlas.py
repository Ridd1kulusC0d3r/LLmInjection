import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import atr_atlas_check as chk  # noqa: E402

ATLAS = """format-version: 6.0.0
collection:
  version: '2026.09'
techniques:
  AML.T0053:
    name: AI Agent Tool Invocation
    maturity: Realized
    id: AML.T0053
  AML.T0051.001:
    name: Indirect
    maturity: Realized
  AML.T0020:
    name: Training Data Poisoning
    maturity: Realized
mitigations:
  AML.M0000:
    name: Not a technique
case-studies:
  AML.CS0041:
    name: Rules File Backdoor
"""

RULE = """title: Example
id: ATR-2026-09999
status: "experimental"
references:
  owasp_llm:
    - "LLM01:2025"
  mitre_atlas:
    - "AML.T0053 - LLM Plugin Compromise"
    - "AML.T0051.001 - LLM Prompt Injection: Indirect"
    - "AML.T0020 - Training Data Poisoning"
    - "AML.T0104 - Publish Poisoned AI Agent Tool"
    - "AML.CS0041 - Rules File Backdoor"
  cve:
    - CVE-2026-0001
"""


class AtrAtlasTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "ATLAS-latest.yaml"
        path.write_text(ATLAS, encoding="utf-8")
        self.version, self.atlas = chk.parse_atlas(path)
        self.rule = chk.parse_atr_rule(RULE)

    def tearDown(self):
        self.tmp.cleanup()

    def test_atlas_parser_reads_techniques_and_case_studies_only(self):
        self.assertEqual(self.version, "2026.09")
        self.assertEqual(sorted(self.atlas), ["AML.CS0041", "AML.T0020", "AML.T0051.001", "AML.T0053"])
        self.assertEqual(self.atlas["AML.T0053"]["name"], "AI Agent Tool Invocation")

    def test_rule_parser_keeps_id_and_atr_label(self):
        self.assertEqual(self.rule["id"], "ATR-2026-09999")
        self.assertEqual(self.rule["atlas"][0], ("AML.T0053", "LLM Plugin Compromise"))
        self.assertIsNone(chk.parse_atr_rule("title: not a rule\n"))

    def test_statuses(self):
        self.rule["category"] = "tool-poisoning"
        rows = {r["atlas_id"]: r for r in chk.analyse([self.rule], self.atlas, {"AML.T0104": {"release": "2026.06", "name": "Publish Poisoned AI Agent Tool"}})}
        self.assertEqual(rows["AML.T0053"]["status"], "renamed")        # ATR still says "LLM Plugin Compromise"
        self.assertEqual(rows["AML.T0051.001"]["status"], "ok")         # parent-qualified label is not a rename
        self.assertEqual(rows["AML.T0020"]["status"], "ok")
        self.assertEqual(rows["AML.T0104"]["status"], "unknown-id")
        self.assertEqual(rows["AML.T0104"]["last_seen"]["release"], "2026.06")
        self.assertEqual(rows["AML.CS0041"]["status"], "case-study")

    def test_our_mappings_exist_in_atlas_names_aside(self):
        # run against the real dataset with a fake ATLAS: everything is "missing", which proves the check reports instead of crashing
        problems = chk.check_ours(self.atlas)
        self.assertTrue(all(p["problem"] in ("missing-in-atlas", "name-differs") for p in problems))


if __name__ == "__main__":
    unittest.main()
