from verify_thesis_anchor import Actual
from random import Random

def reach(z,a):
 seen={a}
 while True:
  ns=seen|{v for p in seen for v in z.x[p]}
  if ns==seen:return seen
  seen=ns

def force(z,a):
 phases=0;used=0
 while True:
  R=reach(z,a)
  if len(R)==z.n:return phases,used
  p,q=next((p,q) for p in range(z.n) if p not in R for q in z.x[p] if q in R)
  P=z.x[p];mx=max(P.values());u=min(v for v in P if P[v]==mx)
  if P[q]==mx:u=q
  if u in R:
   z.step(p,u,set(P)-{u},set(z.x[u]));used+=1
  else:
   z.step(p,u,[q],set(z.x[u]));used+=1
   assert set(z.x[u])=={p,q} and z.x[u][p]==0 and z.x[u][q]>=0
   z.step(u,q,[p],set(z.x[q]));used+=1
  NR=reach(z,a);assert R|{p}<=NR,(R,NR,p,q,u,z.x)
  phases+=1;assert phases<=z.n-1 and used<=2*(z.n-1)

rng=Random(912);cases=0;worst=0
for n in range(3,31):
 for seed in range(100):
  # Orient a spanning tree, respecting capacity, then add random extras.
  x=[{} for _ in range(n)]
  for p in range(1,n):
   q=rng.randrange(p)
   if len(x[q])<2 and rng.randrange(2):x[q][p]=rng.randrange(1000001)
   else:x[p][q]=rng.randrange(1000001)
  for p in range(n):
   if len(x[p])<2 and rng.randrange(2):
    q=rng.choice([q for q in range(n) if q!=p and q not in x[p]]);x[p][q]=rng.randrange(1000001)
  z=Actual(x,2);a=rng.randrange(n);ph,ev=force(z,a);cases+=1;worst=max(worst,ev)
print('PASS',cases,'maximum_controlled_exchanges',worst)
