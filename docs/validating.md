# Validate a candidate and prepare delivery

Use this after changing a package, catalog, repository tool, or documentation. Run from the repository root with uv, Python 3.12+, and Vale 3.26.0 on `PATH`. These checks call no models and need no personal settings or memory files.

## Generate and run focused checks

1. Run `git status --short` and `git diff --check`. Keep unrelated work out of the candidate. Regenerate profiles, preview/apply host policy when it changed, and regenerate docs:

   ```sh
   scripts/build-profiles.py
   scripts/build-host-config.py
   scripts/build-host-config.py --apply
   scripts/build-host-config.py --check
   scripts/build-docs.py
   scripts/build-docs.py --check
   ```

   Review any preview before applying it. Resolve every generator diagnostic and include changed generated files. Done when check mode reports current output.
2. Run the affected `tests/<name>/run.sh`; for docs-generation changes, run `tests/build-docs/run.sh`. Use the [skill workflow](skill-workflows.md) to select behavioral reruns. Done when focused checks pass and unrun behavioral checks are reported.

## Validate the selected files in a clean export

1. Review the diff, then stage only the intended files with `git add -- <path> ...`. Select public eval summaries explicitly; avoid staging raw result directories. The catalog's evaluated gate reads every local summary, including untracked ones. A dirty-checkout pass can therefore depend on evidence that will not ship.
2. Export the selected index and run the complete suite. This includes new staged files and excludes all untracked files:

   ```sh
   task_export=$(mktemp -d "${TMPDIR:-/tmp}/skills-check.XXXXXX")
   git checkout-index --all --prefix="$task_export/"
   if (
     cd "$task_export" &&
     REQUIRE_VALE=1 ./scripts/validate.sh
   ); then
     task_status=0
   else
     task_status=$?
   fi
   rm -rf -- "$task_export"
   test "$task_status" -eq 0
   ```

   Preserve the validation output before cleanup when a review needs it. For an already committed candidate, `git archive HEAD | tar -x -C "$task_export"` can replace `git checkout-index`. Run checks again after any subsequent fix. Done when the exact candidate passes the full suite with Vale required, without untracked evidence or private inputs.
3. Report the source revision, selected diff, commands, exit statuses, skipped checks, and whether model evals ran. Keep local validation separate from hosted CI. Commit or push only within the task's authority; an uncommitted handoff ends with the reviewed diff and report.

## Preserve shell and PR behavior

In zsh, an unquoted variable containing several words is one argument. Pass names as separate arguments, or use an array with `"${task_names[@]}"`; avoid building a command from a space-separated scalar. macOS `/bin/bash` is 3.2: repository shell code must work there or declare and verify a newer interpreter. Do not assume `mapfile`, associative arrays, or Bash 4 syntax.

For stacked PRs, record each parent and child base before a merge. PRs #2 through #7 originally merged into their stacked parent branches; PR #8 was needed to land the stack on main. After a parent lands, retarget each still-open child to the intended branch and inspect its base and diff before merging it. Under explicit forge-write authority, the commands are `gh pr view <number> --json baseRefName,headRefName,state`, `gh pr edit <number> --base <intended-base>`, and the same view again for readback. Handle any required rebase with the recorded old parent tip. Done when the forge shows the intended base, the diff contains only the child's work, and checks describe its current head and base.
