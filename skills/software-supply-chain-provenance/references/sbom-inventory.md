# Independent SBOM inventory

Read this before using `check-sbom-components.py`.

`--expected` takes a nonempty JSON array of objects with `purl` and `version` strings.
Capture this list independently from the final runtime package database, installed dependency tree or vendored-file manifest for the exact artifact/platform.
Do not derive the expected list from the SBOM being checked or accept a lockfile as a complete runtime inventory.
Use exact canonical package URLs, including namespace, qualifiers and subpath where relevant; the helper does no fuzzy name matching or URL normalization.

The helper supports CycloneDX JSON's component trees, including the root metadata component, and SPDX JSON's package list with `purl` external references and `versionInfo`.
Validate the full schema with its native validator first; the helper supports these package projections rather than every revision of either standard.
Unsupported document shapes fail with exit 2.
A missing version, absent expected package, conflicting version record is a finding.
Extra components are allowed because an independent sample may omit components; report the scope of the independent inventory and never call a partial expected set proof of complete coverage.

The helper cannot show that SBOM contents describe a particular artifact.
Authenticate a digest-bound SBOM attestation or the build platform's equivalent before applying the inventory check.
If the platform cannot preserve that binding through export or registry copy, report the gap and stop promotion that requires it.
