#!/usr/bin/env python3
"""Exact three-event owner restoration for tested arbitrary L>=3,c>=L.

No general owner callback is invoked. A holder terminal leaves that separate
obligation open. See docs/research/GENERAL-OWNER-TERMINAL-RESTORATION.md.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros


def prefix(z, a, p, r):
    assert 3 <= z.ell <= z.c and not z.x[a]
    assert a in z.x[p] and r in z.x[p] and a not in z.x[r]
    assert z.x[p][a] == max(z.x[p].values())
    original = [dict(row) for row in z.x]
    holders = {v for v, row in enumerate(z.x) if a in row}
    oldzeros = zeros(z, a)
    residual = set(z.x[p]) - {a}
    high = max(z.x[p][v] for v in residual)
    oldest = {v for v in residual if z.x[p][v] == high}
    s = min({v for v in oldest if a not in z.x[v]} or oldest)
    holder = a in z.x[s]
    e = min(z.ell - 1, len(z.x[p]) - 1)
    extra = {s} | ({r} if holder else set())
    extra |= set(sorted(residual - extra)[:e - len(extra)])
    E = extra - {s}
    d = len(z.x[p])
    z.step(p, a, extra, set())
    assert set(z.x[a]) == {p, s} | E
    extra2 = set(z.x[a]) - {s}
    reply = {a} if holder else set()
    reply |= set(sorted(set(z.x[s]) - reply)[:min(z.ell, len(z.x[s])) - len(reply)])
    resident = set(z.x[a]) - {s}
    needed = max(0, len(resident) + len(reply - resident - {a}) - z.c)
    eligible = extra2 - reply - ({r} if holder else set())
    assert needed <= len(eligible)
    z.step(a, s, extra2, reply, vp=set(sorted(eligible)[:needed]))
    assert {a, p} | E <= set(z.x[s]) and z.x[s][a] == 0
    if holder:
        assert r in z.x[a] and z.x[r] == original[r]
    f = min(z.ell - 1, d - 2)
    assert f - len(E) in (0, 1)
    extra3 = E | set(sorted(set(z.x[p]) - {s} - E)[:f - len(E)])
    incoming = {p} | extra3
    novel = incoming - set(z.x[s])
    assert len(novel) <= 1
    need = max(0, len(z.x[s]) + len(novel) - z.c)
    reply = {a, p}
    if need:
        assert z.c >= z.ell + 1 and len(E) == z.ell - 2
        safe = min(set(z.x[s]) - {a, p} - E)
        assert safe not in incoming
        reply.add(safe)
        victim = {safe}
    else:
        victim = set()
    reply |= set(sorted(set(z.x[s]) - reply)[:min(z.ell, len(z.x[s])) - len(reply)])
    z.step(p, s, extra3, reply, vq=victim)
    assert z.x[p][a] == z.x[s][a] == 0
    assert {v for v, row in enumerate(z.x) if a in row} == holders | {s}
    assert oldzeros <= zeros(z, a)
    assert all(z.x[v] == original[v] for v in range(z.n) if v not in {a, p, s})
    if holder:
        assert r in z.x[a] and z.x[r] == original[r] and a not in z.x[r]
    return Counter({('holder_restored_target_cached' if holder else 'strict_gain'): 1,
                    'safe_x_eviction': need,
                    'third_request_extra_u': f - len(E),
                    'full_shuffle': z.c == z.ell})


def trial(n, c, L, size, seed):
    rng = Random(seed)
    ages = (0, 1, 7, 10**6)
    rows = [{} for _ in range(n)]
    extras = [2] + rng.sample(list(range(3, n)), size - 2)
    rows[1] = {0: 10**6, **{v: rng.choice(ages) for v in extras}}
    for v in range(2, n):
        rows[v] = {1: rng.choice(ages)}
        if v != 2 and rng.randrange(2):
            rows[v][0] = rng.choice(ages)
        candidates = sorted(set(range(n)) - {0, v} - set(rows[v]))
        maximum = min(c, len(rows[v]) + len(candidates))
        target = maximum if seed % 2 else rng.randint(len(rows[v]), maximum)
        for u in rng.sample(candidates, target - len(rows[v])):
            rows[v][u] = rng.choice(ages)
    return prefix(ActualThree(rows, c, L), 0, 1, 2)


def main():
    total = Counter()
    cases = 0
    for n in range(4, 15):
        for L in range(3, n):
            for c in range(L, n):
                for size in range(2, c + 1):
                    for seed in range(6):
                        total.update(trial(n, c, L, size, n * 100000 + L * 10000 + c * 100 + size * 7 + seed))
                        cases += 1
    assert total['safe_x_eviction'] and total['holder_restored_target_cached']
    print('PASS general owner-terminal prefix cases/events:', cases, 3 * cases)
    print('Exact branch counts:', dict(sorted(total.items())))
    print('Scope: three-event prefix only; arbitrary-length callback is NOT invoked or proved.')


if __name__ == '__main__':
    main()
