#!/usr/bin/env python3
"""R17: operator-closure court for finite rescaled RG autonomy."""

from array import array
from functools import lru_cache
from itertools import combinations, product
from math import exp, fsum, log, sqrt
from pathlib import Path
import sys

TOOLS_DIR = str(Path(__file__).resolve().parent)
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import verify_coupling_flow_geometry as r15
import verify_autonomous_rescaled_rg as r16


BASE = ("kappa", "mass2", "lambda")
CANDIDATES = ("m2_sq", "m2_c1", "delta4", "m6")
ALL_PARAMS = BASE + CANDIDATES
DEGREE = {
    "kappa": 2,
    "mass2": 2,
    "lambda": 4,
    "m2_sq": 4,
    "m2_c1": 4,
    "delta4": 4,
    "m6": 6,
}
MAP_AUTONOMY_TOL = r16.MAP_AUTONOMY_TOL
JACOBIAN_AUTONOMY_TOL = r16.JACOBIAN_AUTONOMY_TOL
DERIVATIVE_TOL = r16.FD_STABILITY_TOL


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
            for i in range(len(a))
            for j in range(len(a[0]))
        )
    )


def relative_vector_distance(a, b):
    return vector_distance(a, b) / max(1.0, l2(a), l2(b))


def relative_matrix_distance(a, b):
    return matrix_distance(a, b) / max(1.0, frobenius(a), frobenius(b))


def feature_values(state):
    xs = [float(x) for x in state]
    n = len(xs)
    sq_sum = fsum(x * x for x in xs)
    c1_sum = fsum(xs[i] * xs[(i + 1) % n] for i in range(n))
    kinetic = fsum(
        0.5 * (xs[(i + 1) % n] - xs[i]) ** 2
        for i in range(n)
    )
    mass = 0.5 * sq_sum
    quartic = 0.25 * fsum(x ** 4 for x in xs)
    m2_sq = 0.25 * sq_sum * sq_sum / n
    m2_c1 = 0.5 * (sq_sum / n) * c1_sum
    delta4 = 0.25 * fsum(
        (xs[(i + 1) % n] - xs[i]) ** 4
        for i in range(n)
    )
    m6 = fsum(x ** 6 for x in xs) / 6.0
    return {
        "kappa": kinetic,
        "mass2": mass,
        "lambda": quartic,
        "m2_sq": m2_sq,
        "m2_c1": m2_c1,
        "delta4": delta4,
        "m6": m6,
    }


def mean_m2(state):
    xs = [float(x) for x in state]
    return fsum(x * x for x in xs) / len(xs)


@lru_cache(maxsize=4)
def domain(values, sites):
    values = tuple(values)
    next_values = r15.next_alphabet(values)
    out_sites = sites // 2
    coarse_states = tuple(product(next_values, repeat=out_sites))
    coarse_index = {state: i for i, state in enumerate(coarse_states)}

    block_codes = array("H" if len(coarse_states) <= 65535 else "I")
    input_m2 = array("d")
    columns = {name: array("d") for name in ALL_PARAMS}

    for state in r15.enumerate_states(values, sites):
        block = r15.block_average_exact(state)
        block_codes.append(coarse_index[block])
        feats = feature_values(state)
        for name in ALL_PARAMS:
            columns[name].append(feats[name])
        input_m2.append(mean_m2(state))

    coarse_columns = {
        name: array("d", (feature_values(state)[name] for state in coarse_states))
        for name in ALL_PARAMS
    }
    coarse_m2 = array("d", (mean_m2(state) for state in coarse_states))

    return {
        "values": values,
        "sites": sites,
        "next_values": next_values,
        "out_sites": out_sites,
        "coarse_states": coarse_states,
        "block_codes": block_codes,
        "input_m2": input_m2,
        "columns": columns,
        "coarse_columns": coarse_columns,
        "coarse_m2": coarse_m2,
        "input_count": len(block_codes),
        "output_count": len(coarse_states),
    }


def solve_linear_system(matrix, rhs, tol=1e-11):
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


def family_names(candidates):
    return BASE + tuple(candidates)


