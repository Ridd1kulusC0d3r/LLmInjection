#!/usr/bin/env python3
"""Safe local LLMInjection lab runner.

Defaults to planning and mock adapters. It performs no third-party calls,
does not execute model-generated commands, and ships no jailbreak payloads.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "test-cases.json"

PROFILE_MAP = {
    "all": None,
    "prompt": {"prompt-injection", "data-leakage", "application-security"},
    "rag": {"rag-security", "prompt-injection"},
    "agent": {"agentic-security", "availability"},
    "mcp": {"agentic-protocol"},
    "supply-chain": {"supply-chain"},
    "detection": {"runtime-security", "network-detection"},
}

def load_cases():
    with DATA.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def select_cases(cases, profile):
    categories = PROFILE_MAP[profile]
    return cases if categories is None else [c for c in cases if c.get("category") in categories]

def run_mock(case, adapter):
    result = "pass" if adapter == "mock-secure" else "fail"
    observation = (
        "mock adapter preserved the configured security boundary"
        if result == "pass"
        else "mock adapter intentionally crossed the configured security boundary"
    )
    return {
        "test_case": case["id"],
        "name": case["name"],
        "adapter": adapter,
        "result": result,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "observations": [observation],
        "telemetry_expected": case.get("telemetry", []),
        "controls_expected": case.get("controls", []),
        "framework_mappings": case.get("mappings", []),
        "disclaimer": "Mock result validates runner plumbing only, not a real system security posture.",
    }

def main():
    parser = argparse.ArgumentParser(description="LLMInjection safe local evaluation runner")
    parser.add_argument("--profile", choices=PROFILE_MAP, default="all")
    parser.add_argument("--adapter", choices=["plan", "mock-secure", "mock-insecure"], default="plan")
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument("--list", action="store_true", help="List selected test cases")
    args = parser.parse_args()
    cases = select_cases(load_cases(), args.profile)

    if args.list or args.adapter == "plan":
        payload = {
            "profile": args.profile,
            "adapter": args.adapter,
            "case_count": len(cases),
            "cases": [{"id": c["id"], "name": c["name"], "category": c["category"], "goal": c["goal"], "mode": c["mode"]} for c in cases],
            "note": "Plan mode performs no network requests and no model calls.",
        }
    else:
        payload = {
            "profile": args.profile,
            "adapter": args.adapter,
            "case_count": len(cases),
            "results": [run_mock(c, args.adapter) for c in cases],
        }

    rendered = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(rendered)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
