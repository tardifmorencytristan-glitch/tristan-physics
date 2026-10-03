# Ω Compositional Process Results R1

Status: **FORMAL TOY-MODEL RESULTS — NOT EMPIRICAL PHYSICS**

Let a compositional process system be P=(S,H,s,t,compose), where S is a state set, H is a process set, s,t:H->S are source/target maps, and compose is a partial process-composition law.

The induced existence relation is xRy iff some h in H has source x and target y.

## T5 — equal induced relations do not determine composition

Witness:

S={A,B,C}

H={f,g,h,k}

f:A->B
g:B->C
h:A->C
k:A->C

System P1 has compose(g,f)=h.

System P2 has compose(g,f)=k.

Both induce the same directed relation:

R={(A,B),(B,C),(A,C)}

but their composition laws differ.

Therefore the induced relation does not determine composition.

## T6 — no universal reconstruction from relation alone

Assume a universal map F reconstructs every unrestricted process composition law from its induced relation.

For P1 and P2 above, the induced relations are equal, so F must return the same composition law for both.

But correctness would require F(R)=compose1 and F(R)=compose2 while compose1 != compose2.

Contradiction.

Therefore no universal reconstruction of unrestricted composition laws exists from induced relation alone.

## N4 — relation-only representations lose composition information

Any representation depending only on edge existence assigns the same relation-level description to P1 and P2, so it cannot distinguish their different composition outcomes.

Thus the relation projection is non-injective for this class of compositional process systems.

This proves an information-content separation:

DirectedRelation < CompositionalProcess

for the represented structure considered here.

This does not establish that composition is physically fundamental.

## Next target

Test whether composition can be derived from weaker sequential or rewrite constraints rather than assumed.

Version: R1
Date: 2026-10-03
