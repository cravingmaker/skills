#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Install skills from this repository into an agent's skills folder, together
with every skill they require (the metadata.requires closure).

Usage: install-skills.py --target DIR [--mode copy|symlink] [--force] [--root DIR] NAME [NAME ...]
  NAME      A role router (for example backend-engineer) or any skill in skills/.
  --target  The host's skills folder, for example ~/.claude/skills or .agents/skills.
  --mode    copy (default) or symlink to this checkout.
  --force   Replace skills already present in the target.

Skills kept upstream (catalog external providers) are listed for you to install
from their source. Exit status: 0 installed, 1 a required skill is missing or a
target conflicts, 2 usage errors.
"""

import argparse
import shutil
import sys
from pathlib import Path

import skillcatalog


def parse(arguments: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--target", required=True)
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("names", nargs="+")
    try:
        return parser.parse_args(arguments)
    except SystemExit:
        print(__doc__.strip(), file=sys.stderr)
        raise SystemExit(2)


def resolve(repo: skillcatalog.Repo, names: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Return (skills to install, external skills, missing names)."""
    install: set[str] = set()
    external: set[str] = set()
    missing: set[str] = set()
    pending = list(names)
    while pending:
        name = pending.pop()
        if name in install or name in external or name in missing:
            continue
        if name in repo.frontmatter:
            install.add(name)
            pending.extend(repo.names(name, "requires"))
        elif name in repo.external:
            external.add(name)
        else:
            missing.add(name)
    return sorted(install), sorted(external), sorted(missing)


def main(arguments: list[str]) -> int:
    options = parse(arguments)
    root = Path(options.root).resolve()
    repo = skillcatalog.load(root)
    install, external, missing = resolve(repo, options.names)
    if missing:
        for name in missing:
            print(f"error: {name} is required but is neither in {root / 'skills'} nor an external skill in the catalog", file=sys.stderr)
        return 1

    target = Path(options.target).expanduser()
    conflicts = [name for name in install if (target / name).exists() or (target / name).is_symlink()]
    if conflicts and not options.force:
        for name in conflicts:
            print(f"error: {target / name} already exists; use --force to replace it", file=sys.stderr)
        return 1

    target.mkdir(parents=True, exist_ok=True)
    for name in install:
        source = root / "skills" / name
        destination = target / name
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        elif destination.is_dir():
            shutil.rmtree(destination)
        if options.mode == "symlink":
            destination.symlink_to(source, target_is_directory=True)
        else:
            shutil.copytree(source, destination, ignore=shutil.ignore_patterns("results"))
        print(f"installed {name} ({options.mode}) -> {destination}")

    for name in external:
        provider = repo.external[name]
        spec = (repo.catalog.get("external") or {}).get(provider) or {}
        print(f"prerequisite: install {name} from {provider} ({spec.get('source', 'see catalog')}): {spec.get('install', '')}".rstrip(": "))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
