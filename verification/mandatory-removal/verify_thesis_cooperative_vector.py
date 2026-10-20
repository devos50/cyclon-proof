#!/usr/bin/env python3
"""Exact full-shuffle callback checks with a common positive-age vector.

For ell=c>=3, the old zero holders I share a^0 and c-2 secondary anchors
at arbitrary common ages m_p. The owner caches those secondary IDs at
ages at least m_p. A partial singleton clearing block stops before an
outside residual partner or a residual age below M=max m_p. Owner replies
then add at most one low-age I head. There are at most two nonsecondary
owner heads; with outside-I preference in oldest ties, at most two blocks
precede a new zero-holder contact. Exact numeric transitions are compared
with the residual singleton oracle after each internal exchange.

Run:
    python3 verification/mandatory-removal/verify_thesis_cooperative_vector.py

Default: every n=4,...,12 and c=3,...,n-1, four seeds and three age patterns
including common ages up to1,000,000. This checks the conditional lemma,
not establishment of its hypotheses in a general initial state.

Reproduced default result: 540 cases, 1,421 actual exchanges, comprising
291 independently compared residual exchanges and 1,130 owner exchanges;
maximum trajectory10. The suite exercises 316 empty blocks, 202 outside
boundary blocks and 72 low-inside blocks, ending at 428 secondary and
112 other nonzero targets.
"""
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, Residual, zeros, holder_count


def construct(z, a, P, I, vector, rng, counts):
    I, P = set(I), set(P)
    anchors = {a} | P
    assert len(P) == z.c - 2 and z.ell == z.c
    assert zeros(z, a) == I and P <= set(z.x[a])
    assert all(z.x[a][p] >= vector[p] for p in P)
    assert all(all(z.x[v].get(p) == age for p, age in vector.items()) for v in I)
    M = max(vector[p] for p in P)
    original = [row.copy() for row in z.x]
    H = holder_count(z, a)
    blocks = 0
    while True:
        top = max(z.x[a].values())
        oldest = [v for v in z.x[a] if z.x[a][v] == top]
        outside = [v for v in oldest if v not in I]
        q = rng.choice(outside if outside else oldest)
        if q not in I:
            z.step(a, q, set(z.x[a]) - {q}, set(z.x[q]))
            z.owner_steps += 1
            assert zeros(z, a) == I | {q} and holder_count(z, a) >= H
            assert all(z.x[v] == original[v] for v in range(z.n) if v not in I | {a, q})
            counts['terminal_secondary' if q in P else 'terminal_other'] = counts.get('terminal_secondary' if q in P else 'terminal_other', 0) + 1
            break
        frozen_owner = z.x[a].copy()
        oracle = Residual(z, a, P, I, anchor_ages=vector)
        current = oracle.inv[q]
        residual = None
        events = 0
        reason = 'empty_blocks'
        while oracle.caches[current]:
            cache = oracle.caches[current]
            residual = min(cache, key=lambda v: (-cache[v], v))
            age = cache[residual]
            if oracle.labels[residual] not in I:
                reason = 'outside_blocks'
                break
            if age < M:
                reason = 'low_inside_blocks'
                break
            oracle.activate(current, partner=residual)
            residual = None
            events += 1
            assert events <= len(I)
        assert z.x[a] == frozen_owner
        reply = sorted(anchors)
        if residual is None:
            assert z.x[q] == vector
        else:
            r = oracle.labels[residual]
            assert r in z.x[q]
            reply.append(r)
            if r in I:
                assert z.x[q][r] < M
        counts[reason] = counts.get(reason, 0) + 1
        z.step(a, q, set(z.x[a]) - {q}, reply)
        z.owner_steps += 1
        blocks += 1
        assert blocks <= 2
        assert P <= set(z.x[a]) and len(set(z.x[a]) - P) <= 2
        assert all(z.x[a][p] == vector[p] for p in P)
        assert zeros(z, a) == I and holder_count(z, a) == H
        assert all(all(z.x[v].get(p) == age for p, age in vector.items()) for v in I)
    assert z.owner_steps <= 3
    assert z.steps <= 2 * (z.n + z.c + 1) + 1


def trial(n, c, seed, pattern, counts):
    rng = Random(seed)
    order = list(range(n))
    rng.shuffle(order)
    a = order[0]
    P = set(order[1:c - 1])
    remaining = order[c - 1:]
    I = set(rng.sample(remaining, rng.randint(1, len(remaining))))
    vector = {a: 0}
    for p in P:
        vector[p] = 0 if pattern == 0 else rng.choice((0, 1, 2, 1000000))
    M = max(vector.values())
    anchors = set(vector)
    x = [{} for _ in range(n)]
    for v in range(n):
        if v in I:
            x[v] = dict(vector)
            pool = sorted(set(range(n)) - anchors - {v})
            if pool and rng.randrange(4):
                age = rng.choice((0, max(0, M - 1), M, M + 1, M + 1000000))
                x[v][rng.choice(pool)] = age
        elif v != a:
            pool = sorted(set(range(n)) - {v})
            chosen = rng.sample(pool, rng.randrange(min(c, len(pool)) + 1))
            x[v] = {p: rng.randint(1 if p == a else 0, 1000001) for p in chosen}
    heads = rng.sample(sorted(I), min(2, len(I)))
    x[a] = {**{p: vector[p] for p in P}, **{q: M + rng.randint(1, 1000000) for q in heads}}
    if pattern == 2:
        # A strictly older secondary makes the first contact terminate.
        p = rng.choice(sorted(P))
        x[a][p] = max(x[a].values()) + 1
    z = ActualThree(x, c, c)
    construct(z, a, P, I, vector, rng, counts)
    return z


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-n', type=int, default=12)
    ap.add_argument('--seeds', type=int, default=4)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled; do not use python -O')
    cases = exchanges = residual = owner = longest = 0
    counts = {}
    for n in range(4, args.max_n + 1):
        for c in range(3, n):
            for seed in range(args.seeds):
                for pattern in range(3):
                    z = trial(n, c, 1000003*n+7919*c+seed, pattern, counts)
                    cases += 1
                    exchanges += z.steps
                    residual += z.residual_steps
                    owner += z.owner_steps
                    longest = max(longest, z.steps)
    print('PASS cases/exchanges/residual/owner/longest',
          (cases, exchanges, residual, owner, longest), 'branches', counts)


if __name__ == '__main__':
    main()
