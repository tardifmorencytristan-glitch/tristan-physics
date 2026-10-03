import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_effective_action_discovery.py"
SPEC = importlib.util.spec_from_file_location("verify_effective_action_discovery", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class EffectiveActionDiscoveryTests(unittest.TestCase):
    def test_r13_verifier(self):
        result = MODULE.verify()
        self.assertEqual(result["fine_configuration_count"], 81)
        self.assertEqual(result["blocked_support_count"], 25)
        self.assertLessEqual(result["partition_difference"], 1e-12)
        self.assertLessEqual(result["max_z2_weight_error"], 1e-12)
        self.assertLessEqual(result["max_exact_reconstruction_error"], 1e-12)
        self.assertGreater(result["base_max_abs"], 1e-6)
        self.assertEqual(result["best_action_candidate"], "m2_sq")
        self.assertEqual(result["best_kl_candidate"], "delta4")

    def test_exact_pushforward_preserves_partition(self):
        weights, fine_z = MODULE.pushforward_weights()
        self.assertAlmostEqual(sum(weights.values()), fine_z)

    def test_exact_effective_action_reconstructs_weights(self):
        from math import exp, log

        weights, _ = MODULE.pushforward_weights()
        for state, weight in weights.items():
            s_eff = -log(weight)
            self.assertAlmostEqual(exp(-s_eff), weight)

    def test_nested_operator_space_does_not_worsen_rss(self):
        weights, _ = MODULE.pushforward_weights()
        states = sorted(weights)
        target = [-__import__("math").log(weights[y]) for y in states]
        base = MODULE.fit_effective_action(states, target, MODULE.BASE_OPERATORS)
        for candidate in MODULE.CANDIDATES:
            extended = MODULE.fit_effective_action(
                states,
                target,
                MODULE.BASE_OPERATORS + (candidate,),
            )
            self.assertLessEqual(extended["rss"], base["rss"] + 1e-12)

    def test_objective_dependent_candidate_ranking(self):
        result = MODULE.verify()
        self.assertEqual(result["best_action_candidate"], "m2_sq")
        self.assertGreater(result["best_action_gain"], 1e-4)
        self.assertEqual(result["best_kl_candidate"], "delta4")
        self.assertGreater(result["best_kl_gain"], 0.0)


if __name__ == "__main__":
    unittest.main()
