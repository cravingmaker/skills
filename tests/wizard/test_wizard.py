#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["python-dotenv==1.1.1"]
# ///
"""Round-trip and safety tests for the wizard template's environment-file code.

Each case builds a real wizard from skills/wizard/assets/template.sh, runs it
with bash, and reads the file back with real parsers: python-dotenv, Node's
built-in parser (when node 20.12+ is on PATH) and a POSIX shell. Dummy values
only. Exit 0 when every case passes, 1 on any failure.
"""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "skills" / "wizard" / "assets" / "template.sh"
BASH = shutil.which("bash") or "bash"
NODE = shutil.which("node")
FAILURES: list[str] = []

WRITE_STAGE = """run_wizard() {
TOTAL_STAGES=1
WIZARD_TITLE="Test"
wizard_init "$@"
banner "$WIZARD_TITLE"
stage "write"
write_env "$WIZ_KEY" "$WIZ_VAL"
finish
}
run_wizard "$@"; exit
"""

READ_STAGE = """run_wizard() {
TOTAL_STAGES=1
WIZARD_TITLE="Test"
wizard_init "$@"
banner "$WIZARD_TITLE"
stage "read"
if [[ "${WIZ_SECRET:-0}" == 1 ]]; then ask_secret "$WIZ_KEY" "Value:"; else ask "$WIZ_KEY" "Value:"; fi
printf '%s' "${!WIZ_KEY}" > "$WIZ_OUT"
write_env "$WIZ_KEY" "${!WIZ_KEY}"
finish
}
run_wizard "$@"; exit
"""


def build(stage: str) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    library = text[: text.index("run_wizard() {")]
    return library + stage


def check(condition: bool, label: str) -> None:
    if not condition:
        FAILURES.append(label)
        print(f"FAIL {label}")


def run(work: Path, stage: str, env: dict[str, str], stdin: str = "\n\n", args: tuple[str, ...] = ()) -> subprocess.CompletedProcess:
    script = work / "wizard.sh"
    script.write_text(build(stage), encoding="utf-8")
    full_env = {"PATH": os.environ["PATH"], "HOME": str(work), "LC_ALL": "C", **env}
    return subprocess.run([BASH, str(script), *args], cwd=work, env=full_env, input=stdin,
                          capture_output=True, text=True)


def write(work: Path, key: str, value: str, **env: str) -> subprocess.CompletedProcess:
    return run(work, WRITE_STAGE, {"WIZ_KEY": key, "WIZ_VAL": value, **env})


def node_available() -> bool:
    if NODE is None:
        return False
    probe = subprocess.run([NODE, "-e", "process.exit(typeof require('util').parseEnv === 'function' ? 0 : 3)"])
    return probe.returncode == 0


