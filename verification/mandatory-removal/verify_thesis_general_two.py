#!/usr/bin/env python3
"""Exact colored/numerical-age controller for arbitrary-capacity ell=2.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_general_two.py

Initial conditions are an empty owner, age-zero copies at every current
holder, and one holder caching a nonholder. The controller must increase
the total identity-holder count. Only the current holder initiates until
a terminal underfull service or owner double callback. Every other holder
therefore remains a fixed, never-initiated initial zero holder.

The independent numeric kernel checks actual oldest partners, maximum
buffer sizes, protected victims and MIN ages. Proof-only colors initially
mark every descriptor OLD, fresh selves YOUNG, and merge by OR. Every
unfinished full-holder step checks that global YOUNG count cannot fall;
passive zero-holder contacts and OLD-partner migrations strictly raise it.
Colored supports, fixed passive-holder identities and predecessor facts
are checked after every step. Uniform finite-age resets are not invoked.

Default coverage runs all n=4,...,30, every c=3,...,n-1, varied anchor labels,
random holder sets/cache sizes and age patterns, plus adversarial disjoint
first replies. In particular, c<n/2 cases include full-to-full migrations
and repeated zero-age refreshes, which the earlier full-cache potential
cannot handle. --max-n 12 --seeds 2 gives a quick run. Finite checks
corroborate the arbitrary-size proof rather than replacing it.

Reproduced default coverage: 20,136 initializations and 74,801 exchanges;
16,443 OLD-partner migrations, 273 YOUNG-partner migrations, 3,106 strict
zero-holder resets, 8,227 owner finishes, 6,905 underfull finishes and
5,004 direct gains. Maximum trajectory20, migrations9, resets11, and
constant-F plateau length2. Numerical global-age maxima additionally check
the virtual-age inequalities used to exclude an infinite plateau.
"""
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_anchor import Actual
from verify_thesis_half_dense import holders


class Colored(Actual):
    def __init__(self, caches, c):
        super().__init__(caches, c)
        self.young = [set() for _ in caches]

    def F(self):
        return sum(map(len, self.young))

    def step(self, p, q, extra, reply, vp=None, vq=None):
        # Compute only colors here; the sibling kernel independently handles
        # identities, all numerical ages and exact legal transition choices.
        extra, reply = set(extra), set(reply)
        P, Q = set(self.x[p]), set(self.x[q])
        remaining = P - {q}
        out = {p} | extra
        dp = max(0, len(remaining) + len(reply - remaining - {p}) - self.c)
        dq = max(0, len(Q) + len(out - Q - {q}) - self.c)
        actual_vp = set(sorted(extra - reply)[:dp]) if vp is None else set(vp)
        actual_vq = set(sorted(reply - out)[:dq]) if vq is None else set(vq)
        yp, yq = self.young[p].copy(), self.young[q].copy()
        new_p = (yp - {q} - actual_vp) | (yq & reply - {p})
        new_q = (yq - actual_vq) | (((yp & extra) | {p}) - {q})
        super().step(p, q, extra, reply, actual_vp, actual_vq)
        self.young[p], self.young[q] = new_p, new_q
        assert all(ys <= set(cache) for ys, cache in zip(self.young, self.x))


def random_reply(z, q, rng):
    return rng.sample(sorted(z.x[q]), min(2, len(z.x[q])))


def holder_reply(z, p, q, a, rng, potential=False):
    Q, P = set(z.x[q]), set(z.x[p])
    assert a in Q
    if len(Q) == 1:
        return [a]
    if p in Q:
        return [a, p]
    if potential and len(Q) == z.c:
        candidates = Q - P
        assert candidates
        return [a, rng.choice(sorted(candidates))]
    return [a, rng.choice(sorted(Q - {a}))]


def nonholder_reply(z, p, q, rng):
    Q = set(z.x[q])
    size = min(2, len(Q))
    known = Q & (set(z.x[p]) | {p})
    if known:
        first = rng.choice(sorted(known))
        return [first] + rng.sample(sorted(Q - {first}), size - 1)
    return random_reply(z, q, rng)


def responder_victims(z, p, q, extra, reply):
    out = {p} | set(extra)
    needed = max(0, len(z.x[q]) + len(out - set(z.x[q]) - {q}) - z.c)
    eligible = set(reply) - out
    return sorted(eligible, key=lambda v: (z.x[q][v], v))[:needed]


def maxima(z):
    return [max((row.get(s, 0) for row in z.x), default=0) for s in range(z.n)]


