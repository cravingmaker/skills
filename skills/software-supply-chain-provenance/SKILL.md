---
name: software-supply-chain-provenance
description: Produce and verify SBOMs, build provenance and signatures for images, binaries and packages. Use to "sign our artifacts", verify a third-party download, promote one digest through environments, or assess a SLSA claim with evidence.
license: MIT
compatibility: Python 3.12+ for the optional inventory checker; use repository-pinned native signature and attestation tools.
---

# Software supply chain provenance

Bind the artifact the consumer will execute to authenticated build evidence and an independently chosen signer policy.
Promote the same digest through environments instead of rebuilding per destination.
A signature proves origin and integrity under its trust policy; vulnerability and license decisions need separate evidence.

## Define the consumer policy

Record the artifact kind, platform, source repository/revision, builder, expected signer identity, issuer, workflow/ref restrictions, subject digest and intended consumer.
Resolve tags, action SHAs, tool versions and third-party download digests live from their primary sources.
Choose trust roots and expected identities independently of the artifact being verified; untrusted provenance cannot authorize its own signer.
Check the current registry, repository visibility and verifier support, including how trust roots, transparency and offline bundles work for that target.
Finish this step when the verifier's acceptance policy exists before fetching the candidate artifact.

## Produce evidence with the build

Build once from the recorded source and dependency inputs.
Generate an SBOM for the final deployable artifact and target platform, including runtime components, native libraries and vendored content that lockfiles alone miss.
Use the repository's supported SPDX or CycloneDX schema and validate it with native schema tooling.
For multi-platform images, distinguish the index digest from each platform manifest and its SBOM/provenance attachment.
Record which digest each statement covers.

Use the build platform's current attestation mechanism, not hand-written provenance signed by unrestricted build code.
With BuildKit, verify the installed builder's SBOM/provenance flags, exporter and registry support before choosing them.
Inspect provenance modes for build argument or metadata disclosure; pass secrets through supported secret mounts and exclude their values from evidence.
Test that push/export and later copy operations retain attachments in the destination actually consumed.
Keep artifacts, SBOMs, attestations and verifier bundles linked by digest in the evidence record.

Read [references/verification-policy.md](references/verification-policy.md) when setting verifier constraints or choosing a SLSA claim.
Read [references/verification-commands.md](references/verification-commands.md) when forming GitHub or Cosign command arguments; validate flags against installed help before use.
For workflow identity or untrusted build inputs, read the `github-actions-hardening` skill when installed.
Finish this step when native tooling produces schema-valid evidence for the actual artifact and records its immutable identity.

## Verify at consumption

Use current `gh attestation verify`, Cosign or the artifact platform's native verifier with explicit expected repository, workflow/builder, issuer and certificate identity as applicable.
Inspect installed help before choosing flags; prefer exact identities over broad regexes.
Require the subject digest to equal the bytes or registry manifest the consumer will use.
Then inspect authenticated predicate fields for the allowed source revision/ref, builder and relevant materials; a successful signature alone does not satisfy every build policy.
Preserve the original authenticated statement and verification result without publishing secrets or internal metadata.

Check a changed digest, a changed signer and a changed issuer using inert fixtures with test keys in an explicit disposable local directory, or a disposable owned repository when hosted identity is required.
Each must fail before artifact execution; repeat the authorized case afterward.
Do not weaken production identity policy to make a fixture pass.
For third-party artifacts, verify before extracting or executing them, and compare an independently obtained digest or authenticated provenance.
In a disposable fixture, move a tag to another digest and require promotion to stop; an unrelated correctly signed artifact must not replace the previously accepted digest.
A checksum delivered beside unsigned attacker-controlled bytes is insufficient origin evidence.

Use the optional SBOM helper for an independent completeness check:

```sh
python3 <skill>/scripts/check-sbom-components.py bom.json --expected runtime-components.json
```

The Python 3.12+ helper checks exact versioned package identities in CycloneDX or SPDX JSON against an independently captured expected runtime inventory.
It reads files only; JSON results go to stdout, diagnostics to stderr; exits are 0 pass, 1 missing/conflicting components and 2 invalid input.
It neither verifies signatures nor binds the SBOM to the artifact; the native verifier must establish that binding first.
Read [references/sbom-inventory.md](references/sbom-inventory.md) before preparing its expected inventory.
Finish this step when the intended verifier accepts the exact artifact, substitutions fail, and the SBOM includes the independently expected runtime components.

## Promote and report

Pass the verified digest and verification policy to downstream jobs; re-verify at the consumer's boundary.
For registry copies, verify the destination digest and attachments before promotion; a mutable tag is a display label only.
Publication, signing identities, cluster policy changes and production traffic changes require their task authority; confirm destination account/project/region/cluster immediately before an authorized mutation.
Fixtures and helper checks perform no such mutation.

Use [assets/provenance-record.md](assets/provenance-record.md) when reporting the chain.
State any claimed SLSA track, specification revision and level with a requirement-to-evidence table from the current specification.
An action name or isolated reusable workflow alone does not prove a level; missing builder isolation or signing-key protection stays an unproven requirement.
For artifact advisory findings, read the `dependency-vulnerability-triage` skill when installed.

Done when artifact, SBOM and provenance identities agree, native signature/predicate checks and substitution tests pass, and downstream consumption uses the verified digest.
Report unavailable verification or builder evidence without a SLSA claim that depends on it.
Read [references/sources.md](references/sources.md) when verifying tool flags, schema support, platform attestation behavior or the current SLSA requirements.
