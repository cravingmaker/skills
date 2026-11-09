# correct: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `128a093fe9da0261e4b78fc8bafb7739b5615820`, actual bytes SHA-256 `9a08bf9e19968ba1182be5e01b3640dcba12c038b753bc292a0da3057b8b9181`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `f616d746cb62f1e135cffe8c3c0b77b1bc9dc27d1749cfcd45341557e3e287bb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
A judgment mistake recurred twice and no mechanical check can decide it

Task context supplied identically to both arms:
Correct only the recurring design judgment in history/judgment.md; record a scoped review standard with bad/good example, not an instruction file.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 6 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T03_24_46_804Z-debug-0.log, CONTRIBUTING.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 38.736 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `.cache/npm/_logs/2026-11-09T03_29_29_594Z-debug-0.log, CONTRIBUTING.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 36.369 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a scoped standards rule with a bad/good example that the `change-review` skill reads.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/artifacts/`.
