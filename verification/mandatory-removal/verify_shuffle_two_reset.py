#!/usr/bin/env python3
"""Check the uniform finite-age reset for shuffle length two and any capacity.

Run from the repository root:
    python3 verification/mandatory-removal/verify_shuffle_two_reset.py

Default coverage: n=3,...,20, every capacity c=2,...,n-1, age bounds
0, 1, 100, and 1,000,000, and seeds 0,...,9. Initial cache sizes are
random, including empty and underfull caches; connectivity is unrestricted.
The reproduced default run passes 6,840 initial states and exercises
27,395 forced migrations. Its longest execution takes 1,015 exchanges
(n=20, c=17, initial age bound=1, seed=4).

Each descriptor records (age, initial-lineage mark, birth event). At the
start of each old-identity routing block, the birth event defines a new,
separate old/fresh coloring for the bounded migration argument. Assertions
check that the fresh count never decreases before the target is selected,
and rises whenever the responder lacks the initiator. They also check
pair preservation, immune descriptors, the migration bound, the corrected
2*n+c fixed-holder bound, the callback bound, complete initial-lineage
erasure, and the final uniform age bound.

The checks support the concrete controller; the arbitrary-size result
relies on the symbolic proof. Only Python is needed. Assertions must stay
enabled: do not run Python with -O.
"""
import argparse
from random import Random

