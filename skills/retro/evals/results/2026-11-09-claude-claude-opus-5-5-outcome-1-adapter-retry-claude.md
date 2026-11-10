# retro: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `62fba30d5c3d3c708c04b7ababd51a1066bd58a1`, actual bytes SHA-256 `0cfbcfddbbf901d5a599d64a1eec00cdb3b694b4f134b046298bad984696a300`; dirty: `False`.
- **Fixture.** `outcome-1`, SHA-256 `3a5e6b81ae30042874d408d627a1d20c646874981ee0b0483f0ac3052e8fdfc6`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [retro.tar.gz](https://drive.google.com/file/d/1fuZeOlMvToGWFavSPGMb9rRp57N9rE7Q/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/` inside.

## Prompt

```text
/retro An instruction says to add another rule for a repeated banned import, but the repo linter already has an unwired check. What should change?

Supplied task context:
Use only the authorized history/index.json, history/session-target.jsonl and the supplied incident files. Report only, except outcome-specific export or local-draft authority stated here. No real issue posting or remote access. Incident evidence is history/import-incidents.md; inspect the existing validator and check.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 9 | 0 |
| baseline | n/a | false | 4 | 0 |

Treatment: 39 response lines; changed files `.cache/npm/_logs/2026-11-09T05_23_05_789Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 139.823 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T05_28_50_530Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 43.546 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: "An instruction says to add another rule for a repeated banned import, but the repo linter already has an unwired check. What should change?" Expect: check-over-prose selects wiring or repairing the existing mechanism, with recurrence and reject/accept/repeat evidence, rather than another instruction.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-adapter-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **added**. Baseline criterion: partial; treatment criterion: yes.

Both reject another prose rule and find the unwired import check. Treatment explicitly executes reject/accept/repeat cases, locates the actual required unittest/forge gate instead of inventing a missing validate.sh entry point, and defers broader AST enforcement beyond the observed exact import. No product edits occur.
