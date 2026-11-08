"""Headless host adapters. Authentication stays in temporary, private files."""

import json
import os
import selectors
import shlex
import signal
import subprocess
import time
from pathlib import Path

from .isolation import Arm, InvalidComparison, manifest


def environment(arm: Arm, host: str) -> dict[str, str]:
    # Start from an allowlist, so inherited plugins, host session IDs, provider
    # endpoints, shell startup files, and API credentials cannot change an arm.
    result = {key: os.environ[key] for key in ("PATH", "LANG", "LC_ALL", "TZ", "SSL_CERT_FILE", "SSL_CERT_DIR") if key in os.environ}
    result.update({"HOME": str(arm.home), "TMPDIR": str(arm.base / "tmp"), "XDG_CONFIG_HOME": str(arm.home / ".config"), "XDG_CACHE_HOME": str(arm.home / ".cache"), "SHELL": "/bin/sh", "NO_COLOR": "1"})
    if host == "claude":
        result.update({"CLAUDE_CONFIG_DIR": str(arm.config), "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_TELEMETRY": "1", "DISABLE_ERROR_REPORTING": "1"})
    else:
        result["CODEX_HOME"] = str(arm.config)
    return result


def configure(arm: Arm, host: str) -> None:
    if host == "claude":
        arm.settings = {
            "disableAllHooks": True, "autoMemoryEnabled": False,
            "syncClaudeAiSkills": False, "syncClaudeAiPlugins": False,
            "disableClaudeAiConnectors": True, "enabledPlugins": {},
            "permissions": {"allow": ["Read", "Glob", "Grep", "Skill", "Edit", "Write", "Bash"], "deny": ["Agent", "WebFetch", "WebSearch"], "blockReadsOutsideWorkingDirectories": True},
            "sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True, "allowUnsandboxedCommands": False, "network": {"allowedDomains": []}},
        }
        (arm.config / "settings.json").write_text(json.dumps(arm.settings, indent=2) + "\n", encoding="utf-8")
        (arm.base / "mcp.json").write_text('{"mcpServers": {}}\n', encoding="utf-8")
    else:
        arm.settings = {"approval_policy": "never", "sandbox_mode": "workspace-write", "web_search": "disabled", "cli_auth_credentials_store": "file", "skills.bundled.enabled": False, "features": {name: False for name in ("multi_agent", "plugins", "remote_plugin", "apps", "memories", "hooks", "shell_snapshot")}, "sandbox_workspace_write.network_access": False, "shell_environment_policy.inherit": "none"}
        lines = ['approval_policy = "never"', 'sandbox_mode = "workspace-write"', 'web_search = "disabled"', 'cli_auth_credentials_store = "file"', '[skills.bundled]', 'enabled = false', '[features]']
        lines.extend(f'{key} = false' for key in arm.settings["features"])
        lines.extend(['[sandbox_workspace_write]', 'network_access = false', '[shell_environment_policy]', 'inherit = "none"', '[shell_environment_policy.set]', f'PATH = {json.dumps(os.environ.get("PATH", "/usr/bin:/bin"))}', f'HOME = {json.dumps(str(arm.home))}'])
        (arm.config / "config.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def credentials(arm: Arm, host: str) -> list[bytes]:
    """Copy only authentication, never personal settings, skills, or plugins."""
    if host == "codex":
        original = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "auth.json"
        if not original.is_file():
            raise InvalidComparison("Codex auth.json is unavailable; run codex login before a real evaluation")
        raw = original.read_bytes()
        destination = arm.config / "auth.json"
    else:
        original = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude"))) / ".credentials.json"
        if original.is_file():
            raw = original.read_bytes()
        elif os.uname().sysname == "Darwin":
            value = subprocess.run(["/usr/bin/security", "find-generic-password", "-s", "Claude Code-credentials", "-w"], capture_output=True, timeout=15)
            if value.returncode:
                raise InvalidComparison("Claude credentials are unavailable; run claude auth login before a real evaluation")
            raw = value.stdout.strip()
        else:
            raise InvalidComparison("Claude credential file is unavailable; run claude auth login before a real evaluation")
        destination = arm.config / ".credentials.json"
    try:
        data = json.loads(raw)
    except ValueError as error:
        raise InvalidComparison("the host credential store is not JSON; log in with the supported CLI") from error
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as output:
        output.write(raw)
    tokens = []
    def collect(value, key=""):
        if isinstance(value, dict):
            for name, child in value.items():
                collect(child, name)
        elif isinstance(value, str) and len(value) > 20 and any(part in key.lower() for part in ("token", "key", "secret")):
            tokens.append(value.encode())
    collect(data)
    return tokens


def version(binary: str, host: str) -> str:
    result = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=15)
    if result.returncode:
        raise InvalidComparison(f"{host} --version failed; install the supported host CLI")
    help_command = [binary, "exec", "--help"] if host == "codex" else [binary, "--help"]
    help_result = subprocess.run(help_command, capture_output=True, text=True, timeout=15)
    required = (["--json", "--skip-git-repo-check", "--ignore-rules"] if host == "codex" else ["--setting-sources", "--strict-mcp-config", "--output-format", "--no-session-persistence"])
    if help_result.returncode or any(flag not in help_result.stdout for flag in required):
        raise InvalidComparison(f"{host} lacks required isolation/trace flags; use a CLI that supports {', '.join(required)}")
    return result.stdout.strip()


