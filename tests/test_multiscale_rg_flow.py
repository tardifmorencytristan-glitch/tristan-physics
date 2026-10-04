import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_multiscale_rg_flow.py"
SPEC = importlib.util.spec_from_file_location("verify_multiscale_rg_flow", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class MultiscaleRGFlowTests(unittest.TestCase):
    def test_r14_verifier(self):
        result = MODULE.verify()
        self.assertEqual(result["fine_configuration_count"], 6561)
        self.assertEqual(result["support_counts"], [6561, 625, 81, 17])
        self.assertEqual(result["map_composition_failures"], 0)
        self.assertLessEqual(max(result["partition_differences"]), 1e-12)
        self.assertLessEqual(max(result["direct_pushforward_max_errors"]), 1e-12)
        self.assertEqual(len(result["levels"]), 3)

    def test_exact_rational_block_composition(self):
        state = tuple(Fraction(x) for x in (1, 0, -1, 1, 0, 0, 1, -1))
        for steps in (1, 2, 3):
            self.assertEqual(
                MODULE.repeated_block(state, steps),
                MODULE.direct_group_average(state, 2 ** steps),
            )

    def test_pushforward_preserves_partition(self):
        fine = MODULE.fine_weight_map(8)
        level = fine
        z0 = sum(fine.values())
        for _ in range(3):
            level = MODULE.pushforward_weights(level)
            self.assertAlmostEqual(sum(level.values()), z0, places=12)

    def test_z2_inheritance_each_level(self):
        level = MODULE.fine_weight_map(8)
        for _ in range(3):
            level = MODULE.pushforward_weights(level)
            for state, weight in level.items():
                self.assertAlmostEqual(weight, level[MODULE.z2_state(state)], places=12)

    def test_restricted_ansatz_is_not_exact(self):
        result = MODULE.verify()
        for level in result["levels"]:
            self.assertGreater(level["base_max_abs"], 1e-8)

    def test_nested_operator_spaces_do_not_worsen_action_rss(self):
        result = MODULE.verify()
        for level in result["levels"]:
            for candidate in level["court"]:
                if candidate["status"] == "FIT":
                    self.assertGreaterEqual(candidate["action_gain"], -1e-12)

    def test_redundant_candidates_are_explicit(self):
        result = MODULE.verify()
        redundant = [
            (level["site_count"], item["candidate"])
            for level in result["levels"]
            for item in level["court"]
            if item["status"] == "REDUNDANT_OR_SINGULAR"
        ]
        self.assertTrue(redundant)


if __name__ == "__main__":
    unittest.main()
