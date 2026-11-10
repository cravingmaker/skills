# Sources

Read this when resolving actual subject formats, provider-supported claims, audience defaults, token permissions or SDK/CLI behavior. Sources are link-only; helpers and instructions are original work.

- [GitHub OIDC reference](https://docs.github.com/en/actions/reference/security/oidc): check actual subject templates, immutable/customized claims, reusable workflows and platform applicability live.
- [GitHub OIDC to AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) and [AWS IAM OIDC federation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html): verify issuer registration, client IDs, supported conditions and role trust.
- [AWS get-role](https://docs.aws.amazon.com/cli/latest/reference/iam/get-role.html): verify the native role wrapper and policy encoding for the export tool in use.
- [Google Cloud federation with deployment pipelines](https://cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines): verify issuer/audience, attribute mappings/conditions and service-account IAM bindings; static provider JSON is only one part.
- [Microsoft Entra external trust](https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust): verify federated credential matching and the actual app/managed-identity API shape.
- [GitLab ID tokens](https://docs.gitlab.com/ci/secrets/id_token_authentication/): verify current claims and runtime token configuration.
- [Kubernetes service accounts](https://kubernetes.io/docs/concepts/security/service-accounts/): verify projected audiences, issuer, binding and workload access on the real cluster.

For a registry integration, use that registry's official trusted-publisher/federation docs and the deployed repository's readback. Do not embed rollout dates, historical subject strings or plan-gated environment assumptions in a reusable policy.
