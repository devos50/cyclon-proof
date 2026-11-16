#!/usr/bin/env python3
"""Exact conditional internal reset with shared, unequal bounded p ages.

The reduced color-controller choices follow verify_thesis_general_reset.
Every event is executed and legality-checked by ActualThree. No padding,
service to p, generic accessibility, or convergence is asserted.
"""
from collections import Counter
from pathlib import Path
from random import Random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_thesis_cooperative_owner import ActualThree, zeros


def parameters(h, c, L, M):
    d, e = min(c - 2, h - 1), min(L - 2, h - 1)
    R = 1 if h == 1 else 2 if h == 2 else (h*d+1)*(h*d*d+1)*(h*d*e**d+1)
    B = M + (h*d+1)*R
    return d, e, R, B, (c+1)*R+c, B+c*c+c


def reset(z, H, M, rng, stats):
    h = len(H)
    d, e, R, B, _, _ = parameters(h, z.c, z.ell, M)
    frozen_owner = dict(z.x[0])
    initial = [age for i in H for v, age in z.x[i].items() if v not in {0, 1}]
    j = next(j for j in range(h*d+1) if not any(M+j*R < age <= M+(j+1)*R for age in initial))
    A = M + j*R
    stats['resets'] += 1
    stats['nonfirst_gap'] += j > 0
    elapsed = 0

    def residual():
        return {i: {v: (age, age > A+R) for v, age in z.x[i].items() if v not in {0, 1}} for i in H}

    def potential(X):
        fs = {i: sum(not old for _, old in row.values()) for i, row in X.items()}
        return (h*d-sum(fs.values()), sum(f*f for f in fs.values()),
                sum(sum(old for _, old in X[i].values()) * e**(d-fs[i]) for i in H)), fs

    def pick(values, count):
        assert 0 <= count <= len(values)
        return rng.sample(sorted(values), count)

    while True:
        X = residual()
        oldholders = [i for i in H if any(old for _, old in X[i].values())]
        if not oldholders:
            break
        before, fs = potential(X)
        maximum_young = max(fs[i] for i in oldholders)
        p = rng.choice([i for i in oldholders if fs[i] == maximum_young])
        P = X[p]
        q = rng.choice([v for v in P if P[v][0] == max(age for age, _ in P.values())])
        Q = X[q]
        assert P[q][1] and P[q][0] > M
        assert z.x[p][q] == max(z.x[p].values())
        if e == 1:
            assert h == 2 and d == 1
            S, T, VP, D = [], list(Q), [], []
        else:
            k, m = min(e-1, len(P)-1), min(e, len(Q))
            missing = [v for v in P if not P[v][1] and (v not in Q or Q[v][1])]
            S = pick(missing, 1) if missing else []
            S += pick(set(P)-{q}-set(S), k-len(S))
            U = {p: (0, False), **{v: (P[v][0]+1, P[v][1]) for v in S}}
            new = set(U)-set(Q)
            rq = max(0, len(Q)+len(new)-d)
            excluded = set(Q)&set(U) | {v for v in Q if not Q[v][1] and (v in P or v == p)}
            D = pick(set(Q)-excluded, rq)
            required = {v for v in S if not P[v][1] and v in Q} | ({p} if p in Q else set())
            T = D + sorted(required)
            T += pick(set(Q)-set(T), m-len(T))
            rem = set(P)-{q}
            valid = set(T)-{p}
            rp = max(0, len(rem)+len(valid-rem)-d)
            eligible = set(S)-valid
            oldeligible = {v for v in eligible if P[v][1]}
            VP = pick(oldeligible, min(rp,len(oldeligible)))
            VP += pick(eligible-oldeligible, rp-len(VP))
        z.step(p, q, {0,1}|set(S), {0,1}|set(T), vp=set(VP), vq=set(D))
        elapsed += 1
        stats['residual_events'] += 1
        assert elapsed <= R and z.x[0] == frozen_owner
        assert all(z.x[i][0] == 0 and 0 <= z.x[i][1] <= M for i in H)
        assert all(set(z.x[i])-{0,1} <= set(H) for i in H)
        afterX = residual()
        assert all(age > A+R if old else age <= A+elapsed for row in afterX.values() for age, old in row.values())
        if e >= 2:
            after, _ = potential(afterX)
            assert after < before
            coordinate = next(k for k in range(3) if after[k] != before[k])
            stats[f'potential_coordinate_{coordinate}'] += 1
        else:
            assert sum(old for row in afterX.values() for _,old in row.values()) < sum(old for row in X.values() for _,old in row.values())
            stats['singleton_residual_events'] += 1
    assert all(age <= B for i in H for v, age in z.x[i].items() if v not in {0,1})


