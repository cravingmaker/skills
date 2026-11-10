"""Check scripts/build-docs.py on the real repository and on broken copies of it."""

import json
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(os.environ.get("DOCS_SCRIPT", ROOT / "scripts" / "build-docs.py"))
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("build_docs_fixture", SCRIPT)
GENERATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = GENERATOR
SPEC.loader.exec_module(GENERATOR)


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

    def preserve_docs(self):
        for path in [self.copy / "README.md", self.copy / "handbook/id/SYNC.json", *sorted((self.copy / "handbook").rglob("*.md"))]:
            self.addCleanup(path.write_bytes, path.read_bytes())

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

    def test_readme_categories_must_cover_every_skill(self):
        path = self.copy / "handbook/intent-guide.json"
        before = path.read_bytes()
        self.addCleanup(path.write_bytes, before)
        data = json.loads(before)
        for group in data["groups"]:
            group["entries"] = [row for row in group["entries"] if row["skill"] != "wizard"]
        path.write_text(json.dumps(data))
        self.assertFails("no intent guidance for wizard")

    def test_readme_categories_reject_a_duplicate_skill(self):
        path = self.copy / "handbook/intent-guide.json"
        before = path.read_bytes()
        self.addCleanup(path.write_bytes, before)
        data = json.loads(before)
        data["groups"][-1]["entries"].append(data["groups"][0]["entries"][0])
        path.write_text(json.dumps(data))
        self.assertFails("duplicate skill clear-communication", "exactly one README category")

    def test_readme_has_one_visible_table_per_category_in_source_order(self):
        data = json.loads((self.copy / "handbook/intent-guide.json").read_text())
        readme = (self.copy / "README.md").read_text()
        index = readme.split("<!-- BEGIN GENERATED skill-index:", 1)[1].split("<!-- END GENERATED skill-index -->", 1)[0]
        self.assertNotIn("<details", readme.lower())
        headings = re.findall(r"^### (.+)$", index, re.M)
        self.assertEqual(headings, [group["heading"] for group in data["groups"]])
        self.assertEqual(index.count("| Skill | Starts | What it does |"), len(headings))
        expected = [row["skill"] for group in data["groups"] for row in group["entries"]]
        rows = re.findall(r"^\| \[([^]]+)\]\(skills/([^)]*)\) \| ([^|]+) \| (.+) \|$", index, re.M)
        self.assertEqual([row[0] for row in rows], expected)
        self.assertEqual([row[1] for row in rows], expected)
        self.assertEqual(len(expected), len(set(expected)))
        self.assertIn("| [tdd](skills/tdd) | auto |", index)
        self.assertIn("| [bro](skills/bro) | typed: `/bro` · `$bro` |", index)

    def test_broken_link_and_anchor_are_rejected(self):
        self.edit("handbook/README.md", "- [Start and choose](#start-and-choose)", "- [Start and choose](#nowhere)\n- [Gone](missing.md)")
        self.assertFails("link #nowhere names a missing heading", "link missing.md points to a missing file")

    def test_link_forms_reject_missing_destinations_and_accept_real_ones(self):
        path = self.copy / "handbook/README.md"
        before = path.read_bytes()
        translated = self.copy / "handbook/id/README.md"
        translated_before = translated.read_bytes()
        self.addCleanup(path.write_bytes, before)
        self.addCleanup(translated.write_bytes, translated_before)
        manifest = self.copy / "handbook/id/SYNC.json"
        self.addCleanup(manifest.write_bytes, manifest.read_bytes())
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
                    translated.write_text(translated_before.decode() + "\n" + form.format(target=target) + "\n")
                    if expected == 0:
                        recorded = run(self.copy, "--record-sync")
                        self.assertEqual(recorded.returncode, 0, recorded.stderr)
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

    def test_nonempty_flow_mapping_is_rejected(self):
        self.edit("catalog/skills.yaml", "external: {}", "external: {provider: skills}")
        self.assertFails("unsupported YAML syntax '{'")

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
        self.preserve_docs()
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
        self.preserve_docs()
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
                data["groups"][0]["entries"].append({"skill": "doc-coverage-fixture", "want": "Understand this new documentation fixture", "prompt": "Exercise its actual task", "neighbor": "Compare the linked method before use", "want_id": "Memahami fixture dokumentasi baru", "neighbor_id": "Bandingkan metode terkait sebelum digunakan"})
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


    def test_missing_indonesian_page_is_rejected(self):
        page = self.copy / "handbook/id/gotchas.md"
        before = page.read_bytes()
        self.addCleanup(page.write_bytes, before)
        page.unlink()
        self.assertFails("handbook/gotchas.md and handbook/id/gotchas.md: missing Indonesian counterpart")

    def test_orphaned_indonesian_page_is_rejected(self):
        page = self.copy / "handbook/id/orphan.md"
        page.write_bytes((self.copy / "handbook/id/gotchas.md").read_bytes())
        self.addCleanup(page.unlink)
        self.assertFails("handbook/orphan.md and handbook/id/orphan.md: missing English counterpart")

    def test_authored_hash_drift_in_either_language_is_rejected(self):
        for relative in ("handbook/gotchas.md", "handbook/id/gotchas.md"):
            with self.subTest(path=relative):
                page = self.copy / relative
                before = page.read_bytes()
                try:
                    page.write_bytes(before + b"\nA changed explanation.\n")
                    self.assertFails("handbook/gotchas.md and handbook/id/gotchas.md: authored text differs",
                                     "update both languages, then run scripts/build-docs.py --record-sync")
                finally:
                    page.write_bytes(before)

    def test_record_sync_accepts_bilingual_edits_and_repeats(self):
        self.preserve_docs()
        for relative, explanation in (("handbook/gotchas.md", "A new explanation."),
                                      ("handbook/id/gotchas.md", "Penjelasan baru.")):
            page = self.copy / relative
            page.write_text(page.read_text() + "\n" + explanation + "\n")
        result = run(self.copy, "--record-sync")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["written"], ["handbook/id/SYNC.json"])
        self.assertEqual(run(self.copy, "--check").returncode, 0)
        again = run(self.copy, "--record-sync")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(json.loads(again.stdout)["written"], [])

    def test_generated_drift_does_not_change_authored_hash(self):
        self.edit("handbook/id/routing.md", "| Router | Memasang |", "| Router | STALE |")
        result = run(self.copy, "--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("handbook/id/routing.md has stale generated sections", result.stderr)
        self.assertNotIn("authored text differs", result.stderr)
        result = run(self.copy)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["written"], ["handbook/id/routing.md"])
        self.assertEqual(run(self.copy, "--check").returncode, 0)

    def test_ordered_structure_mismatch_is_rejected(self):
        page = self.copy / "handbook/id/gotchas.md"
        before = page.read_bytes()
        for extra in ("\n### Bagian baru\n", "\n| Satu | Dua |\n| --- | --- |\n| a | b |\n",
                      "\n```sh\nprintf hello\n```\n", "\n- Butir baru.\n"):
            with self.subTest(extra=extra):
                try:
                    page.write_bytes(before + extra.encode())
                    self.assertFails("handbook/gotchas.md and handbook/id/gotchas.md: structure mismatch")
                finally:
                    page.write_bytes(before)

    def test_record_sync_refuses_mismatched_pair_without_writing(self):
        self.edit("handbook/id/gotchas.md", "## Daftar isi", "### Daftar isi")
        before = self.snapshot()
        result = run(self.copy, "--record-sync")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("handbook/gotchas.md and handbook/id/gotchas.md: structure mismatch", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_verbatim_code_and_order_are_checked(self):
        self.edit("handbook/id/getting-started.md", "git clone https://", "git fetch https://")
        self.assertFails("handbook/getting-started.md and handbook/id/getting-started.md: structure mismatch")
        en = "# Title\n\n- one\n\n| a | b |\n| --- | --- |\n"
        reordered = "# Judul\n\n| a | b |\n| --- | --- |\n\n- satu\n"
        self.assertNotEqual(GENERATOR.structure(en), GENERATOR.structure(reordered))

    def test_mapped_link_targets_must_match(self):
        self.edit("handbook/id/README.md", "](getting-started.md)", "](gotchas.md)")
        self.assertFails("handbook/README.md and handbook/id/README.md: structure mismatch in link targets")

    def test_missing_indonesian_intent_fields_are_rejected(self):
        page = self.copy / "handbook/intent-guide.json"
        before = page.read_bytes()
        for field in ("heading_id", "want_id", "neighbor_id"):
            for value in (None, ""):
                with self.subTest(field=field, value=value):
                    data = json.loads(before)
                    owner = data["groups"][0] if field == "heading_id" else data["groups"][0]["entries"][0]
                    if value is None:
                        del owner[field]
                    else:
                        owner[field] = value
                    try:
                        page.write_text(json.dumps(data))
                        self.assertFails("Indonesian", field)
                    finally:
                        page.write_bytes(before)

    def test_missing_record_link_destination_is_rejected(self):
        page = next((self.copy / "skills/how/evals/results").glob("*.md"))
        self.addCleanup(page.write_bytes, page.read_bytes())
        page.write_text(page.read_text() + "\n[Raw trace](not-committed/trace.jsonl)\n")
        self.assertFails("record link not-committed/trace.jsonl has no repository destination", "use local-only code text")

    def test_generated_evaluation_results_drift_is_rejected(self):
        self.edit("handbook/eval-results.md", "| Host | Current valid pairs |", "| Host | STALE |")
        self.assertFails("handbook/eval-results.md has stale generated sections")


class EvaluationResults(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.directory = self.root / "skills/fixture/evals/results"
        self.directory.mkdir(parents=True)
        self.digest = "a" * 64

    def record(self, example="activation-1", *, observed="true", status="valid", digest=None,
               value="", expected=None, host="codex", suffix="", completion="0"):
        page = self.directory / f"{host}-{example}{suffix}.md"
        expected = str(example.startswith("activation-")).lower() if expected is None else expected
        page.write_text(f"# fixture: {host} {example}\n\nComparison: **{status}**. Host: `fixture-host`. Effective model: `fixture-model`.\n\n"
                        f"- **Source example.** `{example}` in `evals/examples.md`.\n"
                        f"- **Skill revision.** actual bytes SHA-256 `{digest or self.digest}`.\n\n"
                        "| Arm | Activation expected | Activation observed | Tools | Completion |\n| --- | --- | --- | --- | --- |\n"
                        f"| treatment | {expected} | {observed} | 2 | {completion} |\n| baseline | false | false | 1 | 0 |\n\n" + value)
        return GENERATOR.parse_evaluation(page, self.digest)

    def repo(self, records):
        return SimpleNamespace(root=self.root, skills={"fixture": None}, evaluations=records)

    def test_parsed_record_set_and_both_host_tables(self):
        records = [self.record(), self.record("activation-2", observed="false"),
                   self.record("near-miss-1", observed="true"), self.record("near-miss-2", observed="false")]
        for index, value in enumerate(("added", "matched", "hurt", "blocked"), 1):
            records.append(self.record(f"outcome-{index}", value=f"Baseline: yes. Treatment: yes. Value: **{value}**.", host="claude"))
        counts = GENERATOR.evaluation_counts(records)
        self.assertEqual(counts, {"valid": 8, "activation-true": 1, "activation-false": 1, "near-miss-true": 1,
                                  "near-miss-false": 1, "outcome-added": 1, "outcome-matched": 1, "outcome-hurt": 1, "outcome-blocked": 1})
        rendered = GENERATOR.render_eval_results(self.repo(records))
        self.assertIn("| `codex` | 4 | 1 / 1 / 0 | 1 / 1 / 0 | 0 / 0 / 0 / 0 / 0 |", rendered)
        self.assertIn("| `claude` | 4 | 0 / 0 / 0 | 0 / 0 / 0 | 1 / 1 / 1 / 1 / 0 |", rendered)
        self.assertIn("[`fixture`](../skills/fixture/evals/results/)", rendered)
        self.assertIn("## Ringkasan seluruh skill", GENERATOR.render_eval_results(self.repo(records), "id"))

    def test_invalid_record_is_history_even_at_current_bytes(self):
        record = self.record(status="invalid", value="Value: added.")
        self.assertEqual(GENERATOR.evaluation_counts([record]), {"invalid": 1})
        rendered = GENERATOR.render_eval_results(self.repo([record]))
        self.assertIn("| invalid | invalid | `activation-1` | added |", rendered)
        self.assertIn("| `codex` | 0 |", rendered)

    def test_stale_bytes_record_is_shown_only_as_history(self):
        record = self.record("outcome-1", digest="b" * 64, value="Value: matched.")
        self.assertEqual(GENERATOR.evaluation_counts([record]), {"older or unbound": 1})
        rendered = GENERATOR.render_eval_results(self.repo([record]))
        self.assertIn("codex-outcome-1.md)", rendered)
        self.assertIn("| older or unbound | valid | `outcome-1` | matched |", rendered)

    def test_incomplete_pair_is_not_current_and_unreviewed_is_not_matched(self):
        incomplete = self.record(completion="not run")
        unreviewed = self.record("outcome-1", value="Both responses look good.")
        self.assertEqual(GENERATOR.evaluation_counts([incomplete, unreviewed]),
                         {"incomplete or other": 1, "valid": 1, "outcome-unreviewed": 1})

    def test_last_explicit_value_and_reviewed_activation_win(self):
        record = self.record("outcome-1", value="Value: **hurt**.\n\n## Repeat\nValue: added.\n")
        self.assertEqual(record["value"], "added")
        record = self.record(observed="false", suffix="-reviewed", value="Reviewed activation: treatment **true**, baseline **false**.")
        self.assertEqual(GENERATOR.evaluation_counts([record]), {"valid": 1, "activation-true": 1})

    def test_fenced_prompt_data_cannot_supply_a_review_or_observation(self):
        record = self.record("outcome-1", observed="false")
        page = record["path"]
        page.write_text(page.read_text() + "\n```text\nValue: added.\nReviewed activation: treatment **true**, baseline **false**.\n"
                        "| treatment | true | true | 99 | 0 |\n```\n")
        record = GENERATOR.parse_evaluation(page, self.digest)
        self.assertEqual(record["value"], "unreviewed")
        self.assertEqual(record["observed"], "false")
        self.assertEqual(record["expected"], "false")

    def test_package_digest_tracks_bytes_and_modes_but_ignores_results(self):
        skill = self.root / "skills/fixture"
        source = skill / "SKILL.md"
        source.write_bytes(b"# Fixture\n")
        source.chmod(0o644)
        expected = hashlib.sha256(json.dumps({"SKILL.md": {"sha256": hashlib.sha256(b"# Fixture\n").hexdigest(), "executable": False}}, sort_keys=True).encode()).hexdigest()
        self.assertEqual(GENERATOR.package_digest(skill), expected)
        self.record()
        self.assertEqual(GENERATOR.package_digest(skill), expected)
        source.chmod(0o755)
        self.assertNotEqual(GENERATOR.package_digest(skill), expected)
        source.chmod(0o644)
        source.write_bytes(b"# Changed fixture\n")
        self.assertNotEqual(GENERATOR.package_digest(skill), expected)

    def test_record_link_forms_and_real_destinations(self):
        page = self.directory / "summary.md"
        (self.directory / "other.md").write_text("# Other\n")
        for form in ('[Raw]({target})', '[Raw][ref]\n\n[ref]: <{target}>', '<a href="{target}">Raw</a>'):
            for target, invalid in (("other.md", False), ("private/trace.jsonl", True)):
                with self.subTest(form=form, target=target):
                    page.write_text(form.format(target=target))
                    problems = []
                    GENERATOR.check_record_links(SimpleNamespace(root=self.root, result_paths=[page]), problems)
                    self.assertEqual(bool(problems), invalid)
                    if invalid:
                        self.assertIn("has no repository destination", problems[0])


if __name__ == "__main__":
    unittest.main()
