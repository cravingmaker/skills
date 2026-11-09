#!/usr/bin/env python3
"""Render an architecture review from JSON into one static HTML file.

Usage:
  render-report.py CANDIDATES.json                 print the HTML to stdout
  render-report.py CANDIDATES.json --output FILE   write the HTML to FILE
  render-report.py CANDIDATES.json --check         validate only; print JSON findings
  render-report.py CANDIDATES.json --mermaid-cdn   also load pinned Mermaid from a CDN
  render-report.py --help

Every value from the JSON is HTML-escaped. The default report has no scripts
and no network requests. --mermaid-cdn adds Mermaid MERMAID_VERSION from
cdn.jsdelivr.net with securityLevel "strict" and a visible notice that the
diagrams need network access. The complete bundle is pinned with SHA-384 SRI;
without it, Mermaid sources render as text.

Exit status: 0 rendered (or valid with --check), 1 the JSON has findings
(listed as JSON on stdout with --check, otherwise on stderr), 2 usage error or
unreadable input. Requires Python 3.12+ and no packages.
"""

import argparse
import html
import json
import sys
from pathlib import Path

MERMAID_VERSION = "11.4.1"
MERMAID_URL = f"https://cdn.jsdelivr.net/npm/mermaid@{MERMAID_VERSION}/dist/mermaid.min.js"
MERMAID_INTEGRITY = "sha384-rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I"
STRENGTHS = {"Strong": "strong", "Worth exploring": "explore", "Speculative": "speculative"}
DEPENDENCIES = {"in-process", "local-substitutable", "ports & adapters", "mock"}
REQUIRED = ("id", "title", "strength", "dependency", "files", "evidence", "problem", "solution", "wins", "before", "after")

CSS = """
:root { --bg:#fafaf9; --fg:#0f172a; --muted:#64748b; --card:#fff; --line:#e2e8f0;
  --accent:#047857; --warn:#b45309; --leak:#dc2626; --deep:#1e293b; }
@media (prefers-color-scheme: dark) { :root { --bg:#0b1120; --fg:#e2e8f0; --muted:#94a3b8;
  --card:#111827; --line:#334155; --accent:#34d399; --warn:#fbbf24; --leak:#f87171; --deep:#e2e8f0; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font:16px/1.5 system-ui, sans-serif; }
main { max-width:64rem; margin:0 auto; padding:2rem 1rem 4rem; }
h1, h2 { font-family:Georgia, serif; line-height:1.2; }
.legend, .meta, .files, .evidence { color:var(--muted); font-size:.875rem; }
.notice { border:1px solid var(--warn); color:var(--warn); padding:.5rem .75rem; border-radius:.5rem; }
article { background:var(--card); border:1px solid var(--line); border-radius:.75rem; padding:1.25rem; margin:2rem 0; }
.badge { display:inline-block; font-size:.75rem; text-transform:uppercase; letter-spacing:.05em;
  border:1px solid currentColor; border-radius:999px; padding:.1rem .6rem; margin-right:.4rem; }
.strong { color:var(--accent); } .explore { color:var(--warn); } .speculative { color:var(--muted); }
.files, .evidence { font-family:ui-monospace, monospace; }
.grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(16rem, 1fr)); gap:1rem; }
.diagram { border:1px solid var(--line); border-radius:.5rem; padding:.75rem; min-height:8rem; }
.diagram h3 { margin:0 0 .5rem; font-size:.75rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); }
.mod { border:1px solid var(--fg); border-radius:.25rem; padding:.25rem .5rem; margin:.25rem 0;
  font-size:.75rem; text-transform:uppercase; letter-spacing:.05em; }
.deep { border:3px solid var(--deep); border-radius:.4rem; padding:.5rem; }
.deep .mod { opacity:.55; border-style:dashed; }
.edge { font-size:.75rem; font-family:ui-monospace, monospace; }
.edge.leak { color:var(--leak); }
.adr { border-left:4px solid var(--warn); padding:.25rem .75rem; }
pre.mermaid, pre.source { overflow-x:auto; font-size:.75rem; }
"""


