# to-tickets: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `53fcbe1f3ae919ea22005551d33abacb7444ae55`, actual bytes SHA-256 `c2c9142422c2683ce739a32d14977452722ef88981b15a86793613fcc5911dab`; dirty: `False`.
- **Fixture.** `outcome-3`, SHA-256 `af79da0050468f3b01cd23ff3d23060375969a6dcb93f61c4cdf0cfc0c30f5b5`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/to-tickets

Use the `to-tickets` skill explicitly for this request.

to-tickets docs/specs/saved-searches.md

Task context supplied to both arms:
Prior settled discussion: Save, list, and rerun named searches for the signed-in shopper; reject blank names; newest first. Use local per-user JSON; no sharing/cloud sync. CLI surface is agreed. No implementation is authorized.

Supplied task context:
Prepare the breakdown for review only. The parent and approved spec are immutable inputs; execution is not authorized.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 3 | 0 |
| baseline | n/a | false | 3 | 0 |

Treatment: 47 response lines; changed files `.cache/npm/_logs/2026-11-09T03_26_37_955Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 51.908 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 52 response lines; changed files `.cache/npm/_logs/2026-11-09T03_29_51_794Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 52.525 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: The parent issue and the spec are unchanged, and no implementation or run plan is started.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Both return breakdowns for review, preserve the parent/spec/product bytes and start neither implementation nor a run plan. Only incidental npm cache logs are written.
