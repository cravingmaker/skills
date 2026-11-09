# to-tickets: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `53fcbe1f3ae919ea22005551d33abacb7444ae55`, actual bytes SHA-256 `c2c9142422c2683ce739a32d14977452722ef88981b15a86793613fcc5911dab`; dirty: `False`.
- **Fixture.** `outcome-2`, SHA-256 `af79da0050468f3b01cd23ff3d23060375969a6dcb93f61c4cdf0cfc0c30f5b5`.
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
The numbered breakdown is approved for filing at the configured local tracker destination. No implementation or run plan is authorized.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 8 | 0 |
| baseline | n/a | false | 4 | 0 |

Treatment: 29 response lines; changed files `.cache/npm/_logs/2026-11-09T03_26_18_721Z-debug-0.log, .planning/work-items/01-save-a-named-search.md, .planning/work-items/02-list-the-current-shoppers-searches.md, .planning/work-items/03-rerun-a-saved-search.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 63.955 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T03_30_37_928Z-debug-0.log, .planning/work-items/search/01-save-named-search.md, .planning/work-items/search/02-list-shopper-searches.md, .planning/work-items/search/03-rerun-saved-search.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 42.84 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Every filed `Blocked by:` line is `None` or comma-separated existing ticket numbers, and `import-tickets.py` reports no `FAIL` lines for the filed directory.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **added**. Baseline criterion: partial; treatment criterion: yes.

Both file numbered tickets with resolvable blockers. Treatment additionally runs the required importer and observes exit 0/no FAIL; baseline does not execute that validation. Different chosen root/subdirectory placement is documented as an ambiguous fixture destination, not a proven path violation.
