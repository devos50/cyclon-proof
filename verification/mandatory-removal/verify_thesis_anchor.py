#!/usr/bin/env python3
"""Exact protected+MIN checks for universal-anchor reduction and merging.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_anchor.py

Default coverage is n=3,...,10, every capacity c=2,...,n-1, age bounds
0 and 1,000,000, and eight reproducible seeds. The 576 initializations
have an arbitrary anchor label, arbitrary possibly nonempty owner cache,
and random disconnected residual partitions, including components smaller
than the residual capacity. The reproduced run passes 1,829,148 actual
ell=2 exchanges: 1,822,679 residual-embedding exchanges, 5,140 four-event
merge-gadget exchanges, and the remaining owner-clearing exchanges.
The longest trajectory has 42,853 exchanges. A faster run uses
--max-n 8 --seeds 3.

This verifies controlled paths conditional on an existing universal age-zero
anchor. It does not prove accessibility of that condition from general states.
The actual ell=2 numerical-age kernel is evaluated independently of the
simulated ell=1 residual updates, and every corresponding outcome is compared.
Residual ell=1 controllers use minimum-age merging too. At residual capacity
one, the code constructs paths through zero-age rooted spanning trees;
otherwise it uses the sibling singleton verifier's constructive induction.
Assertions check oldest choices, maximum buffer sizes, protected victims,
all minimum-age updates, anchor ages, frozen owner caches, exact gadget state
tables, residual component merging, and the final canonical zero-age cache
configuration. These numerical checks corroborate the structural proof and
do not establish the arbitrary-size theorem by enumeration. Only Python's
standard library and the sibling verifier are required. Do not use Python -O.
"""
from itertools import combinations
from random import Random
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify_singleton_general import ControlledCyclon

class Actual:
 def __init__(self,caches,c):
  self.x=[dict(z) for z in caches];self.c=c;self.n=len(caches);self.steps=0;self.embedding_steps=0;self.merge_steps=0
 def step(self,p,q,extra,reply,vp=None,vq=None):
  P0=self.x[p];Q0=self.x[q];assert P0 and p!=q
  P={z:a+1 for z,a in P0.items()};Q=Q0.copy();extra=set(extra);reply=set(reply)
  assert q in P and P[q]==max(P.values()),(p,q,P)
  assert len(extra)==min(1,len(P)-1) and extra<=set(P)-{q}
  assert len(reply)==min(2,len(Q)) and reply<=set(Q)
  out={p:0,**{z:P[z] for z in extra}};incoming={z:Q[z] for z in reply}
  del P[q]
  ip=set(incoming)-set(P)-{p};iq=set(out)-set(Q)-{q}
  dp=max(0,len(P)+len(ip)-self.c);dq=max(0,len(Q)+len(iq)-self.c)
  ep=extra-set(incoming);eq=reply-set(out)
  vp=set(sorted(ep)[:dp]) if vp is None else set(vp)
  vq=set(sorted(eq)[:dq]) if vq is None else set(vq)
  assert len(vp)==dp and vp<=ep and len(vq)==dq and vq<=eq
  A={z:a for z,a in P.items() if z not in vp};B={z:a for z,a in Q.items() if z not in vq}
  for z,a in incoming.items():
   if z!=p:A[z]=min(A.get(z,a),a)
  for z,a in out.items():
   if z!=q:B[z]=min(B.get(z,a),a)
  self.x[p]=A;self.x[q]=B;self.steps+=1
  assert all(len(r)<=self.c and i not in r for i,r in enumerate(self.x))
 def universal(self,a):return all(p==a or self.x[p].get(a)==0 for p in range(self.n))
 def components(self,a):
  W=set(range(self.n))-{a};out=[]
  while W:
   reached={min(W)}
   while True:
    more=reached|{v for u in reached for v in self.x[u] if v!=a}|{u for u in W if set(self.x[u])&reached}
    if more==reached:break
    reached=more
   assert reached<=W
   out.append(reached);W-=reached
  return out

