#!/usr/bin/env python3
"""Build and smoke an emitted Node entry in an explicit disposable directory.

Python 3.12+ standard library; POSIX process groups; no prompts or network calls
of its own. Build/service code runs only with --disposable-dir.
Usage: smoke-built-entry.py --disposable-dir DIR --node /path/to/node
  --expected-version VERSION --build-command '["package-manager","build"]'
  --entry dist/server.js --mode import|start|reject [--ready-file ready]
  reject requires --expect-key KEY; --forbid CANARY tests synthetic secret output.
Build argv is JSON, not shell text. The directory must already exist and must
not be a git checkout. Entry/readiness paths must stay inside it.
start mode waits for a new readiness file, sends SIGTERM, and requires exit 0.
stdout: JSON stage results, never child output. stderr: safe diagnostics.
Exit: 0 pass, 1 build/runtime finding, 2 bad usage/setup.
Child output is suppressed to avoid leaking configuration; use the project's
own secure test diagnostics to investigate failures. All timeouts are seconds.
The explicit disposable flag authorizes the build's writes, not external data
changes. Supply synthetic configuration and owned disposable dependencies.
"""

import argparse
import json
import math
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path


class Finding(Exception):
    pass


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("use a positive finite timeout")
    return number


def inside(root, value):
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("use a relative path inside the disposable directory")
    path = (root / path).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ValueError("path escapes disposable directory")
    return path


def kill_group(process, sig):
    try:
        os.killpg(process.pid, sig)
    except ProcessLookupError:
        pass


def finish(process):
    kill_group(process, signal.SIGKILL)
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        raise Finding("child_cleanup_timeout")


def spawn(command, root, env):
    return subprocess.Popen(command, cwd=root, env=env, stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True)


def bounded(command, root, timeout, env):
    process = spawn(command, root, env)
    try:
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            raise Finding("timeout")
        if code != 0:
            raise Finding("nonzero_exit")
    finally:
        # Also clear children that outlived a successful parent.
        finish(process)


def start_and_drain(command, root, ready_name, startup_timeout, drain_timeout, env):
    ready = inside(root, ready_name)
    if ready.exists() or ready.is_symlink():
        raise ValueError("readiness file must be absent before launch")
    process = spawn(command, root, env)
    try:
        end = time.monotonic() + startup_timeout
        while True:
            if process.poll() is not None:
                raise Finding("exit_before_readiness")
            current = inside(root, ready_name)
            if current.is_file():
                break
            if time.monotonic() >= end:
                raise Finding("readiness_timeout")
            time.sleep(min(0.02, max(0, end - time.monotonic())))
        kill_group(process, signal.SIGTERM)
        try:
            code = process.wait(timeout=drain_timeout)
        except subprocess.TimeoutExpired:
            raise Finding("drain_timeout")
        if code != 0:
            raise Finding("unclean_shutdown")
    finally:
        finish(process)


