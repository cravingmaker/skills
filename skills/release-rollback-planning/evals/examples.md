# Examples

These cases are prepared for paired runs with and without the skill; no model runs are claimed.

## Activation

- "How do we roll back this risky deploy, and how long does the tested undo take?" Expect: exact source/target/authority, retained artifact/config identities, schema compatibility, decision criteria and a measured disposable staging drill through user-path recovery.
- "Our last rollback was slow and the GitOps controller restored the bad version." Expect: desired-state reconciliation handling and a repeatable drill on the deployed controller policy; no production mutation from planning.
- "This release contracts the schema; can old code still run?" Expect: evidence for actual old-code dependencies, cannot-undo effects and compatible rollback or a reviewed roll-forward candidate; no blanket claim that every contraction breaks old code.

## Near miss

- "Run the engineering plugin deploy-checklist for release go/no-go." Expect: the requested release checklist; the rollback plan is an input.
- "Generate our changelog and release tags." Expect: release-automation.
- "Author the expand-contract PostgreSQL migration." Expect: postgres-migrations.
- "Coordinate the live outage with the engineering plugin incident-response." Expect: the requested incident coordinator; planning supplies no execution authority.
- "Upgrade the PostgreSQL engine between major versions." Expect: postgres-version-upgrades.

## Outcome

- "Reject mutable recovery inputs." Fixture: copy tests/release-rollback-planning/fixtures/ready.json and create drill.txt beside it containing synthetic test evidence. Replace previous.artifact with a tag and candidate.config with main. Expect: artifact_not_digest, config_not_pinned and drill binding findings, with no command execution or source values in output.
- "Invalidate a changed plan." Fixture: the filled plan and receipt above have a recorded drill.plan_sha256 for the canonical JSON excluding drill. Change a rollback command, target or config after the drill. Expect: drill_stale; changing only a digest cannot establish a new rehearsal.
- "Preserve config-only recovery." Fixture: previous and candidate artifacts match but their retained configs differ; the drill records those exact configs and recovered artifact. Expect: structural pass. If both artifact and config match, expect same_state.
- "Require compatible, bounded recovery." Fixture: a filled plan says previous_code_compatible false with strategy rollback, or records a drill above its budget, on the deployment target, or with user_path_check.passed false. Expect: schema, budget, target or user-path rejection. A roll-forward plan needs separate pinned repair artifact/config identities, compatible repair commands and a drill of that selected action. With incompatible previous A, failed candidate B and reviewed repair C, the C/C-config recovery passes; recovered B or the wrong repair config fails.
- "Keep a starter visibly incomplete." Fixture: run the checker on assets/rollback-plan.json, then try duplicate-key or non-finite JSON containing an inert synthetic credential. Expect: starter findings or malformed-input exit 2, no credential output and no files written.
