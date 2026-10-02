import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_dependency_dag.py"
SPEC = importlib.util.spec_from_file_location("verify_dependency_dag", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class DependencyDagTests(unittest.TestCase):
    def test_valid_dag(self):
        data = {
            "primitives": [{"name": "A"}],
            "definitions": [{"name": "B", "depends_on": ["A"]}],
            "claims": [{"id": "T1", "depends_on": ["B"]}],
        }
        result = MODULE.validate_dependencies(data)
        self.assertTrue(result["ok"], result)

    def test_cycle_detected(self):
        data = {
            "primitives": [],
            "definitions": [
                {"name": "A", "depends_on": ["B"]},
                {"name": "B", "depends_on": ["A"]},
            ],
            "claims": [],
        }
        result = MODULE.validate_dependencies(data)
        self.assertFalse(result["ok"])
        self.assertTrue(result["cycle"])

    def test_missing_dependency_detected(self):
        data = {
            "primitives": [{"name": "A"}],
            "definitions": [{"name": "B", "depends_on": ["Missing"]}],
            "claims": [],
        }
        result = MODULE.validate_dependencies(data)
        self.assertFalse(result["ok"])
        self.assertIn(("B", "Missing"), result["missing"])

    def test_duplicate_identifier_detected(self):
        data = {
            "primitives": [{"name": "A"}],
            "definitions": [{"name": "A", "depends_on": []}],
            "claims": [],
        }
        result = MODULE.validate_dependencies(data)
        self.assertFalse(result["ok"])
        self.assertIn("A", result["duplicates"])


if __name__ == "__main__":
    unittest.main()
