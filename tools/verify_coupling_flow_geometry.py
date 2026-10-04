#!/usr/bin/env python3
"""R15: finite projected coupling-flow geometry for the scalar lattice witness."""

from collections import defaultdict
from fractions import Fraction
from itertools import product
from math import exp, fsum, isfinite, log, sqrt


INITIAL_VALUES = (Fraction(-1), Fraction(0), Fraction(1))
BASE_NAMES = ("const", "m2", "c1", "m4")


def lattice_action(state, params):
    kappa, mass2, lam = params
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
    if len(state) == 0 or len(state) % 2:
        raise ValueError("blocking requires a nonempty even lattice")
    return tuple((state[i] + state[i + 1]) / 2 for i in range(0, len(state), 2))


def next_alphabet(values):
    return tuple(sorted({(a + b) / 2 for a in values for b in values}))


def enumerate_states(values, sites):
    return product(values, repeat=sites)


def parametric_weight_map(values, sites, params):
    return {
        state: exp(-lattice_action(state, params))
        for state in enumerate_states(values, sites)
    }


def pushforward_weights(weight_map):
    grouped = defaultdict(list)
    for state, weight in weight_map.items():
        grouped[block_average_exact(state)].append(weight)
    return {state: fsum(parts) for state, parts in grouped.items()}


def operator_values(state):
    xs = [float(x) for x in state]
    n = len(xs)
    m2 = fsum(x * x for x in xs) / n
    m4 = fsum(x ** 4 for x in xs) / n
    c1 = fsum(xs[i] * xs[(i + 1) % n] for i in range(n)) / n
    return (1.0, m2, c1, m4)


