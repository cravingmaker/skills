# Examples

These are cases for later matched model runs; catalog status stays unevaluated. Offline synthetic scanner tests do not prove a live rotation or enforce a repository's actual gates.

## Activation

- "Where should this application's secrets live, and how do its jobs receive them?" Expect: existing platform first, identity before stored credentials, complete owner/consumer/recovery contract.
- "Stop committing .env and add a secret-scanning gate." Expect: tracked-pattern check plus the actual configured redacted scanner, synthetic reject/accept/reject evidence and no credential values in output.
- "Rotate this credential safely; the task authorizes the staging rotation and old-key revocation." Expect: staged delivery/reload, harmless consumer assertion, old-key denial and reissue/recovery proof within that target.

## Near miss

- "Replace cloud keys with OIDC and restrict role assumption to one repository and environment." Expect: the `workload-identity-federation` skill owns the trust contract.
- "Add the chosen gitleaks command to pre-commit and CI; secret delivery is already settled." Expect: the `project-guardrails` skill owns gate installation.
- "Audit pull_request_target, cache poisoning and runner trust across our workflows." Expect: the `github-actions-hardening` skill owns that broader audit when installed.
- "A production key leaked in a public log; coordinate containment now." Expect: scoped security incident handling, not a normal storage-design exercise; no invented revocation authority.
- "Use engineering deploy-checklist for a release that already has working secret delivery." Expect: deployment coordination; this skill stays inactive without a secret-delivery/lifecycle job.
- "Use engineering incident-response for a database outage." Expect: incident coordination, without assumed credential rotation.

## Outcome

- "Scan a disposable Git repository tracking .env with a nonfunctional sentinel, a workflow with dotted and bracketed AWS stored-key references, and a kind: Secret YAML containing a sentinel stringData value." Expect: four path/line/rule findings, exit 1, unchanged files and no sentinel in either stream; repeated scans match.
- "Scan two YAML documents: the first has kind: Secret, an ENC[INERT] marker and top-level sops metadata; the second has plaintext stringData and no encryption metadata." Expect: the second document is flagged. A tracked symlink and a missing tracked file are findings, not silent coverage. Encrypted-looking acceptance is explicitly limited to shape.
- "Track infra/terraform.tfstate and its .backup, a GitHub workflow with credentials_json and an AWS secret reference, and .gitlab-ci.yml with a creds input; every value is SYNTHETIC_VALUE_MUST_NOT_APPEAR." Expect: five path/line/rule findings, exit 1, unchanged inputs and no sentinel. A comment naming credentials_json is ignored.
- "Exercise the real scanning gate with an inert scanner canary, remove it, and reinsert it." Expect: reject, accept, reject from the actual hook/CI path. The pattern helper's own tests do not count as proof of an unrelated scanner or gate.
- "Rehearse an authorized disposable rotation, reload, revoke and reissue." Expect: new-credential consumer success, old-credential denial, recovery/reissue receipt and no values in evidence. After revocation, restoring an old file is not offered as a valid rollback. Without that target, live checks remain unrun.
