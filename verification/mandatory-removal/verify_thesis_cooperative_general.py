#!/usr/bin/env python3
"""Exact cooperative-owner service with ell-2 shared secondary anchors.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_cooperative_general.py

Default coverage is n=4,...,12, every 3<=ell<=c<=n-1, two seeds and age
bounds0/1,000,000. The owner caches all ell-2 secondary anchors; all old
zero holders share these anchors at age zero and have arbitrary additional
IDs/ages. Residual singleton clearing has capacity c-ell+1 and stops before
an outside partner. Replies give the owner all shared anchors and at most
one outside ID, strictly reducing its old-holder head count. Exact numeric
transitions are independently compared with residual singleton updates.
This checks a conditional structural lemma, not general bootstrap access
to the required shared anchors. Assertions must be enabled.

Reproduced default result: 660 cases, 4,774 actual exchanges, comprising
2,474 independently compared residual exchanges and 2,300 owner exchanges;
maximum trajectory68. The suite executes 664 outside-boundary blocks and
976 empty blocks, ending at 313 secondary and 347 other nonzero targets.
"""
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, Residual, zeros, holder_count


def construct(z, a, P, I, rng, counts):
    P, I = set(P), set(I)
    anchors = P | {a}
    assert len(P) == z.ell - 2 and P <= set(z.x[a])
    assert zeros(z, a) == I and not (P & I)
    assert all(all(z.x[v].get(p) == 0 for p in anchors) for v in I)
    original = [row.copy() for row in z.x]
    H = holder_count(z, a)
    initial_heads = len(set(z.x[a]) & I)
    blocks = 0
    while True:
        assert P <= set(z.x[a])
        mx = max(z.x[a].values())
        q = rng.choice([v for v in z.x[a] if z.x[a][v] == mx])
        if q not in I:
            pool = sorted(set(z.x[a]) - {q})
            extra = rng.sample(pool, min(z.ell - 1, len(pool)))
            reply = rng.sample(sorted(z.x[q]), min(z.ell, len(z.x[q])))
            z.step(a, q, extra, reply)
            z.owner_steps += 1
            assert zeros(z, a) == I | {q} and holder_count(z, a) >= H
            assert all(z.x[v] == original[v] for v in range(z.n) if v not in I | {a, q})
            counts['terminal_secondary' if q in P else 'terminal_other'] = counts.get('terminal_secondary' if q in P else 'terminal_other', 0) + 1
            break
        frozen_owner = z.x[a].copy()
        oracle = Residual(z, a, P, I)
        current = oracle.inv[q]
        boundary = None
        residual_events = 0
        while oracle.caches[current]:
            cache = oracle.caches[current]
            top = max(cache.values())
            partner = min(v for v in cache if cache[v] == top)
            if oracle.labels[partner] not in I:
                boundary = oracle.labels[partner]
                break
            oracle.activate(current, partner=partner)
            residual_events += 1
            assert residual_events <= len(I) + z.c - z.ell
        assert z.x[a] == frozen_owner and zeros(z, a) == I
        assert holder_count(z, a) == H
        reply = sorted(anchors)
        key = 'empty_blocks'
        if boundary is None:
            assert z.x[q] == dict.fromkeys(anchors, 0)
        else:
            assert boundary in z.x[q] and boundary not in I | anchors
            reply.append(boundary)
            key = 'boundary_blocks'
        counts[key] = counts.get(key, 0) + 1
        extra = sorted(P)
        required = min(z.ell - 1, len(z.x[a]) - 1)
        if len(extra) < required:
            extra.append(rng.choice(sorted(set(z.x[a]) - P - {q})))
        assert len(extra) == required
        old_heads, old_size = len(set(z.x[a]) & I), len(z.x[a])
        z.step(a, q, extra, reply)
        z.owner_steps += 1
        blocks += 1
        assert len(set(z.x[a]) & I) == old_heads - 1
        assert len(z.x[a]) <= old_size and P <= set(z.x[a])
        assert zeros(z, a) == I and holder_count(z, a) == H
        assert all(all(z.x[v].get(p) == 0 for p in anchors) for v in I)
        assert blocks <= initial_heads
    assert z.owner_steps <= initial_heads + 1 <= z.c - z.ell + 3
    assert z.steps <= initial_heads * (len(I) + z.c - z.ell) + initial_heads + 1


def trial(n, c, ell, seed, age, counts):
    rng = Random(seed)
    order = list(range(n))
    rng.shuffle(order)
    a = order[0]
    P = set(order[1:ell - 1])
    pool_I = order[ell - 1:]
    I = set(rng.sample(pool_I, rng.randint(1, len(pool_I))))
    anchors = {a} | P
    x = [{} for _ in range(n)]
    for v in range(n):
        if v in I:
            pool = sorted(set(range(n)) - anchors - {v})
            chosen = rng.sample(pool, rng.randrange(min(c - ell + 1, len(pool)) + 1))
            x[v] = {**dict.fromkeys(anchors, 0), **{q: rng.randint(0, age) for q in chosen}}
        elif v != a:
            pool = sorted(set(range(n)) - {v})
            chosen = rng.sample(pool, rng.randrange(min(c, len(pool)) + 1))
            x[v] = {q: rng.randint(1 if q == a else 0, age + 1) for q in chosen}
    heads = rng.sample(sorted(I), min(c - len(P), len(I)))
    x[a] = {**dict.fromkeys(P, 0), **{q: rng.randint(1, age + 1) for q in heads}}
    z = ActualThree(x, c, ell)
    construct(z, a, P, I, rng, counts)
    return z


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-n', type=int, default=12)
    ap.add_argument('--seeds', type=int, default=2)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled; do not use python -O')
    cases = exchanges = residual = owner = longest = 0
    counts = {}
    for n in range(4, args.max_n + 1):
        for c in range(3, n):
            for ell in range(3, c + 1):
                for seed in range(args.seeds):
                    for age in (0, 1000000):
                        z = trial(n, c, ell, 1000003*n+7919*c+101*ell+seed, age, counts)
                        cases += 1
                        exchanges += z.steps
                        residual += z.residual_steps
                        owner += z.owner_steps
                        longest = max(longest, z.steps)
    print('PASS cases/exchanges/residual/owner/longest',
          (cases, exchanges, residual, owner, longest), 'branches', counts)


if __name__ == '__main__':
    main()
