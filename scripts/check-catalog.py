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

import re
import sys
from pathlib import Path

import skillcatalog
import skillprose
import hostconfig

KINDS = {"capability", "role"}
STATUSES = {"unevaluated", "evaluated"}


def missing_evaluations(directory: Path, records: list[Path]) -> list[str]:
    """Require a valid, completed pair for each activation and near-miss prompt.

    This checks the public record structure, not whether a result passed its
    behavioral expectation; that remains a review decision.
    """
    expected, counts, section = set(), {}, ""
    for line in (directory / "examples.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip().lower().replace(" ", "-")
        elif line.startswith("- ") and section in ("activation", "near-miss"):
            counts[section] = counts.get(section, 0) + 1
            expected.add(f"{section}-{counts[section]}")
    completed = set()
    for path in records:
        text = path.read_text(encoding="utf-8")
        if not re.search(r"^Comparison: \*\*valid\*\*\.", text, re.MULTILINE):
            continue
        source = re.search(r"^- \*\*Source example\.\*\* `([^`]+)`", text, re.MULTILINE)
        arms = set()
        for line in text.splitlines():
            fields = [field.strip() for field in line.split("|")[1:-1]]
            if (len(fields) == 5 and fields[0] in ("treatment", "baseline")
                    and fields[2] in ("true", "false") and fields[3].isdigit() and fields[4] == "0"):
                arms.add(fields[0])
        if source and arms == {"treatment", "baseline"}:
            completed.add(source[1])
    return sorted(expected - completed) if expected else ["no activation or near-miss examples"]


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
        if repo.invocation(name) not in ("model", "user"):
            problems.append(f"{name}: invocation must be model or user")
        if not skillprose.NAME.fullmatch(name) or len(name) > 64:
            problems.append(f"{name}: use a canonical lowercase skill name")
        if name in on_disk and repo.frontmatter[name].get("name") != name:
            problems.append(f"{name}: frontmatter name must equal its catalog and directory name")
        kind = entry.get("kind")
        if kind not in KINDS:
            problems.append(f"{name}: kind must be one of {sorted(KINDS)}")
        if entry.get("status") not in STATUSES:
            problems.append(f"{name}: status must be one of {sorted(STATUSES)}")
        if entry.get("status") == "evaluated":
            directory = repo.root / "skills" / name / "evals"
            records = list((directory / "results").glob("*.md"))
            if not records:
                problems.append(f"{name}: status is evaluated, but skills/{name}/evals/results/ has no recorded runs")
            elif not (directory / "examples.md").is_file():
                problems.append(f"{name}: evaluated skill has no evals/examples.md")
            elif missing := missing_evaluations(directory, records):
                problems.append(f"{name}: status is evaluated, but missing valid completed paired runs for {', '.join(missing)}; record them or mark unevaluated")
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
        for key in ("requires",):
            for target in repo.names(name, key):
                if target == name:
                    problems.append(f"{name}: metadata.{key} names the skill itself")
                elif target not in on_disk and target not in external:
                    problems.append(f"{name}: metadata.{key} names {target}, which is neither in skills/ nor an external skill in the catalog")
    providers = {}
    for provider, spec in (repo.catalog.get("external") or {}).items():
        for target in (spec or {}).get("skills") or []:
            if not isinstance(target, str) or not skillprose.NAME.fullmatch(target) or len(target) > 64:
                problems.append(f"{provider}: external skill names must be canonical")
            if target in providers:
                problems.append(f"{target}: duplicate external inventory entries ({providers[target]}, {provider})")
            providers[target] = provider
    problems.extend(skillprose.check(repo))
    problems.extend(hostconfig.check(repo))
    return problems


def main(arguments: list[str]) -> int:
    if arguments in (["--help"], ["-h"]):
        print(__doc__.strip())
        return 0
    root = Path(".")
    if arguments[:1] == ["--root"] and len(arguments) == 2:
        root = Path(arguments[1])
    elif arguments:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    problems = check(skillcatalog.load(root))
    for problem in problems:
        print(f"  - {problem}", file=sys.stderr)
    if problems:
        print(f"Catalog check failed: {root}", file=sys.stderr)
        return 1
    print(f"Catalog check passed: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
