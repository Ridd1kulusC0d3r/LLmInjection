#!/usr/bin/env python3
"""Check whether curated sources and actor records need re-verification."""

from __future__ import annotations
import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def age_days(value):
    return (date.today() - date.fromisoformat(value)).days

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--warn-days",type=int,default=90)
    p.add_argument("--fail-days",type=int,default=180)
    args=p.parse_args()
    stale=[]
    for src in load(ROOT/"data"/"sources.json"):
        age=age_days(src["last_verified"])
        if age>=args.warn_days:
            stale.append(("source",src["id"],age))
    for actor in load(ROOT/"data"/"actors.json"):
        age=age_days(actor["last_verified"])
        if age>=args.warn_days:
            stale.append(("actor",actor["id"],age))
    for kind,rid,age in sorted(stale,key=lambda x:-x[2]):
        print(f"{kind:6} {rid:40} {age:4} days since verification")
    failures=[x for x in stale if x[2]>=args.fail_days]
    if failures:
        print(f"FAILED: {len(failures)} records exceed {args.fail_days} days")
        return 1
    print(f"OK: {len(stale)} records at or above warning threshold; none exceed fail threshold")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
