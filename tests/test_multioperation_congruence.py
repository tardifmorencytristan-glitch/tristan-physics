import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_multioperation_congruence.py"
SPEC = importlib.util.spec_from_file_location("verify_multioperation_congruence", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class MultiOperationCongruenceTests(unittest.TestCase):
    def test_z4_expected_congruences(self):
        result = MODULE.verify_z4()
        self.assertTrue(result["matches_expected"])
        self.assertEqual(result["partition_count"], 15)

    def test_even_odd_partition_preserves_both(self):
        partition = ((0, 2), (1, 3))
        add = lambda a, b: (a + b) % 4
        mul = lambda a, b: (a * b) % 4
        self.assertTrue(MODULE.congruent(partition, add, 2, 4))
        self.assertTrue(MODULE.congruent(partition, mul, 2, 4))

    def test_bad_partition_fails(self):
        partition = ((0, 1), (2, 3))
        add = lambda a, b: (a + b) % 4
        mul = lambda a, b: (a * b) % 4
        self.assertFalse(MODULE.congruent(partition, add, 2, 4))
        self.assertFalse(MODULE.congruent(partition, mul, 2, 4))


if __name__ == "__main__":
    unittest.main()
