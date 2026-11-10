# Examples

Keep unevaluated until final-skill and no-skill model runs are recorded. The offline fixtures prove helper behavior only.

## Activation

- "Rename these Terraform resources without recreating them and import one existing disk." Expect: backup and writer identity, complete private address/ID mapping, declarative moves/imports and a no-mutation plan check.
- "The remote state is locked. Can we recover it?" Expect: prove the writer stopped, identify the exact lock/target, prepare recovery and respect the explicit unlock boundary.
- "Migrate this state backend and consider switching from Terraform to OpenTofu." Expect: live compatibility checks, disposable migration/restore rehearsal, exact identities and no assumption of reversible engine writes.
- "Scheduled Terraform drift detection found changes." Expect: classify every difference and choose adoption into code or a reviewed revert with the owner; refresh observation is distinct from state mutation.

## Near miss

- "Review a saved plan for destroys, unknown IAM grants and cost." Expect: the `terraform-plan-review` skill owns the verdict.
- "Write a reusable Terraform module from this interface." Expect: module design; state operations remain inactive until a real move/import/backend issue appears.
- "Ansible reports that the host configuration drifted." Expect: host configuration convergence; this state-identity skill stays inactive.
- "Use engineering deploy-checklist for the application release." Expect: release coordination, not automatic state edits.
- "Use engineering incident-response for an outage." Expect: incident coordination; this skill does not force-unlock or restore state merely because an incident exists.

## Outcome

- "Check a native-shaped plan with a managed no-op previous_address move, a managed no-op importing object, a data read, planned_values {}, and format_version 1.2." Expect: helper exit 0 with moved/imported counts; synthetic IDs and values are absent from output, input bytes are unchanged, and repeated output matches.
- "Check test.old moving to test.new and importing test.import with --expect containing moved {test.old: test.new} and imported [test.import]. Then omit the import or change the expected destination." Expect: exact sets pass; missing/unexpected/mismatched sets exit 1; duplicate or malformed expectations exit 2. Output includes the expectation digest and no private identifiers. Forgetting remains outside this gate.
- "Change one managed action in that fixture to create, update, delete, either replacement order, or forget; also try a changed output, drift, unknown mask, deferred work and a failed check." Expect: each variant exits 1 with a row/rule finding, not a pure-refactor pass. A post-application native plan must converge separately.
- "Recover an old-looking lock without active-writer proof or a readable backup." Expect: read-only evidence gathering and a concrete blocker; no force-unlock or state push. An old timestamp alone does not clear the condition.
- "Rehearse a backend or engine migration on a named disposable target with a usable backup and independent keys." Expect: migration, second-plan and actual restore receipts bound to old/new identities; metadata recovery is not described as recovery of destroyed data. No live rehearsal is claimed from the static fixture.
