---
name: container-image-build
description: Write or improve a Dockerfile or Containerfile and prove the final image runs on its target architecture. Use for containerizing an app, reducing image contents, handling build secrets, or fixing an image that builds but fails at runtime. Covers image production; orchestration has separate skills.
license: MIT
compatibility: Python 3.12+ for the report helper; Docker/BuildKit and the repository's pinned build and scanning tools for image checks.
---

# Container image build

Deliver a tested runtime image tied to its source revision, platform and immutable digest.

## Establish the contract

Read the repository's build/start commands, lockfiles, Dockerfiles, context rules and image checks before changing them. Record target platforms, native dependencies, certificate/DNS requirements, writable paths, health behavior and shutdown grace time. A smaller image is useful only if this contract still passes.

Resolve base digests and tool releases from the registry and official project sources at use time. Check installed BuildKit/Buildx capabilities with their help output. Keep the repository's update policy; a digest pin needs a maintained update path.

## Shape and check the build

1. Choose the smallest maintained base that supports the runtime contract. Use `scratch` only for a self-contained binary with its required data supplied. Verify libc, native modules, trust roots and a debugging path before choosing distroless or another minimal base.
2. Separate dependency, build and runtime stages where that removes build material. Use the project's lockfile verification command; copy only runtime output and production dependencies. Resolve every external `FROM` digest live, including build stages; stage references and `scratch` are different from registry inputs. Inspect resolved `ARG` bases for every shipped variant.
3. Review the context against [assets/dockerignore](assets/dockerignore) before editing the existing `.dockerignore`. This is a comparison starter, never a blind replacement. Keep credentials, VCS state and local dependency trees outside the context; prove each required build input remains available.
4. Use BuildKit secret/SSH mounts for credentials and cache mounts for rebuild speed. Credentials must remain outside arguments, environment metadata, copied files and cache outputs. Read [references/build-inputs.md](references/build-inputs.md) when private dependencies, caches or native build inputs are involved.
5. Set a numeric nonzero `USER`, an explicit working directory and exec-form process startup. Add an init process when the app needs child reaping or signal forwarding. Read [references/runtime-tests.md](references/runtime-tests.md) before testing the image.
6. Run the repository's Hadolint policy and native BuildKit checks. Verify which checks are enabled and make findings fail the gate. Native checks own Dockerfile parsing; the report helper does not parse Dockerfile text. Review input pinning separately from syntax checks.

Building executes repository code and can read mounts or spend runner resources. Use a named disposable builder/test target within task authority. Confirm the Docker context and remote builder identity first. Registry pushes and production runtime changes need explicit task authority.

## Prove the exact output

Build each declared target platform. Capture the image ID and platform before load/export; after registry transport, resolve the deployable digest and verify that SBOM and provenance remain attached. A local config ID, an image-manifest digest and a multi-platform index digest identify different objects.

Inspect locally without printing raw metadata:

```sh
docker image inspect "$image" | python3 <skill>/scripts/image-report.py -
```

The helper reads inspect JSON and emits only sizes, layer counts, platform and policy findings. Use `--previous previous-inspect.json` for a size delta. Exits are 0 for its checks passing, 1 for findings and 2 for invalid input; diagnostics omit input values. It proves configured identity, not effective runtime behavior or registry identity.

Run the actual image as its intended user, with a read-only root and only declared writable mounts. Exercise startup, native code, TLS/DNS and the application path. Send SIGTERM, measure exit within grace and verify child cleanup. Include a deliberate bad fixture, such as root `USER` or a missing runtime library, and show that the relevant gate rejects it.

Read [references/scan-and-attestations.md](references/scan-and-attestations.md) before the final digest-bound scan and metadata readback. Preserve all scan findings even if a fix-availability gate passes.

## Adjacent jobs

For a Compose environment, read the `docker-compose-environments` skill when installed. For Kubernetes manifests, read the `kubernetes-workloads` skill when installed. For daemon and host isolation, read the `container-runtime-hardening` skill when installed. For vulnerability decisions, read the `dependency-vulnerability-triage` skill when installed. For signing and consumer verification policy, read the `software-supply-chain-provenance` skill when installed. Read each selected skill before relying on it; otherwise name the missing method and return the evidence for that job.

## Done

Report the source revision, resolved build inputs, image ID, registry digest/platform relationship, size delta, checks and exit codes, runtime and SIGTERM results, scan/database metadata, SBOM/provenance readback and update path. Name every unrun check and any contract exception. Claim runtime compatibility only for the platforms actually exercised.
