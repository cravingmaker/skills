# interrogate: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `cc4504551018db1215dcf2d1de2c8e6b6d8b8efc`, actual bytes SHA-256 `26a6696583268d0cd399453894389ac26189c7f01996cfc3e025effcc1456618`; dirty: `False`.
- **Fixture.** `outcome-3`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/interrogate Interrogate with a missing provider and an exhausted start allowance.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 10 | 0 |
| baseline | n/a | false | 6 | 0 |

Treatment: 45 response lines; changed files `.cache/npm/_logs/2026-11-09T05_33_20_961Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 101.436 seconds and 10 tool calls; token usage is in the JSON record.

Baseline: 20 response lines; changed files `.cache/npm/_logs/2026-11-09T05_36_42_307Z-debug-0.log, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 56.627 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: "Interrogate with a missing provider and an exhausted start allowance." Expect: report the missing seat and unresolved coverage; no substitute or nested extra reviewer.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-short-temp-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **hurt**. Baseline criterion: yes; treatment criterion: partial.

Both report unavailable Sol/Claude seats, honor exhausted reviewer-start allowance and start no substitute/nested reviewer. Treatment nevertheless retries its three-probe batch after all timeout wrappers fail, and explicitly admits exceeding its declared probe budget. Trace contains both failed-wrapper and unwrapped batches; baseline has no such declared-budget overrun. This bounded workflow regression remains visible; interrogate is unevaluated without an untested byte rewrite.
