# Ω Constraint Compression Results R1

Status: **FORMAL TOY-MODEL RESULT — NOT EMPIRICAL PHYSICS**

## 1. Question

Can the three primitive candidates

- Distinction,
- Relation,
- Transformation

be reduced to one primitive:

[
Constraint / Admissibility
]

without reintroducing relation or transformation structure inside the definition of "constraint"?

## 2. Static admissibility model

Let (S) be a nonempty set of states and let

[
A:Sightarrow{0,1}
]

be a unary admissibility predicate.

The pair

[
(S,A)
]

is called a **static admissibility system**.

This structure distinguishes admissible states from inadmissible states, but contains no primitive binary relation, order, orientation, transition map, path structure, or endpoint map.

## 3. Symmetry lemma L1

Let (pi:Sightarrow S) be any permutation satisfying:

[
A(pi(s))=A(s)
]

for all (sin S).

Then (pi) is an automorphism of the static admissibility system.

Therefore any structure that is definable solely from ((S,A)) without additional labels must be invariant under all admissibility-preserving permutations.

## 4. No-Go N2 — unary static admissibility cannot define nontrivial directed reachability canonically

Suppose a directed relation

[
R_Asubseteq S	imes S
]

is claimed to be derivable canonically from ((S,A)) alone.

"Canonically" means every automorphism (pi) of ((S,A)) must preserve the relation:

[
xR_Ay
iff
pi(x)R_Api(y).
]

Assume there exist two distinct admissible states (x,y) with:

[
A(x)=A(y)=1.
]

Because the transposition exchanging (x) and (y) preserves (A), canonicity requires:

[
xR_Ay
iff
yR_Ax.
]

Thus the static unary predicate alone cannot canonically distinguish the direction (x	o y) from (y	o x).

More generally, within any orbit of the automorphism group of ((S,A)), a canonically derived relation cannot encode asymmetric orientation unless some additional structure breaks the symmetry.

Therefore:

[
oxed{
	ext{static unary admissibility alone cannot canonically generate nontrivial directed reachability}
}
]

on symmetric admissible states.

## 5. Interpretation

This blocks the naive compression:

[
{Distinction,Relation,Transformation}
Rightarrow
{Unary Constraint}
]

if "Constraint" means only a unary state-admissibility predicate.

The failure is productive: it tells us what information is missing.

At least one additional kind of structure is required, such as:

- ordered pairs,
- histories,
- endpoint maps,
- composition,
- orientation,
- temporal/causal labels,
- typed constraints.

But those additions must themselves be audited for hidden reintroduction of Relation or Transformation.

## 6. Candidate repair: typed admissibility system

A stronger candidate primitive is:

[
mathfrak C=(S,H,s,t,A_H)
]

where:

- (S): configurations,
- (H): candidate histories,
- (s,t:Hightarrow S): source and target maps,
- (A_H:Hightarrow{0,1}): history admissibility.

Then define:

[
xRy
iff
exists hin H:
A_H(h)=1, s(h)=x, t(h)=y.
]

This can generate a directed relation.

However, source/target maps already contain relational orientation. Therefore this is **not yet a proof of single-primitive compression**.

It is a candidate structured primitive requiring further regeneralization.

## 7. Consequence for Ω-GRG

The correct result is not:

> Constraint successfully replaces all three primitives.

The current result is:

[
oxed{
UnaryConstraint 	ext{fails the anti-smuggling/generalization test for directed dynamics.}
}
]

This creates a new search problem:

[
	ext{find the weakest structure richer than unary admissibility but poorer than explicit Relation + Transformation.}
]

## 8. Next candidates

Competing candidates should include:

1. typed constraints,
2. admissible histories,
3. compositional processes,
4. directed hyperedges,
5. category-like primitive arrows,
6. rewrite rules,
7. constraint satisfaction over path objects.

No candidate receives preference without proving a genuine compression.

---

Version: **R1**
Date: **2026-10-02**
