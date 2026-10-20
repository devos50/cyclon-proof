#!/usr/bin/env python3
"""Exact dense-capacity ell=3 cooperative owner-target service checks.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_dense_three_owner.py

For c>=n-2, owner a caches a nonzero-a target p, while every old zero
holder is otherwise arbitrary. The controller prepares the owner's actual
oldest zero holder Q using Q-only contacts, or temporarily lets Q contact p
and restores Q by the frozen owner's promised contact. It asserts exact
target-age growth per owner event, every macro-global maximum inequality,
and zero preservation at macro endpoints. Preparation can temporarily lose
Q's zero in the Q->p branch, which is explicitly restored by a->Q.

This is an executable audit of a proposed structural lemma, not a finite
enumeration proof or a new convergence claim.

Reproduced default result: 18,400 initializations through n=15 at both
dense capacities, 117,946 exact exchanges, longest trajectory 39.
Branches: 30,950 internal preparations; 27,952 sacrifice/restore events;
40,510 nonfinishing macro boundaries; 94 two-target exits followed by
134 finishing service exchanges. Mixed anchor/residual ages reach 10^6.

The second suite removes the density condition when c>=4 and exactly one
peer p lacks the owner's zero. No second outside residual can occur. The
Q-only internal request has at most two usable replies (a is duplicate),
which fit its vacancies; Q->p explicitly protects a, and the owner event
explicitly protects p. This suite covers every 4<=c<=n-1 through n=20:
27,200 cases, 350,417 exchanges, longest trajectory 52; 120,506 internal
preparations, 94,201 sacrifice/restores and 108,510 macro boundaries.
It assumes that the owner initially caches p, and establishes no general
bootstrap of that premise from arbitrary intermediate zero sets.
"""
from pathlib import Path
from random import Random
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros, holder_count


class TrackedActual(ActualThree):
    def step(self, p, q, extra, reply, vp=None, vq=None):
        owner = getattr(self, 'tracking_owner', None)
        count = holder_count(self, owner) if owner is not None else None
        super().step(p, q, extra, reply, vp, vq)
        if owner is not None:
            assert holder_count(self, owner) >= count


class DenseActual(TrackedActual):
    def step(self, p, q, extra, reply, vp=None, vq=None):
        retained = set(self.x[p]) - {q}
        super().step(p, q, extra, reply, vp, vq)
        assert retained <= set(self.x[p])


def maxima(z):
    return [max((row.get(s, 0) for row in z.x), default=0) for s in range(z.n)]


def oldest(row, rng, prefer=None):
    top = max(row.values())
    choices = sorted(v for v, age in row.items() if age == top)
    good = [v for v in choices if prefer is not None and prefer(v)]
    return rng.choice(good or choices)


def reply_with(z, q, required, rng):
    required = set(required)
    assert required <= set(z.x[q])
    size = min(3, len(z.x[q]))
    assert len(required) <= size
    return sorted(required | set(rng.sample(sorted(set(z.x[q]) - required), size - len(required))))


def preserving_step(z, p, q, extra, reply, keep):
    remaining = set(z.x[p]) - {q}
    usable = set(reply) - remaining - {p}
    needed = max(0, len(remaining) + len(usable) - z.c)
    available = set(extra) - set(reply) - set(keep)
    assert len(available) >= needed
    z.step(p, q, extra, reply, vp=sorted(available)[:needed])
    assert set(keep) <= set(z.x[p])


def owner_step(z, a, q, p, reply, rng):
    size = min(2, len(z.x[a]) - 1)
    extras = [p] if p != q else []
    extras += rng.sample(sorted(set(z.x[a]) - {q} - set(extras)), size - len(extras))
    preserving_step(z, a, q, extras, reply, {p} if p != q else set())
    z.owner_steps += 1


