# Omega Lattice Phi4 Bridge Results R1

Status: **FINITE LATTICE FORMAL/COMPUTATIONAL RESULTS - NOT CONTINUUM OR EMPIRICAL QFT VALIDATION**

## Goal

Instantiate the R10-R11 coarse-graining and error-budget machinery in a concrete scalar-field setting.

Consider an even periodic one-dimensional lattice with real field values phi_i and Euclidean action

S(phi) = sum_i [
  kappa/2 * (phi_(i+1)-phi_i)^2
  + m2/2 * phi_i^2
  + lambda/4 * phi_i^4
].

Indices are periodic.

For the exhaustive software witness only, field values are restricted to the finite symmetric alphabet {-1,0,1} on N=4 sites. The identities below are algebraic and are not limited to that alphabet unless explicitly stated.

## Definitions

For N=2M, define the two-site block average

(B phi)_j = (phi_(2j) + phi_(2j+1))/2.

Define

M2(phi) = (1/N) sum_i phi_i^2,

M4(phi) = (1/N) sum_i phi_i^4,

C1(phi) = (1/N) sum_i phi_i phi_(i+1),

and the mean within-block variance

V_B(phi) = (1/M) sum_j (phi_(2j)-phi_(2j+1))^2 / 4.

The coarse second moment is

M2_c(B phi) = (1/M) sum_j (B phi)_j^2.

## T23 - exact block second-moment residual identity

For every even lattice configuration,

M2(phi) - M2_c(B phi) = V_B(phi).

Proof: for each pair a,b,

(a^2+b^2)/2 - ((a+b)/2)^2 = (a-b)^2/4.

Average over all blocks.

This gives an exact, nonnegative coarse-graining residual for the second moment.

## T24 - Z2 covariance of the action and block map

Under the global sign transformation phi -> -phi,

S(-phi) = S(phi)

and

B(-phi) = -B(phi).

Therefore the chosen coarse-graining respects the Z2 symmetry of the scalar action.

## T25 - odd observables cancel in a finite symmetric ensemble

Let the finite configuration space be closed under phi -> -phi, and let the statistical weight be proportional to exp(-S(phi)).

For every odd observable O(-phi)=-O(phi),

< O > = 0.

Proof: pair every configuration phi with -phi. Their weights are equal by T24 and their observable values cancel.

The finite witness checks this for the mean field.

## T26 - ensemble residual identity

Taking expectations of T23 gives

< M2_fine > - < M2_coarse > = < V_B >.

Thus the loss in second moment under block averaging is exactly the ensemble-mean unresolved within-block fluctuation.

This is a direct physical instantiation of an R11 stage residual.

## T27 - action density decomposes into moments and nearest-neighbor correlation

For a periodic lattice,

(1/N) sum_i (phi_(i+1)-phi_i)^2 = 2(M2-C1).

Hence

S(phi)/N
= kappa (M2-C1)
+ (m2/2) M2
+ (lambda/4) M4.

This makes the lattice action directly expressible through observable moments and the nearest-neighbor correlator.

## N10 - the blocked field does not determine the microscopic action

Use N=4 and kappa=m2=lambda=1.

The two configurations

phi = (1,-1,0,0)

and

psi = (0,0,0,0)

both block to

B phi = B psi = (0,0),

but

S(phi) = 4.5

while

S(psi) = 0.

Therefore no function of the blocked field alone can reconstruct the microscopic action for all configurations in this model.

Coarse-graining has genuinely discarded information.

## Exhaustive finite witness

The verifier enumerates all 3^4 = 81 configurations in {-1,0,1}^4 and checks:

- T23 pointwise on every configuration,
- T24 pointwise on every configuration,
- T27 pointwise on every configuration,
- T25 for the exact finite Boltzmann ensemble,
- T26 for the same ensemble,
- N10 with the explicit pair above.

## Scientific boundary

These results establish exact algebraic identities and a finite exhaustive computational witness for a one-dimensional lattice scalar model.

They do **not** establish:
- a continuum limit,
- renormalizability of a new theory,
- a new particle,
- a new quantum field theory,
- agreement with experiment.

## Next frontier

1. induced blocked probability distribution and effective couplings,
2. covariance matrices and vector-valued residual budgets,
3. repeated block transformations and R11 multi-stage propagation,
4. larger lattices and Monte Carlo sampling,
5. comparison with standard renormalization-group and EFT truncation methods,
6. two-point correlation length and scale flow.

Version: **R1**
Date: **2026-10-03**
