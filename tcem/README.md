# TCEM threat models

Threat models built with **TCEM, the Threat Context Engineering Method**
([Cyber-Threat-Context-Modeling](https://github.com/Ridd1kulusC0d3r/Cyber-Threat-Context-Modeling), v0.5.1).
TCEM is by the same author as this repository: citing it describes the method used here and is not independent
validation.

Each case under `cases/` is one TCEM single-document case (`case.json`) with its crown jewel, threat context,
attack path, telemetry contract, detection specification, safe log-replay validation, intelligence gaps and
decisions, plus `fixtures/events.jsonl`, synthetic defensive events with no payloads. Fields TCEM does not define
(`llminjection_techniques`, `llminjection_detections`, `controls`, `gap` on attack-path steps, and the
`x_llminjection` block) link the case to this repository's records.

| Case | Attack path | Report |
|---|---|---|
| `CASE-ARTEX-STORM-0940` | identity spray, OAuth abuse, provider as a bridge | [section](../reports/dossiers/tcem-artex.md) |
| `CASE-ARTEX-VAPOR-PANDA` | exposed app, web shell, domain credentials | |
| `CASE-ARTEX-STORM-3358` | anonymous upload, downloader, open-source RAT | |
| `CASE-ARTEX-CRAFTY-FALCON` | payment APIs from allow-listed infrastructure, mule accounts | |
| `CASE-ARTEX-CLOUD-SECRETS` | leaked keys, permission probing, secret stores | |
| `CASE-ARTEX-INSIDE` | consoles, scanner hand-off, backdoored image, sandbox escape | |

```bash
python3 scripts/build_tcem.py     # cases, fixtures, figures (assets/tcem) and reports/dossiers/tcem-artex.md
python3 scripts/tcem_validate.py  # required fields, references, LLMInjection ids, replay
tce validate tcem/cases/CASE-ARTEX-STORM-0940   # with the TCEM toolkit installed
```

The cases were also checked against TCEM's JSON Schemas (`schemas/*.schema.json`, v0.5.1) with no errors.