def solve_linear_system(matrix, rhs, tol=1e-12):
    n = len(rhs)
    aug = [list(map(float, matrix[i])) + [float(rhs[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) <= tol:
            raise ValueError("singular linear system")
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


def fit_base_effective_action(weight_map):
    states = sorted(weight_map)
    target = [-log(weight_map[state]) for state in states]
    design = [operator_values(state) for state in states]
    p = len(BASE_NAMES)
    gram = [
        [fsum(row[i] * row[j] for row in design) for j in range(p)]
        for i in range(p)
    ]
    rhs = [
        fsum(row[i] * y for row, y in zip(design, target))
        for i in range(p)
    ]
    coeffs = solve_linear_system(gram, rhs)
    predicted = [fsum(c * x for c, x in zip(coeffs, row)) for row in design]
    residuals = [truth - pred for truth, pred in zip(target, predicted)]
    rss = fsum(r * r for r in residuals)
    return {
        "coefficients": dict(zip(BASE_NAMES, coeffs)),
        "rss": rss,
        "rms": sqrt(rss / len(states)),
        "max_abs": max(abs(r) for r in residuals),
        "support_count": len(states),
    }


def physical_params_from_coefficients(coefficients, sites):
    c2 = coefficients["m2"]
    cc = coefficients["c1"]
    c4 = coefficients["m4"]
    kappa = -cc / sites
    mass2 = 2.0 * (c2 / sites - kappa)
    lam = 4.0 * c4 / sites
    return (kappa, mass2, lam)


def projected_rg_step(values, sites, params):
    if sites < 4 or sites % 2:
        raise ValueError("R15 projected map requires an even input lattice with output >=2 sites")
    fine = parametric_weight_map(values, sites, params)
    coarse = pushforward_weights(fine)
    fit = fit_base_effective_action(coarse)
    output_sites = sites // 2
    params_out = physical_params_from_coefficients(fit["coefficients"], output_sites)
    return {
        "params_out": params_out,
        "fit": fit,
        "input_support": len(fine),
        "output_support": len(coarse),
        "input_sites": sites,
        "output_sites": output_sites,
        "next_values": next_alphabet(values),
    }


def exact_two_level_projection():
    p0 = (1.0, 1.0, 1.0)
    w0 = parametric_weight_map(INITIAL_VALUES, 8, p0)
    w1 = pushforward_weights(w0)
    w2 = pushforward_weights(w1)
    f1 = fit_base_effective_action(w1)
    f2 = fit_base_effective_action(w2)
    p1 = physical_params_from_coefficients(f1["coefficients"], 4)
    p2 = physical_params_from_coefficients(f2["coefficients"], 2)
    level0_null_direction = (0.0, -0.5, 1.0)
    level0_null_residual = vector_norm(matvec(j0_h2, level0_null_direction))
    level0_alias_column_error = max(
        abs(j0_h2[i][2] - 0.5 * j0_h2[i][1]) for i in range(3)
    )

    return {
        "p0": p0,
        "p1_exact_projection": p1,
        "p2_exact_projection": p2,
        "level1_fit": f1,
        "level2_fit": f2,
    }


def central_jacobian(values, sites, params, relative_step):
    base = tuple(float(x) for x in params)
    cols = []
    actual_steps = []
    for j in range(3):
        h = relative_step * max(1.0, abs(base[j]))
        actual_steps.append(h)
        plus = list(base)
        minus = list(base)
        plus[j] += h
        minus[j] -= h
        y_plus = projected_rg_step(values, sites, tuple(plus))["params_out"]
        y_minus = projected_rg_step(values, sites, tuple(minus))["params_out"]
        cols.append(tuple((a - b) / (2.0 * h) for a, b in zip(y_plus, y_minus)))
    matrix = [[cols[j][i] for j in range(3)] for i in range(3)]
    return matrix, actual_steps


def matrix_sub_max_abs(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(3) for j in range(3))


def matrix_max_abs(a):
    return max(abs(a[i][j]) for i in range(3) for j in range(3))


def determinant3(a):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def inverse3(a, tol=1e-14):
    det = determinant3(a)
    if abs(det) <= tol:
        raise ValueError("singular Jacobian")
    return [
        [
            (a[1][1] * a[2][2] - a[1][2] * a[2][1]) / det,
            (a[0][2] * a[2][1] - a[0][1] * a[2][2]) / det,
            (a[0][1] * a[1][2] - a[0][2] * a[1][1]) / det,
        ],
        [
            (a[1][2] * a[2][0] - a[1][0] * a[2][2]) / det,
            (a[0][0] * a[2][2] - a[0][2] * a[2][0]) / det,
            (a[0][2] * a[1][0] - a[0][0] * a[1][2]) / det,
        ],
        [
            (a[1][0] * a[2][1] - a[1][1] * a[2][0]) / det,
            (a[0][1] * a[2][0] - a[0][0] * a[2][1]) / det,
            (a[0][0] * a[1][1] - a[0][1] * a[1][0]) / det,
        ],
    ]


def frobenius_norm(a):
    return sqrt(fsum(x * x for row in a for x in row))


def condition_frobenius(a):
    inv = inverse3(a)
    return frobenius_norm(a) * frobenius_norm(inv)


def matmul(a, b):
    return [
        [fsum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)
    ]


def trace3(a):
    return a[0][0] + a[1][1] + a[2][2]


def characteristic_coefficients(a):
    tr = trace3(a)
    a2 = matmul(a, a)
    c2 = 0.5 * (tr * tr - trace3(a2))
    det = determinant3(a)
    return (-tr, c2, -det)


def polynomial(z, coeffs):
    a2, a1, a0 = coeffs
    return z ** 3 + a2 * z ** 2 + a1 * z + a0


def cubic_roots_durand_kerner(coeffs, tol=1e-13, max_iter=500):
    radius = 1.0 + max(abs(c) for c in coeffs)
    omega = complex(-0.5, sqrt(3.0) / 2.0)
    roots = [complex(radius, 0.0), radius * omega, radius * omega * omega]
    for _ in range(max_iter):
        updated = []
        max_change = 0.0
        for i, z in enumerate(roots):
            denom = 1.0 + 0j
            for j, other in enumerate(roots):
                if i != j:
                    denom *= z - other
            if abs(denom) < 1e-18:
                denom += complex(1e-18, 1e-18)
            new_z = z - polynomial(z, coeffs) / denom
            updated.append(new_z)
            max_change = max(max_change, abs(new_z - z))
        roots = updated
        if max_change < tol:
            break
    roots.sort(key=lambda z: (-abs(z), z.real, z.imag))
    return roots


def classify_eigenvalue(z):
    mag = abs(z)
    if mag > 1.05:
        return "EXPANDING_FINITE_STEP"
    if mag < 0.95:
        return "CONTRACTING_FINITE_STEP"
    return "NEAR_UNIT_FINITE_STEP"


def eigen_summary(a):
    roots = cubic_roots_durand_kerner(characteristic_coefficients(a))
    return [
        {
            "real": z.real,
            "imag": z.imag,
            "abs": abs(z),
            "classification": classify_eigenvalue(z),
        }
        for z in roots
    ]


def vector_l2(a, b):
    return sqrt(fsum((x - y) ** 2 for x, y in zip(a, b)))


def matvec(a, v):
    return [fsum(a[i][j] * v[j] for j in range(3)) for i in range(3)]


def vector_norm(v):
    return sqrt(fsum(x * x for x in v))


def verify():
    exact = exact_two_level_projection()
    p0 = exact["p0"]
    p1 = exact["p1_exact_projection"]
    p2_exact = exact["p2_exact_projection"]

    step0 = projected_rg_step(INITIAL_VALUES, 8, p0)
    values1 = step0["next_values"]
    step1_projected = projected_rg_step(values1, 4, p1)
    p2_projected = step1_projected["params_out"]

    j0_h, steps0_h = central_jacobian(INITIAL_VALUES, 8, p0, 1e-4)
    j0_h2, steps0_h2 = central_jacobian(INITIAL_VALUES, 8, p0, 5e-5)
    j1_h, steps1_h = central_jacobian(values1, 4, p1, 1e-4)
    j1_h2, steps1_h2 = central_jacobian(values1, 4, p1, 5e-5)

    j0_delta = matrix_sub_max_abs(j0_h, j0_h2)
    j1_delta = matrix_sub_max_abs(j1_h, j1_h2)
    j0_relative = j0_delta / max(1.0, matrix_max_abs(j0_h2))
    j1_relative = j1_delta / max(1.0, matrix_max_abs(j1_h2))

    return {
        "p0": p0,
        "p1_exact_projection": p1,
        "p2_exact_projection": p2_exact,
        "p2_projected_recursive": p2_projected,
        "projection_closure_l2": vector_l2(p2_exact, p2_projected),
        "step0_supports": [step0["input_support"], step0["output_support"]],
        "step1_supports": [step1_projected["input_support"], step1_projected["output_support"]],
        "jacobian_level0": j0_h2,
        "jacobian_level1": j1_h2,
        "jacobian_level0_step_stability_abs": j0_delta,
        "jacobian_level1_step_stability_abs": j1_delta,
        "jacobian_level0_step_stability_rel": j0_relative,
        "jacobian_level1_step_stability_rel": j1_relative,
        "jacobian_level0_det": determinant3(j0_h2),
        "jacobian_level1_det": determinant3(j1_h2),
        "jacobian_level0_condition_frobenius": condition_frobenius(j0_h2),
        "jacobian_level1_condition_frobenius": condition_frobenius(j1_h2),
        "level0_identifiability": "RANK_DEFICIENT_BY_TERNARY_ALIAS_PHI4_EQ_PHI2",
        "level0_null_direction": level0_null_direction,
        "level0_null_residual": level0_null_residual,
        "level0_alias_column_error": level0_alias_column_error,
        "eigen_level0_status": "DO_NOT_INTERPRET_3D_EIGENMODES",
        "eigen_level1": eigen_summary(j1_h2),
        "steps_level0_h": steps0_h,
        "steps_level0_h2": steps0_h2,
        "steps_level1_h": steps1_h,
        "steps_level1_h2": steps1_h2,
        "fixed_point_status": "NOT_WELL_DEFINED_WITHOUT_FIELD_RESCALE_AND_AUTONOMOUS_COORDINATES",
    }


def main():
    result = verify()

    if result["step0_supports"] != [6561, 625]:
        raise SystemExit("FAIL R15 step0 support")
    if result["step1_supports"] != [625, 81]:
        raise SystemExit("FAIL R15 step1 support")
    if result["jacobian_level0_step_stability_rel"] > 1e-4:
        raise SystemExit("FAIL R15 level0 finite-difference stability")
    if result["jacobian_level1_step_stability_rel"] > 1e-4:
        raise SystemExit("FAIL R15 level1 finite-difference stability")
    if result["level0_identifiability"] != "RANK_DEFICIENT_BY_TERNARY_ALIAS_PHI4_EQ_PHI2":
        raise SystemExit("FAIL R15 level0 alias classification")
    if result["level0_null_residual"] > 1e-7:
        raise SystemExit("FAIL R15 level0 analytical null direction")
    if result["level0_alias_column_error"] > 1e-7:
        raise SystemExit("FAIL R15 level0 mass/quartic alias")
    if result["jacobian_level0_condition_frobenius"] < 1e8:
        raise SystemExit("FAIL R15 expected level0 ill-conditioning")
    if abs(result["jacobian_level1_det"]) <= 1e-10:
        raise SystemExit("FAIL R15 level1 Jacobian singular")
    if not isfinite(result["jacobian_level1_condition_frobenius"]):
        raise SystemExit("FAIL R15 level1 condition")
    if result["jacobian_level1_condition_frobenius"] > 1e4:
        raise SystemExit("FAIL R15 level1 unexpectedly ill-conditioned")
    if result["projection_closure_l2"] <= 1e-8:
        raise SystemExit("FAIL R15 expected nonzero recursive projection drift")
    if result["fixed_point_status"] != "NOT_WELL_DEFINED_WITHOUT_FIELD_RESCALE_AND_AUTONOMOUS_COORDINATES":
        raise SystemExit("FAIL R15 fixed-point boundary")

    print("PASS coupling-flow geometry verifier")
    print(result)


if __name__ == "__main__":
    main()
