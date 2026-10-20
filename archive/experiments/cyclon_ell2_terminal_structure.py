from cyclon_ell2_identity_scc import graph,POP
from collections import Counter

def structure(code,n):
 adj=[0]*n;full=(1<<n)-1
 for p in range(n):
  row=(code>>(p*n))&full;adj[p]|=row
  for q in range(n):
   if row>>q&1:adj[q]|=1<<p
 deg=[POP[x] for x in adj]
 articulations=[]
 for omit in range(n):
  vs=full&~(1<<omit);seen=vs&-vs
  while True:
   old=seen
   for p in range(n):
    if seen>>p&1:seen|=adj[p]&vs
   if seen==old:break
  if seen!=vs:articulations.append(omit)
 return min(deg),sum(deg)//2,len(articulations)

if __name__=='__main__':
 n=4;c=2
 st,adj,comp,cs,term=graph(n,c,False)
 for k in term:
  z=Counter(structure(st[ix],n) for ix in cs[k]);print('terminal_structure',n,c,dict(z))
 tt={ix for k in term for ix in cs[k]}
 z=Counter((structure(s,n),ix in tt) for ix,s in enumerate(st));print('all_structure',dict(z))
