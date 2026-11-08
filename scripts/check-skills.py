#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Check the repository rules that skills-ref does not enforce.

skills-ref converts metadata values to strings before it validates them, so
this checker reads the original frontmatter. It checks declared provenance,
not whether the attribution is complete; source review establishes that.

Usage: check-skills.py SKILL_DIR [SKILL_DIR ...]
Exit status: 0 when every directory passes, 1 when any rule fails.
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml

MAX_LINES = 500
EVAL_SECTIONS = ("Activation", "Near miss", "Outcome")
REVISION = re.compile(r"[0-9a-f]{40}")


def read_frontmatter(skill_md: Path) -> tuple[dict | None, list[str]]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        return None, ["SKILL.md has no YAML frontmatter block"]
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        return None, [f"frontmatter is not valid YAML: {error}"]
    if not isinstance(data, dict):
        return None, ["frontmatter is not a mapping"]
    return data, []


def check_metadata(frontmatter: dict) -> list[str]:
    if "metadata" not in frontmatter:
        return []
    metadata = frontmatter["metadata"]
    if not isinstance(metadata, dict):
        return ["metadata must be a mapping of strings to strings"]
    key_problems = [
        f"metadata key {key!r} must be a string; quote it"
        for key in metadata
        if not isinstance(key, str)
    ]
    return key_problems + [
        f"metadata.{key} must be a string, got {type(value).__name__}"
        + ("; quote it" if not isinstance(value, (dict, list)) else "")
        for key, value in metadata.items()
        if not isinstance(value, str)
    ]


def is_source_url(value: object) -> bool:
    if not isinstance(value, str) or any(character.isspace() for character in value):
        return False
    try:
        parsed = urlsplit(value)
        return bool(parsed.scheme and parsed.netloc and parsed.hostname)
    except ValueError:
        return False


def check_provenance(skill_dir: Path, frontmatter: dict) -> list[str]:
    metadata = frontmatter.get("metadata")
    metadata = metadata if isinstance(metadata, dict) else {}
    source = metadata.get("source")
    license_files = sorted(path.name for path in skill_dir.glob("LICENSE-*") if path.is_file())
    license_value = frontmatter.get("license")
    has_license = isinstance(license_value, str) and bool(license_value.strip())
    problems = []
    if "license" in frontmatter and not has_license:
        problems.append("license must be a non-empty string")
    if has_license and license_value != "MIT" and not license_files:
        problems.append("a non-MIT license needs a LICENSE-<upstream> file in the skill folder")
    if "source" in metadata:
        if not is_source_url(source):
            problems.append("metadata.source must be an absolute upstream URL, such as https://github.com/owner/repo")
        revision = metadata.get("source-revision")
        if not isinstance(revision, str) or REVISION.fullmatch(revision) is None:
            problems.append("metadata.source needs metadata.source-revision set to a full 40-character commit SHA")
        if not license_files:
            problems.append("metadata.source is set, so the skill folder needs the upstream license notice (a LICENSE-<upstream> file)")
        if not has_license:
            problems.append("adapted skills need a non-empty license field in the frontmatter")
    elif license_files:
        problems.append(f"{', '.join(license_files)} present without metadata.source; declare where the material comes from")
    return problems


def check_evals(skill_dir: Path) -> list[str]:
    examples = skill_dir / "evals" / "examples.md"
    if not examples.is_file():
        return ["evals/examples.md is missing"]
    sections: dict[str, list[str]] = {}
    current = None
    for line in examples.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current is not None and line.startswith("- "):
            sections[current].append(line)
    return [
        f"evals/examples.md needs a '## {name}' section with at least one '- ' item"
        for name in EVAL_SECTIONS
        if not sections.get(name)
    ]


def check_length(skill_md: Path) -> list[str]:
    count = len(skill_md.read_text(encoding="utf-8").splitlines())
    return [f"SKILL.md has {count} lines; keep it under {MAX_LINES}"] if count >= MAX_LINES else []


def check_skill(skill_dir: Path) -> list[str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md is missing"]
    frontmatter, problems = read_frontmatter(skill_md)
    if frontmatter is None:
        return problems
    return [
        *check_metadata(frontmatter),
        *check_provenance(skill_dir, frontmatter),
        *check_evals(skill_dir),
        *check_length(skill_md),
    ]


def main(arguments: list[str]) -> int:
    if not arguments:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    failed = False
    for argument in arguments:
        skill_dir = Path(argument)
        problems = check_skill(skill_dir)
        if problems:
            failed = True
            print(f"Repository rules failed for {skill_dir}:")
            for problem in problems:
                print(f"  - {problem}")
        else:
            print(f"Repository rules passed: {skill_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
