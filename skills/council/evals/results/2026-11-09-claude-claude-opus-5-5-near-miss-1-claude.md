# council: claude near-miss-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `645edc1b3f8b5c5c00854bc61d0d6fc29130ffbc`, actual bytes SHA-256 `b24055566d7c79f421cbb22a5ec0337e4290b06d7d90fb76b6c3191c0957771d`; dirty: `False`.
- **Fixture.** `near-miss-1`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
The meeting notes quote 'council'; summarize them.

Task context supplied identically to both arms:
Read paragraph.md only; explain the quoted words without invoking a panel.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 1 | 0 |
| baseline | false | false | 1 | 0 |

Treatment: 10 response lines; changed files `.cache/npm/_logs/2026-11-09T05_56_47_252Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 20.116 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 12 response lines; changed files `.cache/npm/_logs/2026-11-09T05_57_06_987Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 17.521 seconds and 1 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: no manual-entry selection or model panel.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/artifacts/`.
