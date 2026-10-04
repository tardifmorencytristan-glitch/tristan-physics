#!/usr/bin/env python3
"""Verify R14 exact finite multiscale RG flow: 8 -> 4 -> 2 -> 1 sites."""

from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import exp, fsum, log, sqrt


FINE_VALUES = (Fraction(-1), Fraction(0), Fraction(1))


def lattice_action(state, kappa=1.0, mass2=1.0, lam=1.0):
    n = len(state)
    total = 0.0
    for i, xq in enumerate(state):
        yq = state[(i + 1) % n]
        x = float(xq)
        y = float(yq)
        total += 0.5 * kappa * (y - x) ** 2
        total += 0.5 * mass2 * x ** 2
        total += 0.25 * lam * x ** 4
    return total


def block_average_exact(state):
    n = len(state)
    if n == 0 or n % 2:
        raise ValueError("block averaging requires a nonempty even lattice")
    return tuple((state[i] + state[i + 1]) / 2 for i in range(0, n, 2))


def direct_group_average(state, group_size):
    n = len(state)
    if group_size <= 0 or n % group_size:
        raise ValueError("group_size must divide state length")
    return tuple(
        sum(state[i : i + group_size], Fraction(0)) / group_size
        for i in range(0, n, group_size)
    )


def repeated_block(state, steps):
    out = tuple(state)
    for _ in range(steps):
        out = block_average_exact(out)
    return out


def fine_configurations(sites=8):
    return list(product(FINE_VALUES, repeat=sites))


def fine_weight_map(sites=8):
    return {state: exp(-lattice_action(state)) for state in fine_configurations(sites)}


def pushforward_weights(weight_map):
    grouped = defaultdict(list)
    for state, weight in weight_map.items():
        grouped[block_average_exact(state)].append(weight)
    return {state: fsum(values) for state, values in grouped.items()}


def direct_pushforward_from_fine(fine_weights, steps):
    grouped = defaultdict(list)
    group_size = 2 ** steps
    for state, weight in fine_weights.items():
        grouped[direct_group_average(state, group_size)].append(weight)
    return {state: fsum(values) for state, values in grouped.items()}


def z2_state(state):
    return tuple(-x for x in state)


def operator_value(state, name):
    values = [float(x) for x in state]
    n = len(values)
    m2 = fsum(x * x for x in values) / n
    m4 = fsum(x ** 4 for x in values) / n
    m6 = fsum(x ** 6 for x in values) / n
    m8 = fsum(x ** 8 for x in values) / n
    if n == 1:
        c1 = m2
        delta4 = 0.0
    else:
        c1 = fsum(values[i] * values[(i + 1) % n] for i in range(n)) / n
        delta4 = fsum(
            (values[i] - values[(i + 1) % n]) ** 4 for i in range(n)
        ) / n

    table = {
        "const": 1.0,
        "m2": m2,
        "m4": m4,
        "m6": m6,
        "m8": m8,
        "c1": c1,
        "m2_sq": m2 * m2,
        "m2_c1": m2 * c1,
        "delta4": delta4,
    }
    return table[name]


def base_operators(site_count):
    if site_count == 1:
        return ("const", "m2", "m4")
    return ("const", "m2", "c1", "m4")


def candidate_operators(site_count):
    if site_count == 1:
        return ("m6", "m8")
    return ("m2_sq", "delta4", "m2_c1", "m6")


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


def fit_action(states, exact_action, operators):
    design = [[operator_value(state, name) for name in operators] for state in states]
    p = len(operators)
    gram = [
        [fsum(row[i] * row[j] for row in design) for j in range(p)]
        for i in range(p)
    ]
    rhs = [
        fsum(row[i] * target for row, target in zip(design, exact_action))
        for i in range(p)
    ]
    coeffs = solve_linear_system(gram, rhs)
    predicted = [
        fsum(c * x for c, x in zip(coeffs, row))
        for row in design
    ]
    residuals = [truth - pred for truth, pred in zip(exact_action, predicted)]
    rss = fsum(r * r for r in residuals)
    return {
        "operators": list(operators),
        "coefficients": coeffs,
        "predicted": predicted,
        "residuals": residuals,
        "rss": rss,
        "rms": sqrt(rss / len(residuals)),
        "max_abs": max(abs(r) for r in residuals),
    }


def distribution_from_action(actions):
    weights = [exp(-value) for value in actions]
    z = fsum(weights)
    return [w / z for w in weights]


def kl_divergence(p, q):
    return fsum(pi * log(pi / qi) for pi, qi in zip(p, q))


