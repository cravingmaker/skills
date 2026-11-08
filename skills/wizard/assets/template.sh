#!/usr/bin/env bash
#
# A wizard walks a human through a manual procedure, step by step.
# Generated with the wizard skill. Runtime: Bash 3.2 or later (the macOS
# default works); no other dependencies. gh is optional, for CI secrets.
#
# Usage: ./wizard.sh [--dry-run] [--help]
#   --dry-run  walk every stage and show what would be written, change nothing
#   --help     print this usage and exit
# Exit status: 0 finished, 1 a value or destination was refused (nothing was
# written for it), 2 usage error. Values saved before a refusal stay saved, so
# a re-run resumes with them as defaults.
#
# Environment:
#   ENV_FILE    destination file, relative to the current directory (default .env)
#   ENV_FORMAT  dotenv (default) or shell; see "Environment file" below
#   WIZARD_ENV_FOLLOW_SYMLINK=1  allow ENV_FILE to be a symlink
#   WIZARD_ENV_ALLOW_TRACKED=1   allow ENV_FILE to be a file git tracks
#
# The library above the STAGES marker is shared by every wizard. Change it when
# the procedure needs to, and rerun tests/wizard/run.sh after any change to the
# environment-file code.

set -euo pipefail

# ──────────────────────────────────────────────────────────────────────────
# Wizard library
# ──────────────────────────────────────────────────────────────────────────

if [[ -t 1 ]] && command -v tput >/dev/null 2>&1 && [[ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]]; then
  BOLD=$(tput bold); DIM=$(tput dim); RESET=$(tput sgr0)
  BLUE=$(tput setaf 4); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3)
else
  BOLD=""; DIM=""; RESET=""; BLUE=""; GREEN=""; YELLOW=""
fi

# Author sets these at the top of run_wizard.
TOTAL_STAGES=0
WIZARD_TITLE="Wizard"

_STAGE_INDEX=0
ENV_FILE="${ENV_FILE:-.env}"
ENV_FORMAT="${ENV_FORMAT:-dotenv}"
WIZARD_DRY_RUN=0
WRITTEN_ENV=()    # KEYs written to ENV_FILE this run
WRITTEN_SECRET=() # secret NAMEs set this run
SKIPPED=()        # things we couldn't do (e.g. gh missing)
_ENV_TMP=""

trap '[[ -n "$_ENV_TMP" ]] && rm -f "$_ENV_TMP"' EXIT

# wizard_init "$@" handles --help and --dry-run. Call it once, first.
wizard_init() {
  while (( $# )); do
    case "$1" in
      -h|--help)
        printf '%s: %s stage(s).\n' "$WIZARD_TITLE" "$TOTAL_STAGES"
        printf 'Usage: %s [--dry-run] [--help]\n' "$0"
        printf 'Writes values to %s (format %s). Exit 0 finished, 1 refused, 2 usage.\n' "$ENV_FILE" "$ENV_FORMAT"
        exit 0 ;;
      --dry-run) WIZARD_DRY_RUN=1 ;;
      *) printf 'unknown option: %s (try --help)\n' "$1" >&2; exit 2 ;;
    esac
    shift
  done
  case "$ENV_FORMAT" in
    dotenv|shell) ;;
    *) printf 'ENV_FORMAT must be dotenv or shell, got %s\n' "$ENV_FORMAT" >&2; exit 2 ;;
  esac
}

# _clear wipes the terminal so only the current step is on screen. No-op when
# output isn't a terminal, so piped logs stay readable.
_clear() {
  [[ -t 1 ]] || return 0
  if command -v tput >/dev/null 2>&1 && tput clear 2>/dev/null; then return 0; fi
  printf '\033[2J\033[3J\033[H'
}

