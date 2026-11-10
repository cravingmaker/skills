# Provenance record

- **Artifact.** Kind, platform, source SHA, consumer destination, index/platform/file digest and live resolution evidence.
- **Policy.** Independently chosen trust root, issuer, signer, repository, workflow/builder, source/ref and predicate constraints.
- **Build.** Tool versions, builder identity, dependency inputs, SBOM schema and attachment/export path.
- **Binding.** Authenticated artifact/SBOM/provenance subjects and retained verification bundle locations.
- **Verification.** Native command, exit code, selected authenticated fields and expected runtime component check.
- **Rejection.** Wrong digest, signer and issuer cases, plus a repeated accepted case.
- **Promotion.** Same consumer digest and destination attachment readback, or not run.
- **Claim.** SLSA track/revision/level with every requirement's evidence, or only the properties actually established.
