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
prec_{	ext{information}}
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
- loses process identity and composition information.

Status:
- **FORMALIZED**.

### CompositionalProcess

Strength:
- preserves process identity and composition outcomes not recoverable from induced edge existence alone.

Established result:
- two process systems can have the same states, processes, endpoints, and induced relation while having different composition laws.

Risk:
- may still assume composition rather than derive it from weaker structure.

Status:
- **FORMALIZED / STRICTLY RICHER THAN RELATION PROJECTION FOR COMPOSITION INFORMATION**.

### Next candidate

**SequentialRewriteProcess**

Question:
- can part of composition be derived from weaker sequential/rewrite constraints rather than assumed as a primitive law?

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
