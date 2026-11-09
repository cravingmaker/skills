# agent-orchestrator: claude activation-1

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `b7d5b85899f2cfe0b6ce7e2e715565848a9436ec`, tree `f9c2a7c444908e3c42830e844e3a504c3dbca24e`, actual bytes SHA-256 `a097ef64bd1371905586cf9a3ffe9c093f377046497666f8e5ca76da6f3e5aac`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `21641918e48bf36fd7ed78d6dc46d9bcf3c6551b07569c867e204197e0c0ac2b`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Coordinate delivery of this accepted result: file the PR, then return its link and state.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3.14 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use Python 3.14 for Python scripts. Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | false | 9 | 0 |
| baseline | false | unavailable | unavailable | 143 |

Treatment: 40 response lines; changed files `.cache/npm/_logs/2026-11-09T05_08_23_744Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 50.358 seconds and 9 tool calls; token usage is in the JSON record.


Expected deliverable: Expect file-pr filing within authority and no watch, through this router or the filing capability directly. An unread router gets no method credit.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/comparison.json).

## Invalid comparison

- claude baseline failed (exit 143, timeout False); inspect stderr and trace

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-confirm-claude/baseline/artifacts/`.
