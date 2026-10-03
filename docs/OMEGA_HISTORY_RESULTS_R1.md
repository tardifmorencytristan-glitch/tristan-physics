# Ω Typed-History Results R1

Status: **FORMAL TOY-MODEL RESULTS — NOT EMPIRICAL PHYSICS**

## 1. Question

After the unary-constraint obstruction, the next candidate primitive is a typed admissibility system:

[
mathfrak H=(S,H,s,t,A_H)
]

with:

- (S): states,
- (H): candidate histories,
- (s,t:Hightarrow S): source and target maps,
- (A_H:Hightarrow{0,1}): admissibility.

Define the induced directed relation:

[
xR_{mathfrak H}y
iff
exists hin H:
A_H(h)=1, s(h)=x, t(h)=y.
]

The key question is whether this is a genuine compression of directed relation structure.

---

## Theorem T3 — every typed-history system induces a directed relation

For every typed-history system (mathfrak H), the construction above defines:

[
R_{mathfrak H}subseteq S	imes S.
]

This is immediate from the source and target maps.

Therefore typed histories are sufficient to represent directed reachability at the one-step level.

---

## Theorem T4 — every directed relation has a canonical history encoding

Let:

[
Rsubseteq S	imes S
]

be any directed relation.

Construct:

[
H_R=R.
]

For each history (h=(x,y)in H_R), define:

[
s(h)=x,
qquad
t(h)=y,
qquad
A_H(h)=1.
]

Then the relation induced from the history system is exactly:

[
R_{mathfrak H_R}=R.
]

### Proof

For (x,yin S),

[
xR_{mathfrak H_R}y
]

iff there exists (hin H_R) with (s(h)=x) and (t(h)=y).

Since (H_R=R), this is equivalent to:

[
(x,y)in R.
]

Therefore:

[
oxed{R_{mathfrak H_R}=R.}
]

---

## Corollary C4.1 — typed histories do not automatically compress directed relation structure

At the level of one-step existence information, directed relations and their canonical typed-history encodings are interconvertible:

[
R
ightarrow
mathfrak H_R
ightarrow
R.
]

Therefore merely replacing "Relation" by "History + source + target" is not, by itself, evidence of deeper primitive compression.

It may still be useful as a representation change.

But a genuine compression claim requires additional evidence, such as:

- fewer independent assumptions,
- derivation of source/target orientation from weaker structure,
- stronger predictive constraints,
- simpler generating rules,
- compression across multiple relations,
- nontrivial compositional consequences.

---

## No-Go N3 — renaming relation as typed history does not satisfy the anti-smuggling goal

If (s) and (t) are primitive independent maps, orientation has already been supplied.

Thus the candidate:

[
	ext{Constraint}
ightarrow
	ext{TypedHistory}
]

does not solve the original compression problem if the directionality of (s,t) is assumed rather than derived.

Formally:

[
oxed{
	ext{primitive source/target orientation reintroduces directed relational structure}
}
]

at the representation layer.

This is an anti-smuggling result, not a claim that history-based formalisms are useless.

---

## 5. Composition changes the question

Suppose histories also admit a partial composition:

[
circ:H	imes Hightharpoonup H
]

when:

[
t(h_1)=s(h_2).
]

Then a history system can contain more information than a bare binary relation.

Two systems can induce the same one-step relation while differing in:

- multiplicity of histories,
- internal labels,
- path identity,
- composition laws,
- costs,
- amplitudes,
- constraints.

Therefore the next search target is not:

> Can histories encode relations?

That question is solved.

The stronger question is:

[
oxed{
	ext{Can composition be generated from weaker admissibility structure without assuming directional endpoints?}
}
]

---

## 6. Candidate frontier

The current candidate lattice becomes:

[
UnaryAdmissibility
prec
TypedHistory
sim_{	ext{one-step existence}}
DirectedRelation
prec
CompositionalProcess.
]

The symbol (sim) here means representational equivalence only for one-step existence information.

It does **not** mean complete mathematical equivalence of all enriched history systems and binary relations.

---

## 7. Next formal targets

1. Define a minimal compositional process object.
2. Separate:
   - state identity,
   - orientation,
   - composability,
   - associativity,
   - identity processes.
3. Test whether category-like structure is minimal or excessive.
4. Construct countermodels with same induced relation but different composition.
5. Measure what composition adds that relation alone cannot recover.

---

Version: **R1**
Date: **2026-10-03**
