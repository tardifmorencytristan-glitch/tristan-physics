#!/usr/bin/env python3
"""Finite verifier for free-path associativity and identities."""

from __future__ import annotations

import argparse
from itertools import product


def source(path, edge_map, empty_vertex=None):
    if path:
        return edge_map[path[0]][0]
    return empty_vertex


def target(path, edge_map, empty_vertex=None):
    if path:
        return edge_map[path[-1]][1]
    return empty_vertex


def compose(left, right, edge_map, left_empty_vertex=None, right_empty_vertex=None):
    """Return left o right, represented as right + left."""
    right_target = target(right, edge_map, right_empty_vertex)
    left_source = source(left, edge_map, left_empty_vertex)
    if right_target != left_source:
        raise ValueError("non-composable paths")
    return tuple(right) + tuple(left)


def enumerate_paths(vertices, edges, max_len):
    edge_map = {name: (u, v) for name, u, v in edges}
    paths = [((), v, v) for v in vertices]

    for length in range(1, max_len + 1):
        for names in product(edge_map.keys(), repeat=length):
            ok = True
            for i in range(length - 1):
                if edge_map[names[i]][1] != edge_map[names[i + 1]][0]:
                    ok = False
                    break
            if ok:
                paths.append((tuple(names), edge_map[names[0]][0], edge_map[names[-1]][1]))

    return edge_map, paths


def verify(vertices, edges, max_len=4):
    edge_map, paths = enumerate_paths(vertices, edges, max_len)

    for p, s, t in paths:
        left_identity = compose((), p, edge_map, left_empty_vertex=t, right_empty_vertex=s)
        right_identity = compose(p, (), edge_map, left_empty_vertex=s, right_empty_vertex=s)
        if left_identity != p or right_identity != p:
            return False, {"failure": "identity", "path": p, "s": s, "t": t}

    for p, ps, pt in paths:
        for q, qs, qt in paths:
            if pt != qs:
                continue
            for r, rs, rt in paths:
                if qt != rs:
                    continue
                if len(p) + len(q) + len(r) > max_len:
                    continue

                qp = compose(q, p, edge_map)
                lhs = compose(r, qp, edge_map)

                rq = compose(r, q, edge_map)
                rhs = compose(rq, p, edge_map)

                if lhs != rhs:
                    return False, {
                        "failure": "associativity",
                        "p": p,
                        "q": q,
                        "r": r,
                        "lhs": lhs,
                        "rhs": rhs,
                    }

    return True, {"path_count": len(paths)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-len", type=int, default=4)
    args = parser.parse_args()

    vertices = ("A", "B", "C")
    edges = (
        ("f", "A", "B"),
        ("g", "B", "C"),
        ("h", "A", "C"),
        ("u", "A", "A"),
        ("v", "B", "B"),
        ("w", "C", "C"),
    )

    ok, detail = verify(vertices, edges, args.max_len)
    if not ok:
        print("FAIL", detail)
        raise SystemExit(1)

    print("PASS free-path verifier", detail)


if __name__ == "__main__":
    main()
