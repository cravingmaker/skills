# Comparison starter for a sourced function; never overwrite an existing function blindly.
# No external dependencies. Stdout: the argument unchanged. Stderr: usage.
# Exit: 0 success/help, 2 usage. No file or host changes.
show_literal() {
	emulate -L zsh
	case ${1-} in
	--help | -h)
		printf '%s\n' 'usage: show_literal VALUE' 'Exit: 0 success/help, 2 usage.'
		return 0
		;;
	esac
	if (($# != 1)); then
		printf '%s\n' 'error: pass exactly one literal value' >&2
		return 2
	fi
	local literal_value=$1
	printf '%s\n' "$literal_value"
}
