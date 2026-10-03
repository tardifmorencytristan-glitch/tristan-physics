#!/usr/bin/env python3
"""Verify R12 finite lattice phi4 coarse-graining identities."""

from itertools import product
from math import exp


def lattice_action(phi, kappa=1.0, mass2=1.0, lam=1.0):
    n = len(phi)
    if n < 2:
        raise ValueError("lattice must have at least two sites")
    total = 0.0
    for i, x in enumerate(phi):
        y = phi[(i + 1) % n]
        total += 0.5 * kappa * (y - x) ** 2
        total += 0.5 * mass2 * x ** 2
        total += 0.25 * lam * x ** 4
    return total


def block_average(phi):
    n = len(phi)
    if n == 0 or n % 2:
        raise ValueError("block averaging requires a nonempty even lattice")
    return tuple((phi[i] + phi[i + 1]) / 2.0 for i in range(0, n, 2))


def second_moment(phi):
    return sum(x * x for x in phi) / len(phi)


def fourth_moment(phi):
    return sum(x ** 4 for x in phi) / len(phi)


def nearest_neighbor_correlation(phi):
    n = len(phi)
    return sum(phi[i] * phi[(i + 1) % n] for i in range(n)) / n


def mean_field(phi):
    return sum(phi) / len(phi)


def block_variance(phi):
    n = len(phi)
    if n == 0 or n % 2:
        raise ValueError("block variance requires a nonempty even lattice")
    blocks = n // 2
    return sum((phi[i] - phi[i + 1]) ** 2 / 4.0 for i in range(0, n, 2)) / blocks


def action_density_from_observables(phi, kappa=1.0, mass2=1.0, lam=1.0):
    m2 = second_moment(phi)
    m4 = fourth_moment(phi)
    c1 = nearest_neighbor_correlation(phi)
    return kappa * (m2 - c1) + 0.5 * mass2 * m2 + 0.25 * lam * m4


def enumerate_configs(values=(-1.0, 0.0, 1.0), sites=4):
    return list(product(values, repeat=sites))


def verify(values=(-1.0, 0.0, 1.0), sites=4, kappa=1.0, mass2=1.0, lam=1.0):
    if sites % 2:
        raise ValueError("sites must be even")

    configs = enumerate_configs(values=values, sites=sites)
    max_t23_error = 0.0
    max_action_z2_error = 0.0
    max_block_z2_error = 0.0
    max_t27_error = 0.0

    weighted = []
    for phi in configs:
        blocked = block_average(phi)
        lhs = second_moment(phi) - second_moment(blocked)
        rhs = block_variance(phi)
        max_t23_error = max(max_t23_error, abs(lhs - rhs))

        neg = tuple(-x for x in phi)
        max_action_z2_error = max(
            max_action_z2_error,
            abs(
                lattice_action(phi, kappa, mass2, lam)
                - lattice_action(neg, kappa, mass2, lam)
            ),
        )
        blocked_neg = block_average(neg)
        max_block_z2_error = max(
            max_block_z2_error,
            max(abs(a + b) for a, b in zip(blocked, blocked_neg)),
        )

        direct_density = lattice_action(phi, kappa, mass2, lam) / sites
        decomposed_density = action_density_from_observables(
            phi, kappa, mass2, lam
        )
        max_t27_error = max(
            max_t27_error, abs(direct_density - decomposed_density)
        )

        w = exp(-lattice_action(phi, kappa, mass2, lam))
        weighted.append((phi, w))

    partition = sum(w for _, w in weighted)
    mean_expectation = sum(w * mean_field(phi) for phi, w in weighted) / partition
    fine_m2 = sum(w * second_moment(phi) for phi, w in weighted) / partition
    coarse_m2 = sum(
        w * second_moment(block_average(phi)) for phi, w in weighted
    ) / partition
    variance_mean = sum(w * block_variance(phi) for phi, w in weighted) / partition
    c1_mean = sum(
        w * nearest_neighbor_correlation(phi) for phi, w in weighted
    ) / partition

    t26_error = abs((fine_m2 - coarse_m2) - variance_mean)

    witness_a = (1.0, -1.0, 0.0, 0.0)
    witness_b = (0.0, 0.0, 0.0, 0.0)
    witness_same_block = block_average(witness_a) == block_average(witness_b)
    witness_action_a = lattice_action(witness_a, 1.0, 1.0, 1.0)
    witness_action_b = lattice_action(witness_b, 1.0, 1.0, 1.0)

    return {
        "configuration_count": len(configs),
        "partition_function": partition,
        "max_t23_error": max_t23_error,
        "max_action_z2_error": max_action_z2_error,
        "max_block_z2_error": max_block_z2_error,
        "mean_field_expectation": mean_expectation,
        "fine_m2_expectation": fine_m2,
        "coarse_m2_expectation": coarse_m2,
        "block_variance_expectation": variance_mean,
        "ensemble_t26_error": t26_error,
        "nearest_neighbor_correlation_expectation": c1_mean,
        "max_t27_error": max_t27_error,
        "n10_same_block": witness_same_block,
        "n10_action_a": witness_action_a,
        "n10_action_b": witness_action_b,
        "n10_action_gap": witness_action_a - witness_action_b,
    }


def main():
    result = verify()
    tol = 1e-12
    if result["configuration_count"] != 81:
        raise SystemExit("FAIL configuration count")
    if result["max_t23_error"] > tol:
        raise SystemExit("FAIL T23 block residual identity")
    if result["max_action_z2_error"] > tol or result["max_block_z2_error"] > tol:
        raise SystemExit("FAIL T24 Z2 covariance")
    if abs(result["mean_field_expectation"]) > tol:
        raise SystemExit("FAIL T25 odd-observable cancellation")
    if result["ensemble_t26_error"] > tol:
        raise SystemExit("FAIL T26 ensemble residual identity")
    if result["max_t27_error"] > tol:
        raise SystemExit("FAIL T27 action-density decomposition")
    if not result["n10_same_block"]:
        raise SystemExit("FAIL N10 blocked-field witness")
    if abs(result["n10_action_a"] - 4.5) > tol or abs(result["n10_action_b"]) > tol:
        raise SystemExit("FAIL N10 action witness")
    print("PASS lattice phi4 bridge verifier")
    print(result)


if __name__ == "__main__":
    main()
