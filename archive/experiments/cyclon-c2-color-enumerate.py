from itertools import combinations, product
from collections import defaultdict

n=5;p=0;q=1
outcomes=defaultdict(list)
examples={}
pure_delta=defaultdict(list)
for d in (1,2):
 for extra in ([None] if d==1 else range(2,n)):
  Pids=[q]+([] if extra is None else [extra])
  for e in range(3):
   for Qids in combinations([v for v in range(n) if v!=q],e):
    for colors in product((0,1),repeat=d+e):
     P=dict(zip(Pids,colors[:d]));Q=dict(zip(Qids,colors[d:]))
     S=set(P)-{q};R=set(Q)
     out={p:1,**{r:P[r] for r in S}}
     incoming=Q.copy()
     PR={r:v for r,v in P.items() if r!=q}
     ip=set(incoming)-set(PR)-{p};iq=set(out)-set(Q)-{q}
     dp=max(0,len(PR)+len(ip)-2);dq=max(0,len(Q)+len(iq)-2)
     ep=S-set(incoming);eq=R-set(out)
     for vp in combinations(ep,dp):
      for vq in combinations(eq,dq):
       A={r:v for r,v in PR.items() if r not in vp}
       B={r:v for r,v in Q.items() if r not in vq}
       for r,v in incoming.items():
        if r!=p:A[r]=max(A.get(r,0),v)
       for r,v in out.items():
        if r!=q:B[r]=max(B.get(r,0),v)
       delta=sum(A.values())+sum(B.values())-sum(P.values())-sum(Q.values())
       olddelta=(len(A)+len(B)-sum(A.values())-sum(B.values())
                 -len(P)-len(Q)+sum(P.values())+sum(Q.values()))
       key=(d,e,P[q])
       outcomes[key].append((delta,olddelta))
       pure=lambda row:bool(row) and not any(row.values())
       kd=pure(A)+pure(B)-pure(P)-pure(Q)
       allowed=(P[q]==0 or all(P.values()))
       pure_delta[allowed].append(kd)
       if allowed and kd>0:print('PURE COUNTEREXAMPLE',P,Q,A,B,kd)
       def components(U,V):
        edges=[(p,r) for r,c in U.items() if c]+[(q,r) for r,c in V.items() if c]
        comp=[{i} for i in range(n)]
        for i,j in edges:
         joined=comp[i]|comp[j]
         for k in joined:comp[k]=joined
        return comp
       before=components(P,Q);after=components(A,B)
       joined=before[p]|before[q]
       expected=[joined if before[i]&joined else before[i] for i in range(n)]
       assert after==expected,(P,Q,A,B,before,after,expected)
       examples.setdefault((key,delta),(P,Q,vp,vq,A,B))
for k,v in sorted(outcomes.items()):
 print(k,'count',len(v),'youngΔ',min(t[0] for t in v),max(t[0] for t in v),
       'oldΔ',min(t[1] for t in v),max(t[1] for t in v))
 if min(t[0] for t in v)<0:print('negative young example',examples[(k,min(t[0] for t in v))])
print('TOTAL',sum(map(len,outcomes.values())))
for allowed,values in sorted(pure_delta.items()):
 print('PURE selector respects old priority?',allowed,'range',min(values),max(values),'count',len(values))
