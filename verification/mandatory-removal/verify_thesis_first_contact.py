#!/usr/bin/env python3
"""Exact checks for first contact with a frozen set under protected+MIN ell=2.

Run from the repository root:
    python3 verification/mandatory-removal/verify_thesis_first_contact.py

The reproduced default run passes 28,036 exhaustive outside-cache states
at n=3,4, every capacity, all nontrivial frozen sets containing the tracked
identity, and ages 0 or 1. These give 16,002 first contacts and 12,034
strict minimum-age raises, over 35,374 controlled activations and 15,520
minimum-copy reduction blocks. It also passes 1,365 reproducible random
states through n=15, every capacity, arbitrary frozen-set sizes, and ages
through 1,000,000: 768 first contacts and 597 raises, with at most 16
activations. An additional 455 cases start with minimum tracked age above
K and confirm reset-or-hit, taking 715 activations before first contact.
For a smaller run use --max-n 8 --seeds 2; --skip-exhaustive omits the
small exhaustive enumeration.

The minimum-copy controller is checked on exhaustive small outside-cache
states and reproducible random numerical-age states. A separate controller
checks the outside lexicographic reset-or-hit argument when a frozen identity
has minimum outside age above the proposed reset bound. The controller never
reads frozen caches: each witness stops as soon as the chosen oldest partner
is frozen, before its buffers or merge are evaluated. Counts therefore include
the terminating contact activation but no post-contact update. Frozen-cache
snapshots are used only by the verifier to check that they remain unchanged.

These checks corroborate the symbolic first-contact proof. They do not simulate
its enormous complete horizon or prove the arbitrary-size probability bound.
Only Python and the sibling anchor verifier are required. Do not use Python -O.
"""
from itertools import product,combinations
from random import Random
import argparse
from verify_thesis_anchor import Actual


def minimum(z,S,r):
 ages=[z.x[p][r] for p in S if r in z.x[p]]
 assert ages,'the frozen identity disappeared before first contact'
 return min(ages)


def min_count(z,S,r,m):return sum(z.x[p].get(r)==m for p in S)


def raise_minimum(z,G,r,rng):
 """Return (hit, event count, minimum-copy reduction blocks)."""
 S=set(range(z.n))-set(G);s=len(S);start=minimum(z,S,r)
 frozen={g:z.x[g].copy() for g in G};events=blocks=0
 while minimum(z,S,r)==start:
  p=rng.choice([p for p in sorted(S) if z.x[p].get(r)==start])
  count0=min_count(z,S,r,start);block=0
  while True:
   P=z.x[p];assert P.get(r)==start
   mx=max(P.values());q=rng.choice([q for q in P if P[q]==mx])
   events+=1;block+=1
   if q in G:
    assert block<=s+z.c and events<=s*(s+z.c)
    assert all(z.x[g]==frozen[g] for g in G)
    return True,events,blocks
   assert q!=r and len(P)>=2
   Q=z.x[q]
   if Q.get(r)==start:
    rest=[u for u in Q if u!=r]
    if rest:t=p if p in Q else rng.choice(rest);reply=[r,t]
    else:reply=[r]
   else:reply=rng.sample(list(Q),min(2,len(Q)))
   min0=minimum(z,S,r)
   z.step(p,q,[r],reply)
   assert all(z.x[g]==frozen[g] for g in G)
   assert minimum(z,S,r)>=min0
   count1=min_count(z,S,r,start)
   if count1<count0:
    assert count1==count0-1
    assert z.x[p].get(r)!=start
    blocks+=1;break
   assert count1==count0 and z.x[p].get(r)==start
   assert block<=s+z.c
  assert block<=s+z.c and blocks<=s and events<=s*(s+z.c)
 assert minimum(z,S,r)>=start+1
 return False,events,blocks


def reset_or_hit(z,G,r,rng):
 """Check impossibility of resetting below K while outside min(r)>K."""
 S=set(range(z.n))-set(G);s=len(S);c=z.c
 H=(s*c+1)*(s*c*c+1)*(s*c*2**c+1);K=(s*c+1)*H
 assert minimum(z,S,r)>K
 a=next(j*H for j in range(s*c+1) if not any(j*H<age<=(j+1)*H for p in S for age in z.x[p].values()))
 threshold=a+H;frozen={g:z.x[g].copy() for g in G}
 def pick(xs,k):return rng.sample(list(xs),k)
 def phi():
  f={p:sum(age<=threshold for age in z.x[p].values()) for p in S}
  return (s*c-sum(f.values()),sum(v*v for v in f.values()),sum(sum(age>threshold for age in z.x[p].values())*2**(c-f[p]) for p in S)),f
 for t in range(H):
  before,fs=phi()
  oldholders=[p for p in S if any(age>threshold for age in z.x[p].values())]
  assert oldholders,'reset occurred despite the preserved large-age frozen identity'
  fmax=max(fs[p] for p in oldholders);p=rng.choice([p for p in oldholders if fs[p]==fmax])
  P=z.x[p];q=rng.choice([q for q in P if P[q]==max(P.values())])
  assert P[q]>threshold
  if q in G:
   assert all(z.x[g]==frozen[g] for g in G)
   return t+1
  Q=z.x[q];k=min(1,len(P)-1);m=min(2,len(Q))
  yp={v for v,age in P.items() if age<=threshold};yq={v for v,age in Q.items() if age<=threshold}
  missing=yp-yq;extra=pick(missing,1) if missing else []
  extra+=pick(set(P)-{q}-set(extra),k-len(extra));U={p}|set(extra)
  rq=max(0,len(Q)+len(U-set(Q))-c)
  E=(set(Q)&U)|{v for v in yq if v in set(P)|{p}}
  D=pick(set(Q)-E,rq);B=(set(extra)&yp&set(Q))|({p}&set(Q))
  T=D+list(B);T+=pick(set(Q)-set(T),m-len(T))
  rem=set(P)-{q};I=set(T)-rem-{p};rp=max(0,len(rem)+len(I)-c)
  eligible=set(extra)-set(T);old=[v for v in eligible if P[v]>threshold]
  VP=pick(old,min(rp,len(old)));VP+=pick(eligible-set(VP)-set(old),rp-len(VP))
  min0=minimum(z,S,r);z.step(p,q,extra,T,VP,D)
  after,_=phi();assert after<before
  assert minimum(z,S,r)>=min0>K
  assert all(z.x[g]==frozen[g] for g in G)
  assert all(age>threshold or age<=a+t+1 for p in S for age in z.x[p].values())
 raise AssertionError('the reset-or-hit controller exhausted H without hitting G')


