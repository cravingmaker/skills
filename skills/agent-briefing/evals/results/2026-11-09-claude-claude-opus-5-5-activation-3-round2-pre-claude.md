# agent-briefing: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `adc18eb7748758f2697df7788c1fe2db89539d6b`, actual bytes SHA-256 `6fe92fecbcc8d65a4b813c64b9259eb8d695ed47370bbfd9baf7a30df2c37c55`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `61621f9ebbf5bb301e27aa92f33adea7511ce14744d66e283913a3a2a2fd4d14`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Brief a worker from the approved spec and ticket, using exact paths and hashes, named Proof, and existing testing seams.

Task context supplied to both arms:
# Migration QA brief context

Task QA-1: prepare (do not dispatch) a fresh QA agent to verify the active->status migration. Contract: contracts/status.json revision status-v2. Read backend/service.py, frontend/client.py, tests/test_contract.py. Source has not yet been migrated. Command ./scripts/validate.sh currently fails; no claim of readiness is authorized. QA reads the whole fixture but may write only reports/qa-migration-r1.md; no other repository edits, no deployment, network, credentials, commits, or delegation. QA is a leaf with one verification pass and must return PARTIAL/BLOCKED for unavailable checks. No role/capability skill beyond the current installed inventory is assumed; report missing required inputs. The coordinator owns all shared logs.

User constraints lost from the old brief: status strings must remain exactly active and paused; a paused account must never show Active; schema edits are forbidden. Open decision: product owner must decide copy for unknown status; do not guess it or add unknown to the schema. For the repair task, update delegation-brief.md using this context. Input hashes can be computed locally. Report needs actual commands, outputs, source/output revisions, loaded skills, assumptions, unresolved claims, decisions, and usage or unknown.

No commits or pushes are permitted, including in temporary repositories.
 Approved spec docs/specs/saved-searches.md; approved ticket .planning/work-items/search/02-list-saved-searches.md. Brief only, read exact sources and bind hashes.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 13 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 38 response lines; changed files `.cache/npm/_logs/2026-11-09T11_13_29_669Z-debug-0.log, briefs/search-02-r1.md, delegation-brief.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 176.235 seconds and 13 tool calls; token usage is in the JSON record.

Baseline: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T11_17_54_208Z-debug-0.log, brief-02-list-saved-searches.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 86.006 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: See the Outcome criteria.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/artifacts/`.
