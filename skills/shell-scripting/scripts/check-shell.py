#!/usr/bin/env python3
"""Check explicit executable files with the declared native shell parser.

Python 3.12+ stdlib; requires the caller's selected shell, never installs tools.
Usage: check-shell.py --dialect {sh,bash,zsh} --interpreter /absolute/shell FILE...
Stdout: JSON file-index findings only. Stderr: setup/input diagnostics.
Exit: 0 syntax pass, 1 findings, 2 usage/input/parser setup. No prompts or writes.
--help exits 0 without reading a file or invoking a shell. This is syntax only;
run the project's pinned linter/formatter and real behavioral tests separately.
Native zsh still reads its installation's global zshenv, even with -f.
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path


def shebang_dialect(content):
    lines = content.splitlines()
    first = lines[0] if lines else b""
    if not first.startswith(b"#!"):
        return None
    try:
        words = shlex.split(first[2:].decode("utf-8"))
    except (UnicodeError, ValueError):
        return None
    if not words:
        return None
    name = Path(words[0]).name
    if name == "env":
        words = words[1:]
        if words[:1] == ["-S"]:
            words = words[1:]
        if not words or words[0].startswith("-") or "=" in words[0]:
            return None
        name = Path(words[0]).name
    return name if name in {"sh", "bash", "zsh"} else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dialect", choices=("sh", "bash", "zsh"), required=True)
    parser.add_argument("--interpreter", type=Path, required=True)
    parser.add_argument("files", type=Path, nargs="+")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later", file=sys.stderr)
        return 2
    if not args.interpreter.is_absolute() or not args.interpreter.is_file() or not os.access(args.interpreter, os.X_OK):
        print("error: pass the absolute executable path of the declared target shell", file=sys.stderr)
        return 2
    runtime_names = {"bash": r"bash(?:[-.]?[0-9][0-9.]*)?", "zsh": r"zsh(?:[-.]?[0-9][0-9.]*)?", "sh": r"(?:sh|dash|ash)"}
    if not re.fullmatch(runtime_names[args.dialect], args.interpreter.name):
        print("error: select a native interpreter whose filename matches the declared dialect", file=sys.stderr)
        return 2
    try:
        inputs = [(path.resolve(strict=True), path.read_bytes()) for path in args.files]
    except (OSError, ValueError):
        print("error: pass readable regular script files, not directories or missing paths", file=sys.stderr)
        return 2
    findings, checked = [], []
    flags = {"bash": ["--noprofile", "--norc", "-n"], "sh": ["-n"], "zsh": ["-f", "-n"]}[args.dialect]
    for index, (path, content) in enumerate(inputs):
        if shebang_dialect(content) != args.dialect:
            findings.append({"file_index": index, "code": "shebang_dialect_mismatch"})
            continue
        try:
            result = subprocess.run([str(args.interpreter), *flags, str(path)],
                                    env={"PATH": os.defpath, "LC_ALL": "C"},
                                    stdin=subprocess.DEVNULL, capture_output=True, timeout=10)
        except subprocess.TimeoutExpired:
            findings.append({"file_index": index, "code": "parser_timeout"})
            continue
        except OSError:
            print("error: select a runnable native target shell and rerun", file=sys.stderr)
            return 2
        checked.append({"file_index": index, "exit_code": result.returncode})
        if result.returncode:
            findings.append({"file_index": index, "code": "syntax_failed"})
    print(json.dumps({"dialect": args.dialect, "files": checked, "findings": findings,
                      "scope": "native_syntax_only"}, sort_keys=True))
    if findings:
        print("error: correct the shebang/dialect or inspect the failing file with its native parser locally", file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
