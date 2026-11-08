#!/usr/bin/env python3
"""Tests for improve-codebase-architecture/scripts/render-report.py.

Hostile, source-shaped content must render as text, the default report must
make no network requests, and the Mermaid option must be pinned and strict.
Exit 0 when every case passes, 1 on any failure.
"""

import json
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "improve-codebase-architecture" / "scripts" / "render-report.py"
HOSTILE = '</pre><script>alert(1)</script>"><img src=x onerror=alert(1)>'
MERMAID = 'flowchart LR\n  A["<img src=x onerror=alert(2)>"] --> B\n  click A call alert(3)\n</pre><script>alert(4)</script>'
ALLOWED = {"html", "head", "meta", "title", "style", "script", "body", "main", "header", "h1", "h2", "h3",
           "p", "span", "ul", "li", "div", "pre", "article", "section", "a", "strong"}
FAILURES: list[str] = []


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict]] = []
        self.text: list[str] = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


def check(condition: bool, label: str) -> None:
    if not condition:
        FAILURES.append(label)
        print(f"FAIL {label}")


def sample() -> dict:
    side = {"modules": [HOSTILE, "OrderRepo"], "edges": [[HOSTILE, "OrderRepo", "leak"]], "mermaid": MERMAID}
    return {
        "repo": f"repo {HOSTILE}", "date": "2026-11-08", "scope": f"src/{HOSTILE}",
        "candidates": [{
            "id": 'c1" onmouseover="alert(5)', "title": HOSTILE, "strength": "Strong", "dependency": "in-process",
            "files": [f"src/{HOSTILE}.ts:10"], "evidence": [f"commit abc {HOSTILE}"], "problem": HOSTILE,
            "solution": HOSTILE, "wins": [HOSTILE], "adr": HOSTILE, "before": side,
            "after": {"modules": ["Order intake"], "mermaid": MERMAID},
        }],
        "top": {"id": 'c1" onmouseover="alert(5)', "why": HOSTILE},
    }


def render(data: object, *args: str) -> subprocess.CompletedProcess:
    work = Path(tempfile.mkdtemp(prefix="arch-report-"))
    path = work / "candidates.json"
    path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
    return subprocess.run([sys.executable, str(SCRIPT), str(path), *args], capture_output=True, text=True)


def parse(page: str) -> Collector:
    collector = Collector()
    collector.feed(page)
    return collector


def main() -> int:
    result = render(sample())
    check(result.returncode == 0, f"default render exits 0 ({result.stderr.strip()})")
    page = parse(result.stdout)
    names = [tag for tag, _ in page.tags]
    check(set(names) <= ALLOWED and "img" not in names, "only the report's own tags appear")
    check("script" not in names, "default report has no script")
    attrs = [(k, v or "") for _, a in page.tags for k, v in a.items()]
    check(not any(k.startswith("on") for k, _ in attrs), "no event-handler attributes")
    check(not any(k in ("src", "href") and not v.startswith("#") for k, v in attrs), "default report loads nothing remotely")
    check("http" not in result.stdout.replace("http-equiv", ""), "default report contains no URL")
    text = "".join(page.text)
    check(text.count(HOSTILE) >= 8, "hostile content survives as visible text")
    check("loose" not in result.stdout, "no loose Mermaid setting")

    result = render(sample(), "--mermaid-cdn")
    page = parse(result.stdout)
    scripts = [a for tag, a in page.tags if tag == "script"]
    check(result.returncode == 0 and len(scripts) == 2, "Mermaid option adds the pinned bundle and its initializer")
    remote = [attrs for attrs in scripts if "src" in attrs]
    check(len(remote) == 1 and remote[0].get("src") == "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js", "the optional bundle uses the exact pinned URL")
    check(len(remote) == 1 and remote[0].get("integrity") == "sha384-rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I" and remote[0].get("crossorigin") == "anonymous", "the browser verifies the fetched bundle against the pinned SHA-384")
    check('securityLevel: "strict"' in result.stdout and "loose" not in result.stdout, "Mermaid runs strict")
    check("mermaid@11.4.1/" in result.stdout and "cdn.jsdelivr.net" in "".join(page.text), "Mermaid pinned and network notice shown")
    check(sum(1 for tag, a in page.tags if tag == "pre" and a.get("class") == "mermaid") == 2, "Mermaid sources marked for rendering")

    bad = sample()
    bad["candidates"][0]["strength"] = "Maybe"
    del bad["candidates"][0]["evidence"]
    result = render(bad, "--check")
    report = json.loads(result.stdout)
    check(result.returncode == 1 and not report["valid"] and len(report["findings"]) == 2, "--check lists findings as JSON, exit 1")
    result = render(bad)
    check(result.returncode == 1 and result.stdout == "" and "finding:" in result.stderr, "invalid input renders nothing")
    check(render("{not json").returncode == 2, "unreadable JSON exits 2")
    result = render(sample(), "--check")
    check(result.returncode == 0 and json.loads(result.stdout)["valid"], "--check passes valid input")
    doc = (ROOT / "skills" / "improve-codebase-architecture" / "references" / "report-format.md").read_text(encoding="utf-8")
    example = doc.split("```json\n", 1)[1].split("```", 1)[0]
    result = render(example, "--check")
    check(result.returncode == 0 and json.loads(result.stdout)["valid"], "the documented example JSON is valid")
    help_run = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
    check(help_run.returncode == 0 and "Usage" in help_run.stdout, "--help exits 0")
    check(subprocess.run([sys.executable, str(SCRIPT)], capture_output=True).returncode == 2, "missing argument exits 2")
    out = Path(tempfile.mkdtemp(prefix="arch-out-")) / "report.html"
    result = render(sample(), "--output", str(out))
    check(result.returncode == 0 and out.is_file() and result.stdout.strip() == str(out.resolve()), "--output writes the file and prints its path")

    if FAILURES:
        print(f"improve-codebase-architecture: {len(FAILURES)} failure(s)")
        return 1
    print("improve-codebase-architecture: all cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
