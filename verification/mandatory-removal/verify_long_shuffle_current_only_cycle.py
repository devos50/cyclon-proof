#!/usr/bin/env python3
"""Exact current-only two-cycle at every tested L>=4, c>=L.

The symbolic construction is in PARAMETERIZED-SHUFFLE-INDUCTION.md. This
refutes the unchanged restricted controller, NOT protocol convergence.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree


def check(n, c, L):
    assert 4 <= L <= c <= n - 1
    a, p, r, q, s = range(5)
    rows = [
        {}, {a: 0, r: 0, q: 1}, {p: 0},
        {a: 0, p: 0, r: 0, s: 1},
        {a: 0, p: 0, r: 0, q: 1},
    ] + [{r: 0} for _ in range(n - 5)]
    # Verify underlying connectivity, including frozen embedding peers.
    reached = {a}
    while True:
        more = reached | {v for u, row in enumerate(rows) if u in reached for v in row}
        more |= {u for u, row in enumerate(rows) if set(row) & reached}
        if more == reached:
            break
        reached = more
    assert reached == set(range(n))
    z = ActualThree(rows, c, L)
    original = [dict(row) for row in rows]
    Y = set(range(n)) - {a, q, s}
    F = lambda: sum(len(set(row) & Y) for row in z.x)
    assert F() == n + 1
    for t in range(20):
        partner, following = (q, s) if t % 2 == 0 else (s, q)
        assert z.x[p] == {a: 0, r: 0, partner: 1}
        # Unique oldest, all required extras, and all four reply entries:
        # no scheduler-fixed trajectory choice remains random.
        assert [v for v, age in z.x[p].items() if age == max(z.x[p].values())] == [partner]
        assert min(L - 1, len(z.x[p]) - 1) == 2
        assert min(L, len(z.x[partner])) == 4
        z.step(p, partner, {a, r}, set(z.x[partner]))
        assert z.x[p] == {a: 0, r: 0, following: 1}
        assert all(z.x[v] == original[v] for v in range(n) if v != p)
        assert F() == n + 1 and len(z.x[p]) == 3
        if t % 2:
            assert z.x == original
    return z.steps


def main():
    cases = events = 0
    for n in range(5, 23):
        for L in range(4, n):
            for c in range(L, n):
                events += check(n, c, L)
                cases += 1
    print('PASS current-only exact cycles/checked exchanges:', cases, events)
    print('All cases: connected embedding, unique oldest, forced packets, period two, F=n+1.')
    print('Scope: obstruction to restricted current-only control, not convergence.')


if __name__ == '__main__':
    main()
