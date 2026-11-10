---
name: kubernetes-workloads
description: Write or review Kubernetes application manifests and Kustomize overlays for probes, resources, shutdown, rollout availability and workload security. Use when deploying a workload or reviewing its rendered variants. Live failure diagnosis and cluster-wide policy are separate jobs.
license: MIT
compatibility: The repository's pinned renderers, kubeconform, kube-linter and kubectl; server checks need an explicitly authorized target.
---

# Kubernetes workloads

Review the rendered workload as a running system, then validate its target schemas, admission and application behavior.

## Establish the target

Read the app contract, manifests/chart/overlays, GitOps ownership and existing checks. Record source revision, namespace, context/cluster, provider account/project/region where applicable, server version, image digest/platform, storage/CNI/admission facts and allowed effects. Resolve external images, chart dependencies, remote bases and tool versions live from their primary sources.

Choose Deployment for replaceable replicas, StatefulSet for stable identity/storage association, DaemonSet for per-node work and Job/CronJob for bounded work. StatefulSet does not supply database replication or backups. For scheduled work, decide overlap, deadlines, timezone and duplicate-execution handling with the application owner.

## Review the contracts

- **Health and shutdown.** Make readiness reflect whether the app can accept work; keep liveness independent of shared dependency availability. Use a startup probe for measured slow boot. Budget `preStop`, draining and SIGTERM inside termination grace. Read [references/probes-and-shutdown.md](references/probes-and-shutdown.md) when changing these contracts.
- **Resources and availability.** Set requests from observed demand and scheduling headroom. Choose limits with platform policy, memory failures and CPU throttling evidence. Check selectors, Service target ports, rollout surge/unavailability, PDB and topology together. Read [references/resources-and-rollout.md](references/resources-and-rollout.md) when changing resource or availability settings.
- **Workload security.** Apply the target version's Restricted-compatible security context: nonroot identity, no privilege escalation, dropped capabilities and supported seccomp. Use a read-only root with declared writable mounts as an additional policy; read-only root is not itself a PSS Restricted requirement. Minimize service-account tokens and secret access. Exceptions need a stated application need and an owner.

Cluster-wide RBAC, admission and network-policy design belong to the cluster/security owner. Do not broaden those controls to make one workload pass. Verify current [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) against the target OS/version.

## Validate every variant

Read [references/render-and-validate.md](references/render-and-validate.md) before validation. Render every shipped values/overlay variant; validate final documents rather than template source. Use native tools instead of a second YAML parser shipped with this skill.

1. Use the repository's pinned renderer and dependencies, with Helm's target `--kube-version` where applicable. Require a nonempty rendered set and a positive validated-object count. Record a digest of each complete rendered set in a private artifact; manifests can contain secret material.
2. Run `kubeconform -strict -summary -kubernetes-version "$target_version"` with matching core and CRD schemas. Missing schemas fail the required gate. Never apply a global missing-schema ignore to claim coverage.
3. Run kube-linter with the repository's explicit checks for probes, requests, nonroot identity, read-only root and privilege escalation. Compare [assets/kube-linter.yaml](assets/kube-linter.yaml) with the existing policy, checking names against the installed catalog. It requires requests without imposing CPU or memory limits. Compare [assets/workload.example.yaml](assets/workload.example.yaml) only when a starter is needed; replace its illustrative values from the app contract. Document job-specific exceptions instead of adding meaningless probes to batch work.
4. Reject the [unknown field](assets/negative/unknown-field.yaml) at the strict schema gate, and [missing requests](assets/negative/missing-requests.yaml), [privileged workload](assets/negative/privileged.yaml) and [mismatched selectors](assets/negative/mismatched-selector.yaml) at their named lint gates. Test dependency-independent liveness behavior through a real app fixture; schema or linter success cannot prove an endpoint's behavior.
5. Where authorized, run server dry run and diff against the explicit context/namespace. Inspect admission/defaulting changes privately. `kubectl diff` distinguishes no diff, a diff and an error; check installed help before interpreting its status.

Before any cluster contact, confirm the named context/namespace; server dry run can invoke admission webhooks and diff may disclose secrets. Before mutation, reconfirm account/project/region, cluster and namespace. Production apply, deletion, drain and traffic changes need explicit task authority. Offline checking does not supply deployment authority.

## Verify lifecycle

Use an explicitly named disposable cluster/namespace within task authority for install, readiness, dependency failure and drain checks. Verify the app's user path, desired replicas, graceful termination and a voluntary disruption through the eviction path. An eviction bypass does not prove PDB behavior. Keep resource ownership and exact cleanup targets; no broad delete or prune.

A local kind cluster proves that environment's behavior. It does not establish managed admission, storage, CNI enforcement or hosted identity. A stalled Deployment reporting `ProgressDeadlineExceeded` does not automatically roll back; record the retained artifact/config and the controller-aware recovery path.

## Adjacent jobs

For a live failure, read the `kubernetes-troubleshooting` skill when installed. For app-side health, retries or SIGTERM, read the `service-resilience` skill when installed. For a rehearsed undo, read the `release-rollback-planning` skill when installed. For secret delivery, read the `secrets-management` skill when installed. Read the selected skill before relying on it; otherwise return its evidence to the owner. Chart packaging, cluster upgrades and network/admission policy stay with those job owners.

## Done

Report each rendered variant and digest, target/version/schema coverage, lint/admission/diff results and exit codes, positive and deliberate rejection evidence, readiness/user-path/drain results, exceptions and recovery path. Name unavailable checks. Claim live enforcement only on the target actually exercised.
