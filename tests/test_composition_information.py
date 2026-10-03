import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_composition_information.py"
SPEC = importlib.util.spec_from_file_location("verify_composition_information", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class CompositionInformationTests(unittest.TestCase):
    def test_witness(self):
        result = MODULE.verify_witness()
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["same_relation"])
        self.assertTrue(result["distinct_composition"])
        self.assertTrue(result["composability_ok"])

    def test_expected_relation(self):
        relation = MODULE.induced_relation(MODULE.PROCESSES)
        self.assertEqual(relation, {("A", "B"), ("B", "C"), ("A", "C")})

    def test_composition_outcomes_differ(self):
        self.assertEqual(MODULE.COMPOSITION_1[("g", "f")], "h")
        self.assertEqual(MODULE.COMPOSITION_2[("g", "f")], "k")


if __name__ == "__main__":
    unittest.main()
