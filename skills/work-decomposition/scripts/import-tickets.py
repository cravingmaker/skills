#!/usr/bin/env python3
"""Turn approved local tickets into a check-plan.py plan skeleton.

Reads approved NN-slug.md files from the configured local ticket directory
and prints the PLAN.md JSON block to stdout. Pass the spec path from the
tracker setup with --spec; the default is the sibling spec.md.
Every ticket needs a non-empty Proof line, preserved as its task's proof. Fields only the coordinator
can decide stay {{placeholders}}, which check-plan.py rejects until they are
filled.

Requires Python 3.12 or later, standard library only. No writes or network.
Exit: 0 printed a plan, 1 findings, 2 usage or unreadable input.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

TICKET = re.compile(r"(\d+)-[a-z0-9][a-z0-9-]*\.md")
FIELD = re.compile(
    r"(?:\*\*(blocked by|status|proof):\*\*|\*\*(blocked by|status|proof)\*\*:|"
    r"(blocked by|status|proof):)\s*(.*?)\s*", re.I
)
CHECKBOX = re.compile(r"\s*[-*]\s+\[[ xX]\]\s+(.+?)\s*")
NUMBER = re.compile(r"(?:#|ticket\s+)?(\d+)\b", re.I)
NUMERIC_REFERENCE = re.compile(r"(?:#|ticket\s+)?\d+(?:\s*[:-]\s*.+)?", re.I)
READY = {"ready-for-agent", "ready-for-human"}
FINISHED = {"done", "closed", "resolved"}


def digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def shown(path, workspace):
    return str(path.relative_to(workspace)) if workspace and path.is_relative_to(workspace) else str(path)


def visible_line(line, in_comment):
    """Strip HTML comments while retaining literal markers inside inline code."""
    parts, start, position = [], 0, 0
    while position < len(line):
        if in_comment:
            end = line.find("-->", position)
            if end < 0:
                return "".join(parts), True
            in_comment = False
            position = start = end + 3
        elif line[position] == "\\":
            position += 2
        elif line.startswith("<!--", position):
            parts.append(line[start:position])
            in_comment = True
            position += 4
        elif line[position] == "`":
            end = position + 1
            while end < len(line) and line[end] == "`":
                end += 1
            closing = re.search(r"(?<!`)" + re.escape(line[position:end]) + r"(?!`)", line[end:])
            # An unmatched backtick run is literal text, not an open code span.
            position = end + closing.end() if closing else end
        else:
            position += 1
    if not in_comment:
        parts.append(line[start:])
    return "".join(parts), in_comment


def parse(path, text):
    """Return the ticket's title, fields, and acceptance items, ignoring comments."""
    title, fields, acceptance, listed, errors = None, {}, [], None, []
    fence = None
    in_comment = False
    inline_blockers = False
    for line in text.splitlines():
        if fence:
            marker = re.match(r"^\s*(`{3,}|~{3,})", line)
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                fence = None
            continue
        # A fence's info string is literal, including any HTML comment marker.
        if not in_comment and (marker := re.match(r"^\s*(`{3,}|~{3,})", line)):
            fence = marker[1]
            continue
        line, in_comment = visible_line(line, in_comment)
        if marker := re.match(r"^\s*(`{3,}|~{3,})", line):
            fence = marker[1]
            continue
        if re.fullmatch(r"##\s+comments\s*", line, re.I):
            break
        if title is None and (match := re.fullmatch(r"#\s+(.+?)\s*", line)):
            title = re.sub(r"^\d+\s*[:.)-]\s*", "", match[1])
            continue
        if match := FIELD.fullmatch(line):
            key = next(part for part in match.groups()[:3] if part is not None).lower()
            value = match[4]
            if key in fields:
                errors.append(f"{path.name}: repeated {key!r} field; keep one authoritative value")
            fields[key] = value
            # An empty inline "Blocked by:" or "Proof:" may be followed by one item per list line.
            listed = (key, []) if key in ("blocked by", "proof") and not value else None
            inline_blockers = key == "blocked by" and bool(value)
            continue
        if match := CHECKBOX.fullmatch(line):
            acceptance.append(match[1])
            listed = None
            inline_blockers = False
        elif inline_blockers or (listed is not None and listed[0] == "blocked by"):
            if not line.strip():
                continue
            if re.match(r"\s*#{1,6}\s+", line):
                listed = None
                inline_blockers = False
            elif not inline_blockers and (match := re.fullmatch(r"\s*[-*]\s+(.+?)\s*", line)):
                listed[1].append(match[1])
                fields["blocked by"] = ", ".join(listed[1])
            else:
                errors.append(f"{path.name}: unsupported continuation of 'blocked by'; "
                              "use one inline value, or an empty field followed only by '-' or '*' list items")
        elif listed is not None and (match := re.fullmatch(r"\s*[-*]\s+(.+?)\s*", line)):
            listed[1].append(match[1])
            fields[listed[0]] = "; ".join(listed[1])
        elif line.strip():
            listed = None
    return title, fields, acceptance, errors


