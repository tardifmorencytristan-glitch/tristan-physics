#!/usr/bin/env python3
"""Verify R13 exact finite push-forward and effective-action operator court."""

from collections import defaultdict
from itertools import product
from math import exp, log, sqrt


FINE_VALUES = (-1.0, 0.0, 1.0)
BASE_OPERATORS = ("const", "m2", "c1", "m4")
CANDIDATES = ("m2_sq", "delta4", "m2_c1", "c1_cubic", "m4_c1")


def lattice_action(phi, kappa=1.0, mass2=1.0, lam=1.0):
    n = len(phi)
    return sum(
        0.5 * kappa * (phi[(i + 1) % n] - x) ** 2
        + 0.5 * mass2 * x ** 2
        + 0.25 * lam * x ** 4
        for i, x in enumerate(phi)
    )


def block_average(phi):
    if len(phi) == 0 or len(phi) % 2:
        raise ValueError("block averaging requires a nonempty even lattice")
    return tuple((phi[i] + phi[i + 1]) / 2.0 for i in range(0, len(phi), 2))


def fine_configurations():
    return list(product(FINE_VALUES, repeat=4))


def pushforward_weights():
    weights = defaultdict(float)
    fine_z = 0.0
    for phi in fine_configurations():
        w = exp(-lattice_action(phi))
        fine_z += w
        weights[block_average(phi)] += w
    return dict(weights), fine_z


def operator_value(y, name):
    a, b = y
    m2 = (a * a + b * b) / 2.0
    m4 = (a ** 4 + b ** 4) / 2.0
    c1 = a * b
    values = {
        "const": 1.0,
        "m2": m2,
        "c1": c1,
        "m4": m4,
        "m2_sq": m2 * m2,
        "delta4": (a - b) ** 4,
        "m2_c1": m2 * c1,
        "c1_cubic": c1 ** 3,
        "m4_c1": m4 * c1,
    }
    return values[name]


def solve_linear_system(matrix, rhs, tol=1e-12):
    n = len(rhs)
    aug = [list(map(float, matrix[i])) + [float(rhs[i])] for i in range(n)]

    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) <= tol:
            raise ValueError("singular normal-equation matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]

        scale = aug[col][col]
        for j in range(col, n + 1):
            aug[col][j] /= scale

        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            for j in range(col, n + 1):
                aug[row][j] -= factor * aug[col][j]

    return [aug[i][n] for i in range(n)]


def fit_effective_action(states, target, operators):
    design = [[operator_value(y, name) for name in operators] for y in states]
    p = len(operators)

    gram = [
        [sum(row[i] * row[j] for row in design) for j in range(p)]
        for i in range(p)
    ]
    rhs = [
        sum(row[i] * value for row, value in zip(design, target))
        for i in range(p)
    ]
    coeffs = solve_linear_system(gram, rhs)

    predicted = [
        sum(c * x for c, x in zip(coeffs, row))
        for row in design
    ]
    residuals = [truth - pred for truth, pred in zip(target, predicted)]
    rss = sum(r * r for r in residuals)

    return {
        "operators": list(operators),
        "coefficients": coeffs,
        "predicted_action": predicted,
        "residuals": residuals,
        "rss": rss,
        "rms": sqrt(rss / len(residuals)),
        "max_abs": max(abs(r) for r in residuals),
    }


def normalized_distribution_from_action(actions):
    weights = [exp(-value) for value in actions]
    total = sum(weights)
    return [w / total for w in weights]


def kl_divergence(p, q):
    return sum(pi * log(pi / qi) for pi, qi in zip(p, q))


def verify():
    weights, fine_z = pushforward_weights()
    states = sorted(weights)
    coarse_z = sum(weights.values())
    probabilities = [weights[y] / coarse_z for y in states]
    exact_action = [-log(weights[y]) for y in states]

    max_z2_weight_error = max(
        abs(weights[y] - weights[tuple(-x for x in y)])
        for y in states
    )
    max_exact_reconstruction_error = max(
        abs(exp(-s) - weights[y])
        for y, s in zip(states, exact_action)
    )

    base = fit_effective_action(states, exact_action, BASE_OPERATORS)
    base_q = normalized_distribution_from_action(base["predicted_action"])
    base_kl = kl_divergence(probabilities, base_q)

    court = []
    for candidate in CANDIDATES:
        fitted = fit_effective_action(
            states,
            exact_action,
            BASE_OPERATORS + (candidate,),
        )
        q = normalized_distribution_from_action(fitted["predicted_action"])
        candidate_kl = kl_divergence(probabilities, q)
        court.append(
            {
                "candidate": candidate,
                "rss": fitted["rss"],
                "rms": fitted["rms"],
                "max_abs": fitted["max_abs"],
                "action_rss_gain": base["rss"] - fitted["rss"],
                "kl": candidate_kl,
                "kl_gain": base_kl - candidate_kl,
            }
        )

    best_action = max(court, key=lambda item: (item["action_rss_gain"], item["candidate"]))
    best_kl = max(court, key=lambda item: (item["kl_gain"], item["candidate"]))

    return {
        "fine_configuration_count": len(fine_configurations()),
        "blocked_support_count": len(states),
        "fine_partition_function": fine_z,
        "coarse_partition_function": coarse_z,
        "partition_difference": abs(fine_z - coarse_z),
        "max_z2_weight_error": max_z2_weight_error,
        "max_exact_reconstruction_error": max_exact_reconstruction_error,
        "base_coefficients": dict(zip(BASE_OPERATORS, base["coefficients"])),
        "base_rss": base["rss"],
        "base_rms": base["rms"],
        "base_max_abs": base["max_abs"],
        "base_kl": base_kl,
        "court": court,
        "best_action_candidate": best_action["candidate"],
        "best_action_gain": best_action["action_rss_gain"],
        "best_kl_candidate": best_kl["candidate"],
        "best_kl_gain": best_kl["kl_gain"],
    }


def main():
    result = verify()
    tol = 1e-12

    if result["fine_configuration_count"] != 81:
        raise SystemExit("FAIL fine configuration count")
    if result["blocked_support_count"] != 25:
        raise SystemExit("FAIL blocked support count")
    if result["partition_difference"] > tol:
        raise SystemExit("FAIL T28 partition preservation")
    if result["max_z2_weight_error"] > tol:
        raise SystemExit("FAIL T28 Z2 inheritance")
    if result["max_exact_reconstruction_error"] > tol:
        raise SystemExit("FAIL T29 exact effective-action reconstruction")
    if result["base_max_abs"] <= 1e-6:
        raise SystemExit("FAIL N11: base ansatz unexpectedly exact")
    if result["best_action_candidate"] != "m2_sq":
        raise SystemExit("FAIL T31 action-space candidate ordering")
    if result["best_action_gain"] <= 1e-4:
        raise SystemExit("FAIL T31 action-space gain")
    if result["best_kl_candidate"] != "delta4":
        raise SystemExit("FAIL T31 KL candidate ordering")
    if result["best_kl_gain"] <= 0.0:
        raise SystemExit("FAIL T31 KL gain")

    for item in result["court"]:
        if item["action_rss_gain"] < -tol:
            raise SystemExit("FAIL T30 nested-space monotonicity")

    print("PASS effective-action discovery verifier")
    print(result)


if __name__ == "__main__":
    main()
