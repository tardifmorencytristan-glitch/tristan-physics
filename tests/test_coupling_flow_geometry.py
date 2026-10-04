import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_coupling_flow_geometry.py"
SPEC = importlib.util.spec_from_file_location("verify_coupling_flow_geometry", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class CouplingFlowGeometryTests(unittest.TestCase):
    def test_r15_verifier(self):
        r = MODULE.verify()
        self.assertEqual(r["step0_supports"], [6561, 625])
        self.assertEqual(r["step1_supports"], [625, 81])
        self.assertLessEqual(r["jacobian_level0_step_stability_rel"], 1e-4)
        self.assertLessEqual(r["jacobian_level1_step_stability_rel"], 1e-4)
        self.assertEqual(
            r["level0_identifiability"],
            "RANK_DEFICIENT_BY_TERNARY_ALIAS_PHI4_EQ_PHI2",
        )
        self.assertLessEqual(r["level0_null_residual"], 1e-7)
        self.assertLessEqual(r["level0_alias_column_error"], 1e-7)
        self.assertGreater(r["jacobian_level0_condition_frobenius"], 1e8)
        self.assertGreater(abs(r["jacobian_level1_det"]), 1e-10)
        self.assertLess(r["jacobian_level1_condition_frobenius"], 1e4)
        self.assertGreater(r["projection_closure_l2"], 1e-8)

    def test_alphabet_growth_is_exact(self):
        a0 = MODULE.INITIAL_VALUES
        a1 = MODULE.next_alphabet(a0)
        a2 = MODULE.next_alphabet(a1)
        self.assertEqual(len(a0), 3)
        self.assertEqual(len(a1), 5)
        self.assertEqual(len(a2), 9)
        self.assertIn(Fraction(1, 2), a1)
        self.assertIn(Fraction(1, 4), a2)

    def test_physical_parameter_roundtrip(self):
        params = (1.2, 0.7, 0.9)
        sites = 4
        kappa, mass2, lam = params
        coeffs = {
            "const": 0.0,
            "m2": sites * (kappa + mass2 / 2.0),
            "c1": -sites * kappa,
            "m4": sites * lam / 4.0,
        }
        got = MODULE.physical_params_from_coefficients(coeffs, sites)
        for a, b in zip(params, got):
            self.assertAlmostEqual(a, b)

    def test_ternary_alias_has_analytical_null_direction(self):
        r = MODULE.verify()
        self.assertEqual(tuple(r["level0_null_direction"]), (0.0, -0.5, 1.0))
        self.assertLessEqual(r["level0_null_residual"], 1e-7)

    def test_fixed_point_boundary_is_explicit(self):
        r = MODULE.verify()
        self.assertEqual(
            r["fixed_point_status"],
            "NOT_WELL_DEFINED_WITHOUT_FIELD_RESCALE_AND_AUTONOMOUS_COORDINATES",
        )

    def test_eigenvalues_are_finite(self):
        r = MODULE.verify()
        self.assertEqual(r["eigen_level0_status"], "DO_NOT_INTERPRET_3D_EIGENMODES")
        self.assertEqual(len(r["eigen_level1"]), 3)
        for item in r["eigen_level1"]:
            self.assertGreaterEqual(item["abs"], 0.0)
            self.assertIn(
                item["classification"],
                {
                    "EXPANDING_FINITE_STEP",
                    "CONTRACTING_FINITE_STEP",
                    "NEAR_UNIT_FINITE_STEP",
                },
            )


if __name__ == "__main__":
    unittest.main()
