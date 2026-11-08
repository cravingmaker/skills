#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Measure installed-host discovery with private homes and no model inference.

Install a role through install-skills.py, query the host's discovery interface,
then capture its first inference request on loopback and terminate the host.
The sink never returns a model response. No real authentication is read/copied.
Extra discovery metadata is replayed as standalone skills; bodies and plugin
execution are excluded. agents/openai.yaml preserves Codex visibility policy.
"""

import argparse
import hashlib
import http.server
import json
import math
import os
import re
import selectors
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import yaml

from evalharness.hosts import codex_inventory, configure, environment
from evalharness.isolation import Arm, InvalidComparison, managed_sources
from skillcatalog import read_frontmatter


def plugin_skills(root):
    root = root.resolve()
    manifest = next((root / name for name in [".codex-plugin/plugin.json", ".claude-plugin/plugin.json"]
                     if (root / name).is_file()), None)
    if manifest is None:
        standard = sorted((root / "skills").glob("*/SKILL.md"))
        if standard:
            return standard
        raise ValueError(f"{root}: skill manifest or standard skills folder missing; pass an installed plugin version directory")
    declared = json.loads(manifest.read_text()).get("skills", [])
    result = set()
    for relative in [declared] if isinstance(declared, str) else declared:
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"{manifest}: skill path escapes the plugin directory")
        if (path / "SKILL.md").is_file():
            result.add(path / "SKILL.md")
        else:
            result.update(path.rglob("SKILL.md"))
    return sorted(result)


def texts(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from texts(child)
    elif isinstance(value, list):
        for child in value:
            yield from texts(child)


def replay_metadata(source, destination):
    data = read_frontmatter(source)
    destination.mkdir()  # A duplicate name is an error, never an overwrite.
    fields = {key: data[key] for key in ["name", "description", "when_to_use", "disable-model-invocation", "user-invocable", "argument-hint"] if key in data}
    (destination / "SKILL.md").write_text("---\n" + yaml.safe_dump(fields, sort_keys=False) + "---\n\nDiscovery-only fixture.\n")
    policy = source.parent / "agents/openai.yaml"
    if policy.is_file():
        (destination / "agents").mkdir()
        shutil.copyfile(policy, destination / "agents/openai.yaml")


def listing(request, host):
    for text in texts(request):
        if host == "codex" and "<skills_instructions>" in text:
            block = text.split("<skills_instructions>", 1)[1].split("</skills_instructions>", 1)[0]
            start = block.find("### Skill roots\n")
            if start < 0:
                start = block.find("### Available skills\n")
            if start >= 0:
                return block[start:].rstrip()
        if host == "claude":
            marker = "The following skills are available for use with the Skill tool:\n\n"
            if marker in text:
                return text.split(marker, 1)[1].split("\n\n", 1)[0].rstrip()
    raise ValueError(f"{host}: rendered listing not found; update the extractor for this host version")


def description_state(description, original):
    if description == original:
        return "full"
    normalized = re.sub(r"\s+", " ", original).strip()
    if re.sub(r"\s+", " ", description).strip() == normalized:
        return "whitespace-normalized"
    if normalized.startswith(description.removesuffix("…")):
        return "shortened"
    return "changed"


def description_states(rendered, sources, host):
    rows = {}
    for line in rendered.splitlines():
        if not line.startswith("- "):
            continue
        body = line[2:]
        if host == "codex" and " (file: " in body:
            body = body.rsplit(" (file: ", 1)[0]
        name, separator, description = body.partition(": ")
        if name in sources:
            rows[name] = description if separator else ""
    return {name: "omitted" if name not in rows else "name-only" if not rows[name]
            else description_state(rows[name], data["description"])
            for name, data in sources.items()}


def stop(process):
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)


def claude_inventory(arm, binary):
    argv = [binary, "-p", "--verbose", "--input-format", "stream-json", "--output-format", "stream-json",
            "--no-session-persistence", "--setting-sources", "user", "--settings", str(arm.config / "settings.json"),
            "--strict-mcp-config", "--mcp-config", str(arm.base / "mcp.json"), "--no-chrome", "--tools", "Skill"]
    with (arm.evidence / "sdk-stderr").open("wb") as stderr:
        process = subprocess.Popen(argv, cwd=arm.work, env=environment(arm, "claude"),
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr, start_new_session=True)
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        buffered = b""
        responses = []
        try:
            for subtype, extra in [("initialize", {}), ("get_context_usage", {"detail": "summary"})]:
                value = {"type": "control_request", "request_id": subtype, "request": {"subtype": subtype, **extra}}
                process.stdin.write(json.dumps(value).encode() + b"\n")
                process.stdin.flush()
                deadline = time.monotonic() + 20
                response = None
                while time.monotonic() < deadline and response is None:
                    if not selector.select(timeout=0.5):
                        continue
                    chunk = os.read(process.stdout.fileno(), 65536)
                    if not chunk:
                        break
                    buffered += chunk
                    while b"\n" in buffered:
                        line, buffered = buffered.split(b"\n", 1)
                        event = json.loads(line)
                        if event.get("response", {}).get("request_id") == subtype:
                            response = event["response"]
                if response is None or response.get("subtype") != "success":
                    raise ValueError(f"Claude {subtype} failed; check the installed SDK protocol")
                responses.append(response["response"])
            return responses
        finally:
            stop(process)
            selector.close()
            process.stdin.close()
            process.stdout.close()


def capture(arm, binary, host):
    captured, release = threading.Event(), threading.Event()
    requests = []

    class Sink(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            requests.append({"path": self.path, "body": json.loads(self.rfile.read(int(self.headers["Content-Length"])))})
            captured.set()
            release.wait(timeout=25)  # Keep the request pending until the client has been stopped.

        def do_GET(self):
            self.send_response(404)
            self.end_headers()

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Sink)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_address[1]}"
    env = environment(arm, host)
    if host == "codex":
        with (arm.config / "config.toml").open("a") as output:
            output.write(f'\n[model_providers.local_capture]\nname = "Local capture"\nbase_url = "{url}/v1"\n'
                         'wire_api = "responses"\nrequires_openai_auth = false\nrequest_max_retries = 0\nstream_max_retries = 0\n')
        argv = [binary, "exec", "--json", "--skip-git-repo-check", "--ignore-rules", "--color", "never",
                "-c", 'model_provider="local_capture"', "-c", 'model="local-proof-unknown"', "Reply OK."]
    else:
        env.update(ANTHROPIC_BASE_URL=url, ANTHROPIC_API_KEY="local-capture-not-a-secret", DISABLE_DOCTOR_COMMAND="1")
        argv = [binary, "-p", "--verbose", "--output-format", "stream-json", "--no-session-persistence",
                "--setting-sources", "user", "--settings", str(arm.config / "settings.json"),
                "--strict-mcp-config", "--mcp-config", str(arm.base / "mcp.json"), "--no-chrome", "--tools", "Skill",
                "--model", "haiku", "Reply OK."]
    try:
        with (arm.evidence / "capture-stdout").open("wb") as stdout, (arm.evidence / "capture-stderr").open("wb") as stderr:
            process = subprocess.Popen(argv, cwd=arm.work, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
            try:
                if not captured.wait(timeout=20):
                    raise ValueError(f"{host}: no loopback request; inspect host compatibility before retrying")
            finally:
                stop(process)
        if len(requests) != 1:
            raise ValueError("expected one pending loopback request; no measurement was accepted")
        return requests[0]
    finally:
        release.set()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, choices=["codex", "claude"])
    parser.add_argument("--role", default="agent-orchestrator")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="source distribution containing the requested role and its generated profile")
    parser.add_argument("--mode", choices=["copy", "symlink"], default="copy")
    parser.add_argument("--extra-skill", type=Path, action="append", default=[])
    parser.add_argument("--plugin-root", type=Path, action="append", default=[])
    parser.add_argument("--placeholders", type=int, choices=[0, 30], default=0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binary = shutil.which(args.host)
    if not binary:
        parser.error(f"{args.host} is not installed; install the host CLI first")
    tools_root = Path(__file__).resolve().parent.parent
    repo = args.root.expanduser().resolve()
    profile_file = repo / "catalog/profiles" / f"{args.role}.txt"
    if not profile_file.is_file():
        parser.error(f"{profile_file} is missing; pass --root DIR with this role and run scripts/build-profiles.py there first")
    managed_sources(args.host)
    with tempfile.TemporaryDirectory(prefix="fleet-discovery-") as temporary:
        base = Path(temporary).resolve()
        home = base / "home"
        config = home / (".codex" if args.host == "codex" else ".claude")
        for path in [base / "work", config / "skills", base / "tmp", base / "evidence"]:
            path.mkdir(parents=True, mode=0o700)
        arm = Arm("proof", base, base / "work", home, config, base / "evidence", [], [], {}, {})
        configure(arm, args.host)
        if args.host == "claude":
            arm.settings.update(disableBundledSkills=True, skillOverrides={"plugin-authoring": "off"})
            (config / "settings.json").write_text(json.dumps(arm.settings))
        env = environment(arm, args.host)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        argv = [sys.executable, str(tools_root / "scripts/install-skills.py"), "--root", str(repo),
                "--target", str(config / "skills"), "--mode", args.mode, "--apply", args.role]
        installed = subprocess.run(argv, cwd=arm.work, env=env, capture_output=True, text=True, timeout=20)
        if installed.returncode:
            raise ValueError(installed.stderr)
        profile = sorted(path.name for path in (config / "skills").iterdir() if path.name != ".skills-installer.json")
        expected = sorted(line for line in profile_file.read_text().splitlines() if line and not line.startswith("#"))
        if profile != expected:
            raise ValueError("installer output differs from the generated profile; rebuild the profile first")
        copied_bytes_match = all((config / "skills" / name / "SKILL.md").read_bytes()
                                 == (repo / "skills" / name / "SKILL.md").read_bytes() for name in profile)
        extra = sorted(set(args.extra_skill).union(*(plugin_skills(root) for root in args.plugin_root)))
        source_files = []
        for source in extra:
            data = read_frontmatter(source)
            source_files.append({"name": data["name"], "path": str(source.resolve()),
                                 "description_chars": len(data["description"]),
                                 "sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
            destination = config / "skills" / data["name"]
            replay_metadata(source, destination)
        for index in range(args.placeholders):
            name = f"placeholder-{index + 1:02}"
            description = (f"Review specialty {index + 1:02} requirements, compare implementation choices, identify concrete risks, "
                           "and return a tested recommendation with source evidence. Use when the user asks for this specialty, "
                           "a focused review, or an implementation plan that needs its domain checks and acceptance criteria.")
            destination = config / "skills" / name
            destination.mkdir()
            (destination / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {description}\n---\n\nReturn a checked recommendation.\n")
        sources = {read_frontmatter(path)["name"]: read_frontmatter(path) for path in sorted((config / "skills").glob("*/SKILL.md"))}
        implicit = {}
        for name in sources:
            policy = config / "skills" / name / "agents/openai.yaml"
            data = yaml.safe_load(policy.read_text()) if policy.is_file() else {}
            implicit[name] = (data or {}).get("policy", {}).get("allow_implicit_invocation", True)
        arm.inventory = [{"name": name, "path": str((config / "skills" / name / "SKILL.md").resolve())} for name in sources]
        version = subprocess.run([binary, "--version"], cwd=arm.work, env=env, capture_output=True, text=True, timeout=15).stdout.strip()
        if args.host == "codex":
            response = codex_inventory(arm, binary)
            discovered = response["data"][0]["skills"]
            context = None
        else:
            response, context = claude_inventory(arm, binary)
            discovered = [row for row in response["commands"] if not row.get("builtin")]
        if not extra and not args.placeholders and {row["name"] for row in discovered} != set(profile):
            raise ValueError("host discovery differs from the installed profile")
        discovery_states = {}
        for row in discovered:
            description = row.get("description", "")
            if args.host == "claude":
                description = description.removesuffix(" (user)")
            discovery_states[row["name"]] = description_state(description, sources.get(row["name"], {}).get("description", ""))
        request = capture(arm, binary, args.host)
        rendered = listing(request["body"], args.host)
        normalized = rendered.replace(str(home), "$HOME").replace(str(repo), "$REPO")
        states = description_states(rendered, sources, args.host)
        result = {"host": args.host, "version": version, "mode": args.mode, "profile": profile,
                  "source_count": len(sources), "discovered_count": len(discovered), "discovered": discovered,
                  "discovery_description_states": discovery_states, "profile_bytes_match": copied_bytes_match,
                  "source_files": source_files,
                  "sources": [{"name": name, "description_chars": len(data["description"]),
                               "manual_only": data.get("disable-model-invocation", False),
                               "allow_implicit_invocation": implicit[name]} for name, data in sources.items()],
                  "rendered_chars": len(rendered), "normalized_chars": len(normalized),
                  "estimated_tokens": math.ceil(len(normalized) / 4), "states": states,
                  "listing_sha256": hashlib.sha256(normalized.encode()).hexdigest(), "listing": normalized,
                  "request_path": request["path"], "loopback_requests": 1, "model_inferences": 0,
                  "installer_stdout": installed.stdout, "installer_cwd_outside_checkout": not arm.work.is_relative_to(repo),
                  "profile_symlinks": sum((config / "skills" / name).is_symlink() for name in profile),
                  "claude_context": None if context is None else {key: context.get(key) for key in ["model", "maxTokens", "skills", "apiUsage"]}}
        encoded = json.dumps(result, indent=2).replace(str(home), "$HOME").replace(str(repo), "$REPO").replace(str(base), "$CASE")
        args.output.write_text(encoded + "\n")
        print(json.dumps({key: result[key] for key in ["host", "version", "source_count", "discovered_count", "normalized_chars", "estimated_tokens", "profile_symlinks"]}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, InvalidComparison, subprocess.SubprocessError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