def outside_rows(n,p,c):
 ids=[v for v in range(n) if v!=p]
 for vals in product(range(3),repeat=n-1):
  row={v:t-1 for v,t in zip(ids,vals) if t}
  if len(row)<=c:yield row


def exhaustive():
 cases=hits=raised=events=blocks=0
 for n in (3,4):
  r=n-1
  for c in range(2,n):
   for gnum in range(1,n):
    for rest in combinations(range(n-1),gnum-1):
     G={r,*rest};S=sorted(set(range(n))-G)
     for rows in product(*(list(outside_rows(n,p,c)) for p in S)):
      if not any(r in row for row in rows):continue
      x=[{} for _ in range(n)]
      for p,row in zip(S,rows):x[p]=row
      z=Actual(x,c);hit,ev,bl=raise_minimum(z,G,r,Random(cases))
      cases+=1;hits+=hit;raised+=not hit;events+=ev;blocks+=bl
 print('EXHAUSTIVE',cases,'first_contacts',hits,'minimum_raises',raised,'events',events,'mincopy_blocks',blocks,flush=True)
 return cases


def random_checks(max_n,seeds):
 cases=hits=raised=events=blocks=reset_cases=reset_events=0;worst=0
 for n in range(3,max_n+1):
  for c in range(2,n):
   for seed in range(seeds):
    for mode in ('mixed','all_minimum','unique_minimum'):
     rng=Random((n*100+c)*1000+seed*3+len(mode));gsize=rng.randint(1,n-1);G=set(rng.sample(range(n),gsize));r=rng.choice(sorted(G));S=sorted(set(range(n))-G)
     x=[{} for _ in range(n)]
     for p in range(n):
      ids=[v for v in range(n) if v!=p and (mode=='mixed' or p in G or v in set(S)|{r})]
      chosen=rng.sample(ids,rng.randint(0,min(c,len(ids))));x[p]={v:rng.randint(0,1000000) for v in chosen}
     if mode=='all_minimum':
      for p in S:
       if r not in x[p] and len(x[p])==c:del x[p][next(iter(x[p]))]
       x[p][r]=0
     else:
      p=rng.choice(S)
      if r not in x[p] and len(x[p])==c:del x[p][next(iter(x[p]))]
      x[p][r]=0
      if mode=='unique_minimum' and len(S)>=2:
       q=rng.choice([q for q in S if q!=p]);x[p]={r:0,q:1000001}
       for u in S:
        if u!=p and r in x[u]:x[u][r]=rng.randint(1,1000000)
     z=Actual(x,c);hit,ev,bl=raise_minimum(z,G,r,rng)
     cases+=1;hits+=hit;raised+=not hit;events+=ev;blocks+=bl;worst=max(worst,ev)
    # Large min(r) makes a successful age reset impossible before first contact.
    rng=Random((n*100+c)*1000+seed);G=set(rng.sample(range(n),rng.randint(1,n-1)));r=rng.choice(sorted(G));S=sorted(set(range(n))-G);s=len(S)
    H=(s*c+1)*(s*c*c+1)*(s*c*2**c+1);K=(s*c+1)*H;x=[{} for _ in range(n)]
    for p in S:
     others=[q for q in range(n) if q not in (p,r)];rng.shuffle(others)
     x[p]={r:K+1,**{q:(2*K+rng.randint(1,1000000) if rng.randrange(2) else rng.randint(0,H)) for q in others[:rng.randint(0,min(c-1,len(others)))]}}
    z=Actual(x,c);ev=reset_or_hit(z,G,r,rng);reset_cases+=1;reset_events+=ev
 print('RANDOM',cases,'first_contacts',hits,'minimum_raises',raised,'events',events,'mincopy_blocks',blocks,'maximum_events',worst,flush=True)
 print('RESET_OR_HIT',reset_cases,'events_to_first_contact',reset_events,flush=True)


def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--max-n',type=int,default=15);ap.add_argument('--seeds',type=int,default=5);ap.add_argument('--skip-exhaustive',action='store_true');args=ap.parse_args()
 if args.max_n<3 or args.seeds<1 or not __debug__:ap.error('require max-n>=3, seeds>=1, and enabled assertions')
 if not args.skip_exhaustive:exhaustive()
 random_checks(args.max_n,args.seeds)
if __name__=='__main__':main()
