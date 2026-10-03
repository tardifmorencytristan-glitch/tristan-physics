#!/usr/bin/env python3
"""Verify R11 multi-stage effective-theory error budgets."""

from math import prod


def additive_budget(epsilons):
    if any(e < 0 for e in epsilons):
        raise ValueError("residual bounds must be nonnegative")
    return sum(epsilons)


def recurrence_bound(initial_error, lipschitz, local_errors):
    if len(lipschitz) != len(local_errors):
        raise ValueError("lipschitz and local_errors must have equal length")
    if initial_error < 0 or any(L < 0 for L in lipschitz) or any(d < 0 for d in local_errors):
        raise ValueError("all bounds must be nonnegative")

    inherited = initial_error * prod(lipschitz)
    injected = 0.0
    for i, delta in enumerate(local_errors):
        injected += delta * prod(lipschitz[i + 1 :])
    return inherited + injected


def recurrence_iterate(initial_error, lipschitz, local_errors):
    e = initial_error
    for L, delta in zip(lipschitz, local_errors):
        e = L * e + delta
    return e


def verify():
    eps = [0.125, 0.25, 0.375]
    additive = additive_budget(eps)

    L = [2.0, 0.5, 3.0]
    delta = [0.1, 0.2, 0.05]
    initial = 0.125
    closed = recurrence_bound(initial, L, delta)
    iterative = recurrence_iterate(initial, L, delta)

    amp_initial = 1.0 / 16.0
    amp = recurrence_iterate(amp_initial, [2.0] * 4, [0.0] * 4)

    return {
        "additive_budget": additive,
        "zero_budget": additive_budget([0.0, 0.0, 0.0]),
        "recurrence_closed_form": closed,
        "recurrence_iterative": iterative,
        "recurrence_match": abs(closed - iterative) <= 1e-12,
        "amplification_initial": amp_initial,
        "amplification_final": amp,
        "amplification_factor": amp / amp_initial,
    }


def main():
    result = verify()
    if abs(result["additive_budget"] - 0.75) > 1e-12:
        raise SystemExit("FAIL additive budget")
    if result["zero_budget"] != 0:
        raise SystemExit("FAIL exact zero closure")
    if not result["recurrence_match"]:
        raise SystemExit("FAIL recurrence formula")
    if abs(result["amplification_final"] - 1.0) > 1e-12:
        raise SystemExit("FAIL amplification witness")
    print("PASS effective error budget verifier")
    print(result)


if __name__ == "__main__":
    main()
