#!/usr/bin/env python3
"""Exact checks of conditional cooperative owner service for ell=3.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_cooperative_owner.py

Every old zero-holder stores two reserved anchors a^0,p^0. Owner a caches
p, which is not a zero holder. The first suite keeps residual IDs within I.
The stronger second suite allows arbitrary outside IDs. Before each owner
contact with I, the actual oldest responder's residual cache runs an exact
ell=1, capacity c-2 clearing path until it is empty OR selects an outside
ID r. The owner then receives a,p (and r if present), deletes that I head,
and acquires at most one outside head. The trajectory ends at a new age-zero
a holder. Other positive-age a holders remain frozen until terminal.

The actual ell=3 age kernel and the residual ell=1 kernel are evaluated
independently and compared after every residual exchange. Every maximum
buffer size, oldest choice, received-ID protection, legal sent victim,
minimum-age merge, frozen cache, and claimed path bound is asserted.
Default cases cover n=4,...,30, every c=3,...,n-1, ten reproducible seeds,
arbitrary anchor labels, residual ages0 and up to1,000,000, small I sets,
and effective residual capacities larger than the available ID population.
--max-n 12 --seeds 2 gives a quick run. These finite checks corroborate the
conditional lemma; they do not establish its hypotheses from general states.

Reproduced default run: 15,120 initializations, 647,065 actual exchanges,
including 569,366 independent residual embeddings and 77,699 owner
exchanges; maximum trajectory666. There are 7,911 terminal target contacts
and 7,209 terminal other-nonzero contacts, plus 9,011 cases that exercise
the last internal-contact/closure boundary.
The stronger arbitrary-residual suite adds 15,120 cases and 186,403
exchanges: 130,525 residual embeddings and 55,878 owner exchanges, with
27,535 boundary blocks and 13,223 empty blocks. Maximum trajectory666;
3,773 terminal target contacts and 11,347 other nonzero terminals.
"""
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_singleton_general import ControlledCyclon


class ActualThree:
    def __init__(self, caches, c, ell=3):
        self.x = [dict(row) for row in caches]
        self.c, self.n = c, len(caches)
        self.ell = ell
        self.steps = self.residual_steps = self.owner_steps = 0

    def step(self, p, q, extra, reply, vp=None, vq=None):
        P = {v: t + 1 for v, t in self.x[p].items()}
        Q = self.x[q].copy()
        extra, reply = set(extra), set(reply)
        assert q in P and P[q] == max(P.values())
        assert len(extra) == min(self.ell - 1, len(P) - 1) and extra <= set(P) - {q}
        assert len(reply) == min(self.ell, len(Q)) and reply <= set(Q)
        incoming = {v: Q[v] for v in reply}
        outgoing = {p: 0, **{v: P[v] for v in extra}}
        del P[q]
        ip, iq = set(incoming) - set(P) - {p}, set(outgoing) - set(Q) - {q}
        dp, dq = max(0, len(P) + len(ip) - self.c), max(0, len(Q) + len(iq) - self.c)
        ep, eq = extra - set(incoming), reply - set(outgoing)
        vp = set(sorted(ep)[:dp]) if vp is None else set(vp)
        vq = set(sorted(eq)[:dq]) if vq is None else set(vq)
        assert len(vp) == dp and vp <= ep and len(vq) == dq and vq <= eq
        A, B = {v: t for v, t in P.items() if v not in vp}, {v: t for v, t in Q.items() if v not in vq}
        for v, t in incoming.items():
            if v != p:
                A[v] = min(A.get(v, t), t)
        for v, t in outgoing.items():
            if v != q:
                B[v] = min(B.get(v, t), t)
        self.x[p], self.x[q] = A, B
        self.steps += 1
        assert all(v not in row and len(row) <= self.c for v, row in enumerate(self.x))


def zeros(z, a):
    return {v for v in range(z.n) if v != a and z.x[v].get(a) == 0}


def holder_count(z, a):
    return sum(a in row for row in z.x)


