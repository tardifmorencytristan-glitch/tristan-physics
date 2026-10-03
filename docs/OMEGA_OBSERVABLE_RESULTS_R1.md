# Ω Observable Preservation Results R1

Status: **FORMAL TOY-MODEL RESULTS — NOT EMPIRICAL PHYSICS**

## Goal

Extend quotient/coarse-graining theory from preserved operations to preserved observables and approximate descent.

Let q:X->X/~ be the quotient map and let f:X->R be a real-valued observable.

Define the within-class oscillation:

epsilon_f := sup{|f(x)-f(y)| : x~y}.

## T16 — exact observable descent iff class constancy

There exists a well-defined observable f_bar on X/~ satisfying

f = f_bar o q

if and only if f is constant on every equivalence class.

### Sufficiency
If f is constant on each class, define f_bar([x])=f(x). Representative choice does not matter.

### Necessity
If f=f_bar o q and x~y, then q(x)=q(y), so f(x)=f_bar(q(x))=f_bar(q(y))=f(y).

Therefore exact quotient observables are exactly the class-constant observables.

## T17 — epsilon oscillation gives epsilon representative error

Assume epsilon_f is finite.

Choose any section s:X/~ -> X with s([x]) in [x], and define:

f_bar_s([x]) := f(s([x])).

Then for every x:

|f(x)-f_bar_s([x])| <= epsilon_f.

Therefore bounded within-class oscillation gives a direct effective-observable error bound.

## T18 — midpoint observable gives epsilon/2 for real-valued observables

For each class C, let:

m_C := (min_{x in C} f(x) + max_{x in C} f(x))/2

when extrema exist.

Define f_bar_mid(C)=m_C.

Then for every x in C:

|f(x)-m_C| <= (max_C f - min_C f)/2 <= epsilon_f/2.

So midpoint coarse-graining improves the worst-case classwise error bound from epsilon_f to epsilon_f/2.

## N8 — operation preservation does not imply observable preservation

A quotient may preserve all selected algebraic operations while an observable varies within quotient classes.

Thus:

operation congruence != observable descent.

Observable preservation must be checked separately.

## Three-PC witness on Z4 parity classes

Use classes:

{0,2}, {1,3}.

Observable 1:
f_parity(x)=x mod 2.

Its within-class oscillation is 0, so it descends exactly.

Observable 2:
f_norm(x)=x/3.

Its within-class oscillation is 2/3.

Class midpoints are:
- {0,2}: 1/3
- {1,3}: 2/3

The maximum midpoint reconstruction error is 1/3 = (2/3)/2.

These values were independently generated/checked across the three user PCs and read back from disk before repository integration.

## Effective-theory interpretation

A quotient-based effective theory should declare separately:

1. exact operations preserved,
2. exact observables preserved,
3. approximate observables preserved,
4. per-observable residual/error bounds.

This turns “coarse-graining loses information” into a measurable statement.

## Next frontier

1. vector-valued observables,
2. metric-valued observables,
3. approximate operation congruence,
4. propagated error bounds under repeated operations,
5. residual accumulation across multi-stage coarse-graining.

Version: **R1**
Date: **2026-10-03**
