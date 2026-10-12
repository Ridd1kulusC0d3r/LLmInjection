import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import atr_cve_candidates as cand  # noqa: E402

INDENTED = """title: "Shell Command-Word Reassembly"
id: ATR-2026-02525
status: "experimental"
references:
  cve:
    - "CVE-2026-29783"
    - CVE-2026-29784
  cwe:
    - "CWE-78"
  owasp_llm:
    - "LLM01:2025"
"""

FLAT = """title: "Tool poisoning"
id: ATR-2026-00100
status: stable
references:
  ghsa:
  - GHSA-6qv9-48xg-fc7f
  external:
  - https://github.com/acme/app/security/advisories/GHSA-6qv9-48xg-fc7f
  cve:
  - CVE-2026-29783
"""

SCALAR = """title: x
id: ATR-2026-00200
references:
  cve: CVE-2025-0001
  cwe: CWE-306
"""


class AtrCveTests(unittest.TestCase):
    def test_parser_reads_all_three_list_styles_and_ignores_other_keys(self):
        a = cand.parse_rule(INDENTED, "excessive-autonomy")
        self.assertEqual(a["cve"], ["CVE-2026-29783", "CVE-2026-29784"])
        b = cand.parse_rule(FLAT, "tool-poisoning")
        self.assertEqual((b["cve"], b["ghsa"]), (["CVE-2026-29783"], ["GHSA-6qv9-48xg-fc7f"]))
        self.assertEqual(cand.parse_rule(SCALAR, "x")["cve"], ["CVE-2025-0001"])
        self.assertIsNone(cand.parse_rule("title: not a rule\n", "x"))

    def test_cwe_ids_are_never_read_as_cves(self):
        self.assertEqual(cand.parse_rule(SCALAR, "x")["ghsa"], [])

    def test_known_identifiers_are_excluded(self):
        rules = [cand.parse_rule(INDENTED, "a"), cand.parse_rule(FLAT, "b"), cand.parse_rule(SCALAR, "c")]
        cited = cand.group_by_cve(rules)
        self.assertEqual(len(cited["CVE-2026-29783"]["rules"]), 2)
        rows = cand.candidates(cited, {"CVE-2026-29784"}, {})
        self.assertEqual({r["cve"] for r in rows}, {"CVE-2026-29783", "CVE-2025-0001"})
        # a rule cites a GHSA we already hold: the CVE it sits with is not new either
        rows = cand.candidates(cited, {"GHSA-6QV9-48XG-FC7F"}, {})
        self.assertNotIn("CVE-2026-29783", {r["cve"] for r in rows})

    def test_score_is_bounded_and_follows_the_documented_formula(self):
        self.assertEqual(cand.score(1, {}), 30)
        self.assertEqual(cand.score(9, {}), 50)
        self.assertEqual(cand.score(1, {"in_cisa_kev": True, "epss": 0.5}), 20 + 10 + 30 + 20)
        self.assertEqual(cand.score(9, {"in_cisa_kev": True, "epss": 1.0}), 100)

    def test_queue_item_has_every_field_the_schema_requires(self):
        import json
        schema = json.loads((Path(__file__).resolve().parents[1] / "schemas" / "research-queue.schema.json").read_text(encoding="utf-8"))
        required = schema["properties"]["items"]["items"]["required"]
        row = cand.candidates(cand.group_by_cve([cand.parse_rule(INDENTED, "a")]), set(), {})[0]
        item = cand.queue_item(row, "2026-10-11T00:00:00Z")
        self.assertEqual(sorted(set(required) - set(item)), [])
        self.assertEqual(item["status"], "candidate")
        self.assertTrue(item["url"].startswith("https://"))
        self.assertIn("lead, not evidence", item["summary"])

    def test_chunked_enrichment_asks_for_small_batches(self):
        seen = []
        original = cand.enrich_cves
        cand.enrich_cves = lambda cves: seen.append(len(cves)) or {c: {} for c in cves}
        try:
            out = cand.enrich_chunked([f"CVE-2026-{i:04d}" for i in range(95)], size=40)
        finally:
            cand.enrich_cves = original
        self.assertEqual(seen, [40, 40, 15])
        self.assertEqual(len(out), 95)


if __name__ == "__main__":
    unittest.main()
