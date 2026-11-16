#!/usr/bin/env python3
"""Exhaustive local F/V audit allowing an OLD frozen responder.
Unlike the original reset checker, the responder may have more young
entries than the active peer while still holding old entries. Every
controller completion must preserve F; on F plateaus it must decrease V
or preserve all young sets. W need not descend at this exceptional owner.
This finite colored audit is not a proof of arbitrary-parameter extinction.
"""
from itertools import product,combinations
from collections import Counter
import argparse
from time import monotonic

def choose(xs,k):return combinations(tuple(sorted(xs)),k)
def rows(n,owner,c):
 ids=[z for z in range(n) if z!=owner]
 for vals in product(range(3),repeat=n-1):
  r={z:t for z,t in zip(ids,vals) if t}
  if len(r)<=c:yield r

def step_options(P,Q,c,ell):
 p,q=0,1;a,b=len(P),len(Q)
 assert P.get(q)==1
 yp={z for z in P if P[z]==2};yq={z for z in Q if Q[z]==2}
 k=min(ell-1,a-1);m=min(ell,b)
 missing=yp-yq
 for ss in choose(set(P)-{q},k):
  S=set(ss)
  if missing and not S&missing:continue
  U={p}|S;J=U-set(Q);rq=max(0,b+len(J)-c)
  excluded=(set(Q)&U)|{z for z in yq if z in set(P)|{p}}
  B=({z for z in S if P[z]==2}&set(Q))|({p}&set(Q))
  for dd in choose(set(Q)-excluded,rq):
   D=set(dd);required=D|B
   assert len(required)<=m,(P,Q,c,ell,S,D,B)
   for fill in choose(set(Q)-required,m-len(required)):
    T=required|set(fill)
    rem={z:t for z,t in P.items() if z!=q}
    I=T-(set(rem)|{p});rp=max(0,len(rem)+len(I)-c)
    eligible=S-T
    eo={z for z in eligible if P[z]==1};ey=eligible-eo
    oldnum=min(rp,len(eo));youngnum=rp-oldnum
    assert youngnum<=len(ey),(P,Q,c,ell,S,D,T,rp,eligible)
    for vpold in choose(eo,oldnum):
     for vpyoung in choose(ey,youngnum):
      vp=set(vpold)|set(vpyoung)
      A={z:t for z,t in rem.items() if z not in vp}
      C={z:t for z,t in Q.items() if z not in D}
      for z in T:
       if z!=p:A[z]=max(A.get(z,0),Q[z])
      outgoing={p:2,**{z:P[z] for z in S}}
      for z,t in outgoing.items():
       if z!=q:C[z]=max(C.get(z,0),t)
      assert len(A)<=c and len(C)<=c
      assert (set(T)-{p})<=set(A)
      assert (U-{q})<=set(C)
      yield A,C,(S,D,T,vp)

def audit(n,c,ell):
 rsP=[P for P in rows(n,0,c) if P.get(1)==1];rsQ=list(rows(n,1,c))
 pairs=moves=0;kinds=Counter();start=monotonic()
 for P in rsP:
  fP=sum(t==2 for t in P.values());oP=len(P)-fP
  for Q in rsQ:
   fQ=sum(t==2 for t in Q.values());oQ=len(Q)-fQ
   pairs+=1;count=0
   before=(2*c-fP-fQ,fP*fP+fQ*fQ,oP*ell**(c-fP)+oQ*ell**(c-fQ))
   for A,C,ctrl in step_options(P,Q,c,ell):
    fa=sum(t==2 for t in A.values());fc=sum(t==2 for t in C.values());oa=len(A)-fa;oc=len(C)-fc
    after=(2*c-fa-fc,fa*fa+fc*fc,oa*ell**(c-fa)+oc*ell**(c-fc))
    assert after[:2]<=before[:2],(n,c,ell,P,Q,ctrl,A,C,before,after)
    if after[0]<before[0]:kind='F'
    elif after[1]<before[1]:kind='V'
    elif after[2]<before[2]:kind='W'
    else:kind='OWNER_EXCEPTION'
    kinds[kind]+=1;moves+=1;count+=1
    if kind!='F':
     yp={z for z,t in P.items() if t==2};yq={z for z,t in Q.items() if t==2}
     assert yp<=yq and 0 in yq
     tv=sum(Q[z]==2 for z in ctrl[1])
     assert fa==fP+tv and fc==fQ-tv
     assert tv<=fQ-fP-1
     if after[:2]==before[:2]:
      assert tv==0
      assert {z for z,t in A.items() if t==2}==yp
      assert {z for z,t in C.items() if t==2}==yq
      assert fQ>fP
   assert count,(n,c,ell,P,Q)
 print(n,c,ell,'localpairs',pairs,'controlledmoves',moves,'progress',dict(kinds),'seconds',round(monotonic()-start,3),flush=True)
 return pairs,moves,kinds

def large_transfer_checks():
 """Check the explicit F-plateau family with t=length-1 transfers."""
 count=0;largest=0
 for c in range(2,21):
  for ell in range(2,c+1):
   P={j:1 for j in range(1,c+1)}
   Q={0:2,**{j:2 for j in range(c+1,2*c)}}
   A,C,ctrl=next(step_options(P,Q,c,ell))
   fa=sum(t==2 for t in A.values());fc=sum(t==2 for t in C.values())
   assert fa+fc==c and fa==ell-1 and fc==c-ell+1
   assert fa*fa+fc*fc<c*c
   assert sum(Q[z]==2 for z in ctrl[1])==ell-1
   count+=1;largest=max(largest,ell-1)
 print('LARGE_TRANSFER',count,'maximum_young_transfer',largest,flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--max-n',type=int,default=7)
 args=ap.parse_args()
 if args.max_n<3:ap.error('require --max-n >= 3')
 if not __debug__:ap.error('assertions must be enabled; do not use python -O')
 totals=Counter();pc=mc=0
 for n in range(3,args.max_n+1):
  for c in range(2,n):
   for ell in range(2,c+1):
    p,m,ks=audit(n,c,ell);pc+=p;mc+=m;totals.update(ks)
 print('TOTAL',pc,mc,dict(totals),flush=True)
 large_transfer_checks()
