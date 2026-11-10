---
name: zsh-configuration
description: Diagnose or change macOS zsh startup and interactive state. Use when .zshrc, .zprofile, PATH, completion, a sourced function or shell startup time misbehaves. Executable shell scripts belong to shell-scripting; host package and service repairs stay with their owners.
---

# Zsh configuration

Find the startup context that produces the wrong state, change its owner, and compare the same context afterward.

## Reproduce the context

Record the resolved zsh/version, terminal or caller, login/interactive flags, ZDOTDIR, inherited PATH and relevant configuration files from authorized inspection. Keep raw environment and effective config private. Confirm whether a launcher or managed profile supplies the state; a terminal's interactive shell does not explain a scheduled job.

Read [references/startup-and-measurement.md](references/startup-and-measurement.md) before changing startup order, PATH, completion or plugins. Inspect the installation's global startup files and local `path_helper` manual before attributing macOS PATH order to it. Determine which file actually changes the value, including plugin and compiled startup files; keep the edit narrow.

Use the `shell-scripting` skill when installed and read first for an executable zsh/Bash/sh program. Hand package installation, launchd, managed settings and host-wide repairs to the host owner with the observed context and failing command.

Done when the failure is reproducible in the exact login, interactive or noninteractive context and its changing file or external owner is identified.

## Check a candidate without loading personal startup

Run `zsh -n` on the changed files, after inspecting the target installation's global zshenv. Check the installed shfmt help and [official manual](https://github.com/mvdan/sh/blob/master/cmd/shfmt/shfmt.1.scd) before using a zsh dialect; unavailable dialect support stays an unrun formatter check. ShellCheck does not prove zsh correctness.

For functions, compare [assets/zsh-function.zsh](assets/zsh-function.zsh) with the existing code. Use `emulate -L zsh` when a function needs local, predictable emulation/options; decide error handling inside that scope and test caller state after both success and failure. Avoid using special parameter names such as `path`, `status` or `commands` for ordinary locals.

The Python 3.12+ stdlib helper defaults to a no-execution plan:

```sh
python3 scripts/zsh-startup-probe.py --zsh /bin/zsh
python3 scripts/zsh-startup-probe.py --zsh /bin/zsh --run --disposable-root /absolute/disposable/probe
```

For `--run`, the directory must contain a regular `.zsh-probe-disposable` marker with `zsh-startup-probe` on its only line, a `candidate/` directory of reviewed startup files, and an empty `baseline/` directory. Build them only in an explicitly disposable test environment. Never point it at a real home or dotfile directory. It is a harness, not a sandbox: candidate code and global zshenv can have arbitrary effects. Do not run untrusted or credential-bearing startup code on the host.

The helper launches fresh, non-PTY shells with later global startup disabled, a minimal environment and a bounded wait. It captures source-file announcements rather than command xtrace. It emits only startup-file labels, elapsed time, output byte counts, selected option flags, ordered PATH fingerprints and duplicate/empty/missing entry counts; raw startup output never reaches the report. It compares baseline, noninteractive, login, interactive and combined modes. JSON goes to stdout, diagnostics to stderr; exits are 0 for completed probes, 1 for shell/protocol failures, and 2 for invalid inputs/setup. Help exits 0 without inspecting the host. Exit 0 is not a clean-output, performance or authority verdict.

Done when controlled starts explain the intended differences and a function leaves unrelated caller options unchanged. A non-PTY probe does not prove terminal UI behavior.

## Verify the actual user path

Compare before/after starts with the same environment, filesystem/cache state and shell modes; repeat to expose timing variation. Separate cold startup, warm startup and command latency. If the helper is insufficient, use a scoped `zprof` session or a private source-only trace on a reviewed disposable copy; inspect it locally without publishing values. Avoid raw `-x` traces of secret-bearing configuration.

Initialize completion after the final fpath setup; check the installed completion manual before changing compinit flags or dump validation. Verify PATH precedence with the actual commands that were wrong, completion in a real terminal, noninteractive output cleanliness and a fresh terminal session. Keep UI/plugin initialization conditional on interactive use. Preserve the user's unrelated dotfiles, options and package choices.

Done when the original command works in its actual context, the comparison records startup/output/option differences, and every untested mode or terminal behavior is explicit.
