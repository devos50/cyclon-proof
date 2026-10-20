#!/usr/bin/env python3
"""Check the all-shuffle-length protected+MIN finite-age reset controller.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_general_reset.py

The default covers n=3,...,20, every capacity c=2,...,n-1,
every fixed length ell=2,...,c, and seeds 0,...,9. It includes empty,
underfull, and full caches, with no connectivity requirement. For
H=(nc+1)(nc^2+1)(nc ell^c+1), initial YOUNG ages range from 0 to H,
and OLD ages exceed 2H. Thus every nontrivial execution retains an
actual empty age gap of length H, even when H is enormous. The
default run passes 11,400 starts and 373,413 controlled exchanges:
352,194 strict young-count increases, 2,598 square-sum decreases,
and 18,621 weighted-old decreases. Its longest path has 89 exchanges
(n=20, c=18, ell=4, seed=3).

Every step uses mandatory oldest selection, exact buffer sizes,
received-ID-protected victims, and MIN-age duplicate merges. Assertions
check the age/color barrier and strict lexicographic decrease of
(nc-F, V, W), where F counts YOUNG descriptors, V is the sum of squared
local YOUNG counts, and W weights each OLD descriptor at peer i by
ell^(c-f_i). The final checks cover OLD-color elimination, the uniform
event bound H, and the age bound (nc+1)H after arbitrary padding to H.
Initial YOUNG lineages need not be erased.

This reproducible finite/random check corroborates the symbolic proof;
it does not replace the proof for arbitrary sizes or ages. Only Python
is needed. Assertions must remain enabled: do not run with -O.
"""
from random import Random

def run_case(n, c, ell, seed):
    rng = Random(seed)
    H = (n * c + 1) * (n * c * c + 1) * (n * c * ell ** c + 1)
    a = H
    X = []
    for p in range(n):
        ids = [q for q in range(n) if q != p]
        rng.shuffle(ids)
        cache = {}
        for q in ids[:rng.randrange(c + 1)]:
            old = bool(rng.randrange(2))
            age = 2 * H + rng.randint(1, 1000000) if old else rng.randint(0, a)
            cache[q] = (age, old)
        X.append(cache)

    def pick(z, k):
        z = list(z)
        rng.shuffle(z)
        assert len(z) >= k
        return z[:k]

    def phi():
        fs = [sum((not v[1] for v in P.values())) for P in X]
        F = sum(fs)
        V = sum((f * f for f in fs))
        W = sum((sum((v[1] for v in P.values())) * ell ** (c - f) for (P, f) in zip(X, fs)))
        return ((n * c - F, V, W), fs)

    def merge(v, w):
        if w[0] < v[0]:
            return w
        if w[0] == v[0]:
            assert w[1] == v[1]
        return v
    t = 0
    counts = [0, 0, 0]
    while any((v[1] for P in X for v in P.values())):
        (before, fs) = phi()
        f = max((fs[p] for (p, P) in enumerate(X) if any((v[1] for v in P.values()))))
        p = pick([p for (p, P) in enumerate(X) if fs[p] == f and any((v[1] for v in P.values()))], 1)[0]
        P = X[p]
        M = max((v[0] for v in P.values()))
        q = pick([q for q in P if P[q][0] == M], 1)[0]
        Q = X[q]
        assert P[q][1]
        k = min(ell - 1, len(P) - 1)
        m = min(ell, len(Q))
        missing = [z for (z, v) in P.items() if not v[1] and (z not in Q or Q[z][1])]
        S = pick(missing, 1) if missing else []
        S += pick([z for z in P if z != q and z not in S], k - len(S))
        U = {p: (0, False), **{z: (P[z][0] + 1, P[z][1]) for z in S}}
        J = {z: v for (z, v) in U.items() if z not in Q}
        rq = max(0, len(Q) + len(J) - c)
        # Exclude received IDs and young copies that could be lost on duplicates.
        E = set(Q) & set(U) | {z for (z, v) in Q.items() if not v[1] and (z in P or z == p)}
        D = pick([z for z in Q if z not in E], rq)
        B = {z for z in S if not P[z][1] and z in Q} | ({p} if p in Q else set())
        T = D + list(B)
        T += pick([z for z in Q if z not in T], m - len(T))
        assert len(S) == k and len(set(S)) == k and q not in S
        assert len(T) == m and len(set(T)) == m
        rem = {z: (v[0] + 1, v[1]) for (z, v) in P.items() if z != q}
        reply = {z: Q[z] for z in T if z != p}
        I = {z: v for (z, v) in reply.items() if z not in rem}
        rp = max(0, len(rem) + len(I) - c)
        elig = [z for z in S if z not in reply]
        # Prefer old eligible victims at the initiator.
        O = pick([z for z in elig if P[z][1]], min(rp, sum((P[z][1] for z in elig))))
        VP = O + pick([z for z in elig if not P[z][1]], rp - len(O))
        newP = {z: v for (z, v) in rem.items() if z not in VP}
        for (z, v) in reply.items():
            newP[z] = merge(newP[z], v) if z in newP else v
        newQ = {z: v for (z, v) in Q.items() if z not in D}
        for (z, v) in U.items():
            newQ[z] = merge(newQ[z], v) if z in newQ else v
        X[p] = newP
        X[q] = newQ
        t += 1
        assert len(newP) <= c and len(newQ) <= c and (p not in newP) and (q not in newQ)
        assert set(VP) <= set(S) - set(reply)
        assert set(D) <= set(T) - set(U)
        (after, fs2) = phi()
        assert after < before, (n, c, ell, seed, before, after, P, Q, p, q, S, D, T, VP, newP, newQ)
        j = next((i for (i, (u, v)) in enumerate(zip(before, after)) if u != v))
        counts[j] += 1
        assert t <= H
        for P in X:
            for (age, old) in P.values():
                assert age > 2 * H if old else age <= H + t
    final_max = max([v[0] for P in X for v in P.values()] + [0])
    assert final_max <= a + t
    assert final_max + (H - t) <= (n * c + 1) * H
    return (t, counts)

def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=20)
    parser.add_argument('--seeds', type=int, default=10)
    args = parser.parse_args()
    if args.max_n < 3 or args.seeds < 1 or (not __debug__):
        parser.error('require --max-n >=3, --seeds >=1, and enabled assertions')
    cases = 0
    worst = (0, None)
    totals = [0, 0, 0]
    for n in range(3, args.max_n + 1):
        for capacity in range(2, n):
            for length in range(2, capacity + 1):
                for seed in range(args.seeds):
                    (steps, counts) = run_case(n, capacity, length, seed)
                    cases += 1
                    totals = [a + b for (a, b) in zip(totals, counts)]
                    if steps > worst[0]:
                        worst = (steps, (n, capacity, length, seed))
    print(f'Passed {cases} initial states; {sum(totals)} controlled exchanges.')
    print(f'Strict young-count increases {totals[0]}; strict square-sum decreases {totals[1]}; strict weighted-old decreases {totals[2]}.')
    print(f'Maximum exchanges {worst[0]}, case {worst[1]}.')
if __name__ == '__main__':
    main()
