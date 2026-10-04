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
        self.assertGreater(abs(r["jacobian_level0_det"]), 1e-10)
        self.assertGreater(abs(r["jacobian_level1_det"]), 1e-10)
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

    def test_fixed_point_boundary_is_explicit(self):
        r = MODULE.verify()
        self.assertEqual(
            r["fixed_point_status"],
            "NOT_WELL_DEFINED_WITHOUT_FIELD_RESCALE_AND_AUTONOMOUS_COORDINATES",
        )

    def test_eigenvalues_are_finite(self):
        r = MODULE.verify()
        for level in ("eigen_level0", "eigen_level1"):
            self.assertEqual(len(r[level]), 3)
            for item in r[level]:
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
