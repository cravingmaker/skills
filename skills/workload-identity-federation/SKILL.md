---
name: workload-identity-federation
description: Configure or repair OIDC/workload federation from a named CI runtime or Kubernetes service account to a cloud or registry. Use for "remove cloud keys", "set up OIDC deploy", or "role assumption fails". Bind issuer, audience and workload identity, then test an allowed and denied context.
---

# Workload identity federation

Deliver a trust contract and observed allow/deny results for one runtime-to-provider path. Replacing stored keys does not make a broad trust policy safe.

Secret storage and rotation belong to the `secrets-management` skill when installed. For a broader GitHub Actions trust audit, read the `github-actions-hardening` skill when installed. Permission design beyond the federated workload's role is a separate security task.

## Define the trust contract

Record source runtime and workload owner; destination account/project/tenant, region and role or registry; issuer, audience, subject and supported extra conditions; intended repository/project and ref/environment, or cluster/namespace/service account; narrowly required resource permissions; credential lifetime; and each denied context.

Separate planning, deployment and publication identities when their required permissions differ. A read-only plan job does not need a deployment role.

Obtain claim formats from current platform docs and actual effective configuration. Read GitHub organization/repository subject customization and environment rules; do not assume name-based, immutable-ID or reusable-workflow subjects. A decoded JWT is untrusted evidence until the provider validates it; never print or store the bearer token.

For environment subjects, verify which branches/tags may enter the environment: the subject may not carry a branch. For a service account, bind the actual cluster issuer and namespace/name, then check who can create workloads using that account. A role allowing token exchange still needs separate least-privileged resource permissions.

Done when both the intended and excluded workloads are concrete and every condition is supported by the destination provider.

## Check exported policy first

Read [references/trust-checks.md](references/trust-checks.md) when inspecting AWS, Azure or GCP exports; it defines the expected-contract format, narrow supported policy forms and live tests.

```sh
python3 <skill>/scripts/check-oidc-trust.py trust.json --provider aws --expected expected.json
```

The helper compares a native policy export with explicit issuer/audience/subject expectations. AWS also needs the exact federated principal ARN. GCP checks only a simple conjunction of exact claim equalities; unfamiliar CEL is a finding, not an inferred pass. Azure checks exact federated credentials, not flexible claim expressions.

Exit 0 means the supported static form matches, 1 means a mismatch or unsupported trust form, 2 means invalid input. Output contains rule codes and entry positions, never token or claim values. The check does not inspect all destination IAM bindings, issuer registration, environment protection or actual exchange behavior.

For other runtimes, registries or policy forms, use native validation and readback with the same contract. Keep unsupported helper coverage visible rather than translating a complex policy into a weaker model.

Done when every allow path in the supplied export has a scoped audience, issuer/principal and workload condition; unsupported forms remain unresolved.

## Change and prove the effective path

1. Prepare the runtime request and cloud-side trust changes together. Grant token-request permission only to the job/account that needs it; restrict privileged jobs to trusted code and protected refs/environments.
   For GitHub, scope `id-token: write` to that job and resolve the official authentication action's full SHA and origin live before using it.
2. Use existing authorization for changes; production IAM or credential changes require explicit scope. Recheck account/project/tenant, region and cluster before mutation. Use a disposable destination for drills; no production credentials in local emulators.
3. Run from the real intended runtime. Prove token exchange and a harmless, narrowly permitted resource read; retain only role/principal identity, run ID, ref/environment, time and result.
4. Run a wrong branch/environment and a wrong repository/project or service account against the same destination. They must fail at exchange because of the intended trust restriction; a network error or missing token-request permission proves nothing about cloud denial.
5. Read back the deployed trust and permission bindings. Only after the replacement path is proved, retire the old key under explicit revocation authority and verify consumers no longer depend on it.

For human-only console or credential-entry gaps, read the `wizard` skill when installed; use sufficient connected tooling for steps the agent can perform.

Done when the deployed trust matches the recorded contract, the allowed path works, each denied path fails for the right reason, and remaining key retirement has an owner. Report static and hosted evidence separately. Read [references/sources.md](references/sources.md) when resolving claims, supported conditions, SDK/CLI behavior or issuer integration at use time.