def check_virtual_age_step(before, z, selected):
    after = maxima(z)
    assert all(v <= u + 1 for u, v in zip(before, after))
    assert after[selected] <= before[selected]


def underfull_finish(z, a, p, target, rng):
    H = len(holders(z, a))
    assert z.x[p][a] == 0 and len(z.x[p]) < z.c
    assert target in z.x[p] and target not in holders(z, a)
    start = z.steps
    while len(holders(z, a)) == H:
        others = set(z.x[p]) - {a}
        mx = max(z.x[p][v] for v in others)
        assert mx == max(z.x[p].values())
        q = rng.choice([v for v in others if z.x[p][v] == mx])
        if a in z.x[q]:
            reply = holder_reply(z, p, q, a, rng)
        else:
            reply = nonholder_reply(z, p, q, rng)
        victims = responder_victims(z, p, q, [a], reply)
        z.step(p, q, [a], reply, vq=victims)
        if len(holders(z, a)) == H:
            assert z.x[p][a] == 0 and len(z.x[p]) < z.c
            assert target in z.x[p]
        assert z.steps - start <= z.n + z.c
    assert len(holders(z, a)) == H + 1


def owner_target(z, a, target, rng):
    H = len(holders(z, a))
    assert target in z.x[a] and target not in holders(z, a)
    start = z.steps
    while len(holders(z, a)) == H:
        mx = max(z.x[a].values())
        q = rng.choice([v for v in z.x[a] if z.x[a][v] == mx])
        pool = sorted(set(z.x[a]) - {q})
        extra = [target] if q != target else rng.sample(pool, min(1, len(pool)))
        if a in z.x[q]:
            Q = set(z.x[q])
            reply = [a]
            if len(Q) >= 2:
                reply.append(target if target in Q else rng.choice(sorted(Q - {a})))
        else:
            reply = random_reply(z, q, rng)
        victims = responder_victims(z, a, q, extra, reply)
        z.step(a, q, extra, reply, vq=victims)
        if len(holders(z, a)) == H:
            assert target in z.x[a]
        assert z.steps - start <= z.n + z.c
    assert len(holders(z, a)) == H + 1


def owner_finish(z, a, p, predecessor, rng):
    H = len(holders(z, a))
    assert z.x[a] == {} and predecessor not in holders(z, a)
    assert predecessor in z.x[p]
    age = z.x[p][predecessor]
    z.step(p, a, [predecessor], [])
    assert z.x[a] == {p: 0, predecessor: age + 1}
    assert p not in holders(z, a) and len(holders(z, a)) == H - 1
    reply = random_reply(z, predecessor, rng)
    victims = responder_victims(z, a, predecessor, [p], reply)
    z.step(a, predecessor, [p], reply, vq=victims)
    assert len(holders(z, a)) == H and p in z.x[a]
    assert p not in holders(z, a)
    owner_target(z, a, p, rng)
    assert len(holders(z, a)) == H + 1