def node_parse(path: Path) -> dict[str, str] | None:
    if not node_available():
        return None
    script = "const u=require('util'),f=require('fs');process.stdout.write(JSON.stringify(u.parseEnv(f.readFileSync(process.argv[1],'utf8'))))"
    out = subprocess.run([NODE, "-e", script, str(path)], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def sh_value(path: Path, key: str) -> str:
    out = subprocess.run(["sh", "-c", f'set -a; . "$1"; printf "%s" "${key}"', "sh", str(path)],
                         capture_output=True, text=True, check=True)
    return out.stdout


def fresh() -> Path:
    return Path(tempfile.mkdtemp(prefix="wizard-test-"))


DOTENV_ACCEPTED = [
    ("apostrophe", "O'Reilly"),
    ("plain", "pk_test_123"),
    ("empty", ""),
    ("dollar, double quote and hash", 'a$b"c#d'),
    ("spaces kept", "  spaced value  "),
    ("punctuation", "p@ss:w/rd+=%,"),
    ("backtick", "back`tick"),
    ("apostrophe and hash", "it's #1"),
]
DOTENV_REFUSED = [
    ("dollar braces", "${HOME}x"),
    ("backslash", "C:\\path"),
    ("trailing backslash", "abc\\"),
    ("newline", "line1\nline2"),
    ("carriage return", "a\rb"),
    ("apostrophe and double quote", "it's \"x\""),
    ("apostrophe and dollar", "$HOME's"),
    ("apostrophe and backtick", "it's `x`"),
]
SHELL_ACCEPTED = [
    ("apostrophe", "O'Reilly"),
    ("everything", "it's \"x\" $HOME \\ `y` #z"),
    ("empty", ""),
    ("only quotes", "''"),
]


def test_dotenv_round_trips() -> None:
    for label, value in DOTENV_ACCEPTED:
        work = fresh()
        result = write(work, "EXAMPLE_VALUE", value)
        check(result.returncode == 0, f"dotenv {label}: write exits 0 ({result.stderr.strip()})")
        env_file = work / ".env"
        check(dotenv_values(env_file).get("EXAMPLE_VALUE") == value, f"dotenv {label}: python-dotenv reads it back")
        parsed = node_parse(env_file)
        if parsed is not None:
            check(parsed.get("EXAMPLE_VALUE") == value, f"dotenv {label}: Node parseEnv reads it back")
        check(sh_value(env_file, "EXAMPLE_VALUE") == value, f"dotenv {label}: sh reads it back")
        before = env_file.read_bytes()
        out = work / "out"
        reread = run(work, READ_STAGE, {"WIZ_KEY": "EXAMPLE_VALUE", "WIZ_OUT": str(out)})
        check(reread.returncode == 0 and out.read_text() == value, f"dotenv {label}: re-run keeps the saved value")
        check(env_file.read_bytes() == before, f"dotenv {label}: repeating the write changes no byte")


def test_dotenv_refusals() -> None:
    for label, value in DOTENV_REFUSED:
        work = fresh()
        env_file = work / ".env"
        env_file.write_text("KEEP='1'\nEXAMPLE_VALUE='old'\n")
        before = env_file.read_bytes()
        result = write(work, "EXAMPLE_VALUE", value)
        check(result.returncode == 1, f"dotenv refuses {label}: exit 1")
        check(env_file.read_bytes() == before, f"dotenv refuses {label}: file unchanged")
        if value.strip():
            check(value not in result.stdout + result.stderr, f"dotenv refuses {label}: value not printed")


def test_shell_format() -> None:
    for label, value in SHELL_ACCEPTED:
        work = fresh()
        result = write(work, "EXAMPLE_VALUE", value, ENV_FORMAT="shell")
        check(result.returncode == 0, f"shell {label}: write exits 0 ({result.stderr.strip()})")
        env_file = work / ".env"
        check(sh_value(env_file, "EXAMPLE_VALUE") == value, f"shell {label}: sh reads it back")
        before = env_file.read_bytes()
        out = work / "out"
        reread = run(work, READ_STAGE, {"WIZ_KEY": "EXAMPLE_VALUE", "WIZ_OUT": str(out), "ENV_FORMAT": "shell"})
        check(reread.returncode == 0 and out.read_text() == value, f"shell {label}: re-run keeps the saved value")
        check(env_file.read_bytes() == before, f"shell {label}: repeating the write changes no byte")
    work = fresh()
    check(write(work, "EXAMPLE_VALUE", "a\nb", ENV_FORMAT="shell").returncode == 1, "shell refuses a newline")
    check(not (work / ".env").exists(), "shell newline refusal creates no file")


UNRELATED = (
    "# local settings\n"
    "\n"
    "export OTHER=1\n"
    "TARGET = 'old'\n"
    "PEM=\"-----BEGIN KEY-----\n"
    "TARGET=not-a-real-line\n"
    "-----END KEY-----\"\n"
    "AFTER='x y' # trailing comment\n"
    "export TARGET=dup\n"
    "LAST=no-newline"
)


def test_unrelated_keys_and_repeats() -> None:
    work = fresh()
    env_file = work / ".env"
    env_file.write_text(UNRELATED)
    result = write(work, "TARGET", "O'Reilly")
    check(result.returncode == 0, f"unrelated: write exits 0 ({result.stderr.strip()})")
    expected = UNRELATED.replace("TARGET = 'old'", 'TARGET="O\'Reilly"').replace("export TARGET=dup\n", "") + "\n"
    check(env_file.read_text() == expected, "unrelated: only the TARGET assignments change")
    values = dotenv_values(env_file)
    check(values.get("TARGET") == "O'Reilly", "unrelated: python-dotenv sees the new TARGET")
    check(values.get("PEM", "").count("\n") == 2, "unrelated: multi-line PEM kept")
    check(values.get("LAST") == "no-newline", "unrelated: last line without newline kept")
    for value in ("second", "third", "third"):
        write(work, "TARGET", value)
    text = env_file.read_text()
    check(text.count("TARGET='third'") == 1 and dotenv_values(env_file).get("TARGET") == "third",
          "repeats: one TARGET line with the latest value")
    check("TARGET=not-a-real-line" in text, "repeats: continuation line inside PEM untouched")

    blocked = fresh()
    (blocked / ".env").write_text('TARGET="line1\nline2"\nKEEP=1\n')
    before = (blocked / ".env").read_bytes()
    result = write(blocked, "TARGET", "new")
    check(result.returncode == 1 and (blocked / ".env").read_bytes() == before,
          "multi-line target: refused and file unchanged")


def test_permissions_and_symlinks() -> None:
    work = fresh()
    write(work, "A", "1")
    check(stat.S_IMODE((work / ".env").stat().st_mode) == 0o600, "new file is mode 0600")
    (work / ".env").chmod(0o640)
    write(work, "A", "2")
    check(stat.S_IMODE((work / ".env").stat().st_mode) == 0o640, "existing mode kept")

    linked = fresh()
    target = linked / "real.env"
    target.write_text("A='1'\n")
    (linked / ".env").symlink_to(target)
    result = write(linked, "A", "2")
    check(result.returncode == 1 and target.read_text() == "A='1'\n", "symlink refused by default")
    result = write(linked, "A", "2", WIZARD_ENV_FOLLOW_SYMLINK="1")
    check(result.returncode == 0 and target.read_text() == "A='2'\n" and (linked / ".env").is_symlink(),
          "symlink written through when opted in")


def test_destination_scope() -> None:
    for label, path in (("absolute", "/tmp/wizard-escape.env"), ("parent", "../escape.env"),
                        ("nested parent", "sub/../../escape.env"), ("missing dir", "nope/.env")):
        work = fresh()
        result = write(work, "A", "1", ENV_FILE=path)
        check(result.returncode == 1, f"destination {label}: refused")
    check(not Path("/tmp/wizard-escape.env").exists(), "destination: nothing written outside")
    if shutil.which("git"):
        work = fresh()
        subprocess.run(["git", "init", "-q"], cwd=work, check=True)
        (work / ".env").write_text("A='1'\n")
        subprocess.run(["git", "add", ".env"], cwd=work, check=True)
        result = write(work, "A", "2")
        check(result.returncode == 1 and (work / ".env").read_text() == "A='1'\n", "git-tracked file refused")
        result = write(work, "A", "2", WIZARD_ENV_ALLOW_TRACKED="1")
        check(result.returncode == 0, "git-tracked file allowed when opted in")
        other = fresh()
        subprocess.run(["git", "init", "-q"], cwd=other, check=True)
        result = write(other, "A", "1")
        check(result.returncode == 0 and "not ignored by git" in result.stdout, "untracked, unignored file warns")


def test_hidden_input_and_secret_safe_output() -> None:
    secret = "sk_test_DUMMY_9f8e7d"
    work = fresh()
    out = work / "out"
    result = run(work, READ_STAGE, {"WIZ_KEY": "SECRET_KEY", "WIZ_OUT": str(out), "WIZ_SECRET": "1"},
                 stdin=f"\n{secret}\n")
    check(result.returncode == 0 and out.read_text() == secret, "ask_secret captures the value")
    check(secret not in result.stdout + result.stderr, "ask_secret and write_env never print the value")
    result = run(work, READ_STAGE, {"WIZ_KEY": "SECRET_KEY", "WIZ_OUT": str(out), "WIZ_SECRET": "1"})
    check(result.returncode == 0 and out.read_text() == secret, "Enter keeps the saved secret")
    check(secret not in result.stdout + result.stderr, "re-run does not show the saved secret")


def test_cli() -> None:
    work = fresh()
    result = run(work, WRITE_STAGE, {"WIZ_KEY": "A", "WIZ_VAL": "1"}, args=("--help",))
    check(result.returncode == 0 and "Usage:" in result.stdout and not (work / ".env").exists(), "--help exits 0 with no effect")
    result = run(work, WRITE_STAGE, {"WIZ_KEY": "A", "WIZ_VAL": "1"}, args=("--dry-run",))
    check(result.returncode == 0 and "would write" in result.stdout and not (work / ".env").exists(), "--dry-run writes nothing")
    result = run(work, WRITE_STAGE, {"WIZ_KEY": "A", "WIZ_VAL": "1"}, args=("--bogus",))
    check(result.returncode == 2, "unknown option exits 2")
    result = write(work, "A", "1", ENV_FORMAT="yaml")
    check(result.returncode == 2 and not (work / ".env").exists(), "unknown ENV_FORMAT exits 2")
    check(subprocess.run([BASH, "-n", str(TEMPLATE)]).returncode == 0, "template passes bash -n")


def main() -> int:
    for test in (test_dotenv_round_trips, test_dotenv_refusals, test_shell_format, test_unrelated_keys_and_repeats,
                 test_permissions_and_symlinks, test_destination_scope, test_hidden_input_and_secret_safe_output, test_cli):
        test()
    version = subprocess.run([BASH, "-c", "echo $BASH_VERSION"], capture_output=True, text=True).stdout.strip()
    node = "checked" if node_available() else "skipped (node 20.12+ not found)"
    if FAILURES:
        print(f"wizard: {len(FAILURES)} failure(s) with bash {version}; Node parser {node}")
        return 1
    print(f"wizard: all cases passed with bash {version}; python-dotenv and sh checked; Node parser {node}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
