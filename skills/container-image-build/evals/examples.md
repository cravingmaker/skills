# Examples

Run matched prompts with and without the final skill before changing evaluation status. These cases are prepared, not model-evaluated.

## Activation

- "Containerize this Node service with its existing lockfile and prove the arm64 image starts as nonroot." Expect the runtime contract, resolved inputs, native checks, target build and real startup/shutdown evidence.
- "Our Dockerfile copies a private package token into a layer; fix the build-secret path." Expect a BuildKit secret mount and a retained-layer canary test on an owned disposable build.
- "Make this image smaller without breaking its native Python module or TLS requests." Expect runtime compatibility tests and measured size change for the same platform.

## Near miss

- "Fix the healthcheck ordering in our local Compose file." Expect the `docker-compose-environments` skill; no image redesign without build evidence.
- "Review these Kubernetes Pod probes and PDB." Expect the `kubernetes-workloads` skill.
- "Harden this Docker daemon and remove its runtime socket mounts." Expect the `container-runtime-hardening` skill.
- "Verify the signer and provenance of this already-built digest." Expect the `software-supply-chain-provenance` skill.
- "Triage an unfixed CVE in this base image." Expect the `dependency-vulnerability-triage` skill; no implied acceptance from a scan flag.
- "Run the installed engineering plugin's deploy-checklist for Friday's release." Expect a release checklist, without activating image production solely because the release has an image.
- "Run the installed engineering plugin's incident-response; customers cannot log in." Expect incident coordination; no speculative rebuild.

## Outcome

- "Check the image-inspect report without printing configuration." Fixture: `tests/container-image-build/fixtures/image.json`, with UID `10001:10001`, one layer, size 12000 and a synthetic token in Env/Labels. Expect exit 0, the exact size/layer/platform summary and no token; changing User to `0` must exit 1, and malformed input must exit 2 without values.
- "Compare the new image with the previous image." Fixture: the same inspect JSON with previous Size 15000. Expect `size_delta_bytes` equal to -3000 and identical repeated output, with input bytes unchanged.
- "Keep architecture variants distinct." Fixture: set Architecture to arm and Variant to v7 in the inspect fixture. Expect platform linux/arm/v7; a non-string or slash-containing Variant must exit 2 without input values.
- "Prove the shipped image handles shutdown." Fixture: an owned disposable service that starts a child and drains one in-flight request on SIGTERM; a bad variant ignores SIGTERM. Expect the real variant's request result and bounded clean exit, and a failed shutdown gate for the bad variant. No real credentials or sensitive mounts.
- "Prove image evidence survived registry transport." Fixture: an authorized disposable registry target and one platform-specific build with SBOM/provenance requested. Expect registry digest/platform readback and attachment retrieval; a transport that drops metadata must remain an explicit failed or unavailable check.
