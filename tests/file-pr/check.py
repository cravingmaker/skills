"""Check the shared delivery contract; no host access or model calls."""
from pathlib import Path
import hashlib
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
NAMES = ['file-pr', 'pr', 'babysit-pr', 'fix-ci', 'leaving-pr-comments', 'modernize', 'takeover', 'full-send', 'full-stop']
EXPECTED = '38c62d146861d6b7bf39765bbf043411dfafe2fd4547b5ee0634d39285e5f241'

def valid(text):
    blocks = re.findall(r"^## Delivery contract\n\n((?:- .+\n)+)", text, re.M)
    return len(blocks) == 1 and hashlib.sha256(blocks[0].encode()).hexdigest() == EXPECTED

class DeliveryContract(unittest.TestCase):
    def test_all_nine_match(self):
        for name in NAMES:
            with self.subTest(skill=name):
                self.assertTrue(valid((ROOT/"skills"/name/"SKILL.md").read_text()))

    def test_watch_authority_drift_rejected(self):
        text = (ROOT/"skills/file-pr/SKILL.md").read_text()
        self.assertFalse(valid(text.replace("Only the root agent watches a PR", "Every child watches a PR")))

    def test_missing_and_duplicate_blocks_rejected(self):
        text = (ROOT/"skills/file-pr/SKILL.md").read_text()
        self.assertFalse(valid(text.replace("## Delivery contract", "## Retired contract")))
        self.assertFalse(valid(text + "\n" + text))

    def test_repeat_check_does_not_change_sources(self):
        path = ROOT/"skills/full-stop/SKILL.md"
        original = path.read_bytes()
        self.assertTrue(valid(original.decode()))
        self.assertTrue(valid(original.decode()))
        self.assertEqual(path.read_bytes(), original)

if __name__ == "__main__":
    unittest.main()
