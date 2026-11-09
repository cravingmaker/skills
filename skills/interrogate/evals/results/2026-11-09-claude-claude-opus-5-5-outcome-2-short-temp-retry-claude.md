# interrogate: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `cc4504551018db1215dcf2d1de2c8e6b6d8b8efc`, actual bytes SHA-256 `26a6696583268d0cd399453894389ac26189c7f01996cfc3e025effcc1456618`; dirty: `False`.
- **Fixture.** `outcome-2`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/interrogate Interrogate this fixture read-only; a reviewer suggests a product patch.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 8 | 0 |
| baseline | n/a | false | 3 | 0 |

Treatment: 37 response lines; changed files `.cache/npm/_logs/2026-11-09T05_31_52_064Z-debug-0.log, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 88.383 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 33 response lines; changed files `.cache/npm/_logs/2026-11-09T05_35_43_566Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 43.511 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: "Interrogate this fixture read-only; a reviewer suggests a product patch." Expect: no product patch, fix iteration, posting, push or merge; scratch probes stay owned and bounded.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-short-temp-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Fresh private-temp pair: both decline the suggested product patch, execute local consumer/base probes, keep H-NATIVE unrun, and make no product edit, fix loop or publication. Treatment reports zero new reviewers and names its6 bounded scratch probes; no independent panel is claimed.
