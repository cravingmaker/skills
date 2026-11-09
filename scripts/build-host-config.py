#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Preview generated Codex invocation policy; only --apply changes source files.

Exit: 0 success (including preview), 1 findings/drift or input errors, 2 usage.
JSON on stdout; diagnostics on stderr. Requires uv and Python 3.12+. No prompts.
"""

import argparse
import json
import sys
from pathlib import Path

import hostconfig
import skillcatalog
import yaml


def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="write the previewed owned files")
    mode.add_argument("--check", action="store_true", help="fail on generated-file drift; never write")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    options = parser.parse_args(arguments)
    try:
        repo = skillcatalog.load(options.root.resolve())
        for name in repo.frontmatter:
            if repo.invocation(name) not in ("model", "user"):
                raise ValueError(f"{name}: invocation must be model or user")
        changes, problems = hostconfig.plan(repo)
        if problems:
            raise ValueError("; ".join(problems))
        if options.check and changes:
            for path in changes:
                print(f"error: {path} has host configuration drift; preview and apply build-host-config.py", file=sys.stderr)
            return 1
        output = [{"path": str(path), "action": "delete" if content is None else "write", "content": content} for path, content in changes.items()]
        if options.apply:
            for path, content in changes.items():
                if content is None:
                    path.unlink()
                    if not any(path.parent.iterdir()):
                        path.parent.rmdir()
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")
        print(json.dumps({"mode": "apply" if options.apply else "check" if options.check else "preview", "changes": output}, indent=2))
        return 0
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
