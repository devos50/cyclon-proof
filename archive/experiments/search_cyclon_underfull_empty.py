from itertools import combinations
from random import Random
from collections import deque
import sys
sys.path.insert(0,'/Users/martijndevos/Documents/decentralized-learning-simulator/docs/peer-sampling-convergence/mandatory-removal')
from verify_thesis_cooperative_owner import ActualThree

def state(x): return tuple(tuple(sorted(r.items())) for r in x)
def rows(s): return [dict(r) for r in s]
def transitions(s,c=4,ell=3):
 x=rows(s); n=len(x); I=set(range(2,n))
 for p in range(n):
  if not x[p]: continue
  top=max(x[p].values())
  for q in sorted(v for v,t in x[p].items() if t==top):
   if p in I and q not in I: continue
   pool=set(x[p])-{q}
   for E in combinations(sorted(pool),min(ell-1,len(pool))):
    if p in I and 0 not in E: continue
    for T in combinations(sorted(x[q]),min(ell,len(x[q]))):
     if p in I and 0 not in T: continue
     P=set(x[p])-{q};Q=set(x[q]); U={p}|set(E);R=set(T)
     dp=max(0,len(P)+len(R-P-{p})-c);dq=max(0,len(Q)+len(U-Q-{q})-c)
     for VP in combinations(sorted(set(E)-R),dp):
      for VQ in combinations(sorted(R-U),dq):
       z=ActualThree(x,c,ell);z.step(p,q,E,T,VP,VQ)
       if any(z.x[v].get(0)!=0 for v in I): continue
       ns=state(z.x)
       if ns!=s: yield ns,(p,q,E,T,VP,VQ)

def solve(x,depth=8,cap=50000):
 start=state(x); queue=deque([start]);prev={start:None};acts={};ds={start:0}
 while queue:
  s=queue.popleft();d=ds[s]
  if dict(s[1]).get(0)==0:
   path=[]
   while prev[s] is not None:path.append((acts[s],rows(s)));s=prev[s]
   return list(reversed(path)),len(prev)
  if d>=depth:continue
  for ns,act in transitions(s):
   if ns not in prev:
    prev[ns]=s;acts[ns]=act;ds[ns]=d+1;queue.append(ns)
    if len(prev)>=cap:return None,len(prev)
 return None,len(prev)

rng=Random(712)
for seed in range(30):
 x=[{},{}]+[{0:0} for _ in range(3)]
 x[0]={1:0,**{v:1+rng.randrange(2) for v in rng.sample([2,3,4],rng.randrange(1,4))}}
 for q in [2,3,4]:
  others=rng.sample(sorted(set(range(5))-{0,q}),rng.randrange(3))
  x[q].update({v:rng.randrange(3) for v in others})
 if all(r.get(1)==0 for r in x[2:]):continue
 path,seen=solve(x)
 print(seed,'depth',None if path is None else len(path),'seen',seen,'initial',x,flush=True)
 if path is None or len(path)>=4:
  print('PATH',path,flush=True)
