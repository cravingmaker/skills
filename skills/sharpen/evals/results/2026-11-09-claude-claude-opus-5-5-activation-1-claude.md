# sharpen: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `26ad1989c1d3ad5aee55ea017cefe3acdccca6ca`, actual bytes SHA-256 `cf32e95ff76aeb1aded86b06349ec684023510f2820f42187ad68ef832dff7a3`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `a2c1df86b6a5774b313063cfecbb17600cf1545fb97fb4e1202d5b14b1817dc1`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/sharpen

Use the `sharpen` skill explicitly for this request.

Sharpen this prompt: audit the retry policy using the incident notes.

Task context supplied to both arms:
Incident source is history/incident-8.md; target src/retry.py. Rewrite only; do not audit or change code.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 2 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 50 response lines; changed files `.cache/npm/_logs/2026-11-09T04_53_23_667Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 31.902 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 26 response lines; changed files `.cache/npm/_logs/2026-11-09T04_53_55_674Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 19.424 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the four upstream questions are answered, followed by a deeper prompt grounded in raw evidence, methods, and an external correctness check.

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
