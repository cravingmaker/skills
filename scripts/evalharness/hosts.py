"""Headless host adapters. Authentication stays in temporary, private files."""

import json
import os
import re
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
        result.update({"CLAUDE_CONFIG_DIR": str(arm.config), "CLAUDE_CODE_TMPDIR": str(arm.base / "tmp"), "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_TELEMETRY": "1", "DISABLE_ERROR_REPORTING": "1"})
    else:
        result["CODEX_HOME"] = str(arm.config)
    return result


def configure(arm: Arm, host: str) -> None:
    if host == "claude":
        arm.settings = {
            "disableAllHooks": True, "autoMemoryEnabled": False,
            "disableBundledSkills": True, "skillOverrides": {"doctor": "off", "plugin-authoring": "off"},
            "syncClaudeAiSkills": False, "syncClaudeAiPlugins": False,
            "disableClaudeAiConnectors": True, "enabledPlugins": {},
            "permissions": {"allow": ["Read", "Glob", "Grep", "Skill", "Edit", "Write", "Bash"], "deny": ["Agent", "WebFetch", "WebSearch", "Skill(plugin-authoring)"], "blockReadsOutsideWorkingDirectories": True},
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


def command(arm: Arm, host: str, binary: str, model: str | None, effort: str | None = None) -> list[str]:
    if host == "claude":
        result = [binary, "-p", "--verbose", "--output-format", "stream-json", "--no-session-persistence", "--setting-sources", "user", "--settings", str(arm.config / "settings.json"), "--strict-mcp-config", "--mcp-config", str(arm.base / "mcp.json"), "--no-chrome", "--permission-mode", "dontAsk", "--tools", "Read,Glob,Grep,Skill,Edit,Write,Bash", "--add-dir", str(arm.config / "skills")]
    else:
        result = [binary, "exec", "--strict-config", "--json", "--skip-git-repo-check", "--ignore-rules", "--color", "never", "--cd", str(arm.work)]
    if host == "claude":
        result.extend(["--input-format", "stream-json", "--replay-user-messages"])
    if model:
        result.extend(["--model", model])
    if host == "claude" and effort:
        result.extend(["--effort", effort])
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
    arm.prompt = prompt
    payload = (json.dumps({"type": "user", "message": {"role": "user", "content": prompt}}) + "\n") if host == "claude" else prompt
    with (arm.evidence / "trace.jsonl").open("wb") as stdout, (arm.evidence / "stderr.txt").open("wb") as stderr:
        process = subprocess.Popen(argv, cwd=arm.work, env=environment(arm, host), stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, start_new_session=True)
        timed_out = False
        try:
            process.communicate(payload.encode(), timeout=timeout)
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


def reader_inputs(command_text: str) -> list[str] | None:
    """Return the input files of one simple read command, or None.

    Compound commands need trace review: their aggregate output cannot establish
    which command supplied the visible body text, even in a successful && chain.
    A reader name alone is not enough either: sed can synthesize text, so only
    options and programs that copy input lines are accepted.
    """
    try:
        tokens = shlex.split(command_text)
        if tokens and Path(tokens[0]).name in ("sh", "bash", "zsh", "dash"):
            # Only this exact form identifies the executed command. Other
            # options, script operands, or outer syntax need trace review.
            if len(tokens) != 3 or tokens[1] not in ("-c", "-lc"):
                return None
            command_text = tokens[2]
        if any(marker in command_text for marker in ("\n", "\r", "$(", "`")):
            return None
        lexer = shlex.shlex(command_text, posix=True, punctuation_chars=";&|()<>")
        lexer.whitespace_split = True
        tokens = list(lexer)
        if any(token and all(character in ";&|()<>" for character in token) for token in tokens):
            return None
        if tokens[:1] == ["command"]:
            tokens = tokens[1:]
        if not tokens:
            return None
        reader, arguments = Path(tokens[0]).name, tokens[1:]
        if reader in ("head", "tail"):
            if arguments[:1] and re.fullmatch(r"-[0-9]+", arguments[0]):
                arguments = arguments[1:]
            elif arguments[:1] in (["-n"], ["-c"]) and len(arguments) > 1 and re.fullmatch(r"[+-]?[0-9]+", arguments[1]):
                arguments = arguments[2:]
        elif reader == "sed":
            if arguments[:1] == ["-n"]:
                arguments = arguments[1:]
            if arguments[:1] == ["-e"]:
                arguments = arguments[1:]
            # Only an optional numeric/$ address range followed by p.
            address = r"(?:[1-9][0-9]*|\$)"
            if not arguments or not re.fullmatch(rf"(?:{address}(?:,{address})?)?p", arguments[0]):
                return None
            arguments = arguments[1:]
        elif reader not in ("cat", "more", "less"):
            return None
        if arguments[:1] == ["--"]:
            arguments = arguments[1:]
        if not arguments or any(argument.startswith("-") for argument in arguments):
            return None
        return arguments
    except ValueError:
        return None


def body_read(command_text: str, path: str) -> bool:
    """Recognize a simple read command whose inputs include the candidate."""
    inputs = reader_inputs(command_text)
    return bool(inputs and path in inputs)


def body_in_output(path: str, output: str, others: tuple[str, ...] = ()) -> bool:
    """Require visible text unique to the candidate body among the read inputs."""
    text = Path(path).read_text(encoding="utf-8")
    parts = text.split("\n---\n", 1)
    body = parts[1] if text.startswith("---\n") and len(parts) == 2 else text
    other_text = "\n".join(Path(other).read_text(encoding="utf-8") for other in others)
    return any(len(line.strip()) >= 12 and line.strip() not in other_text and line.strip() in output for line in body.splitlines())


def listing_cat_inputs(command_text: str, skills: Path) -> list[str] | None:
    """Recognize one or two installed-directory listings followed by a full cat.

    Only unconditional semicolons and stderr-to-stdout redirection are allowed.
    Other compound commands remain unclassified.
    """
    if any(marker in command_text for marker in ("\n", "\r", "$(", "`")):
        return None
    try:
        lexer = shlex.shlex(command_text, posix=True, punctuation_chars=";&|()<>")
        lexer.whitespace_split = True
        lexer.commenters = ""
        commands = [[]]
        for token in lexer:
            if token == ";":
                commands.append([])
            else:
                commands[-1].append(token)
        if len(commands) not in (2, 3):
            return None
        for command in commands:
            if command[-3:] == ["2", ">&", "1"]:
                del command[-3:]
            if len(command) != 2 or not os.path.isabs(command[1]):
                return None
            if os.path.commonpath([os.path.normpath(skills), os.path.normpath(command[1])]) != os.path.normpath(skills):
                return None
        if any(command[0] not in ("ls", "/bin/ls", "/usr/bin/ls") for command in commands[:-1]):
            return None
        return [commands[-1][1]] if commands[-1][0] in ("cat", "/bin/cat", "/usr/bin/cat") else None
    except ValueError:
        return None


def candidate_read(command_text: str, path: str, output: str, skills: Path) -> bool:
    """A read of installed skill files whose output shows the candidate's own body text.

    Several installed skills may be read in one command; every input must be an
    installed skill file, so another file cannot supply the matching text.
    """
    inputs = reader_inputs(command_text)
    listing = False
    if not inputs:
        inputs = listing_cat_inputs(command_text, skills)
        listing = bool(inputs)
    if not inputs or path not in inputs:
        return False
    root = os.path.normpath(skills)
    if any(not os.path.isabs(value) or os.path.commonpath([root, os.path.normpath(value)]) != root or not Path(value).is_file() for value in inputs):
        return False
    if listing:
        text = Path(path).read_text(encoding="utf-8")
        parts = text.split("\n---\n", 1)
        body = parts[1] if text.startswith("---\n") and len(parts) == 2 else text
        # Tool output may be truncated. Require a substantial contiguous body
        # prefix, rather than a filename or one line printed by the listings.
        prefix = body.lstrip()[:512]
        return len(prefix) >= 64 and prefix in output
    return body_in_output(path, output, tuple(value for value in dict.fromkeys(inputs) if value != path))


def selected_skill_injections(rollout: list[dict], candidate_path: str) -> list[dict]:
    """Recognize host-selected instructions, never quoted user/report tags.

    Unknown provenance or schemas stay unclassified. Native provenance, the
    installed path/name and the complete installed body must all agree.
    """
    candidate = Path(candidate_path)
    if not candidate.is_file():
        return []
    expected = candidate.read_text(encoding="utf-8").rstrip("\n")
    pattern = re.compile(
        r"\A<skill>\s*<name>" + re.escape(candidate.parent.name)
        + r"</name>\s*<path>" + re.escape(str(candidate))
        + r"</path>\n(.*)\n</skill>\s*\Z", re.DOTALL)
    found = []
    for event in rollout:
        payload = event.get("payload", {})
        if event.get("type") != "response_item" or not isinstance(payload, dict):
            continue
        if payload.get("type") != "message" or payload.get("role") != "user":
            continue
        metadata = payload.get("internal_chat_message_metadata_passthrough")
        if not isinstance(metadata, dict):
            continue
        kinds = metadata.get("content_item_kinds")
        details = metadata.get("content_item_metadata")
        content = payload.get("content")
        if (not all(isinstance(value, list) for value in (kinds, details, content))
                or not len(kinds) == len(details) == len(content)):
            continue
        for index, part in enumerate(content):
            if not isinstance(part, dict) or part.get("type") != "input_text":
                continue
            detail = details[index]
            provenance = detail.get("provenance") if isinstance(detail, dict) else None
            if (kinds[index] != "skills.selected_skill_instructions"
                    or not isinstance(provenance, dict) or provenance.get("type") != "skills"):
                continue
            value = part.get("text")
            match = pattern.fullmatch(value) if isinstance(value, str) else None
            if match and match[1].rstrip("\n") == expected:
                found.append({"event": "skills.selected_skill_instructions",
                              "message_id": payload.get("id"), "content_index": index,
                              "path": candidate_path})
    return found


def claude_native_selection(event: dict, prompt: str, candidate: str, init: dict) -> bool:
    """Match a host-expanded command replay to the actual slash input and inventory.

    The replay's command tags are host output only when the original input was
    an exact leading slash invocation. Quoted or supplied tags cannot prove it.
    """
    match = re.fullmatch(r"/([a-z0-9-]+)(?:\s+(.*))?", prompt.strip(), re.DOTALL)
    if (not match or match[1] != candidate or event.get("type") != "user"
            or event.get("isReplay") is not True or event.get("parent_tool_use_id") is not None
            or event.get("session_id") != init.get("session_id")
            or candidate not in (init.get("skills") or [])
            or candidate not in (init.get("slash_commands") or [])):
        return False
    message = event.get("message", {})
    if not isinstance(message, dict) or message.get("role") != "user":
        return False
    content = message.get("content")
    header = f"<command-message>{candidate}</command-message>\n<command-name>/{candidate}</command-name>"
    arguments = (match[2] or "").strip()
    expected = header + (f"\n<command-args>{arguments}</command-args>" if arguments else "")
    return isinstance(content, str) and content == expected


def observe(arm: Arm, host: str, candidate: str) -> dict:
    trace = events(arm.evidence / "trace.jsonl")
    activation = []
    tool_count, messages, models, sessions = 0, [], set(), set()
    inventory_result = None
    usage = {}
    finished = False
    candidate_path = str(arm.config / "skills" / candidate / "SKILL.md")
    if host == "claude":
        successful_results = {
            item.get("tool_use_id"): item.get("content", "")
            for event in trace if event.get("type") == "user"
            for item in event.get("message", {}).get("content", [])
            if isinstance(item, dict) and item.get("type") == "tool_result" and not item.get("is_error")
        }
        successful_tools = set(successful_results)
        init = {}
        for event in trace:
            result = event.get("tool_use_result")
            stats = event.get("subagent_stats")
            if ((isinstance(result, dict) and result.get("status") == "forked")
                    or (isinstance(stats, dict) and stats.get("spawned", 0))):
                raise InvalidComparison("Claude started a forked model outside the paired-run budget; disable bundled skills and rerun")
            if event.get("type") == "system" and event.get("subtype") == "init":
                init = event
                inventory_result = {key: event.get(key) for key in ("skills", "plugins", "mcp_servers", "tools", "model", "session_id")}
                models.add(event.get("model", "unknown"))
                sessions.add(event.get("session_id", "unknown"))
                external_plugins = [plugin for plugin in event.get("plugins", []) if plugin.get("path") != "builtin" or not plugin.get("source", "").endswith("@builtin")]
                if external_plugins or event.get("mcp_servers"):
                    raise InvalidComparison("Claude loaded plugins or MCP servers; comparison is invalid")
                present = candidate in (event.get("skills") or [])
                if present != (arm.name == "treatment"):
                    raise InvalidComparison(f"Claude {arm.name} init inventory does not prove candidate availability")
            if (Path(candidate_path).is_file()
                    and claude_native_selection(event, getattr(arm, "prompt", ""), candidate, init)):
                activation.append({"event": "native_command_replay", "path": candidate_path,
                                   "session_id": event.get("session_id")})
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
                        elif item.get("name") == "Bash" and item.get("id") in successful_tools:
                            output = successful_results[item["id"]]
                            if isinstance(output, list):
                                output = "\n".join(part.get("text", "") for part in output
                                                   if isinstance(part, dict) and part.get("type") == "text")
                            if isinstance(output, str) and candidate_read(values.get("command", ""), candidate_path, output, arm.config / "skills"):
                                activation.append({"event": "Bash", "tool_use_id": item.get("id"), "command": values.get("command", "")})
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
                # Classify shell body reads here; native selections come from the rollout below.
                if (item.get("exit_code") == 0 and item.get("aggregated_output")
                        and candidate_read(text, candidate_path, item["aggregated_output"], arm.config / "skills")):
                    activation.append({"event": "command_execution", "id": item.get("id"), "command": text})
            if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                messages.append(item.get("text", ""))
            if event.get("type") == "turn.completed":
                finished = True
                usage = event.get("usage", {})
        # The local rollout is retained only as evidence, never the auth store.
        for path in (arm.config / "sessions").rglob("*.jsonl"):
            rollout = events(path)
            activation.extend(selected_skill_injections(rollout, candidate_path))
            for event in rollout:
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
