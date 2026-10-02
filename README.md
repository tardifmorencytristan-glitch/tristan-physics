# tristan-physics

Public-safe physics models, detectors, circuits, electromagnetic research, and reproducible demonstrations.

## Research programs

- [Ω-APT / Ω-GRG R1 — Axiomatic & Regeneralization Physics](docs/OMEGA_APT_GRG_R1.md)
- [Ω-APT / Ω-GRG R2 MAX — proof/falsification architecture](docs/OMEGA_APT_GRG_R2_MAX.md)
- [Ω Formal Results R1 — first proved toy-model results](docs/OMEGA_FORMAL_RESULTS_R1.md)
- [Ω Falsification & Ablation Protocol R1](docs/FALSIFICATION_PROTOCOL_R1.md)
- [Ω Experiment Decision Engine R1](docs/EXPERIMENT_DECISION_ENGINE_R1.md)

## Machine-readable research artifacts

- [Omega theory JSON Schema R1](schemas/omega_theory_r1.schema.json)
- [Omega toy model R1](research/omega_toy_model_r1.json)
- [Omega toy model R2 — formalized claims](research/omega_toy_model_r2.json)

## Verification tools

- `tools/verify_reachability_order.py` — exhaustive finite-model checker
- `tests/test_reachability_order.py` — regression/unit tests
- `.github/workflows/omega-formal-gates.yml` — automated formal gates

## Status discipline

Generated research concepts are not treated as verified physics until they pass explicit proof, empirical, and read-back gates.

Core rule:

[
\text{Generated} \neq \text{Proved} \neq \text{Measured} \neq \text{Replicated}
]

The current proved results are mathematical results about a toy reachability model. They are **not** empirical validation of a fundamental physical theory.
