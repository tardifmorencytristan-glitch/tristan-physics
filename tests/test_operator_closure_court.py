import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_operator_closure_court.py"
SPEC = importlib.util.spec_from_file_location("verify_operator_closure_court", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class OperatorClosureCourtTests(unittest.TestCase):
    def test_complete_subset_lattice(self):
        r = MODULE.verify()
        self.assertEqual(r["subset_count_including_baseline"], 16)
        labels = {row["label"] for row in r["court"]}
        self.assertIn("BASE_ONLY", labels)

    def test_r16_baseline_reproduced(self):
        r = MODULE.verify()
        b = r["baseline_reproduction"]
        self.assertAlmostEqual(
            b["r16_map_relative_discrepancy"],
            b["r17_base_map_relative_discrepancy"],
            places=8,
        )
        self.assertAlmostEqual(
            b["r16_jacobian_relative_discrepancy"],
            b["r17_base_jacobian_relative_discrepancy"],
            places=6,
        )

    def test_derivative_validation(self):
        r = MODULE.verify()
        self.assertTrue(r["derivative_gate_pass"])
        self.assertLessEqual(
            max(
                r["finite_difference_n4_step_stability"],
                r["analytic_vs_fd_n4"],
                r["analytic_vs_fd_n8"],
            ),
            MODULE.DERIVATIVE_TOL,
        )

    def test_winner_is_fitted(self):
        r = MODULE.verify()
        self.assertEqual(r["winner"]["status"], "FIT")
        self.assertLessEqual(
            r["winner"]["map_relative_discrepancy"] / MODULE.MAP_AUTONOMY_TOL,
            r["winner"]["autonomy_ratio"] + 1e-12,
        )

    def test_observed_no_go_is_locked(self):
        r = MODULE.verify()
        self.assertEqual(r["selection_status"], "NO_AUTONOMY_PASSING_FAMILY")
        self.assertEqual(r["winner"]["label"], "BASE_ONLY")
        self.assertEqual(r["best_base_block_family"]["label"], "BASE+delta4")
        singular = [x for x in r["court"] if x["status"] != "FIT"]
        self.assertEqual(len(singular), 2)
        self.assertLess(
            r["best_base_block_family"]["base_block_jacobian_relative_discrepancy"],
            r["baseline_reproduction"]["r17_base_jacobian_relative_discrepancy"],
        )

    def test_dominant_baseline_gap_is_kappa_to_mass(self):
        r = MODULE.verify()
        top = r["baseline_top_jacobian_gaps"][0]
        self.assertEqual((top["row"], top["column"]), ("mass2", "kappa"))
        self.assertGreater(top["abs_gap"], 0.30)

    def test_fixed_point_gate_is_consistent(self):
        r = MODULE.verify()
        if r["autonomy_gate_pass"]:
            self.assertNotEqual(
                r["fixed_point_status"],
                "BLOCKED_NONAUTONOMOUS_OPERATOR_CLOSURE",
            )
        else:
            self.assertEqual(
                r["fixed_point_status"],
                "BLOCKED_NONAUTONOMOUS_OPERATOR_CLOSURE",
            )


if __name__ == "__main__":
    unittest.main()
