#!/usr/bin/env bash
# Prove the ClearCommunication Vale style: errors fail, suggestions advise,
# protected content is skipped, stdin works, and the em-dash rule is opt-in.
set -uo pipefail

cd "$(dirname "$0")"
check=../../skills/clear-communication/scripts/check-prose.sh
status=0

fail() { echo "prose fixture failed: $1" >&2; status=1; }

expect_exit() {
  local want="$1" label="$2"; shift 2
  local got
  output="$("$@" 2>&1)"; got=$?
  [ "$got" -eq "$want" ] || fail "$label exited $got, want $want. Output: $output"
}

expect_exit 0 "pass.md" "$check" pass.md
[ -z "$output" ] || fail "pass.md should report nothing, got: $output"

expect_exit 1 "errors.md" "$check" errors.md
for rule in ChatbotPhrases Filler CurlyQuotes HeadingEmoji; do
  grep -q "ClearCommunication.$rule" <<<"$output" || fail "errors.md should trigger $rule"
done

expect_exit 0 "suggestions.md" "$check" suggestions.md
for rule in FancyIs PlainWords AIVocabulary Hedging Headings; do
  grep -q "ClearCommunication.$rule" <<<"$output" || fail "suggestions.md should suggest $rule"
done

expect_exit 1 "stdin" sh -c "$check - < errors.md"

expect_exit 1 "em dash opt-in" "$check" --config em-dash.ini pass.md
grep -q "ClearCommunication.EmDash" <<<"$output" || fail "em-dash.ini should enable EmDash"

[ "$status" -eq 0 ] && echo "ClearCommunication prose fixtures behave as expected."
exit "$status"
