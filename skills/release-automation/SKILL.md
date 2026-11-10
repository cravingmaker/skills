---
name: release-automation
description: Automate versions, changelogs, tags and GitHub releases with release-please, Changesets or semantic-release. Use for "automate releases", "generate our changelog", or replacing manual version bumps, with an explicit compatibility policy and source-bound dry run.
license: MIT
compatibility: Python 3.12+ for the candidate version checker; use the repository's pinned release engine.
---

# Release automation

Generate reviewable release metadata from the repository's change history, then bind tags and release assets to the reviewed source.
Keep generated metadata, GitHub release state and registry publication as separate observed states.

## Choose the policy and engine

Read existing release configuration, package manifests, lockfiles, changelog, tags, merge strategy and workflows.
Reuse the current release engine unless the task authorizes changing it; keep one owner for version and tag generation.
Record the compatibility promise, including what counts as a breaking change while a package is `0.x`, prereleases, independent versus fixed package versions and tag naming.
For mobile applications, distinguish store/build identifiers from the public compatibility version.
SemVer does not decide the user's compatibility policy for them.
Use [assets/release-policy.md](assets/release-policy.md) when the repository lacks a written public-API and versioning policy; fill it from the actual promise and engine configuration.

Use release-please for generated release PRs when that fits the repository, Changesets for explicit package change records, or semantic-release for commit-driven release generation.
Check the pinned engine's current official documentation and installed help; do not copy a competing engine's config or invent a dry-run flag.
Read [references/engines-and-candidates.md](references/engines-and-candidates.md) when selecting adapters or checking version state.
Finish this step when one engine owns the release sequence and the compatibility and commit policies are explicit.

## Generate metadata without publishing

Validate the actual commit stream the engine consumes, including squash titles or merge commits according to repository policy.
Use the repository's commitlint/configured equivalent over that range; a valid PR title alone cannot prove non-squash commit history.
Resolve the previous release tag to its commit, record the proposed head SHA, and inspect every generated version, changelog entry and tag against that source range.
Handle a no-release range and prerelease channel explicitly.
For multiple packages, inspect dependency range updates and packages that should remain unchanged.

Run the engine's supported planning/dry-run mode with write credentials unavailable.
When the engine needs a generated candidate tree, create it only in an explicit disposable local checkout; inspect local output and never run the publish phase to obtain a preview.
Dry-run logs can contain credentials or repository data; retain only the needed release metadata.
Compare candidate manifests using the optional helper when its adapters apply:

```sh
python3 <skill>/scripts/check-release-config.py --root <candidate> --mode release-please --state .release-please-manifest.json
```

The Python 3.12+ script is read-only and compares planned versions with actual candidate package manifests.
It supports release-please Node/Cargo/static Python candidates and Changesets status JSON with explicit package paths.
Pass `--config release-please-config.json` to compare configured package paths with the candidate manifest; the native engine still validates release types and version syntax.
JSON results go to stdout, setup diagnostics to stderr; exits are 0 pass, 1 findings and 2 invalid input.
It does not require last-released and in-development versions to match outside a generated candidate.
It does not prove changelog accuracy, tag identity, publication or workflow safety.
Finish this step when the exact candidate matches the engine's plan and a no-release case produces no release action.

## Wire the release boundary

Use a trusted event and protected source; give the release job only its needed contents/PR permissions.
Check the current `GITHUB_TOKEN` event-propagation rules, approval requirements and dispatch exceptions in [GitHub's triggering documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
Prove that a bot-created release PR and its tag events reach the required checks on this target before changing token type; scope any necessary App token to the intended repository.
Keep registry publication and deployment in distinct jobs and authority scopes.
Release and publication jobs restore no caches, including setup-action caches; consume verified build outputs or perform a clean reproducible install.
Serialize release mutation with cancellation disabled and inspect tag/version races on reruns.
A repeated event must reuse the existing correct release or stop on conflicting bytes, never move a released tag silently.
If the methods are installed, read the `github-actions-workflow-authoring` skill for job structure and the `github-actions-hardening` skill for trust paths.

Check current GitHub release immutability, signing/attestation support and plan/visibility requirements in primary docs before promising them.
Stage and inspect all intended assets before any irreversible release finalization.
A release attestation, a build attestation and registry package provenance prove different claims; label which was checked.
For build signatures and artifact provenance, read the `software-supply-chain-provenance` skill when installed.
For a rollback or corrective release, read the `release-rollback-planning` skill when installed.

Release creation, publication, tag writes and production changes require the task's explicit authority.
Immediately before an authorized remote mutation, confirm repository, source SHA, target channel/version and relevant account/project/region/environment.
Prepare the concrete candidate and validation before requesting any missing authority.
Registry identity and publication are a separate job; do not invent an unavailable publishing skill or publish merely to prove metadata generation.

## Verify and report

When release execution is authorized, read back the actual tag's peeled commit, generated release, asset names and digests, immutable state and supported release/asset verification output.
Check current `gh release verify` and `gh attestation verify` help before use; do not substitute one command's result for the other's claim.
For registry publication, report only the registry readback actually observed; a GitHub release is not proof of a published package.
Exercise a repeated event and a version/tag conflict in a disposable target or the engine's inert fixtures.

Use [assets/release-record.md](assets/release-record.md) when recording the candidate and result.
Done when generated metadata is consistent with the stated policy and source range, dry-run and conflict checks pass, and every executed release operation has matching readback.
State unrun remote or registry checks plainly.
Read [references/sources.md](references/sources.md) when verifying release engine behavior, compatibility standards or GitHub release features.
