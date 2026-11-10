# wayfinder: claude activation-3

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `4fbc19104eb3977020c3b7730ec008e2fed3b747`, actual bytes SHA-256 `9aa5238f82f9edd5f4c8580e0b7b34e7d8e4c38d8d89fc51c271b3be96a9aea7`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `43f69dc739f9cee03070b38e81012548f0b82c46c64b6d47e5930c45ff619299`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [wayfinder.tar.gz](https://drive.google.com/file/d/1JwLCmS9xRZYC3csBrCeIgzvtDKp-oyrQ/view), folder `2026-11-09-claude-claude-opus-5-5-activation-3-claude/` inside.

## Prompt

```text
/wayfinder

Use the `wayfinder` skill explicitly for this request.

wayfinder: chart this on our GitHub tracker; you can create the issues.

Task context supplied to both arms:
Prior destination agreed: identify the minimal reliable REST-to-events design before any implementation. Postgres storage is settled. Durable delivery, ordering, and migration boundary remain open. Publishing may use the configured tracker only; tools/network are unavailable in this fixture.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 10 | 0 |
| baseline | false | unavailable | unavailable | 1 |

Treatment: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T04_06_16_655Z-debug-0.log, .scratch/event-backend/issues/01-inventory-ordering-billing-callbacks.md, .scratch/event-backend/issues/02-billing-consumer-readiness.md, .scratch/event-backend/issues/03-durable-delivery-guarantee.md, .scratch/event-backend/issues/04-event-ordering-scope.md, .scratch/event-backend/issues/05-migration-boundary.md, .scratch/event-backend/map.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 66.735 seconds and 10 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the map and tickets created on the configured tracker through its wayfinding operations.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json` (local only, not committed).

## Invalid comparison

- claude baseline failed (exit 1, timeout False); inspect stderr and trace

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/artifacts/`.
