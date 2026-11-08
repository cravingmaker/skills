# Sources

Per-file provenance for the modernize skill. Each row is one upstream file this skill retains material from, pinned to a full commit, with the byte hash before adaptation. Reproduce a destination diff by fetching the pinned URL and comparing it with the listed local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/modernize/SKILL.md | skills/modernize/SKILL.md | 1085050f3baed1ac724caa4a8166145fb2ac88af | 6172d774c46f535367086da90db1b0aaaaac969ed05ff040444f9afa9a6b1552 | MIT | 2026 Theo Browne | SKILL.md | Modernize the idea, not just the branch; guardrails (pull latest, user-owned worktree changes, scope of authority, lease-only force pushes, no unrequested comments); establish intent; check what changed around it; MODERNIZE, REWORK or CLOSE dispositions; rebase steps with range-diff and focused checks; report format. | Host-owned isolation first; the lease names a remote SHA captured with `git ls-remote`; a refused lease is reconciled, not retried; owned pending merges cancelled and verified absent before rewriting; child ranges after a parent squash; unresolved threads re-read after the push; no-merge mode and scoped push authority preserved; shared delivery contract added. | LICENSE-tstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/fix-merge-conflicts/SKILL.md | plugins/pstack/skills/fix-merge-conflicts/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 738b251281b30fd33e3892d0679cf94249e9c9e29e1bed40bcdde4a6aca98a76 | MIT | 2026 Lauren Tan; 2026 Michael Denyer; 2026 Cursor | SKILL.md | From cursor-team-kit at e46364b8be46000b7df0f260550cd712afbb8d36, as copied by the port. Detect every conflicted file; minimal correctness-first resolution; preserve both sides when safe, otherwise the compiling variant that keeps public behavior; regenerate lockfiles with the package manager; compile, lint and tests; no conflict markers; no broad refactors; summarize choices. | Folded into the rebase steps; "do not push during resolution" became the leased push after checks. | LICENSE-pstack-claude; LICENSE-cursor-team-kit | NOTICE-pstack-claude.md |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/merge-safety.md | plugins/pstack/skills/poteto-mode/references/merge-safety.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | cbbf0b760e1cbcfb125190983959275341684b6b4fba6246bdc0844254feab64 | MIT | 2026 Lauren Tan; 2026 Michael Denyer | references/restack-safety.md | Inspect and cancel pending mechanisms with readback before topology changes; missing fields never mean absent; captured remote SHA leases; child boundary from the recorded old parent tip; refused leases reconciled; disposable-repository testing. | The bundled `ship-pr` command replaced by portable connected-tool or `gh` steps; scoped to rewrites this skill performs; merge guards stay with the full-send skill. | LICENSE-pstack-claude | NOTICE-pstack-claude.md |

## Legal files

Each license or notice below is the upstream text, copied unchanged after a header that names the adapted local files.

| Local file | Upstream file | Revision | sha256 |
|---|---|---|---|
| LICENSE-tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/LICENSE | 1085050f3baed1ac724caa4a8166145fb2ac88af | 8095f9a9f97d074131f6a2ce09b952d12c18b36f09f4e5df0517c4e64e82c851 |
| LICENSE-pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/licenses/LICENSE | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 5b1faca8cef6b7433b49c812c5e9e04bb1eb73b67171d67729983e0b46b9bb78 |
| NOTICE-pstack-claude.md | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/licenses/NOTICE.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 232a21a3bf88991185e6837270cba41cd83646c3998f91942c823fecc4440b4d |
| LICENSE-cursor-team-kit | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/licenses/LICENSE-cursor-team-kit | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 702f5f331b56aff0e33d8c7826df5202559f894145eb70355c6477b55b5bb8a0 |

## Not copied

- tstack `skills/modernize/agents/openai.yaml`: skipped by plan; host policy is generated from the catalog `invocation` value.

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local adaptations produce diff exit 1; read the full input and each receiving file to review attribution.
