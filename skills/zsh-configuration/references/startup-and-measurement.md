# Startup and measurement

Read this before changing startup order, PATH, completion or plugin initialization.

Zsh reads the installation's global zshenv even for `-f`. With the relevant startup options enabled, user .zshenv follows; login shells read profile files, interactive shells read rc files, and login shells then read login files. ZDOTDIR selects the user startup directory; an unset ZDOTDIR uses the account home. Global paths and compiled startup files depend on the installation. Check the [installed-version files manual](https://zsh.sourceforge.io/Doc/Release/Files.html) before relying on a file order.

Keep universal environment setup small. Put login-specific setup where the actual login caller reaches it, and UI, completion and prompt initialization in interactive branches. A changed option or ZDOTDIR inside one file can change which later files load; a static filename list does not prove execution.

## Controlled probes

Review startup code and its transitive `source` calls before executing it. Use an isolated disposable account/container/VM when it can write, invoke a manager or contact a service. A marked directory alone cannot contain arbitrary shell effects. The helper disables later global startup with `-d`, but global zshenv is unavoidable and a candidate can change startup options again.

Create `candidate/` and empty `baseline/` inside the explicitly disposable probe root, then add the marker required by the helper. Copy only the minimal reviewed files needed to reproduce the problem. Do not copy an entire personal home or credential file. The helper does not set HOME and must not substitute a fake home for a safety boundary.

The probe reports SHA-256 fingerprints for PATH comparison and selected shell options, not effective environment values. Ordered per-entry hashes and duplicate/empty/missing counts help compare PATH without publishing its entries; an absent directory is an observation, not automatic proof of a fault. File-order labels cover the five user startup filenames only; nested source order and globals require local inspection. A candidate can forge trace/protocol output, so this is an observation aid for owned code, not a security verifier.

Compare like modes and repeat runs. A shell error or missing report marker is a failure; extra output counts require operator interpretation. A clean `-c` session can still miss ZLE, terminal-dependent completion, inherited exported state or real login-file interactions. Recheck the original terminal/caller before claiming the repair.

## Primary references

- [Zsh files](https://zsh.sourceforge.io/Doc/Release/Files.html): startup conditions, global zshenv and compiled files.
- [Zsh options](https://zsh.sourceforge.io/Doc/Release/Options.html): verify RCS, GLOBAL_RCS, SOURCE_TRACE and local options in the installed version.
- [Zsh builtins](https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html): function emulation and option scope.
- [Zsh profiling module](https://zsh.sourceforge.io/Doc/Release/Zsh-Modules.html#The-zsh_002fzprof-Module): use when startup cost needs function-level evidence.
- The target Mac's `man path_helper` and actual global profile: check their current implementation rather than assuming PATH ordering from another host.
