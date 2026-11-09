#!/usr/bin/env python3
"""Offline CLI policy fixtures and optional real dependency-cruiser/Cargo probes."""

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1] / "skills/architecture-fitness-functions"
SCRIPT = SKILL / "scripts/check-cargo-boundaries.py"
SCAN = SKILL / "scripts/check-import-scan.py"


class CargoPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cargo-policy-")
        self.root = Path(self.temp.name)
        self.metadata = json.loads((HERE / "fixtures/cargo-metadata.json").read_text())
        self.policy = json.loads((SKILL / "assets/cargo-policy.json").read_text())

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, metadata=None, policy=None, expected=0, raw=None):
        source, rules = self.root / "metadata.json", self.root / "policy.json"
        source.write_text(raw if raw is not None else json.dumps(self.metadata if metadata is None else metadata))
        rules.write_text(json.dumps(self.policy if policy is None else policy))
        before = (source.read_bytes(), rules.read_bytes())
        result = subprocess.run([sys.executable, str(SCRIPT), str(source), str(rules)],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, (result.stdout, result.stderr))
        self.assertEqual(before, (source.read_bytes(), rules.read_bytes()))
        if expected == 2:
            self.assertEqual(result.stdout, "")
            self.assertIn("error:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            return
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def test_allowed_renamed_edge_and_repeat(self):
        data = self.run_cli()
        self.assertEqual(data, self.run_cli())
        self.assertEqual(data["workspace_edges"], 2)
        self.assertEqual(data["edges_by_kind"], {"normal": 2, "build": 0, "dev": 0})
        self.assertEqual(data["external_edges_out_of_scope"], 1)

    def test_forbidden_normal_build_dev_and_targets(self):
        for kind in (None, "build", "dev"):
            data = copy.deepcopy(self.metadata)
            data["resolve"]["nodes"][0]["deps"] = [
                {"name": "innocent_alias", "pkg": "opaque-data",
                 "dep_kinds": [{"kind": kind, "target": "cfg(windows)"}]}]
            result = self.run_cli(metadata=data, expected=1)
            issue = " ".join(result["findings"])
            self.assertIn("domain (domain) -> data-access (adapters)", issue)
            self.assertIn(kind or "normal", issue)
            self.assertIn("cfg(windows)", issue)

    def test_unclassified_and_wrong_policy_names(self):
        policy = copy.deepcopy(self.policy)
        policy["layers"]["domain"] = ["domain-typo"]
        findings = self.run_cli(policy=policy, expected=1)["findings"]
        self.assertTrue(any("classify" in issue for issue in findings))
        self.assertTrue(any("absent" in issue for issue in findings))

    def test_empty_graph_and_missing_resolve(self):
        data = copy.deepcopy(self.metadata)
        for node in data["resolve"]["nodes"]:
            node["deps"] = []
        self.assertIn("empty", self.run_cli(metadata=data, expected=1)["findings"][0])
        data["resolve"] = None
        self.run_cli(metadata=data, expected=2)

    def test_malformed_schema_kind_and_duplicate_keys(self):
        for mutation in ("bad-kind", "missing-node", "missing-package", "missing-dep-kinds", "boolean-version"):
            data = copy.deepcopy(self.metadata)
            if mutation == "bad-kind":
                data["resolve"]["nodes"][1]["deps"][0]["dep_kinds"][0]["kind"] = "future"
            elif mutation == "missing-node":
                data["resolve"]["nodes"].pop(0)
            elif mutation == "missing-package":
                data["packages"].pop(0)
            elif mutation == "missing-dep-kinds":
                data["resolve"]["nodes"][1]["deps"][0]["dep_kinds"] = []
            else:
                data["version"] = True
            self.run_cli(metadata=data, expected=2)
        self.run_cli(raw='{"version":1,"version":1}', expected=2)
        self.run_cli(raw="{", expected=2)
        self.run_cli(raw="[]", expected=2)

    def test_incomplete_or_ambiguous_policy(self):
        policy = copy.deepcopy(self.policy)
        del policy["allow"]["dev"]
        self.run_cli(policy=policy, expected=2)
        policy = copy.deepcopy(self.policy)
        policy["layers"]["application"].append("domain")
        self.run_cli(policy=policy, expected=2)

    def test_help_without_files(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Exits:", result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_real_offline_cargo_metadata_when_available(self):
        cargo = shutil.which("cargo")
        if not cargo:
            self.skipTest("Cargo absent; installed helper fixtures ran, real Cargo metadata probe skipped")
        (self.root / "Cargo.toml").write_text(
            '[workspace]\nmembers = ["domain", "data-access", "service"]\nresolver = "2"\n')
        for name, dependencies in (
            ("domain", ""), ("data-access", 'domain = { path = "../domain" }\n'),
            ("service", 'renamed_storage = { package = "data-access", path = "../data-access" }\n'),
        ):
            crate = self.root / name
            (crate / "src").mkdir(parents=True)
            (crate / "Cargo.toml").write_text(
                f'[package]\nname = "{name}"\nversion = "0.1.0"\nedition = "2021"\n[dependencies]\n' + dependencies)
            (crate / "src/lib.rs").write_text("pub fn marker() {}\n")
        result = subprocess.run([cargo, "metadata", "--offline", "--format-version", "1",
                                 "--manifest-path", str(self.root / "Cargo.toml")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.run_cli(metadata=json.loads(result.stdout))


class ImportScanTests(unittest.TestCase):
    def test_nonempty_empty_wrong_root_and_errors(self):
        with tempfile.TemporaryDirectory(prefix="import-scan-") as directory:
            root = Path(directory)
            report = root / "graph.json"
            good = {"modules": [{"source": "src/app.ts", "dependencies": []}],
                    "summary": {"violations": [], "error": 0}}
            cases = [(good, "src", 0), (good, "not-scanned", 1)]
            empty = {"modules": [], "summary": {"violations": [], "error": 0}}
            cases.append((empty, "src", 1))
            forbidden = copy.deepcopy(good)
            forbidden["summary"]["violations"] = [{"rule": {"name": "boundary", "severity": "error"}}]
            cases.append((forbidden, "src", 1))
            duplicate = copy.deepcopy(good)
            duplicate["modules"] *= 2
            cases.append((duplicate, "src", 2))
            cases.extend([(None, "src", 2), ({"modules": []}, "src", 2)])
            for contents, required, expected in cases:
                report.write_text(json.dumps(contents))
                before = report.read_bytes()
                result = subprocess.run([sys.executable, str(SCAN), str(report), "--require-root", required],
                                        cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, (result.stdout, result.stderr))
                self.assertEqual(report.read_bytes(), before)
                if expected == 2:
                    self.assertEqual(result.stdout, "")
                    self.assertNotIn("Traceback", result.stderr)
                else:
                    self.assertEqual(result.stderr, "")
                    data = json.loads(result.stdout)
                    self.assertEqual(bool(data["findings"]), expected == 1)
            report.write_text(json.dumps(good))
            for _ in range(2):
                result = subprocess.run([sys.executable, str(SCAN), str(report), "--require-root", "src"],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_help_without_input_or_effects(self):
        with tempfile.TemporaryDirectory(prefix="scan-help-") as directory:
            result = subprocess.run([sys.executable, str(SCAN), "--help"], cwd=directory,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertIn("Exits:", result.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])


class TypeScriptAdapterTests(unittest.TestCase):
    def test_real_checker_after_setup_reapplication(self):
        command = os.environ.get("DEPCRUISE") or shutil.which("depcruise")
        if not command:
            self.skipTest("dependency-cruiser absent; set DEPCRUISE to the locally installed pinned binary; no network attempted")
        version = subprocess.run([command, "--version"], capture_output=True, text=True)
        self.assertEqual(version.returncode, 0, version.stderr)
        self.assertEqual(version.stdout.strip(), "18.7.2", "install dependency-cruiser 18.7.2 or update the starter and fixtures together")
        with tempfile.TemporaryDirectory(prefix="ts-boundary-") as directory:
            root = Path(directory)
            shutil.copytree(HERE / "fixtures/typescript", root, dirs_exist_ok=True)
            config = root / ".dependency-cruiser.cjs"

            def run(expected, rule=None):
                result = subprocess.run([command, "--config", str(config), "--output-type", "json", "src"],
                                        cwd=root, capture_output=True, text=True)
                self.assertIn(result.returncode, (0, expected), (result.stdout[:1000], result.stderr))
                report = json.loads(result.stdout)
                self.assertTrue(report["modules"], "a scan of no files is not a passing rule")
                graph = root / "boundary-report.json"
                graph.write_text(result.stdout)
                scan = subprocess.run([sys.executable, str(SCAN), str(graph),
                                       "--require-root", "src/packages", "--require-root", "src/app.ts"],
                                      cwd=root, capture_output=True, text=True)
                self.assertEqual(scan.returncode, expected, (scan.stdout, scan.stderr))
                violations = report["summary"]["violations"]
                if rule:
                    self.assertIn(rule, [item["rule"]["name"] for item in violations])
                    # JSON reports may exit zero; the normal error reporter must reject.
                    rejected = subprocess.run([command, "--config", str(config), "--output-type", "err", "src"],
                                              cwd=root, capture_output=True, text=True)
                    self.assertEqual(rejected.returncode, 1, (rejected.stdout[:1000], rejected.stderr))
                    self.assertIn(rule, rejected.stdout + rejected.stderr)
                else:
                    self.assertEqual(violations, [])

            cases = [
                ("src/app.ts", 'import { read } from "./packages/a/lib/read";\n', "entrypoint-boundary-from-app"),
                ("src/packages/b/index.ts", 'import { read } from "../a/lib/read";\nexport const calculate = read;\n', "entrypoint-boundary-across-packages"),
                ("src/packages/a/tests/main.ts", 'import { read } from "../lib/read";\n', "tests-through-entrypoints"),
                ("src/packages/a/tests/main.ts", 'import { otherFixture } from "../../b/tests/fixture";\n', "tests-through-entrypoints"),
                ("src/packages/a/index.ts", 'import { fixture } from "./tests/fixture";\n', "tests-folder-is-private"),
                ("src/app.ts", 'import type { InternalValue } from "./packages/a/lib/types";\nexport type Public = InternalValue;\n', "entrypoint-boundary-from-app"),
                ("src/app.ts", 'import "./missing";\n', "no-unresolved"),
            ]
            for application in range(2):
                # This fixture's setup is a scoped starter copy, reapplied from source.
                shutil.copyfile(SKILL / "assets/dependency-cruiser.cjs", config)
                self.assertEqual(config.read_bytes(), (SKILL / "assets/dependency-cruiser.cjs").read_bytes())
                run(0)
                for name, contents, rule in cases:
                    path = root / name
                    original = path.read_bytes()
                    path.write_text(contents)
                    run(1, rule)
                    path.write_bytes(original)
                    run(0)
                first = root / "src/packages/a/lib/first.ts"
                second = root / "src/packages/a/lib/second.ts"
                first.write_text('import "./second";\n')
                second.write_text('import "./first";\n')
                run(1, "no-circular")
                first.unlink()
                second.unlink()
                run(0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