def design_columns(dom, family):
    return [array("d", [1.0] * dom["output_count"])] + [
        dom["coarse_columns"][name] for name in family
    ]


def gram_matrix(cols):
    p = len(cols)
    return [
        [fsum(a * b for a, b in zip(cols[i], cols[j])) for j in range(p)]
        for i in range(p)
    ]


def fit_from_target(dom, family, target):
    cols = design_columns(dom, family)
    gram = gram_matrix(cols)
    rhs = [fsum(x * y for x, y in zip(col, target)) for col in cols]
    coeffs = solve_linear_system(gram, rhs)
    predicted = [
        fsum(coeffs[j] * cols[j][i] for j in range(len(cols)))
        for i in range(dom["output_count"])
    ]
    residuals = [target[i] - predicted[i] for i in range(len(target))]
    rss = fsum(r * r for r in residuals)
    return {
        "coefficients": coeffs,
        "gram": gram,
        "columns": cols,
        "rss": rss,
        "rms": sqrt(rss / len(target)),
        "max_abs": max(abs(r) for r in residuals),
    }


@lru_cache(maxsize=4)
def reference_aggregate(values, sites):
    dom = domain(tuple(values), sites)
    theta3 = tuple(r15.exact_two_level_projection()["p1_exact_projection"])
    nout = dom["output_count"]

    weights = [0.0] * nout
    conditional_sums = {
        name: [0.0] * nout for name in ALL_PARAMS
    }
    z = 0.0
    input_m2_num = 0.0
    feature_num = {name: 0.0 for name in ALL_PARAMS}
    input_m2_feature_num = {name: 0.0 for name in ALL_PARAMS}

    cols = dom["columns"]
    block_codes = dom["block_codes"]
    m2_col = dom["input_m2"]

    for i in range(dom["input_count"]):
        action = (
            theta3[0] * cols["kappa"][i]
            + theta3[1] * cols["mass2"][i]
            + theta3[2] * cols["lambda"][i]
        )
        w = exp(-action)
        b = block_codes[i]
        weights[b] += w
        z += w
        m2 = m2_col[i]
        input_m2_num += w * m2
        for name in ALL_PARAMS:
            f = cols[name][i]
            conditional_sums[name][b] += w * f
            feature_num[name] += w * f
            input_m2_feature_num[name] += w * m2 * f

    return {
        "weights": weights,
        "conditional_sums": conditional_sums,
        "z": z,
        "input_m2_num": input_m2_num,
        "feature_num": feature_num,
        "input_m2_feature_num": input_m2_feature_num,
    }


def analyze_family_at_size(values, sites, candidates):
    family = family_names(candidates)
    dom = domain(tuple(values), sites)
    agg = reference_aggregate(tuple(values), sites)
    weights = agg["weights"]
    target = [-log(w) for w in weights]

    fit = fit_from_target(dom, family, target)
    raw = fit["coefficients"][1:]

    selected = list(family)
    parameter_indices = [ALL_PARAMS.index(name) for name in selected]

    raw_jac = [[0.0 for _ in selected] for _ in selected]
    cols = fit["columns"]
    gram = fit["gram"]

    for j, input_name in enumerate(selected):
        dy = [
            agg["conditional_sums"][input_name][b] / weights[b]
            for b in range(dom["output_count"])
        ]
        rhs = [fsum(x * y for x, y in zip(col, dy)) for col in cols]
        dcoeff = solve_linear_system(gram, rhs)[1:]
        for i in range(len(selected)):
            raw_jac[i][j] = dcoeff[i]

    z = agg["z"]
    input_m2 = agg["input_m2_num"] / z
    coarse_m2 = fsum(
        weights[b] * dom["coarse_m2"][b]
        for b in range(dom["output_count"])
    ) / z
    scale = sqrt(input_m2 / coarse_m2)

    dlog_scale = []
    for name in selected:
        ef = agg["feature_num"][name] / z
        e_input_m2_f = agg["input_m2_feature_num"][name] / z
        d_input_m2 = -(e_input_m2_f - input_m2 * ef)

        e_coarse_m2_f = fsum(
            dom["coarse_m2"][b] * agg["conditional_sums"][name][b]
            for b in range(dom["output_count"])
        ) / z
        d_coarse_m2 = -(e_coarse_m2_f - coarse_m2 * ef)

        dlog_scale.append(
            0.5 * (
                d_input_m2 / input_m2
                - d_coarse_m2 / coarse_m2
            )
        )

    params_out = []
    jacobian = []
    for i, name in enumerate(selected):
        degree = DEGREE[name]
        factor = scale ** (-degree)
        params_out.append(raw[i] * factor)
        jacobian.append([
            factor * (
                raw_jac[i][j]
                - degree * raw[i] * dlog_scale[j]
            )
            for j in range(len(selected))
        ])

    return {
        "family": selected,
        "candidates": list(candidates),
        "params_out": tuple(params_out),
        "jacobian": jacobian,
        "scale": scale,
        "fit_rms": fit["rms"],
        "fit_max_abs": fit["max_abs"],
        "input_support": dom["input_count"],
        "output_support": dom["output_count"],
    }


