"""Offline real-Node fixtures for artifact build/import/start and bounded cleanup."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHECK = ROOT / "skills/typescript-node-services/scripts/smoke-built-entry.py"
NODE = shutil.which("node")


@unittest.skipUnless(NODE and os.name == "posix", "install Node on a POSIX host for smoke fixtures")
class Smoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.node = str(Path(NODE).resolve())
        cls.version = subprocess.check_output([cls.node, "--version"], text=True, timeout=5).strip()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="node-smoke-fixtures-")
        self.root = Path(self.temp.name)
        self.source = self.root / "source.mjs"
        self.source.write_text("export const value = 1;\n")
        self.build = [sys.executable, "-c",
                      "from pathlib import Path; Path('dist').mkdir(exist_ok=True); "
                      "Path('dist/entry.mjs').write_bytes(Path('source.mjs').read_bytes())"]

    def tearDown(self):
        self.temp.cleanup()

    def call(self, mode="import", extra=(), env=None, disposable=True):
        command = [sys.executable, str(CHECK), "--node", self.node,
                   "--expected-version", self.version,
                   "--build-command", json.dumps(self.build),
                   "--entry", "dist/entry.mjs", "--mode", mode,
                   "--build-timeout", "3", "--startup-timeout", "3", "--drain-timeout", "1"]
        if disposable:
            command += ["--disposable-dir", str(self.root)]
        if mode == "start":
            command += ["--ready-file", "ready"]
        command += list(extra)
        return subprocess.run(command, text=True, capture_output=True, env=env, timeout=15)

    def assert_no_process(self):
        pid = int((self.root / "pid").read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(pid, 0)

    def write_server(self, handler="process.exit(0)"):
        self.source.write_text(
            'import { writeFileSync } from "node:fs";\n'
            'writeFileSync("pid", String(process.pid));\n'
            f'process.on("SIGTERM", () => {{ {handler}; }});\n'
            'writeFileSync("ready", "application-ready");\n'
            'setInterval(() => {}, 1000);\n')

    def test_help_without_disposable_target_or_effect(self):
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        result = subprocess.run([sys.executable, str(CHECK), "--help"], cwd=self.root,
                                text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Exit:", result.stdout)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_import_accept_repeat_and_builds_emitted_entry(self):
        first = self.call()
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        self.assertEqual(first.stdout, self.call().stdout)
        self.assertEqual((self.root / "dist/entry.mjs").read_bytes(), self.source.read_bytes())

    def test_missing_disposable_target_refused_before_build(self):
        result = self.call(disposable=False)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "dist").exists())

    def test_checkout_wrong_runtime_escape_and_source_entry_refused(self):
        for extra in (["--expected-version", "v0.invalid"], ["--entry", "../escape.mjs"],
                      ["--entry", "source.ts"], ["--build-command", '["not-used"],null']):
            result = self.call(extra=extra)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertFalse((self.root / "dist").exists())
        (self.root / ".git").write_text("fixture git marker")
        self.assertEqual(self.call().returncode, 2)

    def test_syntax_failure_and_child_output_redacted(self):
        self.source.write_text('console.error("SYNTHETIC_SECRET"); throw new Error("SYNTHETIC_SECRET");')
        result = self.call()
        self.assertEqual(result.returncode, 1, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["stage"], "import")
        self.assertNotIn("SYNTHETIC_SECRET", result.stdout + result.stderr)

    def test_build_failure_and_timeout(self):
        self.build = [sys.executable, "-c", "print('SYNTHETIC_SECRET'); raise SystemExit(7)"]
        result = self.call()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["stage"], "build")
        self.assertNotIn("SYNTHETIC_SECRET", result.stdout + result.stderr)
        self.build = [sys.executable, "-c", "import time; time.sleep(10)"]
        result = self.call(extra=["--build-timeout", "0.1"])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["finding"], "timeout")

    def test_missing_emitted_entry(self):
        self.build = [sys.executable, "-c", "pass"]
        result = self.call()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["finding"], "emitted_entry_missing")

    def test_start_readiness_sigterm_clean_drain(self):
        self.write_server('writeFileSync("drained", "committed"); process.exit(0)')
        result = self.call("start")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual((self.root / "drained").read_text(), "committed")
        self.assert_no_process()

    def test_existing_readiness_refused(self):
        (self.root / "ready").write_text("stale")
        result = self.call("start")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "dist").exists())

    def test_drain_timeout_kills_owned_process(self):
        self.write_server("void 0")
        result = self.call("start", extra=["--drain-timeout", "0.1"])
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["finding"], "drain_timeout")
        self.assert_no_process()

    def test_import_with_leaked_handle_times_out(self):
        self.source.write_text('import {writeFileSync} from "node:fs";'
                               'writeFileSync("pid",String(process.pid));setInterval(()=>{},1000);')
        result = self.call(extra=["--startup-timeout", "0.5"])
        self.assertEqual(result.returncode, 1)
        self.assert_no_process()

    def test_invalid_config_stops_before_readiness_and_names_key_only(self):
        self.source.write_text(
            'const value = process.env.NODE_SMOKE_FIXTURE_PORT;'
            'if (!value || !/^[0-9]+$/.test(value)) {'
            'console.error("NODE_SMOKE_FIXTURE_PORT: expected integer"); process.exit(2); }\n'
            'import {writeFileSync} from "node:fs";writeFileSync("ready","unexpected");')
        env = dict(os.environ)
        env.pop("NODE_SMOKE_FIXTURE_PORT", None)
        for value in (None, "SYNTHETIC_SECRET_NOT_A_PORT"):
            if value is not None:
                env["NODE_SMOKE_FIXTURE_PORT"] = value
            result = self.call("start", env=env)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse((self.root / "ready").exists())
            direct = subprocess.run([self.node, str(self.root / "dist/entry.mjs")],
                                    capture_output=True, text=True, env=env, timeout=5)
            self.assertEqual(direct.returncode, 2)
            self.assertIn("NODE_SMOKE_FIXTURE_PORT", direct.stderr)
            self.assertNotIn("SYNTHETIC_SECRET", direct.stderr)

    def test_reject_mode_checks_key_and_canary_without_echoing_output(self):
        self.source.write_text('console.error("FIXTURE_KEY: expected integer"); process.exit(2);')
        result = self.call("reject", extra=["--expect-key", "FIXTURE_KEY",
                                          "--forbid", "SYNTHETIC_ONLY_CANARY"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.source.write_text('console.error("FIXTURE_KEY: SYNTHETIC_ONLY_CANARY"); process.exit(2);')
        result = self.call("reject", extra=["--expect-key", "FIXTURE_KEY",
                                          "--forbid", "SYNTHETIC_ONLY_CANARY"])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["finding"], "config_canary_disclosed")
        self.assertNotIn("SYNTHETIC_ONLY_CANARY", result.stdout + result.stderr)

    def test_reject_mode_fails_success_signal_wrong_key_hang_and_large_output(self):
        cases = [
            ('console.error("FIXTURE_KEY");', "invalid_config_not_rejected_cleanly"),
            ('process.kill(process.pid,"SIGTERM");', "invalid_config_not_rejected_cleanly"),
            ('console.error("OTHER_KEY"); process.exit(2);', "config_key_missing_from_diagnostic"),
            ('setInterval(()=>{},1000);', "invalid_config_did_not_exit"),
            ('console.error("FIXTURE_KEY" + "x".repeat(100000)); process.exit(2);', "diagnostic_size_limit"),
        ]
        for source, code in cases:
            self.source.write_text(source)
            result = self.call("reject", extra=["--expect-key", "FIXTURE_KEY",
                                              "--startup-timeout", "0.5",
                                              "--max-output-bytes", "1024"])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["finding"], code)

    def test_reject_mode_usage_is_checked_before_build(self):
        for extra in ([], ["--expect-key", "not a key"], ["--expect-key", "FIXTURE_KEY", "--forbid", ""]):
            self.assertEqual(self.call("reject", extra=extra).returncode, 2)
            self.assertFalse((self.root / "dist").exists())

    def test_disposable_subdirectory_of_checkout_is_refused(self):
        outer = self.root
        (outer / ".git").write_text("fixture git marker")
        self.root = outer / "nested"
        self.root.mkdir()
        result = self.call()
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "dist").exists())


if __name__ == "__main__":
    if not NODE or os.name != "posix":
        print("Skipped Node smoke fixtures: install Node on a POSIX host.")
    unittest.main()
