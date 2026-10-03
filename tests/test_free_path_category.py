import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_free_path_category.py"
SPEC = importlib.util.spec_from_file_location("verify_free_path_category", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class FreePathCategoryTests(unittest.TestCase):
    def setUp(self):
        self.vertices = ("A", "B", "C")
        self.edges = (
            ("f", "A", "B"),
            ("g", "B", "C"),
            ("h", "A", "C"),
        )
        self.edge_map = {name: (u, v) for name, u, v in self.edges}

    def test_basic_composition(self):
        self.assertEqual(
            MODULE.compose(("g",), ("f",), self.edge_map),
            ("f", "g"),
        )

    def test_left_identity(self):
        p = ("f",)
        result = MODULE.compose((), p, self.edge_map, left_empty_vertex="B", right_empty_vertex="A")
        self.assertEqual(result, p)

    def test_right_identity(self):
        p = ("f",)
        result = MODULE.compose(p, (), self.edge_map, left_empty_vertex="A", right_empty_vertex="A")
        self.assertEqual(result, p)

    def test_associativity(self):
        edge_map = {
            "a": ("A", "B"),
            "b": ("B", "C"),
            "c": ("C", "D"),
        }
        p = ("a",)
        q = ("b",)
        r = ("c",)
        lhs = MODULE.compose(r, MODULE.compose(q, p, edge_map), edge_map)
        rhs = MODULE.compose(MODULE.compose(r, q, edge_map), p, edge_map)
        self.assertEqual(lhs, rhs)

    def test_bounded_verifier(self):
        ok, detail = MODULE.verify(self.vertices, self.edges, max_len=4)
        self.assertTrue(ok, detail)


if __name__ == "__main__":
    unittest.main()
