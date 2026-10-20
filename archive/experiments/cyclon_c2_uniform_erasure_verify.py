import importlib.util
from pathlib import Path

SOURCE=Path('docs/peer-sampling-convergence/mandatory-removal/verify_lineage_erasure.py')
spec=importlib.util.spec_from_file_location('erasure',SOURCE)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
Chain=mod.Chain

def erase(ch):
 n=ch.n
 for r in range(n):
  immune={u for u in range(n) if r in ch.x[u] and not ch.x[u][r][1]}
  iterations=0
  while any(r in cc and cc[r][1] for cc in ch.x):
   iterations+=1;assert iterations<=n-1
   p=next(u for u in range(n) if r in ch.x[u] and ch.x[u][r][1])
   count=0
   while True:
    q,forced=ch.step(p,r,immune,r,callback=True,canonical_pairs=True)
    count+=1;assert count<=n
    if q==r:break
    if forced:
     p=q
     assert set(ch.x[p])=={r,q0} if False else True
     assert ch.x[p][r][0]>ch.x[p][next(z for z in ch.x[p] if z!=r)][0]
   h=p
   assert r not in ch.x[h] and h in ch.x[r]
   count=0
   while True:
    known=[r in cc for cc in ch.x]
    q,forced=ch.step(r,h,immune,r,canonical_pairs=True)
    count+=1;assert count<=n
    if not known[q]:
     assert r in ch.x[q] and not ch.x[q][r][1] and q not in immune
     immune.add(q);break
    assert not forced
  assert all(r not in cc or not cc[r][1] for cc in ch.x)
 assert not any(old for cc in ch.x for a,old in cc.values())
 assert ch.moves<=2*n*n*(n-1)
 assert max([a for cc in ch.x for a,old in cc.values()]+[0])<=ch.moves

if __name__=='__main__':
 total=0;worst=0;wc=None;migrations=0
 for n in range(3,31):
  for maxage in (0,1,100,1000000):
   for seed in range(20):
    ch=Chain(n,2,2,seed,maxage);erase(ch);total+=1;migrations+=ch.migrations
    if ch.moves>worst:worst=ch.moves;wc=(n,maxage,seed)
 print('Passed',total,'cases; max exchanges',worst,'case',wc,'forced migrations',migrations)
