"""CLI, paired execution, and reviewable Markdown/JSON evidence records."""

import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import hosts
from .isolation import (InvalidComparison, build_arm, canonical, check_fixture,
                        contract, dependency_sources, digest, examples, manifest,
                        managed_sources, revision, tree_digest, validate_pair)



def _display_path(value: str, root: Path) -> str:
    """Show a path relative to the repository root, so public records never expose a home directory."""
    try:
        return str(Path(value).resolve().relative_to(root))
    except ValueError:
        return Path(value).name

def parse(arguments: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one paired skill example. Dry runs never call a host or read credentials.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--skill", required=True)
    parser.add_argument("--host", required=True, choices=("claude", "codex"))
    parser.add_argument("--example", required=True, help="activation-1, near-miss-1, etc., in evals/examples.md")
    parser.add_argument("--fixture", required=True, type=Path)
    parser.add_argument("--model", help="host model name; omit to use the host default")
    parser.add_argument("--effort", choices=("low", "medium", "high", "max"), help="Claude reasoning effort; omit to use the host default")
    parser.add_argument("--binary", help="host CLI executable; defaults to --host")
    parser.add_argument("--dependency", action="append", default=[], metavar="DIR", help="a local copy of a required external skill; repeat as needed")
    parser.add_argument("--prompt-file", type=Path, help="concrete prompt for an example with placeholder input")
    parser.add_argument("--record-id", help="filename example identifier for a repeated trial; source example is still recorded")
    parser.add_argument("--timeout", type=int, default=300, help="maximum seconds per model run; default 300")
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args(arguments)
    if options.effort and options.host != "claude":
        parser.error("--effort is supported only by the Claude host")
    for value in (options.skill, options.example, options.record_id or options.example):
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
            parser.error("skill, example, and record identifiers must use lowercase letters, digits, and single hyphens")
    if options.timeout <= 0:
        parser.error("--timeout must be positive")
    return options


def json_file(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def isolation_proof(arms: list, seed: Path) -> dict:
    """Exercise actual copies, then restore the first arm before any host starts."""
    before = manifest(seed)
    sentinel = ".eval-first-arm-only"
    if any((arm.work / sentinel).exists() for arm in arms):
        raise InvalidComparison(f"fixture reserves {sentinel}; remove it before evaluation")
    first = arms[0].work / sentinel
    first.write_text("written only by arm 1\n", encoding="utf-8")
    absent = not (arms[1].work / sentinel).exists() and not (seed / sentinel).exists()
    first.unlink()
    if not absent or manifest(seed) != before:
        raise InvalidComparison("arm 1 changed arm 2 or the pristine seed; use independent copies")
    return {"first_arm": arms[0].name, "sentinel": sentinel, "present_in_first_after_write": True, "absent_in_second": absent, "seed_unchanged": manifest(seed) == before, "shared_file_inodes": 0}


def observations(example: dict, observed: dict, arm) -> dict:
    response = observed["response"]
    changed = sorted(path for path, info in manifest(arm.work).items() if arm.input_manifest.get(path) != info)
    removed = sorted(set(arm.input_manifest) - set(manifest(arm.work)))
    expected_activation = example["kind"] == "activation" and arm.name == "treatment"
    result = {
        "activation": {"expected": expected_activation, "observed": observed["activation"], "matches": observed["activation"] == expected_activation},
        "near_miss_behavior": {"expected": "direct answer, no candidate activation or editing pass" if example["kind"] == "near-miss" else "not a near-miss example", "observed": {"response_lines": len(response.strip().splitlines()), "candidate_activation": observed["activation"], "changed_files": changed, "removed_files": removed}},
        "deliverable_correctness": {"expected": example["expected"], "observed": "review response.txt and artifacts; semantic correctness is not automatically graded", "status": "needs review"},
        "unnecessary_workflow_cost": {"expected": "use only the work needed for the example", "observed": {"tool_calls": observed["tool_calls"], "usage": observed["usage"]}, "status": "needs review"},
    }
    if example["prompt"] == "Which command validates this repo?":
        result["deliverable_correctness"]["command_present"] = "./scripts/validate.sh" in response
        result["near_miss_behavior"]["one_line"] = len(response.strip().splitlines()) == 1
    return result


def record(options, data: dict, arms: list, tokens: list[bytes]) -> Path:
    model = data.get("effective_model") or options.model or "default"
    slug = re.sub(r"[^A-Za-z0-9.-]+", "-", model).strip("-.")[:100] or "default"
    date = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    name = f"{date}-{options.host}-{slug}-{options.record_id or options.example}"
    directory = options.root / "skills" / options.skill / "evals/results"
    destination = directory / name
    markdown = directory / f"{name}.md"
    if markdown.exists() or destination.exists():
        raise InvalidComparison(f"{markdown} already exists; choose a new --record-id to preserve earlier evidence")
    # Export only the workspaces and deliberate trace files. Host homes and
    # authentication are never included in the retained evidence tree.
    hosts.safe_value(data, tokens)
    for arm in arms:
        hosts.safe_evidence(arm.evidence, tokens)
        hosts.safe_evidence(arm.work, tokens)
    directory.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    try:
        for arm in arms:
            target = destination / arm.name
            shutil.copytree(arm.evidence, target)
            shutil.copytree(arm.work, target / "artifacts")
        json_file(destination / "comparison.json", data)
        lines = [f"# {options.skill}: {options.host} {options.example}", "", f"Comparison: **{data['status']}**. Host: `{data.get('host_version', 'unavailable')}`. Effective model: `{model}`.", "", "## Inputs", "", f"- **Source example.** `{options.example}` in `evals/examples.md`.", f"- **Skill revision.** Commit `{data['skill_revision']['commit']}`, tree `{data['skill_revision']['tree']}`, actual bytes SHA-256 `{data['skill_revision']['working_tree_sha256']}`; dirty: `{data['skill_revision']['dirty']}`.", f"- **Fixture.** `{_display_path(data['fixture'], options.root)}`, SHA-256 `{data['fixture_sha256']}`.", f"- **Standing contract.** SHA-256 `{data['contract_sha256']}`, identical in both arms.", f"- **Settings.** Requested model `{options.model or 'host default'}`; effort `{options.effort or 'host default'}`; each arm has a new session and the same host settings.", "", "## Prompt", "", "```text", data["prompt"], "```", "", "## Expected and observed", "", "| Arm | Activation expected | Activation observed | Tools | Completion |", "| --- | --- | --- | --- | --- |"]
        for arm in arms:
            info = data["arms"][arm.name]
            observed = info.get("observed", {})
            expected = options.example.startswith("activation-") and arm.name == "treatment"
            lines.append(f"| {arm.name} | {str(expected).lower()} | {str(observed.get('activation', 'unavailable')).lower()} | {observed.get('tool_calls', 'unavailable')} | {info.get('execution', {}).get('exit_code', 'not run')} |")
        lines.append("")
        for arm in arms:
            info = data["arms"][arm.name]
            assessment = info.get("assessment")
            if assessment:
                behavior = assessment["near_miss_behavior"]["observed"]
                command = assessment["deliverable_correctness"].get("command_present", "requires review")
                lines.append(f"{arm.name.capitalize()}: {behavior['response_lines']} response lines; changed files `{', '.join(behavior['changed_files']) or 'none'}`; removed files `{', '.join(behavior['removed_files']) or 'none'}`; validation command present: `{command}`. Workflow cost: {info['execution']['seconds']} seconds and {info['observed']['tool_calls']} tool calls; token usage is in the JSON record.")
                lines.append("")
        lines.extend(["", f"Expected deliverable: {data['expected']}", "", "Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.", "", "## Isolation evidence", "", f"The first arm's sentinel was absent from the second arm: `{data['isolation_proof']['absent_in_second']}`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.", "", "Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.", "", f"Full configuration, input revisions, effective discovery inventory, and expectations: [{name}/comparison.json]({name}/comparison.json).", ""])
        if data.get("errors"):
            lines.extend(["## Invalid comparison", "", *[f"- {error}" for error in data["errors"]], ""])
        for arm in arms:
            lines.extend([f"## {arm.name.capitalize()} evidence", "", f"- [Raw JSON trace]({name}/{arm.name}/trace.jsonl)", f"- [Standard error]({name}/{arm.name}/stderr.txt)", f"- [Observed response]({name}/{arm.name}/response.txt)", f"- [Input and discovery manifest]({name}/{arm.name}/manifest.json)", f"- Artifacts: `{name}/{arm.name}/artifacts/`.", ""])
        rendered = "\n".join(lines)
        hosts.safe_value(rendered, tokens)
        markdown.write_text(rendered, encoding="utf-8")
    except BaseException:
        shutil.rmtree(destination)
        markdown.unlink(missing_ok=True)
        raise
    return markdown


def main(arguments: list[str]) -> int:
    options = parse(arguments)
    options.root = options.root.expanduser().resolve()
    options.fixture = options.fixture.expanduser().resolve()
    try:
        if not options.fixture.is_dir():
            raise InvalidComparison(f"{options.fixture} is not a fixture directory; pass --fixture DIR")
        check_fixture(options.fixture)
        skill_dir = options.root / "skills" / options.skill
        source_examples = examples(skill_dir / "evals/examples.md")
        example = next((value for value in source_examples if value["id"] == options.example), None)
        if example is None:
            raise InvalidComparison(f"unknown example {options.example}; choose one of {', '.join(value['id'] for value in source_examples)}")
        prompt = options.prompt_file.read_text(encoding="utf-8").strip() if options.prompt_file else example["prompt"]
        if not prompt or ("<" in prompt and ">" in prompt):
            raise InvalidComparison("example has empty/placeholder input; supply the concrete prompt using --prompt-file FILE")
        sources = dependency_sources(options.root, options.skill, options.dependency)
        standing = contract(options.root)
        fixture_before = manifest(options.fixture)
        # A long macOS temp path makes Claude's sandbox fall back to a shared TMPDIR.
        temporary_parent = "/tmp" if options.host == "claude" and Path("/tmp").is_dir() else None
        with tempfile.TemporaryDirectory(prefix="" if options.host == "claude" else "eval-skill-", dir=temporary_parent) as temporary:
            base = Path(temporary).resolve()
            seed = base / "seed"
            from .isolation import copy_tree
            copy_tree(options.fixture, seed)
            if manifest(seed) != fixture_before:
                raise InvalidComparison("fixture changed while being captured; retry with a stable fixture")
            frozen_sources = {}
            for name, source in sources.items():
                frozen = base / "skills" / name
                copy_tree(source, frozen, skill=True)
                frozen_sources[name] = frozen
            arms = [build_arm(base / (name[0] if options.host == "claude" else name), options.host, name, seed, frozen_sources, options.skill, standing) for name in ("treatment", "baseline")]
            for arm in arms:
                hosts.configure(arm, options.host)
            validate_pair(arms, options.host, options.skill)
            proof = isolation_proof(arms, seed)
            machine = managed_sources(options.host)
            data = {"schema_version": 1, "status": "dry-run" if options.dry_run else "valid", "host": options.host, "requested_model": options.model or "host default", "requested_effort": options.effort or "host default", "source_example": example, "prompt": prompt, "expected": example["expected"], "fixture": str(options.fixture), "fixture_sha256": tree_digest(fixture_before), "fixture_manifest": fixture_before, "skill_revision": revision(options.root, skill_dir), "input_revisions": {name: revision(options.root, path) if path.is_relative_to(options.root) else {"working_tree_sha256": tree_digest(manifest(path, skill=True))} for name, path in sources.items()}, "skill_input_manifests": {name: manifest(path, skill=True) for name, path in frozen_sources.items()}, "examples_sha256": digest((skill_dir / "evals/examples.md").read_bytes()), "contract_sha256": digest(standing.encode()), "managed_sources": machine, "isolation_proof": proof, "discovery_policy": {"user": "fresh temporary home and host config directory", "project": "all candidate copies removed; every remaining skill inventoried", "ancestors": "reject any discovered ancestor skills", "plugins": "disabled; no inherited settings or extra roots", "managed": "reject local files/MDM; verify runtime inventory", "system": "bundled skills disabled in both hosts; effective runtime inventory checked", "environment": "allowlist only; no inherited provider/session/skill settings"}, "arms": {}, "errors": [], "model_runs_started": 0}
            for arm in arms:
                info = {"inventory": canonical(arm.inventory, arm.base), "excluded_project_candidates": arm.excluded, "input_manifest": arm.input_manifest, "input_sha256": tree_digest(arm.input_manifest), "settings": canonical(arm.settings, arm.base), "environment": canonical(hosts.environment(arm, options.host), arm.base)}
                data["arms"][arm.name] = info
                json_file(arm.evidence / "manifest.json", info)
            if data["arms"]["treatment"]["settings"] != data["arms"]["baseline"]["settings"]:
                raise InvalidComparison("host settings differ across arms; keep model and tool settings constant")
            if options.dry_run:
                print(json.dumps(data, indent=2, sort_keys=True))
                return 0
            binary = shutil.which(options.binary or options.host)
            if not binary:
                raise InvalidComparison(f"{options.host} CLI not found; install it or pass --binary PATH")
            data["host_version"] = hosts.version(binary, options.host)
            token_values = []
            # All preflights precede either model call. A discovery failure costs
            # zero model runs and cannot be mistaken for an eval outcome.
            try:
                for arm in arms:
                    token_values.extend(hosts.credentials(arm, options.host))
                    if options.host == "codex":
                        observed_inventory = hosts.codex_inventory(arm, binary)
                        data["arms"][arm.name]["runtime_inventory"] = canonical(observed_inventory, arm.base)
                        json_file(arm.evidence / "discovery.json", observed_inventory)
                for arm in arms:
                    if manifest(seed) != fixture_before or manifest(arm.work) != arm.input_manifest:
                        raise InvalidComparison(f"{arm.name} input changed after the first arm; comparison is invalid")
                    argv = hosts.command(arm, options.host, binary, options.model, options.effort)
                    data["arms"][arm.name]["argv"] = canonical(argv, arm.base)
                    data["model_runs_started"] += 1
                    execution = hosts.execute(arm, options.host, argv, prompt, options.timeout)
                    data["arms"][arm.name]["execution"] = execution
                    if execution["exit_code"] != 0 or execution["timed_out"]:
                        raise InvalidComparison(f"{options.host} {arm.name} failed (exit {execution['exit_code']}, timeout {execution['timed_out']}); inspect stderr and trace")
                    observed = hosts.observe(arm, options.host, options.skill)
                    data["arms"][arm.name]["observed"] = observed
                    data["arms"][arm.name]["assessment"] = observations(example, observed, arm)
                    (arm.evidence / "response.txt").write_text(observed["response"] + "\n", encoding="utf-8")
                    if arm.name == "baseline" and observed["activation"]:
                        raise InvalidComparison("candidate activated in baseline; the comparison is invalid")
                first, second = [data["arms"][arm.name]["observed"] for arm in arms]
                if first["models"] != second["models"] or len(first["models"]) != 1:
                    raise InvalidComparison("effective models differ across arms; rerun with an explicit --model")
                if set(first["sessions"]) & set(second["sessions"]) or not first["sessions"] or not second["sessions"]:
                    raise InvalidComparison("session IDs do not prove fresh sessions; update the host adapter")
                data["effective_model"] = first["models"][0]
                if options.host == "claude":
                    def constant_inventory(observed):
                        value = dict(observed["effective_inventory"])
                        value["skills"] = sorted(name for name in value["skills"] if name != options.skill)
                        value.pop("session_id", None)
                        return value
                    if constant_inventory(first) != constant_inventory(second):
                        raise InvalidComparison("Claude non-candidate inventory/tools differ between sessions")
            except (InvalidComparison, OSError, subprocess.TimeoutExpired) as error:
                data["status"] = "invalid"
                data["errors"].append(str(error))
            for arm in arms:
                for filename in ("trace.jsonl", "stderr.txt", "response.txt"):
                    (arm.evidence / filename).touch(exist_ok=True)
                json_file(arm.evidence / "manifest.json", data["arms"][arm.name])
            result = record(options, data, arms, token_values)
            print(f"{data['status']}: {result}")
            for error in data["errors"]:
                print(f"error: {error}", file=sys.stderr)
            return 0 if data["status"] == "valid" else 1
    except (InvalidComparison, OSError, ValueError) as error:
        print(f"invalid comparison: {error}", file=sys.stderr)
        return 1
