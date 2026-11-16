#!/usr/bin/env python3
"""Exact conditional all-younger owner-service dichotomy, L>=4.

Both pre- and post-exchange residual age conditions are explicit filters.
This checks a local implication, not accessibility or general owner service.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree


def check(rows, L, c, rng):
    a, p, q = 0, 1, 2
    u, v = rows[a][p], rows[q][p]
    assert rows[q][a] == 0 and v <= u + 1
    assert rows[a][q] == max(rows[a].values())
    assert all(age < v for identity, age in rows[q].items() if identity not in {a, p})
    others = set(rows[a]) - {p, q}
    B = set(sorted(others, key=lambda x: (-rows[a][x], x))[:min(L - 2, len(others))])
    extras = {p} | B
    reply = {a, p} | (B & set(rows[q]))
    remaining = min(L, len(rows[q])) - len(reply)
    reply |= set(rng.sample(sorted(set(rows[q]) - reply), remaining))
    novel_B = B - set(rows[q])
    request_size = 1 + len(extras)
    old_heads = len(rows[a]) - 1
    z = ActualThree(rows, c, L)
    resident = set(rows[a]) - {q}
    incoming_q = {a} | extras
    dp = max(0, len(resident) + len(reply - resident - {a}) - c)
    dq = max(0, len(rows[q]) + len(incoming_q - set(rows[q]) - {q}) - c)
    vp = set(rng.sample(sorted(extras - reply), dp))
    vq = set(rng.sample(sorted(reply - incoming_q), dq))
    z.step(a, q, extras, reply, vp=vp, vq=vq)
    assert p in z.x[a] and z.x[a][p] == z.x[q][p] == v
    assert z.x[q][a] == 0
    if any(age >= v for identity, age in z.x[q].items() if identity not in {a, p}):
        return Counter({'postcondition_not_met': 1})
    if novel_B or request_size < L:
        assert all(age < v for identity, age in z.x[a].items() if identity != p)
        return Counter({'novel_B_oldest' if novel_B else 'short_request_oldest': 1})
    assert len(z.x[a]) - 1 == old_heads - 1
    return Counter({'full_overlap_head_drop': 1})


def trial(L, c, size, seed):
    rng = Random(seed)
    n = c + 4
    rows = [{} for _ in range(n)]
    v = rng.choice((0, 1, 2, 7, 10**6))
    u = rng.choice((max(0, v - 1), v, v + 3))
    others = rng.sample(list(range(3, n)), size - 2)
    low = (0, max(0, v - 2), max(0, v - 1))
    values = low if seed % 3 else low + (v, v + 3)
    rows[0] = {1: u, **{w: rng.choice(values) for w in others}}
    rows[0][2] = max(rows[0].values()) + rng.randrange(2)
    rows[2] = {0: 0, 1: v}
    if v:
        candidates = list(range(3, n))
        count = rng.randrange(c - 1)
        for w in rng.sample(candidates, count):
            rows[2][w] = rng.choice((0, v - 1))
    return check(rows, L, c, rng)


def main():
    total = Counter()
    cases = 0
    for L in range(4, 11):
        for c in range(L, L + 5):
            for size in range(2, c + 1):
                for seed in range(100):
                    total.update(trial(L, c, size, L * 100000 + c * 1000 + size * 100 + seed))
                    cases += 1
    for branch in ('novel_B_oldest', 'short_request_oldest', 'full_overlap_head_drop'):
        assert total[branch] > 0
    print('PASS conditional transition checks:', cases)
    print('Exact branch/filter counts:', dict(sorted(total.items())))
    print('Scope: postcondition explicitly filtered; no owner-service accessibility claim.')


if __name__ == '__main__':
    main()
