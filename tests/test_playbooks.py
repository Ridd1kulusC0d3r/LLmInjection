import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_playbooks as bp  # noqa: E402
from common import load_data  # noqa: E402


class PlaybookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = bp.build_all()

    def test_pages_are_current(self):
        for name, text in self.pages.items():
            self.assertEqual((bp.OUT / name).read_text(encoding="utf-8"), text, f"{name} is stale; run python scripts/build_playbooks.py")

    def test_one_page_per_technique_plus_index(self):
        self.assertEqual(set(self.pages), {f"{t['id']}.md" for t in load_data("techniques")} | {"README.md"})

    def test_every_linked_test_and_detection_appears(self):
        for row in bp.Data().cov.values():
            text = self.pages[f"{row['id']}.md"]
            for tc in row["tests"]:
                self.assertIn(tc, text)
            for d in row["detections"]:
                self.assertIn(d["id"], text)

    def test_limits_state_gaps(self):
        for row in bp.Data().cov.values():
            text = self.pages[f"{row['id']}.md"]
            self.assertIn("## 6. Limits of this page", text)
            if not row["evidence"]:
                self.assertIn("No incident, campaign or vulnerability", text)
            if any(d["implementation"] == "specification" for d in row["detections"]):
                self.assertIn("specifications, not rules", text)

    def test_example_files_exist(self):
        for ex in bp.EXAMPLES.values():
            self.assertTrue((bp.ROOT / ex["code"]).exists())
            self.assertTrue((bp.ROOT / ex["tests"]).exists())
        self.assertIn("agent_tool_gate.py", self.pages["LLMI-T008.md"])

    def test_third_party_skills_are_labelled_link_only(self):
        text = self.pages["LLMI-T008.md"]
        self.assertIn("not ours, link only", text)
        self.assertIn("not affiliated with Anthropic", text)


if __name__ == "__main__":
    unittest.main()
