#!/usr/bin/env python3
"""Plan controlled zsh startup probes; run only with an explicit disposable root.

Python 3.12+ stdlib; --zsh selects the target's installed native runtime.
Usage: zsh-startup-probe.py --zsh /absolute/zsh [--run --disposable-root DIR]
DIR needs marker .zsh-probe-disposable containing 'zsh-startup-probe\n', a
candidate/ directory of reviewed regular startup files, and empty baseline/.
Stdout: JSON labels, times, byte counts, option flags and PATH hashes, no values.
Stderr: value-free diagnostics. Exit: 0 planned/completed, 1 shell/protocol
failure, 2 invalid input/setup. --help exits 0 without inspection or execution.
The directory is not a sandbox: candidates and global zshenv can have effects.
No inherited credential environment, command xtrace, terminal or network proof.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

NAMES = (".zshenv", ".zprofile", ".zshrc", ".zlogin", ".zlogout")
MODES = {"noninteractive": [], "login": ["-l"], "interactive": ["-i"], "login_interactive": ["-l", "-i"]}
MARKER = b"\0ZSH_PROBE\0"
COMMAND = r"""builtin printf '\000ZSH_PROBE\000%s\000%s,%s\000%s\000' "$PATH" "$options[shwordsplit]" "$options[nomatch]" "$PWD"; builtin exit 0"""


def validate(root, zsh):
    if root is None or not root.is_absolute() or root.is_symlink() or root.resolve() == Path.home():
        raise ValueError
    marker = root / ".zsh-probe-disposable"
    candidate, baseline = root / "candidate", root / "baseline"
    if marker.is_symlink() or marker.read_bytes() != b"zsh-startup-probe\n":
        raise ValueError
    if any(p.is_symlink() or not p.is_dir() for p in (candidate, baseline)) or list(baseline.iterdir()):
        raise ValueError
    if any(p.is_symlink() or not p.is_file() or p.name not in NAMES for p in candidate.iterdir()):
        raise ValueError
    if zsh is None or not zsh.is_absolute() or not zsh.is_file() or not os.access(zsh, os.X_OK):
        raise ValueError
    return root.resolve(), zsh.resolve()


def probe(zsh, directory, root, flags, timeout):
    env = {"PATH": os.defpath, "LC_ALL": "C", "TERM": "dumb", "ZDOTDIR": str(directory), "TMPDIR": str(root)}
    start = time.perf_counter()
    process = subprocess.Popen([str(zsh), "-d", "-o", "sourcetrace", *flags, "-c", COMMAND],
                               cwd=root, env=env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = process.communicate()
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    known = {os.fsencode(directory / name): name for name in NAMES}
    order, extra_stderr = [], len(stderr)
    # Startup output need not end with a newline before a source announcement.
    pattern = rb"\++(" + re.escape(os.fsencode(directory)) + rb"/\.z(?:shenv|profile|shrc|login|logout)):[0-9]+> <sourcetrace>(?:\r?\n)?"
    for match in re.finditer(pattern, stderr):
        order.append(known[match[1]])
        extra_stderr -= len(match[0])
    prefix, found, tail = stdout.partition(MARKER)
    parts = tail.split(b"\0", 3)
    valid = bool(found and len(parts) == 4 and os.path.isabs(parts[2]) and parts[1] in (b"on,on", b"on,off", b"off,on", b"off,off"))
    result = {"elapsed_ms": round((time.perf_counter() - start) * 1000, 3),
              "exit_code": process.returncode, "timeout": timed_out,
              "protocol_complete": valid, "startup_order": order,
              "extra_stdout_bytes": len(prefix) + (len(parts[3]) if valid else len(tail)),
              "extra_stderr_bytes": extra_stderr}
    if valid:
        entries = parts[0].split(b":")
        result.update(path_entry_sha256=[hashlib.sha256(x).hexdigest() for x in entries],
                      duplicate_path_entries=len(entries) - len(set(entries)),
                      empty_path_entries=entries.count(b""),
                      missing_path_entries=sum(bool(x) and not os.path.isdir(os.path.join(parts[2], x)) for x in entries))
        split, glob = parts[1].decode().split(",")
        result.update(path_sha256=hashlib.sha256(parts[0]).hexdigest(),
                      options={"shwordsplit": split, "nomatch": glob})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zsh", type=Path)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--disposable-root", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=5, choices=range(1, 31))
    args = parser.parse_args()
    if not args.run:
        print(json.dumps({"mode": "plan", "shells_executed": 0, "modes": list(MODES),
                          "run_requires": "explicit disposable root and reviewed startup files"}, sort_keys=True))
        return 0
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later", file=sys.stderr)
        return 2
    try:
        root, zsh = validate(args.disposable_root, args.zsh)
    except (OSError, ValueError, RuntimeError):
        print("error: pass an executable zsh and a disposable root with the documented marker, candidate files and empty baseline", file=sys.stderr)
        return 2
    rows = []
    try:
        for variant in ("baseline", "candidate"):
            for mode, flags in MODES.items():
                rows.append({"variant": variant, "mode": mode,
                             **probe(zsh, root / variant, root, flags, args.timeout_seconds)})
    except OSError:
        print("error: run in a supported disposable POSIX environment with a working zsh", file=sys.stderr)
        return 2
    failed = any(row["exit_code"] or row["timeout"] or not row["protocol_complete"] for row in rows)
    print(json.dumps({"mode": "executed", "scope": "controlled_non_pty_startup", "rows": rows}, sort_keys=True))
    if failed:
        print("error: fix the failing startup or inspect the missing probe protocol locally before comparing state", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
