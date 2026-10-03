# tristan-physics

Public-safe physics models, detectors, circuits, electromagnetic research, and reproducible demonstrations.

## Research programs

- [Ω-APT / Ω-GRG R1 — Axiomatic & Regeneralization Physics](docs/OMEGA_APT_GRG_R1.md)
- [Ω-APT / Ω-GRG R2 MAX — proof/falsification architecture](docs/OMEGA_APT_GRG_R2_MAX.md)
- [Ω Formal Results R1](docs/OMEGA_FORMAL_RESULTS_R1.md)
- [Ω Constraint Compression Results R1](docs/OMEGA_CONSTRAINT_RESULTS_R1.md)
- [Ω Typed-History Results R1](docs/OMEGA_HISTORY_RESULTS_R1.md)
- [Ω Compositional Process Results R1](docs/OMEGA_COMPOSITION_RESULTS_R1.md)
- [Ω Free-Path Composition Results R1](docs/OMEGA_FREE_PATH_RESULTS_R1.md)
- [Ω Quotient / Coarse-Graining Results R1](docs/OMEGA_QUOTIENT_RESULTS_R1.md)
- [Ω Multi-Operation Congruence Results R1](docs/OMEGA_MULTIOPERATION_RESULTS_R1.md)
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
- [Omega free-path model R1](research/omega_free_path_model_r1.json)
- [Omega quotient congruence model R1](research/omega_quotient_model_r1.json)
- [Omega multi-operation model R1](research/omega_multioperation_model_r1.json)
- [Omega R9 three-PC evidence](research/omega_r9_pc_evidence.json)

## Verification tools

- `tools/verify_reachability_order.py`
- `tools/verify_dependency_dag.py`
- `tools/verify_history_relation_equivalence.py`
- `tools/verify_composition_information.py`
- `tools/verify_free_path_category.py`
- `tools/verify_quotient_congruence.py`
- `tools/verify_multioperation_congruence.py`
- `.github/workflows/omega-formal-gates.yml`

## Current formal boundary

Proved toy-model results currently include:

- strict partial order from the mutual-reachability quotient,
- finite order-preserving integer rankings,
- no strict cycles in that quotient,
- Distinction is unnecessary for T1,
- unary admissibility alone cannot canonically orient symmetric admissible states,
- typed histories and directed relations are equivalent at one-step existence level,
- arbitrary process composition is not reconstructible from relation projection alone,
- finite directed paths generate a canonical associative composition,
- zero-length paths generate identities,
- arbitrary path quotients require composition-compatible congruence,
- composition congruence is necessary and sufficient for representative-independent quotient composition,
- quotient projection preserves composition,
- arbitrary non-congruence coarse-graining can destroy process structure,
- a preserved operation family descends iff the equivalence is a congruence for every operation in that signature,
- preserving one operation does not imply preserving another.

These are mathematical results about abstract toy structures. They are **not empirical validation of a fundamental physical theory**.

## Status discipline

Generated != Formalized != Proved != Measured != Replicated
