import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class OpenPromptInjectionMapTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "references" / "crosswalks" / "open-prompt-injection.json").read_text(encoding="utf-8"))
        def load(n):
            return {x["id"] for x in json.loads((ROOT / "data" / f"{n}.json").read_text(encoding="utf-8"))}

        self.controls, self.techniques = load("controls"), load("techniques")

    def test_every_attack_and_defence_is_mapped(self):
        self.assertEqual(self.data["summary"]["unmapped_attacks"], [])
        self.assertEqual(self.data["summary"]["unmapped_defences"], [])
        for d in self.data["defences"] + self.data["detectors"]:
            self.assertTrue(d["controls"], d["name"])

    def test_mapped_ids_exist(self):
        for a in self.data["attacks"]:
            self.assertTrue(set(a["techniques"]) <= self.techniques, a["name"])
        for d in self.data["defences"] + self.data["detectors"]:
            self.assertTrue(set(d["controls"]) <= self.controls, d["name"])

    def test_sources_link_upstream(self):
        for x in self.data["attacks"] + self.data["defences"] + self.data["detectors"]:
            self.assertTrue(x["source"].startswith("https://github.com/liu00222/Open-Prompt-Injection/"), x["name"])


if __name__ == "__main__":
    unittest.main()
