# to-tickets: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `53fcbe1f3ae919ea22005551d33abacb7444ae55`, actual bytes SHA-256 `c2c9142422c2683ce739a32d14977452722ef88981b15a86793613fcc5911dab`; dirty: `False`.
- **Fixture.** `outcome-1`, SHA-256 `f04ad174d7ac6bd75acaf80bb590cd45ce5a50be2d7b8898978ce40fd542058a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [to-tickets.tar.gz](https://drive.google.com/file/d/1Yma5TJENr43nnGVl4saovTa9TOBF-C1O/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/` inside.

## Prompt

```text
/to-tickets Check the three supplied worked-tickets files against docs/specs/saved-searches.md using the installed work-decomposition importer with its explicit spec option. Report whether titles, status, Proof, acceptance and blockers survive unchanged. Do not modify inputs or start execution.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 5 | 0 |
| baseline | n/a | false | 5 | 0 |

Treatment: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T05_40_35_849Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 40.31 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T05_42_13_191Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 50.374 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: The worked example in `references/ticket-template.md` imports with `import-tickets.py --spec`, carrying titles, status, Proof, acceptance, and blockers exactly (`tests/to-tickets/run.sh`).

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Fresh private-temp pair: both execute the installed importer with --spec, compare titles/status/Proof/acceptance/blocker strings exactly for all three worked tickets, preserve source/spec hashes and leave placeholders unresolved. Neither modifies inputs, creates a run plan or starts execution.
