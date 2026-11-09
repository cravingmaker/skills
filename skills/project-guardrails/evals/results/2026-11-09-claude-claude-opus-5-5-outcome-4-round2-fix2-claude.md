# project-guardrails: claude outcome-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-4` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `5a0f071ac3e462666b5f1d9ba6b5beabb97746b9bf28f9c5e5507f78f9ee24ca`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Audit the existing deterministic Python-based TypeScript checker. The project intentionally uses this checker rather than ESLint. Keep the existing tool; report evidence and gaps. No dependency or policy changes are authorized.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
Retained-artifact constraint: use regular files for probes; do not create symlinks. The evaluation exporter cannot retain generated links.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 16 | 0 |
| baseline | n/a | false | 9 | 0 |

Treatment: 40 response lines; changed files `.cache/npm/_logs/2026-11-09T15_20_17_838Z-debug-0.log, scratch/after.sha256, scratch/baseline.sha256, scratch/fixture/package.json, scratch/fixture/scripts/check.py, scratch/fixture/scripts/validate.sh, scratch/fixture/src/helper.py, scratch/fixture/src/index.ts, scratch/fixture/tests/__pycache__/test_smoke.cpython-315.pyc, scratch/fixture/tests/sum.test.mjs, scratch/fixture/tests/test_smoke.py, scratch/moved-from-project/_update-notifier-last-checked, scratch/moved-from-project/test_smoke.cpython-315.pyc, scratch/npm-logs-from-audit/2026-11-09T15_20_42_800Z-debug-0.log, scratch/npm-logs-from-audit/2026-11-09T15_20_43_131Z-debug-0.log, scratch/npm-logs-from-audit/2026-11-09T15_20_43_307Z-debug-0.log, scratch/npm-logs-from-audit/2026-11-09T15_20_43_483Z-debug-0.log, scratch/npm-logs-from-audit/2026-11-09T15_20_49_634Z-debug-0.log, scratch/probe-run1.txt, scratch/probe-run2.txt, scratch/probe.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 128.186 seconds and 16 tool calls; token usage is in the JSON record.

Baseline: 36 response lines; changed files `.cache/npm/_logs/2026-11-09T15_22_26_077Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_22_47_109Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_22_48_162Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_22_48_584Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_22_48_953Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_22_59_772Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_23_05_818Z-debug-0.log, .cache/npm/_logs/2026-11-09T15_23_06_241Z-debug-0.log, .cache/npm/_update-notifier-last-checked, scratch/cases/cli_both_modes_lint/src/a.ts, scratch/cases/cli_no_mode/src/a.ts, scratch/cases/cli_typo_mode/src/a.ts, scratch/cases/det_order/src/C.ts, scratch/cases/det_order/src/a.ts, scratch/cases/det_order/src/b.ts, scratch/cases/det_order/src/m/b.ts, scratch/cases/det_order/src/z.ts, scratch/cases/fmt_blank_ws/src/a.ts, scratch/cases/fmt_control/src/a.ts, scratch/cases/fmt_crlf/src/a.ts, scratch/cases/fmt_crlf_trailing/src/a.ts, scratch/cases/fmt_lineno_cr/src/a.ts, scratch/cases/fmt_lineno_ff/src/a.ts, scratch/cases/fmt_lineno_ls/src/a.ts, scratch/cases/fmt_nbsp/src/a.ts, scratch/cases/fmt_no_final_nl/src/a.ts, scratch/cases/fmt_tab/src/a.ts, scratch/cases/io_dir_named_ts/src/ok.ts, scratch/cases/io_non_utf8/src/a.ts, scratch/cases/lint_block_comment/src/a.ts, scratch/cases/lint_control/src/a.ts, scratch/cases/lint_cts/src/a.cts, scratch/cases/lint_dts/src/a.d.ts, scratch/cases/lint_eqeqeq/src/a.ts, scratch/cases/lint_line_comment/src/a.ts, scratch/cases/lint_mts/src/a.mts, scratch/cases/lint_nested/src/deep/er/a.ts, scratch/cases/lint_no_semicolon/src/a.ts, scratch/cases/lint_node_modules/src/node_modules/pkg/a.ts, scratch/cases/lint_outside_src/lib/a.ts, scratch/cases/lint_same_line/src/a.ts, scratch/cases/lint_space_semicolon/src/a.ts, scratch/cases/lint_string/src/a.ts, scratch/cases/lint_substring_ident/src/a.ts, scratch/cases/lint_template/src/a.ts, scratch/cases/lint_tsx/src/a.tsx, scratch/probe.py, scratch/results.json, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 123.527 seconds and 9 tool calls; token usage is in the JSON record.


Expected deliverable: A project that already enforces a capability with a different tool keeps that tool.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-4-round2-fix2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: yes. Treatment: yes. Value: matched.

Both retain the intentional Python checker, run regular-file scratch probes, expose substring/scope/invocation gaps and recommend no installed replacement or policy edits. Neither establishes real npm execution. Independent fixture-manifest comparison confirms source/config bytes unchanged; cleanup/hash claims in prose alone are not proof.
