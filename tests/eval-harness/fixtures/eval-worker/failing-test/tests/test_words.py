import unittest
from word_count import count_words
class Words(unittest.TestCase):
    def test_three(self): self.assertEqual(count_words("three short words"), 3)
    def test_empty(self): self.assertEqual(count_words(""), 0)
