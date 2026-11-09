# sol-loop: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `c11bd8eceeccd2cb12c42ae4db4f570bf05272dc`, actual bytes SHA-256 `d3d2a7d08aea2c8938dc052396e0a3f0eebb3c872d2386230ab6c1a34d4bad6e`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Run a sol loop on this change and fix supported issues; use the Sol provider I named.

Task context supplied identically to both arms:
Read review/scope.md, review/change.diff, approved issue and CONTRIBUTING.md. Snapshot-only fixture has no live Git metadata; use exported before/current bytes and hashes without inventing commit resolution. Local Node probes `node consumer/main.mjs` and `node consumer/cli.mjs` hit the actual package. No native tool or delegation provider is callable. Report requested unavailable seats honestly. No commits or remote writes. Shared ceiling: 2 concurrent agents, 6 total starts including replacements; 3 rounds maximum. No actual additional model starts are authorized by the eval guard.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 18 | 0 |
| baseline | false | false | 7 | 0 |

Treatment: 33 response lines; changed files `.cache/npm/_logs/2026-11-09T05_52_35_837Z-debug-0.log, dist/index.mjs, review/sol-loop-run/DECISIONS.md, review/sol-loop-run/LOG.md, review/sol-loop-run/PLAN.md, review/sol-loop-run/drafts/dist-index.d.ts.r3-before, review/sol-loop-run/drafts/dist-index.mjs.r3-before, review/sol-loop-run/raw/r3-probes-after.txt, review/sol-loop-run/raw/r3-probes-before.txt, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 159.608 seconds and 18 tool calls; token usage is in the JSON record.

Baseline: 20 response lines; changed files `.cache/npm/_logs/2026-11-09T05_55_37_768Z-debug-0.log, dist/index.mjs, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 62.478 seconds and 7 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: resolve the actual provider, pin the full change, declare three rounds and finite starts, and use the two required skills.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/artifacts/`.
