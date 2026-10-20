#!/usr/bin/env python3
"""Exact obstruction to owner-only target service for full/proper shuffles.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_owner_cycle.py

This checks a strongly connected five-peer, initially full-cache state
with arbitrary finite integer ages. Target1 does not cache owner0. Every
oldest choice in the first owner activation leads to an exact forced
two-state cycle: owner0 never contacts target1 while it is the sole
initiator. Maximal underfull buffers, received-ID protection, and MIN are
all implemented. This refutes an auxiliary owner-only service lemma; it
is NOT a counterexample to convergence under iid all-peer initiators.
An additional strongly connected four-peer example verifies the same
cycle and a three-exchange repair using one passive-peer activation.
Finally, for every m=3,...,30, the checker exhausts every state and every
oldest-partner branch of the analogous invariant family at c=ell=m.
It checks both n=m+1 underfull-owner and n=m+2 initially-full versions.
Reproduced totals: 8,120 invariant-state/oldest-partner branches and 434
initially-full first branches, in addition to the four-peer repair check.
The same n=m+2 family is also checked at proper-shuffle capacity c=m+1,
ell=m. Every cache is then underfull, and the same owner-only invariant
persists. This adds 8,120 invariant branches and 434 first branches.
Thus passive cache-size monotonicity alone cannot bootstrap the large-cache
callback hypothesis, even for proper shuffles. The family already has
shared zero anchors a^0,p^0, so it does not obstruct a cooperative callback.
"""
from copy import deepcopy


def step(x, p, q, c=3, ell=3):
    P = {v: age + 1 for v, age in x[p].items()}
    Q = x[q].copy()
    assert q in P and P[q] == max(P.values())
    extra = set(P) - {q}
    reply = set(Q)
    assert len(extra) == min(ell - 1, len(P) - 1)
    assert len(reply) == min(ell, len(Q))
    out = {p: 0, **{v: P[v] for v in extra}}
    incoming = Q
    del P[q]
    ip = set(incoming) - set(P) - {p}
    iq = set(out) - set(Q) - {q}
    dp = max(0, len(P) + len(ip) - c)
    dq = max(0, len(Q) + len(iq) - c)
    ep = extra - set(incoming)
    eq = reply - set(out)
    vp, vq = set(sorted(ep)[:dp]), set(sorted(eq)[:dq])
    assert len(vp) == dp and len(vq) == dq
    P = {v: t for v, t in P.items() if v not in vp}
    Q = {v: t for v, t in Q.items() if v not in vq}
    for v, t in incoming.items():
        if v != p:
            P[v] = min(P.get(v, t), t)
    for v, t in out.items():
        if v != q:
            Q[v] = min(Q.get(v, t), t)
    x[p], x[q] = P, Q
    assert all(i not in row and len(row) <= c for i, row in enumerate(x))


def strongly_connected(x):
    for p in range(len(x)):
        seen = {p}
        while True:
            new = seen | {v for u in seen for v in x[u]}
            if new == seen:
                break
            seen = new
        if len(seen) != len(x):
            return False
    return True


def family(m, full_initial=False, excluded=None):
    n = m + 2 if full_initial else m + 1
    a, p = 0, 1
    R = set(range(2, m + 1))
    x = [{} for _ in range(n)]
    for q in R:
        x[q] = {a: 0, p: 0, **{r: 1 for r in R - {q}}}
    if full_initial:
        w = m + 1
        x[a] = {p: 0, **dict.fromkeys(R, 1)}
        x[p] = dict.fromkeys(R | {w}, 0)
        x[w] = {p: 0, **dict.fromkeys(R, 0)}
        assert all(len(row) == m for row in x)
    else:
        assert excluded in R
        x[a] = {p: 0, **dict.fromkeys(R - {excluded}, 1)}
        x[p] = dict.fromkeys(R, 0)
    assert strongly_connected(x) and a not in x[p]
    return x, R


def verify_families():
    invariant_branches = full_first_branches = 0
    proper_invariant_branches = proper_first_branches = 0
    for m in range(3, 31):
        for excluded in range(2, m + 1):
            initial, R = family(m, excluded=excluded)
            for q in R - {excluded}:
                x = deepcopy(initial)
                step(x, 0, q, m, m)
                assert x[0] == {1: 0, **dict.fromkeys(R - {q}, 1)}
                assert x[1:] == initial[1:]
                invariant_branches += 1
        initial, R = family(m, full_initial=True)
        for q in R:
            x = deepcopy(initial)
            step(x, 0, q, m, m)
            assert x[0] == {1: 0, **dict.fromkeys(R - {q}, 1)}
            assert x[1:] == initial[1:]
            full_first_branches += 1
        for excluded in R:
            invariant = deepcopy(initial)
            invariant[0] = {1: 0, **dict.fromkeys(R - {excluded}, 1)}
            assert strongly_connected(invariant)
            assert all(len(row) < m + 1 for row in invariant)
            for q in R - {excluded}:
                x = deepcopy(invariant)
                step(x, 0, q, m + 1, m)
                assert x[0] == {1: 0, **dict.fromkeys(R - {q}, 1)}
                assert x[1:] == invariant[1:]
                proper_invariant_branches += 1
        for q in R:
            x = deepcopy(initial)
            step(x, 0, q, m + 1, m)
            assert x[0] == {1: 0, **dict.fromkeys(R - {q}, 1)}
            assert x[1:] == initial[1:]
            proper_first_branches += 1
    return invariant_branches, full_first_branches, proper_invariant_branches, proper_first_branches


def main():
    initial = [
        {1: 0, 2: 1, 3: 1},
        {2: 0, 3: 0, 4: 0},
        {0: 0, 1: 0, 3: 1},
        {0: 0, 1: 0, 2: 1},
        {1: 0, 2: 0, 3: 0},
    ]
    assert strongly_connected(initial)
    assert all(len(row) == 3 for row in initial)
    assert 0 not in initial[1]
    for first in (2, 3):
        x = deepcopy(initial)
        step(x, 0, first)
        other = 5 - first
        assert x[0] == {1: 0, other: 1}
        assert x[1:] == initial[1:]
        cycle_start = deepcopy(x)
        for _ in range(100):
            partner = other if _ % 2 == 0 else first
            assert x[0][partner] > x[0][1]
            step(x, 0, partner)
            assert x[1:] == initial[1:]
            assert x[0] == {1: 0, 5 - partner: 1}
        assert x == cycle_start
    small = [{1: 0, 2: 1}, {2: 0},
             {0: 0, 1: 0, 3: 1}, {0: 0, 1: 0, 2: 1}]
    assert strongly_connected(small)
    x = deepcopy(small)
    for partner in (2, 3):
        step(x, 0, partner)
    assert x == small
    repair = deepcopy(small)
    step(repair, 2, 3)
    assert repair == [{1: 0, 2: 1}, {2: 0},
                      {0: 0, 1: 0}, {0: 0, 1: 0, 2: 0}]
    step(repair, 0, 2)
    assert repair == [{1: 0}, {2: 0},
                      {0: 0, 1: 0}, {0: 0, 1: 0, 2: 0}]
    step(repair, 0, 1)
    assert repair == [{2: 0}, {2: 0, 0: 0},
                      {0: 0, 1: 0}, {0: 0, 1: 0, 2: 0}]
    assert all(repair[p].get(0) == 0 for p in (1, 2, 3))
    ff = verify_families()
    print('PASS: n4 cycle and three-step repair; n5 full-initial cycle; m3..30 full invariant/first and proper invariant/first branches', ff)


if __name__ == '__main__':
    main()
