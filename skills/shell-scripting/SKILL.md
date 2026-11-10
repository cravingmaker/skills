---
name: shell-scripting
description: Write or repair an executable Bash, POSIX sh, or zsh script for declared macOS and Linux targets. Use for script authoring, behavior tests, broken quoting, hidden failures, interrupted runs or portability bugs. Sourced zsh state belongs to zsh-configuration.
---

# Shell scripting

Deliver a script whose arguments, effects, failures and supported interpreters have executable evidence.

## Declare the contract

Read the script, its callers, existing checks and target runtime before editing. Record the shebang, resolved interpreter path and version, minimum supported version, OS and utility dependencies, inputs, output streams, exit statuses, working directory, effects and rerun behavior. A login shell does not choose an executable script's interpreter; the shebang does. An `env` shebang depends on PATH, so privileged automation needs a controlled search path.

Choose POSIX sh for a portable language subset, Bash for shared automation that needs its features, and zsh for macOS-specific executable behavior. Test the declared interpreter rather than assuming Bash POSIX mode proves POSIX compatibility. Verify the target Mac's actual Bash version; either support that version or gate unsupported features with an installation fix. For sourced or interactive zsh, use the `zsh-configuration` skill when installed and read it first.

Read [references/portability.md](references/portability.md) when crossing OSes, shell versions or process boundaries. Reconsider shell when structured data, durable retry state or roughly a hundred lines make explicit failure handling hard; preserve the caller contract if moving the implementation to Python or TypeScript.

Done when the declared contract names the real supported targets and the evidence each needs.

## Preserve data and failure status

- Preserve argument boundaries with `"$@"`, quoted scalars and Bash/zsh arrays. Pass values as data; use `printf '%s\n'`, supported `--` separators, and NUL-delimited filename interfaces where available. Match each nested shell's quoting independently.
- Handle critical command statuses explicitly. `set -e` has conditional-context exceptions; a function called from `if` or `||` can continue after a failed child. Separate declarations from command substitutions. Decide how expected nonzero statuses and SIGPIPE affect a pipeline.
- Validate every input before mutation. Bound calls and retries, serialize writers, use securely created temporary paths, preserve the original failure through cleanup, and publish completed files by rename on the same filesystem.
- Make `--help` exit 0 without effects; keep data on stdout and diagnostics on stderr. A dry run uses the same validated inputs and target selection as apply. Keep credentials out of traces and errors.

Read [references/failure-and-tests.md](references/failure-and-tests.md) when changing failure handling, cleanup, retry or file publication. Use [assets/template.bash](assets/template.bash) as a comparison starter when a Bash contract fits; adapt it to existing conventions rather than overwriting a script.

Domain operations retain their authority boundaries. Production changes, deletion, credential rotation and traffic changes need explicit authorization for their actual target and effects. Confirm account, project, region and cluster where relevant immediately before mutation. A disposable fixture is the target for fault injection.

Done when each critical failure stops the intended work, preserves the promised status and leaves a defined retry state.

## Verify the actual executable

Run the project's declared formatter and linter with its pinned tooling. Use ShellCheck only for a supported dialect; check the installed shfmt help and official manual before selecting its dialect. Resolve missing tooling and versions from official sources under the project's update policy instead of silently skipping a required check.

The Python 3.12+ stdlib helper checks an explicit file list with the selected native parser; it does not run the script body:

```sh
python3 scripts/check-shell.py --dialect bash --interpreter /bin/bash path/to/script
python3 scripts/check-shell.py --dialect sh --interpreter /bin/sh path/to/script
```

It reads each shebang and refuses a declared-dialect or interpreter-name mismatch. Select a trusted native binary; matching a name does not authenticate its contents. Results are JSON on stdout, diagnostics on stderr; exits are 0 for syntax pass, 1 for findings, and 2 for usage, unreadable files or an unavailable parser. `--help` exits 0 without reading targets. Parser success proves syntax only; lint, portability and behavior remain separate checks. Native zsh can still read its installation's global zshenv; inspect an unfamiliar host before invoking it.

Read [references/behavior-fixtures.md](references/behavior-fixtures.md) when adding or repairing tests, including requests found through shell-script-testing. Exercise the public executable with hostile filenames, empty/unset input, missing dependencies, failed children, partial progress, interruption and repeat runs in a disposable directory. A supported OS/runtime needs an actual run or CI evidence on that target. Use the `project-guardrails` skill when installed and read first if the task includes wiring these checks into the repo's check command and CI.

Done when syntax, supported lint/format checks and behavioral fixtures pass on the declared targets. Report commands, interpreter/tool versions, exit codes, effects and every target or check not run; do not infer portability from one host.
