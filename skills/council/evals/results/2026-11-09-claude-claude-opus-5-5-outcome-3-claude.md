# council: claude outcome-3

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `645edc1b3f8b5c5c00854bc61d0d6fc29130ffbc`, actual bytes SHA-256 `b24055566d7c79f421cbb22a5ec0337e4290b06d7d90fb76b6c3191c0957771d`; dirty: `False`.
- **Fixture.** `outcome-3`, SHA-256 `c6a4f6092a051f8dcda2bda3debfd28763fe8dc66a92e944630fb3195124812f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/council Council: repair the approved code slice; round three still has an unresolved required probe.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 15 | 0 |
| baseline | n/a | false | 10 | 0 |

Treatment: 22 response lines; changed files `.cache/npm/_logs/2026-11-09T04_59_29_928Z-debug-0.log, dist/index.mjs, review/existing-run/DECISIONS.md, review/existing-run/LOG.md, review/existing-run/PLAN.md, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 78.026 seconds and 15 tool calls; token usage is in the JSON record.

Baseline: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T05_01_25_143Z-debug-0.log, dist/index.mjs, review/existing-run/DECISIONS.md, review/existing-run/LOG.md, review/existing-run/PLAN.md, review/existing-run/raw/r3-probes.txt, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 65.583 seconds and 10 tool calls; token usage is in the JSON record.


Expected deliverable: "Council: repair the approved code slice; round three still has an unresolved required probe." Expect: the parent's declared shared budget and open finding survive; unanimity or exhaustion cannot become agreement.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Superseded outcome review

The later isolation audit invalidated this comparison. The earlier judgment is retained for provenance.

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Both restore the two-line export implementation, run exact-value consumers, preserve staff-only API/declarations, retain H-NATIVE open and stop at round3/3. Both keep4/6 worker starts, adding zero; no independent review claim.

## Bash temporary isolation correction

This comparison is invalid because Bash scratch or output used the shared UID temporary root. Its trace remains local; cross-arm contamination cannot be excluded.
