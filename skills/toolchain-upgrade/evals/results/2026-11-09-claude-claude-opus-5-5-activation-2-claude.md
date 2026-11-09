# toolchain-upgrade: claude activation-2

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `d27e30b7c4a15e1ed9a6fd0dd0495814c52f0c03`, actual bytes SHA-256 `fe83d0da4ecd64601dd54283baa35fb66b4bb37d20390d9462149b112b144818`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `bf918837cbbdbb88aff38d49033715aa2b1d5e2dba812e8d4183834783becc1f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Dependabot opened a PR updating typescript-eslint. Is it safe to merge?
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 8 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 47 response lines; changed files `.cache/npm/_logs/2026-11-09T03_21_17_776Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 85.255 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 20 response lines; changed files `.cache/npm/_logs/2026-11-09T03_23_15_750Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 45.355 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: release notes read for every skipped version, effective-config differences listed with decisions, and the full checks run.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/artifacts/`.

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
