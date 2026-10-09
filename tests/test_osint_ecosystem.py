import sys
import unittest
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import osint_ecosystem as oe  # noqa: E402

ENTRY = {"id": "ECO-900", "owner": "acme", "name": "redteam"}


def fake(project=True, advisories=2, verified=True):
    def get(url, body):
        if "packageversions" in url:
            return {"versions": [
                {"versionKey": {"system": "PYPI", "name": "redteam", "version": "1"}, "relationType": "SOURCE_REPO", "attestations": [{"verified": verified}]},
                {"versionKey": {"system": "PYPI", "name": "unrelated", "version": "1"}, "relationType": "DEPENDENCY", "attestations": []},
                {"versionKey": {"system": "DOCKER", "name": "img", "version": "1"}, "relationType": "SOURCE_REPO", "attestations": []},
            ]}
        if url.startswith(oe.OSV):
            assert body["package"] == {"name": "redteam", "ecosystem": "PyPI"}
            return {"vulns": [{"id": f"GHSA-{i}"} for i in range(advisories)]}
        return {"starsCount": 10, "forksCount": 2, "openIssuesCount": 1} if project else None
    return get


class OsintEcosystemTests(unittest.TestCase):
    def test_signals_use_only_source_repo_packages_with_an_osv_ecosystem(self):
        sig = oe.project_signals(ENTRY, fake())
        self.assertEqual((sig["stars"], sig["forks"], sig["open_issues"]), (10, 2, 1))
        self.assertEqual([p["name"] for p in sig["packages"]], ["redteam"])
        self.assertEqual(sig["packages"][0]["advisories"], 2)
        self.assertTrue(sig["slsa_verified"])

    def test_unverified_attestation_is_not_counted(self):
        self.assertFalse(oe.project_signals(ENTRY, fake(verified=False))["slsa_verified"])

    def test_unknown_project_is_none(self):
        self.assertIsNone(oe.project_signals(ENTRY, fake(project=False)))

    def test_collect_separates_unknown_from_network_errors(self):
        def get(url, body):
            if "bad" in url:
                raise urllib.error.URLError("down")
            return fake(project="redteam" in url)(url, body)
        entries = [ENTRY, {"id": "ECO-901", "owner": "acme", "name": "nothing"}, {"id": "ECO-902", "owner": "acme", "name": "bad"}]
        model = oe.collect(entries, get, today="2026-10-09", workers=1)
        self.assertEqual(sorted(model["entries"]), ["ECO-900"])
        self.assertEqual(model["not_found"], ["ECO-901"])
        self.assertEqual(model["errors"], ["ECO-902"])

    def test_report_lists_advisories_and_provenance(self):
        model = oe.collect([ENTRY], fake(), today="2026-10-09", workers=1)
        text = oe.report(model, [ENTRY])
        self.assertIn("acme/redteam", text)
        self.assertIn("2 advisory", text)


if __name__ == "__main__":
    unittest.main()
