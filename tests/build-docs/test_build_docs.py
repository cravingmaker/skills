"""Check scripts/build-docs.py on the real repository and on broken copies of it."""

import json
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(os.environ.get("DOCS_SCRIPT", ROOT / "scripts" / "build-docs.py"))


def run(root: Path, *arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *arguments, "--root", str(root)],
                          capture_output=True, text=True, timeout=120)


def copy_repository(destination: Path) -> None:
    """Copy the tracked shape of the repository; raw eval evidence folders stay out."""
    def ignore(directory, names):
        parts = Path(directory).relative_to(ROOT).parts
        skipped = {name for name in names if name in (".git", "__pycache__", ".venv", "node_modules")}
        if len(parts) == 4 and parts[0] == "skills" and parts[2:] == ("evals", "results"):
            skipped |= {name for name in names if (Path(directory) / name).is_dir()}
        return skipped
    shutil.copytree(ROOT, destination, ignore=ignore)


class BuildDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.copy = Path(cls.temporary.name) / "repo"
        copy_repository(cls.copy)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def edit(self, relative: str, old: str, new: str) -> None:
        """Change one file in the copy for this test only."""
        path = self.copy / relative
        original = path.read_bytes()
        self.addCleanup(path.write_bytes, original)
        text = original.decode("utf-8")
        self.assertIn(old, text, f"fixture text missing from {relative}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def assertFails(self, *needles: str) -> None:
        result = run(self.copy, "--check")
        self.assertEqual(result.returncode, 1, result.stderr)
        for needle in needles:
            self.assertIn(needle, result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_repository_docs_are_current(self):
        result = run(ROOT, "--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["problems"], 0)

    def test_help_and_usage(self):
        before = (self.copy / "README.md").read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0)
        self.assertIn("--check", result.stdout)
        self.assertEqual((self.copy / "README.md").read_bytes(), before)
        self.assertEqual(run(self.copy, "--bogus").returncode, 2)

    def test_stale_section_is_reported_then_rewritten_once(self):
        self.edit("README.md", "capability skills.", "capability skills. STALE ROW.")
        self.assertFails("README.md has stale generated sections")
        written = run(self.copy)
        self.assertEqual(written.returncode, 0, written.stderr)
        self.assertEqual(json.loads(written.stdout)["written"], ["README.md"])
        again = run(self.copy)
        self.assertEqual(json.loads(again.stdout)["written"], [])
        self.assertEqual(run(self.copy, "--check").returncode, 0)

    def test_catalog_change_makes_docs_stale(self):
        self.edit("catalog/skills.yaml", "  tdd:\n    kind: capability\n", "  tdd:\n    kind: capability\n    invocation: user\n")
        self.assertFails("handbook/typed-commands.md has stale generated sections", "add a section headed `/tdd`")

    def test_agent_facing_file_may_not_point_into_handbook(self):
        self.edit("skills/tdd/SKILL.md", "# Test-driven development\n", "# Test-driven development\n\nSee ../../handbook/gotchas.md first.\n")
        self.assertFails("skills/tdd/SKILL.md:", "must not point into handbook/")

    def test_handbook_page_needs_its_first_line(self):
        self.edit("handbook/gotchas.md", "> **Human documentation.**", "> **Documentation.**")
        self.assertFails("handbook/gotchas.md: the first line must be exactly")

    def test_choosing_page_must_cover_every_skill(self):
        path = self.copy / "handbook/intent-guide.json"
        before = path.read_bytes()
        self.addCleanup(path.write_bytes, before)
        data = json.loads(before)
        for group in data["groups"]:
            group["entries"] = [row for row in group["entries"] if row["skill"] != "wizard"]
        path.write_text(json.dumps(data))
        self.assertFails("no intent guidance for wizard")

    def test_broken_link_and_anchor_are_rejected(self):
        self.edit("handbook/README.md", "- [Start and choose](#start-and-choose)", "- [Start and choose](#nowhere)\n- [Gone](missing.md)")
        self.assertFails("link #nowhere names a missing heading", "link missing.md points to a missing file")

    def test_link_forms_reject_missing_destinations_and_accept_real_ones(self):
        path = self.copy / "handbook/README.md"
        before = path.read_bytes()
        self.addCleanup(path.write_bytes, before)
        forms = (
            '[Guide]({target} "Title")',
            '[Guide](<{target}>)',
            '[Guide][target]\n\n[target]: {target}',
            '[Guide][]\n\n[Guide]: <{target}> "Title"',
            '[Guide]\n\n[Guide]: {target}',
            '<a href="{target}">Guide</a>',
            "<a href='{target}'>Guide</a>",
            '<a href={target}>Guide</a>',
        )
        for form in forms:
            for target, expected in (("getting-started.md", 0), ("missing-guide.md", 1),
                                     ("getting-started.md#missing-heading", 1)):
                with self.subTest(form=form, target=target):
                    path.write_text(before.decode() + "\n" + form.format(target=target) + "\n")
                    result = run(self.copy, "--check")
                    self.assertEqual(result.returncode, expected, result.stderr)
                    if expected:
                        self.assertIn("link " + target, result.stderr)

    def test_unknown_skill_pointer_and_command_are_rejected(self):
        self.edit("handbook/recommended-flow.md", "## Choose the starting point\n", "## Choose the starting point\n\nUse the `no-such-skill` skill, or type `/no-such-command`.\n")
        self.assertFails("'the `no-such-skill` skill' names no current skill", "command `/no-such-command` names no current skill")

    def test_malformed_markers_are_rejected(self):
        self.edit("handbook/routing.md", "<!-- END GENERATED routes -->", "")
        self.assertFails("generated block routes needs its own END GENERATED routes line")

    def test_unsupported_yaml_fails_with_a_message(self):
        self.edit("skills/tdd/SKILL.md", "description: Test-driven", "description: >\n  Test-driven")
        self.assertFails("skills/tdd/SKILL.md:3: unsupported YAML syntax")

    def test_unsupported_plain_scalars_fail_before_any_write(self):
        path = self.copy / "skills/tdd/SKILL.md"
        before = path.read_bytes()
        self.addCleanup(path.write_bytes, before)
        import re
        for value in ("]", "}", ",bad", "- nested", "? key", "true", "null", "42",
                      "0x12", "1.5", ".inf", "2026-11-10"):
            with self.subTest(value=value):
                path.write_text(re.sub(r"(?m)^description: .*?$", "description: " + value, before.decode()))
                snapshot = self.snapshot()
                result = run(self.copy)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("unsupported", result.stderr)
                self.assertIn("quote", result.stderr)
                self.assertEqual(snapshot, self.snapshot())

    def test_parser_matches_pyyaml(self):
        uv = shutil.which("uv")
        if not uv:
            self.skipTest("uv is not installed; validate.sh requires it")
        probe = (
            "import importlib.util, json, re, sys\n"
            "from pathlib import Path\n"
            "import yaml\n"
            f"root, script = Path({str(ROOT)!r}), Path({str(SCRIPT)!r})\n"
            "sys.path.insert(0, str(script.parent))\n"
            "spec = importlib.util.spec_from_file_location('build_docs', script)\n"
            "module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)\n"
            "texts = {'catalog': (root / 'catalog/skills.yaml').read_text()}\n"
            "for path in sorted(root.glob('skills/*/SKILL.md')):\n"
            "    texts[str(path)] = re.match(r'---\\n(.*?)\\n---\\n', path.read_text(), re.S)[1]\n"
            "bad = [name for name, text in texts.items() if module.load_yaml(text, name) != yaml.safe_load(text)]\n"
            "print(json.dumps({'checked': len(texts), 'different': bad}))\n"
        )
        result = subprocess.run([uv, "run", "--quiet", "--no-project", "--with", "pyyaml==6.0.3", "python3", "-c", probe],
                                capture_output=True, text=True, timeout=300, cwd=tempfile.gettempdir())
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertGreater(report["checked"], 1)
        self.assertEqual(report["different"], [])


    def snapshot(self):
        return {path.relative_to(self.copy).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.copy.rglob("*") if path.is_file()}

    def test_agent_boundary_variants(self):
        target = "hand" + "book/README.md"
        cases = [("AGENTS.md", "[guide](hand" + "book)"),
                 ("AGENTS.md", "[guide](" + target + ")"),
                 ("CLAUDE.local.md", "`" + target + "`"),
                 ("nested/AGENTS.override.md", "[guide](../" + target + ")"),
                 ("skills/tdd/references/extra.md", "[guide]: ../../" + target),
                 ("skills/tdd/assets/extra.txt", '<a href="../../' + target + '">guide</a>'),
                 ("docs/extra.md", "[guide](../handbook%2FREADME.md)"),
                 ("catalog/extra.md", "[guide](../handbook&#47;README.md)"),
                 ("template/extra.md", "[guide](../" + target + ")"),
                 ("template-role/extra.md", "[guide](../" + target + ")"),
                 ("scripts/extra.js", "// [guide](../" + target + ")")]
        for relative, content in cases:
            with self.subTest(path=relative):
                path = self.copy / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                old = path.read_bytes() if path.exists() else None
                try:
                    path.write_text((old.decode() if old else "") + "\n" + content + "\n")
                    self.assertFails(relative + ":", "must not point into " + "hand" + "book/")
                finally:
                    if old is None:
                        path.unlink()
                    else:
                        path.write_bytes(old)

    def test_broken_input_never_partially_writes(self):
        self.edit("README.md", "capability skills.", "capability skills. STALE ROW.")
        self.edit("handbook/routing.md", "<!-- END GENERATED routes -->", "")
        before = self.snapshot()
        result = run(self.copy)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("needs its own END", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_invalid_dependency_and_profile_drift(self):
        path = self.copy / "skills/grill-me/SKILL.md"
        before = path.read_bytes()
        try:
            path.write_text(before.decode().replace('requires: "grilling"', 'requires: "missing-input-fixture"'))
            self.assertFails("metadata.requires names missing-input-fixture")
        finally:
            path.write_bytes(before)
        self.edit("catalog/profiles/agent-orchestrator.txt", "agent-briefing\n", "unknown-profile-fixture\n")
        self.assertFails("profile drift")

    def test_direct_resource_routes_are_generated(self):
        relative = "skills/codebase-design/references/expert-design.md"
        path = self.copy / relative
        # Use an existing directly linked file instead of an unreferenced test resource.
        entry = (self.copy / "skills/codebase-design/SKILL.md").read_text()
        import re
        relative = "skills/codebase-design/" + re.search(r"\]\((references/[^)#]+\.md)", entry)[1]
        path = self.copy / relative
        before = path.read_bytes()
        for home in ("handbook/routing.md", "handbook/skills.md"):
            page = self.copy / home
            self.addCleanup(page.write_bytes, page.read_bytes())
        self.addCleanup(path.write_bytes, before)
        path.write_text(before.decode() + "\nUse the `wizard` skill for the human-only step.\n")
        self.assertFails("stale generated sections")
        result = run(self.copy)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("`wizard`", (self.copy / "handbook/routing.md").read_text().split("<!-- BEGIN GENERATED routes", 1)[1])

    def test_inline_code_label_link_is_checked(self):
        self.edit("handbook/README.md", "## Why this lives separately\n", "## Why this lives separately\n\n[`code label`](missing-code-label.md)\n")
        self.assertFails("missing-code-label.md points to a missing file")

    def test_new_catalog_entry_requires_useful_guidance(self):
        directory = self.copy / "skills/doc-coverage-fixture"
        try:
            directory.mkdir()
            (directory / "evals").mkdir()
            (directory / "SKILL.md").write_text('---\nname: doc-coverage-fixture\ndescription: Document a new capability.\n---\n\n# Fixture\n')
            (directory / "evals/examples.md").write_text('## Activation\n- Do it.\n## Near miss\n- Do another job.\n## Outcome\n- The result exists.\n')
            catalog = self.copy / "catalog/skills.yaml"
            before = catalog.read_bytes()
            try:
                catalog.write_text(before.decode().replace("skills:\n", "skills:\n  doc-coverage-fixture:\n    kind: capability\n    roles: [all]\n    status: unevaluated\n", 1))
                self.assertFails("no intent guidance for doc-coverage-fixture")
                pages = [self.copy / "README.md", *sorted((self.copy / "handbook").glob("*.md"))]
                for page in pages:
                    self.addCleanup(page.write_bytes, page.read_bytes())
                guide = self.copy / "handbook/intent-guide.json"
                self.addCleanup(guide.write_bytes, guide.read_bytes())
                data = json.loads(guide.read_text())
                data["groups"][0]["entries"].append({"skill": "doc-coverage-fixture", "want": "Understand this new documentation fixture", "prompt": "Exercise its actual task", "neighbor": "Compare the linked method before use"})
                guide.write_text(json.dumps(data))
                generated = run(self.copy)
                self.assertEqual(generated.returncode, 0, generated.stderr)
                self.assertEqual(run(self.copy, "--check").returncode, 0)
                entry = (self.copy / "handbook/skills.md").read_text().split("### `doc-coverage-fixture`", 1)[1].split("### `", 1)[0]
                self.assertIn("no public evaluation summaries recorded", entry)
                self.assertNotIn("evals/results/", entry)
            finally:
                catalog.write_bytes(before)
        finally:
            shutil.rmtree(directory)


if __name__ == "__main__":
    unittest.main()
