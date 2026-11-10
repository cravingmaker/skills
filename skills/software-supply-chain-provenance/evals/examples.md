# Examples

Run matched prompts with and without the skill only under the coordinator's model-evaluation authority.
These drafts remain unevaluated; the fixture tests are deterministic checks, not paired model results.

## Activation

- "Sign our images and verify they came from the expected workflow." Expect: Define the independent issuer/signer/source/digest policy and verify at consumption.
- "Add a runtime SBOM and provenance to this binary build." Expect: Generate evidence for the final artifact and compare an independent runtime inventory.
- "Verify this third-party package and assess the SLSA level we can claim." Expect: Verify before execution and map current track requirements to evidence rather than infer a level from an action name.

## Near miss

- "Triage a CVE in an image that already has valid provenance." Expect: The dependency-vulnerability-triage scope owns applicability; a signature does not decide vulnerability risk.
- "Create the Dockerfile for our service." Expect: The container-image-build scope owns the build contract.
- "Generate our changelog and release tags." Expect: The release-automation scope owns release metadata.
- "Run deploy-checklist for release readiness." Expect: A broad go/no-go checklist does not select provenance generation by itself.
- "Start incident-response for the current outage." Expect: Incident command is distinct from artifact origin verification.

- "Audit a privileged workflow for PR injection." Expect: The github-actions-hardening scope owns the trust-path audit.
- "Configure cluster admission to require signatures." Expect: Cluster policy enforcement belongs to its security owner; hand over verified identities and digests.

## Outcome

- "Reject a different artifact digest before executing it." Expect: A disposable fixture signs harmless local bytes with a native test-key mechanism. Native verification accepts the original and rejects one-byte-altered bytes under the same name; preserve command/exit evidence. JSON field matching cannot satisfy this case.
- "Reject a different signer or issuer." Expect: In an explicitly disposable owned repository, have two different workflows attest the same harmless fixture bytes. Define the expected signer as workflow A and the expected issuer from the trusted hosted identity contract. Native verification accepts A, rejects B under that policy, rejects A with an intentionally wrong expected issuer, then accepts A again. Resolve current verifier flags live; retain bundles and exit codes. Fixture identities never enter production policy, and unavailable hosted identity evidence is reported unrun.
- "Find a runtime dependency missing from a schema-valid SBOM." Expect: Fixtures provide equivalent CycloneDX and SPDX package projections plus an independently defined purl/version list. Both complete forms pass; removing a required package, changing its exact namespace/version, or recording conflicting versions produces a finding. This helper result is not signature verification.

- "Our promotion step receives a tag that moved after staging." Expect: A disposable owned tag initially resolves to accepted digest A, then is moved to B. Promotion compares with independently retained A and stops before consuming B; restoring A passes again.
