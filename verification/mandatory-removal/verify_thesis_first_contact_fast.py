#!/usr/bin/env python3
"""Exact-age controlled first-contact checks for protected+MIN CYCLON, ell=2.

This checks the polynomial holder-only controller, not arbitrary random runs.
The auxiliary OLD/YOUNG colors merge by YOUNG-OR independently of MIN age;
that proof bookkeeping is deliberately different from initial-lineage colors.
Checks include oldest partner legality, protected victims, nondecreasing holder
count, min-copy raising, YOUNG-count monotonicity, strict forced migrations,
and the uniform path bounds B=s(s+c), J=(sc+1)(2s+c), T=B(J+1)+J.

Default invocation:
    python verification/mandatory-removal/verify_thesis_first_contact_fast.py
Default coverage is n=3..15, all c=2..n-1, all outside sizes s=1..n-1,
five deterministic seeds and low/high tracked-identity age patterns: 9,100
cases, 21,507 exchanges, 4,746 high-age routing executions, 108 migrations,
2,296 completed minimum raises; maximum observed path length 41.
Add --zeroify to plant zero anchors on the frozen nonowner peers and positive
tracked copies outside, execute the terminal exchange, and when needed execute
the owner-only callback until ANY nonholder receives the fresh anchor. This
also checks H_end>=H_start, strict zero-copy gain, and preservation of every
initial zero. Default --zeroify coverage: 9,100 cases, 32,008 exchanges,
4,746 routing executions, 108 migrations, 1,918 completed minimum raises;
maximum observed block length 56. The controller uses deterministic seeds.

A shorter invocation is --max-n 8 --seeds 2. Numeric checks complement the
proof; they do not establish the theorem for arbitrary configurations.
"""
import argparse
from random import Random

