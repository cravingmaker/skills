#!/usr/bin/env bash
# Comparison starter: declare and test the supported Bash/OS versions in the caller.
# Stdout: data/help. Stderr: diagnostics. Exit: 0 success/help, 1 failure, 2 usage.
# This starter creates scratch data only after --disposable-dir is explicit.
set -eu

usage() {
	printf '%s\n' 'usage: script --disposable-dir DIRECTORY' 'Exit: 0 success/help, 1 failure, 2 usage. No prompts.'
}
case ${1-} in
--help | -h)
	usage
	exit 0
	;;
esac
if [ "$#" -ne 2 ] || [ "$1" != --disposable-dir ] || [ ! -d "$2" ]; then
	printf '%s\n' 'error: pass an existing disposable directory with --disposable-dir' >&2
	exit 2
fi
scratch_dir=$(mktemp -d "${2%/}/shell-work.XXXXXX") || {
	printf '%s\n' 'error: create scratch data in a writable disposable directory' >&2
	exit 1
}
cleanup() {
	operation_status=$?
	trap - EXIT
	rm -rf -- "$scratch_dir" || printf '%s\n' 'error: remove the reported scratch directory manually' >&2
	exit "$operation_status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
# Add validated work here; handle each critical failure explicitly.
printf '%s\n' 'No operation configured.'
