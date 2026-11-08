#!/usr/bin/env bash
# Prove check-review.py: well-formed reports pass, each format defect fails with
# a message naming it, and usage errors exit 2.
set -uo pipefail

cd "$(dirname "$0")" || exit 2
check=../../skills/agent-debate/scripts/check-review.py
status=0
output=""

fail() { echo "agent-debate fixture failed: $1" >&2; status=1; }

# expect EXIT "MESSAGE" ARGS...: the checker exits EXIT and prints MESSAGE.
expect() {
  local want="$1" message="$2"; shift 2
  local got
  output="$(python3 "$check" "$@" 2>&1)"; got=$?
  if [ "$got" -ne "$want" ]; then
    fail "check-review.py $* exited $got, want $want. Output: $output"
  elif ! grep -qF -- "$message" <<<"$output"; then
    fail "check-review.py $* should print \"$message\". Output: $output"
  fi
}

expect 0 "matches the format" pass/agreement.md
expect 0 "matches the format" pass/nested-fences.md
expect 0 "matches the format" pass/objections.md
expect 0 "matches the format" --round 2 --prior R1-01,R1-02 pass/objections.md
expect 0 "matches the format" --round 4 --prior R1-01 pass/extension.md
expect 0 "matches the format" - < pass/agreement.md

expect 1 "malformed heading" fail/malformed-heading.md
expect 1 "unclosed code fence" fail/unclosed-fence.md
expect 1 "2 verdict lines" fail/two-verdicts.md
expect 1 "no verdict line" fail/no-verdict.md
expect 1 "malformed verdict" fail/malformed-verdict.md
expect 1 "not the last line" fail/verdict-not-last.md
expect 1 "Make them match" fail/count-mismatch.md
expect 1 "FULL AGREEMENT with 1 open findings" fail/agreement-with-findings.md
expect 1 "OBJECTIONS REMAIN with no findings" fail/objections-without-findings.md
expect 1 "repeats the ID" fail/duplicate-id.md
expect 1 "has severity [major]" fail/invalid-severity.md
expect 1 "has no severity" fail/missing-severity.md
expect 1 "R1-01 has no evidence" fail/missing-evidence.md
expect 1 "has Evidence with no label" fail/unlabeled-evidence.md
expect 1 "has Evidence (obvious)" fail/invalid-evidence-label.md
expect 1 "has no exact change" fail/missing-change.md
expect 1 "no REVIEWED line" fail/missing-reviewed.md
expect 1 "both open and marked" fail/open-and-closed.md
expect 1 "has status 'STILL OPEN'" fail/invalid-prior-status.md
expect 1 "open for 4 rounds (limit 3)" --round 4 fail/past-limit.md
expect 0 "matches the format" --round 4 --max-rounds 4 fail/past-limit.md
expect 1 "R1-03 was open after the last round but is missing" --prior R1-01,R1-03 pass/agreement.md
expect 1 "numbered for round 2, after the current round 1" --round 1 pass/objections.md

input_dir=$(mktemp -d)
trap 'rm -rf "$input_dir"' EXIT
printf '\377' > "$input_dir/invalid-utf8.md"
expect 2 "read a complete UTF-8 report" "$input_dir/invalid-utf8.md"
expect 2 "report not found" no-such-report.md
expect 2 "--round must be 1 or more" --round 0 pass/agreement.md
expect 2 "is not an ID like R1-01" --prior r1 pass/agreement.md
expect 2 "usage:" 

for file in fail/*.md; do
  [ "$file" = fail/past-limit.md ] && continue
  if python3 "$check" "$file" >/dev/null 2>&1; then
    fail "$file should fail without arguments"
  fi
done

[ "$status" -eq 0 ] && echo "check-review.py fixtures behave as expected."
exit "$status"
