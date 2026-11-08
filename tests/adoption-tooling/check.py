#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Offline adoption-tooling fixtures; run.sh supplies the declared uv runtime."""

import contextlib
import copy
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import hostconfig
import skillcatalog
from evalharness.isolation import dependency_sources


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


catalog = module("catalog_checker", "check-catalog.py")
skills = module("skills_checker", "check-skills.py")
installer = module("installer", "install-skills.py")
generator = module("generator", "build-host-config.py")


class FixtureBase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="adoption-tooling-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.home = self.base / "home"
        self.config = self.home / ".claude"
        self.project = self.base / "project"
        self.project.mkdir()
        self.home.mkdir()
        environment = patch.dict(os.environ, {"HOME": str(self.home), "CLAUDE_CONFIG_DIR": str(self.config), "CODEX_HOME": str(self.home / ".codex"), "XDG_CONFIG_HOME": str(self.base / "config")})
        environment.start()
        self.addCleanup(environment.stop)
        self.root = self.base / "repo"
        shutil.copytree(ROOT / "tests/check-catalog/pass/consistent", self.root)
        self.binary = self.base / "claude"
        self.binary.write_text('#!/bin/sh\n# skillOverrides:()=>record(string(),enum(["on","name-only","user-invocable-only","off"]))\n[ "$1" = --version ] || exit 91\nprintf "2.1.311 (Claude Code)\\n"\n')
        self.binary.chmod(0o755)

    def edit_catalog(self, action):
        path = self.root / "catalog/skills.yaml"
        data = yaml.safe_load(path.read_text())
        action(data)
        path.write_text(yaml.safe_dump(data, sort_keys=False))

    def mode(self, mode="user", name="cap-a"):
        self.edit_catalog(lambda data: data["skills"][name].update(invocation=mode))
        self.assert_code(generator.main, ["--root", str(self.root), "--apply"], 0)

    def assert_code(self, fn, args, code):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            actual = fn(args)
        self.assertEqual(actual, code, (out.getvalue(), err.getvalue()))
        return out.getvalue(), err.getvalue()

    def invoke(self, *args, code=0):
        return self.assert_code(installer.main, ["--root", str(self.root), *map(str, args)], code)

    def claude(self, *args, scope="user", code=0):
        config = self.config if scope == "user" else self.project / ".claude"
        settings = config / ("settings.local.json" if scope == "local" else "settings.json")
        return self.invoke("--host", "claude", "--target", config / "skills", "--settings", settings,
                           "--settings-scope", scope, "--project-root", self.project,
                           "--claude-bin", self.binary, *args, code=code)

    def write_settings(self, value, scope="user"):
        directory = self.config if scope == "user" else self.project / ".claude"
        path = directory / ("settings.local.json" if scope == "local" else "settings.json")
        directory.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
        return path

    def checked(self):
        return catalog.check(skillcatalog.load(self.root))