def two_targets(z, a, I, targets, rng, counts):
    targets = set(targets)
    assert len(targets) == 2 and targets <= set(z.x[a]) and not targets & I
    seen = set()
    events = 0
    while True:
        q = oldest(z.x[a], rng, lambda r: r not in I)
        if q not in I:
            reply = rng.sample(sorted(z.x[q]), min(3, len(z.x[q])))
            z.step(a, q, sorted(targets - {q}) + rng.sample(sorted(set(z.x[a]) - {q} - targets), min(2, len(z.x[a]) - 1) - len(targets - {q})), reply)
            events += 1
            assert zeros(z, a) == I | {q}
            break
        reply = reply_with(z, q, {a} | (targets if q in seen else set()), rng)
        z.step(a, q, sorted(targets), reply)
        assert {a} | targets <= set(z.x[q])
        assert zeros(z, a) == I
        seen.add(q)
        events += 1
        assert events <= z.c + 2 * (z.n - 3)
    counts['two_target_events'] = counts.get('two_target_events', 0) + events


def construct(z, a, p, rng, counts, near_complete=False):
    assert z.ell == 3 and z.c >= 3
    assert z.c >= z.n - 2 or (near_complete and z.c >= 4)
    z.tracking_owner = a
    I = zeros(z, a)
    if near_complete:
        assert I == set(range(z.n)) - {a, p}
    H = holder_count(z, a)
    A = z.x[a][p]
    initial_max = maxima(z)
    budget = sum(max(0, initial_max[s] - A + 1) for s in I)
    selections = dict.fromkeys(I, 0)
    owner_events = 0
    while True:
        q = oldest(z.x[a], rng, lambda r: r not in I)
        if q not in I:
            owner_step(z, a, q, p, rng.sample(sorted(z.x[q]), min(3, len(z.x[q]))), rng)
            assert zeros(z, a) == I | {q} and holder_count(z, a) >= H
            counts['direct_gain'] = counts.get('direct_gain', 0) + 1
            break
        before = maxima(z)
        owner_before = z.x[a].copy()
        assert z.x[a][p] == A + owner_events
        assert before[q] - owner_events >= A
        prep = 0
        two = None
        while p in z.x[q] and len(z.x[q]) <= 3:
            residual = set(z.x[q]) - {a, p}
            assert len(residual) <= 1
            r = next(iter(residual), None)
            if r is not None and r not in I:
                assert not near_complete
                owner_step(z, a, q, p, sorted(z.x[q]), rng)
                two = {p, r}
                counts['two_target_branch'] = counts.get('two_target_branch', 0) + 1
                break
            if r is not None and z.x[q][r] >= z.x[q][p]:
                # Here a^0 cannot be older than r, so r is an actual oldest.
                required = {a} | ({p} if p in z.x[r] else set()) | ({q} if q in z.x[r] else set())
                reply = reply_with(z, r, required, rng)
                prep_max = maxima(z)
                preserving_step(z, q, r, [a, p], reply, {a, p})
                assert z.x[a] == owner_before
                assert zeros(z, a) == I
                assert all(maxima(z)[s] <= prep_max[s] for s in range(z.n) if s not in {a, p})
                assert {a, p, q} <= set(z.x[r]) and z.x[r][a] == 0
                prep += 1
                counts['internal_prep'] = counts.get('internal_prep', 0) + 1
                assert prep <= len(I)
                continue
            assert p in z.x[q] and z.x[q][p] == max(z.x[q].values())
            extra = sorted(set(z.x[q]) - {p})
            reply = rng.sample(sorted(z.x[p]), min(3, len(z.x[p])))
            preserving_step(z, q, p, extra, reply, {a})
            assert a in z.x[q] and p not in z.x[q]
            assert zeros(z, a) == I - {q}
            assert z.x[a] == owner_before
            counts['sacrifice_restore'] = counts.get('sacrifice_restore', 0) + 1
            break
        if two is not None:
            assert zeros(z, a) == I and holder_count(z, a) >= H
            two_targets(z, a, I, two, rng, counts)
            assert holder_count(z, a) >= H
            break
        reply = reply_with(z, q, {a}, rng)
        if p in reply:
            candidates = sorted(set(z.x[q]) - {p})
            assert len(candidates) >= min(3, len(z.x[q]))
            reply = [a] + rng.sample(sorted(set(candidates) - {a}), min(3, len(z.x[q])) - 1)
        assert p not in reply
        owner_step(z, a, q, p, reply, rng)
        owner_events += 1
        selections[q] += 1
        after = maxima(z)
        assert all(after[s] <= before[s] + 1 for s in range(z.n) if s not in {a, p})
        assert after[q] <= before[q]
        assert z.x[a][p] == A + owner_events
        assert zeros(z, a) == I and holder_count(z, a) >= H
        assert owner_events <= budget
        assert selections[q] <= max(0, initial_max[q] - A + 1)
        counts['macro_events'] = counts.get('macro_events', 0) + 1
    return owner_events


