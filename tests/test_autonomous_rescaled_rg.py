import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_autonomous_rescaled_rg.py"
SPEC = importlib.util.spec_from_file_location("verify_autonomous_rescaled_rg", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class AutonomousRescaledRGTests(unittest.TestCase):
    def test_r16_verifier(self):
        r = MODULE.verify()
        self.assertEqual(
            r["support_witness"],
            {
                "n8_input": 390625,
                "n8_output": 6561,
                "n4_input": 625,
                "n4_output": 81,
            },
        )
        self.assertIn(r["winner"], MODULE.SCHEMES)
        self.assertLessEqual(
            max(
                r["finite_difference_stability_n8"],
                r["finite_difference_stability_n4"],
            ),
            MODULE.FD_STABILITY_TOL,
        )

    def test_court_contains_all_schemes(self):
        r = MODULE.verify()
        names = {row["scheme"] for row in r["court"]}
        self.assertEqual(names, set(MODULE.SCHEMES))

    def test_reference_alphabet_is_common_five_value_domain(self):
        r = MODULE.verify()
        self.assertEqual(r["reference_alphabet"], [-1.0, -0.5, 0.0, 0.5, 1.0])

    def test_fixed_point_gate_is_consistent(self):
        r = MODULE.verify()
        if r["autonomy_gate_pass"]:
            self.assertNotEqual(
                r["fixed_point_status"],
                "BLOCKED_NONAUTONOMOUS_FINITE_SIZE_DEPENDENCE",
            )
        else:
            self.assertEqual(
                r["fixed_point_status"],
                "BLOCKED_NONAUTONOMOUS_FINITE_SIZE_DEPENDENCE",
            )

    def test_court_sorted_by_declared_map_objective(self):
        r = MODULE.verify()
        scores = [row["map_relative_discrepancy"] for row in r["court"]]
        self.assertEqual(scores, sorted(scores))


if __name__ == "__main__":
    unittest.main()
