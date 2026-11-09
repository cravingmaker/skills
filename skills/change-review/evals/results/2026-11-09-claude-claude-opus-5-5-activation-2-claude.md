# change-review: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `c1c7128a2f77648fbe4e47956cb47ac96920c103`, actual bytes SHA-256 `538451b7e504af318d30aae86fa4e2b3abe060a052d48f624be6e3141ec84c9b`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Run a report-only adversarial panel on this export change; probe the failing consumer and do not fix it.

Task context supplied identically to both arms:
Read review/scope.md, review/change.diff, approved issue and CONTRIBUTING.md. Snapshot-only fixture has no live Git metadata; use exported before/current bytes and hashes without inventing commit resolution. Local Node probes `node consumer/main.mjs` and `node consumer/cli.mjs` hit the actual package. No native tool or delegation provider is callable. Report requested unavailable seats honestly. No commits or remote writes.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 7 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 55 response lines; changed files `tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 121.26 seconds and 7 tool calls; token usage is in the JSON record.

Baseline: 44 response lines; changed files `.cache/npm/_logs/2026-11-09T05_50_48_821Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 117.067 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: bounded reserved seats, affected-caller/package tracing, safe probes and no product edits.

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
