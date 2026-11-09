# correct: claude activation-2

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `128a093fe9da0261e4b78fc8bafb7739b5615820`, actual bytes SHA-256 `9a08bf9e19968ba1182be5e01b3640dcba12c038b753bc292a0da3057b8b9181`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `1e6265b989ceaeea694edecddc96ee2ae8bb564f363771dba76a7c50a802f577`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Make it impossible to forget the `await` on `db.query` again.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 13 | 0 |
| baseline | false | false | 7 | 0 |

Treatment: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T03_31_19_570Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_32_51_736Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_32_55_680Z-debug-0.log, .cache/npm/_logs/2026-11-09T03_32_59_131Z-debug-0.log, .cache/npm/_update-notifier-last-checked, scripts/check-query-await.mjs, src/app.js, tests/query-await.test.mjs`; removed files `none`; validation command present: `requires review`. Workflow cost: 122.714 seconds and 13 tool calls; token usage is in the JSON record.

Baseline: 13 response lines; changed files `.cache/npm/_logs/2026-11-09T03_33_31_479Z-debug-0.log, src/app.js, tests/source-guard.test.mjs`; removed files `none`; validation command present: `requires review`. Workflow cost: 47.945 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a type or lint remedy whose error names the fix, proven against the earlier mistake.

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

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
