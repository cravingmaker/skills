#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Offline regression checks for invariants that determine eval validity."""

import contextlib
import io
import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from evalharness import hosts
from evalharness.isolation import (InvalidComparison, build_arm, check_fixture,
                                   contract, copy_tree, dependency_sources,
                                   examples, inventory, manifest, validate_pair)
from evalharness.runner import isolation_proof, main


class IsolationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="evalharness-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.sources = {"clear-communication": ROOT / "skills/clear-communication"}
        machine = patch("evalharness.runner.managed_sources", return_value=[])
        machine.start()
        self.addCleanup(machine.stop)

    def pair(self, host, project=True):
        seed = self.base / "seed"
        fixture = ROOT / "tests/eval-harness/fixtures" / ("project-installed" if project else "package")
        copy_tree(fixture, seed)
        arms = [build_arm(self.base / name, host, name, seed, self.sources, "clear-communication", contract(ROOT)) for name in ("treatment", "baseline")]
        for arm in arms:
            hosts.configure(arm, host)
        return seed, arms

    def test_project_copies_excluded_for_both_hosts(self):
        for host in ("claude", "codex"):
            with self.subTest(host=host):
                self.base = Path(self.temporary.name).resolve() / host
                seed, arms = self.pair(host)
                validate_pair(arms, host, "clear-communication")
                for arm in arms:
                    self.assertEqual(len(arm.excluded), 2)
                    self.assertFalse((arm.work / ".agents/skills/clear-communication").exists())
                    self.assertFalse((arm.work / ".claude/skills/clear-communication").exists())
                self.assertEqual(arms[0].input_manifest, arms[1].input_manifest)
                print(f"{host}: excluded both project copies; treatment=1 candidate, baseline=0")

    def test_leaked_baseline_candidate_is_rejected_for_both_hosts(self):
        for host in ("claude", "codex"):
            with self.subTest(host=host):
                self.base = Path(self.temporary.name).resolve() / host
                _, arms = self.pair(host)
                copy_tree(self.sources["clear-communication"], arms[1].work / ".agents/skills/leaked-alias", skill=True)
                with self.assertRaisesRegex(InvalidComparison, "baseline candidate inventory has 1"):
                    validate_pair(arms, host, "clear-communication")
                print(f"{host}: rejected a baseline leak whose folder name differs from its skill name")

    def test_first_arm_writes_do_not_reach_second(self):
        seed, arms = self.pair("codex", project=False)
        validate_pair(arms, "codex", "clear-communication")
        self.assertTrue(isolation_proof(arms, seed)["absent_in_second"])
        (arms[0].work / "README.md").write_text("arm 1 overwrote this file\n")
        (arms[0].work / "first-arm.txt").write_text("created in arm 1\n")
        self.assertNotEqual((arms[0].work / "README.md").read_bytes(), (arms[1].work / "README.md").read_bytes())
        self.assertEqual((seed / "README.md").read_bytes(), (arms[1].work / "README.md").read_bytes())
        self.assertFalse((arms[1].work / "first-arm.txt").exists())
        print("arm 1 overwrite and creation: absent from arm 2 and pristine seed")

    def test_real_user_environment_is_not_inherited(self):
        _, arms = self.pair("claude")
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "should-not-inherit", "CLAUDE_PLUGIN_ROOT": "outside", "CODEX_THREAD_ID": "old", "BASH_ENV": "/outside/startup"}):
            result = hosts.environment(arms[0], "claude")
            for name in ("ANTHROPIC_API_KEY", "CLAUDE_PLUGIN_ROOT", "CODEX_THREAD_ID", "BASH_ENV"):
                self.assertNotIn(name, result)
            self.assertEqual(result["HOME"], str(arms[0].home))

    def test_claude_uses_an_arm_private_host_temp_directory(self):
        _, arms = self.pair("claude")
        for arm in arms:
            result = hosts.environment(arm, "claude")
            self.assertEqual(result.get("CLAUDE_CODE_TMPDIR"), str(arm.base / "tmp"))

        built = []
        def capture(*args, **kwargs):
            arm = build_arm(*args, **kwargs)
            built.append(arm)
            return arm
        with patch("evalharness.runner.build_arm", side_effect=capture), contextlib.redirect_stdout(io.StringIO()):
            code = main(["--root", str(ROOT), "--skill", "clear-communication", "--host", "claude",
                         "--example", "near-miss-1", "--fixture", str(ROOT / "tests/eval-harness/fixtures/package"),
                         "--dry-run"])
        self.assertEqual(code, 0)
        self.assertEqual(len(built), 2)
        # Claude falls back to a shared system TMPDIR when the override is long.
        self.assertTrue(all(len(str(arm.base / "tmp" / f"claude-{os.getuid()}").encode()) <= 40 for arm in built))

    def test_uncontrolled_ancestor_is_rejected(self):
        _, arms = self.pair("codex")
        outside = self.base / ".agents/skills/clear-communication"
        copy_tree(self.sources["clear-communication"], outside, skill=True)
        with self.assertRaisesRegex(InvalidComparison, "uncontrolled ancestor"):
            inventory(arms[1], "codex")

    def test_codex_instruction_override_is_rejected(self):
        fixture = self.base / "fixture"
        fixture.mkdir()
        (fixture / "AGENTS.override.md").write_text("Replace the standing contract.\n")
        with self.assertRaisesRegex(InvalidComparison, "host instructions"):
            check_fixture(fixture)

    def test_ancestor_instruction_override_is_rejected(self):
        _, arms = self.pair("codex")
        (self.base / "AGENTS.override.md").write_text("Replace the standing contract.\n")
        with self.assertRaisesRegex(InvalidComparison, "uncontrolled ancestor"):
            inventory(arms[0], "codex")

    def test_symlink_is_rejected(self):
        fixture = self.base / "fixture"
        fixture.mkdir()
        (fixture / "linked").symlink_to(ROOT / "skills/clear-communication")
        with self.assertRaisesRegex(InvalidComparison, "symlink"):
            check_fixture(fixture)

    def test_host_configuration_is_rejected(self):
        fixture = self.base / "fixture"
        (fixture / ".claude").mkdir(parents=True)
        (fixture / ".claude/settings.json").write_text('{"enabledPlugins":{"outside":true}}')
        with self.assertRaisesRegex(InvalidComparison, "only .claude/skills"):
            check_fixture(fixture)

    def test_missing_dependency_fails_before_building(self):
        root = self.base / "repo"
        skill = root / "skills/example"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text('---\nname: example\ndescription: Example\nmetadata:\n  requires: "missing"\n---\n')
        with self.assertRaisesRegex(InvalidComparison, "required skill missing is missing"):
            dependency_sources(root, "example", [])

    def test_mutually_required_skills_resolve_as_one_set(self):
        root = self.base / "repo"
        for name, other in (("first", "second"), ("second", "first")):
            skill = root / "skills" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(f'---\nname: {name}\ndescription: Example\nmetadata:\n  requires: "{other}"\n---\n')
        self.assertEqual(sorted(dependency_sources(root, "first", [])), ["first", "second"])

    def test_null_and_empty_metadata_keep_the_required_closure(self):
        root = self.base / "repo"
        skill = root / "skills/example"
        skill.mkdir(parents=True)
        for block in ("", "metadata:\n", "metadata: {}\n", "metadata: null\n"):
            (skill / "SKILL.md").write_text("---\nname: example\ndescription: Example\n" + block + "---\n")
            self.assertEqual(set(dependency_sources(root, "example", [])), {"example"})

    def test_dependencies_constant_in_both_arms(self):
        dependency = self.base / "dep-source"
        dependency.mkdir()
        (dependency / "SKILL.md").write_text('---\nname: other\ndescription: Dependency\n---\n')
        self.sources["other"] = dependency
        _, arms = self.pair("codex")
        validate_pair(arms, "codex", "clear-communication")
        self.assertEqual([item["name"] for item in arms[1].inventory], ["other"])

    def test_cli_dry_run_calls_no_hosts_and_reads_no_credentials(self):
        for host in ("claude", "codex"):
            output = io.StringIO()
            with patch("evalharness.hosts.credentials", side_effect=AssertionError("credential access")), patch("evalharness.hosts.execute", side_effect=AssertionError("model call")), patch("evalharness.hosts.codex_inventory", side_effect=AssertionError("host call")), contextlib.redirect_stdout(output):
                code = main(["--root", str(ROOT), "--skill", "clear-communication", "--host", host, "--example", "near-miss-1", "--fixture", str(ROOT / "tests/eval-harness/fixtures/project-installed"), "--dry-run"])
            self.assertEqual(code, 0)
            value = json.loads(output.getvalue())
            self.assertEqual(value["status"], "dry-run")
            self.assertEqual(value["arms"]["baseline"]["inventory"], [])
            self.assertTrue(value["isolation_proof"]["seed_unchanged"])

    def test_claude_effort_is_passed_to_both_arms_and_recorded(self):
        root = self.base / "repo"
        copy_tree(self.sources["clear-communication"], root / "skills/clear-communication", skill=True)
        commands = []

        def execute(arm, host, argv, prompt, timeout):
            commands.append(argv)
            trace = [
                {"type": "system", "subtype": "init",
                 "skills": [entry["name"] for entry in arm.inventory],
                 "plugins": [], "mcp_servers": [], "tools": [],
                 "model": "fixture-model", "session_id": arm.name},
                {"type": "result", "subtype": "success", "result": "./scripts/validate.sh"},
            ]
            (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in trace))
            return {"exit_code": 0, "timed_out": False, "seconds": 0}

        with patch("evalharness.hosts.version", return_value="fixture-host"), \
             patch("evalharness.hosts.credentials", return_value=[]), \
             patch("evalharness.hosts.execute", side_effect=execute), \
             contextlib.redirect_stdout(io.StringIO()):
            code = main(["--root", str(root), "--skill", "clear-communication", "--host", "claude",
                         "--binary", sys.executable, "--model", "fixture-model", "--effort", "high",
                         "--example", "near-miss-1", "--fixture", str(ROOT / "tests/eval-harness/fixtures/package")])
        self.assertEqual(code, 0)
        self.assertEqual(len(commands), 2)
        for argv in commands:
            self.assertEqual(argv[argv.index("--effort") + 1], "high")
        directory = root / "skills/clear-communication/evals/results"
        record = json.loads(next(directory.glob("*/comparison.json")).read_text())
        self.assertEqual(record["requested_effort"], "high")
        self.assertIn("effort `high`", next(directory.glob("*.md")).read_text())

    def test_trace_claims_and_failed_commands_do_not_count_as_activation(self):
        _, arms = self.pair("codex")
        arm = arms[0]
        events = [{"type": "thread.started", "thread_id": "new-session"}, {"type": "item.completed", "item": {"type": "agent_message", "text": "I used clear-communication"}}, {"type": "item.completed", "item": {"type": "command_execution", "command": f"cat {arm.config}/skills/clear-communication/SKILL.md", "exit_code": 1}}, {"type": "turn.completed", "usage": {}}]
        (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in events))
        session = arm.config / "sessions/test.jsonl"
        session.parent.mkdir()
        session.write_text(json.dumps({"type": "turn_context", "payload": {"model": "test-model"}}) + "\n")
        self.assertFalse(hosts.observe(arm, "codex", "clear-communication")["activation"])
        events.insert(2, {"type": "item.completed", "item": {"type": "command_execution", "command": f"sed -n '1,200p' {arm.config}/skills/clear-communication/SKILL.md", "exit_code": 0, "aggregated_output": (arm.config / "skills/clear-communication/SKILL.md").read_text()}})
        (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in events))
        self.assertTrue(hosts.observe(arm, "codex", "clear-communication")["activation"])

    def test_example_numbers_and_near_miss_prompt(self):
        values = examples(ROOT / "skills/clear-communication/evals/examples.md")
        self.assertEqual(next(value for value in values if value["id"] == "near-miss-1")["prompt"], "Which command validates this repo?")
        self.assertEqual(values[0]["id"], "activation-1")

    def test_command_mentions_are_not_body_reads(self):
        path = "/temporary/skills/candidate/SKILL.md"
        self.assertFalse(hosts.body_read(f"echo cat {path}", path))
        self.assertFalse(hosts.body_read(f"cat README.md; echo {path}", path))
        self.assertFalse(hosts.body_read(f"rg name {path}", path))
        self.assertFalse(hosts.body_read(f"false && cat {path}; echo harmless", path))
        self.assertFalse(hosts.body_read(f"cat {path} >/dev/null; echo harmless", path))
        self.assertFalse(hosts.body_read(f"true || cat {path}", path))
        self.assertFalse(hosts.body_read(f"cat {path} | head -n 0", path))
        self.assertFalse(hosts.body_read(f"cat {path} && echo done", path))
        self.assertTrue(hosts.body_read(f"cat {path}", path))
        self.assertTrue(hosts.body_read(f"/bin/zsh -lc 'cat {path}'", path))
        self.assertFalse(hosts.body_read(f"pwd && sed -n '1,200p' {path}", path))
        self.assertTrue(hosts.body_read(f"sed -n '1,200p' {path}", path))

    def test_compound_output_cannot_borrow_a_skill_body_line(self):
        _, arms = self.pair("codex")
        arm = arms[0]
        path = shlex.quote(str(arm.config / "skills/clear-communication/SKILL.md"))
        session = arm.config / "sessions/test.jsonl"
        session.parent.mkdir()
        session.write_text(json.dumps({"type": "turn_context", "payload": {"model": "test-model"}}) + "\n")
        empty_read = f"sed -n '99999,100000p' {path}"
        wrapped = f"/bin/sh -c {shlex.quote(empty_read)}"
        commands = [
            f"false && cat {path}\nprintf '%s\\n' '# Clear communication'",
            f"sed -n '99999,100000p' {path} && printf '%s\\n' '# Clear communication'",
            f"{wrapped} && printf '%s\\n' '# Clear communication'",
            f"{wrapped}\nprintf '%s\\n' '# Clear communication'",
            f"{wrapped} >/dev/null; printf '%s\\n' '# Clear communication'",
        ]
        for command in commands:
            with self.subTest(command=command):
                result = subprocess.run(["/bin/sh", "-c", command], cwd=arm.work, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "# Clear communication\n")
                events = [
                    {"type": "thread.started", "thread_id": "test-session"},
                    {"type": "item.completed", "item": {"type": "command_execution", "command": command, "exit_code": result.returncode, "aggregated_output": result.stdout}},
                    {"type": "turn.completed", "usage": {}},
                ]
                (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in events))
                self.assertFalse(hosts.observe(arm, "codex", "clear-communication")["activation"])

    def test_shell_prefixes_cannot_borrow_a_skill_body_line(self):
        _, arms = self.pair("codex")
        arm = arms[0]
        path = shlex.quote(str(arm.config / "skills/clear-communication/SKILL.md"))
        session = arm.config / "sessions/test.jsonl"
        session.parent.mkdir()
        session.write_text(json.dumps({"type": "turn_context", "payload": {"model": "test-model"}}) + "\n")
        helper = arm.work / "outer-output.sh"
        helper.write_text("printf '%s\\n' '# Clear communication'\n")
        (arm.work / "-c").write_text(helper.read_text())
        empty_read = shlex.quote(f"sed -n '99999,100000p' {path}")
        comment_read = f"sed -n '# Clear communication' {path}"
        control = subprocess.run(["/bin/sh", "-c", comment_read], cwd=arm.work, capture_output=True, text=True, timeout=5)
        self.assertEqual((control.returncode, control.stdout, control.stderr), (0, "", ""))
        commands = [
            f"/bin/sh {shlex.quote(str(helper))} -c {empty_read}",
            f"/bin/sh -- -c {empty_read}",
            f"/bin/sh -x -c {shlex.quote(comment_read)}",
        ]
        for command in commands:
            with self.subTest(command=command):
                result = subprocess.run(["/bin/sh", "-c", command], cwd=arm.work, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, text=True, timeout=5)
                self.assertEqual(result.returncode, 0)
                self.assertIn("# Clear communication", result.stdout)
                events = [
                    {"type": "thread.started", "thread_id": "test-session"},
                    {"type": "item.completed", "item": {"type": "command_execution", "command": command, "exit_code": result.returncode, "aggregated_output": result.stdout}},
                    {"type": "turn.completed", "usage": {}},
                ]
                (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in events))
                self.assertFalse(hosts.observe(arm, "codex", "clear-communication")["activation"])

    def test_reader_output_must_come_from_installed_candidate(self):
        _, arms = self.pair("codex")
        arm = arms[0]
        candidate = arm.config / "skills/clear-communication/SKILL.md"
        path = shlex.quote(str(candidate))
        self.assertEqual(candidate.read_text().splitlines()[0], "---")
        session = arm.config / "sessions/test.jsonl"
        session.parent.mkdir()
        session.write_text(json.dumps({"type": "turn_context", "payload": {"model": "test-model"}}) + "\n")
        unrelated = arm.work / "unrelated.txt"
        unrelated.write_text("# Clear communication\n")
        # Another installed skill: reading it alongside the candidate is a real
        # pattern, but its copy of a candidate line cannot prove the candidate read.
        sibling = arm.config / "skills/sibling-skill/SKILL.md"
        sibling.parent.mkdir()
        sibling.write_text('---\nname: sibling-skill\ndescription: "See # Clear communication for writing rules."\n---\n\n# Sibling skill body\n- # Clear communication\n')
        echo = arm.config / "skills/echo-skill/SKILL.md"
        echo.parent.mkdir()
        echo.write_text("".join(line + "\n" for line in candidate.read_text().split("\n---\n", 1)[1].splitlines()))
        commands = [
            (f"cat {path}", True),
            (f"cat -- {path}", True),
            (f"sed -n '1,200p' {path}", True),
            (f"sed -n -e '1,200p' {path}", True),
            (f"sed -n '1p' {path}", False),
            (f"sed -n '1s/.*/# Clear communication/p' {path}", False),
            (f"head -n 200 {path}", True),
            (f"head -200 {path}", True),
            (f"head -n 1 {path} {shlex.quote(str(unrelated))}", False),
            (f"tail -n +1 {path}", True),
            (f"cat {path} {shlex.quote(str(sibling))}", True),
            (f"sed -n '1,200p' {shlex.quote(str(sibling))} {path}", True),
            (f"head -n 1 {path} {shlex.quote(str(echo))}", False),
            (f"head -n 3 {path} {shlex.quote(str(sibling))}", False),
            (f"sed -n '3p' {shlex.quote(str(sibling))} {path}", False),
            (f"tail -c 22 {path} {shlex.quote(str(sibling))}", False),
        ]
        for inner, expected in commands:
            command = f"/bin/sh -c {shlex.quote(inner)}"
            with self.subTest(command=command):
                self.assertEqual(shlex.split(command), ["/bin/sh", "-c", inner])
                result = subprocess.run(["/bin/sh", "-c", command], cwd=arm.work, capture_output=True, text=True, timeout=5)
                self.assertEqual((result.returncode, result.stderr), (0, ""))
                events = [
                    {"type": "thread.started", "thread_id": "test-session"},
                    {"type": "item.completed", "item": {"type": "command_execution", "command": command, "exit_code": result.returncode, "aggregated_output": result.stdout}},
                    {"type": "turn.completed", "usage": {}},
                ]
                (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in events))
                self.assertEqual(hosts.observe(arm, "codex", "clear-communication")["activation"], expected)

    def test_relative_reader_inputs_are_unclassified(self):
        _, arms = self.pair("codex")
        arm = arms[0]
        candidate = arm.config / "skills/clear-communication/SKILL.md"
        path = shlex.quote(str(candidate))
        session = arm.config / "sessions/test.jsonl"
        session.parent.mkdir()
        session.write_text(json.dumps({"type": "turn_context", "payload": {"model": "test-model"}}) + "\n")
        (arm.work / "unrelated.txt").write_text("# Clear communication\n")
        commands = [
            (f"cat {path}", True),
            (f"cat {path} {path}", True),
            (f"cat {path} {shlex.quote(str(arm.work / 'README.md'))}", False),
            (f"head -n 1 {path} unrelated.txt", False),
            (f"cat {path} README.md", False),
            (f"cat {path} {shlex.quote(os.path.relpath(candidate, arm.work))}", False),
        ]
        for inner, expected in commands:
            command = f"/bin/sh -c {shlex.quote(inner)}"
            with self.subTest(command=command):
                result = subprocess.run(["/bin/sh", "-c", command], cwd=arm.work, capture_output=True, text=True, timeout=5)
                self.assertEqual((result.returncode, result.stderr), (0, ""))
                events = [
                    {"type": "thread.started", "thread_id": "test-session"},
                    {"type": "item.completed", "item": {"type": "command_execution", "command": command, "exit_code": result.returncode, "aggregated_output": result.stdout}},
                    {"type": "turn.completed", "usage": {}},
                ]
                (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in events))
                self.assertEqual(hosts.observe(arm, "codex", "clear-communication")["activation"], expected)

    def test_codex_listing_then_cat_stays_unclassified(self):
        _, arms = self.pair("codex")
        arm = arms[0]
        candidate = arm.config / "skills/clear-communication/SKILL.md"
        path = shlex.quote(str(candidate))
        session = arm.config / "sessions/test.jsonl"
        session.parent.mkdir()
        session.write_text(json.dumps({"type": "turn_context", "payload": {"model": "test-model"}}) + "\n")
        commands = [
            (f"cat {path}", True),
            (f"ls {shlex.quote(str(candidate.parent))}; cat {path}", False),
        ]
        for command, expected in commands:
            with self.subTest(command=command):
                result = subprocess.run(["/bin/sh", "-c", command], cwd=arm.work,
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0)
                trace = [
                    {"type": "thread.started", "thread_id": "test-session"},
                    {"type": "item.completed", "item": {"type": "command_execution", "command": command,
                     "exit_code": result.returncode, "aggregated_output": result.stdout}},
                    {"type": "turn.completed", "usage": {}},
                ]
                (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in trace))
                self.assertEqual(hosts.observe(arm, "codex", "clear-communication")["activation"], expected)

    def test_claude_listing_then_cat_proves_a_visible_installed_body(self):
        _, arms = self.pair("claude")
        arm = arms[0]
        candidate = arm.config / "skills/clear-communication/SKILL.md"
        path = shlex.quote(str(candidate))
        listing = f"ls {shlex.quote(str(candidate.parent.parent))}; ls {shlex.quote(str(candidate.parent))} 2>&1"
        body = shlex.quote(candidate.read_text())
        commands = [
            (f"{listing}; cat {path} 2>&1", True, False),
            (f"{listing}; cat {path} 2>&1", True, True),
            (f"{listing}; cat {path} >/dev/null; printf %s {body}", False, False),
            (f"{listing}; false && cat {path}; printf %s {body}", False, False),
        ]
        for command, expected, truncated in commands:
            with self.subTest(command=command, truncated=truncated):
                result = subprocess.run(["/bin/sh", "-c", command], cwd=arm.work,
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0)
                output = result.stdout
                if truncated:
                    output = output[:output.index("# Clear communication") + 600]
                trace = [
                    {"type": "system", "subtype": "init", "skills": ["clear-communication"],
                     "plugins": [], "mcp_servers": [], "model": "test-model", "session_id": "listing-session"},
                    {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash",
                     "id": "read-1", "input": {"command": command}}]}},
                    {"type": "user", "message": {"content": [{"type": "tool_result",
                     "tool_use_id": "read-1", "is_error": False, "content": output}]}},
                    {"type": "result", "subtype": "success", "result": "Done"},
                ]
                (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in trace))
                self.assertEqual(hosts.observe(arm, "claude", "clear-communication")["activation"], expected)

    def test_codex_activation_requires_visible_body_output(self):
        _, arms = self.pair("codex")
        path = str(arms[0].config / "skills/clear-communication/SKILL.md")
        self.assertFalse(hosts.body_in_output(path, "harmless\n"))
        self.assertTrue(hosts.body_in_output(path, Path(path).read_text()))

    def test_failed_claude_skill_tool_is_not_activation(self):
        _, arms = self.pair("claude")
        arm = arms[0]
        trace = [
            {"type": "system", "subtype": "init", "skills": ["clear-communication"], "plugins": [{"path": "builtin", "source": "bundled@builtin"}], "mcp_servers": [], "model": "test-model", "session_id": "new-session"},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Skill", "id": "skill-1", "input": {"skill": "clear-communication"}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "skill-1", "is_error": True, "content": "Permission denied"}]}},
            {"type": "result", "subtype": "success", "result": "Done"},
        ]
        path = arm.evidence / "trace.jsonl"
        path.write_text("\n".join(json.dumps(value) for value in trace))
        self.assertFalse(hosts.observe(arm, "claude", "clear-communication")["activation"])
        trace[2]["message"]["content"][0]["is_error"] = False
        path.write_text("\n".join(json.dumps(value) for value in trace))
        self.assertTrue(hosts.observe(arm, "claude", "clear-communication")["activation"])

    def test_claude_native_command_replay_proves_explicit_selection(self):
        _, arms = self.pair("claude")
        arm = arms[0]
        arm.prompt = "/clear-communication Explain the result."
        replay = {"type": "user", "isReplay": True, "session_id": "native-session",
                  "parent_tool_use_id": None, "message": {"role": "user", "content":
                  "<command-message>clear-communication</command-message>\n"
                  "<command-name>/clear-communication</command-name>\n"
                  "<command-args>Explain the result.</command-args>"}}
        trace = [
            {"type": "system", "subtype": "init", "skills": ["clear-communication"],
             "slash_commands": ["clear-communication"], "plugins": [], "mcp_servers": [],
             "model": "fixture-model", "session_id": "native-session"},
            replay,
            {"type": "result", "subtype": "success", "result": "A clearer result."},
        ]
        path = arm.evidence / "trace.jsonl"
        path.write_text("\n".join(json.dumps(value) for value in trace))
        self.assertTrue(hosts.observe(arm, "claude", "clear-communication")["activation"])
        # Quoted tags and an echoed ordinary prompt are user data, even if a
        # caller supplies replay-shaped fields. They are not native selection.
        arm.prompt = replay["message"]["content"]
        self.assertFalse(hosts.observe(arm, "claude", "clear-communication")["activation"])
        arm.prompt = "/clear-communication Explain the result."
        replay["isReplay"] = False
        path.write_text("\n".join(json.dumps(value) for value in trace))
        self.assertFalse(hosts.observe(arm, "claude", "clear-communication")["activation"])

    def test_claude_command_requests_replayable_native_input(self):
        _, arms = self.pair("claude")
        argv = hosts.command(arms[0], "claude", "claude", "fixture-model", "high")
        self.assertEqual(argv[argv.index("--input-format") + 1], "stream-json")
        self.assertIn("--replay-user-messages", argv)

    def test_claude_disables_bundled_skills_that_can_fork_models(self):
        _, arms = self.pair("claude")
        for arm in arms:
            self.assertIs(arm.settings.get("disableBundledSkills"), True)
            self.assertEqual(arm.settings.get("skillOverrides", {}).get("doctor"), "off")
            self.assertEqual(arm.settings.get("skillOverrides", {}).get("plugin-authoring"), "off")
            self.assertIn("Skill(plugin-authoring)", arm.settings["permissions"]["deny"])

    def test_claude_unmetered_fork_is_an_invalid_comparison(self):
        _, arms = self.pair("claude")
        arm = arms[0]
        trace = [
            {"type": "system", "subtype": "init", "skills": ["clear-communication"],
             "plugins": [], "mcp_servers": [], "model": "fixture-model", "session_id": "fixture-session"},
            {"type": "user", "tool_use_result": {"success": True, "commandName": "code-review",
             "status": "forked", "agentId": "synthetic-child", "result": "Fixture review"},
             "message": {"role": "user", "content": []}},
            {"type": "result", "subtype": "success", "result": "Done"},
        ]
        (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in trace))
        with self.assertRaisesRegex(InvalidComparison, "forked model"):
            hosts.observe(arm, "claude", "clear-communication")

    def test_secret_evidence_is_withheld(self):
        evidence = self.base / "evidence"
        evidence.mkdir()
        # A synthetic marker, never a real credential.
        marker = b"synthetic-private-token-for-test"
        (evidence / "trace.jsonl").write_bytes(marker)
        with self.assertRaisesRegex(InvalidComparison, "evidence is withheld"):
            hosts.safe_evidence(evidence, [marker])

    def test_shared_prompt_secret_is_withheld_without_model_calls(self):
        root = self.base / "repo"
        copy_tree(self.sources["clear-communication"], root / "skills/clear-communication", skill=True)
        marker = "synthetic-private-token-for-prompt-test"
        prompt = self.base / "prompt.txt"
        prompt.write_text("Return OK. " + marker)
        with patch("evalharness.hosts.version", return_value="test-host 1"), \
             patch("evalharness.hosts.credentials", return_value=[marker.encode()]), \
             patch("evalharness.hosts.codex_inventory", side_effect=InvalidComparison("test preflight failure")), \
             patch("evalharness.hosts.execute", side_effect=AssertionError("model call")), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            code = main(["--root", str(root), "--skill", "clear-communication", "--host", "codex", "--binary", sys.executable,
                         "--example", "near-miss-1", "--fixture", str(ROOT / "tests/eval-harness/fixtures/package"),
                         "--prompt-file", str(prompt)])
        self.assertEqual(code, 1)
        self.assertFalse((root / "skills/clear-communication/evals/results").exists())

    def test_invalid_comparison_is_recorded_without_model_calls(self):
        # Use a temporary repository so the fixture test never writes results to
        # the checkout. A credential preflight failure must still yield a record.
        root = self.base / "repo"
        copy_tree(self.sources["clear-communication"], root / "skills/clear-communication", skill=True)
        fixture = ROOT / "tests/eval-harness/fixtures/package"
        output = io.StringIO()
        with patch("evalharness.hosts.version", return_value="test-host 1"), patch("evalharness.hosts.credentials", side_effect=InvalidComparison("test credential unavailable")), patch("evalharness.hosts.execute", side_effect=AssertionError("model call")), contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            code = main(["--root", str(root), "--skill", "clear-communication", "--host", "claude", "--binary", sys.executable, "--example", "near-miss-1", "--fixture", str(fixture)])
        self.assertEqual(code, 1)
        records = list((root / "skills/clear-communication/evals/results").glob("*/comparison.json"))
        self.assertEqual(len(records), 1)
        value = json.loads(records[0].read_text())
        self.assertEqual(value["status"], "invalid")
        self.assertEqual(value["model_runs_started"], 0)
        self.assertIn("test credential unavailable", value["errors"])


    def native_selection_observation(self, change=None):
        self.base = Path(tempfile.mkdtemp(prefix="native-selection-", dir=self.temporary.name))
        _, arms = self.pair("codex", project=False)
        arm = arms[0]
        path = arm.config / "skills/clear-communication/SKILL.md"
        body = path.read_text(encoding="utf-8")
        message = {"type": "response_item", "payload": {
            "type": "message", "id": "native-selected-message", "role": "user",
            "content": [{"type": "input_text", "text":
                f"<skill>\n<name>clear-communication</name>\n<path>{path}</path>\n{body}\n</skill>"}],
            "internal_chat_message_metadata_passthrough": {
                "content_item_kinds": ["skills.selected_skill_instructions"],
                "content_item_metadata": [{"provenance": {"type": "skills"}}]}}}
        if change:
            change(message, path)
        (arm.evidence / "trace.jsonl").write_text(
            json.dumps({"type": "thread.started", "thread_id": "fixture-thread"}) + "\n"
            + json.dumps({"type": "turn.completed", "usage": {}}) + "\n")
        sessions = arm.config / "sessions"
        sessions.mkdir()
        (sessions / "fixture.jsonl").write_text(json.dumps(message) + "\n"
            + json.dumps({"type": "turn_context", "payload": {"model": "fixture-model"}}) + "\n")
        return hosts.observe(arm, "codex", "clear-communication")

    def test_codex_native_selection_counts_without_shell_read(self):
        result = self.native_selection_observation()
        self.assertTrue(result["activation"])
        self.assertEqual(result["activation_evidence"][0]["event"], "skills.selected_skill_instructions")

    def test_codex_quoted_skill_tags_without_native_provenance_do_not_count(self):
        def ordinary(message, path):
            message["payload"].pop("internal_chat_message_metadata_passthrough")
        self.assertFalse(self.native_selection_observation(ordinary)["activation"])

    def test_codex_native_selection_rejects_wrong_provenance_path_and_body(self):
        def wrong_provenance(message, path):
            message["payload"]["internal_chat_message_metadata_passthrough"]["content_item_metadata"][0]["provenance"]["type"] = "human"
        def wrong_path(message, path):
            part = message["payload"]["content"][0]
            part["text"] = part["text"].replace(str(path), str(path) + ".wrong")
        def wrong_body(message, path):
            part = message["payload"]["content"][0]
            part["text"] = part["text"].replace("</skill>", "changed body\n</skill>")
        for change in (wrong_provenance, wrong_path, wrong_body):
            with self.subTest(change=change.__name__):
                self.assertFalse(self.native_selection_observation(change)["activation"])



    def test_codex_native_selection_rejects_unknown_content_types(self):
        def change_type(value):
            def change(message, path):
                part = message["payload"]["content"][0]
                if value == "absent":
                    part.pop("type")
                else:
                    part["type"] = value
            return change
        for value in ("output_text", "input_image", "image", "tool_result", "refusal", "unknown", None, "absent"):
            with self.subTest(content_type=value):
                self.assertFalse(self.native_selection_observation(change_type(value))["activation"])

    def test_codex_native_selection_requires_aligned_metadata(self):
        def extra_kind(message, path):
            message["payload"]["internal_chat_message_metadata_passthrough"]["content_item_kinds"].append("user")
        def extra_detail(message, path):
            message["payload"]["internal_chat_message_metadata_passthrough"]["content_item_metadata"].append({"provenance": {"type": "human"}})
        def extra_content(message, path):
            message["payload"]["content"].append({"type": "input_text", "text": "unannotated"})
        for change in (extra_kind, extra_detail, extra_content):
            with self.subTest(change=change.__name__):
                self.assertFalse(self.native_selection_observation(change)["activation"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
