import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import enrich_ai_sources as enrich  # noqa: E402


class EnrichmentTests(unittest.TestCase):
    def test_safe_url(self):
        with self.assertRaises(ValueError):
            enrich.checked_url("https://api.github.com.attacker.invalid/repo")
        with self.assertRaises(ValueError):
            enrich.checked_url("http://api.osv.dev/v1/vulns/CVE-2026-12345")
        self.assertEqual(enrich.checked_url("https://api.osv.dev/v1/vulns/CVE-2026-12345"),
                         "https://api.osv.dev/v1/vulns/CVE-2026-12345")

    def test_avid_filename_is_not_incident(self):
        src = {"adapter": "avid-list"}
        data = [{"name": "AVID-2026-R0001.json", "path": "reports/2026/test.json",
                 "html_url": "https://github.com/avidml/avid-db/blob/main/reports/2026/test.json",
                 "type": "file"}]
        found = list(enrich.candidates_from(src, data, 1))
        self.assertEqual(found[0]["kind"], "report-discovery")

    def test_mcp_list_metadata_only(self):
        src = {"adapter": "mcp-list"}
        data = {"servers": [{"server": {"name": "example/test", "repository": {
            "url": "https://github.com/example/test"}}}]}
        found = list(enrich.candidates_from(src, data, 1))
        self.assertEqual(found[0]["kind"], "mcp-inventory")
        self.assertNotIn("verified secure", found[0]["summary"])

    def test_veris_stays_secondary(self):
        src = {"adapter": "veris-json", "id": "AISRC-VERIS-2026", "source_grade": "D"}
        data = {"incidents": [{"id": "DR-0001", "title": "Synthetic case"}]}
        record = next(enrich.candidates_from(src, data, 1))
        result = enrich.candidate(src, record, "2026-10-09T12:00:00Z")
        self.assertEqual(result["status"], "candidate")
        self.assertEqual(result["kind"], "secondary-incident-discovery")

    def test_merge_preserves_review(self):
        old = {"id": "RQ-AI-1", "evidence_sha256": "old", "status": "reviewing",
               "review": {"notes": "reviewed"}, "observed_at": "first"}
        new = {"id": "RQ-AI-1", "evidence_sha256": "new", "status": "candidate",
               "review": {}, "observed_at": "second"}
        result, added, changed = enrich.merge({"meta": {}, "items": [old]}, [new])
        self.assertEqual((added, changed), (0, 1))
        self.assertEqual(result["items"][0]["status"], "reviewing")
        self.assertEqual(result["items"][0]["review"]["notes"], "reviewed")

    def test_offline_collection_never_calls_network(self):
        src = {"id": "AISRC-AVID-REPORTS", "enabled": True, "adapter": "avid-list",
               "source_grade": "A", "url": "https://api.github.com/unused"}
        fixture = {"AISRC-AVID-REPORTS": []}
        found, errors = enrich.collect([src], fixtures=fixture, fetcher=lambda url:
                                       self.fail("unexpected network"))
        self.assertEqual(found, [])
        self.assertEqual(errors, [])

    def test_osv_local_only_existing_ids(self):
        src = {"adapter": "osv-local"}
        known = [{"identifiers": ["CVE-2026-12345", "not-an-id"]}]
        payload = {"CVE-2026-12345": {"id": "GHSA-abcd-efgh-ijkl", "summary": "Sample"}}
        result = list(enrich.candidates_from(src, payload, 3, known_vulns=known,
                                             fetcher=lambda url: self.fail("network")))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["kind"], "vulnerability-enrichment")


if __name__ == "__main__":
    unittest.main()
