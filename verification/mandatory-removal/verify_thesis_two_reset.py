#!/usr/bin/env python3
"""Verify the shuffle-two age-gap reset with received-ID protection and MIN ages.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_two_reset.py

The default checks every capacity 2,...,n-1 for n=3,...,20, with
seeds 0,...,9 and four nonvacuous age patterns. Ages are scaled by the
symbolic reset length L, rather than kept below L: every initialization
has both OLD and YOUNG entries separated by an empty age interval of
length L. The patterns include close OLD ages, OLD ages up to 10^12 L,
and many occupied age bands before the first gap. Topologies include
full, empty, and underfull caches and need not be connected. The default
run passes 6,840 nonvacuous states, with 12,508 forced migrations,
12,056 OLD/OLD younger refreshes, 96,752 OLD/YOUNG refreshes,
33,222 tracked conversion stops, and 14,737 callback conversion stops.
Its longest trajectory takes 188 exchanges (n=20, c=19, seed=9,
close-age pattern).

Every step checks mandatory oldest selection, exact buffer sizes,
received-ID-protected victim eligibility, MIN duplicate merges, the
age/color barrier, immune holders, nondecreasing YOUNG count in routing,
strict gains at forced migrations, and all symbolic event bounds.
It checks complete OLD-color erasure and the final age bound, including
arbitrary padding to L. Initial YOUNG lineages need not be erased.

This reproducible finite/random check supports the symbolic proof; it
is not an exhaustive proof for arbitrary population sizes or ages.
Requires only Python. Assertions must remain enabled (do not use -O).
"""
import argparse
from random import Random