def analyze_level(level_index, weight_map):
    states = sorted(weight_map)
    z = fsum(weight_map.values())
    probabilities = [weight_map[state] / z for state in states]
    exact_action = [-log(weight_map[state]) for state in states]

    max_z2_error = max(
        abs(weight_map[state] - weight_map[z2_state(state)])
        for state in states
    )
    max_reconstruction_error = max(
        abs(exp(-action) - weight_map[state])
        for state, action in zip(states, exact_action)
    )

    site_count = len(states[0])
    base_ops = base_operators(site_count)
    base = fit_action(states, exact_action, base_ops)
    base_q = distribution_from_action(base["predicted"])
    base_kl = kl_divergence(probabilities, base_q)

    court = []
    for candidate in candidate_operators(site_count):
        extended = fit_action(states, exact_action, base_ops + (candidate,))
        q = distribution_from_action(extended["predicted"])
        candidate_kl = kl_divergence(probabilities, q)
        court.append(
            {
                "candidate": candidate,
                "rss": extended["rss"],
                "rms": extended["rms"],
                "max_abs": extended["max_abs"],
                "action_gain": base["rss"] - extended["rss"],
                "kl": candidate_kl,
                "kl_gain": base_kl - candidate_kl,
            }
        )

    best_action = max(court, key=lambda x: (x["action_gain"], x["candidate"]))
    best_kl = max(court, key=lambda x: (x["kl_gain"], x["candidate"]))

    return {
        "level": level_index,
        "site_count": site_count,
        "support_count": len(states),
        "partition_function": z,
        "max_z2_weight_error": max_z2_error,
        "max_exact_reconstruction_error": max_reconstruction_error,
        "base_operators": list(base_ops),
        "base_coefficients": dict(zip(base_ops, base["coefficients"])),
        "base_rss": base["rss"],
        "base_rms": base["rms"],
        "base_max_abs": base["max_abs"],
        "base_kl": base_kl,
        "court": court,
        "best_action_candidate": best_action["candidate"],
        "best_action_gain": best_action["action_gain"],
        "best_kl_candidate": best_kl["candidate"],
        "best_kl_gain": best_kl["kl_gain"],
    }


def verify():
    fine_configs = fine_configurations(8)

    max_map_composition_error = 0.0
    map_composition_failures = 0
    for state in fine_configs:
        for steps in (1, 2, 3):
            repeated = repeated_block(state, steps)
            direct = direct_group_average(state, 2 ** steps)
            if repeated != direct:
                map_composition_failures += 1
                max_map_composition_error = max(
                    max_map_composition_error,
                    max(abs(float(a - b)) for a, b in zip(repeated, direct)),
                )

    levels = [fine_weight_map(8)]
    for _ in range(3):
        levels.append(pushforward_weights(levels[-1]))

    fine_z = fsum(levels[0].values())
    expected_supports = [6561, 625, 81, 17]
    support_counts = [len(level) for level in levels]

    partition_differences = [
        abs(fsum(level.values()) - fine_z)
        for level in levels
    ]

    direct_pushforward_max_errors = []
    for steps in (1, 2, 3):
        direct = direct_pushforward_from_fine(levels[0], steps)
        repeated = levels[steps]
        keys = set(direct) | set(repeated)
        direct_pushforward_max_errors.append(
            max(abs(direct.get(key, 0.0) - repeated.get(key, 0.0)) for key in keys)
        )

    analyses = [analyze_level(i, level) for i, level in enumerate(levels[1:], start=1)]

    return {
        "fine_configuration_count": len(fine_configs),
        "support_counts": support_counts,
        "expected_support_counts": expected_supports,
        "map_composition_failures": map_composition_failures,
        "max_map_composition_error": max_map_composition_error,
        "fine_partition_function": fine_z,
        "partition_differences": partition_differences,
        "direct_pushforward_max_errors": direct_pushforward_max_errors,
        "levels": analyses,
        "r11_compatible_local_action_rms": [
            level["base_rms"] for level in analyses
        ],
        "r11_unit_sensitivity_sum": fsum(
            level["base_rms"] for level in analyses
        ),
    }


def main():
    result = verify()
    tol = 1e-12

    if result["fine_configuration_count"] != 6561:
        raise SystemExit("FAIL fine configuration count")
    if result["support_counts"] != result["expected_support_counts"]:
        raise SystemExit("FAIL multiscale support counts")
    if result["map_composition_failures"] != 0:
        raise SystemExit("FAIL exact rational block-map composition")
    if max(result["partition_differences"]) > tol:
        raise SystemExit("FAIL partition conservation")
    if max(result["direct_pushforward_max_errors"]) > tol:
        raise SystemExit("FAIL push-forward functoriality witness")

    for level in result["levels"]:
        if level["max_z2_weight_error"] > tol:
            raise SystemExit("FAIL Z2 inheritance")
        if level["max_exact_reconstruction_error"] > tol:
            raise SystemExit("FAIL exact effective-action reconstruction")
        if level["base_max_abs"] <= 1e-8:
            raise SystemExit("FAIL restricted base ansatz unexpectedly exact")
        for item in level["court"]:
            if item["action_gain"] < -tol:
                raise SystemExit("FAIL nested operator-space monotonicity")

    print("PASS multiscale RG flow verifier")
    print(result)


if __name__ == "__main__":
    main()
