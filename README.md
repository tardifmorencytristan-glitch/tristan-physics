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
- [Ω Observable Preservation Results R1](docs/OMEGA_OBSERVABLE_RESULTS_R1.md)
- [Ω Effective-Theory Error Budget Results R1](docs/OMEGA_EFFECTIVE_ERROR_RESULTS_R1.md)
- [Ω Lattice Phi4 Bridge Results R1](docs/OMEGA_LATTICE_PHI4_RESULTS_R1.md)
- [Ω Effective-Action Discovery Results R1](docs/OMEGA_EFFECTIVE_ACTION_DISCOVERY_R1.md)
- [Ω Multiscale RG Flow Results R1](docs/OMEGA_MULTISCALE_RG_FLOW_R1.md)
- [Ω Coupling-Flow Geometry Results R1](docs/OMEGA_COUPLING_FLOW_GEOMETRY_R1.md)
- [Ω Autonomous Rescaled RG Results R1](docs/OMEGA_AUTONOMOUS_RESCALED_RG_R1.md)
- [Ω Operator-Closure Court Results R1](docs/OMEGA_OPERATOR_CLOSURE_COURT_R1.md)
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
- [Omega observable preservation model R1](research/omega_observable_model_r1.json)
- [Omega R10 three-PC evidence](research/omega_r10_pc_evidence.json)
- [Omega effective error-budget model R1](research/omega_effective_error_model_r1.json)
- [Omega R11 three-PC evidence](research/omega_r11_pc_evidence.json)
- [Omega lattice phi4 model R1](research/omega_lattice_phi4_model_r1.json)
- [Omega R12 three-PC evidence](research/omega_r12_pc_evidence.json)
- [Omega effective-action discovery model R1](research/omega_effective_action_model_r1.json)
- [Omega R13 three-PC evidence](research/omega_r13_pc_evidence.json)
- [Omega multiscale RG model R1](research/omega_multiscale_rg_model_r1.json)
- [Omega R14 three-PC evidence](research/omega_r14_pc_evidence.json)
- [Omega coupling-flow model R1](research/omega_coupling_flow_model_r1.json)
- [Omega R15 three-PC evidence](research/omega_r15_pc_evidence.json)
- [Omega autonomous rescaled RG model R1](research/omega_autonomous_rg_model_r1.json)
- [Omega R16 three-PC evidence](research/omega_r16_pc_evidence.json)
- [Omega operator-closure model R1](research/omega_operator_closure_model_r1.json)
- [Omega R17 three-PC evidence](research/omega_r17_pc_evidence.json)

## Verification tools

- `tools/verify_reachability_order.py`
- `tools/verify_dependency_dag.py`
- `tools/verify_history_relation_equivalence.py`
- `tools/verify_composition_information.py`
- `tools/verify_free_path_category.py`
- `tools/verify_quotient_congruence.py`
- `tools/verify_multioperation_congruence.py`
- `tools/verify_observable_preservation.py`
- `tools/verify_effective_error_budget.py`
- `tools/verify_lattice_phi4_bridge.py`
- `tools/verify_effective_action_discovery.py`
- `tools/verify_multiscale_rg_flow.py`
- `tools/verify_coupling_flow_geometry.py`
- `tools/verify_autonomous_rescaled_rg.py`
- `tools/verify_operator_closure_court.py`
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
- preserving one operation does not imply preserving another,
- exact observable descent requires class constancy,
- bounded within-class oscillation yields explicit approximation error bounds,
- operation preservation does not imply arbitrary observable preservation,
- multi-stage observable residuals are bounded by the sum of declared stage residuals,
- Lipschitz sensitivities propagate and can amplify upstream approximation error,
- small local residuals alone do not guarantee small final residuals under repeated sensitive dynamics,
- two-site block averaging has an exact second-moment loss equal to unresolved within-block variance,
- the lattice phi4 action and the block map respect global Z2 symmetry,
- odd observables cancel in the exact finite Z2-symmetric ensemble,
- periodic phi4 action density decomposes exactly into M2, M4, and nearest-neighbor correlation,
- the blocked field alone cannot reconstruct the microscopic action in general,
- the exact blocked Boltzmann measure preserves total weight and Z2 symmetry,
- an exact finite effective action S_eff=-log W reproduces the blocked measure on its support,
- nested effective-operator spaces cannot worsen the optimal action-space least-squares residual,
- the simple constant+M2+C1+M4 coarse ansatz is not exact on the R13 finite support,
- operator rankings can differ between action-space residual and probability-space KL objectives,
- exact rational block maps compose across the finite 8->4->2->1 flow,
- finite push-forward preserves partition weight across every tested scale,
- exact support-level effective actions inherit Z2 symmetry at every tested scale,
- the restricted retained operator family is not exactly closed under the tested multiscale flow,
- operator identifiability and ranking can change with scale as well as objective,
- ternary scalar fields alias phi^4 with phi^2 and make microscopic mass/quartic directions non-identifiable,
- central finite-difference projected-RG Jacobians are stable under the tested step refinement,
- after one block step the enriched alphabet restores a locally identifiable 3D projected coupling geometry,
- recursive retained-basis projection does not commute with exact multistep push-forward,
- fixed-point language requires an explicit autonomous field-rescaling convention before it is admissible,
- explicit field-rescaling gauges can reduce cross-size projected-map discrepancy on a common reference alphabet,
- Boltzmann second-moment matching is the best tested R16 map-level normalization at the declared reference point,
- map-level cross-size agreement does not imply Jacobian-level autonomy,
- the R16 fixed-point gate remains blocked because the winning normalization fails the declared Jacobian-autonomy threshold,
- a complete 16-family R17 court over m2_sq, m2_c1, delta4, and m6 contains no autonomy-passing family under unchanged R16 thresholds,
- delta4 improves the original physical 3x3 Jacobian sub-block while worsening the full expanded-space Jacobian,
- lower effective-action fit residual does not guarantee a more autonomous projected RG map,
- the dominant remaining cross-size Jacobian mismatch is concentrated in kappa-driven mixing into mass2 and lambda.

These are mathematical results about abstract toy structures. They are **not empirical validation of a fundamental physical theory**.

## Status discipline

Generated != Formalized != Proved != Measured != Replicated
