"""Check explicit skill pointers in bodies and their directly linked resources."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
POINTER = re.compile(r"\bthe\s+(?:(?P<provider>[a-z0-9-]+)\s+)?`(?P<name>[^`\n]+)`\s+skill\b", re.I)
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")


REFERENCE_DEFINITION = re.compile(r"^ {0,3}\[([^\]\n]+)\]:[ \t]*(?:<([^>\n]+)>|(\S+))[^\n]*$", re.M)
REFERENCE_LINK = re.compile(r"\[([^\]\n]+)\](?:\[([^\]\n]*)\])?(?!\()")


def link_targets(body: str) -> list[str]:
    """Resolve inline and used full, collapsed or shortcut reference links."""
    def label(value):
        return " ".join(value.split()).casefold()
    definitions = {}
    for match in REFERENCE_DEFINITION.finditer(body):
        definitions.setdefault(label(match[1]), match[2] or match[3])
    text = REFERENCE_DEFINITION.sub("", body)
    targets = [match[1] for match in LINK.finditer(text)]
    for match in REFERENCE_LINK.finditer(text):
        target = definitions.get(label(match[2] or match[1]))
        if target is not None:
            targets.append(target)
    return targets


def prose(text: str) -> str:
    """Blank fenced code and explicitly marked historical crosswalks, keeping lines."""
    result, fence, historical = [], None, False
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = re.match(r"(`{3,}|~{3,})", stripped)
        if fence:
            if re.fullmatch(re.escape(fence[0]) + "{" + str(fence[1]) + r",}\s*", stripped):
                fence = None
            result.append("")
            continue
        if marker:
            fence = (marker[1][0], len(marker[1]))
            result.append("")
            continue
        if stripped == "<!-- skill-names: historical -->":
            historical = True
        if historical:
            if stripped == "<!-- skill-names: end -->":
                historical = False
            result.append("")
        else:
            result.append(line)
    return "\n".join(result)


def linked_resources(skill_dir: Path) -> tuple[list[Path], list[str]]:
    """Only one level from SKILL.md; links must stay inside owned resources."""
    body = prose((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    paths, problems = set(), []
    for target in link_targets(body):
        value = unquote(urlsplit(target.strip("<>")).path)
        relative = Path(value)
        if relative.parts[:1] not in (("references",), ("assets",)):
            continue
        path = skill_dir / relative
        if not path.resolve().is_relative_to(skill_dir.resolve()) or path.is_symlink():
            problems.append(f"{skill_dir.name}: resource {value} must stay inside the owned skill")
        elif not path.is_file():
            problems.append(f"{skill_dir.name}: linked resource {value} is missing; restore it or fix the link")
        else:
            paths.add(path)
    return sorted(paths), problems


def check(repo) -> list[str]:
    problems = []
    for name in repo.frontmatter:
        directory = repo.root / "skills" / name
        resources, errors = linked_resources(directory)
        problems.extend(errors)
        for path in [directory / "SKILL.md", *resources]:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue  # Binary assets do not contain prose pointers.
            # Frontmatter is data, not a runtime route.
            if path.name == "SKILL.md":
                text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)
            for number, line in enumerate(prose(text).splitlines(), 1):
                for match in POINTER.finditer(line):
                    target, provider = match["name"], match["provider"]
                    if any(token in target for token in ("<", ">", "{{", "}}")):
                        continue  # Explicit template placeholders, never concrete names.
                    location = f"{path.relative_to(repo.root)}:{number}"
                    if not NAME.fullmatch(target) or len(target) > 64:
                        problems.append(f"{location}: noncanonical skill name {target!r}; use its exact catalog name")
                    elif target not in repo.frontmatter and target not in repo.external:
                        problems.append(f"{location}: unknown prose skill {target}; ship it or declare a supported external inventory")
                    elif provider and repo.external.get(target) != provider:
                        problems.append(f"{location}: provider {provider} does not supply {target} in the external inventory")
    return problems
