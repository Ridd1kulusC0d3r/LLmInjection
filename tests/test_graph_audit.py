import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import audit_graph  # noqa: E402


class GraphAuditTests(unittest.TestCase):
    def test_no_orphaned_records(self):
        findings = audit_graph.audit()
        for name in audit_graph.HARD:
            self.assertEqual(findings[name], [], name)


if __name__ == "__main__":
    unittest.main()