def control(z, a, active, rng, stats, limit=100000):
    initial_holders = holders(z, a)
    H = len(initial_holders)
    passive = initial_holders - {active}
    initial_target = next(v for v in z.x[active] if v not in initial_holders | {a})
    assert z.x[a] == {} and all(z.x[p][a] == 0 for p in initial_holders)
    predecessor = None
    migrations = resets = plateau = longest_plateau = 0
    while len(holders(z, a)) == H:
        assert z.steps < limit
        assert holders(z, a) == passive | {active}
        assert all(z.x[q][a] == 0 for q in passive)
        assert all(not (ys & (passive | {a})) for ys in z.young)
        target = predecessor if predecessor is not None else initial_target
        assert target in z.x[active] and target not in holders(z, a)
        if len(z.x[active]) < z.c and z.x[active][a] == 0:
            underfull_finish(z, a, active, target, rng)
            stats['underfull_finish'] = stats.get('underfull_finish', 0) + 1
            break
        P = z.x[active]
        if P[a] == 0:
            others = set(P) - {a}
            mx = max(P[v] for v in others)
            assert mx == max(P.values())
            candidates = [v for v in others if P[v] == mx]
        else:
            candidates = [v for v in P if P[v] == max(P.values())]
        q = a if a in candidates else rng.choice(candidates)
        if q == a:
            assert predecessor is not None
            owner_finish(z, a, active, predecessor, rng)
            stats['owner_finish'] = stats.get('owner_finish', 0) + 1
            break
        oldF = z.F()
        old_maxima = maxima(z)
        anchor_age = z.x[active][a]
        selected_young = q in z.young[active]
        if q in passive:
            assert not selected_young
            reply = holder_reply(z, active, q, a, rng, potential=True)
            victims = responder_victims(z, active, q, [a], reply)
            known_self = active in z.x[q]
            z.step(active, q, [a], reply, vq=victims)
            check_virtual_age_step(old_maxima, z, q)
            assert z.x[active][a] == 0
            assert holders(z, a) == passive | {active}
            resets += 1
            if len(z.x[active]) < z.c:
                underfull_finish(z, a, active, target, rng)
                stats['underfull_finish'] = stats.get('underfull_finish', 0) + 1
                break
            assert not known_self and z.F() >= oldF + 1
            stats['strict_zero_reset'] = stats.get('strict_zero_reset', 0) + 1
        else:
            assert a not in z.x[q]
            known = set(z.x[q]) & (set(P) | {active})
            reply = nonholder_reply(z, active, q, rng)
            victims = responder_victims(z, active, q, [a], reply)
            z.step(active, q, [a], reply, vq=victims)
            check_virtual_age_step(old_maxima, z, q)
            if len(holders(z, a)) == H + 1:
                stats['direct_gain'] = stats.get('direct_gain', 0) + 1
                break
            assert not known and len(z.x[active]) == z.c
            assert q not in z.x[active] and z.x[q][active] == 0
            assert z.x[q][a] > 0
            assert z.F() >= oldF + 1 - int(selected_young)
            stats['young_migration' if selected_young else 'old_migration'] = stats.get('young_migration' if selected_young else 'old_migration', 0) + 1
            predecessor, active = active, q
            migrations += 1
        assert z.F() >= oldF
        if z.F() == oldF:
            assert q not in passive and selected_young
            assert z.x[active][a] == anchor_age + 1
            plateau += 1
            longest_plateau = max(longest_plateau, plateau)
        else:
            plateau = 0
    assert len(holders(z, a)) == H + 1
    return migrations, resets, longest_plateau


def make_case(n, c, seed, forced, age):
    rng = Random(seed)
    labels = list(range(n))
    rng.shuffle(labels)
    a, p, q = labels[:3]
    I = {p} | set(rng.sample(labels[3:], rng.randrange(n - 2)))
    x = [{} for _ in range(n)]
    for v in range(n):
        if v == a:
            continue
        base = {a: 0} if v in I else {}
        pool = sorted(set(range(n)) - {a, v})
        if forced:
            count = min(c - len(base), len(pool))
        else:
            count = rng.randrange(min(c - len(base), len(pool)) + 1)
        x[v] = {**base, **{u: rng.choice((0, 1, 2, 1000000)) for u in rng.sample(pool, count)}}
    if forced:
        peers = [q] + rng.sample(sorted(set(range(n)) - {a, p, q}), c - 2)
        x[p] = {a: 0, **{v: rng.randint(0, 10) for v in peers}}
        x[p][q] = 1000001
        complement = sorted(set(range(n)) - set(x[p]) - {p})
        assert len(complement) >= 2
        chosen = rng.sample(complement, min(c, len(complement)))
        x[q] = {v: age for v in chosen}
    elif q not in x[p]:
        if len(x[p]) == c:
            del x[p][rng.choice(sorted(set(x[p]) - {a}))]
        x[p][q] = rng.randint(0, 1000000)
    return Colored(x, c), a, p, rng


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-n', type=int, default=30)
    ap.add_argument('--seeds', type=int, default=12)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled; do not use python -O')
    cases = exchanges = longest = max_migrations = max_resets = max_plateau = 0
    stats = {}
    for n in range(4, args.max_n + 1):
        for c in range(3, n):
            for seed in range(args.seeds):
                modes = [(False, 0)]
                if n - c - 1 >= 2:
                    modes += [(True, age) for age in (0, 1, 2, 1000000)]
                for forced, age in modes:
                    z, a, p, rng = make_case(n, c, 1000003*n+7919*c+seed, forced, age)
                    mm, rr, pp = control(z, a, p, rng, stats)
                    cases += 1
                    exchanges += z.steps
                    longest = max(longest, z.steps)
                    max_migrations = max(max_migrations, mm)
                    max_resets = max(max_resets, rr)
                    max_plateau = max(max_plateau, pp)
    print('PASS cases/exchanges/worst/migrations/resets/plateau',
          (cases, exchanges, longest, max_migrations, max_resets, max_plateau),
          'branches', stats)


if __name__ == '__main__':
    main()