class Chain:

    def __init__(self, n, c, seed, maxage=100):
        self.n = n
        self.c = c
        self.t = 0
        self.rng = Random(seed)
        self.x = []
        self.migrations = 0
        self.maxsegment = 0
        self.maxroute = 0
        self.maxcallback = 0
        for p in range(n):
            z = [q for q in range(n) if q != p]
            self.rng.shuffle(z)
            k = self.rng.randint(0, c)
            self.x.append({q: (self.rng.randrange(maxage + 1), True, -1) for q in z[:k]})

    def fresh(self, start):
        return sum((b >= start for cc in self.x for (a, o, b) in cc.values()))

    def pick(self, z, k):
        z = list(z)
        self.rng.shuffle(z)
        assert len(z) >= k
        return z[:k]

    def step(self, p, target, immune, outer_r, inner_start=None, callback=False):
        P = self.x[p]
        a = len(P)
        assert target in P
        mx = max((v[0] for v in P.values()))
        q = self.rng.choice([z for (z, v) in P.items() if v[0] == mx])
        Q = self.x[q]
        b = len(Q)
        if q == target:
            S = self.pick([z for z in P if z != q], min(1, a - 1))
            protect = p if callback and p in Q else outer_r if q in immune else None
            T = self.pick(Q, min(2, b)) if protect not in Q else [protect] + self.pick([z for z in Q if z != protect], min(2, b) - 1)
            out = {p: (0, False, self.t), **{z: (P[z][0] + 1, P[z][1], P[z][2]) for z in S}}
            J = {z: v for (z, v) in out.items() if z not in Q and z != q}
            rq = max(0, b + len(J) - self.c)
            victimsQ = self.pick([z for z in T if z != protect], rq)
        else:
            S = [target]
            assert a >= 2
            out = {p: (0, False, self.t), target: (P[target][0] + 1, P[target][1], P[target][2])}
            J = {z: v for (z, v) in out.items() if z not in Q}
            rq = max(0, b + len(J) - self.c)
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
                    if inner_start is not None:
                        candidates = [z for z in candidates if Q[z][2] < inner_start or (z not in P and z != p)]
                    D = self.pick(candidates, 1)[0]
                    T = [sentinel, D]
                    victimsQ = [D]
                else:
                    T = [sentinel] + self.pick(candidates, min(2, b) - 1)
                    victimsQ = []
            else:
                candidates = list(Q)
                if inner_start is not None:
                    candidates = [z for z in candidates if Q[z][2] < inner_start or (z not in P and z != p)]
                victimsQ = self.pick(candidates, rq)
                T = victimsQ + self.pick([z for z in Q if z not in victimsQ], min(2, b) - len(victimsQ))
        rem = {z: (v[0] + 1, v[1], v[2]) for (z, v) in P.items() if z != q}
        I = {z: Q[z] for z in T if z != p and z not in rem}
        rp = max(0, len(rem) + len(I) - self.c)
        assert rp <= len(S)
        victimsP = self.pick(S, rp)
        forced = target in victimsP
        f0 = self.fresh(inner_start) if inner_start is not None else None
        if inner_start is not None and q != target:
            assert P[q][2] < inner_start, (P, q, target, inner_start, self.t)
        self.x[p] = {z: v for (z, v) in rem.items() if z not in victimsP} | I
        self.x[q] = {z: v for (z, v) in Q.items() if z not in victimsQ} | J
        if q != target:
            assert p in self.x[q] and target in self.x[q]
        if forced:
            self.migrations += 1
            assert p not in Q and target not in Q and (target in J)
        if inner_start is not None and q != target:
            f1 = self.fresh(inner_start)
            assert f1 >= f0, (f0, f1, P, Q, out, T, I, J, victimsQ)
            if p not in Q:
                assert f1 >= f0 + 1
        for u in immune:
            assert outer_r in self.x[u] and (not self.x[u][outer_r][1])
        self.t += 1
        return (q, forced)

    def erase(self):
        n = self.n
        c = self.c
        K = 2 * n + c
        for r in range(n):
            immune = {u for u in range(n) if r in self.x[u] and (not self.x[u][r][1])}
            it = 0
            while any((r in cc and cc[r][1] for cc in self.x)):
                it += 1
                assert it <= n - 1
                p = next((u for u in range(n) if r in self.x[u] and self.x[u][r][1]))
                start = self.t
                count = 0
                segments = 0
                migs = 0
                seg = 0
                while True:
                    (q, forced) = self.step(p, r, immune, r, inner_start=start, callback=True)
                    count += 1
                    seg += 1
                    assert seg <= K
                    self.maxsegment = max(self.maxsegment, seg)
                    if q == r:
                        break
                    if forced:
                        p = q
                        migs += 1
                        assert migs <= n * c
                        seg = 0
                assert count <= (n * c + 1) * K
                self.maxroute = max(self.maxroute, count)
                h = p
                assert r not in self.x[h] and h in self.x[r]
                count = 0
                while True:
                    known = [r in cc for cc in self.x]
                    (q, forced) = self.step(r, h, immune, r)
                    count += 1
                    assert count <= n + c - 1
                    if not known[q]:
                        assert r in self.x[q] and (not self.x[q][r][1])
                        assert q not in immune
                        immune.add(q)
                        break
                    assert not forced
                self.maxcallback = max(self.maxcallback, count)
            assert all((r not in cc or not cc[r][1] for cc in self.x))
        assert not any((o for cc in self.x for (a, o, b) in cc.values()))
        L = n * (n - 1) * (n * c + 2) * K
        assert self.t <= L
        assert max([a for cc in self.x for (a, o, b) in cc.values()] + [0]) <= self.t

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=20)
    parser.add_argument('--seeds', type=int, default=10)
    parser.add_argument('--ages', type=int, nargs='+', default=[0, 1, 100, 1000000])
    args = parser.parse_args()
    if args.max_n < 3 or args.seeds < 1 or min(args.ages) < 0:
        parser.error('require --max-n >= 3, --seeds >= 1, and nonnegative --ages')
    if not __debug__:
        parser.error('assertions must be enabled; do not use python -O')
    total = 0
    worst = 0
    worst_case = None
    migrations = 0
    max_segment = 0
    max_route = 0
    max_callback = 0
    for n in range(3, args.max_n + 1):
        for capacity in range(2, n):
            for max_age in args.ages:
                for seed in range(args.seeds):
                    chain = Chain(n, capacity, seed, max_age)
                    chain.erase()
                    total += 1
                    migrations += chain.migrations
                    max_segment = max(max_segment, chain.maxsegment)
                    max_route = max(max_route, chain.maxroute)
                    max_callback = max(max_callback, chain.maxcallback)
                    if chain.t > worst:
                        worst = chain.t
                        worst_case = (n, capacity, max_age, seed)
    print(f'Passed {total} initial states. Forced migrations {migrations}; maximum exchanges {worst}; case {worst_case}.')
    print(f'Maximum fixed-holder segment {max_segment}; routing block {max_route}; callback block {max_callback}.')
if __name__ == '__main__':
    main()