def base_block(matrix):
    return [row[:3] for row in matrix[:3]]


def matrix_entry_attribution(a, b, row_names, col_names, limit=8):
    rows = []
    for i, row_name in enumerate(row_names):
        for j, col_name in enumerate(col_names):
            rows.append({
                "row": row_name,
                "column": col_name,
                "n8": a[i][j],
                "n4": b[i][j],
                "abs_gap": abs(a[i][j] - b[i][j]),
            })
    rows.sort(key=lambda x: (-x["abs_gap"], x["row"], x["column"]))
    return rows[:limit]


def family_label(candidates):
    return "BASE_ONLY" if not candidates else "BASE+" + "+".join(candidates)


def candidate_subsets():
    out = [tuple()]
    for size in range(1, len(CANDIDATES) + 1):
        out.extend(combinations(CANDIDATES, size))
    return tuple(out)


def court(values):
    entries = []
    for subset in candidate_subsets():
        label = family_label(subset)
        try:
            n8 = analyze_family_at_size(tuple(values), 8, subset)
            n4 = analyze_family_at_size(tuple(values), 4, subset)
        except ValueError as exc:
            entries.append({
                "label": label,
                "candidates": list(subset),
                "status": "REDUNDANT_OR_SINGULAR",
                "reason": str(exc),
            })
            continue

        map_rel = relative_vector_distance(
            n8["params_out"], n4["params_out"]
        )
        jac_rel = relative_matrix_distance(
            n8["jacobian"], n4["jacobian"]
        )
        base_jac_rel = relative_matrix_distance(
            base_block(n8["jacobian"]),
            base_block(n4["jacobian"]),
        )
        autonomy_ratio = max(
            map_rel / MAP_AUTONOMY_TOL,
            jac_rel / JACOBIAN_AUTONOMY_TOL,
        )
        entries.append({
            "label": label,
            "candidates": list(subset),
            "status": "FIT",
            "dimension": len(n8["family"]),
            "map_relative_discrepancy": map_rel,
            "jacobian_relative_discrepancy": jac_rel,
            "base_block_jacobian_relative_discrepancy": base_jac_rel,
            "n8_fit_rms": n8["fit_rms"],
            "n4_fit_rms": n4["fit_rms"],
            "n8_scale": n8["scale"],
            "n4_scale": n4["scale"],
            "map_gate_pass": map_rel <= MAP_AUTONOMY_TOL,
            "jacobian_gate_pass": jac_rel <= JACOBIAN_AUTONOMY_TOL,
            "autonomy_ratio": autonomy_ratio,
        })
    return entries


def select_winner(entries):
    fitted = [x for x in entries if x["status"] == "FIT"]
    passing = [
        x for x in fitted
        if x["map_gate_pass"] and x["jacobian_gate_pass"]
    ]
    if passing:
        winner = min(
            passing,
            key=lambda x: (
                len(x["candidates"]),
                x["autonomy_ratio"],
                0.5 * (x["n8_fit_rms"] + x["n4_fit_rms"]),
                x["label"],
            ),
        )
        return winner, "AUTONOMY_PASSING_FAMILY_FOUND"

    winner = min(
        fitted,
        key=lambda x: (
            x["autonomy_ratio"],
            len(x["candidates"]),
            0.5 * (x["n8_fit_rms"] + x["n4_fit_rms"]),
            x["label"],
        ),
    )
    return winner, "NO_AUTONOMY_PASSING_FAMILY"


