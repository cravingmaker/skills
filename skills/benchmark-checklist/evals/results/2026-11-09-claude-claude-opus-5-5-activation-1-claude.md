# benchmark-checklist: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `0ee5d8b14883ca4fbc6edc31277359de3796ff7b`, actual bytes SHA-256 `969f2f4de3b52d92ad22949b3e91f30aa695086802095232a1ac07ca2531f117`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `e6939d55ed86b5134582ebaa37c94e5c32403e1fafc631bf07c705ebc95ecdaf`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Is this measured 30% export speedup believable?

Task context supplied identically to both arms:
Inputs and finite measurement limit are in benchmark/README.md. No optimization or dependency installs.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 4 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 33 response lines; changed files `.cache/npm/_logs/2026-11-09T06_00_35_372Z-debug-0.log, benchmark/__pycache__/algorithms.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 46.105 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T06_01_21_536Z-debug-0.log, benchmark/__pycache__/algorithms.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 32.009 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: inspect timing scope, units, denominator, comparable sides, completed/correct/error counts, limiter and uncertainty before accepting the sentence.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/artifacts/`.
