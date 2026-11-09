# retro: claude outcome-4

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-4` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `62fba30d5c3d3c708c04b7ababd51a1066bd58a1`, actual bytes SHA-256 `0cfbcfddbbf901d5a599d64a1eec00cdb3b694b4f134b046298bad984696a300`; dirty: `False`.
- **Fixture.** `outcome-4`, SHA-256 `7ca18a19159fd0c1cf6d5efd233dde988b5f4b112046eb2ba62cd6b29e6a1abd`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/retro Export the cited incident evidence, redacting a token and private repository name.

Supplied task context:
Use only the authorized history/index.json, history/session-target.jsonl and the supplied incident files. Report only, except outcome-specific export or local-draft authority stated here. No real issue posting or remote access. The source is incident/raw.txt. Export only a redacted copy at scratch/redacted-incident.md; keep the raw file unchanged. The token string is a synthetic test marker.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 7 | 0 |
| baseline | n/a | false | 2 | 0 |

Treatment: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T04_57_11_648Z-debug-0.log, .fixture/events.jsonl, .git/index, scratch/redacted-incident.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 46.514 seconds and 7 tool calls; token usage is in the JSON record.

Baseline: 14 response lines; changed files `.cache/npm/_logs/2026-11-09T04_58_27_840Z-debug-0.log, .fixture/events.jsonl, .git/index, scratch/redacted-incident.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 17.825 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: "Export the cited incident evidence, redacting a token and private repository name." Expect: redact copies consistently, retain safe source markers, verify privacy and finding support separately, and leave raw records unchanged.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-4-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Superseded outcome review

The later isolation audit invalidated this comparison. The earlier judgment is retained for provenance.

Value: **added**. Baseline criterion: partial; treatment criterion: yes.

Both exports remove the two private values and preserve the exact raw hash. Treatment additionally retains line markers, category/count log and explicit evidence limits separately from privacy; baseline export lacks those support limits. the local audit receipt independently checks bytes.

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
