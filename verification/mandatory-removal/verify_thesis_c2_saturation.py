#!/usr/bin/env python3
"""Exact numerical-age checks for the c=ell=2 saturation argument.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_c2_saturation.py

The extremal-state hypotheses are an empty owner a, no positive-age copies
of a, and an outclosed zero-holder set I. For each boundary initiator P and
each actual oldest partner, the controller normalizes the indicated residual
component by actual protected+MIN exchanges, with P frozen. It then executes
the exact incoming-boundary case distinction. Every outcome either increases
the number of age-zero a holders, or keeps that number and the empty owner
while strictly decreasing the residual weak-component count. The four-event
outward-infection gadget is also checked independently with arbitrary ages,
including positive-age a descriptors at its prospective new holder.
Additional checks execute the source-only shortest-path controller and the
positive-copy exclusion argument, including initially empty owners with no
age-zero copies and incoming positive-age descriptors.

Default exhaustive coverage is every cache state satisfying the hypotheses
on 3--5 peers with all residual/nonholder ages in {0,1}, and every legal
boundary initiator/oldest-partner choice. Random checks add arbitrary anchor
labels, populations through 20, and ages up to 1,000,000. Optional arguments
--exhaustive-n 4 --max-n 10 --seeds 2 give a quick run. These finite checks
corroborate the structural argument; they are not an enumeration proof for
arbitrary populations. Only the standard library and sibling verifiers are
required. Assertions must be enabled.

Reproduced default counts: 52,964 exhaustive initial states, 118,498
incoming-boundary witnesses, and 737,512 exact exchanges; 684 random incoming
witnesses plus 684 independent outward gadgets use another 46,582 exchanges.
All five branches occur (2,065 component-decrease outcomes in the combined
run). The normalization executes the actual residual singleton controller;
its endpoint is not assigned by fiat. Auxiliary checks cover 775 source-only
witnesses, 579 positive-copy witnesses, and 864 empty-owner/no-zero-copy
witnesses, using another 4,077 exact exchanges.
"""
from itertools import combinations, product
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_anchor import Actual, canonical_component


def holders(z, a):
    return {v for v in range(z.n) if v != a and z.x[v].get(a) == 0}


def components(z, a, I):
    I = set(I)
    assert all(set(z.x[v]) - {a} <= I for v in I)
    unseen = set(I)
    answer = []
    while unseen:
        reached = {min(unseen)}
        while True:
            more = reached | {
                w for v in reached for w in z.x[v] if w != a
            } | {v for v in I if set(z.x[v]) & reached}
            if more == reached:
                break
            reached = more
        assert reached <= unseen
        answer.append(reached)
        unseen -= reached
    return answer


def normalize(z, a, C, root):
    """Embed the already-verified residual singleton controller in C union a."""
    labels = [a] + sorted(C)
    inv = {v: i for i, v in enumerate(labels)}
    before = [r.copy() for r in z.x]
    local = Actual([{inv[v]: t for v, t in z.x[p].items()} for p in labels], 2)
    canonical_component(local, 0, set(range(1, len(labels))), inv[root])
    for p in labels:
        z.x[p] = {labels[v]: t for v, t in local.x[inv[p]].items()}
    z.steps += local.steps
    z.embedding_steps += local.embedding_steps
    assert z.x[a] == {}
    assert z.x[root] == {a: 0}
    assert all(z.x[v] == {a: 0, root: 0} for v in C - {root})
    assert all(z.x[v] == before[v] for v in range(z.n) if v not in labels)


def exchange(z, p, q):
    z.step(p, q, set(z.x[p]) - {q}, set(z.x[q]))


def outward(z, a, p, x):
    old = holders(z, a)
    assert z.x[a] == {} and z.x[p].get(a) == 0
    assert set(z.x[p]) == {a, x} and x not in old | {a}
    before = [r.copy() for r in z.x]
    exchange(z, p, x)
    assert z.x[x] == {p: 0, a: 1}
    assert x not in z.x[p]
    exchange(z, x, a)
    assert z.x[a] == {x: 0, p: 1} and z.x[x] == {p: 1}
    exchange(z, a, p)
    assert z.x[p] == {a: 0, x: 1}
    exchange(z, x, p)
    assert z.x[x] == {a: 0} and z.x[p] == {a: 0, x: 0}
    assert holders(z, a) == old | {x}
    assert all(z.x[v] == before[v] for v in range(z.n) if v not in {a, p, x})


