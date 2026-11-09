# sharpen: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `26ad1989c1d3ad5aee55ea017cefe3acdccca6ca`, actual bytes SHA-256 `cf32e95ff76aeb1aded86b06349ec684023510f2820f42187ad68ef832dff7a3`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `a2c1df86b6a5774b313063cfecbb17600cf1545fb97fb4e1202d5b14b1817dc1`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/sharpen

Use the `sharpen` skill explicitly for this request.

Use sharpen on this task, keep the scope to one parser, and leave the storage choice to me.

Task context supplied to both arms:
Task: diagnose parser failures for src/parser.ts from raw failing inputs. Scope is one parser. Storage selection belongs to the user and remains undecided. Rewrite only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 3 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 40 response lines; changed files `.cache/npm/_logs/2026-11-09T04_53_27_756Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 33.273 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 32 response lines; changed files `.cache/npm/_logs/2026-11-09T04_54_01_066Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 20.243 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the rewrite retains that scope and leaves storage undecided.

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
