from itertools import product,combinations
import random

def connected(caches,vertices):
 vs=set(vertices)
 if not vs:return True
 seen={next(iter(vs))};todo=list(seen)
 while todo:
  p=todo.pop(); ns=(set(caches[p])|{q for q in vs if p in caches[q]})&vs
  for q in ns-seen:seen.add(q);todo.append(q)
 return seen==vs

class Control:
 def __init__(self,cs,c):self.cs=[dict(x) for x in cs];self.c=c;self.count=0;self.maxblock=0
 def block(self,p,vs,policy=None,first=None):
  initialzero=all(a==0 for x in self.cs for a in x.values())
  steps=0
  while self.cs[p]:
   for v in self.cs[p]:self.cs[p][v]+=1
   M=max(self.cs[p].values());oldest=[v for v,a in self.cs[p].items() if a==M]
   q=first if steps==0 and first is not None else min(oldest)
   assert q in oldest,(p,q,self.cs)
   cq=self.cs[q]
   if p in cq:r=p
   elif not cq:r=None
   elif policy:r=policy(p,q,vs)
   else:r=min(cq)
   assert r is None or r in cq
   age=cq[r] if r is not None else None
   del self.cs[p][q]
   if r is not None and r!=p and r not in self.cs[p]:self.cs[p][r]=age
   if p not in self.cs[q]:
    if len(self.cs[q])==self.c:
     assert r is not None
     del self.cs[q][r]
    self.cs[q][p]=0
   self.count+=1;steps+=1
   assert all(len(x)<=self.c for x in self.cs)
   assert connected(self.cs,range(len(self.cs)))
   assert steps<=len(vs)+self.c-1,(steps,len(vs),self.c,self.cs)
  self.maxblock=max(self.maxblock,steps)
  if initialzero:assert all(a==0 for x in self.cs for a in x.values())
 def zero(self):return all(a==0 for x in self.cs for a in x.values())
 def canon(self,vs):
  assert connected(self.cs,vs)
  assert all(set(self.cs[p])<=set(vs) for p in vs)
  assert self.zero()
  if len(vs)==1:assert not self.cs[vs[0]];return
  src=vs[0];ww=vs[1:];root=ww[-1]
  # separation
  for p in vs:self.block(p,vs)
  assert self.cs[src] and all(src not in self.cs[p] for p in ww)
  assert connected(self.cs,ww) and self.zero()
  self.canon(ww)
  # source extension
  targets=ww[-min(self.c,len(ww)):];protected=targets[:-1]
  self.block(src,vs,policy=lambda p,q,v:min(self.cs[q]))
  assert not self.cs[src] and self.cs[root]=={src:0}
  assert all(root in self.cs[p] for p in ww[:-1])
  for j in protected:
   def pol2(p,q,v):
    if q==root:return src
    opts=set(self.cs[q])
    if len(opts)==self.c and root in opts:opts.remove(root)
    return min(opts)
   self.block(j,vs,policy=pol2,first=root)
  assert set(self.cs[src])==set(protected)
  assert set(self.cs[root])=={src,*protected}
  for h in ww:
   if h in targets:continue
   def pol3(p,q,v):
    opts=set(self.cs[q])
    if q==root and len(opts)==self.c:opts.remove(src)
    if q==src and len(opts)==self.c:opts-=set(protected)
    return min(opts)
   self.block(h,vs,policy=pol3)
  assert src in self.cs[root] and all(src not in self.cs[p] for p in ww if p!=root)
  def pol4(p,q,v):
   opts=set(self.cs[q]);unprot=opts-set(protected)
   return min(unprot if q==src and unprot else opts)
  self.block(root,vs,policy=pol4,first=src)
  assert set(self.cs[src])==set(targets)
  assert all(src not in self.cs[p] for p in ww)
  assert connected(self.cs,ww) and self.zero()
  self.canon(ww)
  for idx,p in enumerate(vs):
   later=vs[idx+1:];expect=later[-min(self.c,len(later)):] if later else[]
   assert self.cs[p]==dict.fromkeys(expect,0),(p,self.cs,expect)


def allstates(n,c):
 options=[]
 for p in range(n):
  vs=[v for v in range(n) if v!=p]
  options.append([dict.fromkeys(cmb,0) for k in range(min(c,n-1)+1) for cmb in combinations(vs,k)])
 yield from product(*options)

if __name__=='__main__':
 count=0;maxsteps=0
 for n,c in [(2,2),(3,2),(4,2),(4,3)]:
  local=0
  for cs in allstates(n,c):
   if not connected(cs,range(n)):continue
   t=Control(cs,c);t.canon(list(range(n)));local+=1;count+=1;maxsteps=max(maxsteps,t.count)
  print('exhaustive',n,c,local,'passed',flush=True)
 rng=random.Random(89372)
 for _ in range(1000):
  n=rng.randrange(2,10);c=rng.randrange(2,7)
  while True:
   cs=[]
   for p in range(n):
    ns=rng.sample([q for q in range(n) if q!=p],rng.randrange(min(c,n-1)+1))
    cs.append({q:rng.randrange(10000) for q in ns})
   if connected(cs,range(n)):break
  t=Control(cs,c)
  for p in range(n):t.block(p,list(range(n)))
  assert t.zero();t.canon(list(range(n)));count+=1;maxsteps=max(maxsteps,t.count)
 print('all passed count',count,'max_actual_exchanges',maxsteps)