def construct(z, H, M, rng):
    d,e,R,B,T,K = parameters(len(H), z.c, z.ell, M)
    original = [dict(row) for row in z.x]
    oldzeros = zeros(z, 0)
    stats = Counter()
    ownerages = [age for v,age in z.x[0].items() if v != 1]
    j = next(j for j in range(z.c+1) if not any(B+j*z.c < age <= B+(j+1)*z.c for age in ownerages))
    A = B+j*z.c
    assert A <= B+z.c*z.c
    rounds = 0
    start = z.steps
    while any(v != 1 and age > A+z.c for v, age in z.x[0].items()):
        reset(z,H,M,rng,stats)
        q = max(z.x[0], key=z.x[0].get)
        assert q in H and z.x[0][q] > A+z.c
        oldcount = sum(v != 1 and age > A+z.c for v,age in z.x[0].items())
        extra = {1}
        extra |= set(rng.sample(sorted(set(z.x[0])-{q,1}), min(z.ell-1,len(z.x[0])-1)-1))
        reply = {0,1}
        reply |= set(rng.sample(sorted(set(z.x[q])-{0,1}), min(z.ell,len(z.x[q]))-2))
        z.step(0,q,extra,reply)
        rounds += 1
        stats['owner_events'] += 1
        assert rounds <= z.c and 1 in z.x[0] and z.x[0][1] <= M
        assert sum(v != 1 and age > A+z.c for v,age in z.x[0].items()) < oldcount
    reset(z,H,M,rng,stats)
    assert z.steps-start <= T
    assert max(z.x[0].values()) <= K
    assert all(z.x[i][1] <= M for i in {0}|set(H))
    assert all(age <= B for i in H for v,age in z.x[i].items() if v not in {0,1})
    assert zeros(z,0) == oldzeros
    assert all(z.x[v] == original[v] for v in range(z.n) if v not in {0}|set(H))
    stats['events'] += z.steps-start
    return stats


def trial(L,c,h,seed):
    rng = Random(seed)
    M = rng.choice((0,1,7,10**6))
    d,e,R,B,T,K = parameters(h,c,L,M)
    H = list(range(2,h+2))
    n = max(c+1,h+3)
    ages = (0,M,M+R,M+2*R,M+(h*d+3)*R)
    rows = [{1:rng.randrange(M+1)}, {0:10**6}]
    for i in H:
        row = {0:0,1:rng.randrange(M+1)}
        ids = rng.sample(sorted(set(H)-{i}),rng.randrange(d+1))
        row.update({v:rng.choice(ages) for v in ids})
        rows.append(row)
    rows += [{0:0} for _ in range(n-len(rows))]
    heads = rng.sample(H,rng.randint(1,min(c-1,h)))
    rows[0].update({v:rng.choice((0,M,B,B+c*c+c+10**6)) for v in heads})
    return construct(ActualThree(rows,c,L),H,M,rng)


def main():
    total = Counter()
    cases = 0
    for L in range(4,9):
        for c in range(L,L+3):
            for h in range(1,c+3):
                for seed in range(15):
                    total.update(trial(L,c,h,L*100000+c*1000+h*20+seed))
                    cases += 1
    assert total['owner_events'] and total['singleton_residual_events'] and total['nonfirst_gap']
    print('PASS conditional shared-positive reset cases:',cases)
    print('Exact counts:',dict(sorted(total.items())))
    print('Scope: bounded internal state only; outside rows frozen, no service or convergence claim.')


if __name__ == '__main__': main()
