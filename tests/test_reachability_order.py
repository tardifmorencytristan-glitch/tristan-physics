import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_reachability_order.py"
SPEC = importlib.util.spec_from_file_location("verify_reachability_order", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ReachabilityOrderTests(unittest.TestCase):
    def test_chain(self):
        ok, detail = MODULE.verify_graph(3, [(0, 1), (1, 2)])
        self.assertTrue(ok, detail)

    def test_mutual_reachability_collapses_scc(self):
        reach = MODULE.transitive_closure(3, [(0, 1), (1, 0), (1, 2)])
        classes = MODULE.quotient_classes(3, reach)
        self.assertIn(frozenset({0, 1}), classes)
        self.assertIn(frozenset({2}), classes)

    def test_singleton_independence_witness(self):
        ok, detail = MODULE.verify_graph(1, [])
        self.assertTrue(ok, detail)

    def test_exhaustive_up_to_four_vertices(self):
        for n in range(1, 5):
            ok, count, detail = MODULE.exhaustive_verify(n)
            self.assertTrue(ok, detail)
            self.assertGreaterEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
