# Omega Multiscale RG Flow Results R1

Status: **FINITE LATTICE FORMAL/COMPUTATIONAL RESULTS - NOT CONTINUUM RG OR EMPIRICAL QFT VALIDATION**

## Goal

Extend R13 from one exact coarse-graining step to an exact finite multiscale flow

8 sites -> 4 sites -> 2 sites -> 1 site

while preserving explicit evidence, operator identifiability, and approximation residuals at every scale.

The microscopic witness is a periodic N=8 scalar lattice with values in {-1,0,1} and

S(phi) = sum_i [
  1/2 * (phi_(i+1)-phi_i)^2
  + 1/2 * phi_i^2
  + 1/4 * phi_i^4
].

All coarse field states are represented internally by exact rational numbers.

## T32 - exact block-map composition

Let B be the two-site arithmetic-mean block map.

For every one of the 3^8 = 6561 microscopic configurations and k=1,2,3,

B^k(phi)

is exactly equal, as a rational state, to direct averaging over groups of 2^k microscopic sites.

The exhaustive witness found:

- map composition failures: 0
- maximum rational map-composition error: 0

Thus the deterministic coarse-graining maps close exactly under composition in this finite construction.

## T33 - push-forward functoriality and partition preservation

Let W_0 be the microscopic Boltzmann weight map and define recursively

W_(k+1) = B_* W_k.

The support sizes are

6561 -> 625 -> 81 -> 17.

The partition function is

Z = 14.896897569403215

at every level within the numerical representation.

Measured partition differences relative to the microscopic level:

[0, 0, 0, 0].

Direct push-forward from the microscopic level and repeated push-forward agree with maximum absolute weight discrepancies

[0, 5.551115123125783e-17, 2.220446049250313e-16].

This is a finite numerical witness of push-forward functoriality.

## T34 - Z2 inheritance and exact effective actions at every scale

For each coarse level k, define

S_eff^(k)(y) = -log W_k(y).

At all three coarse levels:

W_k(-y)=W_k(y)

with measured maximum Z2 weight error 0.

The maximum reconstruction errors in

exp(-S_eff^(k)(y)) = W_k(y)

are respectively

- 4-site level: 2.7755575615628914e-17
- 2-site level: 2.7755575615628914e-17
- 1-site level: 4.440892098500626e-16.

## FlowGenome

For each scale k, R14 records

Gamma_k = (
  N_k,
  support_k,
  Z_k,
  operator_basis_k,
  theta_k,
  RSS_k,
  RMS_k,
  KL_k,
  candidate_court_k,
  identifiability_k
).

The full finite flow is

Gamma_RG = {Gamma_1, Gamma_2, Gamma_3}.

### Level 1 - 4 sites

Base basis:

{1, M2, C1, M4}.

Base fit:

- RSS = 20.04860550801036
- RMS = 0.17910267673269592
- max absolute action residual = 0.56600739953603
- KL = 0.005304213422490202.

Operator court:

- best action-RSS candidate: M2^2
- action-RSS gain: 0.9473907288356003
- best KL candidate: M2*C1
- KL gain: 3.983143383874156e-06
- M6: REDUNDANT_OR_SINGULAR on this finite support.

### Level 2 - 2 sites

Base fit:

- RSS = 1.2446472353115785
- RMS = 0.12395973237612377
- max absolute action residual = 0.36999512707619964
- KL = 0.009251523879000956.

Best tested candidate on both measured objectives:

M6.

Measured gains:

- action-RSS gain = 0.4053577908517164
- KL gain = 0.005535368724080657.

### Level 3 - 1 site

Base basis:

{1, M2, M4}.

Base fit:

- RSS = 0.039258542546861085
- RMS = 0.04805544747651716
- max absolute action residual = 0.08887659999783071
- KL = 0.0011891894344225693.

Best tested candidate on both measured objectives:

M6.

Measured gains:

- action-RSS gain = 0.03710126046627341
- KL gain = 0.0010406846001832838.

## N12 - the restricted retained operator family is not closed under this finite RG flow

At every coarse scale, the restricted base effective-action family has a nonzero maximum residual:

0.56600739953603,
0.36999512707619964,
0.08887659999783071.

Therefore the retained base operator family is not exactly closed under the finite block transformation used here.

This does not imply failure of phi4 field theory. It shows only that an exactly pushed finite effective action generally requires more structure than this restricted projected basis.

## N13 - operator identifiability is scale dependent

M6 is redundant or singular relative to the retained basis on the 4-site support, but it becomes identifiable at the 2-site and 1-site levels and is the strongest tested candidate there on both RSS and KL.

Thus operator identity alone is insufficient metadata.

A candidate must carry at least

(operator, scale, support, retained basis, identifiability status, score functional).

## T35 - operator ranking is both scale and objective dependent

At 4 sites:

argmax action gain = M2^2

while

argmax KL gain = M2*C1.

At 2 and 1 sites, M6 wins both measured objectives among the tested candidates.

Hence no scale-independent or objective-independent operator winner exists in this finite court.

## R11 residual-chain bridge

The base action-space RMS residuals form the scale sequence

[0.17910267673269592,
 0.12395973237612377,
 0.04805544747651716].

Their unit-sensitivity sum is

0.35111785658533684.

This quantity is recorded only as R11-compatible residual bookkeeping. It is **not** asserted to be a physical observable-error bound unless downstream sensitivity assumptions linking action residuals to observables are supplied.

## Scientific boundary

R14 verifies:

- exact rational block-map composition,
- exact finite state support flow,
- finite push-forward consistency,
- partition preservation,
- Z2 inheritance,
- exact support-level effective actions,
- finite projected effective-action residuals,
- scale-local operator identifiability,
- scale- and objective-dependent candidate rankings.

It does **not** establish:

- a continuum RG trajectory,
- continuum beta functions,
- critical exponents,
- a renormalized continuum field theory,
- a new particle or interaction,
- empirical agreement.

## Next frontier

1. infer discrete coupling-flow coordinates from successive effective actions,
2. compare projection schemes: uniform-support, Boltzmann-weighted, KL-optimal,
3. construct covariance-aware residual tensors,
4. generate symmetry-compatible operators automatically,
5. compute finite Jacobians of coupling flow and search for approximate fixed points,
6. scale beyond exhaustive enumeration using Monte Carlo with exact small-lattice regression tests.

Version: **R1**
Date: **2026-10-04**
