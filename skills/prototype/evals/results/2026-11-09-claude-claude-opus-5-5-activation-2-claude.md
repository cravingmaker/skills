# prototype: claude activation-2

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `1b6e410e5d7bba2adc9d9a5c88e7d2b0980deae2`, actual bytes SHA-256 `2fb4cdaf107ded26057a1f1591cdc997edf9980bec726ff7af7a1aa5099e9bf9`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `4ffe598e4a63c4560aac2f1836d73e9449c78180d5050b26e7cdfa88c9689b08`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Try three structurally different settings layouts using our existing page context.

Task context supplied to both arms:
Existing page is settings.html. Keep its header/navigation, team name West team, notifications enabled. Browser/preview tools are unavailable; do not claim a rendered or interaction observation.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 9 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 30 response lines; changed files `.cache/npm/_logs/2026-11-09T04_52_39_792Z-debug-0.log, prototypes/settings-layouts.html`; removed files `none`; validation command present: `requires review`. Workflow cost: 112.415 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `.cache/npm/_logs/2026-11-09T04_54_32_290Z-debug-0.log, variants/settings-a-stacked.html, variants/settings-b-two-pane.html, variants/settings-c-rows.html`; removed files `none`; validation command present: `requires review`. Workflow cost: 41.917 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: labelled alternatives preserve realistic data and surrounding UI; supported preview tools drive the relevant interactions.

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
