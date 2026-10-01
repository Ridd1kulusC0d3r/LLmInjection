#!/usr/bin/env python3
"""Build a versioned, static read-only API from validated LLMInjection datasets."""

from __future__ import annotations
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
DIST=ROOT/"dist"
API=DIST/"api"/"v1"

FILES=[
    "actors.json","campaigns.json","incidents.json","techniques.json","models.json",
    "frameworks.json","test-cases.json","controls.json","detections.json","sources.json",
    "relationships.json","vulnerabilities.json","threat-landscape-2026.json",
]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    API.mkdir(parents=True,exist_ok=True)
    endpoints=[]
    for filename in FILES:
        src=DATA/filename
        dst=API/filename
        shutil.copyfile(src,dst)
        obj=load(src)
        count=len(obj) if isinstance(obj,list) else len(obj.get("key_metrics",[]))
        endpoints.append({"name":filename.removesuffix(".json"),"path":filename,"records":count})

    for filename in ("graph.json","llminjection-stix.json"):
        src=DIST/filename
        if not src.exists():
            raise SystemExit(f"missing {src}; run scripts/build_graph.py first")
        shutil.copyfile(src,API/filename)

    manifest=load(DATA/"dataset-manifest.json")
    index={
        "api_version":"v1",
        "dataset":manifest,
        "endpoints":endpoints,
        "generated_exports":["graph.json","llminjection-stix.json"],
        "note":"Static read-only API generated from CI-validated repository data."
    }
    (API/"index.json").write_text(json.dumps(index,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Built static API with {len(endpoints)} dataset endpoints at {API}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