class Residual(ControlledCyclon):
 def __init__(self,actual,anchor,vertices):
  self.actual=actual;self.anchor=anchor;self.labels=tuple(vertices);self.inv={v:i for i,v in enumerate(vertices)}
  caches=[{self.inv[z]:age for z,age in actual.x[v].items() if z!=anchor} for v in vertices]
  super().__init__(caches,actual.c-1)
  assert actual.universal(anchor)
 def activate(self,initiator,policy=None,partner=None,reply=None):
  P=self.caches[initiator];assert P
  old=self.actual.x[self.anchor].copy()
  for z in P:P[z]+=1
  mx=max(P.values());oldest=[z for z in P if P[z]==mx]
  q=min(oldest) if partner is None else partner;assert q in oldest
  Q=self.caches[q]
  if reply is not None:t=reply
  elif initiator in Q:t=initiator
  elif policy is not None:t=policy(initiator,q)
  else:t=min(Q) if Q else None
  assert (t is None and not Q) or t in Q
  ta=Q.get(t)
  del P[q]
  if t is not None and t!=initiator:P[t]=min(P.get(t,ta),ta)
  vq=[]
  if initiator in Q:Q[initiator]=0
  else:
   if len(Q)>=self.capacity:
    assert t is not None;del Q[t];vq=[self.labels[t]]
   Q[initiator]=0
  rp=[self.anchor]+([] if t is None else [self.labels[t]])
  self.actual.step(self.labels[initiator],self.labels[q],[self.anchor],rp,vp=[],vq=vq)
  assert self.actual.universal(self.anchor)
  assert self.actual.x[self.anchor]==old
  for i,v in enumerate(self.labels):
   expected={self.anchor:0,**{self.labels[z]:age for z,age in self.caches[i].items()}}
   assert self.actual.x[v]==expected,(v,expected,self.actual.x[v])
  self.activations+=1;self.actual.embedding_steps+=1
 def canonical(self):
  for p in range(self.population):self.clear(p)
  assert self.all_ages_zero() and self.connected(range(self.population))
  if self.capacity==1:
   state=tuple(next(iter(r)) if r else -1 for r in self.caches)
   ms,canonical=to_path(state)
   for p in ms:self.activate(p)
   assert tuple(next(iter(r)) if r else -1 for r in self.caches)==canonical
   star=tuple([-1 if p==self.population-1 else self.population-1 for p in range(self.population)])
   sm,sc=to_path(star);assert sc==canonical
   inv=[];s=star
   for p in sm:
    inv.append(s[p]);s=tree_move(s,p)
   for p in reversed(inv):self.activate(p)
   assert tuple(next(iter(r)) if r else -1 for r in self.caches)==star
  else:self.canonicalize(range(self.population))
  assert not self.caches[-1] and self.all_ages_zero()

def tree_move(s,p):
 q=s[p]
 if q==-1:return s
 r=s[q];z=list(s);z[p]=-1 if r in (-1,p) else r;z[q]=p
 return tuple(z)

def to_path(state):
 m=len(state);moves=[];s=state
 def act(p):
  nonlocal s
  assert s[p]!=-1;s=tree_move(s,p);moves.append(p)
 def path():
  z=[];v=0
  while v!=-1:
   assert v not in z;z.append(v);v=s[v]
  return z
 order=path()
 while len(order)<m:
  p=next(p for p in range(m) if p not in order and s[p] in order)
  act(p);new=path();assert len(new)==len(order)+1;order=new
 for i in range(1,m):
  j=order.index(i)
  while j>i:
   x,u,v=order[j-2:j+1]
   for p in (x,x,u,v):act(p)
   order[j-1],order[j]=order[j],order[j-1];j-=1
 assert path()==list(range(m))
 return moves,s

