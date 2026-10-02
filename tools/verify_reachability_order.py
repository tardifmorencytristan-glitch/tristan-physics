#!/usr/bin/env python3
"""Exhaustive verifier for the Omega reachability quotient toy model.

This is computational verification support, not a substitute for the proof in
docs/OMEGA_FORMAL_RESULTS_R1.md.
"""

from __future__ import annotations

import argparse
from itertools import combinations


def all_possible_edges(n: int):
    return [(i, j) for i in range(n) for j in range(n) if i != j]


def transitive_closure(n: int, edges):
    reach = [[False] * n for _ in range(n)]
    for i in range(n):
        reach[i][i] = True
    for u, v in edges:
        reach[u][v] = True

    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return reach


def quotient_classes(n: int, reach):
    unseen = set(range(n))
    classes = []
    while unseen:
        i = min(unseen)
        cls = {j for j in range(n) if reach[i][j] and reach[j][i]}
        classes.append(frozenset(cls))
        unseen.difference_update(cls)
    return classes


def strict_quotient_order(classes, reach):
    relation = set()
    reps = [min(cls) for cls in classes]
    for a, x in enumerate(reps):
        for b, y in enumerate(reps):
            if a == b:
                continue
            if reach[x][y] and not reach[y][x]:
                relation.add((a, b))
    return relation


def check_strict_partial_order(size: int, relation):
    # Irreflexive
    for i in range(size):
        if (i, i) in relation:
            return False, "irreflexivity"

    # Transitive
    for a, b in relation:
        for b2, c in relation:
            if b == b2 and (a, c) not in relation:
                return False, "transitivity"

    return True, None


def has_cycle(size: int, relation):
    outgoing = {i: [] for i in range(size)}
    indegree = {i: 0 for i in range(size)}
    for a, b in relation:
        outgoing[a].append(b)
        indegree[b] += 1

    queue = [i for i in range(size) if indegree[i] == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for nxt in outgoing[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return visited != size


def verify_graph(n: int, edges):
    reach = transitive_closure(n, edges)
    classes = quotient_classes(n, reach)
    relation = strict_quotient_order(classes, reach)

    ok, failure = check_strict_partial_order(len(classes), relation)
    if not ok:
        return False, {
            "failure": failure,
            "edges": sorted(edges),
            "classes": [sorted(c) for c in classes],
            "relation": sorted(relation),
        }

    if has_cycle(len(classes), relation):
        return False, {
            "failure": "cycle",
            "edges": sorted(edges),
            "classes": [sorted(c) for c in classes],
            "relation": sorted(relation),
        }

    return True, None


def exhaustive_verify(n: int):
    possible = all_possible_edges(n)
    total = 1 << len(possible)

    for mask in range(total):
        edges = [edge for bit, edge in enumerate(possible) if mask & (1 << bit)]
        ok, detail = verify_graph(n, edges)
        if not ok:
            return False, mask, detail

    return True, total, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-n",
        type=int,
        default=4,
        help="Exhaustively enumerate all loop-free directed graphs up to this size.",
    )
    args = parser.parse_args()

    if args.max_n < 1:
        raise SystemExit("--max-n must be >= 1")

    grand_total = 0
    for n in range(1, args.max_n + 1):
        ok, count, detail = exhaustive_verify(n)
        if not ok:
            print(f"FAIL n={n} mask={count}: {detail}")
            raise SystemExit(1)
        grand_total += count
        print(f"PASS n={n}: {count} directed graphs")

    print(f"PASS total: {grand_total} directed graphs")
    print("Verified: strict partial order + acyclicity on all enumerated models.")


if __name__ == "__main__":
    main()