def incoming(z, a, P, selected):
    I = holders(z, a)
    J = set(range(z.n)) - I - {a}
    assert I and J and z.x[a] == {}
    assert all(a not in z.x[v] for v in J)
    old_components = components(z, a, I)
    assert P in J and set(z.x[P]) & I
    assert z.x[P][selected] == max(z.x[P].values())
    frozen_P = z.x[P].copy()
    if selected in J:
        Q = next(v for v in z.x[P] if v in I)
        C = next(C for C in old_components if Q in C)
        normalize(z, a, C, Q)
        assert z.x[P] == frozen_P
        exchange(z, P, selected)
        assert set(z.x[selected]) == {P, Q} and z.x[selected][P] == 0
        exchange(z, selected, Q)
        assert z.x[selected] == {a: 0, P: 1}
        assert a not in z.x[P] and len(holders(z, a)) == len(I)
        outward(z, a, selected, P)
        branch = 'outside-oldest'
    else:
        assert selected in I
        Q = selected
        C = next(C for C in old_components if Q in C)
        normalize(z, a, C, Q)
        assert z.x[P] == frozen_P
        extra = set(z.x[P]) - {Q}
        exchange(z, P, Q)
        if not extra:
            assert holders(z, a) == I | {P}
            branch = 'singleton'
        else:
            X = next(iter(extra))
            assert holders(z, a) == (I - {Q}) | {P}
            assert set(z.x[P]) == {a, X} and z.x[P][a] == 0
            if X in J:
                outward(z, a, P, X)
                branch = 'outside-extra'
            elif len(C) >= 2:
                v = next(v for v in C if v != Q)
                assert z.x[v] == {a: 0, Q: 0}
                outward(z, a, v, Q)
                branch = 'nontrivial-root-component'
            else:
                assert X in I - {Q}
                assert z.x[a] == {}
                assert len(components(z, a, holders(z, a))) == len(old_components) - 1
                branch = 'component-decrease'
    if branch == 'component-decrease':
        assert len(holders(z, a)) == len(I)
    else:
        assert len(holders(z, a)) == len(I) + 1
    return branch


def shortest_outside_path(z, a, I):
    todo = [[a]]
    seen = {a}
    for path in todo:
        for q in z.x[path[-1]]:
            if q in seen:
                continue
            seen.add(q)
            pp = path + [q]
            if q not in I:
                return pp
            todo.append(pp)
    return None


def source_gain(z, a):
    """Execute the shortest-path controller against the actual age kernel."""
    old = holders(z, a)
    path = shortest_outside_path(z, a, old)
    assert path is not None
    start = z.steps
    while holders(z, a) == old:
        path = shortest_outside_path(z, a, old)
        assert path is not None
        distance = len(path) - 1
        first = path[1]
        phase = 0
        while holders(z, a) == old:
            q = max(z.x[a], key=lambda q: (z.x[a][q], -q))
            exchange(z, a, q)
            phase += 1
            assert old <= holders(z, a)
            if holders(z, a) != old:
                break
            new = shortest_outside_path(z, a, old)
            assert new is not None and len(new) <= distance + 1
            if len(new) < distance + 1:
                break
            assert first in z.x[a]
            assert phase <= z.n + 1
        assert phase <= z.n + 1
    assert z.steps - start <= (z.n - 1) * (z.n + 1)


def positive_copy_gain(z, a, p, q):
    """Check positive-copy exclusion, including k=0 with an empty owner."""
    old = holders(z, a)
    assert z.x[p].get(a, 0) > 0
    assert z.x[p][q] == max(z.x[p].values())
    if q == a:
        exchange(z, p, a)
        assert old <= holders(z, a) and p not in holders(z, a)
        assert p in z.x[a]
        source_gain(z, a)
    else:
        assert set(z.x[p]) == {a, q}
        exchange(z, p, q)
        if q in old:
            assert holders(z, a) == old | {p}
        else:
            assert set(z.x[q]) == {p, a}
            assert z.x[q][p] == 0 and z.x[q][a] > 0
            assert holders(z, a) == old
            exchange(z, q, a)
            assert q in z.x[a] and holders(z, a) == old
            source_gain(z, a)
    assert old < holders(z, a)


def rows(ids, ages=(0, 1)):
    for k in range(min(2, len(ids)) + 1):
        for chosen in combinations(ids, k):
            for aa in product(ages, repeat=k):
                yield dict(zip(chosen, aa))


def exhaustive(max_n, counts):
    states = witnesses = steps = 0
    for n in range(3, max_n + 1):
        a = 0
        for k in range(1, n - 1):
            for ii in combinations(range(1, n), k):
                I = set(ii)
                J = set(range(1, n)) - I
                options = [[]]
                for p in range(1, n):
                    if p in I:
                        options.append([{a: 0}] + [
                            {a: 0, q: t} for q in sorted(I - {p}) for t in (0, 1)
                        ])
                    else:
                        options.append(list(rows(sorted(set(range(1, n)) - {p}))))
                for caches in product(*options[1:]):
                    x = [{}] + list(caches)
                    candidates = [(P, u) for P in J if set(x[P]) & I
                                  for u in x[P] if x[P][u] == max(x[P].values())]
                    if not candidates:
                        continue
                    states += 1
                    for P, u in candidates:
                        z = Actual(x, 2)
                        branch = incoming(z, a, P, u)
                        counts[branch] = counts.get(branch, 0) + 1
                        witnesses += 1
                        steps += z.steps
    return states, witnesses, steps


