# Native verifier arguments

Read this when constructing verification commands; confirm supported flags in installed help and the linked primary docs before running them.
These patterns express consumer policy and do not establish verification by their presence in a file.

| Native verifier | Explicit trusted inputs | Artifact binding |
| --- | --- | --- |
| `gh attestation verify` | Expected repository, signer workflow and OIDC issuer; add source/ref and predicate constraints the policy requires | An exact local file, or `oci://<registry>/<image>@<digest>` |
| `cosign verify` | Exact certificate identity and OIDC issuer, or an independently trusted public key | An image reference with its immutable digest |
| `cosign verify-attestation` | The same signer constraints plus the expected predicate type | Check the authenticated subject and predicate after signature verification |

For GitHub, inspect `--repo`, `--signer-workflow` and `--cert-oidc-issuer` in the [CLI manual](https://cli.github.com/manual/gh_attestation_verify).
For keyless Cosign, inspect `--certificate-identity` and `--certificate-oidc-issuer` in the [verification docs](https://docs.sigstore.dev/cosign/verifying/verify/).
An owner alone does not constrain the intended repository and workflow.
An identity pattern needs review of its full matching language; anchors alone do not make a broad pattern narrow.
Use native negative verification with wrong bytes, signer and issuer, then repeat the expected case.
A source-text command scanner cannot prove arguments after shell expansion, YAML execution, command chaining or runtime input binding.
