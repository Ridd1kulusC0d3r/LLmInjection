import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "references" / "crosswalks" / "payload-vault.json"


class PayloadVaultTests(unittest.TestCase):
    """The vault declares no licence, so the crosswalk must never carry payload text."""

    def setUp(self):
        self.data = json.loads(CROSSWALK.read_text(encoding="utf-8"))

    def test_items_hold_ids_labels_and_hashes_only(self):
        for item in self.data["items"]:
            self.assertEqual(set(item), {"library", "id", "category", "label", "sha256"}, item["id"])
            self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$")
            self.assertLessEqual(len(item["label"]), 60, item["id"])

    def test_every_category_maps_to_known_techniques(self):
        known = {t["id"] for t in json.loads((ROOT / "data" / "techniques.json").read_text(encoding="utf-8"))}
        self.assertEqual(self.data["summary"]["unmapped_categories"], [])
        for cat in self.data["categories"]:
            self.assertTrue(cat["techniques"], cat["category"])
            self.assertLessEqual(set(cat["techniques"]), known, cat["category"])
        self.assertEqual(sum(c["total"] for c in self.data["categories"]), self.data["summary"]["payloads"])

    def test_every_control_has_a_layer(self):
        controls = json.loads((ROOT / "data" / "controls.json").read_text(encoding="utf-8"))
        self.assertLessEqual({c["layer"] for c in controls}, {"guardrail", "hardening", "monitoring"})


if __name__ == "__main__":
    unittest.main()