def random_checks(max_n, seeds, counts):
    witnesses = steps = gadgets = 0
    for n in range(3, max_n + 1):
        for seed in range(seeds):
            rng = Random(1000003 * n + seed)
            for k in range(1, n - 1):
                labels = list(range(n))
                rng.shuffle(labels)
                a = labels[0]
                I = set(labels[1:k + 1])
                J = set(labels[k + 1:])
                x = [{} for _ in range(n)]
                for p in I:
                    x[p] = {a: 0}
                    candidates = sorted(I - {p})
                    if candidates and rng.randrange(4):
                        x[p][rng.choice(candidates)] = rng.randint(0, 1000000)
                for p in J:
                    candidates = sorted(set(range(n)) - {a, p})
                    x[p] = {q: rng.randint(0, 1000000) for q in rng.sample(candidates, min(2, len(candidates)))}
                P = rng.choice(sorted(J))
                Q = rng.choice(sorted(I))
                if Q not in x[P]:
                    del x[P][rng.choice(sorted(x[P]))]
                    x[P][Q] = rng.randint(0, 1000000)
                oldest = [q for q in x[P] if x[P][q] == max(x[P].values())]
                z = Actual(x, 2)
                branch = incoming(z, a, P, rng.choice(oldest))
                counts[branch] = counts.get(branch, 0) + 1
                witnesses += 1
                steps += z.steps
                # Independently test the outward gadget beyond extremal states:
                # a prospective new holder may have a positive a descriptor.
                other = [q for q in range(n) if q != a]
                p, v = rng.sample(other, 2)
                xx = [{} for _ in range(n)]
                xx[p] = {a: 0, v: rng.randint(0, 1000000)}
                pool = [q for q in range(n) if q != v]
                xx[v] = {q: rng.randint(1, 1000000) for q in rng.sample(pool, rng.randrange(3))}
                zz = Actual(xx, 2)
                outward(zz, a, p, v)
                gadgets += 1
                steps += zz.steps
    return witnesses, gadgets, steps


def auxiliary_checks(max_n, seeds):
    sources = positive = empty_zero = steps = 0
    for n in range(3, max_n + 1):
        for seed in range(seeds):
            rng = Random(7919 * n + seed)
            for sample in range(12):
                a = rng.randrange(n)
                # Start from an oriented spanning tree; extra random entries
                # give nontrivial oldest ages and preserve weak connectivity.
                x = [{} for _ in range(n)]
                order = list(range(n))
                rng.shuffle(order)
                for j in range(1, n):
                    p = order[j]
                    q = rng.choice(order[:j])
                    if rng.randrange(2) and len(x[q]) < 2:
                        p, q = q, p
                    x[p][q] = rng.choice((0, 1, rng.randint(0, 1000000)))
                for p in range(n):
                    pool = [q for q in range(n) if q != p and q not in x[p]]
                    rng.shuffle(pool)
                    for q in pool[:rng.randrange(3 - len(x[p]))]:
                        x[p][q] = rng.choice((0, 1, rng.randint(0, 1000000)))
                z = Actual(x, 2)
                if shortest_outside_path(z, a, holders(z, a)) is not None:
                    source_gain(z, a)
                    sources += 1
                    steps += z.steps
                pp = [p for p in range(n) if x[p].get(a, 0) > 0]
                if pp:
                    p = rng.choice(pp)
                    qq = [q for q in x[p] if x[p][q] == max(x[p].values())]
                    z = Actual(x, 2)
                    positive_copy_gain(z, a, p, rng.choice(qq))
                    positive += 1
                    steps += z.steps
                # Specifically exercise the ordering-sensitive k=0 case:
                # a is empty but is not isolated, because positive copies
                # point to it. No initial fresh a copy exists.
                xx = [{} for _ in range(n)]
                for p in range(n):
                    if p != a:
                        xx[p] = {a: rng.randint(1, 1000000)}
                        pool = [q for q in range(n) if q not in {p, a}]
                        if pool and rng.randrange(2):
                            xx[p][rng.choice(pool)] = rng.randint(0, 1000000)
                p = rng.choice([p for p in range(n) if p != a])
                q = max(xx[p], key=lambda q: (xx[p][q], -q))
                zz = Actual(xx, 2)
                assert not holders(zz, a) and zz.x[a] == {}
                positive_copy_gain(zz, a, p, q)
                empty_zero += 1
                steps += zz.steps
    return sources, positive, empty_zero, steps


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--exhaustive-n', type=int, default=5)
    ap.add_argument('--max-n', type=int, default=20)
    ap.add_argument('--seeds', type=int, default=4)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled; do not use python -O')
    counts = {}
    ex = exhaustive(args.exhaustive_n, counts)
    rr = random_checks(args.max_n, args.seeds, counts)
    aa = auxiliary_checks(args.max_n, args.seeds)
    print('PASS exhaustive_states/witnesses/exchanges', ex,
          'random_witnesses/outward_gadgets/exchanges', rr,
          'aux_source/positive/empty_owner_k0/exchanges', aa,
          'branches', counts)


if __name__ == '__main__':
    main()
