# toolchain-upgrade: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `eba559a3e11b4c243685999046d2e727705be022`, actual bytes SHA-256 `fe83d0da4ecd64601dd54283baa35fb66b4bb37d20390d9462149b112b144818`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `bf918837cbbdbb88aff38d49033715aa2b1d5e2dba812e8d4183834783becc1f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [toolchain-upgrade.tar.gz](https://drive.google.com/file/d/1RqNachapqDeVSXaobA4Qxh4x_vRvaJYF/view), folder `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/` inside.

## Prompt

```text
Bump the ESLint plugins to their latest versions.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 10 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 37 response lines; changed files `.cache/npm/_logs/2026-11-09T11_11_45_884Z-debug-0.log, eslint-policy.json, package-lock.json, package.json`; removed files `none`; validation command present: `requires review`. Workflow cost: 53.647 seconds and 10 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `.cache/npm/_logs/2026-11-09T11_12_38_671Z-debug-0.log, package-lock.json, package.json`; removed files `none`; validation command present: `requires review`. Workflow cost: 31.236 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: versions checked against the project's release-age and pinning policy, a before-and-after effective-config comparison, an explicit decision for every added or changed rule, and a report.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-pre-claude/baseline/artifacts/`.
