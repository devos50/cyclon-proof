#!/usr/bin/env python3
"""Focused exact reserved-a0,p0 embedding and normalized-head deletion.

The reduced transition is implemented independently of ActualThree. Finite
checks corroborate the conditional lemma; no normalization algorithm or
accessibility of its hypotheses is assumed established by this script.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros


def lower_step(rows, cap, length, rng):
    active = [v for v, row in enumerate(rows) if row]
    if not active:
        return None
    p = rng.choice(active)
    P = {v: t + 1 for v, t in rows[p].items()}
    q = rng.choice([v for v, t in P.items() if t == max(P.values())])
    Q = dict(rows[q])
    extras = set(rng.sample(sorted(set(P) - {q}), min(length - 1, len(P) - 1)))
    reply = set(rng.sample(sorted(Q), min(length, len(Q))))
    request = {p: 0, **{v: P[v] for v in extras}}
    incoming = {v: Q[v] for v in reply}
    del P[q]

    def merge(resident, received, sent, receiver):
        valid = set(received) - {receiver}
        new = valid - set(resident)
        need = max(0, len(resident) + len(new) - cap)
        eligible = sent & set(resident) - valid
        assert need <= len(eligible)
        victims = set(rng.sample(sorted(eligible), need))
        result = {v: t for v, t in resident.items() if v not in victims}
        refreshes = sum(v in result and received[v] < result[v] for v in valid)
        for v in valid:
            result[v] = min(result.get(v, received[v]), received[v])
        return result, victims, refreshes

    A, vp, rp = merge(P, incoming, extras, p)
    B, vq, rq = merge(Q, request, reply, q)
    result = [dict(row) for row in rows]
    result[p], result[q] = A, B
    assert all(v not in row and len(row) <= cap for v, row in enumerate(result))
    stats = Counter({'reduced_events': 1, 'active_victims': len(vp),
                     'passive_victims': len(vq), 'minimum_refreshes': rp + rq,
                     'empty_responder': not Q})
    return result, p, q, extras, reply, vp, vq, stats


def embedding(L, c, m, seed):
    rng = Random(seed)
    cap, length = min(c - 2, m - 1), min(L - 2, m - 1)
    assert 1 <= length <= cap
    ages = (0, 1, 7, 10**6)
    lower = []
    # A spanning path keeps this residual component weakly connected;
    # its terminal vertex can have an empty residual cache.
    for v in range(m):
        row = {v + 1: rng.choice(ages)} if v + 1 < m else {}
        candidates = sorted(set(range(m)) - {v} - set(row))
        count = rng.randrange(min(cap - len(row), len(candidates)) + 1)
        for w in rng.sample(candidates, count):
            row[w] = rng.choice(ages)
        lower.append(row)
    n = max(c + 1, m + 2)
    actual = [{1: 7}, {}]
    actual += [{0: 0, 1: 0, **{v + 2: t for v, t in row.items()}} for row in lower]
    actual += [{0: 0} for _ in range(n - len(actual))]
    z = ActualThree(actual, c, L)
    total = Counter({'components': 1, 'effective_length_reduced': length < L - 2,
                     'effective_capacity_reduced': cap < c - 2})
    frozen = [dict(row) for row in actual]
    for _ in range(15):
        transition = lower_step(lower, cap, length, rng)
        if transition is None:
            break
        lower, p, q, extras, reply, vp, vq, stats = transition
        z.step(p + 2, q + 2, {0, 1} | {v + 2 for v in extras},
               {0, 1} | {v + 2 for v in reply},
               vp={v + 2 for v in vp}, vq={v + 2 for v in vq})
        for v in range(m):
            assert z.x[v + 2] == {0: 0, 1: 0, **{w + 2: t for w, t in lower[v].items()}}
        assert z.x[:2] == frozen[:2] and z.x[m + 2:] == frozen[m + 2:]
        total.update(stats)
    return total


def deletion(L, c, size, seed):
    rng = Random(seed)
    n = c + 3
    H = set(range(2, n))
    others = rng.sample(sorted(H - {2}), size - 2)
    rows = [{1: rng.choice((0, 1, 10**6)), 2: 10**6 + 1,
             **{v: rng.choice((0, 7, 10**6)) for v in others}}, {0: 0}]
    rows += [{0: 0, 1: 0} for _ in H]
    z = ActualThree(rows, c, L)
    oldzero = zeros(z, 0)
    original = [dict(row) for row in rows]
    extras = {1} | set(rng.sample(others, min(L - 2, len(others))))
    z.step(0, 2, extras, {0, 1})
    assert set(z.x[0]) == set(original[0]) - {2}
    assert z.x[0][1] == 0 and len(z.x[0]) == size - 1
    assert z.x[2][0] == z.x[2][1] == 0
    assert set(z.x[2]) - {0, 1} <= H
    assert zeros(z, 0) == oldzero
    assert all(z.x[v] == original[v] for v in range(n) if v not in (0, 2))


def main():
    total = Counter()
    deletions = 0
    for L in range(3, 10):
        for c in range(L, L + 4):
            for m in range(2, c + 5):
                for seed in range(12):
                    total.update(embedding(L, c, m, L * 100000 + c * 1000 + m * 20 + seed))
            for size in range(2, c + 1):
                for seed in range(8):
                    deletion(L, c, size, seed)
                    deletions += 1
    # A singleton residual component has no active reduced step; its actual
    # anchor-only row must be left alone, not activated as a fake no-op.
    singleton = ActualThree([{1: 7}, {}, {0: 0, 1: 0}, {0: 0}], 3, 3)
    before = [dict(row) for row in singleton.x]
    assert lower_step([{}], 0, 0, Random(0)) is None
    assert singleton.steps == 0 and singleton.x == before
    assert total['empty_responder'] and total['minimum_refreshes']
    assert total['active_victims'] and total['passive_victims']
    print('PASS exact residual embeddings:', dict(sorted(total.items())))
    print('PASS normalized owner-head deletions:', deletions)
    print('PASS singleton no-op omission; no generic accessibility or parameter-exhaustive proof claimed.')


if __name__ == '__main__':
    main()
