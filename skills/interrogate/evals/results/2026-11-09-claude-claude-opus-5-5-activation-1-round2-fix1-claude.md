# interrogate: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `0081bf09a0026d92425cd3411cd4f11590c1e7ee`, actual bytes SHA-256 `f702b563eb383deefa9384d46fdae7fb643c065b25e4a4a8e28f81f87b122812`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [interrogate.tar.gz](https://drive.google.com/file/d/1BPxC0RceYPCX2iHpSX6OTHCxOvrttbO3/view), folder `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/` inside.

## Prompt

```text
/interrogate

Interrogate this change; try to break it and report only.

Task context supplied identically to both arms:
Read review/scope.md, review/change.diff, approved issue and CONTRIBUTING.md. Snapshot-only fixture has no live Git metadata; use exported before/current bytes and hashes without inventing commit resolution. Local Node probes `node consumer/main.mjs` and `node consumer/cli.mjs` hit the actual package. No native tool or delegation provider is callable. Report requested unavailable seats honestly. No commits or remote writes. Shared ceiling: 2 concurrent agents, 6 total starts including replacements; 3 rounds maximum. No actual additional model starts are authorized by the eval guard.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 8 | 0 |
| baseline | false | false | 7 | 0 |

Treatment: 98 response lines; changed files `.cache/npm/_logs/2026-11-09T11_26_56_794Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 77.513 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 38 response lines; changed files `.cache/npm/_logs/2026-11-09T11_30_47_122Z-debug-0.log, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 67.442 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: change-review opens in report-only panel probe mode within the shared declared scope and budget.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-round2-fix1-claude/baseline/artifacts/`.