def blockers(value, numbers, titles):
    """Resolve a Blocked by value to ticket numbers; return (found, unresolved parts)."""
    text = value.strip()
    if re.fullmatch(r"none(?:\s*\(can start immediately\))?\.?", text, re.I):
        return [], []
    if match := NUMBER.fullmatch(text):
        number = int(match[1])
        return ([number], []) if number in numbers else ([], [text])
    parts = re.split(r"\s*(?:,|;|\band\b)\s*", text, flags=re.I)
    numbered = all(NUMERIC_REFERENCE.fullmatch(part.strip()) for part in parts)
    if not numbered and text.casefold() in titles:
        matches = titles[text.casefold()]
        return (matches, []) if len(matches) == 1 else ([], [text])
    found, unresolved = [], []
    for part in parts:
        part = part.strip()
        if not part:
            unresolved.append("empty blocker")
            continue
        match = NUMBER.match(part)
        if match and int(match[1]) in numbers:
            number = int(match[1])
            suffix = part[match.end():].strip()
            title = numbers[number]["title"]
            labeled = suffix[:1] in (":", "-") and title and suffix[1:].strip().casefold() == title.casefold()
            if not suffix or labeled:
                found.append(number)
            else:
                unresolved.append(part)
        elif NUMERIC_REFERENCE.fullmatch(part):
            unresolved.append(part)
        elif part.casefold() in titles and len(titles[part.casefold()]) == 1:
            found.extend(titles[part.casefold()])
        else:
            unresolved.append(part)
    return found, unresolved


