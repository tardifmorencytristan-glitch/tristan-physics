import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_quotient_congruence.py"
SPEC = importlib.util.spec_from_file_location("verify_quotient_congruence", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class QuotientCongruenceTests(unittest.TestCase):
    def test_parity_is_congruence_for_addition(self):
        self.assertTrue(MODULE.parity_congruence_check(limit=6))

    def test_non_congruence_witness_detected(self):
        self.assertTrue(MODULE.invalid_witness())

    def test_parity_examples(self):
        self.assertTrue(MODULE.same_parity(2, 4))
        self.assertTrue(MODULE.same_parity(-1, 3))
        self.assertFalse(MODULE.same_parity(2, 3))


if __name__ == "__main__":
    unittest.main()
