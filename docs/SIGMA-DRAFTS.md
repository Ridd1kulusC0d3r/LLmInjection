# Sigma drafts and a test of Feedly's `create-sigma-rule` skill

Two detections moved from specification to rule file on 2026-10-10, and a third was assessed and left as a specification. The method came from [feedly/skills](https://github.com/feedly/skills) (MIT, last commit 2026-10-07), which describes an eight-stage workflow for turning intelligence into Sigma rules.

## How the test was run, and what it does not show

- I read `skills/create-sigma-rule/SKILL.md` and **followed its stages by hand**. I did not run it as an installed Claude skill, so this is a test of the method and its helper scripts, not of the packaged skill.
- Input was each detection's `hypothesis` and `telemetry` from `data/detections.json`. The skill ranks that kind of input (a behaviour description) as the weakest, because it carries no command lines or field names.
- There was no organisation profile. The skill's fallback is its defaults, recorded here: generic Sigma field names, no backend-specific mapping, and no invented allowlists.
- Tooling: sigma-cli 3.1.0, plugins `splunk` and `kusto`, ATT&CK Enterprise 19.2 (bundle modified 2026-08-05, loaded through `attack_check.py --bundle` because the default URL returned HTTP 403 from this environment, exactly the case the skill documents).

## Results

| Detection | Outcome | File |
| --- | --- | --- |
| DET-AI-032 Agent runtime launched in unattended auto-approve mode | Rule written | `detections/sigma/det-ai-032-agent-approval-disabled.yml` |
| DET-AI-029 Package install writes AI agent config | Written as a **hunting-tier correlation** (two building blocks plus a temporal rule), because one event cannot express it | `detections/sigma/det-ai-029-package-install-writes-agent-config.yml` |
| DET-AI-036 Inbound scan of AI service ports | **Not drafted** | none |

### DET-AI-032: evidence ledger

| Condition | Label | Source |
| --- | --- | --- |
| `--dangerously-skip-permissions`, `--permission-mode bypassPermissions` | SOURCED | Claude Code CLI reference: the flag is "Equivalent to `--permission-mode bypassPermissions`" |
| `--approval-mode yolo`, `--yolo` | SOURCED | Gemini CLI reference: `--yolo` is deprecated in favour of `--approval-mode=yolo` |
| Codex CLI approval-bypass flags | **not included** | The Codex configuration page I fetched does not document them; a flag taken from memory would be an unsourced condition |
| Gemini `-y` short form | **not included** | Documented, but `-y` is far too common in other tools to match on its own |
| `--allow-dangerously-skip-permissions` | deliberately **not** matched | Per the same reference it only adds the mode to the Shift+Tab cycle without starting in it |

Resilience record: `OriginalFileName` is not applicable (the anchor is a command-line flag, not a known Windows binary). `|windash` is not applied: the flags are parsed by the agent's own CLI and I did not verify that it accepts Unicode dash variants, so this is an assumption, recorded as such. No ATT&CK tag: the repository maps T015 only to ATLAS, and a tag without a sourced rationale would be invented.

### DET-AI-029: why a single event does not work

The specification wants the package-install process tree. A file-creation event carries the writing process, and for npm the writer is `node`, for pip it is `python`, and lifecycle scripts run in children of those. An `Image` anchor on `npm` or `pip` would match nothing, and one on `node` or `python` would match every editor extension host. So the rule is a Sigma **correlation**: a package-install command and an assistant-config write on the same host within ten minutes. The per-host grouping is weaker than a process lineage, and the rule is tagged `detection.threat-hunting` at level `low` for that reason.

### DET-AI-036: not drafted

It needs a count of distinct destination hosts probed by one source, plus a catalogue of AI-service URL paths that I could not source in this session. Writing the paths from memory would be fabrication. It stays a specification.

## Validation

```text
sigma check -i -x d3_fendtag -x namespace_tag detections/sigma      -> 0 errors, 0 condition errors, 0 issues
python check_grouping.py -t splunk --without-pipeline <rule>        -> 1 clean, 0 needing attention
attack_check.py --bundle enterprise-attack.json attack.t1195.001    -> valid (not used in a rule; see below)
```

Converted queries (generic field names; they will not match an index until a field mapping exists):

```text
# DET-AI-032, Splunk
CommandLine IN ("*--dangerously-skip-permissions*", "*--permission-mode bypassPermissions*", "*--permission-mode=bypassPermissions*", "*--approval-mode yolo*", "*--approval-mode=yolo*", "*--yolo*")

# DET-AI-032, Kusto
CommandLine contains "--dangerously-skip-permissions" or CommandLine contains "--permission-mode bypassPermissions" or CommandLine contains "--permission-mode=bypassPermissions" or CommandLine contains "--approval-mode yolo" or CommandLine contains "--approval-mode=yolo" or CommandLine contains "--yolo"

# DET-AI-029, Splunk (correlation; the Kusto backend does not support correlation rules)
| multisearch
[ search CommandLine IN ("*npm install*", "*npm i *", "*pnpm add*", "*pnpm install*", "*yarn add*") OR CommandLine IN ("*pip install*", "*pip3 install*") | eval event_type="llmi_det_ai_029_package_install" ]
[ search TargetFilename IN ("*/.claude/*", "*\\.claude\\*", "*/.cursor/*", "*\\.cursor\\*", "*/.vscode/*", "*\\.vscode\\*") | eval event_type="llmi_det_ai_029_agent_config_write" ]
| bin _time span=10m
| stats dc(event_type) as event_type_count by _time Computer
| search event_type_count >= 2
```

## Findings worth acting on

1. **The repository's own rules fail a default `sigma check`.** The `llminjection.*` tags are an unknown namespace (`InvalidNamespaceTagIssue`, 3 issues on the existing three rules, 6 with the new ones). The tags stay because the repository uses them to link rules to records, and the validator `namespace_tag` is excluded. Anyone submitting these rules upstream must remove them first.
2. **A guarantee the first draft lacked.** The first version of the DET-AI-032 rule used two selections joined by `1 of selection_*`; `check_grouping.py` flagged it because Splunk leaves a top-level OR unbracketed, which is harmless alone and wrong once an index prefix is prepended. Merging into one list removed the risk and `sigma check` could not have caught it.
3. **Splunk's temporal correlation uses fixed ten-minute buckets**, not a sliding window, so an install and a write that straddle a bucket edge are missed.
4. **DET-AI-029 had no linked test.** `test_ids` is empty. A rule without a test cannot be validated; adding a safe test is the next step.
5. **Limits of the skill for this repository:** it targets ATT&CK-shaped intelligence (commands, binaries, registry keys). Most of the 45 detections describe agent-runtime and model-pipeline behaviour whose telemetry (tool-call logs, MCP inventories, model hashes) has no Sigma logsource, so a rule file is the wrong artefact for them.

## Status

Both rules are `experimental`. Neither has been run against real telemetry. The dataset keeps `status: specification` for these detections because the field describes the detection's design; the coverage matrix reads rule files from `detections/`, so it already counts them.