class Residual(ControlledCyclon):
    def __init__(self, actual, a, target, I, anchor_ages=None):
        self.actual, self.a, self.target = actual, a, target
        self.targets = set(target) if isinstance(target, (tuple, list, set)) else {target}
        self.anchors = {a} | self.targets
        self.anchor_ages = dict.fromkeys(self.anchors, 0) if anchor_ages is None else dict(anchor_ages)
        assert set(self.anchor_ages) == self.anchors
        self.I = set(I)
        self.labels = [v for v in range(actual.n) if v not in self.anchors]
        self.inv = {v: i for i, v in enumerate(self.labels)}
        rows = [{self.inv[v]: age for v, age in actual.x[p].items() if v not in self.anchors} if p in I else {} for p in self.labels]
        super().__init__(rows, actual.c - len(self.anchors))
        self.active_population = len(I)

    def activate(self, initiator, policy=None, partner=None, reply=None):
        p = self.labels[initiator]
        before = [row.copy() for row in self.actual.x]
        P = self.caches[initiator]
        for v in P:
            P[v] += 1
        mx = max(P.values())
        q = min(v for v in P if P[v] == mx) if partner is None else partner
        assert P[q] == mx
        assert p in self.I and self.labels[q] in self.I
        Q = self.caches[q]
        t = initiator if initiator in Q else min(Q, default=None)
        if reply is not None:
            t = reply
        assert t is None if not Q else t in Q
        age = Q.get(t)
        del P[q]
        if t is not None and t != initiator:
            P[t] = min(P.get(t, age), age)
        victims = []
        if initiator in Q:
            Q[initiator] = 0
        else:
            if len(Q) == self.capacity:
                assert t is not None
                del Q[t]
                victims = [self.labels[t]]
            Q[initiator] = 0
        packet = sorted(self.anchors) + ([] if t is None else [self.labels[t]])
        self.actual.step(p, self.labels[q], sorted(self.anchors), packet, [], victims)
        self.activations += 1
        self.actual.residual_steps += 1
        for i, v in enumerate(self.labels):
            if v not in self.I:
                continue
            expected = {**self.anchor_ages, **{self.labels[u]: age for u, age in self.caches[i].items()}}
            assert self.actual.x[v] == expected
        assert all(self.actual.x[v] == before[v] for v in range(self.actual.n) if v not in self.I)


def construct(z, a, target, I, rng, counts):
    I = set(I)
    assert I and zeros(z, a) == I and target not in I | {a}
    assert target in z.x[a]
    assert all(z.x[v].get(target) == 0 and set(z.x[v]) - {a, target} <= I for v in I)
    original = [row.copy() for row in z.x]
    H = holder_count(z, a)
    initial_owner_size = len(z.x[a])
    internal = 0
    while True:
        assert target in z.x[a]
        mx = max(z.x[a].values())
        q = rng.choice([v for v in z.x[a] if z.x[a][v] == mx])
        if q not in I:
            pool = sorted(set(z.x[a]) - {q})
            extra = rng.sample(pool, min(2, len(pool)))
            reply = rng.sample(sorted(z.x[q]), min(3, len(z.x[q])))
            z.step(a, q, extra, reply)
            z.owner_steps += 1
            assert zeros(z, a) == I | {q}
            assert holder_count(z, a) >= H
            assert all(z.x[v] == original[v] for v in range(z.n) if v not in I | {a, q})
            counts['terminal_target' if q == target else 'terminal_other'] = counts.get('terminal_target' if q == target else 'terminal_other', 0) + 1
            break
        owner_before = z.x[a].copy()
        oracle = Residual(z, a, target, I)
        oracle.clear(oracle.inv[q])
        assert z.x[a] == owner_before and z.x[q] == {a: 0, target: 0}
        assert zeros(z, a) == I and holder_count(z, a) == H
        R = sorted((set(z.x[a]) - {q, target}) & I)
        extra = [target]
        if len(z.x[a]) >= 3:
            extra.append(rng.choice(R) if R else rng.choice(sorted(set(z.x[a]) - {q, target})))
        old_size = len(z.x[a])
        z.step(a, q, extra, [a, target], [], [])
        z.owner_steps += 1
        internal += 1
        assert len(z.x[a]) == old_size - 1 and target in z.x[a]
        assert zeros(z, a) == I and holder_count(z, a) == H
        assert all(z.x[v].get(target) == 0 for v in I)
        if R:
            assert all(set(z.x[v]) - {a, target} <= I for v in I)
        else:
            assert not (set(z.x[a]) & I)
            counts['last_internal'] = counts.get('last_internal', 0) + 1
        assert internal <= initial_owner_size - 1
    assert z.owner_steps <= initial_owner_size <= z.c
    assert z.steps <= (initial_owner_size - 1) * (len(I) + z.c - 3) + initial_owner_size


