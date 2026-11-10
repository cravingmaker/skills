# Trust checks

Read this when checking a native exported policy or planning effective allow/deny tests.

## Expected contract

Use current claim readback and provider docs to populate a local JSON object with exact string keys `issuer`, `audience` and `subject`; AWS also requires `principal`, the exact OIDC provider ARN. Optional `claims` maps supported extra claim names to exact strings. Do not put JWTs, keys or arbitrary token contents into the contract. Wildcards and alternate subjects are outside the helper's narrow contract.

For example, an inert contract can use issuer `https://issuer.example.invalid`, audience `test-audience`, subject `repo:example/service:ref:refs/heads/main`, and the corresponding disposable provider ARN. These are fixture values, not cloud setup instructions or recommended production subjects.

Match the native export against that contract:

```sh
python3 <skill>/scripts/check-oidc-trust.py trust.json --provider azure --expected expected.json
```

Python 3.12+ stdlib only; local reads, no network, writes or token requests. `--help` exits 0 before file access. Stdout is JSON containing provider, static-scope limit, finding codes and entry numbers; stderr contains fixed diagnostics with payload withheld. Exit 0 means a supported static form matches; 1 findings/unsupported trust; 2 invalid input.

## Supported exports

| Provider | Export | Static checks and limits |
| --- | --- | --- |
| AWS | Native trust policy, an `AssumeRolePolicyDocument` object, or complete `get-role` output under `Role`; policy strings may be plain or URL-encoded JSON | Every allow entry must grant only web-identity assumption to the exact federated principal, with exact audience/subject. Exact `StringEquals` or wildcard-free `StringLike` conditions are supported. Unrelated allow entries, alternatives, missing conditions and unfamiliar operators fail. OIDC provider registration/client IDs and resource permissions need separate readback. |
| Azure | One federated credential, a complete list, or a Graph `value` collection with no next page | Exact issuer, audience list and subject in every supplied credential. Flexible expression credentials and extra claim requirements need native analysis. Export every relevant credential for the app/managed identity; one selected credential cannot rule out another broad trust. Tenant/app target and resource roles need readback. |
| GCP | Native workload identity pool provider object | Explicit audience, exact issuer, `google.subject = assertion.sub`, and `attributeCondition` consisting solely of exact `assertion.claim == 'value'` equalities joined by `&&`. Require exact subject plus any expected extra claims. Implicit audience defaults, alternate mappings, escapes, parentheses and other CEL need native review. Service-account IAM/pool principal bindings are outside this provider export. |

The helper compares the contract; it cannot prove that a subject actually identifies the right repository/ref. Verify that interpretation independently. For GCP, record default audience semantics when using them and test natively rather than weakening the check. Broader legitimate policies can fail this deliberately narrow helper without being vulnerable.

For GCP, inspect both the provider and each service-account/resource IAM binding. Prefer a single-subject `principal://` or exact-attribute `principalSet://` binding over the whole pool; restrict repository/project and ref/environment across the effective path. Prefer immutable repository/project identifiers where supported by the actual issuer and destination. Provider equality alone does not prove the destination grants only the intended identity.

## Runtime-specific checks

- GitHub: inspect the actual subject template, reusable-workflow claims, environment deployment rules, fork behavior, effective job permissions and cloud-supported claims. Exact environment subject matching alone does not restrict eligible branches.
- GitLab: inspect the project's effective ID-token audience, subject, protected ref/environment rules and destination claim support. Do not transplant GitHub syntax.
- Kubernetes: inspect actual issuer, projected token audience, namespace/account subject, service account binding and who may create/exec workloads using it. Local cluster evidence does not prove hosted cluster trust.
- Registries: check the registry's native trusted-publisher or workload identity contract, package/repository/workflow restrictions and effective publication permissions. Do not infer support from a cloud provider's exchange behavior.

## Allow/deny receipt

For each test, record actual runtime/run ID, source context, destination principal, harmless action, expected outcome, observed outcome and denial cause; redact tokens and credentials on every failure path. A wrong branch, fork/project or service account must reach the intended exchange service and be rejected by its trust condition. An unrelated build failure, missing runtime permission or unreachable endpoint is inconclusive. Test a wrong audience too where the runtime supports requesting one.

After the live test, read back deployed policies, environment rules and resource grants. Scope results to that configuration and time. Static fixtures establish checker behavior, not effective federation or revocation of old credentials.
