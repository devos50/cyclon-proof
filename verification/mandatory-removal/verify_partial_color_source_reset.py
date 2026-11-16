#!/usr/bin/env python3
"""Candidate frozen-owner partial-color reset checker.
Excludes peer 0 from initiation; every 0 descriptor is initially OLD.
Checks unchanged protected/MIN kernel and F,V plateau structure, stopping
when all references to 0 vanish. Numerical ages have an H-wide gap.
Random finite checks corroborate, but do not prove, the source argument.
"""
from random import Random
from verify_thesis_cooperative_owner import ActualThree

def run_case(n, c, ell, seed):
    rng = Random(seed)
    K = n * (c + 1) ** c
    D = n * c * ell ** c
    H = (n * c + 1) * (n * c * c + 1) * ((K + 1) * (D + 1) + 1)
    a = H
    X = []
    for p in range(n):
        ids = [q for q in range(n) if q != p]
        rng.shuffle(ids)
        cache = {}
        for q in ids[:rng.randrange(c + 1)]:
            old = q == 0 or bool(rng.randrange(2))
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
    counts = [0, 0, 0, 0]
    while any(0 in P for P in X):
        (before, fs) = phi()
        f = max((fs[p] for (p, P) in enumerate(X) if p != 0 and any((v[1] for v in P.values()))))
        p = pick([p for (p, P) in enumerate(X) if p != 0 and fs[p] == f and any((v[1] for v in P.values()))], 1)[0]
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
        exact = ActualThree([{z: value[0] for z, value in row.items()} for row in X], c, ell)
        exact.step(p, q, S, T, vp=VP, vq=D)
        assert exact.x[p] == {z: value[0] for z, value in newP.items()}
        assert exact.x[q] == {z: value[0] for z, value in newQ.items()}
        X[p] = newP
        X[q] = newQ
        t += 1
        assert len(newP) <= c and len(newQ) <= c and (p not in newP) and (q not in newQ)
        assert set(VP) <= set(S) - set(reply)
        assert set(D) <= set(T) - set(U)
        (after, fs2) = phi()
        assert after[:2] <= before[:2], (n, c, ell, seed, before, after)
        assert p != 0
        assert all(0 not in row or row[0][1] for row in X)
        if after[:2] == before[:2]:
            assert fs == fs2
            assert {z for z,v in P.items() if not v[1]} == {z for z,v in newP.items() if not v[1]}
            assert {z for z,v in Q.items() if not v[1]} == {z for z,v in newQ.items() if not v[1]}
            assert fs[q] > fs[p]
            if q != 0:
                assert all(not value[1] for value in Q.values())
                assert after[2] < before[2]
                counts[2] += 1
            else:
                counts[3] += 1
        elif after[0] < before[0]:
            counts[0] += 1
        else:
            counts[1] += 1
        assert t <= H
        for P in X:
            for (age, old) in P.values():
                assert age > 2 * H if old else age <= H + t
    assert all(0 not in row for row in X)
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
    totals = [0, 0, 0, 0]
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
    print(f'Plateau frozen-owner contacts {totals[3]}.')
    print(f'Maximum exchanges {worst[0]}, case {worst[1]}.')
if __name__ == '__main__':
    main()
