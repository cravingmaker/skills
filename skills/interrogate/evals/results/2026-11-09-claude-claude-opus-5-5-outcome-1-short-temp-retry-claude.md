# interrogate: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `cc4504551018db1215dcf2d1de2c8e6b6d8b8efc`, actual bytes SHA-256 `26a6696583268d0cd399453894389ac26189c7f01996cfc3e025effcc1456618`; dirty: `False`.
- **Fixture.** `outcome-1`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/interrogate Interrogate a fixture with a static missing export, a failing runtime probe and an unrun timing allegation.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 12 | 0 |
| baseline | n/a | false | 4 | 0 |

Treatment: 47 response lines; changed files `.cache/npm/_logs/2026-11-09T05_35_24_198Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 96.85 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 29 response lines; changed files `.cache/npm/_logs/2026-11-09T05_38_26_998Z-debug-0.log, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 48.263 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: "Interrogate a fixture with a static missing export, a failing runtime probe and an unrun timing allegation." Expect: the static proof remains valid, the runtime defect includes the run evidence, and the timing claim remains unresolved under its stable ID.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-short-temp-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Fresh private-temp pair: both preserve deterministic missing-export proof, reproduce the exact-string/null/unknown-field regression at real consumers with a base control, and leave H-NATIVE unrun under its stable ID. No product edit or independent provider claim occurs.
