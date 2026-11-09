#!/usr/bin/env python3
"""Rank Git churn multiplied by file bytes; this is an inspection aid.

Usage: churn-hotspots.py --repo DIR --since WINDOW [--rev REF] [--limit N]
                         [--exclude GLOB ...]
Python 3.12+ stdlib and Git. Read-only, no network, no checkout or file writes.
Uses reachable non-merge commits, rename detection disabled, and the selected
revision's regular files. Churn is added + deleted lines; size is blob bytes.
Binary diffs and deleted files are excluded. Names with tabs/newlines are safe.
Lockfiles, minified bundles, maps and snapshots are excluded; --exclude adds
basename or repository-relative glob patterns for project-generated outputs.
Stdout: JSON with revision, window, counts, and ranked files; no source bodies.
Stderr: diagnostics. Exits: 0 results, 1 empty scan, 2 usage or invalid input.
"""

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from pathlib import Path

EXCLUDES = ("*.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb",
            "Cargo.lock", "go.sum", "poetry.lock", "uv.lock", "*.min.js", "*.min.css", "*.snap", "*.map")


def git(root, *args):
    result = subprocess.run(["git", "--no-pager", "-C", str(root), *args],
                            capture_output=True, check=False)
    if result.returncode:
        raise ValueError("Git input failed; choose a repository, valid revision, and history window")
    return result.stdout


def rank(root, since, revision, limit, exclusions=EXCLUDES):
    sha = git(root, "rev-parse", "--verify", "--end-of-options", revision + "^{commit}").decode().strip()
    sizes = {}
    for item in git(root, "ls-tree", "-rlz", sha).split(b"\0"):
        if not item:
            continue
        fields, name = item.split(b"\t", 1)
        mode, kind, _, size = fields.split()
        if kind == b"blob" and mode in (b"100644", b"100755"):
            sizes[name] = int(size)
    counts, binaries = {}, set()
    log = git(root, "log", "--no-merges", "--no-renames", "--numstat", "-z",
              "--format=", "--since=" + since, sha, "--")
    for item in filter(None, log.split(b"\0")):
        added, deleted, name = item.lstrip(b"\n").split(b"\t", 2)
        if added == b"-" or deleted == b"-":
            binaries.add(name)
            continue
        pair = counts.setdefault(name, [0, 0])
        pair[0] += int(added)
        pair[1] += int(deleted)
    rows = [
        {"path": os.fsdecode(name), "added": counts[name][0], "deleted": counts[name][1],
         "churn_lines": sum(counts[name]), "size_bytes": size,
         "score": sum(counts[name]) * size}
        for name, size in sizes.items() if name in counts and name not in binaries
        and not any(fnmatch.fnmatchcase(os.fsdecode(name), pattern)
                    or fnmatch.fnmatchcase(os.fsdecode(name).rsplit("/", 1)[-1], pattern) for pattern in exclusions)
    ]
    rows.sort(key=lambda row: (-row["score"], row["path"]))
    return {"revision": sha, "since": since, "history": "non-merge; no rename following",
            "tracked_regular_files": len(sizes), "ranked_files": len(rows),
            "binary_paths_excluded": len(binaries), "exclusions": list(exclusions), "files": rows[:limit],
            "findings": [] if rows else ["empty churn scan; widen the history window or supply repository history"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--since", required=True)
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--exclude", action="append", default=[])
    args = parser.parse_args()
    if sys.version_info < (3, 12) or args.limit < 1 or not args.since.strip():
        parser.error("use Python 3.12+, a non-empty window, and a positive --limit")
    try:
        result = rank(args.repo, args.since, args.rev, args.limit, EXCLUDES + tuple(args.exclude))
    except (OSError, ValueError) as error:
        print(f"error: {error}; correct the input and rerun", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
