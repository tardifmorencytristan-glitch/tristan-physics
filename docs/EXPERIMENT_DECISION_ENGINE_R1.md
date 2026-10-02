# Ω Experiment Decision Engine R1

Status: **RESEARCH DESIGN SPECIFICATION**

## Objective

Given competing theories (Theta_1,ldots,Theta_n), search for an intervention or observation (x) that maximizes their distinguishability.

Candidate objective:

[
x^star = argmax_x D(P_{Theta_i}(x),P_{Theta_j}(x))
]

or, probabilistically:

[
x^star = argmax_x EIG(x)
]

where (EIG) is expected information gain.

## Decision artifact

Every proposed experiment should include:

- competing claims/theories,
- controllable variables,
- predicted observables,
- uncertainty model,
- safety/feasibility constraints,
- expected separation,
- null result interpretation,
- update rule after observation.

## Unknown-unknown mode

Priority regions may be selected where:

[
Var_{Theta in mathfrak T}(P_Theta(x))
]

is large.

This does not prove new physics; it identifies regions where current candidates disagree most strongly.

## Gate

No experiment is considered discriminating unless at least two candidate theories produce meaningfully different predictions under the declared uncertainty model.
