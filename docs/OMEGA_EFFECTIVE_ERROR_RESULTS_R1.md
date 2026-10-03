# Omega Effective-Theory Error Budget Results R1

Status: **FORMAL TOY-MODEL RESULTS - NOT EMPIRICAL PHYSICS**

## Goal

Extend R10 observable preservation from a one-stage coarse-graining bound to multi-stage effective descriptions with explicit residual propagation.

Let q_i : X_(i-1) -> X_i and observables f_i : X_i -> R.
For x_i = q_i(x_(i-1)), assume each stage obeys

|f_(i-1)(x_(i-1)) - f_i(x_i)| <= epsilon_i.

## T19 - additive multi-stage residual bound

For k stages,

|f_0(x_0) - f_k(x_k)| <= sum_i epsilon_i.

Proof: insert and subtract every intermediate observable value and apply the triangle inequality.

## T20 - exact stages compose exactly

If every epsilon_i is zero, exact observable descent is preserved by the composite map.

## T21 - Lipschitz post-processing propagates bounds

If g is L-Lipschitz and |u-v| <= epsilon, then

|g(u)-g(v)| <= L epsilon.

Later sensitive transformations therefore multiply upstream approximation error.

## T22 - affine recurrence bound

If

e_(i+1) <= L_i e_i + delta_i

with nonnegative L_i and delta_i, then

e_n <= e_0 product_(j=0..n-1) L_j
     + sum_(i=0..n-1) delta_i product_(j=i+1..n-1) L_j.

The first term is inherited error; the second is accumulated local residual.

## N9 - small local error does not imply small final error

For repeated T(x)=2x, an initial discrepancy delta becomes 2^n delta after n stages.
Hence local residual size alone cannot certify a final effective description; sensitivity factors must also be tracked.

## Finite verifier witness

The verifier checks:
- additive residual budgets,
- exact closure at zero residual,
- the T22 closed form against direct recurrence iteration,
- delta=1/16 under four doublings, yielding final error 1.

## Effective-field interpretation

This does not derive or validate a physical EFT. It establishes a reusable mathematical contract:
1. declare every approximation/coarse-graining stage;
2. attach a local residual bound;
3. attach downstream sensitivity bounds;
4. propagate the full error budget;
5. reject claims whose declared tolerance is exceeded.

Future instantiations may target lattice fields, renormalization-group flows, amplitudes, or detector response only after domain-specific assumptions are supplied and tested.

## Next frontier

1. vector- and metric-valued observables;
2. approximate operation congruence;
3. stochastic residuals and covariance propagation;
4. lattice scalar-field coarse-graining;
5. comparison with established EFT truncation-error methods.

Version: **R1**
Date: **2026-10-03**
