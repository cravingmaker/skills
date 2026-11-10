# project-guardrails: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `7af466aad380e89b419f204d52baed99995023c3`, tree `b7f67884fe8c374e3890bc7c5dede0d762a482a6`, actual bytes SHA-256 `957cd054f871774c2d2616f005bfd6ad3f1a6b9599822320957a55750de5bed9`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/guardrails`, SHA-256 `c1791385097e3fd87d062d5bc927dbd84f2a68c73dabeabefcd9a6e12748a9ed`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [project-guardrails.tar.gz](https://drive.google.com/file/d/1fSH2U9UNI7IIVPu9ccStaHEcXIb9BsK5/view), folder `2026-11-08-claude-claude-opus-5-5-activation-3/` inside.

## Prompt

```text
Harden the CI workflows.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 11 | 0 |
| baseline | false | false | 6 | 0 |

Treatment: 35 response lines; changed files `.github/workflows/check.yml, package.json`; removed files `none`; validation command present: `requires review`. Workflow cost: 81.602 seconds and 11 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `.github/workflows/check.yml, package.json`; removed files `none`; validation command present: `requires review`. Workflow cost: 53.502 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: pinned SHAs, least-privilege `permissions`, and workflow analysis assessed and proven, without unrelated changes.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-claude-opus-5-5-activation-3/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-3/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-3/baseline/artifacts/`.
