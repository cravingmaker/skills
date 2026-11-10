# Engines and candidate versions

Read this when checking a release engine or choosing the candidate adapter.

A release-please manifest can record the last released version while a working package has moved ahead.
Compare equality only at the generated candidate state whose package versions and manifest are meant to agree.
The helper reads manifest keys as package directories; each directory must contain exactly one supported static version source: `package.json`, `Cargo.toml` or `pyproject.toml`.
For Python, it reads `[project].version` or `[tool.poetry].version`; workspace-inherited Cargo and dynamically generated Python versions need the repository's native checks.
Paths must resolve inside the explicit candidate root, including symlinks.
Use `--config <relative-config.json>` to require that its `packages` keys match the generated candidate manifest.
Paths are checked inside the candidate root; native engine validation still owns supported release types, version syntax and dependency updates.

For Changesets, save the original status output from the source tree and pass it with `--mode changesets --state status.json --package <path/package.json>` for every planned release package.
The helper compares each `releases[].newVersion` with the corresponding generated candidate package's version, by package name.
It does not compare `oldVersion` to the generated tree or treat status output as permission to run `publish`.
Also check fixed/linked groups and internal dependency range updates with the pinned Changesets tooling.

For semantic-release, use its supported dry run and plugins to capture the proposed version, tag and commit range; verify resulting package state with repository-native checks.
A plugin can execute commands even in a dry run; inspect configured plugins and remove write credentials before previewing.
For store-specific mobile versions, use the platform's manifest/build tool and preserve the distinction between public version, build counter and Git tag.
These branches are outside the helper's adapters, not outside this skill's release metadata scope.