class Fixtures(FixtureBase):
    def test_catalog_default_and_explicit_modes_accept_repeat(self):
        self.assertEqual(self.checked(), [])
        self.assertEqual(skillcatalog.load(self.root).invocation("cap-a"), "model")
        self.mode()
        self.assertEqual(self.checked(), [])
        self.assertEqual(self.checked(), [])
        self.mode("model")
        self.assertFalse((self.root / "skills/cap-a/agents").exists())
        self.assertEqual(self.checked(), [])

    def test_catalog_rejects_invalid_invocation(self):
        for value in (None, False, "manual", 4):
            self.edit_catalog(lambda data: data["skills"]["cap-a"].update(invocation=value))
            self.assertIn("invocation must be model or user", "\n".join(self.checked()))

    def test_generator_preview_drift_apply_repeat_and_foreign_file(self):
        self.edit_catalog(lambda data: data["skills"]["cap-a"].update(invocation="user"))
        out, _ = self.assert_code(generator.main, ["--root", str(self.root)], 0)
        path = self.root / "skills/cap-a/agents/openai.yaml"
        self.assertFalse(path.exists())
        self.assertEqual(json.loads(out)["changes"][0]["content"], hostconfig.USER_POLICY)
        self.assert_code(generator.main, ["--root", str(self.root), "--check"], 1)
        self.mode()
        self.assertEqual(path.read_text(), hostconfig.USER_POLICY)
        before = path.stat().st_mtime_ns
        self.assert_code(generator.main, ["--root", str(self.root), "--apply"], 0)
        self.assertEqual(path.stat().st_mtime_ns, before)
        path.write_text("policy:\n  allow_implicit_invocation: true\n")
        self.assert_code(generator.main, ["--root", str(self.root), "--apply"], 1)
        self.assertIn("true", path.read_text())

    def test_generator_rejects_links_and_unowned_agents_content(self):
        self.mode()
        directory = self.root / "skills/cap-a/agents"
        (directory / "extra.yaml").write_text("foreign")
        self.assertIn("only generated", "\n".join(self.checked()))
        (directory / "extra.yaml").unlink()
        policy = directory / "openai.yaml"
        policy.unlink()
        policy.symlink_to(self.base / "outside")
        self.assertIn("must not be a symlink", "\n".join(self.checked()))
        self.assertFalse((self.base / "outside").exists())

    def test_prose_known_owned_external_qualified_accepts(self):
        path = self.root / "skills/cap-a/SKILL.md"
        path.write_text(path.read_text() + "\nWhen needed, read the `cap-b` skill, then the upstream `ext-x` skill.\n")
        self.assertEqual(self.checked(), [])
        self.assertEqual(self.checked(), [])
        # The optional pointer does not expand the closure.
        self.assertEqual(skillcatalog.closure(skillcatalog.load(self.root), "cap-a")[0], ["cap-a", "cap-b"])

    def test_prose_unknown_renamed_provider_and_dropped_inventory_reject(self):
        path = self.root / "skills/cap-a/SKILL.md"
        original = path.read_text()
        for text in ("the `nope` skill", "the `old-cap-b` skill", "the favorite `ext-x` skill"):
            path.write_text(original + "\n" + text)
            self.assertTrue(any("prose skill" in problem or "provider favorite" in problem for problem in self.checked()))
        path.write_text(original + "\nWhen needed, use the `ext-x` skill.\n")
        self.edit_catalog(lambda data: data["external"].clear())
        self.assertIn("unknown prose skill ext-x", "\n".join(self.checked()))

    def test_prose_fences_placeholders_historical_crosswalk_accept(self):
        path = self.root / "skills/cap-a/SKILL.md"
        path.write_text(path.read_text() + '''
```markdown
Read the `unknown-code` skill.
```
~~~~text
Read the `unknown-tilde` skill.
~~~~
When <condition> applies, read the `<name>` skill and the `{{name}}` skill.
<!-- skill-names: historical -->
The `removed-name` skill was renamed in the old inventory.
<!-- skill-names: end -->
When needed, read the `cap-b` skill.
''')
        self.assertEqual(self.checked(), [])
        path.write_text(path.read_text() + "\nRead the `unknown-after-history` skill.\n")
        self.assertIn("unknown prose skill unknown-after-history", "\n".join(self.checked()))

    def test_prose_one_level_owned_reference_and_asset(self):
        path = self.root / "skills/cap-a/SKILL.md"
        path.write_text(path.read_text() + "\nRead [guide](references/guide.md) for the narrow case and [data](assets/note.txt).\n")
        directory = path.parent
        (directory / "references").mkdir()
        (directory / "assets").mkdir()
        guide = directory / "references/guide.md"
        guide.write_text("Use the `cap-b` skill. [More](nested.md)\n")
        (directory / "references/nested.md").write_text("Use the `unknown-indirect` skill.")
        asset = directory / "assets/note.txt"
        asset.write_text("Use the `ext-x` skill.")
        self.assertEqual(self.checked(), [])
        asset.write_text("Use the `unknown-asset` skill.")
        self.assertIn("unknown prose skill unknown-asset", "\n".join(self.checked()))
        asset.write_text("Use the `cap-b` skill.")
        guide.write_text("Use the `unknown-reference` skill.")
        self.assertIn("unknown prose skill unknown-reference", "\n".join(self.checked()))
        guide.unlink()
        self.assertIn("linked resource references/guide.md is missing", "\n".join(self.checked()))

    def test_required_unknown_reserved_and_exact_canonical_names_reject(self):
        path = self.root / "skills/cap-a/SKILL.md"
        original = path.read_text()
        path.write_text(original.replace('requires: "cap-b"', 'requires: "missing"'))
        self.assertIn("metadata.requires names missing", "\n".join(self.checked()))
        with self.assertRaisesRegex(ValueError, "missing required skills missing"):
            skillcatalog.closure(skillcatalog.load(self.root), "cap-a")
        path.write_text(original.replace('name: cap-a', 'name: renamed'))
        self.assertIn("frontmatter name must equal", "\n".join(self.checked()))
        path.write_text(original)
        with (self.root / "catalog/reserved-names.txt").open("a") as stream:
            stream.write("\ncap-a\n")
        self.assertIn("cap-a is a reserved name", "\n".join(self.checked()))
        self.assertIn("verify", skillcatalog.load(ROOT).reserved)
        self.assertIn("run-skill-generator", skillcatalog.load(ROOT).reserved)

    def test_external_generic_uniqueness_rejects_within_and_across_providers(self):
        self.edit_catalog(lambda data: data["external"].update(other={"skills": ["ext-x"]}))
        self.assertIn("duplicate external inventory", "\n".join(self.checked()))
        self.edit_catalog(lambda data: data["external"].pop("other"))
        self.edit_catalog(lambda data: data["external"]["upstream"]["skills"].append("ext-x"))
        self.assertIn("duplicate external inventory", "\n".join(self.checked()))

    def test_null_empty_metadata_and_actual_cycle_closures_accept(self):
        path = self.root / "skills/cap-b/SKILL.md"
        for block in ("", "metadata:\n", "metadata: null\n", "metadata: {}\n"):
            path.write_text("---\nname: cap-b\ndescription: Fixture\n" + block + "---\n\nBody.\n")
            self.assertEqual(self.checked(), [])
            self.assertEqual(set(dependency_sources(self.root, "cap-a", [])), {"cap-a", "cap-b"})
            self.assertEqual(skillcatalog.closure(skillcatalog.load(self.root), "cap-a"), (["cap-a", "cap-b"], []))
        owned, upstream = skillcatalog.closure(skillcatalog.load(ROOT), "decision-log")
        self.assertEqual(owned, ["decision-log", "work-decomposition"])
        self.assertEqual(upstream, [])
        self.assertEqual(set(dependency_sources(ROOT, "decision-log", [])), set(owned))
        self.assertEqual(installer.resolve(skillcatalog.load(ROOT), ["decision-log"]), (owned, [], []))

    def test_user_invocation_remains_a_valid_required_edge(self):
        self.mode(name="cap-b")
        self.assertEqual(self.checked(), [])
        self.assertEqual(skillcatalog.closure(skillcatalog.load(self.root), "cap-a")[0], ["cap-a", "cap-b"])

    def test_copy_symlink_multi_name_closure_and_source_policy_stays_readonly(self):
        self.mode()
        source_before = installer.files(self.root / "skills/cap-a")
        for mode in ("copy", "symlink"):
            target = self.base / mode
            out, _ = self.invoke("--target", target, "--mode", mode, "cap-a", "role-one")
            self.assertFalse(target.exists())
            self.assertEqual(json.loads(out)["mode"], "preview")
            out, _ = self.invoke("--target", target, "--mode", mode, "--apply", "cap-a", "role-one")
            self.assertEqual(json.loads(out)["installed"], ["cap-a", "cap-b", "role-one"])
            self.assertEqual((target / "cap-a").is_symlink(), mode == "symlink")
            self.assertEqual((target / "cap-a/agents/openai.yaml").read_text(), hostconfig.USER_POLICY)
            self.assertEqual(installer.files(target / "cap-a"), source_before)
            receipt = target / installer.STATE
            before = receipt.read_bytes(), receipt.stat().st_mtime_ns
            self.invoke("--target", target, "--mode", mode, "--apply", "cap-a", "role-one")
            self.assertEqual((receipt.read_bytes(), receipt.stat().st_mtime_ns), before)
        self.assertEqual(installer.files(self.root / "skills/cap-a"), source_before)

    def test_foreign_and_edited_destinations_even_force_never_overwrite(self):
        target = self.base / "installed"
        destination = target / "cap-a"
        destination.mkdir(parents=True)
        marker = destination / "mine"
        marker.write_text("foreign")
        _, err = self.invoke("--target", target, "--apply", "--force", "cap-a", code=1)
        self.assertIn("foreign or edited", err)
        self.assertEqual(marker.read_text(), "foreign")
        shutil.rmtree(destination)
        self.invoke("--target", target, "--apply", "cap-a")
        marker = destination / "SKILL.md"
        marker.write_text("edited")
        self.invoke("--target", target, "--apply", "--force", "cap-a", code=1)
        self.assertEqual(marker.read_text(), "edited")

    def test_owned_source_update_needs_force_and_accepts_repeat(self):
        target = self.base / "installed"
        self.invoke("--target", target, "--apply", "cap-a")
        source = self.root / "skills/cap-a/SKILL.md"
        source.write_text(source.read_text() + "\nUpdated source.\n")
        self.invoke("--target", target, "--apply", "cap-a", code=1)
        self.invoke("--target", target, "--apply", "--force", "cap-a")
        self.assertEqual((target / "cap-a/SKILL.md").read_bytes(), source.read_bytes())
        self.invoke("--target", target, "--apply", "cap-a")

    def test_private_destination_results_and_foreign_links_are_conflicts(self):
        target = self.base / "installed"
        self.invoke("--target", target, "--apply", "cap-a")
        private = target / "cap-a/evals/results/private.md"
        private.parent.mkdir()
        private.write_text("local evidence")
        self.invoke("--target", target, "--apply", "--force", "cap-a", code=1)
        self.assertEqual(private.read_text(), "local evidence")
        shutil.rmtree(target / "cap-a")
        (target / "cap-a").symlink_to(self.root / "skills/cap-a", target_is_directory=True)
        self.invoke("--target", target, "--apply", "--force", "cap-a", code=1)
        self.assertTrue((target / "cap-a").is_symlink())

    def test_settings_preview_exact_apply_and_repeat(self):
        self.mode()
        path = self.write_settings({"theme": "dark", "permissions": {"deny": ["example"]}, "skillOverrides": {"unrelated": "off"}})
        before = path.read_bytes()
        out, _ = self.claude("cap-a")
        self.assertEqual(json.loads(out)["settings"]["changes"], [{"skill": "cap-a", "before": None, "after": "user-invocable-only"}])
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse((self.config / "skills").exists())
        self.claude("--apply", "cap-a")
        data = json.loads(path.read_text())
        self.assertEqual(data["theme"], "dark")
        self.assertEqual(data["permissions"], {"deny": ["example"]})
        self.assertEqual(data["skillOverrides"], {"unrelated": "off", "cap-a": "user-invocable-only"})
        before = path.read_bytes(), path.stat().st_mtime_ns
        out, _ = self.claude("--apply", "cap-a")
        self.assertEqual(json.loads(out)["settings"]["changes"], [])
        self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), before)
        self.assertFalse(any((self.config / "skills/cap-a").glob("settings*")))

    def test_settings_mode_change_removes_only_owned_override(self):
        self.mode()
        path = self.write_settings({"skillOverrides": {"cap-b": "user-invocable-only", "unrelated": "off"}})
        self.claude("--apply", "cap-a")
        self.mode("model")
        self.claude("--apply", "--force", "cap-a")
        self.assertEqual(json.loads(path.read_text())["skillOverrides"], {"cap-b": "user-invocable-only", "unrelated": "off"})

    def test_settings_mode_change_restores_previous_and_preserves_user_edits(self):
        self.mode()
        path = self.write_settings({"skillOverrides": {"cap-a": "name-only"}})
        self.claude("--apply", "cap-a")
        self.mode("model")
        self.claude("--apply", "--force", "cap-a")
        self.assertEqual(json.loads(path.read_text())["skillOverrides"]["cap-a"], "name-only")
        self.mode()
        self.claude("--apply", "--force", "cap-a")
        path.write_text('{"skillOverrides":{"cap-a":"off"}}')
        self.mode("model")
        self.claude("--apply", "--force", "cap-a")
        self.assertEqual(json.loads(path.read_text())["skillOverrides"]["cap-a"], "off")

    def test_settings_preexisting_stricter_and_manual_choices_stay_unowned(self):
        self.mode()
        for value in ("off", "user-invocable-only"):
            path = self.write_settings({"skillOverrides": {"cap-a": value}})
            self.claude("--apply", "--force", "cap-a")
            self.mode("model")
            self.claude("--apply", "--force", "cap-a")
            self.assertEqual(json.loads(path.read_text())["skillOverrides"]["cap-a"], value)
            self.mode()

    def test_settings_all_scopes_and_effective_precedence(self):
        self.mode()
        local = self.write_settings({"skillOverrides": {"cap-a": "on"}}, "local")
        _, err = self.claude("--apply", "cap-a", code=1)
        self.assertIn("higher-precedence", err)
        self.assertFalse((self.config / "skills").exists())
        self.claude("--apply", "cap-a", scope="local")
        self.assertEqual(json.loads(local.read_text())["skillOverrides"]["cap-a"], "user-invocable-only")
        local.unlink()
        self.write_settings({"skillOverrides": {"cap-a": "off"}})
        project = self.write_settings({"theme": "light"}, "project")
        self.claude("--apply", "cap-a", scope="project")
        self.assertNotIn("skillOverrides", json.loads(project.read_text()))
        # A higher disabled state also remains unchanged.
        self.write_settings({"skillOverrides": {"cap-a": "off"}}, "local")
        out, _ = self.claude("--apply", "cap-a")
        self.assertEqual(json.loads(out)["settings"]["effective"]["cap-a"], "off")

    def test_settings_rejects_malformed_without_any_install_or_overwrite(self):
        self.mode()
        path = self.write_settings({})
        for text in ('{', '[]', 'null', '{"theme":1,"theme":2}', '{"skillOverrides":[]}', '{"skillOverrides":{"cap-a":true}}', '{"skillOverrides":{"cap-a":{}}}', '{"skillOverrides":{"cap-a":"future"}}'):
            path.write_text(text)
            self.claude("--apply", "cap-a", code=1)
            self.assertEqual(path.read_text(), text)
            self.assertFalse((self.config / "skills").exists())
        path.write_text('{}')
        self.claude("--apply", "cap-a")

    def test_settings_changed_during_support_check_are_preserved(self):
        self.mode()
        path = self.write_settings({"theme": "original"})
        def changed(binary):
            path.write_text('{"theme":"edited elsewhere","newKey":true}')
            return {"version": "fixture"}
        with patch("claudesettings.support", side_effect=changed):
            _, err = self.claude("--apply", "cap-a", code=1)
        self.assertIn("changed after preview", err)
        self.assertEqual(json.loads(path.read_text()), {"theme": "edited elsewhere", "newKey": True})
        self.assertFalse((self.config / "skills").exists())
        self.claude("--apply", "cap-a")
        self.assertTrue(json.loads(path.read_text())["newKey"])

    def test_malformed_ownership_state_rejects_before_overwrite(self):
        self.mode()
        path = self.write_settings({"theme": "preserved"})
        state = path.with_name(path.name + ".skills-installer.json")
        for value in ('[]', '{"version":2,"overrides":{}}', '{"version":1,"overrides":{"cap-a":{"written":"off","previous":null}}}'):
            state.write_text(value)
            self.claude("--apply", "cap-a", code=1)
            self.assertEqual(state.read_text(), value)
            self.assertEqual(json.loads(path.read_text()), {"theme": "preserved"})
            self.assertFalse((self.config / "skills").exists())
        state.unlink()
        self.claude("--apply", "cap-a")
        receipt = self.config / "skills" / installer.STATE
        receipt.write_text('{"version":99}')
        self.claude("--apply", "--force", "cap-a", code=1)
        self.assertEqual(receipt.read_text(), '{"version":99}')

    def test_settings_requires_actual_target_and_installed_support(self):
        self.mode()
        _, err = self.invoke("--host", "claude", "--target", self.base / "wrong", "--settings", self.base / "wrong.json", "--settings-scope", "user", "--project-root", self.project, "--apply", "cap-a", code=1)
        self.assertIn("scope needs", err)
        self.binary.write_text('#!/bin/sh\nprintf "2.1.311 (Claude Code)\\n"\n')
        _, err = self.claude("--apply", "cap-a", code=1)
        self.assertIn("support not found", err)
        self.assertFalse((self.config / "settings.json").exists())
        self.assertFalse((self.config / "skills").exists())


