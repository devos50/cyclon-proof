#!/usr/bin/env python3
"""Exact sparse/full-capacity coupling until the first merge overflow.

Identical legal scheduler/oldest/packet choices are used before separation.
Finite runs corroborate only this local coupling, not an atom probability,
a geometric tail, almost-sure overflow, or infinitely many evictions.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree


def connected(rows):
    reached = {0}
    while True:
        more = reached | {v for u, row in enumerate(rows) if u in reached for v in row}
        more |= {u for u, row in enumerate(rows) if set(row) & reached}
        if more == reached:
            return len(reached) == len(rows)
        reached = more


def run(rows, c, L, rng, horizon=60):
    n = len(rows)
    assert L <= c < n - 1 and connected(rows)
    sparse, full = ActualThree(rows, c, L), ActualThree(rows, n - 1, L)
    stats = Counter({'runs': 1})
    for event in range(horizon):
        assert sparse.x == full.x
        p = rng.randrange(n)
        if not sparse.x[p]:
            stats['empty_scheduler_noops'] += 1
            continue
        age = max(sparse.x[p].values())
        q = rng.choice([v for v, t in sparse.x[p].items() if t == age])
        extras = set(rng.sample(sorted(set(sparse.x[p]) - {q}), min(L - 1, len(sparse.x[p]) - 1)))
        reply = set(rng.sample(sorted(sparse.x[q]), min(L, len(sparse.x[q]))))
        before = [dict(row) for row in sparse.x]
        # Independent merge-union sizes after mandatory partner removal and
        # self filtering, before any capacity-dependent victim selection.
        resident_p = set(before[p]) - {q}
        received_p = reply - {p}
        resident_q = set(before[q])
        received_q = ({p} | extras) - {q}
        union_p, union_q = resident_p | received_p, resident_q | received_q
        dp, dq = max(0, len(union_p) - c), max(0, len(union_q) - c)
        eligible_p, eligible_q = extras & resident_p - received_p, reply - received_q
        assert dp <= len(eligible_p) and dq <= len(eligible_q)
        vp = set(rng.sample(sorted(eligible_p), dp))
        vq = set(rng.sample(sorted(eligible_q), dq))
        sparse.step(p, q, extras, reply, vp=vp, vq=vq)
        full.step(p, q, extras, reply, vp=set(), vq=set())
        assert set(full.x[p]) == union_p and set(full.x[q]) == union_q
        assert all(sparse.x[v] == full.x[v] == before[v]
                   for v in range(n) if v not in {p, q})
        stats['coupled_exchanges'] += 1
        if not (dp or dq):
            assert sparse.x == full.x
            stats['no_overflow_exchanges'] += 1
            continue
        assert sparse.x != full.x
        assert dp + dq > 0 and (len(full.x[p]) > c or len(full.x[q]) > c)
        if dp:
            assert len(sparse.x[p]) == c and len(full.x[p]) > c
        if dq:
            assert len(sparse.x[q]) == c and len(full.x[q]) > c
        # Surviving entries have exactly the same MIN-merged numerical ages.
        for v in (p, q):
            assert set(sparse.x[v]) <= set(full.x[v])
            assert all(full.x[v][w] == t for w, t in sparse.x[v].items())
        stats['first_overflow'] += 1
        stats['active_first_overflow'] += bool(dp)
        stats['passive_first_overflow'] += bool(dq)
        stats['victims_at_first_overflow'] += dp + dq
        return stats
    stats['horizon_without_overflow'] += 1
    return stats


def trial(n, c, L, seed):
    rng = Random(seed)
    rows = []
    for v in range(n):
        # A directed cycle ensures initial weak connectivity at every c.
        row = {(v + 1) % n: rng.choice((0, 1, 9, 10**6))}
        candidates = sorted(set(range(n)) - {v} - set(row))
        size = c if seed % 3 == 0 else rng.randint(1, c)
        for w in rng.sample(candidates, size - 1):
            row[w] = rng.choice((0, 1, 9, 10**6))
        rows.append(row)
    return run(rows, c, L, rng)


def main():
    stats = Counter()
    for n in range(3, 15):
        for c in range(1, n - 1):
            for L in range(1, c + 1):
                for seed in range(12):
                    stats.update(trial(n, c, L, n * 100000 + c * 1000 + L * 20 + seed))
    assert stats['first_overflow'] and stats['no_overflow_exchanges']
    assert stats['active_first_overflow'] and stats['passive_first_overflow']
    print('PASS sparse/full first-overflow coupling:', dict(sorted(stats.items())))
    print('Per-run scheduler-event horizon: 60; no tail, probability, or infinite-eviction assertion.')


if __name__ == '__main__':
    main()
