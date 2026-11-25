import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))

import pth_audit  # noqa: E402


class PthAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        (self.dir / name).write_text(text, encoding="utf-8")

    def test_path_only_and_allowlisted_files_are_ignored(self):
        self.write("mypkg.pth", "/opt/mypkg/src\n")
        self.write("zz-distutils-precedence.pth",
                   "import os; var = 'SETUPTOOLS_USE_DISTUTILS'; enabled = os.environ.get(var, 'local') == 'local'; "
                   "enabled and __import__('_distutils_hack').add_shim(); \n")
        self.assertEqual(pth_audit.audit([self.dir]), [])

    def test_setuptools_name_with_other_content_is_not_allowed(self):
        self.write("distutils-precedence.pth", "import os; os.environ.get('AZURE_CLIENT_SECRET')\n")
        [f] = pth_audit.audit([self.dir])
        self.assertEqual(f["verdict"], "risky")

    def test_known_bad_name_is_flagged(self):
        # Harmless stand-in: only the file name matters for this verdict.
        self.write("agent_framework_meta.pth", "import sys\n")
        [f] = pth_audit.audit([self.dir])
        self.assertEqual(f["verdict"], "known-bad")

    def test_unknown_import_line_with_network_or_decode_is_risky(self):
        self.write("helper.pth", "import base64, os; os.environ.get('X')\n")
        self.write("plain.pth", "import sys\n")
        verdicts = {Path(f["file"]).name: f["verdict"] for f in pth_audit.audit([self.dir])}
        self.assertEqual(verdicts, {"helper.pth": "risky", "plain.pth": "review"})


if __name__ == "__main__":
    unittest.main()
