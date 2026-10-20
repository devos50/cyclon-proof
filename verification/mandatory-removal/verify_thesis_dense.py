#!/usr/bin/env python3
"""Exact ell=2 checks for the dense-cache common-class argument.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_dense.py

For every dense capacity max(3,n-2)<=c<=n-1 through --max-n (default 7),
enumerate every active cache with fixed initiator 0 and oldest partner 1,
every responder cache, every legal one-extra choice, and every maximum-size
reply subset. Check that no surviving active resident is evicted. Symmetry
of labels makes the fixed endpoint labels immaterial for this local claim.
The same enumeration checks every possible root-only-anchor incoming
contact with an initiator having no anchor copy.

Random numerical-age cases through --random-n (default 30) execute the
outward-closure controller from extremal-state hypotheses: only the chosen
zero-holder activates, every holder reply includes the anchor and its
initiator identity when known, and the first nonholder contact increases
the TOTAL number of anchor holders. This tests exact maximum-size buffers,
protected victim choices, MIN merges, and actual oldest choices. Additional
random cases check the normalized-root contact with arbitrary anchor labels
and ages. These finite checks corroborate the arbitrary-size structural
proof; they do not replace it. Requires the sibling exact-kernel verifier
and Python's standard library. Assertions must be enabled.

Reproduced default result: 43,338 exhaustive no-eviction transitions and
468 exhaustive root contacts; 1,060 random outward-control witnesses and
1,060 random root contacts, using 3,145 exchanges. The longest outward
prelude/contact trajectory uses 27 exchanges.
"""
from itertools import combinations
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_anchor import Actual


def subsets(ids, capacity):
    for k in range(min(len(ids), capacity) + 1):
        yield from combinations(ids, k)


def holders(z, a):
    return {p for p in range(z.n) if a in z.x[p]}


def root_contact(z, a, p, q, extra):
    old = holders(z, a)
    assert z.c >= 3 and z.x[q] == {a: 0} and p not in old
    active = set(z.x[p])
    z.step(p, q, extra, [a])
    assert holders(z, a) == old | {p}
    assert z.x[p][a] == z.x[q][a] == 0
    assert active - {q} <= set(z.x[p])


def exhaustive(max_n):
    count = root = 0
    for n in range(4, max_n + 1):
        p, q = 0, 1
        for c in range(max(3, n - 2), n):
            P_options = [v for v in subsets(tuple(range(1, n)), c) if q in v]
            Q_options = list(subsets(tuple(v for v in range(n) if v != q), c))
            for P in P_options:
                extras = [()] if len(P) == 1 else [(v,) for v in P if v != q]
                for Q in Q_options:
                    for reply in combinations(Q, min(2, len(Q))):
                        for extra in extras:
                            x = [{} for _ in range(n)]
                            x[p] = {v: int(v == q) for v in P}
                            x[q] = dict.fromkeys(Q, 0)
                            z = Actual(x, c)
                            z.step(p, q, extra, reply)
                            assert set(P) - {q} <= set(z.x[p])
                            count += 1
                for a in set(range(n)) - set(P) - {p}:
                    for extra in extras:
                        x = [{} for _ in range(n)]
                        x[p] = {v: int(v == q) for v in P}
                        x[q] = {a: 0}
                        z = Actual(x, c)
                        root_contact(z, a, p, q, extra)
                        root += 1
    return count, root


def outward(z, a, p, J, rng):
    old = holders(z, a)
    assert z.x[p].get(a) == 0 and set(z.x[p]) & J
    original_targets = set(z.x[p]) & J
    start = z.steps
    while True:
        nonanchors = set(z.x[p]) - {a}
        assert nonanchors
        q = max(nonanchors, key=lambda v: (z.x[p][v], -v))
        assert z.x[p][q] == max(z.x[p].values())
        Q = z.x[q]
        if q in old:
            reply = [a]
            if len(Q) >= 2:
                reply.append(p if p in Q else rng.choice(sorted(set(Q) - {a})))
        else:
            assert q in J and a not in Q
            reply = rng.sample(sorted(Q), min(2, len(Q)))
        z.step(p, q, [a], reply)
        assert original_targets - {q} <= set(z.x[p])
        if q in J:
            assert holders(z, a) == old | {q}
            assert a in z.x[p] and z.x[p][a] > 0
            assert z.steps - start <= z.n + z.c
            return z.steps - start
        assert z.x[p][a] == 0
        assert holders(z, a) == old
        assert z.steps - start <= z.n + z.c


def random_checks(max_n, seeds):
    count = roots = exchanges = longest = 0
    for n in range(4, max_n + 1):
        for c in range(max(3, n - 2), n):
            for seed in range(seeds):
                rng = Random(1000003 * n + 7919 * c + seed)
                labels = list(range(n))
                rng.shuffle(labels)
                a = labels[0]
                k = rng.randint(1, n - 2)
                I = set(labels[1:k + 1])
                J = set(labels[k + 1:])
                x = [{} for _ in range(n)]
                for p in I:
                    pool = sorted(set(range(n)) - {a, p})
                    chosen = rng.sample(pool, rng.randrange(min(c - 1, len(pool)) + 1))
                    x[p] = {a: 0, **{v: rng.randint(0, 1000000) for v in chosen}}
                for p in J:
                    pool = sorted(set(range(n)) - {a, p})
                    chosen = rng.sample(pool, rng.randrange(min(c, len(pool)) + 1))
                    x[p] = {v: rng.randint(0, 1000000) for v in chosen}
                p = rng.choice(sorted(I))
                target = rng.choice(sorted(J))
                if target not in x[p]:
                    if len(x[p]) == c:
                        del x[p][rng.choice(sorted(set(x[p]) - {a}))]
                    x[p][target] = rng.randint(0, 1000000)
                z = Actual(x, c)
                length = outward(z, a, p, J, rng)
                exchanges += length
                longest = max(longest, length)
                count += 1
                # Normalized Q need not be known before the pending exchange;
                # its initiator is frozen while only Q's component is cleared.
                p = rng.choice(sorted(J))
                q = rng.choice(sorted(I))
                pool = sorted(set(range(n)) - {a, p, q})
                chosen = rng.sample(pool, rng.randrange(min(c - 1, len(pool)) + 1))
                xx = [{} for _ in range(n)]
                xx[p] = {v: rng.randint(0, 1000000) for v in chosen}
                xx[p][q] = max(xx[p].values(), default=0) + rng.randint(0, 1000000)
                xx[q] = {a: 0}
                extras = rng.sample(sorted(set(xx[p]) - {q}), min(1, len(xx[p]) - 1))
                zz = Actual(xx, c)
                root_contact(zz, a, p, q, extras)
                roots += 1
                exchanges += 1
    return count, roots, exchanges, longest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-n', type=int, default=7)
    ap.add_argument('--random-n', type=int, default=30)
    ap.add_argument('--seeds', type=int, default=20)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled; do not use python -O')
    ex = exhaustive(args.max_n)
    rr = random_checks(args.random_n, args.seeds)
    print('PASS exhaustive_no_eviction/root_contacts', ex,
          'random_outward/root_contacts/exchanges/max_prelude', rr)


if __name__ == '__main__':
    main()