# banner "Title" shows the opening frame: what this wizard does.
banner() {
  _clear
  printf '\n%s%s  %s%s\n' "$BOLD" "$BLUE" "$1" "$RESET"
  printf '%s  %s stages%s\n\n' "$DIM" "$TOTAL_STAGES" "$RESET"
  (( WIZARD_DRY_RUN )) && printf '  %sDry run: nothing will be written.%s\n\n' "$YELLOW" "$RESET"
  printf '%s  You drive the browser; this wizard tells you exactly what to do and\n' "$DIM"
  printf '  captures the values you copy back. Stop any time with Ctrl-C and re-run\n'
  printf '  later, since it remembers values already saved.%s\n' "$RESET"
  pause "Ready to start?"
}

# stage "Name" clears the screen, then announces a stage and shows progress.
stage() {
  _clear
  _STAGE_INDEX=$((_STAGE_INDEX + 1))
  printf '\n%s%s▸ Stage %s/%s · %s%s\n' \
    "$BOLD" "$BLUE" "$_STAGE_INDEX" "$TOTAL_STAGES" "$1" "$RESET"
}

# say "..." prints a plain instruction line.
say()  { printf '  %s\n' "$1"; }
# step "..." is a numbered-feeling action the human takes in the browser.
step() { printf '  %s•%s %s\n' "$BLUE" "$RESET" "$1"; }
note() { printf '  %s%s%s\n' "$DIM" "$1" "$RESET"; }
warn() { printf '  %s⚠ %s%s\n' "$YELLOW" "$1" "$RESET"; }

# _die "message" names the fix on stderr and stops with status 1.
_die() { printf '%s✗ %s%s\n' "$YELLOW" "$1" "$RESET" >&2; exit 1; }

# open_url URL opens it in the human's browser, cross-platform incl. WSL.
open_url() {
  local url="$1"
  printf '  %s↗ opening%s %s\n' "$GREEN" "$RESET" "$url"
  { if   command -v wslview     >/dev/null 2>&1; then wslview "$url"
    elif command -v explorer.exe >/dev/null 2>&1; then explorer.exe "$url"
    elif command -v xdg-open    >/dev/null 2>&1; then xdg-open "$url"
    elif command -v open        >/dev/null 2>&1; then open "$url"
    else false; fi
  } >/dev/null 2>&1 || warn "couldn't open a browser, so visit it manually: $url"
}

# pause "msg" waits for the human to confirm they've done the manual part.
pause() {
  printf '  %s%s%s ' "$DIM" "${1:-Press Enter to continue}" "$RESET"
  read -r _ || true
}

# confirm "question" is a y/N gate; returns success on yes.
confirm() {
  local reply=""
  printf '  %s? %s [y/N] ' "$YELLOW" "$1"
  read -r reply || true
  [[ "$reply" =~ ^[Yy] ]]
}

# ── Environment file ──────────────────────────────────────────────────────
# ENV_FORMAT=dotenv writes only values that npm dotenv, Node's built-in
# parser, python-dotenv and a POSIX shell all read back unchanged:
#   no ' and no backslash   KEY='value'
#   a ' but no " \ $ `      KEY="value"
# Anything else is refused before the file changes: a backslash, a line
# break, ${ (python-dotenv expands it even in single quotes), or ' together
# with " $ or `.
# ENV_FORMAT=shell is for files only ever sourced by sh/bash: it writes
# KEY='value' with each ' as '\'' and refuses only line breaks.
# Projects that add interpolation (dotenv-expand, Compose) must still check
# values containing $ with their own loader.

