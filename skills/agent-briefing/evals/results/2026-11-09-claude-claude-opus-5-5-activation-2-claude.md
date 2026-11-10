# agent-briefing: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `c494c272d436388a8ce17e6702dee6fcc516d9fc`, actual bytes SHA-256 `6fe92fecbcc8d65a4b813c64b9259eb8d695ed47370bbfd9baf7a30df2c37c55`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `33463c4e501e93b8ab400421d45fa14297d85ea04ed0341f9975e12fea65a2be`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [agent-briefing.tar.gz](https://drive.google.com/file/d/1FqpvKO1UwLeqNh4Svp5DeVQe_VEueOLL/view), folder `2026-11-09-claude-claude-opus-5-5-activation-2-claude/` inside.

## Prompt

```text
This agent keeps missing constraints from our chat; repair its delegation brief.

Task context supplied to both arms:
# Migration QA brief context

Task QA-1: prepare (do not dispatch) a fresh QA agent to verify the active->status migration. Contract: contracts/status.json revision status-v2. Read backend/service.py, frontend/client.py, tests/test_contract.py. Source has not yet been migrated. Command ./scripts/validate.sh currently fails; no claim of readiness is authorized. QA reads the whole fixture but may write only reports/qa-migration-r1.md; no other repository edits, no deployment, network, credentials, commits, or delegation. QA is a leaf with one verification pass and must return PARTIAL/BLOCKED for unavailable checks. No role/capability skill beyond the current installed inventory is assumed; report missing required inputs. The coordinator owns all shared logs.

User constraints lost from the old brief: status strings must remain exactly active and paused; a paused account must never show Active; schema edits are forbidden. Open decision: product owner must decide copy for unknown status; do not guess it or add unknown to the schema. For the repair task, update delegation-brief.md using this context. Input hashes can be computed locally. Report needs actual commands, outputs, source/output revisions, loaded skills, assumptions, unresolved claims, decisions, and usage or unknown.

No commits or pushes are permitted, including in temporary repositories.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 6 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 34 response lines; changed files `.cache/npm/_logs/2026-11-09T03_46_05_829Z-debug-0.log, delegation-brief.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 103.238 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 36 response lines; changed files `.cache/npm/_logs/2026-11-09T03_47_55_498Z-debug-0.log, delegation-brief.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 83.074 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the missing constraints and open decisions appear in the brief itself.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/artifacts/`.