def command(arm: Arm, host: str, binary: str, model: str | None) -> list[str]:
    if host == "claude":
        result = [binary, "-p", "--verbose", "--output-format", "stream-json", "--no-session-persistence", "--setting-sources", "user", "--settings", str(arm.config / "settings.json"), "--strict-mcp-config", "--mcp-config", str(arm.base / "mcp.json"), "--no-chrome", "--permission-mode", "dontAsk", "--tools", "Read,Glob,Grep,Skill,Edit,Write,Bash", "--add-dir", str(arm.config / "skills")]
    else:
        result = [binary, "exec", "--strict-config", "--json", "--skip-git-repo-check", "--ignore-rules", "--color", "never", "--cd", str(arm.work)]
    if model:
        result.extend(["--model", model])
    result.append("-" if host == "codex" else "")
    if host == "claude":
        result.pop()  # Claude reads the prompt from stdin when no argument is set.
    return result


def codex_inventory(arm: Arm, binary: str) -> dict:
    """Use the host's own discovery API without creating a thread/model turn."""
    process = subprocess.Popen([binary, "app-server"], cwd=arm.work, env=environment(arm, "codex"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    buffered = b""
    responses = {}
    def send(value):
        process.stdin.write(json.dumps(value).encode() + b"\n")
        process.stdin.flush()
    def receive(identifier):
        nonlocal buffered
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            while b"\n" in buffered:
                line, buffered = buffered.split(b"\n", 1)
                try:
                    value = json.loads(line)
                except ValueError:
                    continue
                if "id" in value:
                    responses[value["id"]] = value
            if identifier in responses:
                value = responses[identifier]
                if "error" in value:
                    raise InvalidComparison("Codex skills/list failed; update the adapter to the installed app-server schema")
                return value["result"]
            if selector.select(timeout=min(1, max(0, deadline - time.monotonic()))):
                chunk = os.read(process.stdout.fileno(), 65536)
                if not chunk:
                    break
                buffered += chunk
        raise InvalidComparison("Codex discovery timed out; check that codex app-server supports skills/list")
    try:
        send({"id": 0, "method": "initialize", "params": {"clientInfo": {"name": "skill_eval_harness", "version": "1.0.0"}}})
        receive(0)
        send({"method": "initialized", "params": {}})
        send({"id": 1, "method": "skills/list", "params": {"cwds": [str(arm.work)], "forceReload": True}})
        result = receive(1)
        rows = result.get("data", [])
        if len(rows) != 1 or rows[0].get("errors"):
            raise InvalidComparison("Codex returned incomplete skill discovery; fix every discovery error before evaluating")
        enabled = rows[0].get("skills", [])
        expected = {(entry["name"], entry["path"]) for entry in arm.inventory if ".claude/skills/" not in entry["path"]}
        observed = {(entry["name"], entry.get("path")) for entry in enabled if entry.get("enabled", True)}
        if observed != expected:
            raise InvalidComparison(f"Codex effective inventory differs: expected {sorted(expected)}, observed {sorted(observed)}; an uncontrolled source is enabled")
        return result
    finally:
        selector.close()
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        process.stdin.close()
        process.stdout.close()


def execute(arm: Arm, host: str, argv: list[str], prompt: str, timeout: int) -> dict:
    start = time.monotonic()
    with (arm.evidence / "trace.jsonl").open("wb") as stdout, (arm.evidence / "stderr.txt").open("wb") as stderr:
        process = subprocess.Popen(argv, cwd=arm.work, env=environment(arm, host), stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, start_new_session=True)
        timed_out = False
        try:
            process.communicate(prompt.encode(), timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
    return {"exit_code": process.returncode, "timed_out": timed_out, "seconds": round(time.monotonic() - start, 3)}


def events(path: Path) -> list[dict]:
    result = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except ValueError as error:
            raise InvalidComparison(f"{path.name} has a non-JSON trace line; update the host adapter") from error
        if not isinstance(value, dict):
            raise InvalidComparison("host trace contains a non-object event; update the host adapter")
        result.append(value)
    return result


def body_read(command_text: str, path: str) -> bool:
    """Recognize a body read in a simple command or successful && chain.

    Pipelines, redirections, conditional branches, and shell substitution need
    manual trace review; a compound command's exit code cannot prove their reads.
    """
    try:
        tokens = shlex.split(command_text)
        if tokens and Path(tokens[0]).name in ("sh", "bash", "zsh", "dash"):
            index = next((i for i in (1, 2) if i < len(tokens) and tokens[i] in ("-c", "-lc")), None)
            if index is None or index + 1 >= len(tokens):
                return False
            command_text = tokens[index + 1]
        if "$(" in command_text or "`" in command_text:
            return False
        lexer = shlex.shlex(command_text, posix=True, punctuation_chars=";&|()<>")
        lexer.whitespace_split = True
        segments = [[]]
        for token in lexer:
            if token and all(character in ";&|()<>" for character in token):
                if token != "&&" or not segments[-1]:
                    return False
                segments.append([])
            else:
                segments[-1].append(token)
        for segment in segments:
            if segment[:1] == ["command"]:
                segment = segment[1:]
            if segment and Path(segment[0]).name in ("cat", "sed", "head", "tail", "more", "less") and path in segment[1:]:
                return True
        return False
    except ValueError:
        return False


def body_in_output(path: str, output: str) -> bool:
    """Require visible skill-body text, not output from another command."""
    text = Path(path).read_text(encoding="utf-8")
    parts = text.split("\n---\n", 1)
    body = parts[1] if text.startswith("---\n") and len(parts) == 2 else text
    return any(len(line.strip()) >= 12 and line.strip() in output for line in body.splitlines())


def observe(arm: Arm, host: str, candidate: str) -> dict:
    trace = events(arm.evidence / "trace.jsonl")
    activation = []
    tool_count, messages, models, sessions = 0, [], set(), set()
    inventory_result = None
    usage = {}
    finished = False
    candidate_path = str(arm.config / "skills" / candidate / "SKILL.md")
    if host == "claude":
        successful_tools = {
            item.get("tool_use_id")
            for event in trace if event.get("type") == "user"
            for item in event.get("message", {}).get("content", [])
            if isinstance(item, dict) and item.get("type") == "tool_result" and not item.get("is_error")
        }
        for event in trace:
            if event.get("type") == "system" and event.get("subtype") == "init":
                inventory_result = {key: event.get(key) for key in ("skills", "plugins", "mcp_servers", "tools", "model", "session_id")}
                models.add(event.get("model", "unknown"))
                sessions.add(event.get("session_id", "unknown"))
                external_plugins = [plugin for plugin in event.get("plugins", []) if plugin.get("path") != "builtin" or not plugin.get("source", "").endswith("@builtin")]
                if external_plugins or event.get("mcp_servers"):
                    raise InvalidComparison("Claude loaded plugins or MCP servers; comparison is invalid")
                present = candidate in (event.get("skills") or [])
                if present != (arm.name == "treatment"):
                    raise InvalidComparison(f"Claude {arm.name} init inventory does not prove candidate availability")
            if event.get("type") == "assistant":
                for item in event.get("message", {}).get("content", []):
                    if item.get("type") == "tool_use":
                        tool_count += 1
                        values = item.get("input", {})
                        skill = values.get("skill", "")
                        if item.get("name") == "Skill" and skill.split(":")[-1] == candidate and item.get("id") in successful_tools:
                            activation.append({"event": "Skill", "tool_use_id": item.get("id"), "input": values})
                        elif item.get("name") == "Read" and values.get("file_path") == candidate_path and item.get("id") in successful_tools:
                            activation.append({"event": "Read", "tool_use_id": item.get("id"), "path": candidate_path})
                    elif item.get("type") == "text":
                        messages.append(item.get("text", ""))
            if event.get("type") == "result":
                finished = event.get("subtype") == "success" and not event.get("is_error")
                usage = {key: event.get(key) for key in ("usage", "modelUsage", "total_cost_usd", "num_turns", "duration_ms")}
                if event.get("result"):
                    messages = [event["result"]]
        if inventory_result is None:
            raise InvalidComparison("Claude trace lacks system.init; effective inventory cannot be verified")
    else:
        for event in trace:
            if event.get("type") == "thread.started":
                sessions.add(event.get("thread_id", "unknown"))
            item = event.get("item", {})
            if event.get("type") == "item.completed" and item.get("type") == "command_execution":
                tool_count += 1
                text = item.get("command", "")
                # A mention in prose or a grep result is not a skill activation.
                # Codex has no Skill tool: require a successful body read command.
                if (item.get("exit_code") == 0 and item.get("aggregated_output") and body_read(text, candidate_path)
                        and body_in_output(candidate_path, item["aggregated_output"])):
                    activation.append({"event": "command_execution", "id": item.get("id"), "command": text})
            if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                messages.append(item.get("text", ""))
            if event.get("type") == "turn.completed":
                finished = True
                usage = event.get("usage", {})
        # The local rollout is retained only as evidence, never the auth store.
        for path in (arm.config / "sessions").rglob("*.jsonl"):
            for event in events(path):
                if event.get("type") == "turn_context":
                    model = event.get("payload", {}).get("model")
                    if model:
                        models.add(model)
            (arm.evidence / "session.jsonl").write_bytes(path.read_bytes())
        if not models:
            raise InvalidComparison("Codex rollout lacks the effective model; the comparison cannot verify model parity")
    if not finished:
        raise InvalidComparison(f"{host} {arm.name} did not emit a successful completion")
    return {"activation": bool(activation), "activation_evidence": activation, "tool_calls": tool_count, "models": sorted(models), "sessions": sorted(sessions), "response": "\n\n".join(messages), "usage": usage, "effective_inventory": inventory_result}


def safe_value(value, tokens: list[bytes]) -> None:
    """Check shared record fields as well as each arm's retained files."""
    if isinstance(value, str):
        if any(token in value.encode() for token in tokens):
            raise InvalidComparison("credential material appeared in evidence; evidence is withheld and the temporary environment will be deleted")
    elif isinstance(value, dict):
        for key, child in value.items():
            safe_value(key, tokens)
            safe_value(child, tokens)
    elif isinstance(value, (list, tuple)):
        for child in value:
            safe_value(child, tokens)


def safe_evidence(directory: Path, tokens: list[bytes]) -> None:
    for relative in manifest(directory):
        raw = (directory / relative).read_bytes()
        if any(token in raw for token in tokens):
            raise InvalidComparison("credential material appeared in evidence; evidence is withheld and the temporary environment will be deleted")
