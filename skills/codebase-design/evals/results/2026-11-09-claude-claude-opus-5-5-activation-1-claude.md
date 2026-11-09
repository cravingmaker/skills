# codebase-design: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `d8fc38b8ce045ab310577b5b2056b24d92ffcd90`, actual bytes SHA-256 `07ffdfc28750768242eb6b4d12385f325e18b4f6f5e9aeef8e5dc7690e3c01a1`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `4c7f4e00bc441adc626f7ff1cecd9a21aef5165b2ad6f4b1627bbdd4a0f20a8a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
This OrderService has twelve public methods and every caller strings four of them together. How should its interface look?

Task context supplied identically to both arms:
Relevant source: src/billing, src/rate_limiter.py, src/api.py, src/job_runner.py, src/plugin_loader.py and src/sync.py. Domain configuration: docs/agents/domain.md. History is an exported synthetic text capture, not live Git. Design/report only; no product edits.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 7 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T04_58_02_488Z-debug-0.log, scratch/__pycache__/order_service_sketch.cpython-315.pyc, scratch/order_service_sketch.py, scratch/probe_place.py, scratch/tmp/order_service_interface.md, src/billing/__pycache__/order_service.cpython-315.pyc, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 67.531 seconds and 7 tool calls; token usage is in the JSON record.

Baseline: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T04_59_54_421Z-debug-0.log, scratch/tmp/order-service-interface.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 38.855 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the skill loads; the answer judges depth at the interface, applies the deletion test and proposes a smaller interface that hides the sequencing.

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
