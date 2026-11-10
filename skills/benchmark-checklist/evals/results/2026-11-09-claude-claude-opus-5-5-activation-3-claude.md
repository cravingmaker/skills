# benchmark-checklist: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `0ee5d8b14883ca4fbc6edc31277359de3796ff7b`, actual bytes SHA-256 `969f2f4de3b52d92ad22949b3e91f30aa695086802095232a1ac07ca2531f117`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `e6939d55ed86b5134582ebaa37c94e5c32403e1fafc631bf07c705ebc95ecdaf`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [benchmark-checklist.tar.gz](https://drive.google.com/file/d/1diEWbY5-z896P1HfJjlzvh0kLmxiwret/view), folder `2026-11-09-claude-claude-opus-5-5-activation-3-claude/` inside.

## Prompt

```text
Check the regression number from our macOS runner.

Task context supplied identically to both arms:
Inputs and finite measurement limit are in benchmark/README.md. No optimization or dependency installs.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 6 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 34 response lines; changed files `.cache/npm/_logs/2026-11-09T06_00_42_381Z-debug-0.log, benchmark/__pycache__/algorithms.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 49.135 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T06_01_31_616Z-debug-0.log, benchmark/__pycache__/algorithms.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 43.824 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: project-native supported tooling rather than an assumed Linux-only command set.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/artifacts/`.