def trial(n, c, seed, offset, counts):
    rng = Random(seed)
    order = list(range(n))
    rng.shuffle(order)
    a, p = order[:2]
    I = set(rng.sample(order[2:], rng.randint(0, n - 2)))
    x = [{} for _ in range(n)]
    for q in range(n):
        pool = sorted(set(range(n)) - {q, a}) if q in I else sorted(set(range(n)) - {q})
        maxsize = c - (q in I)
        size = rng.randrange(min(maxsize, len(pool)) + 1)
        x[q] = {r: offset + rng.randrange(7) for r in rng.sample(pool, size)}
        if q in I:
            x[q][a] = 0
        elif a in x[q]:
            x[q][a] = max(1, x[q][a])
    x[a][p] = offset
    if len(x[a]) > c:
        del x[a][next(q for q in x[a] if q != p)]
    z = DenseActual(x, c, 3)
    construct(z, a, p, rng, counts)
    return z


def targeted(n, c, seed, offset, counts, near_complete=False):
    rng = Random(seed)
    a, p = 0, 1
    I = set(range(2, n))
    x = [{}, {}] + [{a: 0} for _ in I]
    for q in I:
        m = rng.choice([0, 1, 2, offset, offset + 2])
        x[q][p] = m
        if rng.randrange(5):
            r = rng.choice(sorted(I - {q}))
            x[q][r] = rng.choice([0, 1, 2, m, m + 1, offset + 4])
    x[a] = {p: offset}
    heads = rng.sample(sorted(I), rng.randint(1, min(c - 1, len(I))))
    x[a].update({q: offset + rng.randint(1, 4) for q in heads})
    size = rng.randrange(c + 1)
    x[p] = {q: rng.choice([0, 1, 2, offset, offset + 4]) for q in rng.sample(sorted(set(range(n)) - {p}), size)}
    if a in x[p]:
        x[p][a] = max(1, x[p][a])
    z = TrackedActual(x, c, 3) if near_complete else DenseActual(x, c, 3)
    construct(z, a, p, rng, counts, near_complete=near_complete)
    return z


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--max-n', type=int, default=15)
    ap.add_argument('--seeds', type=int, default=200)
    ap.add_argument('--nearcomplete-max-n', type=int, default=20)
    args = ap.parse_args()
    if not __debug__:
        ap.error('assertions must be enabled')
    cases = steps = longest = 0
    counts = {}
    for n in range(4, args.max_n + 1):
        for c in range(max(3, n - 2), n):
            for seed in range(args.seeds):
                for offset in (0, 1000000):
                    z = trial(n, c, 1000003*n+7919*c+seed, offset, counts)
                    cases += 1
                    steps += z.steps
                    longest = max(longest, z.steps)
                    z = targeted(n, c, 1000003*n+7919*c+seed, offset, counts)
                    cases += 1
                    steps += z.steps
                    longest = max(longest, z.steps)
    print('PASS cases/exchanges/longest', (cases, steps, longest), 'branches', counts)
    cases = steps = longest = 0
    counts = {}
    for n in range(5, args.nearcomplete_max_n + 1):
        for c in range(4, n):
            for seed in range(max(1, args.seeds // 2)):
                for offset in (0, 1000000):
                    z = targeted(n, c, 1000003*n+7919*c+seed, offset, counts, near_complete=True)
                    cases += 1
                    steps += z.steps
                    longest = max(longest, z.steps)
    print('PASS proper near-complete cases/exchanges/longest', (cases, steps, longest), 'branches', counts)


if __name__ == '__main__':
    main()
