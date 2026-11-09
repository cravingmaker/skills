# interrogate: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `0081bf09a0026d92425cd3411cd4f11590c1e7ee`, actual bytes SHA-256 `79eaf31d8a5ea0aa326a2701a5142991eea5f5cea45e815469bc0d4380d7eead`; dirty: `True`.
- **Fixture.** `activation-2`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/interrogate

Interrogate the modified package exports using the providers I specified.

Task context supplied identically to both arms:
Read review/scope.md, review/change.diff, approved issue and CONTRIBUTING.md. Snapshot-only fixture has no live Git metadata; use exported before/current bytes and hashes without inventing commit resolution. Local Node probes `node consumer/main.mjs` and `node consumer/cli.mjs` hit the actual package. No native tool or delegation provider is callable. Report requested unavailable seats honestly. No commits or remote writes. Shared ceiling: 2 concurrent agents, 6 total starts including replacements; 3 rounds maximum. No actual additional model starts are authorized by the eval guard. Requested seats Sol and Claude; neither callable. Preserve H-NATIVE as an unrun allegation.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 9 | 0 |
| baseline | false | false | 6 | 0 |

Treatment: 77 response lines; changed files `.cache/npm/_logs/2026-11-09T14_59_14_656Z-debug-0.log, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 87.443 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 51 response lines; changed files `.cache/npm/_logs/2026-11-09T15_01_11_316Z-debug-0.log, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 52.952 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the parent traces affected callers, preserves requested seats and reports unavailable providers honestly.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-round2-fix2-quota-retry-claude/baseline/artifacts/`.