_env_key_ok() { [[ "$1" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; }

# _env_encode KEY VALUE prints the line to write, or fails naming the problem.
_env_encode() {
  local key="$1" value="$2" sq="'\\''"
  case "$value" in
    *$'\n'*|*$'\r'*) printf '%s contains a line break, which %s files here cannot hold' "$key" "$ENV_FORMAT"; return 1 ;;
  esac
  if [[ "$ENV_FORMAT" == shell ]]; then
    printf "%s='%s'" "$key" "${value//\'/$sq}"
  elif [[ "$value" == *'${'* ]]; then
    printf '%s contains ${, which python-dotenv expands even in single quotes' "$key"
    return 1
  elif [[ "$value" != *[\'\\]* ]]; then
    printf "%s='%s'" "$key" "$value"
  elif [[ "$value" != *[\"\\\$\`]* ]]; then
    printf '%s="%s"' "$key" "$value"
  else
    printf '%s contains a backslash, or a single quote together with " $ or `, which common dotenv parsers read differently' "$key"
    return 1
  fi
}

# _env_decode RAW prints the value RAW (the text after KEY=) stands for, or
# fails when it is not one of the unambiguous forms this library writes.
_env_decode() {
  local raw="$1" inner sq="'\\''" q="'"
  raw="${raw#"${raw%%[![:space:]]*}"}"; raw="${raw%"${raw##*[![:space:]]}"}"
  if [[ "$raw" == \'*\' && ${#raw} -ge 2 ]]; then
    inner="${raw:1:${#raw}-2}"
    if [[ "$ENV_FORMAT" == shell ]]; then
      local rest="${inner//"$sq"/}"
      [[ "$rest" != *\'* ]] || return 1
      printf '%s' "${inner//"$sq"/$q}"
    else
      [[ "$inner" != *[\'\\]* ]] || return 1
      printf '%s' "$inner"
    fi
  elif [[ "$raw" == \"*\" && ${#raw} -ge 2 ]]; then
    inner="${raw:1:${#raw}-2}"
    [[ "$inner" != *[\"\\\$\`]* ]] || return 1
    printf '%s' "$inner"
  elif [[ "$raw" =~ ^[A-Za-z0-9_./:@+,%=-]*$ ]]; then
    printf '%s' "$raw"
  else
    return 1
  fi
}

# _env_split LINE: sets _K (the key the line assigns, or empty) and _V (the
# raw value text). Accepts KEY=, KEY =, and export KEY= forms.
_env_split() {
  local line="$1" re='^[[:space:]]*(export[[:space:]]+)?([A-Za-z_][A-Za-z0-9_]*)[[:space:]]*=(.*)$'
  _K=""; _V=""; _EXPORT=""
  if [[ "$line" =~ $re ]]; then
    _EXPORT="${BASH_REMATCH[1]}"; _K="${BASH_REMATCH[2]}"; _V="${BASH_REMATCH[3]}"
  fi
}

# _env_quote_closes TEXT QUOTE finds a closing quote, honoring escaped quotes
# in dotenv and shell double quotes. Backslashes are literal in shell single quotes.
_env_quote_closes() {
  local text="$1" quote="$2" char escaped=0 i
  for (( i=0; i<${#text}; i++ )); do
    char="${text:i:1}"
    if (( escaped )); then escaped=0; continue; fi
    if [[ "$char" == '\' && ( "$ENV_FORMAT" != shell || "$quote" != "'" ) ]]; then
      escaped=1
    elif [[ "$char" == "$quote" ]]; then
      return 0
    fi
  done
  return 1
}

# _env_opens_block RAW: succeeds when RAW starts a quoted value that does not
# close on the same line (a multi-line value), and sets _Q to its quote.
_env_opens_block() {
  local raw="$1" q rest
  raw="${raw#"${raw%%[![:space:]]*}"}"
  q="${raw:0:1}"
  [[ "$q" == "'" || "$q" == '"' || "$q" == '`' ]] || return 1
  rest="${raw:1}"
  _env_quote_closes "$rest" "$q" && return 1
  _Q="$q"
}

# _existing KEY prints KEY's saved value when the file holds it in a form this
# library can read back exactly; otherwise it fails and the wizard asks again.
_existing() {
  local key="$1" line found=1 value="" block=""
  [[ -f "$ENV_FILE" ]] || return 1
  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ -n "$block" ]]; then _env_quote_closes "$line" "$block" && block=""; continue; fi
    _env_split "$line"
    [[ -n "$_K" ]] || continue
    if _env_opens_block "$_V"; then
      block="$_Q"; [[ "$_K" == "$key" ]] && found=2
      continue
    fi
    if [[ "$_K" == "$key" ]]; then
      if value=$(_env_decode "$_V"); then found=0; else found=2; fi
    fi
  done < "$ENV_FILE"
  (( found == 0 )) || return 1
  printf '%s' "$value"
}

# _env_destination_ok refuses an ENV_FILE outside the current directory, a
# symlink, a non-regular file, or a file git tracks, unless opted in above.
_env_destination_ok() {
  local dir root resolved parent link hops=0
  case "$ENV_FILE" in
    ''|/*) _die "ENV_FILE must be a path inside this directory, got '$ENV_FILE'" ;;
  esac
  case "/$ENV_FILE/" in
    */../*) _die "ENV_FILE must not leave this directory: '$ENV_FILE'" ;;
  esac
  dir=$(dirname -- "$ENV_FILE")
  [[ -d "$dir" ]] || _die "the directory for $ENV_FILE does not exist; create it first"
  if [[ -L "$ENV_FILE" && "${WIZARD_ENV_FOLLOW_SYMLINK:-0}" != 1 ]]; then
    _die "$ENV_FILE is a symlink; set WIZARD_ENV_FOLLOW_SYMLINK=1 to write through it"
  fi
  root=$(pwd -P)
  parent=$(CDPATH='' cd -P -- "$dir" && pwd -P) || _die "cannot resolve the directory for $ENV_FILE"
  case "$parent/" in
    "${root%/}/"*) ;;
    *) _die "the resolved directory for $ENV_FILE leaves this directory" ;;
  esac
  resolved="$parent/$(basename -- "$ENV_FILE")"
  while [[ -L "$resolved" ]]; do
    hops=$((hops + 1))
    (( hops <= 40 )) || _die "$ENV_FILE has a symlink loop; use a regular file inside this directory"
    link=$(readlink "$resolved") || _die "cannot resolve $ENV_FILE; use a regular file"
    case "$link" in
      /*) resolved="$link" ;;
      *) resolved="$(dirname -- "$resolved")/$link" ;;
    esac
    parent=$(CDPATH='' cd -P -- "$(dirname -- "$resolved")" && pwd -P) || _die "cannot resolve $ENV_FILE"
    case "$parent/" in
      "${root%/}/"*) ;;
      *) _die "the symlink target for $ENV_FILE leaves this directory" ;;
    esac
    resolved="$parent/$(basename -- "$resolved")"
  done
  if [[ -e "$ENV_FILE" && ! -f "$ENV_FILE" ]]; then
    _die "$ENV_FILE is not a regular file"
  fi
  if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if git ls-files --error-unmatch -- "$resolved" >/dev/null 2>&1; then
      [[ "${WIZARD_ENV_ALLOW_TRACKED:-0}" == 1 ]] ||
        _die "$ENV_FILE is tracked by git, so its values would be committed; untrack it or set WIZARD_ENV_ALLOW_TRACKED=1"
    elif ! git check-ignore -q -- "$resolved" 2>/dev/null; then
      warn "$ENV_FILE is not ignored by git; add it to .gitignore before committing"
    fi
  fi
}

# ask KEY "Prompt" reads a value into $KEY. Offers the saved value as the
# default on re-runs (Enter keeps it), without showing it. Visible input
# (non-secret), edited with Readline. Fails at EOF with no input.
ask() {
  local key="$1" prompt="$2" current input s=$'\001' e=$'\002' p rc=0
  current=$(_existing "$key" || true)
  # Readline needs the colour codes wrapped in \001..\002 to place the cursor.
  p="  $s$BOLD$e$prompt$s$RESET$e "
  [[ -n "$current" ]] && p+="$s$DIM$e[Enter keeps current]$s$RESET$e "
  read -e -r -p "$p" input || rc=1
  if (( rc )) && [[ -z "$input" ]]; then return 1; fi
  [[ -z "$input" && -n "$current" ]] && input="$current"
  printf -v "$key" '%s' "$input"
}

# ask_secret KEY "Prompt" is like ask, but input is hidden.
ask_secret() {
  local key="$1" prompt="$2" current input rc=0
  current=$(_existing "$key" || true)
  if [[ -n "$current" ]]; then
    printf '  %s%s%s %s[Enter keeps current]%s ' "$BOLD" "$prompt" "$RESET" "$DIM" "$RESET"
  else
    printf '  %s%s%s ' "$BOLD" "$prompt" "$RESET"
  fi
  read -rs input || rc=1
  printf '\n'
  if (( rc )) && [[ -z "$input" ]]; then return 1; fi
  [[ -z "$input" && -n "$current" ]] && input="$current"
  printf -v "$key" '%s' "$input"
}

# write_env KEY VALUE upserts KEY into ENV_FILE in ENV_FORMAT and sets $KEY.
# The line replaces KEY's first assignment in place; later duplicates are
# dropped; every other line, comment and multi-line value is kept byte for
# byte. A new file is created at mode 0600; an existing file keeps its mode.
# Refuses (exit 1, file unchanged) a value the format cannot hold, a KEY that
# is part of a multi-line value, or an unsafe destination. Never prints VALUE.
write_env() {
  local key="$1" value="$2" newline reason line block="" placed=0 exported=0 terminated=1 last_terminated=1
  _env_key_ok "$key" || { printf 'write_env: invalid key %s\n' "$key" >&2; exit 2; }
  if ! newline=$(_env_encode "$key" "$value"); then
    reason="$newline"
    _die "not saved: $reason. Set it by hand or in the project's secret store."
  fi
  _env_destination_ok
  if [[ -f "$ENV_FILE" ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
      if [[ -n "$block" ]]; then _env_quote_closes "$line" "$block" && block=""; continue; fi
      _env_split "$line"
      [[ "$_K" == "$key" && -n "$_EXPORT" ]] && exported=1
      if [[ -n "$_K" ]] && _env_opens_block "$_V"; then
        [[ "$_K" == "$key" ]] && _die "not saved: $key in $ENV_FILE spans several lines; edit it by hand"
        block="$_Q"
      fi
    done < "$ENV_FILE"
    [[ -z "$block" ]] || _die "not saved: $ENV_FILE has an unterminated quoted value; repair it first"
  fi
  (( exported )) && newline="export $newline"
  if (( WIZARD_DRY_RUN )); then
    printf -v "$key" '%s' "$value"
    printf '  %s∘ would write%s %s → %s\n' "$DIM" "$RESET" "$key" "$ENV_FILE"
    return 0
  fi
  if [[ ! -e "$ENV_FILE" ]]; then (umask 077 && : > "$ENV_FILE"); fi
  _ENV_TMP=$(mktemp "$(dirname -- "$ENV_FILE")/.wizard-env.XXXXXX")
  cp -p "$ENV_FILE" "$_ENV_TMP" 2>/dev/null || true
  {
    block=""
    while :; do
      terminated=1
      IFS= read -r line || terminated=0
      [[ -n "$line" ]] || (( terminated )) || break
      if [[ -n "$block" ]]; then
        printf '%s' "$line"
        (( terminated )) && printf '\n'
        last_terminated=$terminated
        _env_quote_closes "$line" "$block" && block=""
        continue
      fi
      _env_split "$line"
      if [[ -n "$_K" ]] && _env_opens_block "$_V"; then block="$_Q"; fi
      if [[ "$_K" == "$key" ]]; then
        if (( ! placed )); then
          printf '%s' "$newline"
          (( terminated )) && printf '\n'
          last_terminated=$terminated
        fi
        placed=1
      else
        printf '%s' "$line"
        (( terminated )) && printf '\n'
        last_terminated=$terminated
      fi
    done < "$ENV_FILE"
    if (( ! placed )); then
      (( last_terminated )) || printf '\n'
      printf '%s\n' "$newline"
    fi
  } > "$_ENV_TMP"
  if [[ -L "$ENV_FILE" ]]; then
    cat "$_ENV_TMP" > "$ENV_FILE"; rm -f "$_ENV_TMP"
  else
    mv -f "$_ENV_TMP" "$ENV_FILE"
  fi
  _ENV_TMP=""
  printf -v "$key" '%s' "$value"
  WRITTEN_ENV+=("$key")
  printf '  %s✓ wrote%s %s → %s\n' "$GREEN" "$RESET" "$key" "$ENV_FILE"
}

# set_secret NAME VALUE sets a GitHub Actions repo secret via gh, passing the
# value on stdin. Falls back to a warning (and records it) if gh is
# unavailable or unauthenticated.
set_secret() {
  local name="$1" value="$2"
  if (( WIZARD_DRY_RUN )); then
    printf '  %s∘ would set%s GitHub secret %s\n' "$DIM" "$RESET" "$name"; return 0
  fi
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if printf '%s' "$value" | gh secret set "$name" >/dev/null 2>&1; then
      WRITTEN_SECRET+=("$name")
      printf '  %s✓ set%s GitHub secret %s\n' "$GREEN" "$RESET" "$name"
      return
    fi
  fi
  SKIPPED+=("GitHub secret $name (set it manually: gh secret set $name)")
  warn "skipped GitHub secret $name: gh not ready; set it later"
}

# set_var NAME VALUE sets a GitHub Actions repo variable (non-secret: the
# value is passed as an argument).
set_var() {
  local name="$1" value="$2"
  if (( WIZARD_DRY_RUN )); then
    printf '  %s∘ would set%s GitHub variable %s\n' "$DIM" "$RESET" "$name"; return 0
  fi
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if gh variable set "$name" --body "$value" >/dev/null 2>&1; then
      printf '  %s✓ set%s GitHub variable %s\n' "$GREEN" "$RESET" "$name"
      return
    fi
  fi
  SKIPPED+=("GitHub variable $name")
  warn "skipped GitHub variable $name, gh not ready; set it later"
}

# finish clears, then shows a closing summary of everything configured.
finish() {
  _clear
  if (( WIZARD_DRY_RUN )); then
    printf '\n%s%s  ✓ Dry run complete: nothing was written%s\n\n' "$BOLD" "$GREEN" "$RESET"
    return 0
  fi
  printf '\n%s%s  ✓ Setup complete%s\n' "$BOLD" "$GREEN" "$RESET"
  (( ${#WRITTEN_ENV[@]} ))    && note "wrote ${#WRITTEN_ENV[@]} value(s) to $ENV_FILE: ${WRITTEN_ENV[*]}"
  (( ${#WRITTEN_SECRET[@]} )) && note "set ${#WRITTEN_SECRET[@]} GitHub secret(s): ${WRITTEN_SECRET[*]}"
  if (( ${#SKIPPED[@]} )); then
    printf '\n'; warn "still to do by hand:"
    for s in "${SKIPPED[@]}"; do note "  - $s"; done
  fi
  printf '\n'
}

# ──────────────────────────────────────────────────────────────────────────
# STAGES: author this section. One stage() per step the human takes.
# Replace the example below. Set TOTAL_STAGES to match the stages you write.
# Keep every stage inside run_wizard and the last line as is: bash then parses
# the whole file before the first prompt, so an edit mid-run can't break it.
# ──────────────────────────────────────────────────────────────────────────

run_wizard() {

TOTAL_STAGES=1
WIZARD_TITLE="Stripe setup"
wizard_init "$@"

banner "$WIZARD_TITLE"

# ── Example stage: replace with your real steps ───────────────────────────
stage "Stripe: API keys"
say "We'll grab your Stripe test keys and store them for local dev + CI."
open_url "https://dashboard.stripe.com/test/apikeys"
step "On the API keys page, copy the Publishable key (starts pk_test_)."
ask STRIPE_PUBLISHABLE_KEY "Paste the publishable key:"
step "Click 'Reveal test key' on the Secret key row, then copy it."
ask_secret STRIPE_SECRET_KEY "Paste the secret key:"
write_env STRIPE_PUBLISHABLE_KEY "$STRIPE_PUBLISHABLE_KEY"
write_env STRIPE_SECRET_KEY "$STRIPE_SECRET_KEY"
set_secret STRIPE_SECRET_KEY "$STRIPE_SECRET_KEY"   # CI needs this one
# ──────────────────────────────────────────────────────────────────────────

finish
}

run_wizard "$@"; exit
