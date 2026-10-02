#!/usr/bin/env python3
"""Dependency-DAG verifier for Omega machine-readable theory files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_nodes(data):
    nodes = {}

    for primitive in data.get("primitives", []):
        name = primitive["name"]
        nodes[name] = []

    for definition in data.get("definitions", []):
        name = definition["name"]
        nodes[name] = list(definition.get("depends_on", []))

    for claim in data.get("claims", []):
        cid = claim["id"]
        nodes[cid] = list(claim.get("depends_on", []))

    return nodes


def validate_dependencies(data):
    nodes = build_nodes(data)
    missing = []

    for node, deps in nodes.items():
        for dep in deps:
            if dep not in nodes:
                missing.append((node, dep))

    visiting = set()
    visited = set()
    cycle = []

    def dfs(node, stack):
        nonlocal cycle
        if node in visited:
            return False
        if node in visiting:
            start = stack.index(node)
            cycle = stack[start:] + [node]
            return True

        visiting.add(node)
        stack.append(node)
        for dep in nodes.get(node, []):
            if dep in nodes and dfs(dep, stack):
                return True
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return False

    for node in nodes:
        if node not in visited and dfs(node, []):
            break

    duplicate_names = []
    seen = set()
    ordered_names = (
        [x["name"] for x in data.get("primitives", [])]
        + [x["name"] for x in data.get("definitions", [])]
        + [x["id"] for x in data.get("claims", [])]
    )
    for name in ordered_names:
        if name in seen:
            duplicate_names.append(name)
        seen.add(name)

    return {
        "ok": not missing and not cycle and not duplicate_names,
        "missing": missing,
        "cycle": cycle,
        "duplicates": duplicate_names,
        "node_count": len(nodes),
    }


def verify_file(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return validate_dependencies(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    failed = False
    for filename in args.files:
        path = Path(filename)
        result = verify_file(path)
        if result["ok"]:
            print(f"PASS {path}: {result['node_count']} dependency nodes, acyclic")
        else:
            failed = True
            print(f"FAIL {path}: {result}")

    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
