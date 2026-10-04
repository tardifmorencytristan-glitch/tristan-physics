# Omega Autonomous Rescaled RG Results R1

Status: **FINITE LATTICE FORMAL/COMPUTATIONAL RESULTS - NOT CONTINUUM RG OR EMPIRICAL QFT VALIDATION**

## Goal

R15 established that fixed-point language is not admissible until the projected RG map is expressed in common coordinates with an explicit field-rescaling convention.

R16 therefore builds a **rescaling court** on a common five-value reference alphabet

{-1,-1/2,0,1/2,1}

and compares the same projected coupling map at two finite sizes:

N=8 -> 4

and

N=4 -> 2.

The reference coupling point is the R15 first projected point

theta_ref =
(1.0025373737493564,
 6.336155263803127,
 -6.897723845947594).

## Common finite supports

At N=8, the reference alphabet gives

5^8 = 390625

input states and the pair-average output has

9^4 = 6561

states.

At N=4, the same reference alphabet gives

5^4 = 625

input states and

9^2 = 81

output states.

Thus the two maps are compared in the same input field alphabet and the same projected coupling coordinates, while retaining explicit finite-size dependence.

## T39 - field-rescaling law for projected couplings

For the coordinate change

z = a y,

the retained action coefficients transform as

kappa' = kappa / a^2,

m2' = m2 / a^2,

lambda' = lambda / a^4.

R16 uses this analytical transform instead of refitting every rescaled support.

An independent direct refit on the small N=4 support agrees with the analytical transformation to the unit-test tolerance.

## Rescaling court

Four declared normalizations were compared:

1. NONE
2. SUPPORT_M2_MATCH
3. BOLTZMANN_M2_MATCH
4. KINETIC_MATCH

The court objective is the relative coupling-map discrepancy

d_map =
||R_8(theta_ref)-R_4(theta_ref)||_2
/
max(1, ||R_8(theta_ref)||_2, ||R_4(theta_ref)||_2).

The declared map autonomy tolerance is

0.05.

### Court results

| Scheme | Relative map discrepancy | Scale N=8 | Scale N=4 |
| --- | ---: | ---: | ---: |
| BOLTZMANN_M2_MATCH | 0.043242478789013494 | 1.2923132299208768 | 1.2883319952219607 |
| SUPPORT_M2_MATCH | 0.04344924397300383 | 1.0954451150103321 | 1.0954451150103321 |
| NONE | 0.04798366312934844 | 1.0 | 1.0 |
| KINETIC_MATCH | 0.048648456193393995 | 1.0003926785927215 | 1.0 |

The declared winner is therefore

BOLTZMANN_M2_MATCH.

Its scale-factor logarithmic gap is

0.0030854592631274305.

## T40 - best tested rescaling passes the map-level finite-size gate

For BOLTZMANN_M2_MATCH,

R_8(theta_ref) =
(0.600766905014788,
 3.919040634231423,
 -0.4284272452265697),

while

R_4(theta_ref) =
(0.6040111932098129,
 4.0668097470395566,
 -0.5298535523114655).

The relative discrepancy is

0.043242478789013494 < 0.05.

Thus the best tested normalization passes the declared **map-level** autonomy gate at this reference point.

This is only a local finite-size witness.

## T41 - Jacobians are numerically stable under step refinement

Central finite-difference Jacobians were computed at relative steps

1e-4

and

5e-5.

The relative changes were

- N=8: 6.241222106346949e-10
- N=4: 6.445898698970088e-10.

Both are far below the declared finite-difference tolerance

1e-4.

The cross-size Jacobian discrepancy is therefore not explained by the tested finite-difference step.

## N16 - map agreement does not imply local RG-geometry agreement

For the winning normalization, the refined Jacobians are

J_8 =
[
 [ 0.6650469416755107, -0.021254002571437475, -0.010221637091402454 ],
 [ 0.5621801002547171,  1.1949649926162746,    0.47834596363737814  ],
 [-0.6809149537459754, -0.2496185868264839,    0.06819237369864867  ]
]

and

J_4 =
[
 [ 0.6750246455276249, -0.02330873923962204,  -0.011211958452129253 ],
 [ 0.8720400237702993,  1.1877967186524905,    0.46782919238291476  ],
 [-0.9279557720451156, -0.2508828103850856,    0.07632866086195018  ]
].

Their relative Frobenius discrepancy is

0.20414221604038493.

The declared Jacobian-autonomy tolerance is

0.10.

Therefore

0.20414221604038493 > 0.10.

The rescaled finite RG map is **not autonomous under the declared R16 gate**, even though the map values themselves are relatively close.

This is a concrete finite witness that

local map agreement != local flow-geometry agreement.

## N17 - fixed-point search remains blocked

The full R16 autonomy gate requires simultaneously:

- map discrepancy <= 0.05,
- Jacobian discrepancy <= 0.10,
- finite-difference instability <= 1e-4.

Measured status:

- map gate: PASS,
- Jacobian gate: FAIL,
- finite-difference gate: PASS.

Therefore

autonomy gate = FAIL

and R16 records

BLOCKED_NONAUTONOMOUS_FINITE_SIZE_DEPENDENCE.

No fixed-point search was executed after the gate failed.

This preserves the R15 requirement that fixed-point claims must only be generated after common-coordinate autonomy is demonstrated.

## Performance correction

The first R16 implementation recomputed the full finite action and push-forward separately for every gauge and finite-difference perturbation and did not complete promptly.

That run was terminated without being classified as a scientific failure.

The verified implementation uses:

- precomputed sufficient statistics for the action,
- cached raw push-forwards,
- analytical coupling transformation under field rescaling.

The scientific court, metrics, and thresholds were unchanged.

## Scientific boundary

R16 verifies:

- a common five-value reference domain,
- four explicit field-rescaling conventions,
- map-level finite-size comparison,
- a winning tested normalization under the declared map objective,
- stable finite-difference Jacobians,
- failure of the stronger Jacobian autonomy gate,
- correct blocking of fixed-point search.

R16 does **not** establish:

- an autonomous continuum RG,
- a continuum fixed point,
- beta functions,
- universal critical exponents,
- relevant/marginal/irrelevant continuum directions,
- empirical particle physics.

## Next frontier

The immediate residual is now narrower:

1. identify which Jacobian entries carry the dominant N=8 vs N=4 mismatch,
2. enlarge the retained operator basis before projection,
3. test whether missing operators reduce Jacobian non-autonomy,
4. compare action-RSS-selected and KL-selected bases,
5. repeat the same rescaling court,
6. admit fixed-point search only if both map and Jacobian gates pass.

Version: **R1**
Date: **2026-10-04**
