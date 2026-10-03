import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_effective_error_budget.py"
SPEC = importlib.util.spec_from_file_location("verify_effective_error_budget", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class EffectiveErrorBudgetTests(unittest.TestCase):
    def test_r11_witness(self):
        r = MODULE.verify()
        self.assertAlmostEqual(r["additive_budget"], 0.75)
        self.assertEqual(r["zero_budget"], 0)
        self.assertTrue(r["recurrence_match"])
        self.assertAlmostEqual(r["amplification_final"], 1.0)
        self.assertAlmostEqual(r["amplification_factor"], 16.0)

    def test_closed_form_matches_iteration(self):
        cases = [
            (0.0, [1.0], [0.1]),
            (0.2, [2.0, 3.0], [0.1, 0.4]),
            (1.0, [0.5, 0.5, 0.5], [0.0, 0.0, 0.0]),
            (0.25, [0.0, 4.0], [0.5, 0.25]),
        ]
        for initial, L, delta in cases:
            with self.subTest(initial=initial, L=L, delta=delta):
                self.assertAlmostEqual(
                    MODULE.recurrence_bound(initial, L, delta),
                    MODULE.recurrence_iterate(initial, L, delta),
                )

    def test_rejects_negative_bounds(self):
        with self.assertRaises(ValueError):
            MODULE.additive_budget([0.1, -0.1])
        with self.assertRaises(ValueError):
            MODULE.recurrence_bound(0.1, [1.0], [-0.2])


if __name__ == "__main__":
    unittest.main()