class ProvenanceFixtures(FixtureBase):
    def setUp(self):
        super().setUp()
        self.skill = self.base / "adapted-skill"
        shutil.copytree(ROOT / "tests/check-skills/pass/adapted-skill", self.skill)

    def test_provenance_accepts_manifest_and_repeat(self):
        self.assertEqual(skills.check_skill(self.skill), [])
        self.assertEqual(skills.check_skill(self.skill), [])
        self.assertEqual(skills.check_skill(ROOT / "skills/project-guardrails"), [])

    def test_provenance_rejects_each_declared_contract_violation(self):
        original = {path.relative_to(self.skill): path.read_bytes() for path in self.skill.rglob("*") if path.is_file()}
        manifest = self.skill / "references/SOURCES.md"
        for before, after, expected in [
            ("# Sources", "# Wrong", "must start"),
            ("source_revision", "revision", "twelve manifest columns"),
            ("0123456789abcdef0123456789abcdef01234567", "0123456", "full 40-character"),
            ("a" * 64, "not-a-hash", "64-character"),
            ("| SKILL.md | Fixture method", "| missing.md | Fixture method", "missing"),
            ("| LICENSE-upstream |", "| LICENSE-missing |", "every contributor"),
            ("| none |", "| NOTICE-missing |", "missing"),
            ("| 2026 Fixture |", "| 2026 Secondary |", "copyright holder"),
            ("| MIT |", "| Apache-2.0 |", "NOTICE"),
            ("| SKILL.md | 012345", "| ../SKILL.md | 012345", "relative to its pinned"),
        ]:
            with self.subTest(expected=expected):
                for path, data in original.items():
                    (self.skill / path).write_bytes(data)
                text = manifest.read_text()
                self.assertIn(before, text)
                manifest.write_text(text.replace(before, after))
                self.assertIn(expected, "\n".join(skills.check_skill(self.skill)))
        for path, data in original.items():
            (self.skill / path).write_bytes(data)
        self.assertEqual(skills.check_skill(self.skill), [])

    def test_csv_manifest_header_accept_reject_and_repeat(self):
        import csv
        import provenance
        markdown = self.skill / "references/SOURCES.md"
        rows = provenance.manifest_rows(markdown)
        target = self.skill / "references/sources.csv"
        with target.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=provenance.COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        source = self.skill / "SKILL.md"
        source.write_text(source.read_text().replace("references/SOURCES.md", "references/sources.csv"))
        self.assertEqual(skills.check_skill(self.skill), [])
        self.assertEqual(skills.check_skill(self.skill), [])
        target.write_text(target.read_text().replace("source_revision", "revision"))
        self.assertIn("CSV header must be", "\n".join(skills.check_skill(self.skill)))

    def test_secondary_contributor_and_notice_accept_reject(self):
        manifest = self.skill / "references/SOURCES.md"
        original = manifest.read_text()
        row = original.splitlines()[-1]
        secondary = row.replace("| upstream |", "| secondary |")
        manifest.write_text(original + secondary + "\n")
        self.assertIn("LICENSE-secondary", "\n".join(skills.check_skill(self.skill)))
        secondary = secondary.replace("| LICENSE-upstream |", "| LICENSE-secondary |")
        manifest.write_text(original + secondary + "\n")
        shutil.copyfile(self.skill / "LICENSE-upstream", self.skill / "LICENSE-secondary")
        self.assertEqual(skills.check_skill(self.skill), [])
        manifest.write_text(manifest.read_text().replace("| none |", "| NOTICE-upstream |"))
        self.assertIn("NOTICE-upstream", "\n".join(skills.check_skill(self.skill)))
        (self.skill / "NOTICE-upstream").write_text("Original upstream notice (fixture).\n")
        self.assertEqual(skills.check_skill(self.skill), [])

    def test_provenance_rejects_legal_header_missing_contributor_and_unlinked_manifest(self):
        license_path = self.skill / "LICENSE-upstream"
        original = license_path.read_text()
        license_path.write_text(original.replace("Adapted files: SKILL.md", "Adapted files: another.md"))
        self.assertIn("header must name", "\n".join(skills.check_skill(self.skill)))
        license_path.write_text(original)
        manifest = self.skill / "references/SOURCES.md"
        text = manifest.read_text()
        row = text.splitlines()[-1]
        manifest.write_text(text + row.replace("| upstream |", "| secondary |") + "\n")
        self.assertIn("LICENSE-secondary", "\n".join(skills.check_skill(self.skill)))
        manifest.write_text(text)
        source = self.skill / "SKILL.md"
        source.write_text(source.read_text().replace("](references/SOURCES.md)", "](references/unlinked.md)"))
        self.assertIn("link one per-file manifest", "\n".join(skills.check_skill(self.skill)))

    def test_reference_size_contents_reject_accept_repeat(self):
        path = self.skill / "references/long.md"
        path.write_text("# Reference\n\n" + "A bounded reference rule.\n" * 100)
        self.assertIn("over 100 lines need a table of contents", "\n".join(skills.check_skill(self.skill)))
        path.write_text("# Reference\n\n## Contents\n\n- [Method](#method)\n\n## Method\n" + "A bounded reference rule.\n" * 100)
        self.assertEqual(skills.check_skill(self.skill), [])
        self.assertEqual(skills.check_skill(self.skill), [])

    def test_layout_frontmatter_and_retired_metadata_reject_accept(self):
        source = self.skill / "SKILL.md"
        text = source.read_text()
        source.write_text(text.replace("metadata:\n", "disable-model-invocation: true\nmetadata:\n  handoffs: \"cap-a\"\n"))
        output = "\n".join(skills.check_skill(self.skill))
        self.assertIn("unsupported frontmatter field", output)
        self.assertIn("handoffs is retired", output)
        source.write_text(text)
        directory = self.skill / "agents"
        directory.mkdir()
        policy = directory / "openai.yaml"
        policy.write_text("foreign")
        self.assertIn("only the exact generated", "\n".join(skills.check_skill(self.skill)))
        policy.write_text(hostconfig.USER_POLICY)
        self.assertEqual(skills.check_skill(self.skill), [])
        (self.skill / "other").mkdir()
        self.assertIn("unexpected skill directory", "\n".join(skills.check_skill(self.skill)))


