#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml==6.0.3"]
# ///
"""Offline tests for discovery evidence; no host, authentication, or model calls."""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
spec = importlib.util.spec_from_file_location("discovery", Path(sys.path[0]) / "measure-skill-discovery.py")
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)


class DiscoveryEvidence(unittest.TestCase):
    def test_codex_extracts_dynamic_roots_and_rows(self):
        block = "### Skill roots\n- `r0` = `/private/home/skills`\n### Available skills\n- sample: Review data (file: r0/sample/SKILL.md)"
        request = {"input": [{"content": [{"text": "<skills_instructions>Static instructions\n" + block + "\n</skills_instructions>"}]}]}
        self.assertEqual(discovery.listing(request, "codex"), block)

    def test_claude_excludes_following_reminders(self):
        request = {"messages": [{"content": [{"text": "The following skills are available for use with the Skill tool:\n\n- sample: Review data\n\nToday's date is later."}]}]}
        self.assertEqual(discovery.listing(request, "claude"), "- sample: Review data")

    def test_missing_listing_is_not_a_zero_cost_measurement(self):
        for host in ["codex", "claude"]:
            with self.assertRaisesRegex(ValueError, "update the extractor"):
                discovery.listing({"messages": []}, host)

    def test_whitespace_cleanup_is_not_truncation(self):
        self.assertEqual(discovery.description_state("Review data carefully.", "Review data\n\ncarefully.\n"), "whitespace-normalized")

    def test_distinguishes_truncation_name_only_and_omission(self):
        sources = {name: {"description": "Review data carefully."} for name in ["full", "short", "bare", "absent", "changed"]}
        rows = "- full: Review data carefully.\n- short: Review data…\n- bare\n- changed: Other instructions"
        self.assertEqual(discovery.description_states(rows, sources, "claude"),
                         {"full": "full", "short": "shortened", "bare": "name-only", "absent": "omitted", "changed": "changed"})

    def test_plugin_manifest_excludes_fixtures_and_unpublished_skills(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".claude-plugin").mkdir()
            (root / ".claude-plugin/plugin.json").write_text(json.dumps({"skills": ["./skills/published"]}))
            for relative in ["skills/published", "skills/in-progress/draft", "fixtures/example"]:
                path = root / relative
                path.mkdir(parents=True)
                (path / "SKILL.md").write_text("fixture")
            self.assertEqual(discovery.plugin_skills(root), [(root / "skills/published/SKILL.md").resolve()])

    def test_plugin_path_cannot_escape_cache(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".codex-plugin").mkdir()
            (root / ".codex-plugin/plugin.json").write_text(json.dumps({"skills": ["../other"]}))
            with self.assertRaisesRegex(ValueError, "escapes"):
                discovery.plugin_skills(root)

    def test_manifest_free_package_uses_only_standard_skill_children(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in ["skills/published", "skills/in-progress/draft", "fixtures/example"]:
                path = root / relative
                path.mkdir(parents=True)
                (path / "SKILL.md").write_text("fixture")
            self.assertEqual(discovery.plugin_skills(root), [(root / "skills/published/SKILL.md").resolve()])

    def test_replay_keeps_visibility_and_excludes_source_body(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            (source / "agents").mkdir(parents=True)
            original = "---\nname: sample\ndescription: 'Review data: preserve values.'\ndisable-model-invocation: true\n---\n\nPRIVATE_BODY_SENTINEL\n"
            (source / "SKILL.md").write_text(original)
            (source / "agents/openai.yaml").write_text("policy:\n  allow_implicit_invocation: false\n")
            discovery.replay_metadata(source / "SKILL.md", root / "installed")
            data = discovery.read_frontmatter(root / "installed/SKILL.md")
            self.assertEqual(data["description"], "Review data: preserve values.")
            self.assertTrue(data["disable-model-invocation"])
            self.assertNotIn("PRIVATE_BODY_SENTINEL", (root / "installed/SKILL.md").read_text())
            self.assertEqual((source / "SKILL.md").read_text(), original)
            self.assertEqual((root / "installed/agents/openai.yaml").read_text(), (source / "agents/openai.yaml").read_text())


if __name__ == "__main__":
    unittest.main()
