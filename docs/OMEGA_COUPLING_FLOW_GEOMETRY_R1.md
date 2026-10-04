# Omega Coupling-Flow Geometry Results R1

Status: **FINITE LATTICE FORMAL/COMPUTATIONAL RESULTS - NOT CONTINUUM RG OR EMPIRICAL QFT VALIDATION**

## Goal

Extend R14 from scale-wise effective actions to a local geometry of projected coupling flow.

The projected scalar action is parameterized by

theta = (kappa, m2, lambda)

through

S(phi;theta) = sum_i [
  kappa/2 * (phi_(i+1)-phi_i)^2
  + m2/2 * phi_i^2
  + lambda/4 * phi_i^4
].

At each finite block step, the exact pushed weight is projected back to the retained phi4-like basis, producing a finite projected map

R_k : theta_k -> theta_(k+1).

This map is **scale dependent** because the lattice size and field alphabet change under blocking.

## Coordinate extraction

For an output lattice with N sites and fitted action

S_fit = c0 + c2*M2 + cC*C1 + c4*M4,

the projected physical coordinates are defined by

kappa = -cC/N,

m2 = 2*(c2/N - kappa),

lambda = 4*c4/N.

This is only a coordinate projection of the finite effective action; it is not asserted to be an exact continuum coupling definition.

## T36 - exact ternary mass/quartic alias

On the microscopic alphabet

phi_i in {-1,0,1},

one has pointwise

phi_i^4 = phi_i^2.

Therefore

m2/2 * phi_i^2 + lambda/4 * phi_i^4
=
( m2/2 + lambda/4 ) * phi_i^2.

The microscopic finite witness cannot identify m2 and lambda separately.

Equivalently, the parameter direction

v_null = (0, -1/2, 1)

leaves the microscopic action invariant.

The numerical Jacobian confirms this analytical null direction:

||J_0 v_null|| = 3.4555712597468572e-09,

and the lambda column differs from one half of the m2 column by at most

2.97983859809392e-09.

The 3x3 microscopic Jacobian is therefore classified

RANK_DEFICIENT_BY_TERNARY_ALIAS_PHI4_EQ_PHI2.

Its Frobenius condition estimate is approximately

6.979628518173767e10.

No three-dimensional microscopic eigenmode interpretation is accepted.

## T37 - finite-difference Jacobian stability

Central finite-difference Jacobians were computed at two relative step sizes, 1e-4 and 5e-5.

Maximum relative Jacobian changes were

- microscopic step: 6.067339808006931e-10,
- first coarse step: 1.4302659603173183e-09.

Thus the observed rank deficiency at the microscopic level and the identifiable geometry at the next level are not artifacts of the chosen finite-difference step at the declared precision.

## Projected coupling coordinates

Starting from

theta_0 = (1,1,1),

the exact first push-forward followed by projection gives

theta_1 =
(1.0025373737493564,
 6.336155263803127,
 -6.897723845947594).

The exact two-step push-forward followed by projection gives

theta_2^exact =
(0.8698677071359057,
 6.676551620515189,
 -0.6908425270106108).

If instead the first projected action is treated as the new microscopic model and projected recursively, the second step gives

theta_2^projected =
(1.0025373737493564,
 6.7500880930182365,
 -1.4597114685670747).

## N14 - projection is not closed under recursive RG

The Euclidean coupling-space discrepancy is

||theta_2^exact - theta_2^projected||_2
=
0.7836889067210743.

Therefore replacing the exact level-1 effective action by its restricted phi4 projection and then blocking again does **not** reproduce the exact two-step projected result.

Projection and exact push-forward do not commute in this witness.

This is a concrete mechanism for accumulated model-form error and connects directly to the R11 residual-budget program.

## T38 - identifiable local geometry after one blocking step

After one block transformation, the field alphabet is

{-1,-1/2,0,1/2,1}.

On this alphabet, phi^4 and phi^2 are no longer identical, so the three projected coordinates become locally identifiable.

The measured Jacobian is

J_1 =
[
 [ 0.99999999999721,  0.0,                 3.219099660759575e-13 ],
 [ 0.6367210483289073, 2.2319895070200775, 0.9018010976029259 ],
 [-2.2058319582296244,-0.8038258137274343, 0.15608861739412624 ]
].

Its determinant is

1.0732791572883524

and its Frobenius condition estimate is

18.645245175631917.

The finite-step eigenvalue magnitudes are approximately

1.7877141625664503,
0.9999999999949493,
0.6003639618500127.

They are classified only as

- EXPANDING_FINITE_STEP,
- NEAR_UNIT_FINITE_STEP,
- CONTRACTING_FINITE_STEP.

These labels are **not** continuum relevant/marginal/irrelevant critical exponents.

## N15 - fixed point status is not yet well defined

The raw block map changes

- lattice size,
- field alphabet,
- effective coordinate interpretation.

Therefore an equation such as

theta* = R(theta*)

is not coordinate invariant yet.

A fixed-point search requires an explicit field-rescaling / normalization convention that makes the projected RG map autonomous on a common state and coupling space.

R15 therefore records

NOT_WELL_DEFINED_WITHOUT_FIELD_RESCALE_AND_AUTONOMOUS_COORDINATES

instead of manufacturing a fixed point.

## Scientific boundary

R15 verifies:

- a finite projected coupling map,
- exact microscopic parameter aliasing on the ternary field alphabet,
- finite-difference Jacobian stability,
- recovery of local three-dimensional identifiability after one blocking step,
- finite-step local eigenvalue structure,
- nonzero recursive projection-closure drift,
- the need for explicit rescaling before fixed-point language is admissible.

R15 does **not** establish:

- continuum beta functions,
- continuum scaling dimensions,
- universal critical exponents,
- a continuum fixed point,
- empirical particle physics.

## Next frontier

The next mathematically necessary step is an **autonomous rescaled RG map**:

1. define a field normalization after every block,
2. map every scale back to a common reference alphabet/domain,
3. define dimensionless coupling coordinates,
4. test coordinate stability under alternate normalizations,
5. only then search for approximate fixed points and linearized relevant/marginal/irrelevant directions.

Version: **R1**
Date: **2026-10-04**
