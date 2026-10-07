#!/usr/bin/env python3
"""Package a LLMInjection data release and write its SHA-256 digest."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/"dist"
OUT=DIST/"releases"

INCLUDE_DIRS=["data","schemas"]
INCLUDE_FILES=[
    "LICENSE","CITATION.cff","docs/METHODOLOGY.md","docs/INTELLIGENCE-GRAPH.md",
    "docs/THREAT-LANDSCAPE-2026.md","docs/AI-SUPPLY-CHAIN.md",
]
GENERATED=[
    "dist/graph.json","dist/graph.graphml","dist/llminjection-stix.json",
]

def add(zf,path):
    full=ROOT/path
    if full.exists() and full.is_file():
        zf.write(full,path.as_posix())

def main():
    manifest=json.loads((ROOT/"data"/"dataset-manifest.json").read_text(encoding="utf-8"))
    version=manifest["schema_version"].replace("+","-")
    snapshot=manifest["snapshot"]
    OUT.mkdir(parents=True,exist_ok=True)
    archive=OUT/f"llminjection-intelligence-{snapshot}-schema-{version}.zip"

    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
        for dirname in INCLUDE_DIRS:
            for full in sorted((ROOT/dirname).rglob("*")):
                if full.is_file():
                    zf.write(full,full.relative_to(ROOT).as_posix())
        for value in INCLUDE_FILES+GENERATED:
            add(zf,Path(value))
        api=DIST/"api"
        if api.exists():
            for full in sorted(api.rglob("*")):
                if full.is_file():
                    zf.write(full,full.relative_to(ROOT).as_posix())

    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum=archive.with_suffix(archive.suffix+".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n",encoding="utf-8")
    print(archive)
    print(checksum)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
