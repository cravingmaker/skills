#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Check that catalog/skills.yaml, the skills/ folders, and their declared
dependencies agree.

Usage: check-catalog.py [--root DIR]
Exit status: 0 when consistent, 1 when any rule fails, 2 on usage errors.
"""

import sys
from pathlib import Path

import skillcatalog

KINDS = {"capability", "role"}
STATUSES = {"unevaluated", "evaluated"}


def check(repo: skillcatalog.Repo) -> list[str]:
    problems = []
    entries = repo.entries
    roles = set(repo.roles)
    external = repo.external
    on_disk = set(repo.frontmatter)

    for name in sorted(on_disk - set(entries)):
        problems.append(f"skills/{name} has no entry in catalog/skills.yaml")
    for name in sorted(set(entries) - on_disk):
        problems.append(f"catalog entry {name} has no skills/{name}/SKILL.md")

    for name in sorted(on_disk | set(entries)):
        if name in repo.reserved:
            problems.append(f"{name} is a reserved name (catalog/reserved-names.txt); choose another")
        if name in external:
            problems.append(f"{name} is listed as external ({external[name]}) and also exists in skills/")

    for name, entry in sorted(entries.items()):
        entry = entry or {}
        kind = entry.get("kind")
        if kind not in KINDS:
            problems.append(f"{name}: kind must be one of {sorted(KINDS)}")
        if entry.get("status") not in STATUSES:
            problems.append(f"{name}: status must be one of {sorted(STATUSES)}")
        if entry.get("status") == "evaluated" and not any((repo.root / "skills" / name / "evals" / "results").glob("*.md")):
            problems.append(f"{name}: status is evaluated, but skills/{name}/evals/results/ has no recorded runs")
        if kind == "role":
            if name not in roles:
                problems.append(f"{name}: kind role, but it is not in the catalog's roles list")
            if name in on_disk and not repo.names(name, "requires"):
                problems.append(f"{name}: a role router needs metadata.requires listing its capabilities")
        if kind == "capability":
            listed = entry.get("roles") or []
            if not listed:
                problems.append(f"{name}: list the roles that use this capability, or [all]")
            for role in listed:
                if role != "all" and role not in roles:
                    problems.append(f"{name}: unknown role {role}")

    for name in sorted(on_disk):
        for key in ("requires", "handoffs"):
            for target in repo.names(name, key):
                if target == name:
                    problems.append(f"{name}: metadata.{key} names the skill itself")
                elif target not in on_disk and target not in external:
                    problems.append(f"{name}: metadata.{key} names {target}, which is neither in skills/ nor an external skill in the catalog")
    return problems


def main(arguments: list[str]) -> int:
    root = Path(".")
    if arguments[:1] == ["--root"] and len(arguments) == 2:
        root = Path(arguments[1])
    elif arguments:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    problems = check(skillcatalog.load(root))
    for problem in problems:
        print(f"  - {problem}")
    if problems:
        print(f"Catalog check failed: {root}")
        return 1
    print(f"Catalog check passed: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
