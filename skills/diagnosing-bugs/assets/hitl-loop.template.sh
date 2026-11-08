#!/usr/bin/env bash
# Human-in-the-loop reproduction loop. Runtime: Bash 3.2 or later.
# Copy this file to a scratch path, edit the steps below, and have the human
# run it in their own terminal (an agent's non-interactive shell cannot answer
# the prompts). The human pastes the "Captured" block back to the agent.
# Delete the copy when the diagnosis is done.
#
# Usage:
#   bash hitl-loop.sh
#
# Two helpers:
#   step "<instruction>"          → show instruction, wait for Enter
#   capture VAR "<question>"      → show question, read a one-line answer into VAR
#
# At the end, captured values are printed as KEY=VALUE for the agent to parse.
# Exit status: 0 when every step was answered, 1 when input ended early.
#
# `capture` prints its value back to the terminal, where the agent reads it,
# so capture observations only, never passwords or tokens, and leave signing
# in to the human as a `step`.

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _ || { printf '\ninput ended before this step\n' >&2; exit 1; }
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer || { printf '\ninput ended before an answer\n' >&2; exit 1; }
  printf -v "$var" '%s' "$answer"
}

# --- edit below ---------------------------------------------------------

step "Open the app at http://localhost:3000 and sign in."

capture ERRORED "Click the 'Export' button. Did it throw an error? (y/n)"

capture ERROR_MSG "Paste the error message (or 'none'):"

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
