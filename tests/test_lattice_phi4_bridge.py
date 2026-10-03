import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_lattice_phi4_bridge.py"
SPEC = importlib.util.spec_from_file_location("verify_lattice_phi4_bridge", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class LatticePhi4BridgeTests(unittest.TestCase):
    def test_r12_exhaustive_witness(self):
        r = MODULE.verify()
        self.assertEqual(r["configuration_count"], 81)
        self.assertLessEqual(r["max_t23_error"], 1e-12)
        self.assertLessEqual(r["max_action_z2_error"], 1e-12)
        self.assertLessEqual(r["max_block_z2_error"], 1e-12)
        self.assertLessEqual(abs(r["mean_field_expectation"]), 1e-12)
        self.assertLessEqual(r["ensemble_t26_error"], 1e-12)
        self.assertLessEqual(r["max_t27_error"], 1e-12)

    def test_t23_known_configuration(self):
        phi = (1.0, -1.0, 1.0, 1.0)
        fine = MODULE.second_moment(phi)
        coarse = MODULE.second_moment(MODULE.block_average(phi))
        residual = MODULE.block_variance(phi)
        self.assertAlmostEqual(fine - coarse, residual)

    def test_t27_action_decomposition(self):
        for phi in [
            (0.0, 0.0, 0.0, 0.0),
            (1.0, -1.0, 0.0, 0.0),
            (1.0, 1.0, -1.0, -1.0),
        ]:
            self.assertAlmostEqual(
                MODULE.lattice_action(phi) / len(phi),
                MODULE.action_density_from_observables(phi),
            )

    def test_n10_information_loss_witness(self):
        a = (1.0, -1.0, 0.0, 0.0)
        b = (0.0, 0.0, 0.0, 0.0)
        self.assertEqual(MODULE.block_average(a), MODULE.block_average(b))
        self.assertAlmostEqual(MODULE.lattice_action(a), 4.5)
        self.assertAlmostEqual(MODULE.lattice_action(b), 0.0)
        self.assertNotEqual(MODULE.lattice_action(a), MODULE.lattice_action(b))

    def test_odd_lattice_rejected_for_blocking(self):
        with self.assertRaises(ValueError):
            MODULE.block_average((1.0, 0.0, -1.0))


if __name__ == "__main__":
    unittest.main()