def build(directory, run_id, workspace, spec=None):
    errors = []
    tickets = {}
    for path in sorted(directory.iterdir()):
        if path.suffix != ".md" or not path.is_file():
            continue
        match = TICKET.fullmatch(path.name)
        if not match:
            errors.append(f"{path.name}: rename it to NN-slug.md or move it out of the issues directory")
            continue
        number = int(match[1])
        if number in tickets:
            errors.append(f"{path.name}: number {match[1]} repeats {tickets[number]['path'].name}; renumber one ticket")
            continue
        raw = path.read_bytes()
        title, fields, acceptance, findings = parse(path, raw.decode("utf-8"))
        errors.extend(findings)
        tickets[number] = {"path": path, "title": title, "fields": fields, "acceptance": acceptance,
                           "digest": "sha256:" + hashlib.sha256(raw).hexdigest()}
    if not tickets and not errors:
        raise ValueError(f"no NN-slug.md ticket files in {directory}; pass the to-tickets issues directory")

    titles = {}
    for number, ticket in tickets.items():
        if ticket["title"]:
            titles.setdefault(ticket["title"].casefold(), []).append(number)
    finished = set()
    for number, ticket in tickets.items():
        name = ticket["path"].name
        source_status = ticket["fields"].get("status", "")
        status = source_status.lower()
        ticket["status"] = source_status
        if not ticket["title"]:
            errors.append(f"{name}: add a '# NN: Title' heading")
        if not status:
            errors.append(f"{name}: add a 'Status:' line, such as ready-for-agent")
        elif status in FINISHED:
            finished.add(number)
        elif status not in READY:
            errors.append(f"{name}: status {status} is not ready to build; settle it with the user, then set ready-for-agent")
        proof = ticket["fields"].get("proof", "")
        if not proof.strip() or "{{" in proof:
            errors.append(f"{name}: add a non-empty 'Proof:' line naming the surface or source and the result to observe; resolve placeholders")
        if not ticket["fields"].get("blocked by"):
            errors.append(f"{name}: add a 'Blocked by:' line with ticket numbers, or 'Blocked by: None'")
            ticket["blockers"] = []
            continue
        found, unresolved = blockers(ticket["fields"]["blocked by"], tickets, titles)
        for part in unresolved:
            errors.append(f"{name}: cannot resolve blocker {part!r}; use comma-separated existing ticket numbers or an unambiguous exact title")
        if number in found:
            errors.append(f"{name}: a ticket cannot block itself; fix its Blocked by line")
        if len(set(found)) != len(found):
            errors.append(f"{name}: duplicate blockers; name each prerequisite once")
        ticket["blockers"] = [item for item in found if item != number]
        if status not in FINISHED and not ticket["acceptance"]:
            errors.append(f"{name}: add at least one '- [ ] criterion' acceptance checkbox")
    if tickets and not errors and len(finished) == len(tickets):
        errors.append("every ticket is done, closed, or resolved; there is nothing left to plan")
    if errors:
        return None, errors

    if not errors:
        visiting, visited = set(), set()

        def visit(number):
            if number in finished or number in visited:
                return
            if number in visiting:
                raise ValueError(f"{tickets[number]['path'].name}: dependency cycle; fix the Blocked by edges")
            visiting.add(number)
            for dependency in tickets[number]["blockers"]:
                visit(dependency)
            visiting.remove(number)
            visited.add(number)

        try:
            for number in tickets:
                visit(number)
        except (ValueError, RecursionError) as error:
            return None, [f"{error}; simplify the ticket graph before planning"]

    spec = spec or directory.parent / "spec.md"
    if not spec.is_file():
        raise ValueError(f"spec not found: {spec}; pass --spec with the approved spec path from the tracker setup")
    spec_input = [f"{shown(spec, workspace)} {digest(spec)}"]
    ids = {number: ticket["path"].stem for number, ticket in tickets.items()}
    tasks = []
    for number, ticket in tickets.items():
        if number in finished:
            continue
        tasks.append({
            "id": ids[number],
            "title": ticket["title"],
            "ticket_status": ticket["status"],
            "owner": "{{owner}}",
            "execution": "{{direct or a delegation reason}}",
            "reason": "{{why delegation pays; delete this field for direct work}}",
            "depends_on": [ids[b] for b in ticket["blockers"] if b not in finished],
            "write_paths": ["{{literal write path}}"],
            "inputs": [f"{shown(ticket['path'], workspace)} {ticket['digest']}", *spec_input],
            "outputs": ["{{artifact or revision this ticket delivers}}"],
            "acceptance": ticket["acceptance"],
            "proof": ticket["fields"]["proof"],
            "shared_resources": ["{{shared resource, or use [] for none}}"],
        })
    plan = {
        "run_id": run_id,
        "workspace": str(workspace) if workspace else "{{absolute workspace}}",
        "integration_owner": "{{integration owner}}",
        "source": {
            "tickets": shown(directory, workspace),
            "finished": sorted(ids[n] for n in finished),
        },
        "tasks": tasks,
        "budget": {
            "coordinator": "{{coordinator}}",
            "worker_starts": {"limit": "{{limit}}", "used": 0},
            "retries": {"limit": "{{limit}}", "used": 0},
            "review_rounds": {"limit": "{{limit}}", "used": 0},
            "concurrency": {"ceiling": "{{1 to 8}}", "active": 0},
            "reserve": {"worker_starts": "{{starts}}", "plan": "{{integration and verification plan}}"},
        },
    }
    return plan, []


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("issues", type=Path, help="the ticket directory from the tracker setup")
    parser.add_argument("--spec", type=Path, help="approved spec path; defaults to sibling spec.md")
    parser.add_argument("--run-id", help="defaults to the feature directory name")
    parser.add_argument("--workspace", type=Path, help="defaults to the directory that holds .scratch")
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: install Python 3.12 or later and rerun import-tickets.py", file=sys.stderr)
        return 2
    directory = args.issues.resolve()
    if not directory.is_dir():
        print(f"error: {args.issues} is not a directory; pass the ticket directory from the tracker setup", file=sys.stderr)
        return 2
    derived = len(directory.parts) >= 3 and directory.name == "issues" and directory.parent.parent.name == ".scratch"
    workspace = args.workspace.resolve() if args.workspace else directory.parent.parent.parent if derived else None
    run_id = args.run_id or (directory.parent.name if derived else "{{run id}}")
    try:
        plan, errors = build(directory, run_id, workspace, args.spec.resolve() if args.spec else None)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
