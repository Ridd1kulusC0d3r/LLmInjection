#!/usr/bin/env python3
"""pth_audit.py — list .pth files whose import lines Python runs at every start (stdlib only).

DET-AI-054 watches .pth files written *outside* a package install. The malicious agent-framework
1.26.1/1.26.2 (LLMI-20261125-02) and LiteLLM 1.82.8 arrived *through* pip, so the file event is filtered
as a normal install. This audit closes that gap at rest: it reads every .pth in the interpreter's
site-packages and reports the ones with executable `import` lines that are not on an allowlist.

Heuristic layer, not a complete defence; not tested in production. Run it in CI after dependency
install and on build images, and review every non-allowlisted hit.

    python examples/pth_audit.py                  # this interpreter's site-packages
    python examples/pth_audit.py /path/to/venv/lib/python3.12/site-packages
"""

from __future__ import annotations

import json
import re
import site
import sys
from pathlib import Path

# Common, legitimate .pth files that carry import lines. Extend after inventory.
ALLOW = re.compile(r"^(_virtualenv|__editable__\..*|coverage.*|.*-nspkg)\.pth$")
# setuptools' shim (named distutils-precedence.pth or zz-distutils-precedence.pth) is allowed by name AND content,
# so a stealer cannot hide behind the name alone.
SETUPTOOLS_NAME = re.compile(r"^(zz-)?distutils-precedence\.pth$")
SETUPTOOLS_SHIM = re.compile(r"^import os; var = 'SETUPTOOLS_USE_DISTUTILS'; enabled = os\.environ\.get\(var, 'local'\) == 'local'; "
                             r"enabled and __import__\('_distutils_hack'\)\.add_shim\(\);?\s*$")
# File names reported in public write-ups of trojanised AI packages.
KNOWN_BAD = {"agent_framework_meta.pth", "af_runtime_diag.pth", "litellm_init.pth"}
RISKY = re.compile(r"base64|b64decode|exec\(|eval\(|subprocess|urllib|http|socket|os\.environ", re.I)


def audit(dirs: list[Path]) -> list[dict]:
    findings = []
    for d in dirs:
        for pth in sorted(d.glob("*.pth")):
            lines = pth.read_text(encoding="utf-8", errors="replace").splitlines()
            code = [ln for ln in lines if ln.startswith(("import ", "import\t"))]
            if not code or (ALLOW.match(pth.name) and pth.name not in KNOWN_BAD):
                continue
            if SETUPTOOLS_NAME.match(pth.name) and all(SETUPTOOLS_SHIM.match(c) for c in code):
                continue
            findings.append({
                "file": str(pth),
                "verdict": "known-bad" if pth.name in KNOWN_BAD else ("risky" if any(RISKY.search(c) for c in code) else "review"),
                "import_lines": [c[:160] for c in code],
            })
    return findings


def default_dirs() -> list[Path]:
    dirs = [*site.getsitepackages(), site.getusersitepackages()]
    return [Path(d) for d in dict.fromkeys(dirs) if Path(d).is_dir()]


if __name__ == "__main__":
    targets = [Path(a) for a in sys.argv[1:]] or default_dirs()
    result = audit(targets)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(1 if any(f["verdict"] != "review" for f in result) else 0)
