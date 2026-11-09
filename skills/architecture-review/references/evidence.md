# Evidence limits

Read this when collecting graphs, history, or execution evidence.

Record the exact revision, dirty-state scope, command, installed tool version, roots, exclusions, and supported target/feature set. Confirm a non-empty graph contains the relevant imports. Inspect resolution of aliases, re-exports, type-only edges, and generated code before claiming that a dependency is absent.

`churn-hotspots.py` uses Git history and committed blob sizes at `--rev`, which defaults to HEAD. `--since` is required so the review chooses its own window. The helper follows reachable non-merge commits, treats renames as deletion and addition, and excludes deleted files, symlinks, submodules, and any path with a binary diff in the window. Lockfiles, minified bundles, source maps, and snapshots are excluded by default. Add project-generated paths with repeatable `--exclude GLOB` arguments; matching uses case-sensitive basenames or repository-relative paths. It does not inspect working-tree content or follow rename history. Use source inspection at the review revision to investigate the candidates it reports.

The JSON records the resolved revision, window, scan counts, binary exclusions, configured exclusion patterns, and ranked files. Each file has added and deleted lines, total churn lines, blob bytes, and their product as `score`. The score is an inspection heuristic, not complexity, defect probability, or severity. Ties sort by path for stable output. An empty scan exits 1; invalid or missing history exits 2. `--help` exits 0 and does not inspect a repository.

Shallow clones and unavailable history limit the ranking. Name that limit; do not fetch or expand scope merely to fill a report. If the task permits fetching, record what history was obtained. Use the selected Git release's [log documentation](https://git-scm.com/docs/git-log) for history semantics.

A code path shows possible flow; a runtime trace shows an observed execution. A plan shows intended behavior; a controlled failure and recovery result support the corresponding recovery claim. Use independent expected outcomes and mark every unavailable environment.
