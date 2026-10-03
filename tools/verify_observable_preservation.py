#!/usr/bin/env python3
"""Verify exact and approximate observable descent on the Z4 parity quotient."""

def oscillation(f, cls):
    return max(abs(f(a)-f(b)) for a in cls for b in cls)


def verify():
    classes=[[0,2],[1,3]]
    parity=lambda x:x%2
    normalized=lambda x:x/3

    parity_eps=max(oscillation(parity,c) for c in classes)
    norm_eps=max(oscillation(normalized,c) for c in classes)

    max_mid_error=0.0
    for c in classes:
        vals=[normalized(x) for x in c]
        midpoint=(min(vals)+max(vals))/2
        max_mid_error=max(max_mid_error,max(abs(normalized(x)-midpoint) for x in c))

    return {
        "parity_exact": parity_eps == 0,
        "parity_epsilon": parity_eps,
        "normalized_epsilon": norm_eps,
        "normalized_midpoint_max_error": max_mid_error,
        "half_bound_ok": max_mid_error <= norm_eps/2 + 1e-12
    }


def main():
    result=verify()
    if not result["parity_exact"]:
        print("FAIL exact parity descent",result)
        raise SystemExit(1)
    if not result["half_bound_ok"]:
        print("FAIL midpoint half bound",result)
        raise SystemExit(1)
    print("PASS observable preservation verifier")
    print(result)


if __name__=="__main__":
    main()
