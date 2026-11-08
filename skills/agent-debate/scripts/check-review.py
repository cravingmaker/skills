#!/usr/bin/env python3
"""Check a review report against the agent-debate format.

The format is described in references/report-format.md. This script checks
structure, not truth: whether a finding is correct still needs a check at
the source.

Checks:
  - exactly one verdict line, the last non-empty line outside code blocks,
    either "VERDICT: FULL AGREEMENT" or
    "VERDICT: OBJECTIONS REMAIN (n blockers, n shoulds, n nits)";
  - the verdict counts match the findings, and FULL AGREEMENT has none;
  - a "REVIEWED:" line names what was reviewed;
  - finding IDs are unique, including against prior-finding lines;
  - each finding has a valid severity, at least one labeled Evidence line,
    and a Change line;
  - with --prior, every finding open last round is closed, withdrawn, or
    still listed;
  - with --round, a finding open longer than --max-rounds carries an
    Extension line naming the new evidence or material change.

Usage: check-review.py [--round N] [--max-rounds N] [--prior ID,ID] REPORT | -
Exit status: 0 the report passes, 1 the report has defects, 2 usage error.
Requires Python 3.12 or later; standard library only; reads only.
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SEVERITIES = ("blocker", "should", "nit")
EVIDENCE_LABELS = ("executed", "static", "hypothesis")
PRIOR_STATUSES = ("CLOSED", "WITHDRAWN")

ID = r"[A-Z][A-Z0-9]*-\d+"
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
FINDING_LIKE = re.compile(rf"^#{{1,6}}\s+({ID})\b")
FINDING = re.compile(rf"^#{{2,4}}\s+({ID})\b\s*(.*)$")
SEVERITY = re.compile(r"^\[([^\]]*)\]\s*(.*)$")
FIELD = r"^(?:[-*]\s+)?"
EVIDENCE = re.compile(FIELD + r"Evidence\s*(?:\(([^)]*)\))?\s*:\s*(.*)$")
CHANGE = re.compile(FIELD + r"Change\s*:\s*(.*)$")
EXTENSION = re.compile(FIELD + r"Extension\s*:\s*(.*)$")
PRIOR = re.compile(rf"^[-*]\s+({ID})\s+([A-Z][A-Z ]*?)\s*:\s*(.*)$")
VERDICT_LIKE = re.compile(r"^\W*VERDICT\b", re.IGNORECASE)
VERDICT_AGREE = re.compile(r"^VERDICT: FULL AGREEMENT$")
VERDICT_OPEN = re.compile(
    r"^VERDICT: OBJECTIONS REMAIN \((\d+) blockers?, (\d+) shoulds?, (\d+) nits?\)$"
)
ROUND_ID = re.compile(r"^R(\d+)-\d+$")
FORMAT_HINT = "see references/report-format.md"


@dataclass
class Finding:
    id: str
    line: int
    severity: str | None = None
    evidence: list[str] = field(default_factory=list)
    change: str | None = None
    extension: str | None = None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check a review report against the agent-debate format.",
        epilog="Exit status: 0 pass, 1 defects found, 2 usage error.",
    )
    parser.add_argument("report", help="report file, or - for stdin")
    parser.add_argument("--round", type=int, help="the current round number (1 or more)")
    parser.add_argument(
        "--max-rounds", type=int, default=3, help="rounds a finding may stay open (default 3)"
    )
    parser.add_argument(
        "--prior", default="", help="comma-separated IDs that were open after the last round"
    )
    args = parser.parse_args(argv)
    if args.round is not None and args.round < 1:
        parser.error("--round must be 1 or more")
    if args.max_rounds < 1:
        parser.error("--max-rounds must be 1 or more")
    args.prior_ids = [item.strip() for item in args.prior.split(",") if item.strip()]
    for prior_id in args.prior_ids:
        if not re.fullmatch(ID, prior_id):
            parser.error(f"--prior ID {prior_id!r} is not an ID like R1-01")
    return args


def read_report(path: str) -> str:
    try:
        if path == "-":
            return sys.stdin.read()
        file = Path(path)
        if not file.is_file():
            print(f"error: report not found: {path}. Pass the saved raw report.", file=sys.stderr)
            raise SystemExit(2)
        return file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"error: read a complete UTF-8 report with accessible permissions: {error}", file=sys.stderr)
        raise SystemExit(2) from None


def check(text: str, args: argparse.Namespace) -> list[str]:
    problems: list[str] = []
    findings: list[Finding] = []
    prior_lines: dict[str, int] = {}
    verdicts: list[tuple[int, str]] = []
    reviewed = False
    last_line = (0, "")
    current: Finding | None = None
    fence: tuple[str, int, int] | None = None

    for number, raw in enumerate(text.splitlines(), start=1):
        marker = FENCE.match(raw)
        if fence is not None:
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= fence[1] and not marker.group(2).strip():
                fence = None
            continue
        if marker:
            token, info = marker.groups()
            if token[0] != "`" or "`" not in info:
                fence = (token[0], len(token), number)
                continue
        line = raw.strip()
        if line:
            last_line = (number, line)
        if VERDICT_LIKE.match(line):
            verdicts.append((number, line))
            current = None
            continue
        if line.startswith("REVIEWED:") and line.removeprefix("REVIEWED:").strip():
            reviewed = True
        if match := FINDING.match(line):
            current = Finding(match.group(1), number)
            findings.append(current)
            severity = SEVERITY.match(match.group(2))
            if severity is None:
                problems.append(
                    f"line {number}: {current.id} has no severity. "
                    f"Write '### {current.id} [blocker|should|nit] <location>: <claim>'."
                )
            elif severity.group(1) not in SEVERITIES:
                problems.append(
                    f"line {number}: {current.id} has severity [{severity.group(1)}]. "
                    "Use exactly one of [blocker], [should], [nit]."
                )
            else:
                current.severity = severity.group(1)
                if not severity.group(2).strip():
                    problems.append(
                        f"line {number}: {current.id} has no location or claim after its severity."
                    )
            continue
        if line.startswith("#"):
            if match := FINDING_LIKE.match(line):
                problems.append(f"line {number}: malformed heading for {match.group(1)}. Use two to four # characters.")
            current = None
            continue
        if match := PRIOR.match(line):
            status = match.group(2)
            if status not in PRIOR_STATUSES:
                problems.append(
                    f"line {number}: {match.group(1)} has status {status!r}. "
                    "A prior finding is CLOSED or WITHDRAWN; list it as a finding if it stays open."
                )
            elif not match.group(3).strip():
                problems.append(f"line {number}: {match.group(1)} {status} needs a reason.")
            if match.group(1) in prior_lines:
                problems.append(f"line {number}: {match.group(1)} is listed twice as a prior finding.")
            prior_lines.setdefault(match.group(1), number)
            continue
        if current is None:
            continue
        if match := EVIDENCE.match(line):
            label = (match.group(1) or "").strip()
            if label not in EVIDENCE_LABELS:
                shown = f"({label})" if label else "with no label"
                problems.append(
                    f"line {number}: {current.id} has Evidence {shown}. "
                    "Write 'Evidence (executed|static|hypothesis): <what>'."
                )
            elif not match.group(2).strip():
                problems.append(f"line {number}: {current.id} Evidence ({label}) is empty.")
            else:
                current.evidence.append(label)
        elif match := CHANGE.match(line):
            current.change = match.group(1).strip()
        elif match := EXTENSION.match(line):
            current.extension = match.group(1).strip()

    if fence is not None:
        problems.append(f"line {fence[2]}: unclosed code fence. Close it before the final verdict.")
    problems += check_findings(findings, prior_lines, args)
    problems += check_verdict(verdicts, last_line, findings)
    if not reviewed:
        problems.append(
            "no REVIEWED line. Add 'REVIEWED: <artifact> at <revision or SHA-256>; scope: <what was read>'."
        )
    return problems


def check_findings(
    findings: list[Finding], prior_lines: dict[str, int], args: argparse.Namespace
) -> list[str]:
    problems: list[str] = []
    seen: dict[str, int] = {}
    for finding in findings:
        if finding.id in seen:
            problems.append(
                f"line {finding.line}: {finding.id} repeats the ID from line {seen[finding.id]}. "
                "Give each finding its own ID."
            )
        seen.setdefault(finding.id, finding.line)
        if finding.id in prior_lines:
            problems.append(
                f"line {finding.line}: {finding.id} is both open and marked "
                f"closed or withdrawn on line {prior_lines[finding.id]}. Keep one."
            )
        if not finding.evidence:
            problems.append(
                f"line {finding.line}: {finding.id} has no evidence. "
                "Add 'Evidence (executed|static|hypothesis): <what>'."
            )
        if not finding.change:
            problems.append(
                f"line {finding.line}: {finding.id} has no exact change. "
                "Add 'Change: <the replacement text, command, or check to run>'."
            )
        if args.round is not None and (match := ROUND_ID.match(finding.id)):
            opened = int(match.group(1))
            if opened > args.round:
                problems.append(
                    f"line {finding.line}: {finding.id} is numbered for round {opened}, "
                    f"after the current round {args.round}."
                )
            elif args.round - opened + 1 > args.max_rounds and not finding.extension:
                problems.append(
                    f"line {finding.line}: {finding.id} has been open for "
                    f"{args.round - opened + 1} rounds (limit {args.max_rounds}). "
                    "Add 'Extension: <new evidence or material change>', "
                    "or bring it to the user as a decision."
                )
    for prior_id in args.prior_ids:
        if prior_id not in seen and prior_id not in prior_lines:
            problems.append(
                f"{prior_id} was open after the last round but is missing. "
                f"List it as a finding, or add '- {prior_id} CLOSED: <reason>'."
            )
    return problems


def check_verdict(
    verdicts: list[tuple[int, str]], last_line: tuple[int, str], findings: list[Finding]
) -> list[str]:
    if not verdicts:
        return [
            "no verdict line. End with 'VERDICT: FULL AGREEMENT' or "
            "'VERDICT: OBJECTIONS REMAIN (n blockers, n shoulds, n nits)'."
        ]
    if len(verdicts) > 1:
        where = ", ".join(str(number) for number, _ in verdicts)
        return [f"{len(verdicts)} verdict lines (lines {where}). Keep exactly one, as the last line."]
    number, line = verdicts[0]
    problems: list[str] = []
    if number != last_line[0]:
        problems.append(f"line {number}: the verdict is not the last line. Move it to the end.")
    counts = {severity: 0 for severity in SEVERITIES}
    for finding in findings:
        if finding.severity:
            counts[finding.severity] += 1
    if VERDICT_AGREE.match(line):
        if findings:
            problems.append(
                f"line {number}: FULL AGREEMENT with {len(findings)} open findings. "
                "Use OBJECTIONS REMAIN with their counts, or close them."
            )
    elif match := VERDICT_OPEN.match(line):
        stated = dict(zip(SEVERITIES, (int(group) for group in match.groups())))
        if stated != counts:
            problems.append(
                f"line {number}: the verdict states {stated['blocker']} blockers, "
                f"{stated['should']} shoulds, {stated['nit']} nits; the findings have "
                f"{counts['blocker']} blockers, {counts['should']} shoulds, {counts['nit']} nits. "
                "Make them match."
            )
        if not findings:
            problems.append(
                f"line {number}: OBJECTIONS REMAIN with no findings. Use VERDICT: FULL AGREEMENT."
            )
    else:
        problems.append(
            f"line {number}: malformed verdict {line!r}. Use 'VERDICT: FULL AGREEMENT' or "
            "'VERDICT: OBJECTIONS REMAIN (n blockers, n shoulds, n nits)'."
        )
    return problems


def main(argv: list[str]) -> int:
    if sys.version_info < (3, 12):
        print("error: check-review.py needs Python 3.12 or later.", file=sys.stderr)
        return 2
    args = parse_args(argv)
    problems = check(read_report(args.report), args)
    name = "stdin" if args.report == "-" else args.report
    if problems:
        noun = "defect" if len(problems) == 1 else "defects"
        print(f"{name}: {len(problems)} {noun} ({FORMAT_HINT}):")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(f"{name}: the review report matches the format.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
