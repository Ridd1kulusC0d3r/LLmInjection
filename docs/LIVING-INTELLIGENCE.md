# Living Intelligence Pipeline

LLMInjection treats AI threat intelligence as a **continuous evidence process**, not a periodically rewritten README.

## Operating model

```text
allow-listed primary sources
          ↓
automated metadata collection
          ↓
deduplication + relevance scoring
          ↓
research queue
          ↓
human evidence review
          ↓
promotion into structured CTI
          ↓
graph / STIX / API
          ↓
snapshot
          ↓
entity-level diff
          ↓
monthly landscape report
```

Collection is automated. **Promotion is not.**

The intake pipeline cannot create or modify official actor attribution, campaign intelligence, incidents, technique mappings, vulnerabilities, relationships or landscape metrics by itself.

## Daily intake

Workflow:

`.github/workflows/intelligence-intake.yml`

Schedule: daily.

The job reads `data/source-feeds.json` and collects metadata from enabled feeds. New items are normalized into `data/research-queue.json`.

If no new candidates are found, no PR is created.

If new candidates are found, the workflow updates a dedicated automation branch and opens or refreshes a review PR.

### Initial monitored feeds

| Feed | Role |
|---|---|
| MITRE ATLAS releases | canonical behavior / case-study changes |
| OWASP GenAI LLM Top 10 repository | canonical application-risk changes |
| Model Context Protocol releases | protocol/security evolution |
| GitHub Advisory Database | reviewed vulnerabilities |
| GitHub malware advisories | malicious-package intelligence |
| CISA KEV | authoritative exploited-vulnerability prioritization |

The registry is intentionally explicit. Arbitrary URLs are not fetched simply because a model decided they looked interesting.

## Research queue

`data/research-queue.json` is **not** an intelligence database.

It contains review candidates with:

- source feed;
- source grade;
- publication timestamp;
- candidate type;
- relevance score;
- matched terms;
- extracted CVE/GHSA/ATLAS/OWASP identifiers;
- review status;
- analyst notes.

Statuses:

`candidate → reviewing → accepted / rejected / duplicate`

An accepted queue item still needs to be represented correctly in the relevant official dataset.

## Relevance scoring

Scoring is transparent and intentionally simple.

Canonical framework/repository feeds receive maximum intake priority because they are already allow-listed by role.

Broad feeds such as advisories or KEV require AI/LLM/agent/MCP-related keyword matches. Identifiers such as CVE or GHSA increase triage priority.

The score is a **review-priority signal**, not analytic confidence.

## Monthly snapshots

Workflow:

`.github/workflows/landscape-snapshot.yml`

A monthly run generates:

```text
data/snapshots/YYYY-MM.json
reports/monthly/YYYY-MM.md
reports/monthly/YYYY-MM-diff.json
reports/monthly/YYYY-MM-diff.md
```

Snapshots include stable entity IDs and SHA-256 fingerprints for each structured object.

The diff engine therefore distinguishes:

- **added** objects;
- **removed** objects;
- **changed** objects.

This lets LLMInjection answer “what changed?” without pretending that a modified paragraph is a new threat.

## Explorer integration

The Pages build generates a current snapshot and compares it to the latest committed monthly baseline.

The Explorer exposes this as **What’s New**.

The diff is also published as:

```text
/intelligence-diff.json
/intelligence-diff.md
/current-snapshot.json
```

## Failure behavior

A temporary feed failure:

- is recorded in the intake report;
- does not promote stale or partial data;
- emits a workflow warning;
- does not convert missing evidence into a negative finding.

If a source disappears permanently, its registry entry should be disabled only after review.

## Promotion checklist

Before a candidate becomes official intelligence, verify:

1. Is the source primary or otherwise appropriate for the claim?
2. Is the candidate an observed fact, an assessment, research, or a proof of concept?
3. Does an existing object already represent it?
4. Are actor aliases and attribution claims explicitly supported?
5. Is the external framework mapping exact or only related?
6. Is confidence independent from source grade?
7. Are time window and affected population preserved?
8. Does the object need relationships, detections, tests or controls?
9. Does the change belong in the intelligence changelog?

## Design principle

The collector is allowed to be fast.

The intelligence layer is required to be careful.

## Daily digest intake

The scheduled daily digest ("Threat Landscape IA") reads sources every morning, but its edition used to stay in the run's output folder and never reached the datasets. It now feeds the research queue:

1. The task writes, next to its Markdown edition, `intake/digests/YYYY-MM-DD.json` (shape below) and opens a pull request with it.
2. `python scripts/import_digest.py intake/digests/YYYY-MM-DD.json` turns each item into a `candidate` under `FEED-LLMI-DAILY-DIGEST`. Unconfirmed items and URLs already queued or held are skipped.
3. An analyst reads the primary source and promotes with `scripts/merge_promotions.py`, or rejects with a reason.
4. Weekly trends and the monthly landscape (`reports/templates/`) are written from the queue and the datasets, and their open questions become the next month's searches.

Each item carries its own `source_grade` (the analyst's grade for that source, per [SOURCE-GRADING.md](SOURCE-GRADING.md)), so the queue no longer grades everything D.

```json
{"digest_id": "LLMI-20261120", "date": "2026-11-20", "producer": "...", "window": "...",
 "items": [{"id": "LLMI-20261120-01", "title": "...", "url": "https://...", "published": "2026-11-20",
            "seal": "original | secondary | unconfirmed", "temporal": "new | update | retrospective | recovered",
            "source_grade": "A-E", "kind": "vulnerability | threat-report | research | regulation",
            "techniques": ["LLMI-T001"], "identifiers": ["CVE-..."], "summary": "...", "brazil_latam": false}]}
```

**More than one file per day.** The scheduled edition keeps the plain name `YYYY-MM-DD.json`. Any other batch for the same day takes a suffix and a matching `digest_id`: `-report`/`-REPORT` (an authored report's source list), `-spectrum`/`-SPECTRUM` (references cited by one article), and `-ampliado`/`-AMPLIADO` (the analyst's expanded edition of that day's digest, which repeats the scheduled items and adds backfill). An expanded edition may carry reader-only fields: `notes`, `companion_of`, per-item `analyst_context` (ATLAS, OWASP, ATT&CK, IOCs, defensive action, gaps), `companion` (detections, validators, proposals, hunting hypothesis, OSINT note made from that day), `agent_reports`, `not_included` and `sources_consulted`. `import_digest.py` ignores those fields and skips URLs already queued, and `build_weekly.py` counts each item ID once, so keeping both files does not duplicate anything. Example: `intake/digests/2026-11-21.json` (5 items) and `intake/digests/2026-11-21-ampliado.json` (13 items).

### Text to add to the scheduled task's prompt

> 5. Besides the Markdown edition, write `intake/digests/AAAA-MM-DD.json` in the shape described in `docs/LIVING-INTELLIGENCE.md` ("Daily digest intake"): one entry per item of section B, with the item's ID, the seal mapped to `original`, `secondary` or `unconfirmed`, and the source grade A–E from `docs/SOURCE-GRADING.md`. Clone the repository, add the file on a branch `digest/AAAA-MM-DD`, run `python scripts/import_digest.py` and `make check`, and open a pull request. Never promote into `data/` beyond the research queue.
