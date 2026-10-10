import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from metrics import calculate, number
class MetricsTest(unittest.TestCase):
    def test_observed_zero(self):
        self.assertEqual(calculate({"reach":100,"shares":0})["shares_per_1000"],0)
    def test_unknown_is_not_zero(self):
        self.assertIsNone(calculate({"reach":100,"shares":""})["shares_per_1000"])
    def test_zero_denominator(self):
        self.assertIsNone(calculate({"reach":0,"shares":10})["shares_per_1000"])
    def test_partial_er(self):
        self.assertIsNone(calculate({"reach":100,"likes":10})["er_reach_pct"])
    def test_metrics_do_not_merge_reposts(self):
        r=calculate({"reach":1000,"likes":40,"comments":10,"saves":12,"shares":8,"reposts":2})
        self.assertAlmostEqual(r["er_reach_pct"],7)
        self.assertEqual(r["reposts_per_1000"],2)
    def test_invalid_source(self):
        for v in (-1,"NaN","inf"):
            with self.assertRaises(ValueError): number(v)
