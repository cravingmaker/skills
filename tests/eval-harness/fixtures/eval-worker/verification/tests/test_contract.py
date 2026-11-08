import unittest
from backend.service import label as backend
from frontend.client import label as frontend
class Contract(unittest.TestCase):
    def test_consumers(self):
        for fn in (backend, frontend):
            self.assertEqual(fn({"status":"active"}),"Active")
            self.assertEqual(fn({"status":"paused"}),"Paused")