def construct_open(z, a, target, I, rng, counts):
    I = set(I)
    assert I and zeros(z, a) == I and target not in I | {a}
    assert target in z.x[a]
    assert all(z.x[v].get(target) == 0 for v in I)
    original = [row.copy() for row in z.x]
    H = holder_count(z, a)
    initial_heads = len(set(z.x[a]) & I)
    blocks = 0
    while True:
        assert target in z.x[a]
        mx = max(z.x[a].values())
        q = rng.choice([v for v in z.x[a] if z.x[a][v] == mx])
        if q not in I:
            pool = sorted(set(z.x[a]) - {q})
            extra = rng.sample(pool, min(2, len(pool)))
            reply = rng.sample(sorted(z.x[q]), min(3, len(z.x[q])))
            z.step(a, q, extra, reply)
            z.owner_steps += 1
            assert zeros(z, a) == I | {q} and holder_count(z, a) >= H
            assert all(z.x[v] == original[v] for v in range(z.n) if v not in I | {a, q})
            key = 'terminal_target' if q == target else 'terminal_other'
            counts[key] = counts.get(key, 0) + 1
            break
        owner_before = z.x[a].copy()
        oracle = Residual(z, a, target, I)
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
            assert residual_events <= len(I) + z.c - 3
        assert z.x[a] == owner_before
        assert zeros(z, a) == I and holder_count(z, a) == H
        reply = [a, target]
        if boundary is None:
            assert z.x[q] == {a: 0, target: 0}
            counts['empty_blocks'] = counts.get('empty_blocks', 0) + 1
        else:
            assert boundary in z.x[q] and boundary not in I | {a, target}
            reply.append(boundary)
            counts['boundary_blocks'] = counts.get('boundary_blocks', 0) + 1
        extra = [target]
        if len(z.x[a]) >= 3:
            extra.append(rng.choice(sorted(set(z.x[a]) - {q, target})))
        old_size = len(z.x[a])
        old_heads = len(set(z.x[a]) & I)
        z.step(a, q, extra, reply)
        z.owner_steps += 1
        blocks += 1
        assert len(z.x[a]) <= old_size and target in z.x[a]
        assert len(set(z.x[a]) & I) == old_heads - 1
        assert zeros(z, a) == I and holder_count(z, a) == H
        assert all(z.x[v].get(target) == 0 for v in I)
        assert blocks <= initial_heads
    assert z.owner_steps <= initial_heads + 1 <= z.c
    assert z.steps <= initial_heads * (len(I) + z.c - 3) + initial_heads + 1


def trial(n, c, seed, age, targeted, counts, open_residual=False):
    rng = Random(seed)
    order = list(range(n))
    rng.shuffle(order)
    a, target = order[:2]
    I = set(rng.sample(order[2:], rng.randint(1, n - 2)))
    x = [{} for _ in range(n)]
    for v in range(n):
        if v in I:
            pool = sorted((set(range(n)) - {a, target, v}) if open_residual else I - {v})
            chosen = rng.sample(pool, rng.randrange(min(c - 2, len(pool)) + 1))
            x[v] = {a: 0, target: 0, **{q: rng.randint(0, age) for q in chosen}}
        elif v != a:
            pool = sorted(set(range(n)) - {v})
            chosen = rng.sample(pool, rng.randrange(min(c, len(pool)) + 1))
            x[v] = {q: rng.randint(1 if q == a else 0, age + 1) for q in chosen}
    if targeted:
        chosen_I = rng.sample(sorted(I), min(c - 1, len(I)))
        other = sorted(set(range(n)) - I - {a, target})
        chosen_other = rng.sample(other, rng.randrange(min(c - 1 - len(chosen_I), len(other)) + 1))
        x[a] = {target: 0, **{v: rng.randint(1, age + 1) for v in chosen_I}, **{v: 0 for v in chosen_other}}
    else:
        pool = sorted(set(range(n)) - {a, target})
        chosen = rng.sample(pool, rng.randrange(min(c - 1, len(pool)) + 1))
        x[a] = {target: rng.randint(0, age), **{v: rng.randint(0, age) for v in chosen}}
    z = ActualThree(x, c)
    (construct_open if open_residual else construct)(z, a, target, I, rng, counts)
    return z


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-n', type=int, default=30)
    ap.add_argument('--seeds', type=int, default=10)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled; do not use python -O')
    for open_residual in (False, True):
        cases = exchanges = residual = owner = longest = 0
        counts = {}
        for n in range(4, args.max_n + 1):
            for c in range(3, n):
                for seed in range(args.seeds):
                    for age in (0, 1000000):
                        for targeted in (False, True):
                            z = trial(n, c, 1000003*n+7919*c+seed, age, targeted, counts, open_residual)
                            cases += 1
                            exchanges += z.steps
                            residual += z.residual_steps
                            owner += z.owner_steps
                            longest = max(longest, z.steps)
        print('PASS', 'arbitrary-residual' if open_residual else 'closed-residual',
              'cases/exchanges/residual/owner/longest',
              (cases, exchanges, residual, owner, longest), 'branches', counts)


if __name__ == '__main__':
    main()
