# Ω Quotient / Coarse-Graining Results R1

Status: **FORMAL TOY-MODEL RESULTS — NOT EMPIRICAL PHYSICS**

## 1. Goal

R7 established that a quotient of process/path space is only compositionally valid when the equivalence relation is compatible with composition.

R8 formalizes that statement and connects it to structure-preserving coarse-graining.

Let P be a compositional process system with partial composition o.

Let ~ be an equivalence relation on processes.

We want to define quotient composition by:

[q] o [p] := [q o p].

The central question is:

When is this well-defined independently of representative choice?

## T10 — composition congruence is sufficient

Assume that whenever p~p' and q~q', and both compositions are defined,

q o p ~ q' o p'.

Then quotient composition is representative-independent.

Proof:

Choose any representatives p,p' of [p] and q,q' of [q].

By the congruence assumption:

q o p ~ q' o p'.

Therefore both representative choices yield the same quotient class.

Hence quotient composition is well-defined.

## T11 — representative-independent quotient composition implies compatibility

Assume quotient composition is well-defined for all quotient classes.

Take p~p' and q~q' with both q o p and q' o p' defined.

Since [p]=[p'] and [q]=[q']:

[q] o [p] = [q'] o [p'].

Well-definedness therefore implies:

[q o p] = [q' o p'],

hence:

q o p ~ q' o p'.

Thus compatibility is necessary.

## Corollary

For the process systems considered here:

composition on equivalence classes is well-defined
iff
the equivalence is a composition congruence.

This gives an exact gate rather than a heuristic.

## T12 — quotient projection is a homomorphism

Let pi:P->P/~ map each process to its equivalence class.

If ~ is a composition congruence, then whenever q o p is defined:

pi(q o p) = pi(q) o pi(p).

Thus quotienting preserves composition through the projection map.

This is the structural form of coarse-graining that R8 accepts.

## N6 — arbitrary coarse-graining can destroy process structure

If an equivalence relation is not a composition congruence, quotient composition is not representative-independent.

Therefore arbitrary aggregation of processes can destroy the compositional law.

So:

coarse-graining != arbitrary grouping.

A structure-preserving coarse-graining must preserve the operations needed by the effective theory.

## 2. Valid witness

Take integers modulo parity under addition.

Processes are integers.
Composition is addition.

Define:

a ~ b iff a and b have the same parity.

Then:

a~a' and b~b'
implies
a+b ~ a'+b'.

Therefore parity equivalence is a congruence and quotient composition is addition modulo 2.

This is a valid toy coarse-graining.

## 3. Invalid witness

Take process labels a,a',b,c,d with:

a~a'

but:

b o a = c
b o a' = d

and c is not equivalent to d.

Then the quotient product [b] o [a] depends on whether a or a' is chosen.

This is invalid coarse-graining.

## 4. Effective-theory interpretation

R8 suggests a precise candidate notion:

An effective process theory is a quotient of a finer process theory only when the chosen identification is a congruence for every operation the effective theory intends to preserve.

For multiple operations O_i, the stronger requirement is:

x~x' and y~y'
=> O_i(x,y) ~ O_i(x',y')

for each preserved operation.

This opens a route to multi-operation coarse-graining.

## Next frontier

1. Generalize from one operation to many.
2. Add weighted processes: cost, action, amplitude, probability.
3. Determine which observables descend to the quotient.
4. Define residual information lost by quotienting.
5. Connect quotient compatibility with RG/effective-theory maps.

Version: **R1**
Date: **2026-10-03**
