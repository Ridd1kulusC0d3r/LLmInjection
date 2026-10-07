import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_navigator  # noqa: E402


class NavigatorTests(unittest.TestCase):
    def setUp(self):
        self.layers = build_navigator.build_layers()

    def test_layer_shape(self):
        for name, layer in self.layers.items():
            self.assertEqual(layer["versions"]["layer"], "4.5", name)
            self.assertTrue(layer["techniques"], name)
            for t in layer["techniques"]:
                self.assertIn(t["score"], range(4), t["techniqueID"])
                self.assertTrue(t["comment"])

    def test_scores_follow_coverage(self):
        atlas = {t["techniqueID"]: t for t in self.layers["atlas-coverage.layer.json"]["techniques"]}
        self.assertIn("AML.T0051.000", atlas)
        self.assertGreaterEqual(atlas["AML.T0051.000"]["score"], 1)


if __name__ == "__main__":
    unittest.main()
