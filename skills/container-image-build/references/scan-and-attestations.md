# Scan and attestations

Use this reference for the final image scan and metadata transport check.

Select the repository's scanner, resolve its release live from the maintainer and verify its binary checksum or attestation. Record the scanner version, vulnerability database identity/age, scan time, image digest, platform, package coverage and omitted ecosystems. A tool that scans one platform does not establish coverage of an entire image index.

Fail on fixable high and critical findings under the repository's agreed policy. Keep unfixed findings visible for triage. Exceptions need an owner, reason, scope and expiry; a scanner flag is not an exception decision. A database download failure or absent package coverage is an unavailable check, never a clean scan.

Request SBOM and provenance through the installed Buildx build interface after checking its help. Match build credentials and provenance mode to the repository's disclosure policy; build arguments can appear in metadata. Read back attachments for the registry digest that consumers will pull. A local export can discard attachments even when the build succeeded.

A valid signature establishes a stated origin under a verification policy. It does not clear vulnerability findings. Signing policy and negative signer/digest verification belong to the adjacent provenance method.

Sources to check at use time: [BuildKit attestations](https://docs.docker.com/build/metadata/attestations/), [Trivy documentation](https://trivy.dev/docs/latest/guide/) and [Grype documentation](https://oss.anchore.com/docs/guides/vulnerability/getting-started/).
