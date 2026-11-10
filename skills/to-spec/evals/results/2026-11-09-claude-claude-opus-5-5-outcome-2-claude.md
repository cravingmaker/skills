# to-spec: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `3407cb8d65a8b6749edb784778f9077683f1e3ec`, actual bytes SHA-256 `14e3f9478478a86870db323071f754380c6c8caf6cc63ad7c3f12c40abf17326`; dirty: `False`.
- **Fixture.** `outcome-2`, SHA-256 `73fec0d7fb4088ef7969634837226a6f96eb91bfa95ee190c49feff5508cbcfd`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [to-spec.tar.gz](https://drive.google.com/file/d/1o-lmAqCyGzRuDWEfzjqUPXkj4q1I3y9y/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/` inside.

## Prompt

```text
/to-spec

Use the `to-spec` skill explicitly for this request.

to-spec

Task context supplied to both arms:
Prior settled discussion: Save, list, and rerun named searches for the signed-in shopper; reject blank names; newest first. Use local per-user JSON; no sharing/cloud sync. CLI surface is agreed. No implementation is authorized.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 4 | 0 |
| baseline | n/a | false | 2 | 0 |

Treatment: 89 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 86.105 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 24 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 33.157 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: Every user story has an acceptance line and a proof naming a real surface and an observable result.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **added**. Baseline criterion: partial; treatment criterion: yes.

Treatment returns the complete draft with acceptance and CLI/observable-result Proof for all three stable stories. Baseline points at the existing approved spec and lists gaps without producing the requested full draft.
