#!/usr/bin/env python3
"""Fail if any tracked file contains a term listed in references/policy/blocked-terms.txt (stdlib only).

The list holds names that must never be published from this repository. Matching is case-insensitive and
covers file contents and paths; binary files are skipped. The list file itself is the only exemption.

    python scripts/check_blocked_terms.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIST = ROOT / "references" / "policy" / "blocked-terms.txt"


def patterns() -> list[re.Pattern]:
    lines = [ln.strip() for ln in LIST.read_text(encoding="utf-8").splitlines()]
    return [re.compile(ln, re.I) for ln in lines if ln and not ln.startswith("#")]


def tracked() -> list[Path]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    return [ROOT / p for p in out.decode().split("\0") if p]


def scan(files: list[Path] | None = None) -> list[str]:
    pats, hits = patterns(), []
    for f in files if files is not None else tracked():
        if f == LIST or not f.is_file():
            continue
        rel = f.relative_to(ROOT).as_posix()
        hits += [f"{rel}: path matches {p.pattern}" for p in pats if p.search(rel)]
        data = f.read_bytes()
        if b"\0" in data[:4096]:
            continue
        text = data.decode("utf-8", "replace")
        for p in pats:
            for m in p.finditer(text):
                hits.append(f"{rel}:{text.count(chr(10), 0, m.start()) + 1}: matches {p.pattern}")
    return hits


def main() -> int:
    hits = scan()
    for h in hits:
        print(h)
    print(f"blocked terms: {len(hits)} hit(s) in tracked files")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
