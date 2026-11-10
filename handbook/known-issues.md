> **Human documentation.** Agents should not read this page unless a person asks them to.

# Known issues and evidence limits

The main-branch core is evaluated, with specific host limits and a small recorded nit still visible. This page separates current limitations from fixed defects; it does not infer bugs from untested paths.

## Contents

- [Manual-only is not a file-access boundary](#manual-only-is-not-a-file-access-boundary)
- [Current limits and nits](#current-limits-and-nits)
- [Fixed defects](#fixed-defects)
- [What remains untested](#what-remains-untested)
- [How to report a useful issue](#how-to-report-a-useful-issue)

## Manual-only is not a file-access boundary

Status: known visibility limit; one observed read, not a confirmed repeated trigger. Claude hid a manual entry from its own skill list, but a negative survey prompt still read that entry through Bash. The [original public record](../skills/to-questionnaire/evals/results/2026-11-09-claude-claude-opus-5-5-near-miss-3-claude.md) retains the observation. Its [fresh repeat](../skills/to-questionnaire/evals/results/2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude.md) read no candidate body.

Use native explicit selection for intended manual work and review unexpected body reads. Do not treat visibility settings as a sandbox. The same general filesystem distinction applies to this human handbook.

## Current limits and nits

Each workaround stays within the existing task and host permissions.

| Item | Status | Evidence and practical response |
| --- | --- | --- |
| Claude permission denial on a combined offline PR edit/readback | Historical host-confounded failure; same-byte repeat completed | [PR #9](https://github.com/cravingmaker/skills/pull/9) retains both observations; no skill-body defect or universal permission clearance was established |
| Claude hook-path writes and real npm execution | Environment limitation in the recorded fixtures | Protected-path denials were separated from trigger misses with a disposable hook fixture; real npm and staged-index parity remain unproved in that setup |
| Unsupported Claude installation roots/wrappers | Deliberate fail-closed adapter limit | [Installation contract](../docs/installing.md#claude-code): linked worktrees, separate Git directories, subdirectories, and unsupported native schemas need reconciliation |
| Host memory/context injection | Isolation caveat | Host memory can add context beyond a clean project; paired adapters disable it, while campaign coordinator context is a separate boundary |
| Orphaned plugin cache after uninstall | Observed host lifecycle behavior | The cutover observed cache retention while sessions still referenced it; verify fresh discovery rather than deleting shared cache broadly |
| Hanging Codex remote plugin listing | Observed cutover limitation | A remote-catalog inventory call can hang; a bounded alternative inventory is needed |
| Minor source-label error in a final retrospective answer | Open response nit | [Claude Outcome 6](../skills/retro/evals/results/2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude.md) attributes an off-topic instruction to the wrong source label; the destination check and scope result still pass |
| Public raw-evidence links do not resolve in a clone | Intentional evidence-access limit | [Harness evidence contract](../docs/eval-harness.md#read-the-evidence): raw traces remain private; inspect the committed summary and its limits |
| `--host codex` currently adds no behavior | Open installer interface nit | [`install-skills.py`](../scripts/install-skills.py): the flag is parsed at line 45, while only the Claude value branches at lines 53, 55 and 161. Source-policy checking at lines 126-127 runs regardless; retain the flag to state intent or omit it |
| Catalog status checks do not bind current bytes or semantic hurt | Deliberate structural-check limit | [`check-catalog.py`](../scripts/check-catalog.py) `missing_evaluations` (lines 25-52) checks valid/completed example coverage. Final-byte and unresolved-hurt decisions require the campaign review |
| No general uninstall command | Open installer capability limit | [`install-skills.py`](../scripts/install-skills.py) `parse` exposes install/update flags and no remove operation. Inspect ownership and dependent packages before scoped manual reconciliation; removal is not exercised here |
| Claude adapter checks one project at a time | Adapter scope limit; multi-project override behavior not exercised | [`claudesettings.py`](../scripts/claudesettings.py) resolves user/project/local targets for the supplied root. Other project settings may differ |
| Original cutover checklist uses future tense | Historical wording retained | [Archived checklist](cutover.md) was written before the [observed cutover in PR #10](https://github.com/cravingmaker/skills/pull/10). Its new wrapper labels the date; the original checklist is not rewritten |
| README authoring step used to require a manual table row | Fixed in this handbook change | [AGENTS.md](../AGENTS.md#workflow), step 4, now runs the generator and its check and requests the human guidance each new skill needs |
| Evaluation guide omits some later Claude activation details | Documentation gap in main | Compare the [base guide](../docs/eval-harness.md) with [PR #9](https://github.com/cravingmaker/skills/pull/9) and the [current observer](../scripts/evalharness/hosts.py) for native replay and Bash-body evidence |
| Older overview names additional clients | Unproved historical support wording | The [original overview](https://github.com/cravingmaker/skills/blob/812abc3e9ed0ffe1ffc85dc9505bb6473deb5081/README.md) names Cursor and other clients; retained installation and behavioral records cover Claude Code and Codex. Format compatibility does not prove another host's runtime behavior |
| Old automatic activation fields retain observer misses | Historical evidence limitation; observer fixed before PR #8 landed | [Evaluation contract](../docs/eval-harness.md#codex) now recognizes trusted native selection. Earlier records can retain the automatic `false` field with a reviewed correction; read both before drawing a behavioral conclusion |
| Historical install proof describes an earlier smaller profile | Snapshot limitation | Its pinned revision is valid historical evidence; the [current generated profile reference](routing.md#what-each-profile-installs) gives current membership |

The memory, cache, and hanging-list observations are published here as sanitized observations supplied for the cutover documentation. The public cutover PR establishes installed/discovered policy state; it does not contain every low-level diagnostic from that operation.

## Fixed defects

These are historical failures with corrections in merged work. Their old records remain available and must not be counted as current passing evidence.

| Defect | Status | Evidence |
| --- | --- | --- |
| Dotenv serialization could corrupt an apostrophe-containing value | Fixed in PR #6; landed on main through PR #8 | [PR #6](https://github.com/cravingmaker/skills/pull/6) describes parser round trips and fail-before-write refusal |
| Architecture-report rendering safeguards | Hardening added in PR #6; landed through PR #8 | [PR #6](https://github.com/cravingmaker/skills/pull/6) records escaped static offline output and optional pinned strict Mermaid |
| Native Codex skill injection was missed by the activation observer | Fixed in the stack landed by PR #8 | Main history includes native-selection detection and the input-text provenance restriction; the [current evidence contract](../docs/eval-harness.md#codex) states the accepted event |
| A historical-name exemption accidentally covered a live route | Fixed before the stack landed in PR #8 | Main history ends the exemption before live guidance; the [current reference](../skills/clear-communication/references/clarifying.md) separates the regions |
| Router could report acceptance without required dispatch/isolation | Fixed before PR #8 landed | The [current router](../skills/agent-orchestrator/SKILL.md#build-from-an-approved-spec-and-code-tickets) stops at source-bound preflight when those facilities are unavailable |
| Claude bundled skills could fork uncontrolled children during evals | Fixed in the harness in PR #9 | [PR #9](https://github.com/cravingmaker/skills/pull/9) records bundled-skill exclusion and fork rejection; affected old attempts stay invalid |
| Long Claude temporary paths could fall back to shared Bash temp | Fixed in the harness in PR #9 | The adapter uses a short private physical path and a retained live two-arm temp check; affected shared-temp attempts are invalid |
| Native Claude slash selection and Bash body reads were missed | Fixed in PR #9 | [PR #9](https://github.com/cravingmaker/skills/pull/9) and the [current activation contract](../docs/eval-harness.md) distinguish native replay and visible installed-body reads |
| Claude-only listing/cat detection leaked into Codex classification | Fixed in PR #9 | The listing/cat extension is Claude-only; Codex compound reads remain unclassified for manual trace review |
| Retrospective read outside named sources | Fixed and rerun through the final PR #9 revision | Final-byte paired source audits pass on both hosts; the [source-boundary method](../skills/retro/SKILL.md) includes exact-path and separate-history rules |
| Failed or repeated adversarial probes escaped their allowance | Fixed in PR #9 | The [entry](../skills/interrogate/SKILL.md) charges every execution and captures output/status once; controlled wrapper-failure cases run on both hosts |
| Guardrail handling reopened a broad audit for an already named missing-helper gap | Fixed in PR #9 | The [method](../skills/project-guardrails/SKILL.md) now reports that gap on supplied evidence and stops the dependent flow |
| Narrow description misses for contextual repair, human-ruling checks, and staged-hook wiring | Fixed and retested in PR #9 | [PR #9](https://github.com/cravingmaker/skills/pull/9) records description changes and their paired retests |

The architecture-report row describes the shipped safeguards. It does not claim an independently reproduced exploit against the old upstream code. Importer strictness and blocker/Proof parsing were reviewed and corrected within the stack; the current template/importer fixtures define the supported forms.

## What remains untested

The retained evidence supports bounded fixtures and specific host checks. It does not establish every live flow described by a skill.

| Surface or claim | Current evidence limit |
| --- | --- |
| Future CLI versions or different models/settings | Recorded versions are snapshots; rerun the capability and session checks |
| Other Agent Skills hosts | Format compatibility is expected; runtime routing and manual policy are untested |
| Live production discovery with every plugin, namespace, hook, and server policy | Discovery replays and isolated sessions do not reproduce all managed sources |
| A successful guarded merge, queue completion, and late head/base races | Local shipping fixtures mainly exercise safe progress and blocked gates |
| Root watcher lifecycle on a live forge | A one-pass fallback or simulated watch does not establish service behavior |
| Actual independent provider panels and native delegated-worker recovery | Paired evals disable delegation; the daily-chain adapter used serial isolated CLI workers |
| Real hosted CI, required bots, and human review completion | Offline forge metadata is a stand-in |
| Full native/UI/device coverage and every generated feature map | A driven CLI or one feature establishes only that surface/journey |
| Crash recovery halfway through checkpoint publication | Atomic record checks are not a crash-injection experiment |
| Real npm and complete staged/local/CI parity in denied environments | A custom-hook stand-in keeps those surfaces open |
| General reliability, superiority, and cost savings | Single paired examples with different host-default models cannot establish population effects |

## How to report a useful issue

Include the host and version, exact selected entry, source revision, relevant invocation setting, task scope, expected result, and what actually happened. Name the command or user surface and preserve its exit status or visible result. Separate a missing method, an activation miss, a permission denial, a wrong artifact, and an unavailable observation. Share sanitized evidence; do not publish credentials, personal paths, or private transcripts.
