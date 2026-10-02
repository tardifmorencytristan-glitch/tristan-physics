# Ω Falsification & Ablation Protocol R1

Status: **METHOD SPECIFICATION**

## 1. Claim classes

Every claim must be classified as one of:

- AXIOM
- DEFINITION
- LEMMA
- THEOREM
- CONJECTURE
- NO_GO
- PREDICTION

## 2. Falsification paths

### Logical falsification
Find an explicit contradiction from the claim set.

### Countermodel falsification
Construct a model satisfying declared dependencies while violating the target claim.

### Limit falsification
Show failure to recover a required known limit.

### Empirical falsification
Observe a declared falsifier under controlled conditions.

### Representation falsification
Show that a supposedly physical claim changes under a transformation declared to be purely representational.

## 3. Axiom ablation

For each axiom (a_i):

1. remove (a_i),
2. recompute reachable definitions and claims,
3. search for new countermodels,
4. compare empirical/structural coverage,
5. classify (a_i) as:
   - REQUIRED,
   - REDUNDANT,
   - DOMAIN_SPECIFIC,
   - UNRESOLVED.

## 4. Anti-smuggling audit

For every derived concept (C):

- expand its full dependency DAG,
- inspect every definition for synonyms or operational equivalents of (C),
- reject the derivation if (C) was assumed earlier.

## 5. Evidence rule

No claim may be promoted solely by eloquence, analogy, simulation output, or fit quality.

Promotion requires explicit evidence references appropriate to the status.

## 6. Failure is productive

Every failed claim should generate a failure artifact containing:

- target claim,
- failure type,
- smallest counterexample,
- affected dependencies,
- suggested mutation of the axiom/definition set,
- whether the failure generalizes.

This artifact becomes input to Ω-GRG regeneration.
