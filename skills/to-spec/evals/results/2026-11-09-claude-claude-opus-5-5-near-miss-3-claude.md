# to-spec: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `3407cb8d65a8b6749edb784778f9077683f1e3ec`, actual bytes SHA-256 `14e3f9478478a86870db323071f754380c6c8caf6cc63ad7c3f12c40abf17326`; dirty: `False`.
- **Fixture.** `near-miss-3`, SHA-256 `e7a0a1d4d69c54406e7fd6a3950b8c55968d68f00e335375f20193a8ad27f965`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Write a requirements document that reconciles the contract, the regulation, and the support tickets.

Task context supplied to both arms:
Use inputs/contract.md, regulation.md, and support.md as synthetic supplied obligations. Identify conflicts, do not claim legal advice or reconcile away the contradiction.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 5 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 19 response lines; changed files `.cache/npm/_logs/2026-11-09T03_32_10_142Z-debug-0.log, docs/specs/data-retention.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 42.811 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 19 response lines; changed files `.cache/npm/_logs/2026-11-09T03_33_14_462Z-debug-0.log, .planning/specifications/data-retention.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 53.858 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: no ordinary engineering spec; this is a multi-source obligation reconciliation task.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/artifacts/`.