def run(n,c,s,seed,high=False,zeroify=False):
 rng=Random(seed);Sset=set(range(s));G=set(range(s,n));r=s
 J=(s*c+1)*(2*s+c);B=s*(s+c);Tmax=B*(J+1)+J
 X=[]
 for p in range(n):
  ids=[q for q in range(n) if q!=p];rng.shuffle(ids)
  P={q:(rng.randrange(1000*J+1),True) for q in ids[:rng.randrange(c+1)]}
  if p in Sset and rng.randrange(2)==0:
   if r not in P and len(P)==c:P.pop(next(iter(P)))
   P[r]=(J+1+rng.randrange(J+1) if high else rng.randrange(5),True)
  X.append(P)
 if not any(r in X[p] for p in Sset):
  p=rng.randrange(s)
  if len(X[p])==c:X[p].pop(next(iter(X[p])))
  X[p][r]=(J+1 if high else 0,True)
 if zeroify:
  for p in Sset:
   if r in X[p]:X[p][r]=(max(1,X[p][r][0]),True)
  for p in G-{r}:
   if r not in X[p] and len(X[p])==c:X[p].pop(next(iter(X[p])))
   X[p][r]=(0,True)
 initial_h=sum(r in P for P in X)
 initial_z=sum(r in P and P[r][0]==0 for P in X)
 frozen_zeros={p for p,P in enumerate(X) if r in P and P[r][0]==0}
 t=0;migs=0;epochs=0;route_steps=0
 def pick(z,k):
  z=list(z);rng.shuffle(z);assert len(z)>=k;return z[:k]
 def holdercount():return sum(r in P for P in X)
 def minr():return min(X[p][r][0] for p in Sset if r in X[p])
 def young():return sum(not v[1] for p in Sset for v in X[p].values())
 def merge(v,w):return (min(v[0],w[0]), v[1] and w[1])
 def select(p):return pick([q for q in X[p] if X[p][q][0]==max(v[0] for v in X[p].values())],1)[0]
 def step(p,q,routing=False):
  nonlocal t,migs
  P=X[p];Q=X[q];assert r in P and q!=r
  out={p:(0,False),r:(P[r][0]+1,P[r][1])}
  rq=max(0,len(Q)+len(set(out)-set(Q))-c)
  known=[z for z in (p,r) if z in Q]
  if len(known)==2:T=[p,r];DQ=[];assert rq==0
  elif len(known)==1:
   z=known[0];cand=[u for u in Q if u!=z]
   if rq:
    assert rq==1
    if routing:cand=[u for u in cand if Q[u][1] or (u not in P and u!=p)]
    DQ=pick(cand,1);T=[z]+DQ
   else:DQ=[];T=[z]+pick(cand,min(2,len(Q))-1)
  else:
   cand=list(Q)
   if routing:cand=[u for u in cand if Q[u][1] or (u not in P and u!=p)]
   DQ=pick(cand,rq);T=DQ+pick([u for u in Q if u not in DQ],min(2,len(Q))-len(DQ))
  reply={u:Q[u] for u in T if u!=p}
  rem={u:(v[0]+1,v[1]) for u,v in P.items() if u!=q}
  newids=set(reply)-set(rem);rp=max(0,len(rem)+len(newids)-c)
  eligible=[r] if r not in reply else []
  DP=pick(eligible,rp);forced=r in DP
  f0=young();hc=holdercount()
  NP={u:v for u,v in rem.items() if u not in DP}
  for u,v in reply.items():NP[u]=merge(NP[u],v) if u in NP else v
  NQ={u:v for u,v in Q.items() if u not in DQ}
  for u,v in out.items():NQ[u]=merge(NQ[u],v) if u in NQ else v
  X[p]=NP;X[q]=NQ;t+=1
  assert holdercount()>=hc
  assert set(DQ)<=set(T)-set(out)
  assert set(DP)<={r}-set(reply)
  assert len(NP)<=c and len(NQ)<=c
  if routing:
   assert P[q][1]
   assert all(v[0]<=route_steps+1 for u in Sset for v in X[u].values() if not v[1])
   assert all(X[u][r][1] for u in Sset if r in X[u])
   assert young()>=f0
   if forced:assert p not in Q and r not in Q and young()>f0;migs+=1
  return forced
 def arbitrary_step(p,q,extra=None,reply_ids=None):
  """One exact exchange used only for owner-terminal/callback checks."""
  nonlocal t
  P=X[p];Q=X[q]
  if extra is None:extra=pick([u for u in P if u!=q],min(1,len(P)-1))
  out={p:(0,False),**{u:(P[u][0]+1,P[u][1]) for u in extra}}
  if reply_ids is None:reply_ids=pick(Q,min(2,len(Q)))
  reply={u:Q[u] for u in reply_ids if u!=p}
  rq=max(0,len(Q)+len(set(out)-set(Q))-c)
  DQ=pick(set(reply_ids)-set(out),rq)
  rem={u:(v[0]+1,v[1]) for u,v in P.items() if u!=q}
  rp=max(0,len(rem)+len(set(reply)-set(rem))-c)
  DP=pick(set(extra)-set(reply),rp)
  NP={u:v for u,v in rem.items() if u not in DP}
  NQ={u:v for u,v in Q.items() if u not in DQ}
  for u,v in reply.items():NP[u]=merge(NP[u],v) if u in NP else v
  for u,v in out.items():NQ[u]=merge(NQ[u],v) if u in NQ else v
  X[p]=NP;X[q]=NQ;t+=1
  assert len(NP)<=c and len(NQ)<=c
  assert set(DP)<=set(extra)-set(reply)
  assert set(DQ)<=set(reply_ids)-set(out)
 def terminal(p,q):
  if not zeroify:return t+1
  if q!=r:
   step(p,q)
  else:
   arbitrary_step(p,q)
   assert r not in X[p] and p in X[r]
   for callback_step in range(n+c):
    q=select(r)
    stop=r not in X[q]
    extra=pick([u for u in X[r] if u!=q],min(1,len(X[r])-1)) if q==p else [p]
    if r in X[q]:
     rem=[u for u in X[q] if u!=r]
     other=[p] if p in rem else pick(rem,min(1,len(rem)))
     reply_ids=[r]+other
    else:reply_ids=None
    arbitrary_step(r,q,extra,reply_ids)
    assert all(r in X[z] and X[z][r][0]==0 for z in frozen_zeros)
    if stop:break
    assert p in X[r] and r not in X[p]
   else:raise AssertionError('owner callback exceeded n+c')
  assert holdercount()>=initial_h
  assert sum(r in P and P[r][0]==0 for P in X)>initial_z
  assert all(r in X[z] and X[z][r][0]==0 for z in frozen_zeros)
  return t
 while minr()<=J:
  m=minr();before=minr();epoch_steps=0
  while any(r in X[p] and X[p][r][0]==m for p in Sset):
   p=pick([p for p in Sset if r in X[p] and X[p][r][0]==m],1)[0]
   count=0
   while True:
    q=select(p)
    if q in G:return terminal(p,q),False,migs,epochs,route_steps
    h0=sum(r in X[u] and X[u][r][0]==m for u in Sset)
    step(p,q)
    count+=1;epoch_steps+=1
    assert count<=s+c
    assert minr()>=m
    h1=sum(r in X[u] and X[u][r][0]==m for u in Sset)
    assert h1<=h0
    if h1<h0:break
   assert epoch_steps<=B
  assert minr()>before;epochs+=1;assert epochs<=J+1
 for p in Sset:X[p]={u:(v[0],True) for u,v in X[p].items()}
 p=pick([p for p in Sset if r in X[p]],1)[0];segment=0
 while True:
  q=select(p)
  if q in G:
   assert route_steps+1<=J and t+1<=Tmax
   return terminal(p,q),True,migs,epochs,route_steps+1
  forced=step(p,q,routing=True);route_steps+=1;segment+=1
  assert route_steps<=J and segment<=2*s+c
  assert minr()>J and migs<=s*c
  if forced:p=q;segment=0

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--max-n',type=int,default=15)
 parser.add_argument('--seeds',type=int,default=5)
 parser.add_argument('--zeroify',action='store_true',help='also execute the terminal exchange and owner callback; verify H_end>=H_start and strict zero gain')
 args=parser.parse_args()
 cases=steps=fast=migs=ep=0;worst=(0,None)
 for n in range(3,args.max_n+1):
  for c in range(2,n):
   for s in range(1,n):
    for seed in range(args.seeds):
     for high in [False,True]:
      t,f,m,e,j=run(n,c,s,seed,high,args.zeroify);cases+=1;steps+=t;fast+=f;migs+=m;ep+=e
      if t>worst[0]:worst=t,(n,c,s,seed,high)
 print(f'cases={cases} exchanges={steps} routed={fast} migrations={migs} min_raises={ep} worst={worst}')
