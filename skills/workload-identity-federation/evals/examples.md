# Examples

Prepare matched final-skill and no-skill runs before marking evaluated. Native-looking exported JSON fixtures are not a hosted federation test.

## Activation

- "Remove stored AWS keys from this GitHub deployment job and set up OIDC." Expect: current subject/audience readback, narrow trust and permissions, allowed and denied runtime contexts, old-key retirement within authority.
- "Our GitLab deployment cannot assume its cloud role." Expect: inspect effective runtime claims and provider restrictions without printing a token; distinguish token request, exchange and resource permission failures.
- "Federate this Kubernetes service account to Azure or GCP." Expect: bind actual issuer, audience and namespace/account, inspect workload-creation access and prove the denied account path.

## Near miss

- "Choose where the application API secret lives and rehearse reload during rotation." Expect: the `secrets-management` skill owns delivery/lifecycle.
- "Audit the entire GitHub workflow for injection, artifact poisoning and runner trust." Expect: the `github-actions-hardening` skill owns the broader audit when installed.
- "Design the deploy role's S3 resource permissions." Expect: scoped IAM permission design; federation is not a general IAM-design skill.
- "Review a saved Terraform plan that creates the federation role." Expect: the `terraform-plan-review` skill owns the saved-plan verdict.
- "Use engineering deploy-checklist for tonight's release." Expect: release coordination; no federation-policy change without a concrete trust job.
- "Use engineering incident-response for an outage." Expect: incident coordination; no implied IAM mutation or credential retirement.

## Outcome

- "Check an AWS export with a single web-identity Allow to the expected provider ARN, and exact issuer-prefixed aud/sub equalities." Expect: helper exit 0. Removing aud, changing sub to a wrong branch, adding repo wildcards or an unconstrained second Allow exits 1. Synthetic claim values never appear in either stream.
- "Wrap that AWS policy in Role.AssumeRolePolicyDocument, first as an object, then plain JSON text, then URL-encoded JSON text." Expect: the same static result for all three forms; malformed wrappers exit 2 without a payload or traceback. Literal percent escapes inside plain JSON are preserved.
- "Check an Azure federated credential with exact issuer, one expected audience and subject, plus a GCP provider with exact oidc fields, google.subject mapping and a conjunction of exact assertion equalities." Expect: both supported forms pass; alternate audiences, flexible Azure subject expressions, incomplete Azure pagination, missing GCP subject equality and CEL OR/prefix forms do not pass. These JSON fixtures are defined fully by the expected contract in the helper reference.
- "A GitHub environment subject matches the expected string, but any branch may enter that environment." Expect: branch eligibility remains unresolved; static subject equality is not accepted as proof of branch restriction.
- "Run the allowed context and wrong branch/repository/account against the same disposable destination." Expect: actual exchange and harmless resource read for the allowed case, provider trust denial for each excluded case, and no token evidence. Network failure or missing runtime token permission is inconclusive. Without runtime access, report the live checks unrun.
