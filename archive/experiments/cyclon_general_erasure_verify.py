from random import Random
from itertools import combinations

class Chain:
 def __init__(self,n,c,l,seed):
  self.n=n;self.c=c;self.l=l;self.rng=Random(seed);self.t=0
  self.x=[]
  for p in range(n):
   ids=[q for q in range(n) if q!=p];self.rng.shuffle(ids)
   k=self.rng.randint(0,min(c,n-1))
   self.x.append({q:(self.rng.randrange(101),True) for q in ids[:k]})
  self.initialmax=max([a for cc in self.x for a,o in cc.values()]+[0])
  self.moves=0;self.migrations=0
 def choose(self,ids,k,exclude=None):
  z=[q for q in ids if q!=exclude]
  assert len(z)>=k
  self.rng.shuffle(z)
  return z[:k]
 def step(self,p,target,immune,r,callback=False):
  P=self.x[p];a=len(P);assert target in P
  M=max(v[0] for v in P.values());oldest=[q for q in P if P[q][0]==M]
  q=self.rng.choice(oldest);Q=self.x[q];b=len(Q)
  k=min(self.l-1,a-1);m=min(self.l,b)
  extra=[z for z in P if z!=q]
  S=self.choose(extra,k,target if target!=q and len(extra)>k else None)
  # protect existing immunity; final old-r contact also keeps callback identity p at home r
  protectQ=r if q in immune else None
  if callback and q==r:protectQ=p if p in Q else None
  T=self.choose(Q,m,protectQ if b>m else None)
  incP={z:(v[0]+1,v[1]) for z,v in P.items() if z!=q}
  out={p:(0,False),**{z:incP[z] for z in S}}
  I={z:Q[z] for z in T if z!=p and z not in incP}
  J={z:v for z,v in out.items() if z!=q and z not in Q}
  reqP=max(0,len(incP)+len(I)-self.c)
  reqQ=max(0,b+len(J)-self.c)
  victimP=[z for z in S if z!=target]
  self.rng.shuffle(victimP)
  forced=reqP>len(victimP)
  if forced:victimP.append(target)
  victimP=victimP[:reqP]
  victimQ=[z for z in T if z!=protectQ]
  assert reqQ<=len(victimQ),(self.x,p,q,target,immune,r,S,T,reqQ,victimQ)
  self.rng.shuffle(victimQ);victimQ=victimQ[:reqQ]
  if forced:
   assert self.l==self.c and len(I)==self.c and b==self.c
   assert not set(Q)&(set(P)|{p})
   assert target in J
   self.migrations+=1
  self.x[p]={z:v for z,v in incP.items() if z not in victimP}|I
  self.x[q]={z:v for z,v in Q.items() if z not in victimQ}|J
  for u in immune:assert r in self.x[u] and not self.x[u][r][1]
  self.t+=1;self.moves+=1
  return q,forced
 def erase(self):
  for r in range(self.n):
   immune={u for u in range(self.n) if r in self.x[u] and not self.x[u][r][1]}
   iterations=0
   while any(r in cc and cc[r][1] for cc in self.x):
    iterations+=1;assert iterations<=self.n-1
    p=next(u for u in range(self.n) if r in self.x[u] and self.x[u][r][1])
    a=self.x[p][r][0];M=[max([cc[s][0] for cc in self.x if s in cc]+[0]) for s in range(self.n)]
    lim=1+sum(max(0,M[s]-a+1) for s in range(self.n) if s!=r)
    count=0
    while True:
     q,forced=self.step(p,r,immune,r,callback=True);count+=1
     assert count<=lim,(count,lim)
     if q==r:break
     if forced:p=q
     assert r in self.x[p] and self.x[p][r][1]
    h=p
    assert r not in self.x[h] and h in self.x[r]
    a=self.x[r][h][0];M=[max([cc[s][0] for cc in self.x if s in cc]+[0]) for s in range(self.n)]
    lim=1+sum(max(0,M[s]-a+1) for s in range(self.n) if s not in (r,h))
    count=0
    while True:
     q,forced=self.step(r,h,immune,r);count+=1
     assert count<=lim
     if q==h or forced:
      assert r in self.x[q] and not self.x[q][r][1] and q not in immune
      immune.add(q);break
   assert all(r not in cc or not cc[r][1] for cc in self.x)
  assert not any(o for cc in self.x for a,o in cc.values())
  assert max([a for cc in self.x for a,o in cc.values()]+[0])<=self.moves

if __name__=='__main__':
 total=0;migrations=0;worst=0;case=None
 for n in range(2,11):
  for c in range(1,n):
   for l in range(1,c+1):
    for seed in range(20):
     ch=Chain(n,c,l,seed);ch.erase();total+=1;migrations+=ch.migrations
     if ch.moves>worst:worst=ch.moves;case=(n,c,l,seed)
 print('Passed',total,'initial states. Forced migrations',migrations,'max exchanges',worst,'case',case)
