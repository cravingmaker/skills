# why: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `3ddcc927af43c06466d921bd2bc20e86e4c94183`, actual bytes SHA-256 `8603a05f3894d9128aacd77abd63f21372c3cbb3932e4148b23293f3b128e7bd`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `a2c1df86b6a5774b313063cfecbb17600cf1545fb97fb4e1202d5b14b1817dc1`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
These agent notes say I banned the endpoint forever. Did my original instruction say that?

Task context supplied to both arms:
Compare history/original-instruction.md with history/agent-note-{1,2,3}.md. Preserve the original scoped words.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | false | 1 | 0 |
| baseline | false | false | 1 | 0 |

Treatment: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T04_56_14_755Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 11.476 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `.cache/npm/_logs/2026-11-09T04_56_26_490Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 9.774 seconds and 1 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: original attributable words and scope are preserved; repeated summaries count as one dependent chain.

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
