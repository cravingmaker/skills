#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Preview a named skill/role's required closure; --apply installs it.

Python 3.12+ through uv. Multiple NAMEs, --mode copy|symlink and --force remain
supported. --force updates only an unchanged installation owned by this tool;
foreign/edited destinations always fail. evals/results is excluded from copies.
Claude requires explicit settings, scope and project targets. Settings live
outside copied content. --help never inspects a host or writes. No prompts.
JSON on stdout (plan, installed names, upstream prerequisites); diagnostics on
stderr. Exit: 0 success/preview, 1 findings/conflicts or input errors, 2 usage.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import claudesettings
import hostconfig
import skillcatalog
import yaml


STATE = ".skills-installer.json"


def parse(arguments: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy")
    parser.add_argument("--force", action="store_true", help="update unchanged destinations previously owned by this installer")
    parser.add_argument("--apply", action="store_true", help="apply this invocation's previewed changes")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--host", choices=("codex", "claude"), help="enable the explicit host adapter")
    parser.add_argument("--settings", type=Path, help="actual Claude settings file to preview/apply")
    parser.add_argument("--settings-scope", choices=("user", "project", "local"))
    parser.add_argument("--project-root", type=Path, help="Claude project whose settings precedence to inspect")
    parser.add_argument("--claude-bin", default="claude", help="installed native CLI to check without a model call")
    parser.add_argument("names", nargs="+")
    options = parser.parse_args(arguments)
    if options.host == "claude" and not all((options.settings, options.settings_scope, options.project_root)):
        parser.error("--host claude requires --settings, --settings-scope and --project-root")
    if options.host != "claude" and any((options.settings, options.settings_scope, options.project_root)):
        parser.error("settings options require explicit --host claude")
    return options


def resolve(repo, names):
    install, external, missing, seen = set(), set(), set(), set()
    pending = list(names)
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        seen.add(name)
        if name in repo.frontmatter:
            if repo.frontmatter[name].get("name") != name or name in repo.reserved:
                raise ValueError(f"{name}: canonical/directory name mismatch or reserved name; fix the catalog before installing")
            install.add(name)
            pending.extend(repo.names(name, "requires"))
        elif name in repo.external:
            external.add(name)
        else:
            missing.add(name)
    return sorted(install), sorted(external), sorted(missing)


def files(directory: Path, *, omit_eval_results: bool = True) -> dict:
    """A source/installed-copy receipt; no source symlinks or special files."""
    result = {}
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory)
        if omit_eval_results and relative.parts[:2] == ("evals", "results"):
            continue
        if path.is_symlink():
            raise ValueError(f"{path}: skill content symlink; use regular source files")
        if path.is_dir():
            result[relative.as_posix() + "/"] = "directory"
        elif path.is_file():
            result[relative.as_posix()] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "executable": bool(path.stat().st_mode & 0o111)}
        else:
            raise ValueError(f"{path}: special skill file; use regular source files")
    return result


def receipt(path: Path) -> dict:
    if path.is_symlink():
        return {"mode": "symlink", "source": str(path.resolve())}
    if not path.is_dir():
        raise ValueError(f"{path}: foreign destination is not a skill directory")
    return {"mode": "copy", "files": files(path, omit_eval_results=False)}