class CLIFixtures(unittest.TestCase):
    def test_help_no_effect_stdout_and_no_required_host_tools(self):
        with tempfile.TemporaryDirectory(prefix="adoption-help-") as value:
            base = Path(value)
            env = {**os.environ, "HOME": str(base / "home"), "CLAUDE_CONFIG_DIR": str(base / "claude"), "CODEX_HOME": str(base / "codex"), "XDG_CONFIG_HOME": str(base / "config"), "PYTHONDONTWRITEBYTECODE": "1", "VALE_BIN": str(base / "missing-vale")}
            scripts = sorted(path for path in (ROOT / "skills").glob("*/scripts/*") if path.is_file() and path.suffix in (".sh", ".py"))
            # Assets/templates are deliberately excluded from executable checks.
            scripts += [ROOT / "scripts" / name for name in ("check-skills.py", "check-catalog.py", "build-profiles.py", "build-host-config.py", "install-skills.py")]
            for path in scripts:
                with self.subTest(script=str(path.relative_to(ROOT))):
                    command = [sys.executable, str(path)] if path.suffix == ".py" else [str(path)]
                    result = subprocess.run([*command, "--help"], cwd=base, env=env, text=True, capture_output=True, timeout=15)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue(result.stdout.strip(), result.stderr)
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(list(base.iterdir()), [])
            self.assertFalse(any("/assets/" in str(path) for path in scripts))


if __name__ == "__main__":
    unittest.main(verbosity=2)