def direct_projected_map(values, sites, candidates, params):
    family = family_names(candidates)
    if len(params) != len(family):
        raise ValueError("parameter dimension mismatch")

    dom = domain(tuple(values), sites)
    weights = [0.0] * dom["output_count"]
    z = 0.0
    input_m2_num = 0.0
    cols = dom["columns"]

    for i in range(dom["input_count"]):
        action = fsum(
            params[j] * cols[name][i]
            for j, name in enumerate(family)
        )
        w = exp(-action)
        b = dom["block_codes"][i]
        weights[b] += w
        z += w
        input_m2_num += w * dom["input_m2"][i]

    target = [-log(w) for w in weights]
    fit = fit_from_target(dom, family, target)
    raw = fit["coefficients"][1:]

    input_m2 = input_m2_num / z
    coarse_m2 = fsum(
        weights[b] * dom["coarse_m2"][b]
        for b in range(dom["output_count"])
    ) / z
    scale = sqrt(input_m2 / coarse_m2)

    return tuple(
        raw[i] * scale ** (-DEGREE[name])
        for i, name in enumerate(family)
    )


def finite_difference_jacobian(values, sites, candidates, params, relative_step):
    base = tuple(float(x) for x in params)
    columns = []
    for j in range(len(base)):
        h = relative_step * max(1.0, abs(base[j]))
        plus = list(base)
        minus = list(base)
        plus[j] += h
        minus[j] -= h
        y_plus = direct_projected_map(
            tuple(values), sites, tuple(candidates), tuple(plus)
        )
        y_minus = direct_projected_map(
            tuple(values), sites, tuple(candidates), tuple(minus)
        )
        columns.append(
            tuple((a - b) / (2.0 * h) for a, b in zip(y_plus, y_minus))
        )
    dim = len(base)
    return [[columns[j][i] for j in range(dim)] for i in range(dim)]


