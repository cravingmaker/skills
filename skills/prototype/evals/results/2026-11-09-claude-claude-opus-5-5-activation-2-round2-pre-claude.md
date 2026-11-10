# prototype: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `8106b30496f573941b8efa889c51d814d5aa2b5e`, actual bytes SHA-256 `2fb4cdaf107ded26057a1f1591cdc997edf9980bec726ff7af7a1aa5099e9bf9`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `4ffe598e4a63c4560aac2f1836d73e9449c78180d5050b26e7cdfa88c9689b08`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [prototype.tar.gz](https://drive.google.com/file/d/1Rv_qtYdd-oR2lwSJsU6BlCDP6YUTIkRc/view), folder `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/` inside.

## Prompt

```text
Try three structurally different settings layouts using our existing page context.

Task context supplied to both arms:
Existing page is settings.html. Keep its header/navigation, team name West team, notifications enabled. Browser/preview tools are unavailable; do not claim a rendered or interaction observation.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 6 | 0 |
| baseline | false | false | 8 | 0 |

Treatment: 29 response lines; changed files `.cache/npm/_logs/2026-11-09T11_23_59_272Z-debug-0.log, prototypes/settings-layouts/index.html`; removed files `none`; validation command present: `requires review`. Workflow cost: 90.949 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 14 response lines; changed files `.cache/npm/_logs/2026-11-09T11_27_51_213Z-debug-0.log, settings-a-sidebar.html, settings-b-rows.html, settings-c-tabs.html`; removed files `none`; validation command present: `requires review`. Workflow cost: 46.655 seconds and 8 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: labelled alternatives preserve realistic data and surrounding UI; supported preview tools drive the relevant interactions.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-pre-claude/baseline/artifacts/`.
