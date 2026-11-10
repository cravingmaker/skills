# Run and review paired evals

Use this to evaluate a new or materially changed skill against the no-skill baseline. Read the [harness contract](eval-harness.md) for fixture rules, host adapters, evidence files, activation detection, and exit codes. Authoring and offline validation need no model calls.

## Prepare and budget

1. Read the skill's examples and choose concrete fixtures and expected results before running anything. Plan both supported hosts, `claude` and `codex`, for the claimed support. Cover all Activation and Near miss examples and exercise the Outcomes affected by the change. Done when each planned pair has a host, example, fixture, and result a reviewer can check.
2. Obtain authority for model runs and set a finite total start budget, retry allowance, timeout, and concurrency limit. One pair costs two serial model sessions. For example, two pairs reserve four starts; a larger campaign needs its own total. Default to one active pair and no delegates; count any concurrent agent work against the same allowance. The harness has a per-arm timeout, not a hard token-budget flag; review recorded usage before authorizing another pair. Stop when the allowance is spent. Done when the complete campaign, including retries, fits the agreed budget.
3. Use uv, Python 3.12+, and the selected native host CLI. Inspect the harness's supported flags and run the offline suite:

   ```sh
   scripts/eval-skill.py --help
   tests/eval-harness/run.sh
   ```

   Set a fixture path containing only task inputs and commands. Put task context in its `README.md`; the harness supplies host instructions. It rejects credentials, symlinks, Git metadata, host settings, and ancestor configuration. Never read personal settings or memory files during evals, or copy their contents into prompts or fixtures. Leave authentication to the adapter. Done when preparation and isolation checks pass without a model call.

## Run the pairs

1. Preview each planned example. This existing fixture supports the smoke example:

   ```sh
   scripts/eval-skill.py --skill clear-communication --host claude \
     --example near-miss-1 --fixture tests/eval-harness/fixtures/package --dry-run
   scripts/eval-skill.py --skill clear-communication --host codex \
     --example near-miss-1 --fixture tests/eval-harness/fixtures/package --dry-run
   ```

   Substitute the campaign's actual skill, fixture, and example. Use `--prompt-file FILE` for placeholder input and repeat `--dependency DIR` for required external skills. Done when each dry run accepts its inputs; a dry run writes no result and establishes no behavioral outcome.
2. Run only the reserved pairs. Removing `--dry-run` makes two model calls. For a new trial, preserve earlier records with a new `--record-id`:

   ```sh
   scripts/eval-skill.py --skill clear-communication --host codex \
     --example near-miss-1 --fixture tests/eval-harness/fixtures/package \
     --record-id near-miss-1-trial-2 --timeout 300
   ```

   Use `--host claude` for Claude Code. `--model NAME` selects a model; omitting it records the host default. Only Claude accepts `--effort low|medium|high|max`. Record requested and effective settings; the adapters reject model or inventory mismatches across arms. Each pair must keep identical inputs, dependencies, and non-candidate discovery. Done when both arms finish or a preserved invalid record explains the failure.
3. Review the [evidence files](eval-harness.md#read-the-evidence), including unsupported or unclassified reads. Exit 0 means a valid comparison, not a passing skill. Grade activation, scope, correctness, and added workflow cost separately against the baseline. A matched Outcome at much higher token cost is evidence against adoption. Keep invalid and hurt results; a retry does not erase them. Done when the record has a source-bound reviewer verdict and actual usage, with unsupported observations labeled.

The CLI accepts only Activation and Near miss IDs. Apply relevant Outcome criteria to those runs' artifacts. When an Outcome needs a separate job, write its concrete prompt to `task_prompt`, set `task_fixture` to its fixture, and reserve a separate pair:

```sh
scripts/eval-skill.py --skill "$task_skill" --host codex --example activation-1 \
  --fixture "$task_fixture" --prompt-file "$task_prompt" \
  --record-id outcome-1-trial-1 --timeout 300
```

The harness records `activation-1` as the source slot and preserves the actual prompt. Label the reviewed summary with the true Outcome reference and exclude this overridden prompt from the original Activation example's coverage. The status checker cannot detect that mismatch. Replacing placeholder input without changing the original task still counts as that source example.

## Clean up owned resources

The harness removes temporary host homes on success or failure and terminates timed-out host process groups. Fixtures that launch detached services need their own recorded resource ownership and cleanup.

1. Record each disposable database's data directory, socket/port, process ID, and launch command before starting it. Check exact process identity before stopping it. For an owned PostgreSQL fixture, set `task_pgdata` to its recorded data directory and use its matching binary:

   ```sh
   pg_ctl -D "$task_pgdata" status
   pg_ctl -D "$task_pgdata" -m fast -w stop
   ```

   Confirm the process exited and that directory's server is stopped before removing its private files. For another owned process, inspect `ps -p "$task_pid" -o pid=,command=`, send `kill -TERM "$task_pid"` only after it matches the recorded launch, and wait for exit. Never use a broad process-name kill.
2. If a crashed PostgreSQL fixture leaves shared memory, inspect `ipcs -m` and its launch/error record. Use `ipcrm -m "$task_shmid"` only when the exact segment ID, owner, and dead fixture prove it belongs to this run. Leave unrelated or uncertain segments alone. Done when all owned processes and databases are stopped and only proven owned stale resources have been removed.

## Record and set status

1. Retain the generated public Markdown summaries in `skills/<name>/evals/results/` and add reviewed outcomes and limitations. Keep raw traces and artifacts private; inspect public text for personal paths and secrets before selecting it for commit. Bind results to the recorded actual-byte hash, dependencies, fixture, host, and model. Done when another reviewer can distinguish validity, behavior, and comparative value.
2. Keep `status: unevaluated` until every Activation and Near miss has a valid completed pair for the final materially changed bytes, required Outcomes are reviewed, and no comparative regression remains unresolved. The checker verifies only structural valid/completed coverage; it does not verify hashes, require both hosts, grade Outcomes, or reject semantic hurt. The campaign review owns those decisions.
3. Run `scripts/check-catalog.py`, regenerate with `scripts/build-docs.py`, and follow [clean-export validation](validating.md). Untracked eval summaries can satisfy the status gate locally but disappear from a clone; include the intended public records in the export and repeat the check there. Done when committed-candidate evidence supports the status, all checks pass, and cleanup is recorded. If the budget or authority ends first, report the missing pairs and leave the skill unevaluated.
