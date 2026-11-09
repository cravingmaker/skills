# wait-what: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `112be18d25916e38f717a003de18fc07e9397c70`, actual bytes SHA-256 `f5c23c382ff1ae563601e3348904d31fac084a144d8f173032fea823724a437a`; dirty: `False`.
- **Fixture.** `outcome-3`, SHA-256 `16e92b82377241283f122410704bcd7ca07063d4c00646e5e14385c83ced60a6`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/wait-what Wait-what, explain the full-stop prepare-only result.

Supplied task context:
Previous assistant answer, supplied as context: Full-stop result: prepare-only; PR open and unmerged, auto-merge and queue off. Helper allowance is exhausted. No merge or new helper is authorized.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 1 | 0 |
| baseline | n/a | false | 1 | 0 |

Treatment: 13 response lines; changed files `.cache/npm/_logs/2026-11-09T05_03_54_344Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 14.073 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 13 response lines; changed files `.cache/npm/_logs/2026-11-09T05_04_41_272Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 14.515 seconds and 1 tool calls; token usage is in the JSON record.


Expected deliverable: "Wait-what, explain the full-stop prepare-only result." Check: the last unclear point is explained while no-merge and existing helper limits persist.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Both explain prepare-only/open/unmerged state, disabled auto-merge/queue and exhausted helper allowance. No new helper or merge occurs, and both say the state is supplied context rather than freshly verified.