def canonical_component(z,a,component,root):
 order=sorted(component-{root})+[root]
 r=Residual(z,a,order);r.canonical()
 assert z.x[root]=={a:0}

def merge(z,a,u,v):
 assert z.x[a]=={} and z.x[u]==z.x[v]=={a:0}
 assert z.universal(a)
 before=[r.copy() for r in z.x]
 expected=[({u:0},{},{a:0}),({u:0,v:0},{},{u:0}),({u:0},{},{u:0,a:0}),({},{a:0},{u:0,a:0})]
 for k,(p,q,extra,reply) in enumerate(((u,a,[],[]),(v,a,[],[u]),(a,v,[u],[u]),(a,u,[],[]))):
  z.step(p,q,extra,reply,[],[]);z.merge_steps+=1
  assert (z.x[a],z.x[u],z.x[v])==expected[k]
  assert all(z.x[w]==before[w] for w in range(z.n) if w not in (a,u,v))
 assert z.universal(a) and z.x[a]=={}

def construct(z,a):
 assert z.universal(a)
 while z.x[a]:
  q=max(z.x[a],key=lambda q:(z.x[a][q],-q))
  comp=next(s for s in z.components(a) if q in s)
  canonical_component(z,a,comp,q)
  extra=sorted(set(z.x[a])-{q})[:1]
  before=len(z.x[a]);z.step(a,q,extra,[a],[],[])
  assert len(z.x[a])==before-1 and z.universal(a)
 comps=z.components(a)
 roots=[]
 for comp in comps:
  root=max(comp);canonical_component(z,a,comp,root);roots.append(root)
 if roots:
  u=roots[0]
  for v in roots[1:]:merge(z,a,u,v)
 assert len(z.components(a))==1
 W=set(range(z.n))-{a};canonical_component(z,a,W,max(W))
 order=sorted(W)+[a]
 for k,v in enumerate(order):
  expected={u:0 for u in order[max(k+1,len(order)-z.c):]}
  assert z.x[v]==expected,(z.n,z.c,a,z.x,order,v,expected)
 assert z.universal(a) and z.x[a]=={}

def trial(n,c,seed,age_bound):
 rng=Random(seed);a=rng.randrange(n);W=[p for p in range(n) if p!=a]
 # Random residual partition supplies both connected and disconnected cases.
 groups=[[] for _ in range(rng.randint(1,len(W)))]
 rng.shuffle(W)
 for i,p in enumerate(W):groups[i%len(groups)].append(p)
 x=[{} for _ in range(n)]
 for group in groups:
  for i,p in enumerate(group):
   peers=[q for q in group if q!=p];rng.shuffle(peers)
   chosen=peers[:rng.randint(0,min(c-1,len(peers)))];x[p]={a:0,**{q:rng.randint(0,age_bound) for q in chosen}}
 x[a]={q:rng.randint(0,age_bound) for q in rng.sample(W,rng.randint(0,c))}
 z=Actual(x,c);construct(z,a)
 return z

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--max-n',type=int,default=10);ap.add_argument('--seeds',type=int,default=8);args=ap.parse_args()
 if args.max_n<3 or args.seeds<1:ap.error('require --max-n >= 3 and --seeds >= 1')
 if not __debug__:ap.error('assertions must be enabled; do not use python -O')
 count=steps=embedding=merges=0;worst=(0,None)
 for n in range(3,args.max_n+1):
  for c in range(2,n):
   for age in (0,1000000):
    for seed in range(args.seeds):
     z=trial(n,c,seed,age);count+=1;steps+=z.steps;embedding+=z.embedding_steps;merges+=z.merge_steps
     if z.steps>worst[0]:worst=(z.steps,(n,c,seed,age))
 print('PASS',count,'initializations','actual_exchanges',steps,'residual_embedding_exchanges',embedding,'four_event_merge_exchanges',merges,'worst',worst)
if __name__=='__main__':main()
