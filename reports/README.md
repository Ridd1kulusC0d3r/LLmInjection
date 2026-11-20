# Generated Intelligence Reports

LLMInjection produces review-oriented intelligence reports from the structured datasets.

## Intake

`reports/intake/latest.md` is created when the daily living-intelligence collector finds new review candidates.

## Monthly landscape

Monthly automation creates:

```text
YYYY-MM.md
YYYY-MM-diff.json
YYYY-MM-diff.md
```

The monthly report summarizes dataset state, entity-level change and unresolved research candidates. It does not convert queue candidates into confirmed intelligence.

## Templates

[`reports/templates/`](templates/README.md) holds the four product skeletons (intelligence report, monthly landscape, weekly trends, dossier) in the site's analyst-desk style, with their mastheads in `assets/reports/` (`scripts/build_report_mastheads.py`).
