"""Offline contracts for check-rollback-plan.py using the shipped starter as the base fixture."""

import copy
import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCRIPT = ROOT / "skills/release-rollback-planning/scripts/check-rollback-plan.py"
STARTER = HERE / "fixtures/ready.json"
TODAY = "2026-11-10"


class CheckRollbackPlan(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rollback-plan-")
        self.path = Path(self.temp.name) / "plan.json"
        self.plan = json.loads(STARTER.read_text())
        (self.path.parent / "drill.txt").write_text("Synthetic test evidence only; no drill occurred")

    def tearDown(self):
        self.temp.cleanup()

    def call(self, plan=None, *args, restamp=True):
        value = copy.deepcopy(self.plan if plan is None else plan)
        if restamp and isinstance(value.get("drill"), dict):
            value["drill"]["plan_sha256"] = hashlib.sha256(json.dumps({k:v for k,v in value.items() if k != "drill"}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        self.path.write_text(json.dumps(value))
        result = subprocess.run([sys.executable, str(SCRIPT), "--today", TODAY, *args, str(self.path)],
                                capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout) if result.stdout.strip().startswith("{") else None
        return result, data

    def rules(self, plan=None, *args):
        result, data = self.call(plan, *args)
        return result.returncode, {f["rule"] for f in data["findings"]}

    def variant(self, change):
        plan = copy.deepcopy(self.plan)
        change(plan)
        return plan

    def test_help(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertIn("Exit:", result.stdout)

    def test_starter_passes_and_repeats(self):
        first, data = self.call()
        before = self.path.read_bytes()
        second = subprocess.run([sys.executable, str(SCRIPT), "--today", TODAY, str(self.path)],
                                capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stdout)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(data["summary"]["irreversible_effects"], 2)

    def test_tags_and_branches_are_rejected(self):
        def change(plan):
            plan["previous"]["artifact"] = "registry.example.com/checkout:1.41.0"
            plan["candidate"]["config"] = "main"
        code, rules = self.rules(self.variant(change))
        self.assertEqual(code, 1)
        self.assertTrue({"artifact_not_digest", "config_not_pinned", "drill_artifacts"} <= rules, rules)

    def test_config_only_recovery_is_valid_but_identical_state_is_not(self):
        def change(plan):
            plan["previous"]["artifact"] = plan["candidate"]["artifact"]
            plan["drill"]["previous_artifact"] = plan["candidate"]["artifact"]
            plan["drill"]["recovered_artifact"] = plan["candidate"]["artifact"]
        config_only = self.variant(change)
        self.assertEqual(self.rules(config_only)[0], 0)
        config_only["previous"]["config"] = config_only["candidate"]["config"]
        config_only["drill"]["previous_config"] = config_only["candidate"]["config"]
        self.assertIn("same_state", self.rules(config_only)[1])

    def test_empty_cannot_undo_list_is_rejected(self):
        code, rules = self.rules(self.variant(lambda p: p.update(irreversible_effects=[])))
        self.assertEqual((code, rules), (1, {"irreversible_effects"}))

    def test_contracted_schema_blocks_rollback_strategy(self):
        def change(plan):
            plan["schema"].update(phase="contract", previous_code_compatible=False)
        code, rules = self.rules(self.variant(change))
        self.assertEqual((code, rules), (1, {"rollback_blocked_by_schema"}))
        forward = self.variant(lambda p: (change(p), p.update(strategy="roll-forward"),
                                          p["drill"].update(action="roll-forward", recovered_artifact=p["candidate"]["artifact"])))
        self.assertEqual(self.rules(forward)[0], 0)
        no_conditions = self.variant(lambda p: (change(p), p.update(strategy="roll-forward"),
                                                p["decision"].update(roll_forward_when=[])))
        self.assertIn("decision", self.rules(no_conditions)[1])

    def test_gitops_needs_auto_sync_handling(self):
        self.assertIn("gitops_auto_sync", self.rules(self.variant(lambda p: p["delivery"].pop("auto_sync")))[1])
        push = self.variant(lambda p: p.update(delivery={"mechanism": "push"}))
        self.assertEqual(self.rules(push)[0], 0)

    def test_drill_must_be_outside_production_on_these_artifacts_within_budget(self):
        self.assertIn("drill_environment", self.rules(self.variant(lambda p: p["drill"].update(environment="production")))[1])
        self.assertIn("drill_too_slow", self.rules(self.variant(lambda p: p["drill"].update(measured_seconds=900)))[1])
        self.assertIn("drill_user_path", self.rules(self.variant(lambda p: p["drill"]["user_path_check"].update(passed=False)))[1])
        self.assertIn("drill_artifacts", self.rules(self.variant(
            lambda p: p["drill"].update(candidate_artifact=p["previous"]["artifact"])))[1])

    def test_missing_or_old_drill(self):
        undrilled = self.variant(lambda p: p.pop("drill"))
        self.assertEqual(self.rules(undrilled), (1, {"unrehearsed"}))
        self.assertEqual(self.rules(undrilled, "--allow-unrehearsed")[0], 0)
        self.assertEqual(self.rules(None, "--max-drill-age-days", "2"), (1, {"drill_stale"}))

    def test_decision_needs_threshold_decider_and_placeholder_free_commands(self):
        rules = self.rules(self.variant(lambda p: (p["decision"]["rollback_when"][0].pop("threshold"),
                                                   p["decision"].pop("decider"))))[1]
        self.assertEqual(rules, {"decision"})
        placeholder = self.variant(lambda p: p["rollback"]["commands"].append("kubectl rollout undo <deployment>"))
        self.assertEqual(self.rules(placeholder)[1], {"rollback_commands"})

    def test_usage_errors(self):
        self.path.write_text("not json")
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.path.write_text("[]")
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)

    def test_changed_plan_or_config_invalidates_old_drill(self):
        changed = self.variant(lambda p: p["rollback"]["commands"].append("Changed since rehearsal"))
        result, data = self.call(changed, restamp=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("drill_stale", {x["rule"] for x in data["findings"]})
        changed = self.variant(lambda p: p["drill"].update(previous_config="git:" + "f" * 40))
        self.assertIn("drill_config", self.rules(changed)[1])
        changed = self.variant(lambda p: p["drill"].update(receipt="../outside"))
        self.assertIn("drill_receipt", self.rules(changed)[1])

    def test_private_values_never_appear_in_output(self):
        plan = self.variant(lambda p: p.update(service="SYNTHETIC_CREDENTIAL"))
        result, _ = self.call(plan)
        self.assertNotIn("SYNTHETIC_CREDENTIAL", result.stdout + result.stderr)
        self.path.write_text('{"service":"SYNTHETIC_CREDENTIAL", "service":1}')
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("SYNTHETIC_CREDENTIAL", result.stdout + result.stderr)
        self.path.write_text('{"value":Infinity}')
        self.assertEqual(subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True).returncode, 2)

    def test_missing_target_authority_abort_and_unfilled_starter(self):
        for field in ("target", "owner", "authority"):
            self.assertIn("missing", self.rules(self.variant(lambda p: p.pop(field)))[1])
        self.assertIn("recovery_boundary", self.rules(self.variant(lambda p: p["rollback"].pop("abort")))[1])
        asset = ROOT / "skills/release-rollback-planning/assets/rollback-plan.json"
        result = subprocess.run([sys.executable, str(SCRIPT), str(asset)], capture_output=True)
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
