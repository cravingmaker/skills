#!/usr/bin/env python3
"""Find visible call sites that need a timeout or fan-out review.

Python 3.12+ standard library. Read-only, offline, no prompts.
Usage: find-unbounded-calls.py SOURCE [SOURCE ...]
Supply explicit UTF-8 .ts/.tsx/.mts/.cts/.js/.jsx/.mjs/.cjs/.rs files; no directory scan.
stdout: JSON candidate codes and file/line locations, never source snippets.
stderr: usage/input diagnostics. Exit: 0 no candidates, 1 candidates, 2 bad input.
This text heuristic cannot prove the absence of unbounded work. Indirect options,
shared clients, aliases, query wrappers, template strings and Rust macros need review.
"""

import argparse
import json
import re
import sys
from pathlib import Path

CALL = re.compile(
    r"\bfetch\s*\(|\bPromise\.(?:all|allSettled|any|race)\s*\(|"
    r"\breqwest::(?:get|Client::new|Client::builder)\s*\(|"
    r"\baxios\.(?:create|get|post|put|patch|delete|request)\s*\(|"
    r"\b(?:(?:futures::future::)?(?:try_)?join_all)\s*\(|"
    r"\bnew\s+(?:pg\.)?(?:Pool|Client)\s*\("
)


def mask_comments(text):
    # Retain ordinary quoted strings while removing comments and their hints.
    pattern = re.compile(r"""("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(/\*[\s\S]*?\*/|//[^\n]*)""")
    return pattern.sub(lambda m: m[1] if m[1] is not None else
                       "".join("\n" if c == "\n" else " " for c in m[0]), text)


def call_end(text, start):
    depth, quote, escaped = 0, None, False
    for offset in range(start, len(text)):
        char = text[offset]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in ('"', "'", chr(96)):
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return offset + 1
    return len(text)


def scan(text, label):
    text = mask_comments(text)
    findings = []
    for match in CALL.finditer(text):
        head = match[0]
        end = call_end(text, match.end() - 1)
        call = text[match.start():end]
        code = None
        if head.startswith("fetch") and not re.search(r"\bsignal\s*[:,}]", call):
            code = "fetch_no_visible_signal"
        elif head.startswith("Promise"):
            if re.search(r"\.map\s*\(|\.\.\.", call):
                code = "fanout_requires_input_bound"
        elif "join_all" in head and re.search(r"\.map\s*\(", call):
            code = "fanout_requires_input_bound"
        elif head.startswith("axios") and not re.search(r"\b(?:timeout|signal)\s*[:,}]", call):
            code = "axios_no_visible_timeout_or_signal"
        elif head.startswith("reqwest"):
            # Builder chains finish after the initial empty constructor call.
            finish = text.find(";", end)
            chain = text[match.start():finish if finish >= 0 else len(text)]
            if not re.search(r"\.timeout\s*\(", chain):
                code = "reqwest_no_visible_total_timeout"
        elif head.startswith("new") and not re.search(
            r"\b(?:query_timeout|statement_timeout)\s*:", call
        ):
            code = "pg_client_no_visible_query_timeout"
        if code:
            findings.append({
                "file": label,
                "line": text.count("\n", 0, match.start()) + 1,
                "code": code,
            })
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: use Python 3.12 or later", file=sys.stderr)
        return 2
    findings = []
    scanned = 0
    try:
        for source in dict.fromkeys(args.sources):
            if source.suffix not in {".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs", ".rs"} or not source.is_file():
                raise ValueError("unsupported source")
            text = source.read_text(encoding="utf-8")
            scanned += 1
            findings.extend(scan(text, str(source)))
    except (OSError, UnicodeError, ValueError):
        print("error: supply existing UTF-8 source files listed in --help, not directories", file=sys.stderr)
        return 2
    print(json.dumps({"files_scanned": scanned, "complete_analysis": False,
                      "candidates": findings}, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
