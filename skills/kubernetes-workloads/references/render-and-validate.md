# Render and validate

Use this reference before checking a chart, Kustomize overlay or rendered manifest.

Enumerate the values/overlay variants that ship. Pin remote inputs under the repository's update policy, then render each one with its actual toolchain. A default render does not cover a production values file or a later overlay. Inspect Kustomize patches for selector, name and namespace changes in the final documents.

Keep Kustomize patches small and targeted, and use its `images` transform for per-environment image digests. Use the same standalone Kustomize or kubectl-bundled implementation as CI. Render Helm with the target `--kube-version` and exact values-file order before any further patching; revalidate the final output after composition.

Use the target server version and required CRD schemas with kubeconform. Keep schema provenance, version and digest alongside the check record. A missing CRD schema is missing proof; either supply the schema or state that the variant failed its required validation. Do not hide that gap under a global ignore.

Read the installed kube-linter check list and the repository policy. Enable the checks needed for the contract and run a positive fixture plus deliberate violations. Static lint cannot infer that an HTTP endpoint calls a shared database; prove that branch with a fixture application whose dependency can fail.

The offline fixture runner in `tests/kubernetes-workloads/run.sh` uses an already installed kube-linter for the comparison policy, a valid fixture and deliberate request/security/selector violations. It skips explicitly when the tool is absent; it never fetches a tool or schema. The unknown-field asset needs a separate strict schema check. This is linter evidence only. Target schemas, server admission, startup and drain remain separate checks.

Use explicit context and namespace options for server dry run/diff. Keep raw output private because generated Secret resources or annotations may contain values. Confirm target identity and authorization before applying or invoking a mutating lifecycle test. A server dry run exercises admission but does not prove that the app will start.

Check version-specific API removals in the target's [deprecation guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/) and provider release policy. Distinguish an API's status from a controller project's maintenance. Do not infer controller support from a manifest that validates.

Sources to check at use time: [Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/), [kubeconform](https://github.com/yannh/kubeconform), [kube-linter](https://github.com/stackrox/kube-linter) and [kubectl diff](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/).
