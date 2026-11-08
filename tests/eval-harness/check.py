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

    def test_uncontrolled_ancestor_is_rejected(self):
        _, arms = self.pair("codex")
        outside = self.base / ".agents/skills/clear-communication"
        copy_tree(self.sources["clear-communication"], outside, skill=True)
        with self.assertRaisesRegex(InvalidComparison, "uncontrolled ancestor"):
            inventory(arms[1], "codex")

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

    def test_trace_claims_and_failed_commands_do_not_count_as_activation(self):
        _, arms = self.pair("codex")
        arm = arms[0]
        events = [{"type": "thread.started", "thread_id": "new-session"}, {"type": "item.completed", "item": {"type": "agent_message", "text": "I used clear-communication"}}, {"type": "item.completed", "item": {"type": "command_execution", "command": f"cat {arm.config}/skills/clear-communication/SKILL.md", "exit_code": 1}}, {"type": "turn.completed", "usage": {}}]
        (arm.evidence / "trace.jsonl").write_text("\n".join(json.dumps(value) for value in events))
        session = arm.config / "sessions/test.jsonl"
        session.parent.mkdir()
        session.write_text(json.dumps({"type": "turn_context", "payload": {"model": "test-model"}}) + "\n")
        self.assertFalse(hosts.observe(arm, "codex", "clear-communication")["activation"])
        events.insert(2, {"type": "item.completed", "item": {"type": "command_execution", "command": f"sed -n '1,200p' {arm.config}/skills/clear-communication/SKILL.md", "exit_code": 0, "aggregated_output": "# Skill body"}})
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
        self.assertTrue(hosts.body_read(f"/bin/zsh -lc 'cat {path}'", path))
        self.assertTrue(hosts.body_read(f"pwd && sed -n '1,200p' {path}", path))

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

    def test_secret_evidence_is_withheld(self):
        evidence = self.base / "evidence"
        evidence.mkdir()
        # A synthetic marker, never a real credential.
        marker = b"synthetic-private-token-for-test"
        (evidence / "trace.jsonl").write_bytes(marker)
        with self.assertRaisesRegex(InvalidComparison, "evidence is withheld"):
            hosts.safe_evidence(evidence, [marker])

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
