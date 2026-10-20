#!/usr/bin/env python3
"""Exact local checks for a proper-shuffle underfull-zero bootstrap.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_underfull_bootstrap.py

For ell<c, a nonzero-a initiator contacting an underfull a^0 responder
can receive a^0 while preserving the responder's old zero. The checker
exhausts small local ID configurations and all maximum request extras;
it searches a legal reply/victim choice, then executes the exact MIN,
received-protected kernel. This hypothesis fails at full shuffle when
the request has c novel IDs.

The second suite checks a two-exchange bootstrap when exactly one
nonowner p lacks a^0, all old zero holders are underfull, and p is
nonempty. If p's oldest is a zero holder, use the local exchange. If it
is owner a, first p->a leaves p with zero-holder heads, or makes owner a
singleton p and p empty; the next legal exchange creates the new zero.
This does not resolve the missing-peer-empty initial regime.

Reproduced default result: 33,520 exhaustive local exchanges through
n=8; 5,720 near-complete cases through n=15 and 6,300 exchanges. The
macro suite exercises 5,140 direct contacts, 572 owner-then-zero-holder
paths, and eight owner-then-singleton callbacks. Ages include 0,...,3
and independent offsets of 1,000,000.
"""
from itertools import combinations
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros


def subsets(pool, size):
    return (set(t) for t in combinations(sorted(pool), size))


def retaining_reply(z, p, q, a, extra):
    Q = set(z.x[q])
    outgoing = {p} | set(extra)
    needed = max(0, len(Q) + len(outgoing - Q - {q}) - z.c)
    length = min(z.ell, len(Q))
    assert z.ell < z.c and len(Q) < z.c and a in Q
    eligible = sorted(Q - outgoing - {a})
    assert len(eligible) >= needed and needed <= length - 1
    victims = set(eligible[:needed])
    reply = {a} | victims
    reply.update(sorted(Q - reply)[:length - len(reply)])
    assert len(reply) == length
    return sorted(reply), sorted(victims)


def finish(z, p, q, a):
    before = zeros(z, a)
    P = set(z.x[p])
    k = min(z.ell - 1, len(P) - 1)
    extra = ([a] if a in P - {q} else [])
    extra += sorted(P - {q} - set(extra))[:k - len(extra)]
    reply, victims = retaining_reply(z, p, q, a, extra)
    z.step(p, q, extra, reply, vq=victims)
    assert zeros(z, a) == before | {p}


def local(max_n):
    cases = 0
    # Owner a=1, active nonholder p=0, actual partner q=2; labels are
    # fixed by local permutation symmetry. Source has no a descriptor,
    # which is the harder retention case since outgoing a protects it.
    p, a, q = 0, 1, 2
    for n in range(5, max_n + 1):
        for c in range(4, n):
            for ell in range(3, c):
                source_pool = set(range(n)) - {p, a, q}
                target_pool = set(range(n)) - {q, a}
                for source_size in range(1, min(c, n - 2) + 1):
                    for other in subsets(source_pool, source_size - 1):
                        P = other | {q}
                        for extra in subsets(P - {q}, min(ell - 1, len(P) - 1)):
                            for b in range(1, c):
                                for rest in subsets(target_pool, b - 1):
                                    x = [{} for _ in range(n)]
                                    x[p] = dict.fromkeys(P, 0)
                                    x[q] = {a: 0, **dict.fromkeys(rest, 0)}
                                    z = ActualThree(x, c, ell)
                                    reply, victims = retaining_reply(z, p, q, a, extra)
                                    z.step(p, q, extra, reply, vq=victims)
                                    assert z.x[p].get(a) == z.x[q].get(a) == 0
                                    cases += 1
    return cases


def near_complete(n, c, ell, rng, offset, counts):
    order = list(range(n))
    rng.shuffle(order)
    a, p = order[:2]
    I = set(order[2:])
    x = [{} for _ in range(n)]
    for q in I:
        pool = sorted(set(range(n)) - {q, a})
        k = rng.randrange(c - 1)
        x[q] = {a: 0, **{r: offset + rng.randrange(4) for r in rng.sample(pool, k)}}
    for q in (a, p):
        pool = sorted(set(range(n)) - {q})
        k = rng.randint(1 if q == p else 0, c)
        x[q] = {r: offset + rng.randrange(4) for r in rng.sample(pool, k)}
        if q == p and a in x[q]:
            x[q][a] = max(1, x[q][a])
    z = ActualThree(x, c, ell)
    assert zeros(z, a) == I
    top = max(z.x[p].values())
    q = min(r for r in z.x[p] if z.x[p][r] == top)
    if q in I:
        finish(z, p, q, a)
        counts['direct'] = counts.get('direct', 0) + 1
    else:
        assert q == a
        source = set(z.x[p])
        extra = sorted(source - {a})[:min(ell - 1, len(source) - 1)]
        reply = sorted(z.x[a])[:min(ell, len(z.x[a]))]
        # If owner can return an old zero-holder head, include one.
        if set(z.x[a]) & I and not set(reply) & I:
            reply[-1] = min(set(z.x[a]) & I)
        z.step(p, a, extra, reply)
        assert zeros(z, a) == I
        if z.x[p]:
            assert set(z.x[p]) <= I
            top = max(z.x[p].values())
            q = min(r for r in z.x[p] if z.x[p][r] == top)
            finish(z, p, q, a)
            counts['owner_then_zero'] = counts.get('owner_then_zero', 0) + 1
        else:
            assert z.x[a] == {p: 0}
            z.step(a, p, [], [])
            counts['owner_then_singleton'] = counts.get('owner_then_singleton', 0) + 1
    assert zeros(z, a) == I | {p} and z.steps <= 2
    return z.steps


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--local-max-n', type=int, default=8)
    ap.add_argument('--max-n', type=int, default=15)
    ap.add_argument('--seeds', type=int, default=10)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled')
    lc = local(args.local_max_n)
    cases = exchanges = 0
    counts = {}
    for n in range(5, args.max_n + 1):
        for c in range(4, n):
            for ell in range(3, c):
                for seed in range(args.seeds):
                    for offset in (0, 1000000):
                        exchanges += near_complete(n, c, ell, Random(1000003*n+7919*c+101*ell+seed), offset, counts)
                        cases += 1
    # Tight excluded full-shuffle case: singleton a^0 responder has no
    # alternative victim when the three received IDs are all novel.
    x = [{2: 0, 3: 0, 4: 0}, {}, {1: 0}, {}, {}]
    bad = ActualThree(x, 3, 3)
    bad.step(0, 2, [3, 4], [1])
    assert bad.x[0].get(1) == 0 and 1 not in bad.x[2]
    print('PASS exhaustive local cases', lc, 'near-complete cases/exchanges', (cases, exchanges), 'branches', counts, 'and excluded full-shuffle failure')


if __name__ == '__main__':
    main()
