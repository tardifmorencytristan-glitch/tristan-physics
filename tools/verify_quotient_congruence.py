#!/usr/bin/env python3
"""Verify valid and invalid quotient/coarse-graining witnesses."""

def same_parity(a, b):
    return (a - b) % 2 == 0


def parity_congruence_check(limit=5):
    values = range(-limit, limit + 1)
    for a in values:
        for ap in values:
            if not same_parity(a, ap):
                continue
            for b in values:
                for bp in values:
                    if not same_parity(b, bp):
                        continue
                    if not same_parity(a + b, ap + bp):
                        return False
    return True


def invalid_witness():
    # a ~ ap, but composing on the left by b yields c and d in different classes.
    classes = {
        "a": 0,
        "ap": 0,
        "b": 1,
        "c": 2,
        "d": 3,
    }
    composition = {
        ("b", "a"): "c",
        ("b", "ap"): "d",
    }
    equivalent_inputs = classes["a"] == classes["ap"]
    equivalent_outputs = classes[composition[("b", "a")]] == classes[composition[("b", "ap")]]
    return equivalent_inputs and not equivalent_outputs


def main():
    parity_ok = parity_congruence_check()
    invalid_ok = invalid_witness()

    if not parity_ok:
        print("FAIL parity congruence")
        raise SystemExit(1)
    if not invalid_ok:
        print("FAIL invalid witness")
        raise SystemExit(1)

    print("PASS parity congruence witness")
    print("PASS non-congruence counterexample")
    print("Verified: structure-preserving quotient requires composition compatibility.")


if __name__ == "__main__":
    main()
