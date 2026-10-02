# Ω Formal Results R1

Status: **FORMAL MATHEMATICAL RESULTS FOR A TOY MODEL — NOT EMPIRICAL PHYSICS**

This document promotes two claims from the finite reachability toy model from conjectural status to mathematical results under explicit assumptions.

## 0. Formal setting

Let (G=(V,E)) be a directed graph.

Define (Rsubseteq V	imes V) as the reflexive-transitive closure of (E):

[
xRy
]

iff there exists a finite directed path from (x) to (y), including the length-zero path (xRx).

Therefore (R) is a preorder:

1. reflexive: (xRx),
2. transitive: (xRyland yRzRightarrow xRz).

Define mutual reachability:

[
xsim y iff xRyland yRx.
]

Let (Q=V/{sim}) be the set of equivalence classes.

Define strict precedence on (Q):

[
[x]prec[y]
iff
xRyland 
eg(yRx).
]

---

## Theorem T1 — Reachability quotient induces a strict partial order

**Claim.** (prec) is well-defined, irreflexive, and transitive on (Q).

### Well-definedness

Suppose:

[
xsim x',qquad ysim y'
]

and:

[
xRy,qquad 
eg(yRx).
]

From (x'Rx), (xRy), and (yRy'), transitivity gives:

[
x'Ry'.
]

Assume for contradiction that (y'Rx'). Since (yRy') and (x'Rx),

[
yRy'Rx'Rx,
]

so (yRx), contradicting (
eg(yRx)).

Therefore:

[
[x']prec[y'].
]

Hence the relation is independent of representatives.

### Irreflexivity

For any ([x]),

[
[x]prec[x]
]

would require both:

[
xRx
]

and:

[

eg(xRx),
]

which is impossible.

Therefore:

[

eg([x]prec[x]).
]

### Transitivity

Suppose:

[
[x]prec[y]
]

and:

[
[y]prec[z].
]

Then:

[
xRy,qquad yRz.
]

By transitivity:

[
xRz.
]

Assume (zRx). Since (xRy),

[
zRxRy,
]

hence (zRy), contradicting ([y]prec[z]), which requires (
eg(zRy)).

Therefore:

[

eg(zRx),
]

and thus:

[
[x]prec[z].
]

### Conclusion

[
oxed{(Q,prec)	ext{ is a strict partially ordered set.}}
]

This proves the finite-toy-model version of former claim **C1**; in fact finiteness is not needed for T1.

---

## Theorem T2 — Finite quotient admits an integer-valued time-like ranking

Assume (Q) is finite.

Since ((Q,prec)) is a finite strict partial order, its Hasse/precedence graph is acyclic.

Every finite directed acyclic graph admits a topological ordering:

[
q_0,q_1,ldots,q_{n-1}.
]

Define:

[
	au(q_i)=i.
]

Then:

[
q_iprec q_j Rightarrow 	au(q_i)<	au(q_j).
]

Therefore there exists an injective order-preserving map:

[
oxed{	au:Qightarrow{0,ldots,n-1}.}
]

This proves the finite version of former claim **C2**.

### Important limitation

(	au) is:

- not unique,
- not yet a physical clock,
- not a metric,
- not proper time,
- not evidence that physical time is fundamentally reachability.

It is only a mathematically valid order representation of the toy model.

---

## No-Go N1 — No strict causal cycle survives the quotient

There cannot exist classes:

[
q_0,q_1,ldots,q_k=q_0
]

such that:

[
q_0prec q_1preccdotsprec q_k.
]

If such a cycle existed, repeated transitivity would imply:

[
q_0prec q_0,
]

contradicting irreflexivity.

Therefore:

[
oxed{	ext{strict precedence cycles are forbidden in the reachability quotient.}}
]

This is a formal obstruction of the toy model.

---

## Independence witness I1 — Distinction is not required for T1

Consider a model with a single realization:

[
V={a}
]

and only its identity reachability:

[
aRa.
]

There are no two distinct realizations, so the Distinction axiom:

> there exist (x,y) with (x
otsim y)

is false.

Nevertheless:

- reachability is reflexive and transitive,
- the quotient (Q) contains one equivalence class,
- (prec) is empty,
- T1 holds.

Thus Distinction is not necessary for T1.

This does **not** prove that Distinction is globally redundant in Ω-APT; it establishes only that T1 does not depend on it.

---

## Computational verification

The repository includes an exhaustive finite checker:

`tools/verify_reachability_order.py`

and unit tests:

`tests/test_reachability_order.py`.

The checker is verification support, not the proof. The proof above establishes T1/T2 under the stated assumptions; finite enumeration tests implementation consistency on bounded graph sizes.

---

Version: **R1**
Date: **2026-10-02**
