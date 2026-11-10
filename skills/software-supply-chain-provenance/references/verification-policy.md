# Verification policy

Read this when preparing native verifier commands or assessing a SLSA claim.

An artifact digest identifies bytes; an authenticated statement binds those bytes to claims; consumer policy decides whether those claims are acceptable.
Choose repository, workflow/builder, source ref/revision, issuer and signer identity before inspecting the candidate's self-description.
Prefer explicit expected identity flags and exact values from the trusted build contract.
Inspect the installed verifier help and primary docs for the supported artifact type and bundle format.

A successful verification command must cover the exact consumer digest, trusted issuer/root and signer, and required provenance predicate.
Record command, verifier version, exit code and selected authenticated fields.
Check that the verifier rejects different bytes even if their filename/tag stays the same.
Use separately generated disposable test keys or identity fixtures for wrong-signer tests; fixture signers never enter the production allowlist.
Do not mark a fixture with an invented identity as cryptographically verified merely because its JSON fields match.

For SLSA, read the current specification and identify its track, revision and each applicable requirement.
Record evidence for provenance generation/authentication, build-platform isolation, source integrity and protection of signing authority as required by that track and level.
Signing from an ordinary build step or moving it into another YAML file cannot alone prove platform isolation.
If evidence is unavailable, report the supported properties rather than assign a level.
