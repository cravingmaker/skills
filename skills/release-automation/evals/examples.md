# Examples

Run matched prompts with and without the skill only under the coordinator's model-evaluation authority.
These drafts remain unevaluated; the fixture tests are deterministic checks, not paired model results.

## Activation

- "Automate releases with generated versions and changelogs." Expect: Choose one existing-compatible engine and state the compatibility/commit policy.
- "Configure release-please for our independently versioned packages." Expect: Bind the generated candidate, source range, tag scheme and package versions.
- "Our Changesets version PR has inconsistent package versions. Fix the release generation." Expect: Compare planned newVersion values with the generated candidate and retain separate publication status.

## Near miss

- "Publish this already versioned package to the registry." Expect: Registry identity/publication is a separate job; this skill does not authorize it.
- "Audit whether our release workflow can run attacker-controlled code." Expect: The github-actions-hardening scope owns the trust audit.
- "Write and rehearse the rollback before deployment." Expect: The release-rollback-planning scope owns the recovery plan.
- "Run deploy-checklist to make the release go/no-go decision." Expect: Readiness is distinct from generated metadata.
- "Use incident-response to recover our production outage." Expect: Incident coordination is distinct from release generation.

- "Write a reusable test workflow." Expect: The github-actions-workflow-authoring scope owns job and caller structure.
- "Verify the signer and issuer of a release asset." Expect: The software-supply-chain-provenance scope owns artifact origin verification.

## Outcome

- "Check a generated release-please candidate for Node, Cargo and static Python packages." Expect: Fixture manifest maps three directories to synthetic version strings and each directory has one matching native manifest. All pass; changing any actual version yields a finding. No tag is written.
- "Compare Changesets status with a version PR, not the source tree." Expect: Fixture status has oldVersion 1.0.0 and newVersion 1.1.0. Candidate package 1.1.0 passes, 1.0.0 fails, and missing package paths fail. A no-release status with an empty releases array passes with zero planned packages.
- "Handle a repeated release and conflicting tag safely." Expect: In an explicitly disposable target or native engine fixtures, the same source/version produces one release; a tag pointing at different bytes stops. Report generated metadata, GitHub release and registry publication as separate states, without moving an immutable tag.

- "Our release candidate forgot a configured package." Expect: Pass config and candidate manifest to the helper; three matching configured paths pass, adding an absent path fails, and traversal paths are rejected. Native release-engine validation still checks version syntax.
- "Our bot release PR never reaches required checks." Expect: Read the current platform token/approval/dispatch rules and verify a representative target event before choosing credentials; no permanent no-trigger assumption is used.
