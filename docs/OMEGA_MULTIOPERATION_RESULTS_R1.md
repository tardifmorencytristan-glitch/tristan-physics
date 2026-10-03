# Ω Multi-Operation Congruence Results R1

Status: **FORMAL TOY-MODEL RESULTS — NOT EMPIRICAL PHYSICS**

## 1. Goal

R8 established the single-operation criterion:

A quotient operation is representative-independent if and only if the equivalence relation is a congruence for that operation.

R9 generalizes this from one operation to an entire preserved signature.

Let a process/algebraic system carry operations:

O_1, O_2, ..., O_n.

Let ~ be an equivalence relation on the carrier.

For each k-ary operation O_i, require:

x_j ~ x'_j for every input position j
implies
O_i(x_1,...,x_k) ~ O_i(x'_1,...,x'_k).

## T13 — familywise congruence is sufficient

If ~ is a congruence for every operation in the preserved signature, then every quotient operation

[O_i]( [x_1],...,[x_k] )
:=
[ O_i(x_1,...,x_k) ]

is independent of representative choice.

Therefore all operations descend simultaneously to the quotient.

## T14 — familywise congruence is necessary

Assume every operation in the preserved signature is well-defined on equivalence classes.

Then, for each O_i, equivalent inputs must yield equivalent outputs; otherwise the quotient value would depend on representative choice.

Therefore ~ must be a congruence for every preserved operation.

## Corollary

For a family of operations:

all quotient operations are well-defined
iff
~ is a congruence for each operation in the preserved signature.

This is the multi-operation extension of R8.

## T15 — quotient projection preserves the whole signature

Let pi map each element/process to its equivalence class.

If ~ is a congruence for every operation O_i, then:

pi(O_i(x_1,...,x_k))
=
[O_i](pi(x_1),...,pi(x_k))

for every preserved operation.

Thus pi is a homomorphism for the entire preserved signature.

## N7 — preserving one operation does not imply preserving another

An equivalence may be a congruence for one operation but fail for another.

Therefore a coarse-graining that preserves one law may destroy another.

So effective-theory validity must be indexed by the exact signature being preserved.

## 2. Three-PC computational witness on Z4

The user's three PCs independently evaluated congruence structure for the carrier Z4 with the two operations:

- addition modulo 4,
- multiplication modulo 4.

All 15 set partitions of Z4 were considered by the exhaustive generator/verifier pair.

The congruences preserving both operations were exactly:

1. {{0},{1},{2},{3}}
2. {{0,2},{1,3}}
3. {{0,1,2,3}}

A candidate partition {{0,1},{2,3}} was separately checked and fails to preserve both operations.

This result was produced on:

- DESKTOP-SHA9IHL — exhaustive generator,
- DESKTOP-2G1SSMT — targeted OAK formalization/checks,
- LAPTOP-AIU36QN6 — independent exhaustive verifier.

Read-back of the written JSON result artifacts was completed on all three machines before GitHub integration.

## 3. Important scope

These results establish a structural theorem and finite algebraic witnesses.

They do not establish:
- a new law of physics,
- that all physical coarse-graining is quotient-by-congruence,
- that the selected operations are physically privileged.

They provide a stronger mathematical gate for future effective-theory constructions.

## Next frontier

1. Add observables to the preserved signature.
2. Define observable-compatible quotient maps.
3. Quantify information lost by valid quotients.
4. Distinguish exact congruence from approximate congruence.
5. Connect approximate preservation to residuals and effective-theory error bounds.

Version: **R1**
Date: **2026-10-03**
