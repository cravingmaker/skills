# work-decomposition: claude near-miss-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-4` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `7a576f6c0cbf17fcc0a2a47e0dec8e13d2e36291`, actual bytes SHA-256 `a83da8598f67faed667175b6c6782ffa69bb79ece6034a6591a00d2b2a60caaf`; dirty: `False`.
- **Fixture.** `near-miss-4`, SHA-256 `ce18dd0bf7c1c64d7341da57ba1340ccec17a2ba074552ebadf595a1284cb9c7`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Write tickets from this approved spec, presenting the breakdown for review.

Task context supplied to both arms:
Approved spec: docs/specs/saved-searches.md. Tracker and domain configuration are in docs/agents/. The exact ticket breakdown has not yet been approved.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 3 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 44 response lines; changed files `.cache/npm/_logs/2026-11-09T03_45_26_267Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 55.908 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 31 response lines; changed files `.cache/npm/_logs/2026-11-09T03_46_22_394Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 41.963 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the `to-tickets` skill, with no ownership plan or dispatch.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-4-claude/baseline/artifacts/`.
