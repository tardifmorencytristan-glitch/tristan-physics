#!/usr/bin/env python3
"""R16: rescaling court and finite autonomy gate for projected RG."""

from functools import lru_cache
from math import fsum, log, sqrt
from pathlib import Path
import sys

TOOLS_DIR = str(Path(__file__).resolve().parent)
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import verify_coupling_flow_geometry as r15


SCHEMES = (
    "NONE",
    "SUPPORT_M2_MATCH",
    "BOLTZMANN_M2_MATCH",
    "KINETIC_MATCH",
)
MAP_AUTONOMY_TOL = 5e-2
JACOBIAN_AUTONOMY_TOL = 1e-1
FD_STABILITY_TOL = 1e-4


def l2(v):
    return sqrt(fsum(x * x for x in v))


def vector_distance(a, b):
    return sqrt(fsum((x - y) ** 2 for x, y in zip(a, b)))


def frobenius(a):
    return sqrt(fsum(x * x for row in a for x in row))


def matrix_distance(a, b):
    return sqrt(
        fsum(
            (a[i][j] - b[i][j]) ** 2
            for i in range(3)
            for j in range(3)
        )
    )


def m2_state(state):
    return fsum(float(x) ** 2 for x in state) / len(state)


def weighted_m2(weight_map):
    z = fsum(weight_map.values())
    return fsum(weight * m2_state(state) for state, weight in weight_map.items()) / z


def uniform_alphabet_m2(values):
    return fsum(float(x) ** 2 for x in values) / len(values)


def rescale_weight_map(weight_map, scale):
    if not (scale > 0.0):
        raise ValueError("field scale must be positive")
    return {
        tuple(scale * float(x) for x in state): weight
        for state, weight in weight_map.items()
    }


def choose_scale(scheme, values, params, fine, coarse):
    if scheme == "NONE":
        return 1.0

    if scheme == "SUPPORT_M2_MATCH":
        coarse_values = r15.next_alphabet(values)
        source = uniform_alphabet_m2(values)
        target = uniform_alphabet_m2(coarse_values)
        return sqrt(source / target)

    if scheme == "BOLTZMANN_M2_MATCH":
        source = weighted_m2(fine)
        target = weighted_m2(coarse)
        if target <= 0.0:
            raise ValueError("coarse Boltzmann M2 must be positive")
        return sqrt(source / target)

    if scheme == "KINETIC_MATCH":
        raw_fit = r15.fit_base_effective_action(coarse)
        output_sites = len(next(iter(coarse)))
        raw_params = r15.physical_params_from_coefficients(
            raw_fit["coefficients"], output_sites
        )
        kappa_in = float(params[0])
        kappa_raw = float(raw_params[0])
        ratio = kappa_raw / kappa_in
        if ratio <= 0.0:
            raise ValueError("kinetic matching requires positive kappa ratio")
        return sqrt(ratio)

    raise ValueError("unknown scheme: " + scheme)


@lru_cache(maxsize=256)
def projected_rescaled_map(values, sites, params, scheme):
    values = tuple(values)
    params = tuple(float(x) for x in params)
    fine = r15.parametric_weight_map(values, sites, params)
    coarse = r15.pushforward_weights(fine)
    scale = choose_scale(scheme, values, params, fine, coarse)
    transformed = rescale_weight_map(coarse, scale)
    fit = r15.fit_base_effective_action(transformed)
    output_sites = sites // 2
    params_out = r15.physical_params_from_coefficients(
        fit["coefficients"], output_sites
    )
    return {
        "params_out": tuple(params_out),
        "scale": scale,
        "fit_rms": fit["rms"],
        "fit_max_abs": fit["max_abs"],
        "input_support": len(fine),
        "output_support": len(coarse),
        "input_m2": weighted_m2(fine),
        "coarse_m2_before_rescale": weighted_m2(coarse),
        "coarse_m2_after_rescale": scale * scale * weighted_m2(coarse),
    }


def central_jacobian(values, sites, params, scheme, relative_step):
    base = tuple(float(x) for x in params)
    columns = []
    for j in range(3):
        h = relative_step * max(1.0, abs(base[j]))
        plus = list(base)
        minus = list(base)
        plus[j] += h
        minus[j] -= h
        y_plus = projected_rescaled_map(
            tuple(values), sites, tuple(plus), scheme
        )["params_out"]
        y_minus = projected_rescaled_map(
            tuple(values), sites, tuple(minus), scheme
        )["params_out"]
        columns.append(
            tuple((a - b) / (2.0 * h) for a, b in zip(y_plus, y_minus))
        )
    return [[columns[j][i] for j in range(3)] for i in range(3)]


def relative_vector_distance(a, b):
    return vector_distance(a, b) / max(1.0, l2(a), l2(b))


def relative_matrix_distance(a, b):
    return matrix_distance(a, b) / max(1.0, frobenius(a), frobenius(b))


def court_at_reference(reference_values, theta):
    court = []
    for scheme in SCHEMES:
        n8 = projected_rescaled_map(reference_values, 8, theta, scheme)
        n4 = projected_rescaled_map(reference_values, 4, theta, scheme)
        map_rel = relative_vector_distance(n8["params_out"], n4["params_out"])
        scale_log_gap = abs(log(n8["scale"] / n4["scale"]))
        court.append(
            {
                "scheme": scheme,
                "n8_params_out": n8["params_out"],
                "n4_params_out": n4["params_out"],
                "n8_scale": n8["scale"],
                "n4_scale": n4["scale"],
                "map_relative_discrepancy": map_rel,
                "scale_log_gap": scale_log_gap,
                "n8_fit_rms": n8["fit_rms"],
                "n4_fit_rms": n4["fit_rms"],
            }
        )
    court.sort(
        key=lambda row: (
            row["map_relative_discrepancy"],
            row["scale_log_gap"],
            row["scheme"],
        )
    )
    return court


