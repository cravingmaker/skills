---
name: kubernetes-troubleshooting
description: Diagnose Kubernetes Pending pods, CrashLoopBackOff, OOMKilled, image pulls, failing probes, stuck rollouts, DNS or Service selector failures. Use when a workload is unhealthy now. Starts from read-only evidence; manifest authoring and live incident coordination are separate jobs.
license: MIT
compatibility: Python 3.12+ for the offline JSON triage helper; kubectl read access to a named context/namespace for live evidence.
---

# Kubernetes troubleshooting

Choose the next probe from observed state, then distinguish a supported cause from a hypothesis. Keep diagnosis read-only until a specific remediation is authorized.

## Bind the evidence

Confirm context, cluster, namespace, affected workload and observation time before cluster reads. Record provider account/project/region where relevant, recent source/image/config changes and user impact. Inspect the least data needed; logs, events, describe output and Pod specs may contain secrets. Keep raw captures private and share sanitized findings.

Use explicit context/namespace options for `get`, `describe`, bounded `logs` and `rollout status`. Inspect command help and target-version documentation at use time. Avoid broad all-namespace dumps and Secret reads. `exec`, `debug`, port-forward, patch/edit, restart, scale, delete and rollout undo are outside the default read-only path.

Collect Pods and events in a bounded namespace snapshot, plus Deployments, Services, EndpointSlices and PVCs when those surfaces are involved. Preserve Pod UIDs and timestamps; a same-named replacement or old event is different evidence.

```sh
kubectl --context "$context" --namespace "$namespace" get pods,events -o json |
  python3 <skill>/scripts/pod-triage.py -
```

The helper reads a native JSON List or resource object without contacting a cluster. It covers scheduling, image/config/runtime starts, terminations, probe/mount/sandbox events, PVC binding, rollout deadlines and Service endpoint evidence. It emits fixed signal names, object/container indexes, state labels and next-probe labels rather than raw messages, commands or values. Exits are 0 for no recognized signals, 1 for observed signals and 2 for invalid input; exit 0 is not a health certificate. It correlates Pod events by UID and namespaced events by object identity. It does not count label-selected Pods as proven Service endpoints.

## Narrow the cause

Read [references/evidence-matrix.md](references/evidence-matrix.md) for the matching branch and its next discriminating check. Check current and previous container state, including init containers and restart counts. Use bounded previous logs when a restarted container is involved; avoid assuming that current logs explain the prior exit.

- **Pending.** Separate scheduling, volume binding/attachment, image startup and node conditions. FailedScheduling text chooses a hypothesis; confirm the resource/taint/affinity/PVC fact before changing requests or adding capacity.
- **Terminated or restarting.** `OOMKilled` is an explicit runtime reason to investigate. Exit 137 is compatible with SIGKILL, but an application can also return that code; it does not prove OOM. Compare last/current reason, events, node evidence and memory metrics before attributing cause. CrashLoopBackOff describes retry backoff, not the application defect.
- **Pull or probe failure.** Inspect the exact pull/probe reason privately and separate registry authorization, digest/platform, DNS/TLS and endpoint behavior. A readiness failure and a liveness restart require different remedies.
- **Stuck rollout.** Compare desired/updated/available replicas, controller conditions and actual Pods. `ProgressDeadlineExceeded` does not automatically restore the previous release. Check the GitOps owner before proposing recovery.
- **Service or DNS.** Trace selector, namespaced Pods, EndpointSlice readiness and target port before DNS/CNI hypotheses. A Service with no selector can intentionally use managed endpoints. A matching label alone does not prove a ready endpoint or network reachability.

Choose one probe that separates the leading hypotheses, state the predicted outcomes and inspect the result. Bound repeated collection by the next observable transition; do not restart or delete a Pod merely to obtain a different symptom. Access failure remains a named evidence gap.

## Remediate within authority

Prefer a source change through the owning delivery controller once diagnosis supports it. Immediately before an authorized mutation, confirm account/project/region, cluster and namespace and check that the observed Pod/controller identity is still current. Production changes, deletion, drain, rollout undo, credentials and traffic changes require explicit task authority. Existing authorization remains valid within its stated scope.

A debug container, exec probe or network test can run code or alter a workload. Use one only with explicit target and authority; never print credentials to prove access. Recheck the user path and relevant workload condition after an authorized remedy.

## Adjacent jobs

For a manifest change, read the `kubernetes-workloads` skill when installed. For an image architecture, entrypoint or dependency cause, read the `container-image-build` skill when installed. For an application defect, read the `diagnosing-bugs` skill when installed. For rehearsed recovery, read the `release-rollback-planning` skill when installed. Read each selected skill before relying on it; otherwise return its evidence to the owner. Coordinate active user impact with the incident owner, host faults with the sysadmin and CNI/admission/RBAC policy with the security owner.

## Done

Return the target/time/UID-bound observations, supported cause or ranked hypotheses, discriminating probes and results, proposed or authorized remedy and recovery check. Name actions not taken and unavailable evidence. Keep symptoms, causal proof and post-fix service recovery distinct.