def write_json(path: Path, value: dict) -> None:
    """Replace one regular settings/state document atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=".skills-", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        if path.exists():
            os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def run(options) -> int:
    root = options.root.resolve()
    repo = skillcatalog.load(root)
    install, external, missing = resolve(repo, options.names)
    if missing:
        raise ValueError("; ".join(f"{name} is required but is neither in {root / 'skills'} nor an external skill in the catalog" for name in missing))
    for name in install:
        if repo.invocation(name) not in ("model", "user"):
            raise ValueError(f"{name}: invocation must be model or user")
    if errors := hostconfig.check(repo):
        raise ValueError("; ".join(errors))
    target = options.target.expanduser().resolve()
    sources = [(root / "skills").resolve()]
    for name in install:
        destination = target / name  # Do not follow the destination's own link.
        if any(destination.is_relative_to(source) or source.is_relative_to(destination) for source in sources):
            raise ValueError(f"{destination} overlaps the source skills; choose a target outside the source tree")
    state_path = target / STATE
    state = claudesettings.load_json(state_path)
    if state and (set(state) != {"version", "source", "skills"} or state["version"] != 1 or state["source"] != str(root) or not isinstance(state["skills"], dict)):
        raise ValueError(f"{state_path}: foreign/invalid installer state; reconcile before installing")
    owned = state.get("skills", {}).copy()
    changes, expected = [], {}
    for name in install:
        source, destination = root / "skills" / name, target / name
        source_files = files(source)
        expected[name] = ({"mode": "symlink", "source": str(source)} if options.mode == "symlink" else {"mode": "copy", "files": source_files})
        exists = destination.exists() or destination.is_symlink()
        if exists:
            actual = receipt(destination)
            if name not in owned or actual != owned[name]:
                raise ValueError(f"{destination}: foreign or edited destination conflict; reconcile it explicitly (--force cannot overwrite it)")
            if actual == expected[name]:
                changes.append({"skill": name, "action": "keep", "path": str(destination), "mode": options.mode})
                continue
            if not options.force:
                raise ValueError(f"{destination}: owned installation changed at source; preview with --force to update it")
        changes.append({"skill": name, "action": "replace" if exists else "install", "path": str(destination), "mode": options.mode})
    settings = None
    if options.host == "claude":
        settings = claudesettings.plan(repo, install, target, options.settings.expanduser().absolute(), options.settings_scope, options.project_root.expanduser(), options.claude_bin)
    upstream = []
    for name in external:
        provider = repo.external[name]
        spec = repo.catalog["external"][provider]
        upstream.append({"name": name, "provider": provider, "source": spec.get("source"), "install": spec.get("install")})
    output = {"mode": "apply" if options.apply else "preview", "target": str(target), "changes": changes,
              "prerequisites": upstream, "settings": settings["preview"] if settings else None}
    def check_settings_snapshot():
        if settings:
            for path, before in settings["snapshots"].items():
                if path.is_symlink() or (path.read_bytes() if path.exists() else None) != before:
                    raise ValueError(f"{path}: settings changed after preview; rerun before applying")
    if options.apply:
        check_settings_snapshot()
        # All conflicts/settings/support failures are preflighted before the first write.
        target.mkdir(parents=True, exist_ok=True)
        for change in changes:
            name, destination = change["skill"], Path(change["path"])
            source = root / "skills" / name
            if change["action"] != "keep":
                # Recheck ownership immediately before replacing; never force a late conflict.
                if destination.exists() or destination.is_symlink():
                    if name not in owned or receipt(destination) != owned[name]:
                        raise ValueError(f"{destination}: changed after preview; reconcile before retrying")
                    if destination.is_symlink():
                        destination.unlink()
                    else:
                        shutil.rmtree(destination)
                if options.mode == "symlink":
                    destination.symlink_to(source, target_is_directory=True)
                else:
                    def omit_results(directory, names):
                        return {"results"} if Path(directory) == source / "evals" else set()
                    shutil.copytree(source, destination, ignore=omit_results)
            if receipt(destination) != expected[name] or files(destination) != files(source):
                raise ValueError(f"{destination}: installed tree/required closure verification failed; inspect before retrying")
            owned[name] = expected[name]
        new_state = {"version": 1, "source": str(root), "skills": owned}
        if new_state != state:
            write_json(state_path, new_state)
        if settings:
            check_settings_snapshot()
            if settings["changed"]:
                write_json(settings["path"], settings["data"])
            if settings["state_changed"]:
                write_json(settings["state_path"], settings["state"])
        output["installed"] = install
    print(json.dumps(output, indent=2))
    return 0


def main(arguments):
    options = parse(arguments)
    try:
        return run(options)
    except (OSError, ValueError, yaml.YAMLError, subprocess.TimeoutExpired) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