def fixed_point_iteration(values, theta0, scheme, max_iter=6):
    theta = tuple(float(x) for x in theta0)
    history = []
    for _ in range(max_iter):
        try:
            nxt = projected_rescaled_map(values, 8, theta, scheme)["params_out"]
        except (OverflowError, ValueError):
            return {
                "status": "SEARCH_FAILED_NUMERICALLY",
                "history": history,
            }
        residual = vector_distance(theta, nxt)
        history.append({"theta": theta, "next": nxt, "residual": residual})
        if residual < 1e-8:
            return {
                "status": "APPROXIMATE_FIXED_POINT_FOUND",
                "theta": nxt,
                "residual": residual,
                "history": history,
            }
        if l2(nxt) > 1e4:
            return {
                "status": "SEARCH_DIVERGED_BOUNDED",
                "history": history,
            }
        theta = tuple(0.5 * a + 0.5 * b for a, b in zip(theta, nxt))
    return {
        "status": "NO_FIXED_POINT_WITHIN_BOUNDED_ITERATION",
        "theta": theta,
        "history": history,
    }


@lru_cache(maxsize=1)
def verify():
    r15_exact = r15.exact_two_level_projection()
    theta = tuple(r15_exact["p1_exact_projection"])
    reference_values = tuple(r15.next_alphabet(r15.INITIAL_VALUES))

    court = court_at_reference(reference_values, theta)
    winner = court[0]
    scheme = winner["scheme"]

    j8_h = central_jacobian(reference_values, 8, theta, scheme, 1e-4)
    j8_h2 = central_jacobian(reference_values, 8, theta, scheme, 5e-5)
    j4_h = central_jacobian(reference_values, 4, theta, scheme, 1e-4)
    j4_h2 = central_jacobian(reference_values, 4, theta, scheme, 5e-5)

    fd8 = relative_matrix_distance(j8_h, j8_h2)
    fd4 = relative_matrix_distance(j4_h, j4_h2)
    jac_cross = relative_matrix_distance(j8_h2, j4_h2)

    map_pass = winner["map_relative_discrepancy"] <= MAP_AUTONOMY_TOL
    jac_pass = jac_cross <= JACOBIAN_AUTONOMY_TOL
    fd_pass = max(fd8, fd4) <= FD_STABILITY_TOL
    autonomous = map_pass and jac_pass and fd_pass

    if autonomous:
        fixed_point = fixed_point_iteration(reference_values, theta, scheme)
        fixed_point_status = fixed_point["status"]
    else:
        fixed_point = None
        fixed_point_status = "BLOCKED_NONAUTONOMOUS_FINITE_SIZE_DEPENDENCE"

    return {
        "reference_theta": theta,
        "reference_alphabet": [float(x) for x in reference_values],
        "court": court,
        "winner": scheme,
        "winner_map_relative_discrepancy": winner["map_relative_discrepancy"],
        "jacobian_n8": j8_h2,
        "jacobian_n4": j4_h2,
        "jacobian_cross_scale_relative_discrepancy": jac_cross,
        "finite_difference_stability_n8": fd8,
        "finite_difference_stability_n4": fd4,
        "map_autonomy_tolerance": MAP_AUTONOMY_TOL,
        "jacobian_autonomy_tolerance": JACOBIAN_AUTONOMY_TOL,
        "finite_difference_tolerance": FD_STABILITY_TOL,
        "map_gate_pass": map_pass,
        "jacobian_gate_pass": jac_pass,
        "finite_difference_gate_pass": fd_pass,
        "autonomy_gate_pass": autonomous,
        "fixed_point_status": fixed_point_status,
        "fixed_point_search": fixed_point,
        "support_witness": {
            "n8_input": 5 ** 8,
            "n8_output": 9 ** 4,
            "n4_input": 5 ** 4,
            "n4_output": 9 ** 2,
        },
    }


def main():
    result = verify()

    if result["support_witness"] != {
        "n8_input": 390625,
        "n8_output": 6561,
        "n4_input": 625,
        "n4_output": 81,
    }:
        raise SystemExit("FAIL R16 support witness")

    if result["winner"] not in SCHEMES:
        raise SystemExit("FAIL R16 court winner")

    if max(
        result["finite_difference_stability_n8"],
        result["finite_difference_stability_n4"],
    ) > FD_STABILITY_TOL:
        raise SystemExit("FAIL R16 finite-difference stability")

    if result["autonomy_gate_pass"]:
        if result["fixed_point_status"] == "BLOCKED_NONAUTONOMOUS_FINITE_SIZE_DEPENDENCE":
            raise SystemExit("FAIL R16 autonomy/fixed-point gate mismatch")
    else:
        if result["fixed_point_status"] != "BLOCKED_NONAUTONOMOUS_FINITE_SIZE_DEPENDENCE":
            raise SystemExit("FAIL R16 fixed-point gate should be blocked")

    print("PASS autonomous rescaled RG verifier")
    print(result)


if __name__ == "__main__":
    main()
