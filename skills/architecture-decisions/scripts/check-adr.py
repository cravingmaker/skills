#!/usr/bin/env python3
"""Audit numbered Markdown ADRs without rewriting their format.

Usage: check-adr.py ADR_DIRECTORY [--base GIT_REF] [--require-confirmation]
                    [--signed-off NUMBER ...]
Python 3.12+ standard library; Git is needed only for --base. No writes/network.
Stdout: JSON with record status, confirmation presence, and findings.
Stderr: usage/input diagnostics. Exits: 0 pass, 1 findings, 2 invalid input.
Statusless short records remain 'recorded', not implicitly accepted, and their
historical text is protected by --base. Lifecycle fields may change; reasoning
may not. Confirmation presence does not prove its evidence. With --base, each
new acceptance needs --signed-off NUMBER, supplied only after user sign-off.
That acknowledgement is not independent proof of permission.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

NUMBER = re.compile(r"^(?:adr[-_ ]?)?(\d+)(?:[-_. ]|$)", re.I)
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
FIELD = re.compile(r"^(status|supersedes|superseded[- ]by|confirmation)\s*:\s*(.*)$", re.I)
STATUSES = {"proposed", "accepted", "rejected", "deprecated", "superseded"}
PLACEHOLDER = re.compile(r"^(?:tbd|todo|n/?a|none|null|~|-|\.{3}|<[^>]*>|\{[^}]*\})$", re.I)


def label(value):
    return value.strip().casefold().replace("-", " ")


def parse(text):
    status, relations, confirmation, body = [], {"supersedes": [], "superseded by": []}, [], []
    section, fence, front = "", None, text.startswith("---\n") or text.startswith("---\r\n")
    for index, line in enumerate(text.splitlines()):
        if front and line == "---":
            if index:
                front = False
            continue
        marker = re.match(r"^\s*(" + chr(96) + r"{3,}|~{3,})", line)
        if marker and not front:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            body.append(line)
            continue
        if fence:
            body.append(line)
            continue
        heading = HEADING.match(line) if not front else None
        if heading:
            section = label(heading.group(1))
            if section in ("status", "supersedes", "superseded by"):
                continue
        clean = re.sub(r"^\s*[-*]\s+", "", line.strip()).replace("**", "")
        field = FIELD.match(clean)
        key, value = (label(field.group(1)), field.group(2)) if field else (section, line)
        value = value.strip().strip("'\"")
        if key == "status":
            if value:
                status.append(value)
                match = re.search(r"superseded[- ]by\s*:?\s*(.+)", value, re.I)
                if match:
                    relations["superseded by"].append(match.group(1))
            continue
        if key in relations:
            if value:
                relations[key].append(value)
            continue
        if key == "confirmation" and not heading and value.casefold() not in {"null", "~"}:
            confirmation.append(value)
        body.append(line)
    if front:
        raise ValueError("close the scalar frontmatter block before auditing this ADR")
    issues, state = [], "recorded"
    if status:
        states = {re.split(r"\s+", value.casefold(), maxsplit=1)[0] for value in status}
        if len(states) != 1 or not states <= STATUSES:
            issues.append("use one recognized lifecycle status or adapt the native checker")
        else:
            state = states.pop()
    confirmation_text = re.sub(r"<!--.*?-->", "", "\n".join(confirmation), flags=re.S).strip()
    meaningful = any(value and not PLACEHOLDER.fullmatch(value)
                     for value in (line.strip().lstrip("-* ") for line in confirmation_text.splitlines()))
    return {"status": state, "relations": relations, "body": "\n".join(body).strip(),
            "confirmation": meaningful, "issues": issues}


def git(directory, *args):
    result = subprocess.run(["git", "--no-pager", "-C", str(directory), *args],
                            capture_output=True, check=False)
    if result.returncode:
        raise ValueError("Git input failed; choose a readable repository and a valid commit ref")
    return result.stdout


def targets(values, source, root, by_number, findings):
    result = set()
    for value in values:
        links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", value)
        if links:
            for link in links:
                parsed = urlsplit(link.strip("<>"))
                if parsed.scheme or parsed.netloc or not parsed.path or parsed.query:
                    findings.append(f"{source.name}: use local ADR links for supersession")
                    continue
                target = (source.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(root):
                    findings.append(f"{source.name}: supersession must stay inside the ADR directory")
                else:
                    result.add(target)
        else:
            numbers = re.findall(r"\bADR[-_ ]?(\d+)\b", value, re.I)
            if not numbers and re.fullmatch(r"\d+", value):
                numbers = [value]
            if not numbers:
                findings.append(f"{source.name}: use a Markdown link or ADR-NNNN supersession reference")
            for number in numbers:
                matches = by_number.get(int(number), [])
                if len(matches) != 1:
                    findings.append(f"{source.name}: ADR-{number} must resolve to one numbered record")
                else:
                    result.add(matches[0])
    return result


def audit(root, base=None, require_confirmation=False, signed_off=()):
    paths = []
    for path in root.rglob("*"):
        if path.suffix.casefold() == ".md" and NUMBER.match(path.stem):
            if path.is_symlink():
                raise ValueError("use regular ADR files, not symlinks")
            if path.is_file():
                paths.append(path.resolve())
    paths.sort()
    findings, by_number = [], {}
    records = {path: parse(path.read_text(encoding="utf-8")) for path in paths}
    for path in paths:
        number = int(NUMBER.match(path.stem).group(1))
        by_number.setdefault(number, []).append(path)
    for number, matches in by_number.items():
        if len(matches) > 1:
            findings.append(f"ADR-{number}: use a unique number within this ADR directory")
    if not paths:
        findings.append("empty ADR scan; point to the directory containing numbered records")
    for path, record in records.items():
        findings.extend(f"{path.relative_to(root)}: {issue}" for issue in record["issues"])
        if require_confirmation and not record["confirmation"]:
            findings.append(f"{path.relative_to(root)}: add or link confirmation evidence in the established format")
        record["links"] = {key: targets(values, path, root, by_number, findings)
                           for key, values in record["relations"].items()}
    for path, record in records.items():
        links = record["links"]
        if record["status"] == "superseded" and not links["superseded by"]:
            findings.append(f"{path.name}: a superseded record needs its successor link")
        if links["superseded by"] and record["status"] != "superseded":
            findings.append(f"{path.name}: mark the replaced record superseded")
        for direction, reverse in (("supersedes", "superseded by"), ("superseded by", "supersedes")):
            for target in links[direction]:
                if target == path:
                    findings.append(f"{path.name}: a record cannot supersede itself")
                elif target not in records:
                    findings.append(f"{path.name}: restore the missing supersession target {target.name}")
                elif (path not in records[target]["links"][reverse]
                      and not (direction == "supersedes" and record["status"] in {"proposed", "rejected"})):
                    findings.append(f"{path.name}: add the reciprocal {reverse} link in {target.name}")
                if direction == "superseded by" and target in records and records[target]["status"] in {"proposed", "rejected"}:
                    findings.append(f"{path.name}: a proposed or rejected successor cannot replace a recorded decision")
    def cycle(path, trail):
        if path in trail:
            return True
        return any(cycle(target, trail | {path})
                   for target in records[path]["links"]["superseded by"] if target in records)
    if any(cycle(path, set()) for path in records):
        findings.append("supersession cycle; retain an acyclic history ending at the current decision")
    base_sha = None
    if base:
        repository = Path(os.fsdecode(git(root, "rev-parse", "--show-toplevel")).strip()).resolve()
        relative = root.relative_to(repository).as_posix()
        base_sha = git(repository, "rev-parse", "--verify", "--end-of-options", base + "^{commit}").decode().strip()
        previous_states = {}
        for name in filter(None, git(repository, "ls-tree", "-rz", "--name-only", base_sha, "--", relative).split(b"\0")):
            old_path = Path(os.fsdecode(name))
            if old_path.suffix.casefold() != ".md" or not NUMBER.match(old_path.stem):
                continue
            previous = parse(git(repository, "show", base_sha + ":" + old_path.as_posix()).decode("utf-8"))
            previous_states[(repository / old_path).resolve()] = previous["status"]
            if previous["status"] in {"accepted", "superseded", "deprecated", "recorded"}:
                current = records.get((repository / old_path).resolve())
                if current is None or current["body"] != previous["body"]:
                    findings.append(f"{old_path}: recorded reasoning changed or was removed; supersede with a new ADR")
                if current and previous["status"] == "accepted" and current["status"] in {"proposed", "rejected", "recorded"}:
                    findings.append(f"{old_path}: preserve accepted history instead of reverting it to an unaccepted status")
        for path, record in records.items():
            number = int(NUMBER.match(path.stem).group(1))
            if (record["status"] == "accepted" and previous_states.get(path) != "accepted"
                    and number not in signed_off):
                findings.append(f"{path.relative_to(root)}: new acceptance needs user sign-off; keep proposed or acknowledge with --signed-off {number}")
    return {"base": base_sha, "scanned": len(records),
            "records": [{"path": path.relative_to(root).as_posix(), "status": record["status"],
                         "confirmation": record["confirmation"]} for path, record in records.items()],
            "findings": sorted(set(findings))}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--base")
    parser.add_argument("--require-confirmation", action="store_true")
    parser.add_argument("--signed-off", type=int, action="append", default=[])
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error("use Python 3.12 or later")
    if args.signed_off and (not args.base or any(number < 0 for number in args.signed_off)):
        parser.error("use --signed-off with --base and non-negative ADR numbers only after user sign-off")
    try:
        root = args.directory.resolve(strict=True)
        if not root.is_dir():
            raise ValueError("point to an existing ADR directory")
        result = audit(root, args.base, args.require_confirmation, set(args.signed_off))
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        print(f"error: {error}; check the input format and paths", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
