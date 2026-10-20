import random
from itertools import combinations

class Cyclon:
 def __init__(self,caches,c):self.cc=[dict(x) for x in caches];self.n=len(caches);self.c=c;self.steps=0
 def zero(self):return all(a==0 for row in self.cc for a in row.values())
 def conn(self,V):
  V=set(V)
  if not V:return True
  seen={min(V)}
  while True:
   ns=seen|{j for i in V for j in self.cc[i] if i in seen and j in V}|{i for i in V for j in self.cc[i] if j in seen}
   if ns==seen:return seen==V
   seen=ns
 def act(self,p,policy=None,forceq=None,forcer=None):
  a=self.cc[p]
  assert a
  for j in a:a[j]+=1
  oldest=max(a.values());qs=[j for j in a if a[j]==oldest]
  q=min(qs) if forceq is None else forceq
  assert q in qs,(p,q,a)
  b=self.cc[q]
  if forcer is not None:r=forcer
  elif p in b:r=p
  elif policy is not None:r=policy(p,q)
  else:r=min(b) if b else None
  assert r is None and not b or r in b,(p,q,r,b)
  age=b.get(r)
  del a[q]
  if r is not None and r!=p and r not in a:a[r]=age
  if p not in b:
   if len(b)>=self.c:
    assert r is not None
    del b[r]
   b[p]=0
  assert all(len(row)<=self.c for row in self.cc)
  self.steps+=1
 def clear(self,p,policy=None,forceq=None,forcer=None):
  k=0
  while self.cc[p]:
   self.act(p,policy,forceq if k==0 else None,forcer if k==0 else None)
   k+=1
   assert k<=self.n+self.c-1,(p,k,self.cc)
 def canon(self,V):
  V=tuple(sorted(V));n=len(V)
  assert self.zero() and self.conn(V),(V,self.cc)
  assert all(set(self.cc[i])<=set(V) for i in V)
  if n==1:
   assert not self.cc[V[0]]
   return
  z=V[0];W=V[1:];m=W[-1]
  # Source separation.
  self.clear(z)
  for p in W:self.clear(p)
  assert self.zero() and self.conn(W)
  assert self.cc[z] and all(z not in self.cc[p] for p in W)
  self.canon(W)
  # Extend source.
  d=min(self.c,len(W));J=W[-d:];S=J[:-1];H=tuple(p for p in W if p not in J)
  self.clear(z)
  assert self.cc[m]=={z:0},(V,self.cc)
  assert all(m in self.cc[q] for q in W if q!=m)
  assert self.conn(W) and self.zero()
  def protect_m(p,q):
   b=self.cc[q]
   if len(b)>=self.c and m in b:return min(j for j in b if j!=m)
   return min(b) if b else None
  for j in S:
   assert m in self.cc[j] and self.zero()
   self.clear(j,protect_m,forceq=m,forcer=z)
  assert set(self.cc[z])==set(S) and set(self.cc[m])=={z,*S}
  def purge_policy(p,q):
   b=self.cc[q]
   if q==m and len(b)>=self.c:return min(j for j in b if j!=z)
   if q==z and len(b)>=self.c:return next(j for j in b if j not in S)
   return min(b) if b else None
  for h in H:self.clear(h,purge_policy)
  assert self.zero() and z in self.cc[m]
  assert all(z not in self.cc[p] for p in W if p!=m)
  b=self.cc[z];r=next((j for j in b if j not in S),min(b) if b else None)
  self.clear(m,purge_policy,forceq=z,forcer=r)
  assert self.zero() and self.conn(W)
  assert set(self.cc[z])==set(J) and all(z not in self.cc[p] for p in W)
  self.canon(W)
  assert all(set(self.cc[i])==set(V[max(V.index(i)+1,n-self.c):]) for i in V),(V,self.cc)

if __name__=='__main__':
 random.seed(734)
 count=0;largest=0
 for n in range(2,11):
  for c in range(2,min(n+2,6)):
   for sample in range(8):
    cc=[]
    for i in range(n):
     ids=([i+1] if i<n-1 else [])
     opts=[j for j in range(n) if j!=i and j not in ids];random.shuffle(opts)
     ids+=opts[:random.randrange(min(c-len(ids),len(opts))+1)]
     cc.append({j:random.randrange(30) for j in ids})
    p=Cyclon(cc,c)
    for i in range(n):p.clear(i)
    assert p.zero() and p.conn(range(n))
    p.canon(tuple(range(n)));count+=1;largest=max(largest,p.steps)
 print('PASS random initializations',count,'max activations',largest)
