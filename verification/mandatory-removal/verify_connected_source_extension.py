#!/usr/bin/env python3
"""Exact two-exchange source extension; does not test source accessibility."""
from itertools import combinations
from verify_thesis_cooperative_owner import ActualThree


def partitions(items):
    if not items:
        yield []
        return
    x, *tail = items
    for blocks in partitions(tail):
        yield [{x}] + [set(b) for b in blocks]
        for i in range(len(blocks)):
            out = [set(b) for b in blocks]
            out[i].add(x)
            yield out


def check_core():
    # Enumerates all complement partitions; S labels are representative
    # by permutation symmetry. Theorems supply paths between the inspected
    # canonical endpoints: this is not a simulation of those paths.
    count = 0
    for n in range(2, 8):
        W = set(range(1, n))
        for c in range(1, n):
            for s in range(1, c+1):
                S = set(range(1, s+1))
                for blocks in partitions(sorted(W)):
                    if any(not (A & S) for A in blocks):
                        continue
                    rows = [{v: 7 for v in S}] + [{} for _ in W]
                    for A in blocks:
                        order = sorted(A-S) + sorted(A & S)
                        for i, p in enumerate(order):
                            rows[p] = dict.fromkeys(order[i+1:][-c:], 0)
                    assert all(set(rows[p]) <= S for p in S)
                    K = S | {0}
                    assert set(rows[0]) == S
                    # Exact effective buffer cardinalities for every L.
                    for length in range(1, c+1):
                        effective = min(length, s)
                        for size in range(1, s+1):
                            assert min(length-1, size-1) == min(effective-1, size-1)
                            assert min(length, size) == min(effective, size)
                    # Replace closed full-capacity core by its canonical atom.
                    old = [dict(row) for row in rows]
                    order = [0] + sorted(S)
                    for i, p in enumerate(order):
                        rows[p] = dict.fromkeys(order[i+1:], 0)
                    assert set(rows[0]) == S
                    assert all(0 not in rows[p] for p in W)
                    assert all(rows[p] == old[p] for p in W-S)
                    adjacency = {p: set() for p in W}
                    for p in W:
                        for v in rows[p]:
                            assert v in W
                            adjacency[p].add(v)
                            adjacency[v].add(p)
                    reached = {next(iter(W))}
                    while True:
                        new = reached | set().union(*(adjacency[p] for p in reached))
                        if new == reached:
                            break
                        reached = new
                    assert reached == W
                    count += 1
    print(f'PASS {count} core-closure/endpoint configurations, n=2..7.')
    print('Core paths rely on the established full-capacity theorem, not this check.')


def main():
    count = 0
    for n in range(2, 9):
        for c in range(1, n):
            for length in range(1, c + 1):
                for s in range(1, c + 1):
                    # q=0; u=1 greatest; v=2 second greatest when s>=2.
                    order = list(range(3, n)) + ([2] if n > 2 else []) + [1]
                    for tied in (False, True):
                        rows = [{} for _ in range(n)]
                        rows[0] = {w: 7 if tied else 100-w for w in range(1, s+1)}
                        for i, p in enumerate(order):
                            rows[p] = dict.fromkeys(order[i+1:][-c:], 0)
                        for first in combinations(range(2, s+1), min(length-1, s-1)):
                            a = ActualThree(rows, c, length)
                            a.step(0, 1, first, (), vp=(), vq=())
                            if s == 1:
                                a.step(1, 0, (), (), vp=(), vq=())
                                assert all(a.x[p].get(1) == 0 for p in range(n) if p != 1)
                                count += 1
                                continue
                            for second in combinations(range(3, s+1), min(length-1, s-2)):
                                b = ActualThree(a.x, c, length)
                                b.step(0, 2, second, (1,), vp=(), vq=())
                                assert all(b.x[p].get(1) == 0 for p in range(n) if p != 1)
                                assert len(b.x[0]) == s-1
                                count += 1
    print(f'PASS {count} exact two-event paths, n=2..8, all c,L,s; strict/tied ages.')
    print('Scope: conditional local extension, not connected-source accessibility.')


if __name__ == '__main__':
    main()
    check_core()
