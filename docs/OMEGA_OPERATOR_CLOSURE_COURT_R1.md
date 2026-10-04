# Omega Operator-Closure Court Results R1

Status: **FINITE LATTICE FORMAL/COMPUTATIONAL RESULTS - NOT CONTINUUM RG OR EMPIRICAL QFT VALIDATION**

## Goal

R16 showed that the best tested field normalization, `BOLTZMANN_M2_MATCH`, passes the declared cross-size map gate but fails the cross-size Jacobian autonomy gate:

- map discrepancy: 0.043242478789013494 < 0.05,
- Jacobian discrepancy: 0.20414221604038493 > 0.10.

R17 asks whether the R16 Jacobian mismatch can be closed by retaining additional Z2-compatible operators.

The complete tested candidate set is:

- `m2_sq`,
- `m2_c1`,
- `delta4`,
- `m6`.

All 15 nonempty subsets plus the base-only family are tested, for 16 total families.

## Common reference domain

The same five-value input alphabet is used at both sizes:

[
{-1,-1/2,0,1/2,1}.
]

The two maps are:

[
N=8	o4
]

and

[
N=4	o2.
]

The reference base coupling is inherited from R15/R16:

[
	heta_{m ref}
=
(1.0025373737493564,
6.336155263803127,
-6.897723845947594).
]

All candidate couplings are set to zero at the reference point.

## Homogeneous operator coordinates

The retained extensive features are:

[
K_2=rac12sum_i(phi_{i+1}-phi_i)^2,
]

[
M_2=rac12sum_iphi_i^2,
]

[
M_4=rac14sum_iphi_i^4,
]

plus candidate features

[
M_2^2=rac{1}{4N}left(sum_iphi_i^2ight)^2,
]

[
M_2C_1=
rac12
left(rac1Nsum_iphi_i^2ight)
left(sum_iphi_iphi_{i+1}ight),
]

[
Delta_4=rac14sum_i(phi_{i+1}-phi_i)^4,
]

[
M_6=rac16sum_iphi_i^6.
]

Their field-scaling degrees are respectively 2, 2, 4, 4, 4, 4, and 6.

## T42 - R16 baseline reproduction

The R17 formulation reproduces the R16 base-only map and Jacobian court.

R16:

[
d_{m map}=0.043242478789013494,
]

[
d_J=0.20414221604038493.
]

R17 base-only:

[
d_{m map}=0.04324247878887285,
]

[
d_J=0.20414221569466146.
]

The differences are numerical roundoff at the declared reproduction tolerances.

This verifies that the R17 extensive-feature formulation is compatible with the previous physical-coordinate map before testing extra operators.

## T43 - exact local derivative identity

For a coarse block (B),

[
W_B(	heta)=
sum_{phi:,Bphi=B}
e^{-S_	heta(phi)}.
]

For any retained input feature (F_j),

[
oxed{
partial_{	heta_j}[-log W_B]
=
mathbb E_	heta[F_jmid B]
}.
]

R17 uses this identity to obtain the local projected-map Jacobian from one reference ensemble rather than re-enumerating every operator family.

The final selected family is independently validated by finite differences.

Measured derivative validation:

- N=4 step-halving discrepancy: 6.466331012533801e-10,
- analytic vs finite difference at N=4: 1.341473633866872e-10,
- analytic vs finite difference at N=8: 1.6136156650849165e-08.

All are below the retained derivative tolerance (10^{-4}).

## Complete operator-subset court

No tested extension passes the full autonomy gate.

The base-only family remains the best full-space autonomy score:

[
d_{m map}=0.04324247878887285,
]

[
d_J=0.20414221569466146.
]

Thus

[
oxed{	ext{selection status}=
	ext{NO\_AUTONOMY\_PASSING\_FAMILY}}.
]

Two larger families are rejected as singular/redundant on the tested finite supports:

- BASE + m2_sq + m2_c1 + delta4,
- BASE + m2_sq + m2_c1 + delta4 + m6.

This is treated as identifiability information, not as a software failure.

## T44 - DELTA4 improves the physical 3x3 sub-block

Although no expanded family closes the full RG geometry, the family

[
oxed{	ext{BASE}+Delta_4}
]

reduces the cross-size discrepancy of the original physical 3x3 Jacobian block from

[
0.20414221569466146
]

to

[
0.1874308212567953.
]

At the same time, the full 4D Jacobian discrepancy becomes

[
0.36499749666942183,
]

so the expanded family is **not** globally more autonomous.

This is a finite witness that

[
oxed{
	ext{better base-sector closure}

otRightarrow
	ext{better full-space closure}
}.
]

## N18 - tested operator closure is insufficient

Across all 16 tested families:

- no family passes both the map gate (d_{m map}le0.05) and the full Jacobian gate (d_Jle0.10),
- the global winner therefore remains BASE_ONLY,
- fixed-point search remains blocked.

The final status is

[
oxed{
	ext{BLOCKED\_NONAUTONOMOUS\_OPERATOR\_CLOSURE}
}.
]

## N19 - action-space improvement is not an autonomy guarantee

The sextic operator substantially lowers the action-space RMS:

BASE_ONLY:
- N=8 RMS: 0.11686080486542735,
- N=4 RMS: 0.06216227448658173.

BASE + m6:
- N=8 RMS: 0.09910309438220476,
- N=4 RMS: 0.034936829179318056.

However its map discrepancy rises to

[
0.12213201088139856,
]

and therefore fails the 0.05 map gate.

Thus

[
oxed{
	ext{better effective-action fit}

otRightarrow
	ext{better autonomous RG map}
}.
]

## N20 - dominant cross-size mismatch is kappa-driven mixing

For the base map, the largest Jacobian gaps are:

1. output (m^2) vs input (kappa):
   [
   |0.5621801007228765-0.8720400238026129|
   =
   0.3098599230797364;
   ]

2. output (lambda) vs input (kappa):
   [
   |-0.680914954426772-(-0.9279557722173123)|
   =
   0.24704081779054032.
   ]

All remaining tested base entries are far smaller.

Therefore the next residual is not a generic “add more powers” problem. It is specifically concentrated in the response of mass/quartic coordinates to perturbations of the kinetic coupling.

## Scientific boundary

R17 verifies a finite exhaustive operator-family court at one declared reference point.

It does **not** establish:

- continuum RG autonomy,
- a continuum fixed point,
- universal critical exponents,
- beta functions,
- empirical particle physics,
- uniqueness of the best future operator basis.

## Next frontier

The R17 residual suggests a directed R18 generator:

[
Delta J_{kappa	o(m^2,lambda)}
ightarrow
	ext{kinetic-mixing operator generator}.
]

Instead of adding generic powers, R18 should generate homogeneous Z2-compatible operators that explicitly couple local gradients and amplitudes, for example structures of the form

[
phi^2(Deltaphi)^2,
]

[
(Deltaphi)^2(phi_i^2+phi_{i+1}^2),
]

[
(Deltaphi)^2phi_iphi_{i+1},
]

and compete them by the same map/Jacobian gates.

Version: **R1**
Date: **2026-10-04**
