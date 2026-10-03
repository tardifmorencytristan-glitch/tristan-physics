#!/usr/bin/env python3
"""Finite verifier for canonical relation <-> history encoding."""

from __future__ import annotations

import argparse


def all_possible_edges(n):
    return [(i, j) for i in range(n) for j in range(n)]


def relation_from_mask(n, mask):
    edges = all_possible_edges(n)
    return {
        edge
        for bit, edge in enumerate(edges)
        if mask & (1 << bit)
    }


def canonical_history_encoding(relation):
    # Histories are exactly relation pairs. Each history is admissible.
    return [
        {"source": x, "target": y, "admissible": True}
        for x, y in sorted(relation)
    ]


def induced_relation(histories):
    return {
        (h["source"], h["target"])
        for h in histories
        if h["admissible"]
    }


def verify_relation(relation):
    histories = canonical_history_encoding(relation)
    reconstructed = induced_relation(histories)
    return reconstructed == relation, reconstructed


def exhaustive_verify(n):
    edge_count = n * n
    total = 1 << edge_count
    for mask in range(total):
        relation = relation_from_mask(n, mask)
        ok, reconstructed = verify_relation(relation)
        if not ok:
            return False, mask, relation, reconstructed
    return True, total, None, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=3)
    args = parser.parse_args()

    if args.max_n < 1:
        raise SystemExit("--max-n must be >= 1")

    grand_total = 0
    for n in range(1, args.max_n + 1):
        ok, count, relation, reconstructed = exhaustive_verify(n)
        if not ok:
            print(f"FAIL n={n} mask={count}")
            print("relation:", sorted(relation))
            print("reconstructed:", sorted(reconstructed))
            raise SystemExit(1)
        grand_total += count
        print(f"PASS n={n}: {count} directed relations")

    print(f"PASS total: {grand_total} directed relations")
    print("Verified: canonical relation -> history -> relation round trip.")


if __name__ == "__main__":
    main()
