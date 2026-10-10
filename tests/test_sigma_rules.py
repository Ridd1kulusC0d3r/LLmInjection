import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGMA = ROOT / "detections" / "sigma"
UUID = re.compile(r"^id: ([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$", re.M)


class SigmaRuleTests(unittest.TestCase):
    def test_every_rule_names_its_detection_and_is_experimental(self):
        import json
        known = {d["id"] for d in json.loads((ROOT / "data" / "detections.json").read_text(encoding="utf-8"))}
        files = sorted(SIGMA.glob("det-ai-*.yml"))
        self.assertGreaterEqual(len(files), 4)
        for path in files:
            det = "-".join(path.name.split("-")[:3]).upper()
            text = path.read_text(encoding="utf-8")
            self.assertIn(det, known, path.name)
            self.assertIn(f"llminjection.{det.lower()}", text, path.name)
            self.assertNotIn("status: stable", text)
            self.assertIn("status: experimental", text)

    def test_rule_ids_are_unique_uuid4(self):
        ids = [i for p in SIGMA.glob("*.yml") for i in UUID.findall(p.read_text(encoding="utf-8"))]
        self.assertEqual(len(ids), len(set(ids)))

    def test_auto_approve_patterns_match_documented_flags_only(self):
        text = (SIGMA / "det-ai-032-agent-approval-disabled.yml").read_text(encoding="utf-8")
        patterns = re.findall(r"^\s+- '([^']+)'$", text.split("detection:")[1].split("condition:")[0], re.M)

        def hit(cmd):
            return any(p in cmd for p in patterns)

        for cmd in ("claude --dangerously-skip-permissions", "claude --permission-mode=bypassPermissions -p x", "gemini --approval-mode yolo", "gemini --yolo"):
            self.assertTrue(hit(cmd), cmd)
        for cmd in ("claude --permission-mode plan --allow-dangerously-skip-permissions", "claude -p hello", "npm install -y left-pad", "gemini -y"):
            self.assertFalse(hit(cmd), cmd)


if __name__ == "__main__":
    unittest.main()
