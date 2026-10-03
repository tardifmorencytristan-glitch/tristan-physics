# tristan-physics

Public-safe physics models, detectors, circuits, electromagnetic research, and reproducible demonstrations.

## Research programs

- [Ω-APT / Ω-GRG R1 — Axiomatic & Regeneralization Physics](docs/OMEGA_APT_GRG_R1.md)
- [Ω-APT / Ω-GRG R2 MAX — proof/falsification architecture](docs/OMEGA_APT_GRG_R2_MAX.md)
- [Ω Formal Results R1](docs/OMEGA_FORMAL_RESULTS_R1.md)
- [Ω Constraint Compression Results R1](docs/OMEGA_CONSTRAINT_RESULTS_R1.md)
- [Ω Typed-History Results R1](docs/OMEGA_HISTORY_RESULTS_R1.md)
- [Ω Compositional Process Results R1](docs/OMEGA_COMPOSITION_RESULTS_R1.md)
- [Ω Primitive Candidate Lattice R1](docs/OMEGA_CANDIDATE_LATTICE_R1.md)
- [Ω Falsification & Ablation Protocol R1](docs/FALSIFICATION_PROTOCOL_R1.md)
- [Ω Experiment Decision Engine R1](docs/EXPERIMENT_DECISION_ENGINE_R1.md)

## Machine-readable research artifacts

- [Omega theory JSON Schema R1](schemas/omega_theory_r1.schema.json)
- [Omega toy model R1](research/omega_toy_model_r1.json)
- [Omega toy model R2](research/omega_toy_model_r2.json)
- [Omega constraint-compression model R1](research/omega_constraint_model_r1.json)
- [Omega typed-history model R1](research/omega_history_model_r1.json)
- [Omega compositional-process model R1](research/omega_composition_model_r1.json)

## Verification tools

- `tools/verify_reachability_order.py`
- `tools/verify_dependency_dag.py`
- `tools/verify_history_relation_equivalence.py`
- `tools/verify_composition_information.py`
- `.github/workflows/omega-formal-gates.yml`

## Current formal boundary

Proved toy-model results currently include:

- strict partial order from the mutual-reachability quotient,
- finite order-preserving integer rankings,
- no strict cycles in that quotient,
- Distinction is unnecessary for T1,
- unary admissibility alone cannot canonically orient symmetric admissible states,
- typed histories and directed relations are equivalent at one-step existence level,
- primitive source/target maps do not establish deeper primitive compression,
- induced relation does not determine process composition,
- unrestricted composition cannot in general be reconstructed from relation projection alone.

These are mathematical results about abstract toy structures. They are **not empirical validation of a fundamental physical theory**.

## Status discipline

[
\text{Generated} \neq \text{Formalized} \neq \text{Proved} \neq \text{Measured} \neq \text{Replicated}
]
