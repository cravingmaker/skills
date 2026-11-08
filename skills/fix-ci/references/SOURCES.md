# Sources

Per-file provenance for the fix-ci skill. Each row is one upstream file this skill retains material from, pinned to a full commit, with the byte hash before adaptation. Reproduce a destination diff by fetching the pinned URL and comparing it with the listed local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/fix-ci/SKILL.md | plugins/pstack/skills/fix-ci/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 925f8c3e11de8bcc0cd015ec907f4d00b12cde6714246554ed3a52e096536522 | MIT | 2026 Lauren Tan; 2026 Michael Denyer; 2026 Cursor | SKILL.md | From cursor-team-kit at e46364b8be46000b7df0f260550cd712afbb8d36, as copied by the port. Resolve the PR and its checks; inspect failed jobs and the first actionable error from logs or the check link; smallest safe fix; push and re-check; one failure at a time; minimal changes; output of failing job, root error, fixes in order and next action. | Bound run ID, attempt, head and base; folded the ci-failure-triage classification (code, test, stale base, flake, runner, outage, quota, billing); no edits for no-step billing or quota failures; repeat only within the round budget; diagnosing-bugs required; connected tools before `gh`; shared delivery contract added. | LICENSE-pstack-claude; LICENSE-cursor-team-kit | NOTICE-pstack-claude.md |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/poteto-mode/playbooks/babysit.md | pstack/skills/poteto-mode/playbooks/babysit.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | d546a937ed800abe1d29aae8a689fb57212280fdde62fae1fc1dc7f2efd9d904 | MIT | 2026 Lauren Tan | SKILL.md | Step 7: classify CI before any retrigger; one fresh build for flake or infrastructure, never a job retry; an identical second failure is reclassified; a failure outside the diff means a stale base, checked with `git merge-base --is-ancestor`; only the diff's own code gets a commit. | Moved from the babysit playbook into this skill's classification and action steps. | LICENSE-pstack | none |

## Legal files

Each license or notice below is the upstream text, copied unchanged after a header that names the adapted local files.

| Local file | Upstream file | Revision | sha256 |
|---|---|---|---|
| LICENSE-pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/LICENSE | 6b0300214a09fd6029cfb7077043125758cd1fd2 | bc957ca6bee02792566a1a028d105e02e247c6e77cf057061674273da77b200e |
| LICENSE-pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/licenses/LICENSE | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 5b1faca8cef6b7433b49c812c5e9e04bb1eb73b67171d67729983e0b46b9bb78 |
| NOTICE-pstack-claude.md | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/licenses/NOTICE.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 232a21a3bf88991185e6837270cba41cd83646c3998f91942c823fecc4440b4d |
| LICENSE-cursor-team-kit | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/licenses/LICENSE-cursor-team-kit | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 702f5f331b56aff0e33d8c7826df5202559f894145eb70355c6477b55b5bb8a0 |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local adaptations produce diff exit 1; read the full input and each receiving file to review attribution.
