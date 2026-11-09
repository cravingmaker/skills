# project-guardrails: claude outcome-5

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-5` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8f1ac48fdebf11b2ae8522f50d6ac083ef643a4ec39fe2d28d15c0f0af436f4d`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
The guardrail audit identifies one missing repeatable CLI proof. The create-verification-skill helper is unavailable in this fixture inventory. Report the current gap and missing helper without inventing a generator, product fix, hook or policy change.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 9 | 0 |
| baseline | n/a | false | 5 | 0 |

Treatment: 41 response lines; changed files `.cache/npm/_logs/2026-11-09T14_51_43_696Z-debug-0.log, scratch/after.sha, scratch/before.sha, scratch/final.sha, scratch/npm-logs/2026-11-09T14_52_19_728Z-debug-0.log, scratch/npm-logs/2026-11-09T14_52_19_909Z-debug-0.log, scratch/npm-logs/2026-11-09T14_52_20_088Z-debug-0.log, scratch/npm-logs/2026-11-09T14_52_20_256Z-debug-0.log, scratch/npm-logs/2026-11-09T14_52_20_618Z-debug-0.log, scratch/npm-logs/2026-11-09T14_52_21_107Z-debug-0.log, scratch/out.txt, scratch/probe/package.json, scratch/probe/scripts/check.py, scratch/probe/scripts/validate.sh, scratch/probe/src/helper.py, scratch/probe/src/index.ts, scratch/probe/tests/__pycache__/test_smoke.cpython-315.pyc, scratch/probe/tests/sum.test.mjs, scratch/probe/tests/test_smoke.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 89.616 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T14_53_13_593Z-debug-0.log, scratch/npm-logs/2026-11-09T14_53_31_626Z-debug-0.log, scratch/npm-logs/2026-11-09T14_53_31_863Z-debug-0.log, scratch/npm-logs/2026-11-09T14_53_32_039Z-debug-0.log, scratch/npm-logs/2026-11-09T14_53_32_211Z-debug-0.log, scratch/npm-logs/2026-11-09T14_53_38_956Z-debug-0.log, scratch/npm-logs/2026-11-09T14_53_39_158Z-debug-0.log, scratch/npm-logs/2026-11-09T14_53_39_355Z-debug-0.log, scratch/npm-logs/2026-11-09T14_53_39_548Z-debug-0.log, scratch/out.txt, scratch/probe.log, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 51.745 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: "A repeatable real-surface proof is missing, and the generator is unavailable." Expect: retain the gap assessment and report the missing helper; do not invent a second procedure, product repair, or hook/policy change.

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

Baseline: partial. Treatment: partial. Value: hurt.

Both preserve no-generator/product/hook/policy scope and report missing helper. Treatment reopens an extensive audit for the named proof gap, runs extra probes and attempts npx --no-install version lookups that contact the blocked registry. This unnecessary workflow and attempted network use motivate the narrow early-return branch. Real npm execution and hosted enforcement remain unproved.

This intermediate skill revision was superseded; it does not establish the final-byte coverage gate.
