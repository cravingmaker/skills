# Examples

Run matched prompts with and without the skill only under the coordinator's model-evaluation authority.
These drafts remain unevaluated; the fixture tests are deterministic checks, not paired model results.

## Activation

- "Add CI for PRs and our merge queue, with a stable required gate." Expect: Map events and exact check contexts, build the graph, then seek hosted check-run evidence.
- "Split our giant build job into a target matrix and a reusable workflow." Expect: Preserve required-check names and caller interfaces; validate the parsed graph.
- "Make a composite action for our setup steps and serialize staging deploys." Expect: Choose the step/job interface and preserve mutation concurrency without granting deployment authority.

## Near miss

- "Is this pull_request_target workflow vulnerable to cache poisoning?" Expect: The github-actions-hardening scope owns the trust audit.
- "Fix the test assertion failing in the latest CI run." Expect: The fix-ci scope owns failure classification and repair.
- "Run deploy-checklist for tomorrow's production go/no-go." Expect: A broad release readiness checklist does not load this authoring skill.
- "Use incident-response to coordinate the current outage." Expect: Incident coordination does not load workflow authoring.

- "Wire one repository-wide check command into hooks and branch protection." Expect: The project-guardrails scope owns enforcement; workflow authoring applies only to a separately requested graph change.
- "Choose test shards, quarantine rules and result manifests." Expect: Test-stage design belongs to the test owner; adding parallel jobs alone does not settle that contract.
- "CI takes too long; find the bottleneck." Expect: Measure pipeline performance before proposing structural changes; this authoring skill does not own timing diagnosis.
- "Replace cloud access keys with workload identity federation." Expect: The cloud trust-policy scope owns identity setup.
- "Set up generated changelogs and release tags." Expect: The release-automation scope owns metadata policy and generation.

## Outcome

- "Check a multiline workflow whose runner job has no timeout but a comment says timeout-minutes: 10." Expect: Export actual YAML through a parser, run actionlint, and require the JSON checker to flag the missing field. Fixtures use a parsed workflow object with on, permissions, concurrency and a job lacking timeout-minutes; comments never supply it.
- "Preserve the required context CI while adding a matrix." Expect: Fixture rules require CI; a non-matrix CI gate passes the name check, while removing it, duplicating it or replacing it with a matrix job produces findings. A hosted failed dependency must also make the gate red.
- "Check a reusable call and a dependency cycle." Expect: A call job using a pinned reusable workflow needs no unsupported runner timeout; its called runner job does. Two jobs needing each other fail. Local graph checks alone are not reported as hosted proof.

- "A deployment job sets cancellation false but its workflow cancels in progress." Expect: An environment job under workflow-level cancellation fails even with a job-level false setting. Disabling both passes; an unresolved cancellation expression remains a finding until separately proven.