def findings(data: object) -> list[str]:
    problems: list[str] = []
    if not isinstance(data, dict):
        return ["top level must be an object with repo, candidates and top"]
    for key in ("repo", "date", "scope"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            problems.append(f"{key} must be a non-empty string")
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        problems.append("candidates must be a non-empty list")
        candidates = []
    ids = []
    for index, candidate in enumerate(candidates):
        where = f"candidates[{index}]"
        if not isinstance(candidate, dict):
            problems.append(f"{where} must be an object")
            continue
        for key in REQUIRED:
            if key not in candidate:
                problems.append(f"{where}.{key} is missing")
        for key in ("id", "title", "problem", "solution"):
            if not isinstance(candidate.get(key), str) or not candidate[key].strip():
                problems.append(f"{where}.{key} must be a non-empty string")
        if not isinstance(candidate.get("strength"), str) or candidate["strength"] not in STRENGTHS:
            problems.append(f"{where}.strength must be one of {', '.join(STRENGTHS)}")
        if not isinstance(candidate.get("dependency"), str) or candidate["dependency"] not in DEPENDENCIES:
            problems.append(f"{where}.dependency must be one of {', '.join(sorted(DEPENDENCIES))}")
        for key in ("files", "evidence", "wins"):
            if key not in candidate:
                continue
            value = candidate[key]
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
                problems.append(f"{where}.{key} must be a non-empty list of strings")
        for key in ("before", "after"):
            if key not in candidate:
                continue
            side = candidate[key]
            if not isinstance(side, dict) or not isinstance(side.get("modules"), list) or not side["modules"]:
                problems.append(f"{where}.{key}.modules must be a non-empty list")
                continue
            if not all(isinstance(m, str) for m in side["modules"]):
                problems.append(f"{where}.{key}.modules must hold strings")
            edges = side.get("edges", [])
            if not isinstance(edges, list):
                problems.append(f"{where}.{key}.edges must be a list")
                edges = []
            for edge in edges:
                if not (isinstance(edge, list) and len(edge) in (2, 3) and all(isinstance(e, str) for e in edge) and (len(edge) == 2 or edge[2] == "leak")):
                    problems.append(f"{where}.{key}.edges entries must be [from, to] or [from, to, \"leak\"]")
            if "mermaid" in side and not isinstance(side["mermaid"], str):
                problems.append(f"{where}.{key}.mermaid must be a string")
        if isinstance(candidate.get("id"), str):
            ids.append(candidate["id"])
    if len(set(ids)) != len(ids):
        problems.append("candidate ids must be unique")
    top = data.get("top")
    if not isinstance(top, dict) or not isinstance(top.get("id"), str) or top["id"] not in ids or not isinstance(top.get("why"), str) or not top["why"].strip():
        problems.append("top must name an existing candidate id and give a why string")
    return problems


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def diagram(label: str, side: dict, deep: bool, mermaid: bool) -> str:
    modules = "".join(f'<div class="mod">{esc(m)}</div>' for m in side["modules"])
    if deep:
        modules = f'<div class="deep">{modules}</div>'
    edges = "".join(
        f'<div class="edge{" leak" if len(e) == 3 and e[2] == "leak" else ""}">{esc(e[0])} → {esc(e[1])}'
        f'{" (leak)" if len(e) == 3 and e[2] == "leak" else ""}</div>'
        for e in side.get("edges", []))
    source = ""
    if side.get("mermaid"):
        css = "mermaid" if mermaid else "source"
        source = f'<pre class="{css}">{esc(side["mermaid"])}</pre>'
    return f'<div class="diagram"><h3>{esc(label)}</h3>{modules}{edges}{source}</div>'


def render(data: dict, mermaid: bool) -> str:
    cards = []
    for c in data["candidates"]:
        adr = f'<p class="adr">{esc(c["adr"])}</p>' if c.get("adr") else ""
        cards.append(
            f'<article id="{esc(c["id"])}"><h2>{esc(c["title"])}</h2>'
            f'<p><span class="badge {STRENGTHS[c["strength"]]}">{esc(c["strength"])}</span>'
            f'<span class="badge">{esc(c["dependency"])}</span></p>'
            f'<ul class="files">{"".join(f"<li>{esc(f)}</li>" for f in c["files"])}</ul>'
            f'<div class="grid">{diagram("Before", c["before"], False, mermaid)}{diagram("After", c["after"], True, mermaid)}</div>'
            f'<p><strong>Problem:</strong> {esc(c["problem"])}</p>'
            f'<p><strong>Solution:</strong> {esc(c["solution"])}</p>'
            f'<ul>{"".join(f"<li>{esc(w)}</li>" for w in c["wins"])}</ul>'
            f'<p><strong>Evidence</strong></p><ul class="evidence">{"".join(f"<li>{esc(e)}</li>" for e in c["evidence"])}</ul>'
            f"{adr}</article>")
    top = data["top"]
    top_title = next(c["title"] for c in data["candidates"] if c["id"] == top["id"])
    notice = ""
    script = ""
    if mermaid:
        notice = (f'<p class="notice">Diagrams load Mermaid {MERMAID_VERSION} from cdn.jsdelivr.net; '
                  "without network access they show as text.</p>")
        script = (f'<script src="{MERMAID_URL}" integrity="{MERMAID_INTEGRITY}" '
                  'crossorigin="anonymous"></script><script>'
                  'if (window.mermaid) { mermaid.initialize({ startOnLoad: true, '
                  'theme: "neutral", securityLevel: "strict" }); }'
                  "</script>")
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>Architecture review: {esc(data['repo'])}</title><style>{CSS}</style>{script}</head>"
        f"<body><main><header><h1>Architecture review: {esc(data['repo'])}</h1>"
        f'<p class="meta">{esc(data["date"])} · scope: {esc(data["scope"])}</p>'
        '<p class="legend">box = module · thick box = deepened module · faded = now internal · red edge = leakage</p>'
        f"{notice}</header>{''.join(cards)}"
        f'<section id="top-recommendation"><h2>Top recommendation</h2>'
        f'<p><a href="#{esc(top["id"])}">{esc(top_title)}</a>: {esc(top["why"])}</p></section>'
        "</main></body></html>\n")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)
    parser.add_argument("candidates")
    parser.add_argument("--output")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--mermaid-cdn", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as error:
        return 0 if error.code == 0 else 2
    if sys.version_info < (3, 12):
        print("error: render-report.py needs Python 3.12 or later; use python3.12 or a newer versioned interpreter on PATH, or uv run --python 3.12 render-report.py", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"cannot read {args.candidates}: {error}", file=sys.stderr)
        return 2
    problems = findings(data)
    if args.check:
        print(json.dumps({"valid": not problems, "findings": problems}, indent=2))
        return 1 if problems else 0
    if problems:
        for problem in problems:
            print(f"finding: {problem}", file=sys.stderr)
        print("fix the JSON, then render again; --check lists findings as JSON", file=sys.stderr)
        return 1
    page = render(data, args.mermaid_cdn)
    if args.output:
        try:
            Path(args.output).write_text(page, encoding="utf-8")
        except OSError as error:
            print(f"cannot write {args.output}: {error}; choose a writable output path", file=sys.stderr)
            return 2
        print(str(Path(args.output).resolve()))
    else:
        sys.stdout.write(page)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
