#!/usr/bin/env python3
"""Check that Cargo lint tables set the required lints for every crate.

Usage: check-workspace-lints.py [--root DIR] [--metadata FILE] [--require TOOL::LINT ...]

Reads DIR/Cargo.toml (default: the current directory). In a workspace, every member must
inherit `[workspace.lints]` with `[lints] workspace = true` or set its own `[lints]`;
Cargo silently ignores workspace lints for members that do not opt in. Each required
lint must be set to warn, deny, or forbid. Lints set only through RUSTFLAGS or CI flags
are outside this check.

For a workspace, --metadata is required: capture cargo metadata --no-deps --locked
--offline --format-version 1 on that root. Cargo supplies exact membership,
including automatic path-dependency members; this script does not guess globs.
Default required lints: clippy::unwrap_used clippy::expect_used
clippy::await_holding_lock. --require replaces the whole set.

Requires Python 3.12 or later, standard library only (tomllib). Reads files; no writes.
Output: "FAIL <crate>: <problem>" lines on stdout, or "OK <n> crates".
Exit: 0 pass, 1 findings, 2 usage or unreadable input.
"""

import argparse
import json
import sys
import tomllib
from pathlib import Path

DEFAULT = ("clippy::unwrap_used", "clippy::expect_used", "clippy::await_holding_lock")
ACTIVE = {"warn", "deny", "forbid"}


def read(path):
    with open(path, "rb") as handle:
        return tomllib.load(handle)


def level(table, tool, lint):
    group = table.get(tool, {})
    if not isinstance(group, dict):
        raise ValueError("lint group must be a table")
    value = group.get(lint)
    if isinstance(value, dict):
        value = value.get("level")
    return value


def members(root, metadata_path):
    if not metadata_path:
        raise ValueError("workspace requires --metadata from cargo metadata --no-deps --locked --offline --format-version 1")
    data = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
    if data.get("version") != 1 or Path(data["workspace_root"]).resolve() != root:
        raise ValueError("metadata must use format version 1 and match --root")
    packages = {package["id"]: package["manifest_path"] for package in data["packages"]}
    names = data["workspace_members"]
    if not isinstance(names, list) or not names or len(names) != len(set(names)):
        raise ValueError("metadata needs a nonempty unique workspace_members list")
    return [Path(packages[name]).resolve().parent for name in names]


def main(argv):
    parser = argparse.ArgumentParser(
        prog="check-workspace-lints.py",
        description=__doc__.split("\n\n", 2)[2],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--metadata", help="Cargo format-version 1 metadata for this workspace")
    parser.add_argument("--require", action="append", metavar="TOOL::LINT")
    args = parser.parse_args(argv[1:])
    required = args.require or list(DEFAULT)
    for item in required:
        if item.count("::") != 1 or not all(item.split("::")):
            print(f"usage error: --require {item!r} must look like clippy::unwrap_used", file=sys.stderr)
            return 2
    root = Path(args.root).resolve()
    try:
        manifest = read(root / "Cargo.toml")
    except (OSError, tomllib.TOMLDecodeError) as error:
        print(f"cannot read {root / 'Cargo.toml'}: {error}; pass --root at the crate or workspace root", file=sys.stderr)
        return 2

    workspace_lints = manifest.get("workspace", {}).get("lints", {})
    try:
        crates = members(root, args.metadata) if "workspace" in manifest else [root]
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError):
        print("cannot establish workspace members; pass --metadata from cargo metadata --no-deps --locked --offline --format-version 1 for --root", file=sys.stderr)
        return 2
    problems = []
    for directory in crates:
        try:
            crate = manifest if directory == root else read(directory / "Cargo.toml")
        except (OSError, UnicodeError, tomllib.TOMLDecodeError):
            print("cannot read a workspace member; provide readable valid Cargo manifests", file=sys.stderr)
            return 2
        name = crate.get("package", {}).get("name", str(directory))
        lints = crate.get("lints")
        if isinstance(lints, dict) and lints.get("workspace") is True:
            effective, source = workspace_lints, "[workspace.lints]"
        elif isinstance(lints, dict) and lints:
            effective, source = lints, "[lints]"
        else:
            hint = "add [lints] workspace = true" if "workspace" in manifest else "add a [lints] table"
            problems.append(f"FAIL {name}: no lint table applies; {hint}")
            continue
        for item in required:
            tool, lint = item.split("::")
            try:
                value = level(effective, tool, lint)
            except (AttributeError, ValueError):
                print("invalid lint table; use Cargo's documented lint configuration", file=sys.stderr)
                return 2
            if not isinstance(value, str) or value not in ACTIVE:
                state = "missing" if value is None else f"set to {value!r}"
                problems.append(f"FAIL {name}: {item} is {state} in {source}; set it to deny (or warn with warnings denied in CI)")
    for line in problems:
        print(line)
    if problems:
        return 1
    print(f"OK {len(crates)} crates")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