def reject_startup(command, root, timeout, expected_key, forbidden, max_bytes, env):
    # Keep raw diagnostics in an unlinked temporary file, never in tool output.
    with tempfile.TemporaryFile(dir=root) as output:
        process = subprocess.Popen(command, cwd=root, env=env, stdin=subprocess.DEVNULL,
                                   stdout=output, stderr=output, start_new_session=True)
        try:
            end = time.monotonic() + timeout
            while process.poll() is None:
                if os.fstat(output.fileno()).st_size > max_bytes:
                    raise Finding("diagnostic_size_limit")
                if time.monotonic() >= end:
                    raise Finding("invalid_config_did_not_exit")
                time.sleep(0.02)
            if os.fstat(output.fileno()).st_size > max_bytes:
                raise Finding("diagnostic_size_limit")
            output.seek(0)
            diagnostics = output.read(max_bytes).decode("utf-8", errors="replace")
            if process.returncode <= 0:
                raise Finding("invalid_config_not_rejected_cleanly")
            if expected_key not in diagnostics:
                raise Finding("config_key_missing_from_diagnostic")
            if any(value in diagnostics for value in forbidden):
                raise Finding("config_canary_disclosed")
        finally:
            finish(process)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--disposable-dir", required=True, type=Path)
    parser.add_argument("--node", required=True, type=Path)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--build-command", required=True, help="JSON argv; no shell expansion")
    parser.add_argument("--entry", required=True)
    parser.add_argument("--mode", required=True, choices=("import", "start", "reject"))
    parser.add_argument("--ready-file")
    parser.add_argument("--expect-key", help="reject mode: configuration key the application must name")
    parser.add_argument("--forbid", action="append", default=[], help="reject mode: synthetic output canary, never a real credential")
    parser.add_argument("--max-output-bytes", type=int, default=65536)
    parser.add_argument("--build-timeout", type=positive, default=60)
    parser.add_argument("--version-timeout", type=positive, default=10)
    parser.add_argument("--startup-timeout", type=positive, default=10)
    parser.add_argument("--drain-timeout", type=positive, default=10)
    args = parser.parse_args()
    stage = "setup"
    try:
        if sys.version_info < (3, 12) or os.name != "posix":
            raise ValueError("use Python 3.12+ on a POSIX host")
        root = args.disposable_dir.resolve(strict=True)
        if not root.is_dir() or any((parent / ".git").exists() for parent in (root, *root.parents)):
            raise ValueError("use a disposable copy without .git")
        node = args.node.resolve(strict=True)
        if not args.node.is_absolute() or not node.is_file() or not os.access(node, os.X_OK):
            raise ValueError("supply an absolute executable Node path")
        command = json.loads(args.build_command)
        if not isinstance(command, list) or not command or any(not isinstance(x, str) or not x or "\0" in x for x in command):
            raise ValueError("build-command must be a nonempty JSON argv")
        entry = inside(root, args.entry)
        if entry.suffix not in {".js", ".mjs", ".cjs"}:
            raise ValueError("supply an emitted JavaScript entry")
        if args.mode == "start" and not args.ready_file:
            raise ValueError("start mode needs --ready-file")
        if args.mode != "start" and args.ready_file:
            raise ValueError("ready-file applies only to start mode")
        if args.mode == "reject":
            if not args.expect_key or not args.expect_key.isascii() or not args.expect_key.isidentifier():
                raise ValueError("reject mode needs an ASCII configuration key")
        elif args.expect_key or args.forbid:
            raise ValueError("expect-key and forbid apply only to reject mode")
        if args.max_output_bytes < 1 or any(not value for value in args.forbid):
            raise ValueError("use a positive output bound and nonempty synthetic canaries")
        if args.ready_file:
            ready = inside(root, args.ready_file)
            if ready.exists() or ready.is_symlink():
                raise ValueError("readiness file must start absent")
        # Version output is not forwarded; mismatch cannot echo arbitrary data.
        version = subprocess.run([str(node), "--version"], cwd=root, capture_output=True,
                                 text=True, timeout=args.version_timeout, check=False)
        if version.returncode or version.stdout.strip() != args.expected_version:
            raise ValueError("Node version differs from deployment record")
        env = os.environ.copy()
        stage = "build"
        bounded(command, root, args.build_timeout, env)
        entry = inside(root, args.entry)
        if not entry.is_file():
            raise Finding("emitted_entry_missing")
        stage = args.mode
        if args.mode == "import":
            env["NODE_SMOKE_ENTRY_URL"] = entry.as_uri()
            bounded([str(node), "--input-type=module", "--eval",
                     "await import(process.env.NODE_SMOKE_ENTRY_URL)"],
                    root, args.startup_timeout, env)
        elif args.mode == "start":
            start_and_drain([str(node), str(entry)], root, args.ready_file,
                            args.startup_timeout, args.drain_timeout, env)
        else:
            reject_startup([str(node), str(entry)], root, args.startup_timeout,
                           args.expect_key, args.forbid, args.max_output_bytes, env)
    except (ValueError, OSError, subprocess.TimeoutExpired, UnicodeError):
        print("error: fix the disposable target, Node version, argv or paths; see --help", file=sys.stderr)
        return 2
    except Finding as error:
        print(json.dumps({"stage": stage, "finding": str(error)}, sort_keys=True))
        return 1
    print(json.dumps({"build": "passed", "mode": args.mode, "runtime": "passed"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
