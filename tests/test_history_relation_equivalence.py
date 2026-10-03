import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_history_relation_equivalence.py"
SPEC = importlib.util.spec_from_file_location("verify_history_relation_equivalence", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class HistoryRelationEquivalenceTests(unittest.TestCase):
    def test_empty_relation(self):
        ok, reconstructed = MODULE.verify_relation(set())
        self.assertTrue(ok)
        self.assertEqual(reconstructed, set())

    def test_asymmetric_relation(self):
        relation = {(0, 1)}
        ok, reconstructed = MODULE.verify_relation(relation)
        self.assertTrue(ok)
        self.assertEqual(reconstructed, relation)

    def test_bidirectional_relation(self):
        relation = {(0, 1), (1, 0)}
        ok, reconstructed = MODULE.verify_relation(relation)
        self.assertTrue(ok)
        self.assertEqual(reconstructed, relation)

    def test_self_loop(self):
        relation = {(0, 0)}
        ok, reconstructed = MODULE.verify_relation(relation)
        self.assertTrue(ok)
        self.assertEqual(reconstructed, relation)

    def test_exhaustive_up_to_three_states(self):
        for n in range(1, 4):
            ok, count, relation, reconstructed = MODULE.exhaustive_verify(n)
            self.assertTrue(ok, (relation, reconstructed))
            self.assertGreater(count, 0)


if __name__ == "__main__":
    unittest.main()