def fixed_point_iteration(values, candidates, theta0, max_iter=6):
    theta = tuple(float(x) for x in theta0)
    history = []
    for _ in range(max_iter):
        try:
            nxt = direct_projected_map(
                tuple(values), 8, tuple(candidates), theta
            )
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
    r16_result = r16.verify()
    values = tuple(r15.next_alphabet(r15.INITIAL_VALUES))
    theta3 = tuple(r15.exact_two_level_projection()["p1_exact_projection"])

    entries = court(values)
    fitted = [x for x in entries if x["status"] == "FIT"]
    baseline = next(x for x in fitted if x["label"] == "BASE_ONLY")
    winner, selection_status = select_winner(entries)
    candidates = tuple(winner["candidates"])

    n8 = analyze_family_at_size(values, 8, candidates)
    n4 = analyze_family_at_size(values, 4, candidates)

    theta_ref = theta3 + tuple(0.0 for _ in candidates)

    fd4_h = finite_difference_jacobian(
        values, 4, candidates, theta_ref, 1e-4
    )
    fd4_h2 = finite_difference_jacobian(
        values, 4, candidates, theta_ref, 5e-5
    )
    fd8_h2 = finite_difference_jacobian(
        values, 8, candidates, theta_ref, 5e-5
    )

    fd4_step = relative_matrix_distance(fd4_h, fd4_h2)
    analytic_fd4 = relative_matrix_distance(n4["jacobian"], fd4_h2)
    analytic_fd8 = relative_matrix_distance(n8["jacobian"], fd8_h2)
    derivative_pass = max(fd4_step, analytic_fd4, analytic_fd8) <= DERIVATIVE_TOL

    autonomy_pass = (
        winner["map_gate_pass"]
        and winner["jacobian_gate_pass"]
        and derivative_pass
    )

    if autonomy_pass:
        fixed_point = fixed_point_iteration(
            values, candidates, theta_ref
        )
        fixed_point_status = fixed_point["status"]
    else:
        fixed_point = None
        fixed_point_status = "BLOCKED_NONAUTONOMOUS_OPERATOR_CLOSURE"

    baseline_n8 = analyze_family_at_size(values, 8, tuple())
    baseline_n4 = analyze_family_at_size(values, 4, tuple())

    best_base_block = min(
        fitted,
        key=lambda x: (
            x["base_block_jacobian_relative_discrepancy"],
            len(x["candidates"]),
            x["label"],
        ),
    )

    return {
        "reference_theta_base": theta3,
        "reference_alphabet": [float(x) for x in values],
        "candidate_operators": list(CANDIDATES),
        "subset_count_including_baseline": len(entries),
        "court": entries,
        "baseline_reproduction": {
            "r16_map_relative_discrepancy": r16_result[
                "winner_map_relative_discrepancy"
            ],
            "r17_base_map_relative_discrepancy": baseline[
                "map_relative_discrepancy"
            ],
            "r16_jacobian_relative_discrepancy": r16_result[
                "jacobian_cross_scale_relative_discrepancy"
            ],
            "r17_base_jacobian_relative_discrepancy": baseline[
                "jacobian_relative_discrepancy"
            ],
        },
        "selection_status": selection_status,
        "winner": winner,
        "best_base_block_family": best_base_block,
        "winner_n8_params_out": n8["params_out"],
        "winner_n4_params_out": n4["params_out"],
        "winner_n8_jacobian": n8["jacobian"],
        "winner_n4_jacobian": n4["jacobian"],
        "winner_top_jacobian_gaps": matrix_entry_attribution(
            n8["jacobian"], n4["jacobian"], n8["family"], n8["family"]
        ),
        "baseline_top_jacobian_gaps": matrix_entry_attribution(
            baseline_n8["jacobian"], baseline_n4["jacobian"],
            baseline_n8["family"], baseline_n8["family"]
        ),
        "finite_difference_n4_step_stability": fd4_step,
        "analytic_vs_fd_n4": analytic_fd4,
        "analytic_vs_fd_n8": analytic_fd8,
        "derivative_tolerance": DERIVATIVE_TOL,
        "derivative_gate_pass": derivative_pass,
        "autonomy_gate_pass": autonomy_pass,
        "fixed_point_status": fixed_point_status,
        "fixed_point_search": fixed_point,
        "map_autonomy_tolerance": MAP_AUTONOMY_TOL,
        "jacobian_autonomy_tolerance": JACOBIAN_AUTONOMY_TOL,
        "support_witness": {
            "n8_input": 5 ** 8,
            "n8_output": 9 ** 4,
            "n4_input": 5 ** 4,
            "n4_output": 9 ** 2,
        },
    }


def main():
    result = verify()

    if result["subset_count_including_baseline"] != 16:
        raise SystemExit("FAIL R17 complete subset lattice")

    if result["support_witness"] != {
        "n8_input": 390625,
        "n8_output": 6561,
        "n4_input": 625,
        "n4_output": 81,
    }:
        raise SystemExit("FAIL R17 support witness")

    base = result["baseline_reproduction"]
    if abs(
        base["r16_map_relative_discrepancy"]
        - base["r17_base_map_relative_discrepancy"]
    ) > 1e-8:
        raise SystemExit("FAIL R17 baseline map reproduction")

    if abs(
        base["r16_jacobian_relative_discrepancy"]
        - base["r17_base_jacobian_relative_discrepancy"]
    ) > 1e-6:
        raise SystemExit("FAIL R17 baseline Jacobian reproduction")

    if not result["derivative_gate_pass"]:
        raise SystemExit("FAIL R17 derivative validation")

    if result["autonomy_gate_pass"]:
        if result["fixed_point_status"] == "BLOCKED_NONAUTONOMOUS_OPERATOR_CLOSURE":
            raise SystemExit("FAIL R17 fixed-point gate mismatch")
    else:
        if result["fixed_point_status"] != "BLOCKED_NONAUTONOMOUS_OPERATOR_CLOSURE":
            raise SystemExit("FAIL R17 blocked-search status")

    print("PASS operator-closure court verifier")
    print(result)


if __name__ == "__main__":
    main()
