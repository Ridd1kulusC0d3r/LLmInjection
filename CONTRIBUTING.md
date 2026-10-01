# Contributing to LLMInjection

LLMInjection accepts contributions that improve the evidence base for AI/LLM cyber threat intelligence.

## What we want

- Primary-source threat reporting.
- New or corrected actor/campaign records.
- Framework mappings and crosswalk corrections.
- Detection ideas tied to observable telemetry.
- Defensive benchmarks and evaluation methods.
- Model, agent, RAG, MCP/A2A and AI supply-chain security research.
- Reproducible lab notes that do not depend on attacking third-party systems.

## Evidence requirements

Every factual contribution should provide:

1. **Claim** — one concise statement.
2. **Source** — URL to the best available source.
3. **Source date** — publication date if known.
4. **Observation type** — observed, assessed, inferred or unverified.
5. **Confidence** — confirmed, high, medium, low or unverified.
6. **Last verified** — YYYY-MM-DD.
7. **Framework mapping** — when a relevant mapping exists.

Prefer primary sources (vendor incident reports, government publications, project advisories, original papers) over aggregators.

## Attribution discipline

Do not merge aliases merely because two reports mention similar behavior. Threat actor naming is messy enough without us manufacturing certainty.

When attribution differs between sources:

- retain each vendor's name;
- describe the claimed overlap;
- identify the source making the assessment;
- do not silently normalize disputed aliases.

## Safe research

This repository documents offensive techniques for defensive understanding and authorized security evaluation. Contributions should emphasize threat models, observable behaviors, detections, mitigations and controlled testing.

Do not submit stolen credentials, private victim data, secrets, live access tokens or instructions intended to compromise third-party systems.

## Data changes

Machine-readable intelligence lives in `data/`. Run:

```bash
python scripts/validate_intel.py
```

before opening a pull request.

## Pull request checklist

- [ ] I linked primary sources where available.
- [ ] I separated observed facts from analyst assessment.
- [ ] I assigned a confidence value.
- [ ] I added or corrected framework mappings.
- [ ] I updated `last_verified`.
- [ ] I did not include victim-sensitive data or secrets.
- [ ] `python scripts/validate_intel.py` passes.
