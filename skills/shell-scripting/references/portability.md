# Portability and process boundaries

Read this when a script crosses OSes, shell versions or quoting boundaries.

| Boundary | Check |
| --- | --- |
| Interpreter | Inspect the shebang and resolved executable/version in each target. Test the minimum supported Bash with that binary; newer parsers accept syntax older targets reject. |
| Utilities | Check the target manuals for `sed -i`, `date`, `stat`, `readlink`, `mktemp`, `grep`, `xargs`, `base64` and timeout/locking tools. A flag that works on one BSD/GNU release is not a portable contract. Declare a dependency or select a tested alternative. |
| POSIX sh | Avoid Bash arrays, `[[ ... ]]`, process substitution and Bash-only options. Use a POSIX analyzer and the actual target sh; an implementation's extensions can pass its own parser. |
| Bash versions | Gate newer arrays, expansion forms and builtins against the declared minimum. Empty arrays under nounset and command-substitution error handling need behavior tests on that version. |
| zsh | Check scalar splitting, array indexing, unmatched globs and special parameters against the installed manual. ShellCheck output is not zsh lint evidence. |
| Nested command | The local shell, remote shell and structured format each own a parsing layer. Prefer an argument vector, stdin or a format-native serializer to concatenated command text. |

Keep filenames as arguments. Test spaces, tabs, newlines, glob characters, an empty string and a leading dash independently. A path containing `$(...)` must stay literal; use an inert sentinel in a disposable test directory to prove no command substitution occurs.

Resolve tool versions using the target project's pins and official releases when used. This skill embeds no current-release or platform-version claim.

## Primary references

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/bash.html): read the installed version's option, expansion and invocation semantics when relying on them.
- [POSIX shell language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html): read when promising a POSIX contract.
- [Zsh expansion](https://zsh.sourceforge.io/Doc/Release/Expansion.html) and [parameters](https://zsh.sourceforge.io/Doc/Release/Parameters.html): read when writing executable zsh.
- [ShellCheck dialect support](https://www.shellcheck.net/wiki/SC1071) and [shfmt manual](https://github.com/mvdan/sh/blob/master/cmd/shfmt/shfmt.1.scd): verify installed tool support before linting.
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html): method reference for language choice and shell complexity; no text or code is copied here.
