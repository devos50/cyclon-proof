#!/usr/bin/env python3
from fractions import Fraction
from math import comb
from collections import deque

def make(n):
 assert n>=14
 c=[{1:0,5:0,2:0},{5:0,3:0,4:0},{0:0,1:0,3:0},{0:0,1:0,4:0},{0:0,1:0,2:0},
    {6:0,2:0,7:0},{2:0,8:0,9:0},{5:0,6:0,8:0},{5:0,6:0,10:0},{5:0,6:0,7:0}]
 m=n-10
 for k in range(m):c.append({10+(k+h)%m:0 for h in (1,2,3)})
 assert all(len(x)==3 and p not in x for p,x in enumerate(c))
 return c

def reach(c,start,directed=False,subset=None):
 vs=set(range(len(c))) if subset is None else set(subset)
 seen={start};todo=deque([start])
 while todo:
  p=todo.popleft();adj=set(c[p])&vs
  if not directed:adj|={q for q in vs if p in c[q]}
  for q in adj-seen:seen.add(q);todo.append(q)
 return seen

def move(c,p,q,victimp,victimq):
 # fullshuffle c=ell=3; explicit uniform choices.
 cap=3
 oldest=max(c[p].values());ties=[r for r,a in c[p].items() if a==oldest]
 assert q in ties
 prob=Fraction(1,10*len(ties)) # initiation conditional on core subsequence
 for r in c[p]:c[p][r]+=1
 extra={r:a for r,a in c[p].items() if r!=q};out={p:0,**extra}
 reply=dict(c[q]);del c[p][q]
 inp={r:a for r,a in reply.items() if r!=p and r not in c[p]}
 inq={r:a for r,a in out.items() if r!=q and r not in c[q]}
 needp=max(0,len(inp)-(cap-len(c[p])));needq=max(0,len(inq)-(cap-len(c[q])))
 assert len(victimp)==needp and set(victimp)<=set(extra)&set(c[p])
 assert len(victimq)==needq and set(victimq)<=set(reply)
 prob/=comb(len(extra),needp)*comb(len(reply),needq)
 for r in victimp:del c[p][r]
 for r in victimq:del c[q][r]
 c[p].update(inp);c[q].update(inq)
 assert all(len(x)<=3 and j not in x for j,x in enumerate(c))
 return prob

def check(n):
 c=make(n)
 assert len(reach(c,0))==n
 assert all(reach(c,p,True,range(10))==set(range(10)) for p in range(10))
 assert all(not (set(c[p])&set(range(10))) for p in range(10,n))
 prob=move(c,5,6,{2},{2,8})
 assert set(c[5])=={7,8,9} and set(c[6])=={9,5,7}
 prob*=move(c,0,1,{5},{5,3})
 assert prob==Fraction(1,32400)
 assert set(c[0])=={2,3,4} and set(c[1])=={4,0,2}
 s=set(range(5))
 assert all(set(c[p])<=s for p in s)
 assert all(not (set(c[p])&s) for p in range(5,n))
 assert reach(c,0)==s
 return prob

if __name__=='__main__':
 for n in (14,17,31):print('checked',n,'event_probability',check(n))
 p0=Fraction(1,32400);n=648002
 gap=p0-Fraction(20,n-1)
 assert gap>0
 print('strict_nonconvergence_threshold',n,'sum_TV_lower_bound',gap)
