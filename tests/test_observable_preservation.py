import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_observable_preservation.py"
SPEC = importlib.util.spec_from_file_location("verify_observable_preservation", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

class ObservablePreservationTests(unittest.TestCase):
    def test_r10_witness(self):
        r=MODULE.verify()
        self.assertTrue(r["parity_exact"])
        self.assertTrue(r["half_bound_ok"])
        self.assertAlmostEqual(r["normalized_epsilon"],2/3)
        self.assertAlmostEqual(r["normalized_midpoint_max_error"],1/3)

    def test_zero_oscillation_exact(self):
        f=lambda x:7
        self.assertEqual(MODULE.oscillation(f,[0,1,2]),0)

if __name__=="__main__":
    unittest.main()
