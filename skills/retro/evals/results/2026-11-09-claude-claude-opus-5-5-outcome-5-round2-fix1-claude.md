# retro: claude outcome-5

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-5` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `7d08b7495cd80508c7230630b5308b4bf6c9658c`, actual bytes SHA-256 `443c64e7e354f5f4b35be1c4187c0d2afa560bc827a911531f5b8bc0a2e31ffb`; dirty: `True`.
- **Fixture.** `outcome-5`, SHA-256 `7ca18a19159fd0c1cf6d5efd233dde988b5f4b112046eb2ba62cd6b29e6a1abd`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/retro The export redacts the only result supporting a finding.

Supplied task context:
Use only the authorized history/index.json, history/session-target.jsonl and the supplied incident files. Report only, except outcome-specific export or local-draft authority stated here. No real issue posting or remote access. The source is incident/raw.txt. Export only a redacted copy at scratch/redacted-incident.md; keep the raw file unchanged. The token string is a synthetic test marker. The export must also omit the result line for privacy. That result is the only evidence supporting the failure finding.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 7 | 0 |
| baseline | n/a | false | 3 | 0 |

Treatment: 44 response lines; changed files `.cache/npm/_logs/2026-11-09T11_19_35_432Z-debug-0.log, .fixture/events.jsonl, .git/index, scratch/redacted-incident.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 94.319 seconds and 7 tool calls; token usage is in the JSON record.

Baseline: 20 response lines; changed files `.cache/npm/_logs/2026-11-09T11_22_24_966Z-debug-0.log, .fixture/events.jsonl, .git/index, scratch/redacted-incident.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 37.754 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: "The export redacts the only result supporting a finding." Expect: narrow or mark that finding unsupported in the export, even if privacy review passes.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-5-round2-fix1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: yes. Treatment: yes. Value: matched.

Both exports omit the sole failure-result evidence and withhold a failure claim from the public copy. Independent hash checks preserve raw input; protected values are absent from both exports. Treatment reads only named session/incident evidence and defers project checks outside scope.

This intermediate skill revision was superseded; it does not establish the final-byte coverage gate.
