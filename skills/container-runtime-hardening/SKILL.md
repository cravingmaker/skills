---
name: container-runtime-hardening
description: Harden how containers run on Docker or a single host outside Kubernetes. Use to review rootless versus userns-remap, runtime users, mounts, capabilities, seccomp or Docker socket exposure, and prove the app still works with the intended isolation.
license: MIT
compatibility: Python 3.12+ for the offline inspect checker; Docker and a declared disposable target for runtime verification.
---

# Container runtime hardening

Reduce container access to the host, then prove the allowed application path and a harmless denied path under the effective runtime settings.

## Establish the boundary

Read the container launch definitions, Docker context, host/VM boundary, daemon configuration and application storage/network contract. Record which host owns the daemon, who can reach its API and what the task authorizes. A remote context can target production even when the CLI runs locally.

Choose rootless operation when the runtime contract supports it. Rootless runs the daemon and containers without host root; `userns-remap` maps container identities while leaving the daemon privileged. Neither mode substitutes for a nonroot process, narrow mounts or restricted capabilities. Docker Desktop's Linux VM and a Linux host are different verification targets.

Check installed Engine/kernel support and the official [rootless](https://docs.docker.com/engine/security/rootless/), [user namespace](https://docs.docker.com/engine/security/userns-remap/) and [seccomp](https://docs.docker.com/engine/security/seccomp/) documentation at use time. Avoid fixed claims about support or default syscall lists.

## Tighten the effective settings

1. Use an explicit numeric nonzero runtime user; match writable volume ownership without making host paths world-writable.
2. Drop all capabilities and add back only a measured, documented application need. Keep privilege escalation blocked, seccomp enabled and the root filesystem read-only. Declare each writable volume/tmpfs and verify its ownership.
3. Remove privileged mode, host namespace sharing, sensitive host-system mounts and host devices unless a scoped requirement explains each exception. Remove access to Docker/container-runtime sockets, including sockets reached through parent-directory mounts or proxies. A read-only socket mount still exposes an API; the authority is the daemon owner's, including host root for a rootful daemon.
4. Set memory, CPU, process and log bounds from the workload contract. Inspect daemon API access and host port reachability as separate surfaces. Network restrictions need a real allowed/denied path test.
5. Treat custom security profiles and daemon-mode changes as host changes. Preview the affected containers, storage mappings and recovery path first. Confirm account/project/region where applicable, Docker context and host immediately before an authorized mutation. Production changes and traffic changes require explicit task authority.

## Check before execution

Capture `docker inspect` and `docker info --format '{{json .}}'` privately from the same confirmed context. Their raw outputs can contain credentials or host details. Run:

```sh
python3 <skill>/scripts/check-runtime.py containers.json --info daemon-info.json --daemon-mode rootless
```

Use `--daemon-mode userns-remap` only when that is the chosen boundary. The read-only helper checks identity, mounts, capabilities, explicit seccomp/LSM disabling, host namespaces and memory/process bounds against the strict baseline. It reports indexes/rule names, never environment values or mount paths. Exits are 0 for its checks passing, 1 for findings and 2 for usage/input errors. It catches common control sockets and their parent mounts; it cannot discover every proxy or prove live kernel enforcement. Record justified deviations as unresolved baseline findings rather than suppressing them silently.

Read [references/runtime-verification.md](references/runtime-verification.md) before executing the allowed and denied fixtures. Every fixture needs an explicit disposable host/container target and cleanup ownership; the shipped helper never invokes Docker or changes a host.

## Adjacent jobs

For image contents or the configured image user, read the `container-image-build` skill when installed. For Compose lifecycle and persistent storage, read the `docker-compose-environments` skill when installed. For Pod security contexts, read the `kubernetes-workloads` skill when installed. Read a selected skill before relying on it; otherwise return evidence to the owner of that job. Cluster-wide policy belongs to the security owner.

## Done

Report the target/daemon identity, chosen isolation mode and observed security options, effective user/mount/capability findings, allowed app result, denied fixture result, resource/log bounds and recovery plan. Name every exception and unrun proof. Configuration inspection alone does not establish host isolation.
