from random import Random
def run_case(n, c, ell, s, seed):
    rng = Random(seed)
    G=set(range(s,n)); r=s; R=(s*c+1)*c
    X=[]
    for p in range(n):
        ids=[q for q in range(n) if q!=p];rng.shuffle(ids)
        P={q:(rng.randrange(100*R+1),True) for q in ids[:rng.randrange(c+1)]}
        if p<s and rng.randrange(2)==0:
            if r not in P and len(P)==c:P.pop(next(iter(P)))
            P[r]=(R+1+rng.randrange(R+1),True)
        X.append(P)
    if not any(r in X[p] for p in range(s)):
        p=rng.randrange(s)
        if len(X[p])==c:X[p].pop(next(iter(X[p])))
        X[p][r]=(R+1,True)
    for p in range(s):
        if r in X[p]:X[p][r]=(max(R+1,X[p][r][0]),True)

    def pick(z, k):
        z = list(z)
        rng.shuffle(z)
        assert len(z) >= k
        return z[:k]

    def phi():
        fs=[sum(not v[1] for v in P.values()) for P in X]
        F=sum(fs[:s]);M=max(fs[p] for p in range(s) if r in X[p])
        return ((s*c-F,c-1-M),fs)
    def merge(v,w):return (min(v[0],w[0]),v[1] and w[1])
    t = 0
    counts = [0, 0]
    while True:
        (before, fs) = phi()
        f = max(fs[p] for p in range(s) if r in X[p])
        p = pick([p for p in range(s) if fs[p]==f and r in X[p]],1)[0]
        P = X[p]
        M = max((v[0] for v in P.values()))
        q = pick([q for q in P if P[q][0] == M], 1)[0]
        if q in G:
            assert t+1<=R
            return t+1,counts
        Q = X[q]
        assert P[q][1]
        k = min(ell - 1, len(P) - 1)
        m = min(ell, len(Q))
        missing = [z for (z, v) in P.items() if not v[1] and (z not in Q or Q[z][1])]
        S = [r]+(pick(missing,1) if missing else [])
        S += pick([z for z in P if z != q and z not in S], k - len(S))
        U = {p: (0, False), **{z: (P[z][0] + 1, P[z][1]) for z in S}}
        J = {z: v for (z, v) in U.items() if z not in Q}
        rq = max(0, len(Q) + len(J) - c)
        # Exclude received IDs and young copies that could be lost on duplicates.
        E = set(Q) & set(U) | {z for (z, v) in Q.items() if not v[1] and (z in P or z == p)}
        D = pick([z for z in Q if z not in E], rq)
        B = set(Q)&set(U)
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
        assert t<=R
        for u in range(s):
            for z,(age,old) in X[u].items():
                if not old:assert age<=t
                if z==r:assert old and age>R

if __name__=='__main__':
    cases=events=0;counts=[0,0];worst=(0,None)
    for n in range(4,16):
        for c in range(3,n):
            for ell in range(3,c+1):
                for s in range(1,n):
                    for seed in range(5):
                        t,z=run_case(n,c,ell,s,seed)
                        cases+=1;events+=t;counts=[a+b for a,b in zip(counts,z)]
                        if t>worst[0]:worst=t,(n,c,ell,s,seed)
    print(cases,events,counts,worst)
