"""Minimal personal/project Claude settings adapter, outside installed skill content."""

import copy
import hashlib
import json
import mmap
import os
import re
import shutil
import subprocess
from pathlib import Path

STATES = {"on", "name-only", "user-invocable-only", "off"}


def load_json(path: Path) -> dict:
    """Reject duplicate keys and non-JSON constants instead of losing user settings."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"{path}: duplicate JSON key {key}; repair settings before retrying")
            result[key] = value
        return result
    def invalid(value):
        raise ValueError(f"{path}: invalid JSON constant {value}")
    if path.is_symlink():
        raise ValueError(f"{path}: settings/state symlink; select a regular owned target")
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_constant=invalid)
    except (OSError, ValueError) as error:
        raise ValueError(f"{path}: malformed settings/state; repair it before retrying ({error})") from error
    if not isinstance(data, dict):
        raise ValueError(f"{path}: settings/state must be a JSON object")
    return data


def support(binary: str) -> dict:
    """Inspect the installed native bundle's settings enum without a model session.

    Deliberately fails closed on wrappers/unsupported packaging; no inferred
    support from the version number or from current online documentation.
    """
    executable = shutil.which(binary)
    if not executable:
        raise ValueError(f"Claude executable {binary} not found; pass --claude-bin for the installed native CLI")
    path = Path(executable).resolve()
    with path.open("rb") as stream:
        if path.stat().st_size == 0:
            raise ValueError("Claude skillOverrides support not found in the installed bundle")
        with mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
            # Match the settings schema itself, not unrelated UI strings.
            match = re.search(rb'\bskillOverrides\s*:\s*[^\n]{0,160}?\(\["on","name-only","user-invocable-only","off"\]\)', data)
            if not match:
                raise ValueError("Claude skillOverrides support not found in the installed native settings schema; use a supported native CLI")
            schema_hash = hashlib.sha256(match[0]).hexdigest()
    result = subprocess.run([str(path), "--version"], capture_output=True, text=True, timeout=15)
    version = result.stdout.strip()
    if result.returncode or not re.fullmatch(r"\d+\.\d+\.\d+(?:[^\n]*) \(Claude Code\)", version):
        raise ValueError("installed Claude version could not be verified; no settings were changed")
    return {"executable": str(path), "version": version, "settings_enum_sha256": schema_hash}


def plan(repo, names: list[str], target: Path, settings: Path, scope: str,
         project: Path, binary: str) -> dict:
    config = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude"))).expanduser().resolve()
    project = project.resolve()
    # This minimal adapter supports the main checkout root or a non-Git project.
    # Claude can read local settings from the main checkout for linked worktrees.
    for ancestor in (project, *project.parents):
        marker = ancestor / ".git"
        if marker.exists() or marker.is_symlink():
            if ancestor != project or marker.is_symlink() or not marker.is_dir():
                raise ValueError("Claude settings in linked Git worktrees, separate Git directories or repository subdirectories are unsupported; use the main checkout root or a standalone project")
            break
    project_config = project / ".claude"
    layers = [config / "settings.json", project_config / "settings.json", project_config / "settings.local.json"]
    if len(set(layers)) != 3:
        raise ValueError("Claude user and project settings overlap; choose a separate project root")
    index = ("user", "project", "local").index(scope)
    if settings != layers[index] or target != (config if index == 0 else project_config) / "skills":
        raise ValueError(f"Claude {scope} scope needs --settings {layers[index]} and --target {(config if index == 0 else project_config) / 'skills'}")
    state_path = settings.with_name(settings.name + ".skills-installer.json")
    snapshots = {path: path.read_bytes() if path.exists() else None for path in [*layers, state_path]}
    documents = [load_json(path) for path in layers]
    original = copy.deepcopy(documents[index])
    for path, data in zip(layers, documents):
        overrides = data.get("skillOverrides", {})
        if not isinstance(overrides, dict) or any(not isinstance(key, str) or not isinstance(value, str) or value not in STATES for key, value in overrides.items()):
            raise ValueError(f"{path}: skillOverrides must map skill names to on/name-only/user-invocable-only/off; repair it before retrying")
    state = load_json(state_path)
    if any((path.read_bytes() if path.exists() else None) != before for path, before in snapshots.items()):
        raise ValueError("Claude settings changed while being read; rerun the preview")
    if state and (set(state) != {"version", "overrides"} or state["version"] != 1 or not isinstance(state["overrides"], dict)):
        raise ValueError(f"{state_path}: invalid ownership state; reconcile it before retrying")
    owned = copy.deepcopy(state.get("overrides", {}))
    for name, record in owned.items():
        if (not isinstance(record, dict) or set(record) != {"written", "previous"}
                or record["written"] != "user-invocable-only"
                or record["previous"] not in (None, "on", "name-only")):
            raise ValueError(f"{state_path}: invalid override ownership for {name}")
    data = copy.deepcopy(documents[index])
    overrides = data.get("skillOverrides", {}).copy()
    before = overrides.copy()
    for name in names:
        current = overrides.get(name)
        record = owned.get(name)
        if record and current != record["written"]:
            # A user edit ends our ownership. Never undo it on a later mode change.
            owned.pop(name)
            record = None
        if repo.invocation(name) == "model":
            if record:
                previous = record["previous"]
                lower = next((document.get("skillOverrides", {}).get(name) for document in reversed(documents[:index]) if name in document.get("skillOverrides", {})), None)
                if lower == "off":
                    previous = None
                if previous is None:
                    overrides.pop(name, None)
                else:
                    overrides[name] = previous
                owned.pop(name)
            continue
        values = [document.get("skillOverrides", {}).get(name) for document in documents]
        higher = next((value for value in reversed(values[index + 1:]) if value is not None), None)
        if higher in ("on", "name-only"):
            raise ValueError(f"{name}: a higher-precedence Claude settings file exposes this user entry; preview/apply at that scope instead")
        # Recheck disabled lower settings before accepting an existing override.
        lower = next((value for value in reversed(values[:index]) if value is not None), None)
        if lower == "off":
            effective = higher if higher is not None else current
            if effective not in (None, "off"):
                raise ValueError(f"{name}: this scope would relax a lower disabled setting; reconcile it explicitly")
            continue
        if current in ("off", "user-invocable-only") or higher in ("off", "user-invocable-only"):
            continue
        owned.setdefault(name, {"written": "user-invocable-only", "previous": current})
        overrides[name] = "user-invocable-only"
    if overrides:
        data["skillOverrides"] = overrides
    elif "skillOverrides" in data:
        # Keep the original empty mapping; remove only entries, not unrelated keys.
        data["skillOverrides"] = {}
    documents[index] = data
    effective = {}
    for document in documents:
        effective.update(document.get("skillOverrides", {}))
    for name in names:
        if repo.invocation(name) == "user" and effective.get(name) not in ("user-invocable-only", "off"):
            raise ValueError(f"{name}: effective settings would expose a user entry; choose the effective settings target")
    checked = support(binary)
    new_state = {"version": 1, "overrides": owned}
    changes = [{"skill": name, "before": before.get(name), "after": overrides.get(name)}
               for name in sorted(set(before) | set(overrides)) if before.get(name) != overrides.get(name)]
    return {"snapshots": snapshots, "path": settings, "data": data, "changed": data != original,
            "state_path": state_path, "state": new_state,
            "state_changed": bool(owned or state) and new_state != state,
            "preview": {"target": str(settings), "scope": scope, "support": checked,
                        "changes": changes, "effective": {name: effective.get(name, "on") for name in names}}}