class Chain:
    def __init__(self, n, capacity, seed, pattern):
        self.n = n
        self.c = capacity
        self.rng = Random(seed)
        self.t = 0
        self.K = 2 * n + capacity
        self.L = n * (n - 1) * (n * capacity + 2) * self.K
        self.migrations = 0
        self.old_old_refreshes = 0
        self.mixed_refreshes = 0
        self.tracked_refresh_stops = 0
        self.callback_refresh_stops = 0
        self.max_route = 0
        self.max_segment = 0
        self.max_callback = 0
        self.x = []
        for p in range(n):
            ids = [q for q in range(n) if q != p]
            self.rng.shuffle(ids)
            size = capacity if pattern == 'close' else self.rng.randrange(capacity + 1)
            self.x.append({q: (0, False) for q in ids[:size]})
        # Guarantee two stored descriptors so every test has both colors.
        for p, q in ((0, 1), (1, 0)):
            if q not in self.x[p] and len(self.x[p]) == capacity:
                self.x[p].pop(next(iter(self.x[p])))
            self.x[p].setdefault(q, (0, False))
        slots = [(p, q) for p, cc in enumerate(self.x) for q in cc]
        self.rng.shuffle(slots)
        ages = []
        if pattern == 'staircase':
            k = max(1, len(slots) // 2)
            for j in range(len(slots)):
                if j < k:
                    ages.append(j * self.L + self.rng.randint(1, self.L))
                else:
                    ages.append((k + 1) * self.L + self.rng.randint(1, 10 * self.L))
        else:
            for j in range(len(slots)):
                young = j == 0 or (j != 1 and self.rng.randrange(2) == 0)
                if young:
                    ages.append(self.rng.randrange(self.L + 1))
                elif pattern == 'close':
                    ages.append(2 * self.L + self.rng.randint(1, 10))
                elif pattern == 'huge':
                    ages.append(2 * self.L + self.rng.randint(1, 10**12) * self.L)
                else:
                    ages.append(2 * self.L + self.rng.randint(1, 20 * self.L))
            ages[0] = self.L  # Occupy the first band; the next band is empty.
        for (p, q), age in zip(slots, ages):
            self.x[p][q] = (age, False)
        occupied = {(age - 1) // self.L for age in ages if age > 0}
        gap = next(j for j in range(n * capacity + 1) if j not in occupied)
        self.a = gap * self.L
        self.threshold = self.a + self.L
        self.x = [{q: (age, age > self.threshold) for q, (age, _) in cc.items()}
                  for cc in self.x]
        assert any(old for cc in self.x for age, old in cc.values())
        assert any(not old for cc in self.x for age, old in cc.values())
        self.barrier()

    def pick(self, values, count):
        values = list(values)
        assert 0 <= count <= len(values)
        self.rng.shuffle(values)
        return values[:count]

    def young_count(self):
        return sum(not old for cc in self.x for age, old in cc.values())

    def barrier(self):
        assert self.t <= self.L
        for p, cc in enumerate(self.x):
            assert p not in cc and len(cc) <= self.c
            for age, old in cc.values():
                assert age > self.threshold if old else age <= self.a + self.t

    def merge(self, resident, incoming):
        if incoming[0] < resident[0]:
            if resident[1] and incoming[1]:
                self.old_old_refreshes += 1
            if resident[1] and not incoming[1]:
                self.mixed_refreshes += 1
            return incoming
        if resident[0] == incoming[0]:
            # The gap makes mixed-color equal-age merges impossible.
            assert resident[1] == incoming[1]
        return resident

    def step(self, p, target, immune, outer_r, routing=False):
        self.barrier()
        P = self.x[p]
        Qold = max(v[0] for v in P.values())
        q = self.pick([z for z in P if P[z][0] == Qold], 1)[0]
        Q = self.x[q]
        assert target in P
        if routing:
            assert P[target][1]
        if q == target:
            S = self.pick([z for z in P if z != q], min(1, len(P) - 1))
            out = {p: (0, False), **{z: (P[z][0] + 1, P[z][1]) for z in S}}
            J = {z: v for z, v in out.items() if z != q and z not in Q}
            rq = max(0, len(Q) + len(J) - self.c)
            victimsQ = self.pick([z for z in Q if z not in out], rq)
            T = victimsQ + self.pick([z for z in Q if z not in victimsQ],
                                     min(2, len(Q)) - rq)
        else:
            S = [target]
            out = {p: (0, False), target: (P[target][0] + 1, P[target][1])}
            J = {z: v for z, v in out.items() if z not in Q}
            rq = max(0, len(Q) + len(J) - self.c)
            known = [z for z in (p, target) if z in Q]
            if len(known) == 2:
                T = [p, target]
                victimsQ = []
                assert rq == 0
            elif len(known) == 1:
                sentinel = known[0]
                candidates = [z for z in Q if z != sentinel]
                if rq:
                    assert rq == 1
                    if routing:
                        candidates = [z for z in candidates
                                      if Q[z][1] or (z not in P and z != p)]
                    victim = self.pick(candidates, 1)[0]
                    T = [sentinel, victim]
                    victimsQ = [victim]
                else:
                    T = [sentinel] + self.pick(candidates, min(2, len(Q)) - 1)
                    victimsQ = []
            else:
                candidates = list(Q)
                if routing:
                    candidates = [z for z in candidates
                                  if Q[z][1] or (z not in P and z != p)]
                victimsQ = self.pick(candidates, rq)
                T = victimsQ + self.pick([z for z in Q if z not in victimsQ],
                                         min(2, len(Q)) - rq)
        assert len(S) == min(1, len(P) - 1)
        assert len(T) == min(2, len(Q)) and len(set(T)) == len(T)
        reply = {z: Q[z] for z in T if z != p}
        rem = {z: (v[0] + 1, v[1]) for z, v in P.items() if z != q}
        I = {z: v for z, v in reply.items() if z not in rem}
        rp = max(0, len(rem) + len(I) - self.c)
        eligibleP = [z for z in S if z not in reply]
        eligibleQ = [z for z in T if z not in out]
        assert set(victimsQ) <= set(eligibleQ)
        assert len(victimsQ) == max(0, len(Q) + len(J) - self.c)
        victimsP = self.pick(eligibleP, rp)
        forced = target in victimsP
        before = self.young_count()
        if routing and q != target:
            assert P[q][1], ('barrier failure', p, q, target, P)
        newP = {z: v for z, v in rem.items() if z not in victimsP}
        for z, value in reply.items():
            newP[z] = self.merge(newP[z], value) if z in newP else value
        newQ = {z: v for z, v in Q.items() if z not in victimsQ}
        for z, value in out.items():
            if z == q:
                continue
            newQ[z] = self.merge(newQ[z], value) if z in newQ else value
        self.x[p] = newP
        self.x[q] = newQ
        self.t += 1
        self.barrier()
        if q != target:
            assert p in newQ and target in newQ
        if forced:
            self.migrations += 1
            assert p not in Q and target not in Q
            assert target in J
        if routing and q != target:
            after = self.young_count()
            assert after >= before
            if p not in Q:
                assert after >= before + 1
        for u in immune:
            assert outer_r in self.x[u] and not self.x[u][outer_r][1]
        converted = routing and target in newP and not newP[target][1]
        if converted:
            self.tracked_refresh_stops += 1
        return q, forced, converted

    def erase(self):
        for r in range(self.n):
            immune = {u for u, cc in enumerate(self.x) if r in cc and not cc[r][1]}
            iterations = 0
            while any(r in cc and cc[r][1] for cc in self.x):
                iterations += 1
                assert iterations <= self.n - 1
                p = self.pick([u for u, cc in enumerate(self.x)
                               if r in cc and cc[r][1]], 1)[0]
                count = segment = migrations = 0
                converted = False
                while True:
                    q, forced, converted = self.step(p, r, immune, r, routing=True)
                    count += 1
                    segment += 1
                    assert segment <= self.K
                    self.max_segment = max(self.max_segment, segment)
                    if q == r or converted:
                        break
                    if forced:
                        p = q
                        migrations += 1
                        assert migrations <= self.n * self.c
                        segment = 0
                assert count <= (self.n * self.c + 1) * self.K
                self.max_route = max(self.max_route, count)
                if converted:
                    assert p not in immune
                    immune.add(p)
                    continue
                h = p
                assert r not in self.x[h] and h in self.x[r]
                count = 0
                while True:
                    was_immune = set(immune)
                    had_old_r = {u for u, cc in enumerate(self.x)
                                 if r in cc and cc[r][1]}
                    q, forced, _ = self.step(r, h, immune, r)
                    count += 1
                    assert count <= self.n + self.c - 1
                    if q not in was_immune:
                        assert r in self.x[q] and not self.x[q][r][1]
                        if q in had_old_r:
                            self.callback_refresh_stops += 1
                        immune.add(q)
                        break
                    assert not forced
                self.max_callback = max(self.max_callback, count)
            assert all(r not in cc or not cc[r][1] for cc in self.x)
        assert not any(old for cc in self.x for age, old in cc.values())
        assert self.t <= self.L
        final_max = max([age for cc in self.x for age, old in cc.values()] + [0])
        assert final_max <= self.a + self.t
        # Arbitrary further steps increase the maximum by at most one per step.
        assert final_max + (self.L - self.t) <= (self.n * self.c + 1) * self.L


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=20)
    parser.add_argument('--seeds', type=int, default=10)
    args = parser.parse_args()
    if args.max_n < 3 or args.seeds < 1 or not __debug__:
        parser.error('require --max-n >=3, --seeds >=1, and enabled assertions')
    cases = migrations = old_old = mixed = tracked = callback = 0
    worst = (0, None)
    max_route = max_segment = max_callback = 0
    patterns = ('gapped', 'close', 'huge', 'staircase')
    for n in range(3, args.max_n + 1):
        for capacity in range(2, n):
            for seed in range(args.seeds):
                for pattern in patterns:
                    chain = Chain(n, capacity, seed, pattern)
                    chain.erase()
                    cases += 1
                    migrations += chain.migrations
                    old_old += chain.old_old_refreshes
                    mixed += chain.mixed_refreshes
                    tracked += chain.tracked_refresh_stops
                    callback += chain.callback_refresh_stops
                    max_route = max(max_route, chain.max_route)
                    max_segment = max(max_segment, chain.max_segment)
                    max_callback = max(max_callback, chain.max_callback)
                    if chain.t > worst[0]:
                        worst = chain.t, (n, capacity, seed, pattern)
    print(f'Passed {cases} nonvacuous states; forced migrations {migrations}.')
    print(f'OLD/OLD younger refreshes {old_old}; OLD/YOUNG refreshes {mixed}; '
          f'tracked conversion stops {tracked}; callback conversion stops {callback}.')
    print(f'Maximum exchanges {worst[0]}, case {worst[1]}; fixed-holder segment '
          f'{max_segment}; routing block {max_route}; callback block {max_callback}.')


if __name__ == '__main__':
    main()
