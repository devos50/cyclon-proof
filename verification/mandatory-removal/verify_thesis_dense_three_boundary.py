#!/usr/bin/env python3
"""Exact n=5,c=ell=3 singleton-responder component-minimum gadget.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_dense_three_boundary.py

Owner a is empty, I is residually closed, and every I component is in a
canonical rooted form. The actual oldest nonholder P contacts root Q with
cache {a^0}. The exact exchange must either create another zero, give a
new-I outward edge, or keep the zero count while strictly reducing the
number of residual I components. All partitions and canonical orders on
the available old-zero vertices are checked, with every request size and
three residual-age patterns. This audits the final local proof gadget;
it does not independently establish the earlier extremal hypotheses.

Reproduced result: 144 exact boundary cases; 108 zero gains, 27 outward
edges, and nine strict residual-component-count decreases.
"""
from itertools import combinations, permutations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros


def partitions(xs):
    if not xs:
        yield []
        return
    x, *rest = xs
    for blocks in partitions(rest):
        yield [{x}] + [set(b) for b in blocks]
        for j in range(len(blocks)):
            out = [set(b) for b in blocks]
            out[j].add(x)
            yield out


def components(x, I, a):
    left = set(I)
    result = []
    while left:
        reached = {min(left)}
        while True:
            more = reached | {v for u in reached for v in set(x[u]) & I} | {u for u in I if set(x[u]) & reached}
            if more == reached:
                break
            reached = more
        result.append(reached)
        left -= reached
    return result


def main():
    a, P, Q = 0, 1, 2
    n, c, ell = 5, 3, 3
    counts = {}
    cases = 0
    for k in range(1, 4):
        for others in combinations([3, 4], k - 1):
            I = {Q, *others}
            for blocks in partitions(sorted(I)):
                options = []
                for block in blocks:
                    roots = [Q] if Q in block else sorted(block)
                    options.append([tuple(order) + (root,) for root in roots for order in permutations(sorted(block - {root}))])
                for orders in product(*options):
                    for age in (0, 1, 1000000):
                        base = [{} for _ in range(n)]
                        for order in orders:
                            for j, v in enumerate(order):
                                # Canonical residual capacity-two atom: all
                                # nonroots cache the root and up to one next
                                # greatest ID in this prescribed order.
                                heads = order[max(j + 1, len(order) - 2):]
                                base[v] = {a: 0, **{r: age for r in heads}}
                        assert base[Q] == {a: 0}
                        assert zeros(ActualThree(base, c, ell), a) == I
                        d = len(components(base, I, a))
                        for extra_count in range(3):
                            for extras in combinations([3, 4], extra_count):
                                x = [row.copy() for row in base]
                                x[P] = {Q: age + 3, **dict.fromkeys(extras, age)}
                                z = ActualThree(x, c, ell)
                                z.step(P, Q, extras, [a])
                                newI = zeros(z, a)
                                assert z.x[a] == {}
                                if len(newI) == len(I) + 1:
                                    branch = 'zero_gain'
                                    assert extra_count <= 1
                                else:
                                    assert newI == (I - {Q}) | {P}
                                    assert extra_count == 2
                                    assert set(extras) <= set(z.x[P])
                                    outgoing = [(u, v) for u in newI for v in z.x[u] if v not in newI | {a}]
                                    if outgoing:
                                        branch = 'outward_edge'
                                    else:
                                        branch = 'component_decrease'
                                        assert len(components(z.x, newI, a)) < d
                                counts[branch] = counts.get(branch, 0) + 1
                                cases += 1
    print('PASS exact n5c3 normalized boundary cases', cases, 'branches', counts)


if __name__ == '__main__':
    main()
