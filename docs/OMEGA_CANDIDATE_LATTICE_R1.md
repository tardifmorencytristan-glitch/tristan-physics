# Ω Primitive Candidate Lattice R1

Status: **RESEARCH MAP**

This file tracks candidate primitives without assuming that "more abstract" means "better".

## Current lattice

[
UnaryAdmissibility
prec
TypedHistory
sim_{	ext{edge-existence}}
DirectedRelation
prec
CompositionalProcess
]

### UnaryAdmissibility

Strength:
- minimal.

Failure:
- cannot canonically orient symmetric admissible states.

Status:
- **BLOCKED for directed-dynamics compression**.

### TypedHistory

Strength:
- represents orientation.

Failure:
- source/target maps already carry direction.

Status:
- **FORMALIZED / REPRESENTATION EQUIVALENT to directed relations at edge-existence level**.

### DirectedRelation

Strength:
- explicit orientation.

Failure:
- no native path identity or composition semantics.

Status:
- **FORMALIZED**.

### CompositionalProcess

Strength:
- candidate to encode path identity and compositional structure.

Risk:
- may simply become category theory by assumption rather than derivation.

Status:
- **NEXT TARGET**.

## Court rule

A candidate primitive advances only if it demonstrates at least one of:

1. fewer independent assumptions,
2. stronger derivations,
3. measurable compression,
4. new no-go theorems,
5. better empirical constraints,
6. representation-independent explanatory gain.

Simple renaming does not count as progress.
