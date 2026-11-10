#!/usr/bin/env python3
"""Flag tracked delivery patterns, not credential values or a clean bill of health."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

STORED_KEY = re.compile(r"\bsecrets\s*(?:\.\s*|\[\s*['\"])(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN|AZURE_CREDENTIALS|GOOGLE_CREDENTIALS|GCP_SA_KEY|GCLOUD_SERVICE_KEY)\b", re.I)
STATIC_INPUT = re.compile(r"^\s*-?\s*(?:aws-secret-access-key|aws-access-key-id|credentials_json|creds)\s*:\s*\S", re.I)
SECRET_KIND = re.compile(r"^\s*kind\s*:\s*['\"]?Secret['\"]?\s*(?:#.*)?$")
SOPS = re.compile(r"^sops\s*:\s*(?:#.*)?$")


def main():
    parser = argparse.ArgumentParser(description=(
        "Read tracked files in a Git repository; flag .env copies, common stored "
        "cloud-key references in workflows and unencrypted-looking Kubernetes Secret "
        "YAML. Requires git on PATH and Python 3.12+ stdlib. No writes or network. "
        "JSON path/line/rule on stdout, diagnostics on stderr. Exits: 0 no heuristic "
        "findings, 1 findings, 2 invalid input. Not a general secret scanner."))
    parser.add_argument("--repo", required=True, type=Path)
    args = parser.parse_args()
    if shutil.which("git") is None:
        print("error: git is missing; install Git and retry with --repo", file=sys.stderr)
        return 2
    try:
        root = args.repo.resolve(strict=True)
        command = ["git", "-c", "core.fsmonitor=false", "-C", str(root)]
        target = subprocess.run(command + ["rev-parse", "--show-toplevel"], capture_output=True, check=True)
        if Path(target.stdout.decode().strip()).resolve() != root:
            raise ValueError("supply the repository root")
        tracked = subprocess.run(command + ["ls-files", "-z", "--cached"], capture_output=True, check=True)
        names = sorted(set(n.decode("utf-8") for n in tracked.stdout.split(b"\0") if n))
        findings = []
        for name in names:
            relative = Path(name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("invalid tracked path")
            path = root / relative
            def flag(line, rule):
                findings.append({"path": name, "line": line, "rule": rule})
            if path.is_symlink() or any(parent.is_symlink() for parent in list(path.parents) if parent != root and root in parent.parents):
                flag(1, "symlink-not-scanned")
                continue
            if not path.is_file():
                flag(1, "tracked-file-unavailable")
                continue
            if path.name.endswith((".tfstate", ".tfstate.backup")):
                flag(1, "tracked-state-file")
                continue
            if path.name == ".env" or path.name.startswith(".env."):
                if path.name not in (".env.example", ".env.sample", ".env.template"):
                    flag(1, "tracked-dotenv-review")
            workflow = (name.startswith(".github/workflows/") and path.suffix.lower() in (".yml", ".yaml")) or name == ".gitlab-ci.yml"
            yaml_file = path.suffix.lower() in (".yml", ".yaml")
            if not (workflow or yaml_file):
                continue
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            if workflow:
                for number, line in enumerate(lines, 1):
                    if not line.lstrip().startswith("#") and STORED_KEY.search(line):
                        flag(number, "stored-cloud-key-reference")
                    elif STATIC_INPUT.search(line):
                        flag(number, "static-cloud-login-input-review")
            start = 0
            for end in [i for i, line in enumerate(lines) if re.fullmatch(r"---\s*(?:#.*)?", line)] + [len(lines)]:
                document = lines[start:end]
                kinds = [start + offset + 1 for offset, line in enumerate(document) if SECRET_KIND.fullmatch(line)]
                encrypted = any(SOPS.fullmatch(line) for line in document) and any("ENC[" in line for line in document)
                if not encrypted:
                    for number in kinds:
                        flag(number, "secret-document-without-encryption-evidence")
                start = end + 1
    except (OSError, ValueError, UnicodeError, subprocess.CalledProcessError):
        print("error: cannot inspect tracked files; supply a readable Git root and UTF-8 workflow/manifest files (payload withheld)", file=sys.stderr)
        return 2
    print(json.dumps({"tracked_files": len(names), "findings": findings,
                      "scope": "tracked delivery-pattern heuristic; run the configured redacted secret scanner too"}, sort_keys=True))
    return int(bool(findings))


if __name__ == "__main__":
    sys.exit(main())
