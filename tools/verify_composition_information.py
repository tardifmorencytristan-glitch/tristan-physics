#!/usr/bin/env python3
"""Verify the explicit Omega composition-information witness."""

PROCESSES = {
    "f": ("A", "B"),
    "g": ("B", "C"),
    "h": ("A", "C"),
    "k": ("A", "C"),
}

COMPOSITION_1 = {("g", "f"): "h"}
COMPOSITION_2 = {("g", "f"): "k"}


def induced_relation(processes):
    return {(source, target) for source, target in processes.values()}


def verify_witness():
    relation_1 = induced_relation(PROCESSES)
    relation_2 = induced_relation(PROCESSES)

    same_relation = relation_1 == relation_2
    distinct_composition = COMPOSITION_1 != COMPOSITION_2

    composability_ok = True
    for composition in (COMPOSITION_1, COMPOSITION_2):
        for (right, left), result in composition.items():
            left_source, left_target = PROCESSES[left]
            right_source, right_target = PROCESSES[right]
            result_source, result_target = PROCESSES[result]
            if left_target != right_source:
                composability_ok = False
            if result_source != left_source or result_target != right_target:
                composability_ok = False

    return {
        "ok": same_relation and distinct_composition and composability_ok,
        "same_relation": same_relation,
        "distinct_composition": distinct_composition,
        "composability_ok": composability_ok,
        "relation": sorted(relation_1),
    }


def main():
    result = verify_witness()
    if not result["ok"]:
        print("FAIL", result)
        raise SystemExit(1)

    print("PASS composition witness")
    print("relation:", result["relation"])
    print("Verified: induced relation does not determine composition.")


if __name__ == "__main__":
    main()
