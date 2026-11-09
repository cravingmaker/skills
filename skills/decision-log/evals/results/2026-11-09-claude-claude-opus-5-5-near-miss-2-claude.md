# decision-log: claude near-miss-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `c7d1da47cacadfcc4bf88c1784b33b8f25cc418b`, actual bytes SHA-256 `e26dc3c07e363f7ca92df862efafb3cd58606439c17f8a865f2029473aaf53dc`; dirty: `False`.
- **Fixture.** `near-miss-2`, SHA-256 `3d12eb408a56df6f3d56227a811a297a291b91eefb8e93bbd9b85ee0ba480053`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Write an architecture decision record explaining our cache choice.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3.14 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 7 | 0 |
| baseline | false | false | 6 | 0 |

Treatment: 14 response lines; changed files `.cache/npm/_logs/2026-11-09T04_00_48_255Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 34.598 seconds and 7 tool calls; token usage is in the JSON record.

Baseline: 14 response lines; changed files `.cache/npm/_logs/2026-11-09T04_01_50_904Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 33.663 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: domain-modeling or architecture writing, without a fleet scaffold.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-2-claude/baseline/artifacts/`.
