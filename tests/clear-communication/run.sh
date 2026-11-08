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

for file in protected.md protected.txt; do
  expect_exit 0 "$file" "$check" "$file"
  [ -z "$output" ] || fail "$file should report nothing, got: $output"
done

expect_exit 1 "prose outside quotation" "$check" outside-source.md
[ "$(grep -c 'ClearCommunication.Filler' <<<"$output")" -eq 1 ] || fail "only prose outside the quotation should be flagged"

expect_exit 1 "unquoted contraction" "$check" unquoted-contraction.md
grep -q "ClearCommunication.Filler" <<<"$output" || fail "apostrophes must not hide unquoted prose"

expect_exit 2 "missing input file" "$check" no-such-fixture.md
expect_exit 2 "missing config argument" "$check" --config
expect_exit 2 "mixed stdin and files" sh -c "printf 'Press Enter.\n' | $check - errors.md"
expect_exit 2 "missing Vale" env VALE_BIN=/no-such-vale "$check" pass.md

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
