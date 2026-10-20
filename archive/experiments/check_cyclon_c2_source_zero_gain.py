from verify_thesis_anchor import Actual
from random import Random
from collections import deque

def path_to_nonzero(z,a):
 todo=deque([a]);parent={a:None};end=None
 while todo:
  p=todo.popleft()
  if p!=a and z.x[p].get(a)!=0:end=p;break
  for q in z.x[p]:
   if q not in parent:parent[q]=p;todo.append(q)
 if end is None:return None
 path=[]
 while end is not None:path.append(end);end=parent[end]
 return list(reversed(path))

def holders(z,a):return {p for p in range(z.n) if p!=a and z.x[p].get(a)==0}

def force(z,a):
 I=holders(z,a);path=path_to_nonzero(z,a)
 if path is None:return None
 start=len(I);used=0;phases=0
 while len(holders(z,a))==start:
  oldpath=path_to_nonzero(z,a);assert oldpath is not None
  d=len(oldpath)-1;target=oldpath[1];events=0
  while len(holders(z,a))==start:
   P=z.x[a];u=max(P,key=lambda q:(P[q],q==target));extra=set(P)-{u}
   z.step(a,u,extra,set(z.x[u]));used+=1;events+=1
   assert I<=holders(z,a)
   if len(holders(z,a))>start:break
   np=path_to_nonzero(z,a);assert np is not None and len(np)-1<=d
   if len(np)-1<d:break
   assert target in z.x[a] and events<=z.n+1
  phases+=1;assert phases<=z.n-1
 assert len(holders(z,a))>=start+1
 assert used<=(z.n-1)*(z.n+1)
 return used

rng=Random(914);cases=skipped=worst=0
for n in range(3,31):
 for seed in range(100):
  a=rng.randrange(n);x=[]
  for p in range(n):
   peers=[q for q in range(n) if q!=p];rng.shuffle(peers);row={q:rng.randrange(1000001) for q in peers[:rng.randint(0,2)]}
   if p!=a and rng.randrange(2):
    if len(row)==2 and a not in row:del row[next(iter(row))]
    row[a]=0
   x.append(row)
  z=Actual(x,2);u=force(z,a)
  if u is None:skipped+=1
  else:cases+=1;worst=max(worst,u)
print('PASS',cases,'applicable','skipped',skipped,'maximum_controlled_exchanges',worst)
