#!/usr/bin/env python3
"""Corroborate the dimension-independent c=ell=3 incoming boundary identity.

This checks the local merge/component alternative, not accessibility of its
extremal hypotheses. Initial unused outside rows may be empty; connectedness
is not an assumption of this local identity. No convergence claim follows
from these finite tests alone.
"""
from collections import Counter
from random import Random
from verify_thesis_cooperative_owner import ActualThree, zeros
from verify_thesis_dense_three_boundary import components


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    counts = Counter()
    cases = 0
    a, P, Q = 0, 1, 2
    for n in range(4, 41):
        for seed in range(150):
            rng = Random(1000*n + seed)
            I = {Q, *rng.sample(list(range(3, n)), rng.randrange(n-2))}
            groups = {}
            for v in sorted(I):
                groups.setdefault(rng.randrange(1 + len(I)), []).append(v)
            base = [{} for _ in range(n)]
            age = rng.choice((0, 1, 2, 10**6))
            for group in groups.values():
                rng.shuffle(group)
                if Q in group:
                    group.remove(Q)
                    group.append(Q)
                for j, v in enumerate(group):
                    heads = group[max(j+1, len(group)-2):]
                    base[v] = {a: 0, **{r: age for r in heads}}
            assert base[Q] == {a: 0}
            d = len(components(base, I, a))
            for size in range(3):
                extras = rng.sample(list(range(3, n)), min(size, n-3))
                x = [row.copy() for row in base]
                x[P] = {Q: age+3, **dict.fromkeys(extras, age)}
                z = ActualThree(x, 3, 3)
                assert zeros(z, a) == I
                z.step(P, Q, extras, [a])
                newI = zeros(z, a)
                assert not z.x[a]
                if len(extras) <= 1:
                    assert newI == I | {P}
                    branch = 'zero_gain'
                else:
                    assert newI == (I - {Q}) | {P}
                    assert set(z.x[P]) == {a, *extras}
                    assert set(z.x[Q]) == {P, *extras}
                    outgoing = [(u, v) for u in newI for v in z.x[u] if v not in newI | {a}]
                    if outgoing:
                        branch = 'outward_edge'
                    else:
                        assert len(components(z.x, newI, a)) < d
                        branch = 'component_decrease'
                counts[branch] += 1
                cases += 1
    print('PASS c3 boundary local cases:', cases, 'n=4..40', dict(counts))


if __name__ == '__main__':
    main()
