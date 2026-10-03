# Ω Free-Path Composition Results R1

Status: **FORMAL TOY-MODEL RESULTS — NOT EMPIRICAL PHYSICS**

## 1. Goal

Start with a directed graph G=(V,E). A finite path is a composable finite sequence of directed edges. For every vertex v, include an empty path epsilon_v.

Define path composition by sequence concatenation whenever endpoints match.

The orientation is still supplied by the directed graph. The narrower question here is whether composition laws, associativity, and identities can be generated from path syntax instead of being supplied as an independent composition table.

## T7 — path concatenation is associative

For composable finite paths p, q, r:

(r o q) o p = r o (q o p).

This follows from associativity of finite sequence concatenation.

Therefore associativity is derived inside the free-path construction rather than added as an independent lookup-table axiom.

## T8 — empty paths are identities

For every path p:x->y:

p o epsilon_x = p

and:

epsilon_y o p = p.

Thus the zero-length path at each vertex acts as the identity process.

## T9 — every directed graph generates a compositional process system

For any directed graph G=(V,E), let Path(G) be all finite directed paths.

Using:
- vertices as states,
- finite paths as processes,
- concatenation as partial composition,
- empty paths as identities,

the resulting structure has typed composition, associativity, and identities.

Research consequence:

DirectedRelation + FinitePathConstruction
=> AssociativeComposition + Identities.

This does not mean every arbitrary hidden composition law is recoverable from a relation. R6 already proved that it is not.

## C7.1 — canonical free composition versus arbitrary composition

R6:
- arbitrary composition is not reconstructible from relation alone.

R7:
- a distinguished free composition can be generated canonically from a directed graph by finite paths.

So the correct distinction is:

1. recovering an arbitrary hidden composition law;
2. generating one canonical free composition law.

Only the second is achieved here.

## N5 — arbitrary path identification can destroy well-defined composition

Suppose paths are identified by an equivalence relation approx and one tries to define:

[q] o [p] = [q o p].

This is well-defined only if equivalence is compatible with composition:

p approx p' and q approx q'
implies
q o p approx q' o p'.

If this compatibility fails, representative choice changes the result.

Therefore quotienting paths requires a composition congruence.

## Counterexample

Take processes a, a', b, c, d with:

a approx a'

but:

b o a = c

and:

b o a' = d

while c is not equivalent to d.

Then [a]=[a'] but [b] o [a] is representative-dependent.

So quotient composition is not well-defined.

## Updated hierarchy

UnaryAdmissibility
< TypedHistory
~ DirectedRelation at edge-existence level
< ArbitraryCompositionalProcess in information content.

A separate constructive branch is:

DirectedRelation
-> finite-path construction
-> FreeCompositionalProcess.

## Next frontier

1. Determine which path equivalences are composition congruences.
2. Test coarse-graining as quotient-by-congruence.
3. Add costs, amplitudes, probabilities, or actions while preserving composition.
4. Define observables on process equivalence classes.
5. Test whether physical effective theories can be represented as structure-preserving quotients.

Version: **R1**
Date: **2026-10-03**
