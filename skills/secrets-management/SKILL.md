---
name: secrets-management
description: Choose and wire secret delivery and lifecycle for pipelines and workloads. Use for "where should this secret live", "stop committing .env", or an authorized credential rotation. Prefer workload identity, name owners and consumers, and prove reload and revocation without exposing values.
---

# Secrets management

Deliver a minimal secret-delivery contract and a tested lifecycle. Inventory identifiers and dependencies, never secret values.

Use the `workload-identity-federation` skill when installed for CI/workload-to-cloud trust. A confirmed leak needs immediate security incident handling and scoped revocation; preserve evidence without copying the credential. Git history cleanup, masking and base64 do not revoke it. Deployment coordination and general incident command remain separate jobs.

## Choose delivery from the consumer backward

For each secret, record owner, consumers, purpose, permitted operations, delivery/reload mechanism, expiry, rotation/revocation authority, audit source and recovery dependency. Include bootstrap/decryption keys, standby consumers, scheduled jobs and recovery tooling. Reject an ownerless secret or a recovery design whose only key lives inside the system it must restore.

| Consumer support | Preferred choice | Check before adopting |
| --- | --- | --- |
| Native workload identity | Short-lived federated identity | Exact trust, least privilege, positive and negative exchange tests |
| Dynamic credential support | Existing cloud secret manager or Vault/OpenBao integration | Lease/revoke behavior, store availability, audit access, bootstrap and recovery keys |
| Static secret required | Store-backed delivery with a named rotation owner | Minimum scope, bounded life, consumers' reload behavior, overlap/revoke plan |
| GitOps encrypted files | SOPS with age or an approved KMS, or a supported external-secret controller | Actual encryption, recipient/key custody, admission and reconciliation behavior; encryption metadata alone is insufficient |

Prefer the platform already operated by the team. A new store adds availability, recovery and access-control work; feature availability and maintainer health need live primary-source checks.

Done when every consumer has a delivery path and an owner can issue, recover and revoke the credential.

## Add deterministic prevention

```sh
python3 <skill>/scripts/find-long-lived-credentials.py --repo /path/to/repo
```

The read-only helper examines tracked files: `.env` variants, state files, familiar stored cloud-key references and static login inputs in GitHub/GitLab CI, and common Kubernetes Secret YAML documents. It reports relative paths, line numbers and rule codes only. Exit 0 means no heuristic findings, 1 findings, 2 unusable input; it is not a general secret scanner and a clean result does not establish absence of secrets.

Read [references/lifecycle-checks.md](references/lifecycle-checks.md) when wiring scanning, Kubernetes delivery or a rotation drill; it defines what the helper misses and the required executable checks.

Use the repository's pinned scanner with redacted output and a synthetic, nonfunctional secret fixture. Prove the actual hook and CI path reject the fixture, accept its removal, and reject it again. Test changed files and the agreed history scope; document suppressions by rule/path and owner. For repository gate installation, read the `project-guardrails` skill when installed.

Keep secrets out of CLI arguments, debug traces, effective config, rendered manifests, tokens, screenshots and evidence artifacts. Prefer hidden entry or the approved store's input mechanism. Use metadata-only receipts; verify that tool redaction covers failure paths too.

Done when the actual enforcement path catches the inert fixture and the store/consumer permissions are read back.

## Prove rotation, reload and revocation

1. Identify all consumers and the service's availability constraint. Choose staged overlap, dual credentials, short-lived renewal or a documented outage; don't assume every provider supports overlap.
2. Rehearse on an explicitly disposable target with synthetic credentials. Confirm account/project, region and cluster immediately before changes. Existing task authorization must explicitly cover credential rotation, production effects and revocation; drafting a plan grants none.
3. Issue the new credential through the approved path, trigger or observe the real consumer reload, and prove the user path using a harmless operation. Record only credential/version identifiers, measured rotation/reload durations and observations.
4. Revoke the old credential, then prove the old credential fails and the current consumer still works. A pre-revocation rollback may restore the old path; after revocation, recovery normally requires reissue and delivery, not reuse of the revoked value. Test store/lease failure and restart behavior too.
5. Remove obsolete copies and access within scope; retain the nonsecret audit receipt and recovery instructions. If a drill fails, stop propagation and use the tested recovery path before retrying.

For Kubernetes, verify Secret encryption at rest with the platform owner, RBAC and the ability to create pods or exec into consumers; broad workload creation can bypass a Secret-read denial. Check whether the actual delivery mode reloads: env vars, mounted files and application caches behave differently.

Done when new delivery, reload, old-credential denial and reissue/recovery are observed on the authorized target, or the remaining live checks have a concrete owner. Read [references/sources.md](references/sources.md) when selecting current stores/controllers, encryption support, scanner flags or rotation mechanisms.
