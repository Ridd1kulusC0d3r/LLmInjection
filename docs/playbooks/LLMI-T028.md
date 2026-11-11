# LLMI-T028: AI-Assisted Tooling Development

> Generated from the datasets by `scripts/build_playbooks.py`; do not edit by hand. Change the data, or add hand-written notes in `docs/playbooks/notes/`. It says what the repository knows and where it stops. Use it only on systems you are authorised to test.

| | |
|---|---|
| Category | offensive-enablement |
| Maturity | **observed in the wild** |
| Priority | 6 of 16 (maturity weight times the layers still missing) |
| Frameworks | none mapped |

## Where it stands

| Layer | Status |
|---|---|
| Evidence | 69 record(s), 31 publisher(s), best grade A, newest 2026 |
| Safe tests | 1 |
| Detections | 0 rule file(s), 1 specification(s) |
| Controls | 1 |
| Benchmarks | 0 |

**Next step:** Turn DET-AI-045 (Rapid Iterative Script Variants on One Host) from a specification into a rule file, starting with the telemetry listed in section 3.

## 1. Understand it

Operators use LLMs to generate or iterate on reconnaissance, exploitation, credential-validation and deployment scripts or malware, compressing development time without changing the underlying attack paths.

What the repository links to it:

- 2026 · [APT27 Gemini-assisted ORB management tooling](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-APT27-ORB-TOOLING) (campaign, confirmed)
- 2025-08 · [APT41 Gemini-assisted OSSTUN C2 and obfuscation development](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-APT41-OSSTUN-TOOLING) (campaign, confirmed)
- 2026 · [APT45 recursive CVE analysis and PoC validation prompting](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-APT45-CVE-POC-PROMPTING) (campaign, confirmed)
- 2026-07 · [Armored Likho BusySnake Stealer campaign with AI-generated first-stage payloads](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARMORED-LIKHO-BUSYSNAKE) (campaign, high)
- 2026-10 · [Chinese-speaking ARTEX multi-model operator targeting 19 markets](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-ARTEX-MULTI-MODEL-OPERATOR) (campaign, high)
- 2026-04 · [bandcampro Gemini CLI-driven C2 botnet build and fraud operations](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-BANDCAMPRO-GEMINI-CLI-C2) (campaign, confirmed)
- 2026 · [BREEZE COMET payment-system fraud in Brazil](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-BREEZE-COMET-PAYMENTS) (campaign, confirmed)
- 2026 · [BUGSTER Hermes Agent/DeepSeek multi-domain cybercrime](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-BUGSTER-HERMES-DEEPSEEK-CYBERCRIME) (campaign, confirmed)
- 2026-09 · [CaptiveCrunch](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CAPTIVECRUNCH) (campaign, confirmed)
- 2026 · [CL-CRI-1131 LLM-assisted intrusions in Mexico and Ecuador](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CL-CRI-1131) (campaign, medium)
- 2026-02 · [CL-CRI-1163 phishing against Brazilian financial sector with LLM-generated scripts](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CL-CRI-1163-BRAZIL-FINANCE) (campaign, medium)
- 2026 · [Coral Sleet AI-built repository trojanization](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CORAL-SLEET-REPO-TROJANIZATION) (campaign, high)
- 2026-08 · [CrowdStrike Threat Actor 1: Claude Code dual-agent harness against Argentine healthcare](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-CROWDSTRIKE-TA1-ARGENTINA-HEALTHCARE) (campaign, confirmed)
- 2026 · [Earth Krahang AI-enhanced CVE-2026-0740 exploit scanner](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-EARTH-KRAHANG-AI-EXPLOIT-SCANNER) (campaign, confirmed)
- 2026 · [Earth Naga vibe-coded PowerShell/C# backdoor loader](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-EARTH-NAGA-VIBE-CODED-LOADER) (campaign, confirmed)
- 2024-12 · [FunkSec AI-assisted ransomware-as-a-service operation](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-FUNKSEC-AI-ASSISTED-RAAS) (campaign, medium)
- 2026-04 · [GREYVIBE AI-assisted operations against Ukraine](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GREYVIBE-UKRAINE) (campaign, high)
- 2026 · [GTG-10007 exploit foundry and autonomous attack frameworks](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-10007) (campaign, confirmed)
- 2026 · [GTG-14021 stability-maintenance and transnational repression tooling](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-14021) (campaign, confirmed)
- 2026 · [GTG-14022 public-opinion monitoring pipeline](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-14022) (campaign, confirmed)
- 2026-04 · [GTG-15001 deceptive dating-app network](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-15001) (campaign, confirmed)
- 2026 · [GTG-20006 Claude-driven espionage operation lifecycle](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-20006) (campaign, confirmed)
- 2025-08 · [GTG-2002 Claude Code data-extortion operation ("vibe hacking")](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-2002-VIBE-HACKING-EXTORTION) (campaign, confirmed)
- 2026 · [GTG-30004 OSINT profiling and malware obfuscation](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-30004) (campaign, confirmed)
- 2026 · [GTG-30005 military reconnaissance and surveillance tooling](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-30005) (campaign, confirmed)
- 2026 · [GTG-30006 domestic surveillance malware and phishing tooling](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-30006) (campaign, confirmed)
- 2026 · [GTG-34007 paramilitary surveillance tooling](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-34007) (campaign, confirmed)
- 2026-05 · [GTG-50014 AI-driven smash-and-grab intrusions and extortion](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-50014) (campaign, confirmed)
- 2026 · [GTG-50027 Lakana 360 mass-interception platform development](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-50027) (campaign, confirmed)
- 2026-07 · [GTG-50029 hacktivist campaign against European political entities](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-50029) (campaign, confirmed)
- 2025-08 · [GTG-5004 Claude-assisted ransomware-as-a-service](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTG-5004-AI-BUILT-RAAS) (campaign, confirmed)
- 2025 · [China-nexus actor using a capture-the-flag pretext to misuse Gemini](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTIG-CHINA-NEXUS-CTF-PRETEXT) (campaign, confirmed)
- 2025 · [Suspected China-nexus actor using Gemini across an intrusion lifecycle (cloud, vSphere, Kubernetes)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-GTIG-CHINA-NEXUS-GEMINI-INTRUSION-LIFECYCLE) (campaign, confirmed)
- 2026-10 · [INC / The Gentlemen affiliate AI-driven ransomware operations (Phantom framework)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-INC-GENTLEMEN-PHANTOM-AI) (campaign, confirmed)
- 2026-06 · [Jade Sleet AI-accelerated job-themed targeting via front companies](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-JADE-SLEET-FRONT-COMPANIES-2026-06) (campaign, high)
- 2026-03 · [LAUNDRY BEAR Zimbra phishing with AI-assisted Flowerbed development](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-LAUNDRY-BEAR-ZIMBRA-FLOWERBED) (campaign, medium)
- 2025 · [Korean-language operators malware and C2 development (OpenAI)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-OPENAI-KOREAN-LANGUAGE-OPERATORS-2025) (campaign, confirmed)
- 2025 · [Phish and Scripts: Chinese-language phishing and tooling (OpenAI)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-OPENAI-PHISH-AND-SCRIPTS-2025) (campaign, confirmed)
- 2025 · [Russian-speaking malware tooling development (OpenAI)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-OPENAI-RU-MALWARE-TOOLING-2025) (campaign, confirmed)
- 2026 · [Unnamed PRC-nexus attempt to build an agentic pentest framework with Gemini](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-PRC-AGENTIC-PENTEST-FRAMEWORK-DESIGN) (campaign, confirmed)
- 2026 · [Unnamed PRC-nexus AI-assisted exploitation pipeline (CC Switch, Phalanx, Shai-Hulud)](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-PRC-CC-SWITCH-EXPLOITATION-PIPELINE) (campaign, confirmed)
- 2025 · [RevengeHotels 2025 LLM-generated loaders delivering VenomRAT](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-REVENGEHOTELS-2025-LLM-VENOMRAT) (campaign, medium)
- 2026 · [SANDWORM RELIC Gemini-assisted operations against Ukraine](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-SANDWORM-RELIC-UKRAINE-GEMINI-2026) (campaign, confirmed)
- 2026-08 · [Sapphire Sleet Rust software supply-chain compromise](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-SAPPHIRE-SLEET-RUST-2026-08) (campaign, medium)
- 2026 · [SHADOW-AETHER-040 agentic intrusions against Latin American governments](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-SHADOW-AETHER-040) (campaign, high)
- 2026-08 · [SilkParasite espionage against Central Asian governments](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-SILKPARASITE-CENTRAL-ASIA) (campaign, medium)
- 2026 · [STAC6994 agent-driven EDR-evasion development lab](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-STAC6994-AGENTIC-EDR-EVASION-LAB) (campaign, confirmed)
- 2025 · [TEMP.Zagros Gemini-assisted custom malware development](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-TEMP-ZAGROS-GEMINI-MALWARE-DEV) (campaign, confirmed)
- 2026 · [The Gentlemen AI-generated attack scripts](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-THE-GENTLEMEN-AI-SCRIPTS) (campaign, medium)
- 2025 · [UNC1069 Gemini-assisted cryptocurrency theft and deepfake lures](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-UNC1069-GEMINI-CRYPTO-THEFT) (campaign, confirmed)
- 2026 · [UNC2814 expert-persona prompting for embedded-device vulnerability research](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-UNC2814-PERSONA-VULN-RESEARCH) (campaign, confirmed)
- 2025 · [UNC4899 Gemini-assisted exploit research and tooling](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-UNC4899-GEMINI-EXPLOIT-RESEARCH) (campaign, confirmed)
- 2025-11 · [COINBAIT phishing kit built with Lovable AI](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-UNC5356-COINBAIT) (campaign, medium)
- 2025 · [UNC795 Gemini use across the attack lifecycle](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-UNC795-GEMINI-INTRUSION-TOOLING) (campaign, confirmed)
- 2026-10 · [VAPOR PANDA ARTEX-driven global espionage campaign](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=CAMPAIGN-VAPOR-PANDA-ARTEX) (campaign, confirmed)
- 2025 · [Carding store maintained with Claude Code](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-ANTHROPIC-AI-CARDING-STORE) (fraud, confirmed)
- 2026 · [CANFAIL and LONGSTREAM: LLM-generated decoy code in Russia-nexus malware against Ukraine](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-CANFAIL-LONGSTREAM-LLM-DECOY-CODE) (malware, high)
- 2026-02 · [EvilTokens AI-enabled email compromise service disrupted](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-EVILTOKENS-AI-BEC-SERVICE) (fraud, confirmed)
- 2026-01 · [AI-augmented mass access to FortiGate devices](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-FORTIGATE-AI-AUGMENTED-ACCESS) (intrusion, confirmed)
- 2026 · [Multi-agent credential harvesting from compromised cloud in under six hours](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-GTIG-AGENTIC-CREDENTIAL-HARVESTING) (intrusion, confirmed)
- 2026 · [Criminal actor uses an AI model to develop a 2FA-bypass zero-day](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-GTIG-AI-ZERO-DAY) (intrusion, high)
- 2026-06 · [Suspected Chinese operators use Claude Code and DeepSeek in government and financial intrusions](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-HUNTIO-CLAUDE-DEEPSEEK-INTRUSIONS) (intrusion, confirmed)
- 2026-06 · [Suspected AI-generated PowerShell script used for Active Directory enumeration](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-HUNTRESS-VIBE-CODED-AD-ENUMERATION) (intrusion, high)
- 2026-08 · [AI-agent-driven mass exploitation of PaperCut NG/MF](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-PAPERCUT-AI-AGENT-EXPLOITATION) (intrusion, confirmed)
- 2026-08 · [AI-generated exploitation scripts against Siemens S7 PLCs](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-SIEMENS-S7-AI-EXPLOIT-SCRIPTS) (exploit-development, confirmed)
- 2024 · [LLM-generated PowerShell and HTML delivery scripts in malware campaigns](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-SYMANTEC-LLM-GENERATED-LOADERS) (malware, high)
- 2026 · [TuxBot v3 Evolution IoT botnet built with LLM assistance](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-TUXBOT-V3-LLM-DEVELOPMENT) (malware, confirmed)
- 2026 · [Unit 42 investigation of a sub-10-hour AI-agent-assisted intrusion](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-UNIT42-AI-ASSISTED-INTRUSION) (intrusion, high)
- 2026 · [VoidLink AI-assisted malware engineering case](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=INCIDENT-VOIDLINK) (observed-research-case, confirmed)

Actors whose campaigns use it: APT27, APT41, APT45, Armored Likho, bandcampro, BREEZE COMET, BUGSTER, CL-CRI-1131, CL-CRI-1163, Coral Sleet, Earth Krahang, Earth Naga, FunkSec, GREYVIBE, GTG-10007, GTG-14021, GTG-14022, GTG-15001, GTG-20006, GTG-2002, GTG-30004, GTG-30005, GTG-30006, GTG-34007, GTG-50014, GTG-50027, GTG-50029, GTG-5004, Jade Sleet, LAUNDRY BEAR, RevengeHotels, SANDWORM RELIC, Sapphire Sleet, SilkParasite, STAC6994, Storm-2945, TEMP.Zagros, The Gentlemen, UNC1069, UNC2814, UNC4899, UNC5356, UNC795, VAPOR PANDA. Vendor labels are kept as published and never merged without evidence.

## 2. Test it safely

Run these in a lab you own. Each is a specification: a goal, a benign stimulus, the expected secure behaviour and the telemetry that proves it.

### TC-TOOL-040 · Iterative Script Trial-and-Error Detection

- **Goal:** Verify that rapid iteration of near-identical scripts on one host is detected by behavior, independent of who or what wrote them.
- **Stimulus:** A sandbox host runs a series of benign, numbered script variants in a short window, with failures followed by small corrections, from a user-writable path.
- **Expected:** The execution policy blocks unknown scripts from the user-writable path, and the iteration pattern raises an alert with the script hashes and exit codes.
- **Telemetry to capture:** `process-creation`, `script-content-hash`, `file-naming-pattern`, `exit-code`
- **Controls it exercises:** execution allowlisting, behavioral detection, script logging

```bash
python scripts/query_intel.py coverage LLMI-T028
python scripts/run_safe_lab.py --profile detection   # lists the cases for this surface; plan mode makes no model calls
```

The runner has plan and mock adapters only: it does not call your system. To run a case, build its stimulus in your own harness (section 7 points at tools that do) and record the outcome in the shape of [`schemas/lab-result.schema.json`](../../schemas/lab-result.schema.json).

## 3. Detect it

### DET-AI-045 · Rapid Iterative Script Variants on One Host

- **Severity:** medium
- **Hypothesis:** A host runs a series of near-identical scripts with incrementally changed names or content, failures followed by corrections, in a short window from a user-writable path. Unit 42 describes this trial-and-error pattern in the CL-CRI-1131 intrusions.
- **Telemetry:** `process-creation`, `script-content-hash`, `file-naming-pattern`, `exit-code`
- **Implementation:** specification only. Collect the telemetry above first; if you cannot, the detection cannot work yet.

## 4. Prevent it

- **Script and Unknown Binary Execution Policy** (`CTRL-EXEC-POLICY`): Restrict execution of unsigned or unknown scripts and binaries from user-writable paths, so attacker tooling is stopped by behavior and provenance regardless of how it was written.

## 5. Close the loop

- [ ] Run each test in section 2 against your system and keep the outcome with the model, prompt and tool versions.
- [ ] For every failed case, confirm which control in section 4 should have stopped it, and whether it is deployed.
- [ ] Confirm the telemetry named in the tests and detections actually exists in your logs. A detection without its telemetry is silent, not safe.
- [ ] After the fix, re-run the failed cases and confirm the detection fires on the attempt.
- [ ] Re-run all of it after any change to the model, system prompt, tools, retrieval sources or policy.

## 6. Limits of this page

- 1 of 1 detection(s) are specifications, not rules. They say what to look for, not how to query it. Nothing here has been run against real telemetry.
- No benchmark maps to it, so there is no public yardstick for how well a defence performs.
- The tests use benign markers and synthetic data. A pass in a lab is not a security rating for a production system.
- Ecosystem tools and benchmarks help you test and measure. They never support a claim that an actor used the technique.

## 7. Go deeper (links only)

- **Live record:** [this technique in the Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#node=LLMI-T028)
