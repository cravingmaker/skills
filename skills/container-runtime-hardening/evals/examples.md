# Examples

Run matched prompts with and without the final skill before changing evaluation status. These cases are prepared, not model-evaluated.

## Activation

- "Harden how this service runs under Docker on one Linux host." Expect the host/daemon boundary, effective settings, app proof and a harmless denied fixture.
- "We set USER in the image; is our rootless versus userns-remap setup actually doing what we intend?" Expect separate daemon-mode and process-identity evidence.
- "Remove privileged mode, writable root and Docker socket exposure without breaking the app." Expect inspect findings, named exceptions and actual allowed/denied tests within authority.

## Near miss

- "Split this Dockerfile into build and runtime stages." Expect the `container-image-build` skill.
- "Fix Compose profiles and preserve this database volume across restarts." Expect the `docker-compose-environments` skill.
- "Set a Pod securityContext in our Kubernetes Deployment." Expect the `kubernetes-workloads` skill.
- "Design cluster-wide admission and RBAC policy." Expect the cluster/security owner; no Docker daemon procedure.
- "Run the installed engineering plugin's deploy-checklist for the launch." Expect the release checklist without a daemon-mode migration.
- "Run the installed engineering plugin's incident-response for an outage." Expect incident coordination and scoped evidence, without speculative host hardening.

## Outcome

- "Check the effective runtime baseline privately." Fixture: `tests/container-runtime-hardening/fixtures/containers.json` plus `info.json`; a nonzero numeric UID, read-only root, CapDrop ALL, no added caps, no-new-privileges, finite memory/PID limits and rootless/seccomp daemon evidence. Expect exit 0 with no env or mount values, and stable repeated output.
- "Catch the additional effective confinement gaps." Fixture: separately add apparmor=unconfined, host UTS mode, Memory 0, PidsLimit -1 and a bind of /etc/shadow to the runtime fixture. Expect the corresponding LSM, namespace, resource and host-system findings, without raw paths or values. A zero-padded UID 000 must still fail numeric-nonroot.
- "Find socket access even when the socket is read-only or indirectly mounted." Fixture: change one fixture mount to `/var/run/docker.sock`, `/run/user/1000/docker.sock`, parent `/run`, or host `/`. Expect exit 1 with `control-socket-mount`; no paths or token values in output.
- "Require observed daemon evidence." Fixture: info SecurityOptions is empty, then replaced with `name=userns` and `name=seccomp,profile=builtin`. Expect findings for missing mode/seccomp, then pass only for declared userns-remap mode.
- "Prove the app still works and the filesystem restriction denies the intended write." Fixture: an explicitly authorized disposable container with an independent app result and a write attempt to its read-only root. Expect useful work success and a denial caused by the mount; a fixture missing the write tool must not count as a successful denial. No real runtime socket is mounted.
