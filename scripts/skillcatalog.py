"""Shared loading for the catalog scripts (check-catalog.py, build-profiles.py).

Reads catalog/skills.yaml, catalog/reserved-names.txt, and the frontmatter of
every skills/<name>/SKILL.md under a repository root.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Repo:
    root: Path
    catalog: dict
    reserved: set[str]
    frontmatter: dict[str, dict] = field(default_factory=dict)

    @property
    def roles(self) -> list[str]:
        return list(self.catalog.get("roles") or [])

    @property
    def entries(self) -> dict[str, dict]:
        return dict(self.catalog.get("skills") or {})

    @property
    def external(self) -> dict[str, str]:
        """Map each external skill name to its provider."""
        names = {}
        for provider, spec in (self.catalog.get("external") or {}).items():
            for name in (spec or {}).get("skills") or []:
                names[name] = provider
        return names

    def invocation(self, skill: str) -> str:
        return (self.entries.get(skill) or {}).get("invocation", "model")

    def names(self, skill: str, key: str) -> list[str]:
        metadata = self.frontmatter.get(skill, {}).get("metadata") or {}
        value = metadata.get(key, "") if isinstance(metadata, dict) else ""
        return value.split() if isinstance(value, str) else []


def read_frontmatter(skill_md: Path) -> dict:
    match = re.match(r"---\n(.*?)\n---\n", skill_md.read_text(encoding="utf-8"), re.DOTALL)
    data = yaml.safe_load(match.group(1)) if match else None
    return data if isinstance(data, dict) else {}


def load(root: Path) -> Repo:
    catalog = yaml.safe_load((root / "catalog" / "skills.yaml").read_text(encoding="utf-8")) or {}
    reserved_file = root / "catalog" / "reserved-names.txt"
    reserved = set()
    if reserved_file.is_file():
        for line in reserved_file.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                reserved.add(line)
    repo = Repo(root=root, catalog=catalog, reserved=reserved)
    for skill_md in sorted((root / "skills").glob("*/SKILL.md")):
        repo.frontmatter[skill_md.parent.name] = read_frontmatter(skill_md)
    return repo


def closure(repo: Repo, role: str) -> tuple[list[str], list[str]]:
    """Return (repository skills, external skills) a role needs, following `requires` transitively."""
    seen: set[str] = set()
    external: set[str] = set()
    missing: set[str] = set()
    pending = [role]
    while pending:
        name = pending.pop()
        if name in seen or name in external:
            continue
        if name in repo.frontmatter:
            seen.add(name)
            pending.extend(repo.names(name, "requires"))
        elif name in repo.external:
            external.add(name)
        else:
            missing.add(name)
    if missing:
        raise ValueError(f"{role}: missing required skills {', '.join(sorted(missing))}; restore them or fix metadata.requires before generating profiles")
    return sorted(seen), sorted(external)
