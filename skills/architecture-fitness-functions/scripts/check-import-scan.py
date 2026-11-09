#!/usr/bin/env python3
"""Reject empty or wrongly scoped dependency-cruiser JSON reports.

Usage: check-import-scan.py GRAPH.json --require-root ROOT [--require-root ROOT]
Python 3.12+ standard library. Read-only; does not invoke tools or inspect code.
Stdout: JSON module/edge counts and findings. Stderr: input diagnostics.
Exits: 0 covered scan without errors, 1 empty/missing-root/error findings,
2 usage or malformed report. Pair with the real checker's own exit status.
Generate a fresh report; this helper cannot prove its freshness or completeness.
"""

import argparse
import json
import sys
from pathlib import Path


def check(data, roots):
    if not isinstance(data, dict) or not isinstance(data.get("modules"), list):
        raise ValueError("supply the dependency-cruiser JSON report with modules")
    summary = data.get("summary")
    if not isinstance(summary, dict) or not isinstance(summary.get("violations"), list):
        raise ValueError("include the original report summary and violations")
    sources, edges, findings = set(), 0, []
    for module in data["modules"]:
        if (not isinstance(module, dict) or not isinstance(module.get("source"), str)
                or not module["source"] or not isinstance(module.get("dependencies"), list)):
            raise ValueError("retain each module's source and dependencies")
        if module["source"] in sources:
            raise ValueError("retain unique module sources")
        sources.add(module["source"])
        edges += len(module["dependencies"])
    if not sources:
        findings.append("empty import scan; install a supported parser and correct the input roots")
    for root in roots:
        if not any(source == root or source.startswith(root + "/") for source in sources):
            findings.append(f"{root}: required root has no scanned modules; correct roots, exclusions, or parser support")
    for violation in summary["violations"]:
        if not isinstance(violation, dict) or not isinstance(violation.get("rule"), dict):
            raise ValueError("retain the original violation rule objects")
        rule = violation["rule"]
        if rule.get("severity") == "error":
            findings.append(f"{rule.get('name', 'unnamed rule')}: resolve this dependency error")
    if summary.get("error", 0) and not findings:
        findings.append("report contains dependency errors; retain and inspect the full rule diagnostics")
    return {"modules": len(sources), "edges": edges, "required_roots": roots, "findings": findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("graph", type=Path)
    parser.add_argument("--require-root", action="append", required=True)
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error("use Python 3.12 or later")
    roots = [root.rstrip("/") for root in args.require_root]
    if any(not root or root.startswith("/") or ".." in root.split("/") or root.startswith("./") for root in roots):
        parser.error("give non-empty report-relative roots, without a leading ./ or parent traversal")
    try:
        result = check(json.loads(args.graph.read_text(encoding="utf-8")), roots)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}; regenerate the full JSON report and rerun", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
