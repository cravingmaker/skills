# domain-modeling: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `08732655babb98aa1271794ba6b6d918a02d691e`, actual bytes SHA-256 `5c3388210e74bb4d79a3516c7eb0f61802fa7eca560dd3968be4b9f11b39857f`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `0ef5b6872fa169dc4847f5c3ca4907883ce146a6acd310b4bb61723052277c54`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
We're switching from REST callbacks to domain events between Ordering and Billing. That reverses ADR-0003; record it.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 6 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 8 response lines; changed files `.cache/npm/_logs/2026-11-09T04_05_06_280Z-debug-0.log, docs/decisions/architecture/0003-billing-callbacks.md, docs/decisions/architecture/0004-billing-domain-events.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 30.454 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 8 response lines; changed files `.cache/npm/_logs/2026-11-09T04_05_40_058Z-debug-0.log, docs/decisions/architecture/0003-billing-callbacks.md, docs/decisions/architecture/0004-billing-domain-events.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 26.317 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a new ADR that supersedes ADR-0003; only ADR-0003's status line changes.

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
