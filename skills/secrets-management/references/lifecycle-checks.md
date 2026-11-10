# Lifecycle checks

Read this when adding scanning, choosing Kubernetes delivery or rehearsing credential rotation.

## Scanner contract and limits

`scripts/find-long-lived-credentials.py --repo <root>` needs Python 3.12+ standard library and Git on PATH. It uses `git ls-files` to inspect the current bytes of tracked files; it reads no history or untracked files. Run it from an owned working tree and use the exact repository root. It makes no network calls or writes. `--help` exits 0 without inspecting a host.

Stdout is JSON: tracked-file count, findings with relative path/line/rule, and the heuristic coverage limit. Diagnostics go to stderr with payload withheld. Exit 0 means no heuristic findings; 1 findings; 2 unusable input. Tracked missing files and symlinks are findings, so skipping them does not look like coverage.

It flags tracked `.env` and `.env.*`, except `.env.example`, `.env.sample` and `.env.template`; `*.tfstate` and `*.tfstate.backup`; familiar stored cloud-key references or static cloud-login inputs in GitHub workflows and `.gitlab-ci.yml`; and common `kind: Secret` YAML documents without both document-local SOPS metadata and an encrypted marker. Document separators prevent an encrypted neighbor from exempting a plaintext Secret.

This is a delivery-pattern check, not YAML validation or a general secret detector. Bracketed/dotted workflow key references are recognized only in the supported line form. Encrypted-looking markers can coexist with plaintext values; markers are not proof of encryption. Flow-style YAML, anchors, generated manifests, JSON secrets, unusual credential names, values in example files, submodule contents, untracked files and history need the configured scanner/native parser and an explicit scope. Do not add exclusions because a value looks like a placeholder without checking its origin.

Test a nonfunctional scanner-specific canary in the actual hook/CI scope, with redacted findings. Pin the scanner from its current upstream release, verify the downloaded bytes, and record rule/DB/config identities where applicable. A changed gate needs rejection, acceptance after removal, and rejection after reinsertion; a scanner invocation that never reads the changed file is not proof.

## CI, containers and infrastructure

Give credentials only to the trusted job/step and protected environment that need them. Check effective deployment rules and fork/untrusted-code paths; masking is not an access boundary. Prefer runtime fetch or mounted-file delivery when the consumer supports it; environment values can reach children, crash reports and debug endpoints.

Use builder secret mounts for build-time access, then verify the build did not copy the secret into layers or image configuration. Keep values out of build arguments, committed Compose files and image environment variables. Read only metadata or redacted scan results into evidence.

Terraform/OpenTofu `sensitive` marking does not by itself prevent persistence in state or a saved plan. Prefer store-generated secrets and references, or secret-avoiding arguments/resources supported by the installed engine and provider. Verify that support live; state encryption needs independently recoverable keys.

## Kubernetes delivery

Check actual API-server/managed-service encryption at rest and its key custody with the platform owner. Reading an encrypted object through an authorized API normally returns plaintext; object retrieval does not prove encryption at rest. Do not print Secret objects or decrypted manifests for the check.

Evaluate Secret get/list/watch, pod creation, exec/debug, service account use, controller reconciliation and namespace boundaries together. A principal able to run arbitrary code as a consumer can often obtain its secrets despite direct read restrictions. Base64 is encoding, not encryption.

Record delivery behavior from the installed platform and the actual application: environment variables usually need a process restart, file updates still need consumer reload, and subPath mounts or application caches may keep old material. Test propagation, failed reconcile, store outage, restart and revoke with an inert disposable credential. A controller reporting Ready does not prove the user path uses the new value.

## Rotation and recovery receipt

Record owner/authority, account/project/region/cluster, store/version IDs, consumer inventory, chosen overlap or outage behavior, reload trigger, user-path assertion, old-credential denial, new-credential success, audit metadata, recovery/reissue result and remaining copies. Keep values out of arguments, logs and receipts; test diagnostic paths with synthetic values too.

Before revocation, a controlled rollback may return to the old credential if it remains valid and its exposure is acceptable. After revocation, issue and distribute a replacement; do not claim that restoring an old file restores validity. A confirmed leak needs scoped security response rather than a normal leisurely rotation. Root credentials, shared keys, provider rotation limits and irreversible revocation need current native documentation and explicit task authority.
