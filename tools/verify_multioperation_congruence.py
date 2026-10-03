#!/usr/bin/env python3
"""Exhaustive verifier for Z4 under addition and multiplication modulo 4."""

from __future__ import annotations

import itertools


def canonical_partition(labels):
    blocks = {}
    for i, label in enumerate(labels):
        blocks.setdefault(label, []).append(i)
    return tuple(sorted(tuple(v) for v in blocks.values()))


def all_partitions(n):
    seen = set()
    for labels in itertools.product(range(n), repeat=n):
        p = canonical_partition(labels)
        if p not in seen:
            seen.add(p)
            yield p


def class_map(partition):
    out = {}
    for i, block in enumerate(partition):
        for x in block:
            out[x] = i
    return out


def congruent(partition, operation, arity, n):
    c = class_map(partition)
    elements = range(n)
    tuples = list(itertools.product(elements, repeat=arity))

    for left in tuples:
        for right in tuples:
            if all(c[a] == c[b] for a, b in zip(left, right)):
                if c[operation(*left)] != c[operation(*right)]:
                    return False
    return True


def verify_z4():
    n = 4
    add = lambda a, b: (a + b) % 4
    mul = lambda a, b: (a * b) % 4

    partitions = list(all_partitions(n))
    good = []

    for partition in partitions:
        if congruent(partition, add, 2, n) and congruent(partition, mul, 2, n):
            good.append(partition)

    expected = {
        ((0,), (1,), (2,), (3,)),
        ((0, 2), (1, 3)),
        ((0, 1, 2, 3),),
    }

    return {
        "partition_count": len(partitions),
        "good": set(good),
        "expected": expected,
        "matches_expected": set(good) == expected,
    }


def main():
    result = verify_z4()

    if result["partition_count"] != 15:
        print("FAIL partition count", result["partition_count"])
        raise SystemExit(1)

    if not result["matches_expected"]:
        print("FAIL congruence set", result)
        raise SystemExit(1)

    print("PASS Z4 multi-operation congruence verifier")
    print("partitions:", result["partition_count"])
    print("congruences:", sorted(result["good"]))


if __name__ == "__main__":
    main()
