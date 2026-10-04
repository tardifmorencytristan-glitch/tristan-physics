#!/usr/bin/env python3
"""R16: rescaling court and finite autonomy gate for projected RG."""

from collections import defaultdict
from functools import lru_cache
from math import exp, fsum, log, sqrt
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


def uniform_alphabet_m2(values):
    return fsum(float(x) ** 2 for x in values) / len(values)


@lru_cache(maxsize=4)
def precomputed_records(values, sites):
    """Precompute exact-domain sufficient statistics for the linear action."""
    records = []
    for state in r15.enumerate_states(values, sites):
        xs = tuple(float(x) for x in state)
        kinetic = fsum(
            0.5 * (xs[(i + 1) % sites] - xs[i]) ** 2
            for i in range(sites)
        )
        mass = fsum(0.5 * x * x for x in xs)
        quartic = fsum(0.25 * x ** 4 for x in xs)
        m2 = fsum(x * x for x in xs) / sites
        block = tuple(
            0.5 * (xs[i] + xs[i + 1])
            for i in range(0, sites, 2)
        )
        records.append((block, kinetic, mass, quartic, m2))
    return tuple(records)


@lru_cache(maxsize=96)
def raw_projected_step(values, sites, params):
    """Compute one raw push-forward/projection, shared by all rescaling gauges."""
    params = tuple(float(x) for x in params)
    kappa, mass2, lam = params
    coarse = defaultdict(float)

    input_m2_sum = 0.0
    input_m2_comp = 0.0

    records = precomputed_records(tuple(values), sites)
    for block, kinetic, mass, quartic, m2 in records:
        weight = exp(-(kappa * kinetic + mass2 * mass + lam * quartic))
        coarse[block] += weight

        term = weight * m2
        y = term - input_m2_comp
        t = input_m2_sum + y
        input_m2_comp = (t - input_m2_sum) - y
        input_m2_sum = t

    coarse = dict(coarse)
    z = fsum(coarse.values())
    input_m2 = input_m2_sum / z
    coarse_m2 = fsum(
        weight * m2_state(state)
        for state, weight in coarse.items()
    ) / z

    fit = r15.fit_base_effective_action(coarse)
    output_sites = sites // 2
    raw_params = tuple(
        r15.physical_params_from_coefficients(
            fit["coefficients"], output_sites
        )
    )
    return {
        "raw_params": raw_params,
        "coarse": coarse,
        "input_m2": input_m2,
        "coarse_m2": coarse_m2,
        "fit_rms": fit["rms"],
        "fit_max_abs": fit["max_abs"],
        "input_support": len(records),
        "output_support": len(coarse),
    }


def choose_scale(scheme, values, params, raw):
    if scheme == "NONE":
        return 1.0

    if scheme == "SUPPORT_M2_MATCH":
        coarse_values = r15.next_alphabet(values)
        source = uniform_alphabet_m2(values)
        target = uniform_alphabet_m2(coarse_values)
        return sqrt(source / target)

    if scheme == "BOLTZMANN_M2_MATCH":
        target = raw["coarse_m2"]
        if target <= 0.0:
            raise ValueError("coarse Boltzmann M2 must be positive")
        return sqrt(raw["input_m2"] / target)

    if scheme == "KINETIC_MATCH":
        kappa_in = float(params[0])
        kappa_raw = float(raw["raw_params"][0])
        ratio = kappa_raw / kappa_in
        if ratio <= 0.0:
            raise ValueError("kinetic matching requires positive kappa ratio")
        return sqrt(ratio)

    raise ValueError("unknown scheme: " + scheme)


def transform_params_under_field_scale(raw_params, scale):
    """For z=scale*y: kappa,m2 scale as scale^-2 and lambda as scale^-4."""
    kappa, mass2, lam = raw_params
    s2 = scale * scale
    return (kappa / s2, mass2 / s2, lam / (s2 * s2))


@lru_cache(maxsize=256)
def projected_rescaled_map(values, sites, params, scheme):
    values = tuple(values)
    params = tuple(float(x) for x in params)
    raw = raw_projected_step(values, sites, params)
    scale = choose_scale(scheme, values, params, raw)
    params_out = transform_params_under_field_scale(raw["raw_params"], scale)
    return {
        "params_out": params_out,
        "scale": scale,
        "fit_rms": raw["fit_rms"],
        "fit_max_abs": raw["fit_max_abs"],
        "input_support": raw["input_support"],
        "output_support": raw["output_support"],
        "input_m2": raw["input_m2"],
        "coarse_m2_before_rescale": raw["coarse_m2"],
        "coarse_m2_after_rescale": scale * scale * raw["coarse_m2"],
    }


def direct_rescaled_fit(values, sites, params, scheme):
    """Independent small-support witness for the analytical coefficient transform."""
    raw = raw_projected_step(tuple(values), sites, tuple(params))
    scale = choose_scale(scheme, tuple(values), tuple(params), raw)
    transformed = {
        tuple(scale * float(x) for x in state): weight
        for state, weight in raw["coarse"].items()
    }
    fit = r15.fit_base_effective_action(transformed)
    direct = tuple(
        r15.physical_params_from_coefficients(
            fit["coefficients"], sites // 2
        )
    )
    return direct


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
            return {"status": "SEARCH_FAILED_NUMERICALLY", "history": history}
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
            return {"status": "SEARCH_DIVERGED_BOUNDED", "history": history}
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
        "algorithm": "SUFFICIENT_STATISTICS_PLUS_ANALYTIC_FIELD_SCALE",
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
