# retro: claude outcome-7

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-7` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `62fba30d5c3d3c708c04b7ababd51a1066bd58a1`, actual bytes SHA-256 `0cfbcfddbbf901d5a599d64a1eec00cdb3b694b4f134b046298bad984696a300`; dirty: `False`.
- **Fixture.** `outcome-7`, SHA-256 `1e150473e8d87eae1e2dbbb6d4a04dab533a1086c2e3ccafb5f40ceb7d386d48`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/retro Prepare a local issue draft and compare only the two named similar sessions.

Supplied task context:
Use only the authorized history/index.json, history/session-target.jsonl and the supplied incident files. Report only, except outcome-specific export or local-draft authority stated here. No real issue posting or remote access. Compare only history/session-target.jsonl and history/session-child.jsonl. Search the local issue inventory incident/local-issues.json. Write a local draft to scratch/issue-draft.md; no posting.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 9 | 0 |
| baseline | n/a | false | 3 | 0 |

Treatment: 31 response lines; changed files `.cache/npm/_logs/2026-11-09T04_57_12_975Z-debug-0.log, .fixture/events.jsonl, .git/index, scratch/issue-draft.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 81.179 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `.cache/npm/_logs/2026-11-09T04_58_52_368Z-debug-0.log, .fixture/events.jsonl, .git/index, scratch/issue-draft.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 45.055 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: "Prepare a local issue draft and compare only the two named similar sessions." Expect: relevant issue search, bounded signature checks and exact hit/miss/unknown pointers; no issue posting or fixed analyst panel.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-7-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-7-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Superseded outcome review

The later isolation audit invalidated this comparison. The earlier judgment is retained for provenance.

Value: **hurt**. Baseline criterion: yes; treatment criterion: partial.

Treatment adds explicit local issue searches and bounded signature hit/miss pointers, but its batch read also opens history/conventions.md outside the named history scope; baseline does not. Both write only a local issue draft, do not post, and identify the child as a dependent summary. The extra history read is a scope regression, admitted in the response and visible in the trace. Causality from one pair is uncertain; retain as unresolved hurt and mark retro unevaluated.

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
