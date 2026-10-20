#!/usr/bin/env python3
"""Exact checks for the large-shuffle conditional-nonconvergence construction.

Scope: fixed 3 <= shuffle length <= capacity, iid uniform initiators,
uniform oldest ties, uniform packet subsets, and independent uniform
victim sets among sent entries. Incoming duplicates are discarded before
victim selection; their resident copies remain eligible victims. Both a
weakly connected construction and a strongly connected construction are
checked. All initial caches are full and all ages zero.

The proof is algebraic for arbitrary parameters. These checks corroborate
its two cache constructions, exact two-exchange certificates, probabilities,
partition closure and thresholds across 39 parameter choices: every
3 <= shuffle length <= capacity <= 10, plus (20, 5), (20, 20), (50, 5).
They do not replace the arbitrary-size proof.

With M = 2(capacity + 2) and
D = capacity * C(capacity - 1, length - 1) * C(capacity, length)
    * (length - 1) * C(length, 2),
the weak construction's isolation probability is 1 / (M^2 D^2), independent
of total peers. A sufficient size for conditional nonconvergence is
max(3*capacity + 5, (capacity + 2)*(capacity + 1)*M^2*D^2 + 2).
The case capacity = length = 3 gives probability 1/32400 and size 648002.

The strong construction has the rigorous isolation-probability lower bound
1 / ((capacity + 2)*M^2*D^2), and sufficient size
max(3*capacity + 5, (capacity + 2)^2*(capacity + 1)*M^2*D^2 + 2).
For capacity = length = 3 these are 1/162000 and 3240002.
The additional probability factor follows from the symbolic Poisson-clock
argument documented below; finite cache checks do not prove that bound.
"""
from fractions import Fraction
from math import comb
from collections import deque

def make(c,ell,n,strong=False):
 assert 3<=ell<=c and n>=3*c+5
 p,q=0,1;a=list(range(2,c+2));v,w=c+2,c+3;b=list(range(c+4,2*c+4));M=2*c+4
 A={p,q,*a};B={v,w,*b};cs=[{} for _ in range(n)]
 cs[p]=dict.fromkeys({q,v,*a[:c-2]},0);cs[q]=dict.fromkeys({v,*a[1:]},0)
 cs[v]=dict.fromkeys({w,a[0],*b[:c-2]},0);cs[w]=dict.fromkeys({a[0],*b[1:]},0)
 for x in a:cs[x]=dict.fromkeys(A-{x,q},0)
 for x in b:cs[x]=dict.fromkeys(B-{x,w},0)
 del cs[b[-1]][b[0]];cs[b[-1]][M]=0
 o=n-M
 for k in range(o):cs[M+k]={M+(k+h)%o:0 for h in range(1,c+1)}
 if strong:
  # The +1 cycle remains intact. This single gateway gives O a return edge
  # to the core, while the original bc -> M edge leads from the core to O.
  del cs[M][M+2]
  cs[M][b[-1]]=0
 assert all(len(cc)==c and i not in cc for i,cc in enumerate(cs))
 return cs,(p,q,a,v,w,b,M,A,B)

def reach(cs,start,vertices,directed=False):
 vs=set(vertices);seen={start};todo=deque([start])
 while todo:
  p=todo.popleft();adj=set(cs[p])&vs
  if not directed:adj|={q for q in vs if p in cs[q]}
  for q in adj-seen:seen.add(q);todo.append(q)
 return seen

def move(cs,p,q,extra,reply,vp,vq,c,ell,M):
 assert len(cs[p])==c and len(cs[q])==c
 oldest=max(cs[p].values());ties={x for x,z in cs[p].items() if z==oldest};assert q in ties
 assert len(extra)==ell-1 and extra<=set(cs[p])-{q}
 assert len(reply)==ell and reply<=set(cs[q])
 probability=Fraction(1,M*len(ties)*comb(c-1,ell-1)*comb(c,ell))
 for x in cs[p]:cs[p][x]+=1
 packet={p:0,**{x:cs[p][x] for x in extra}};response={x:cs[q][x] for x in reply}
 del cs[p][q]
 inp={x:z for x,z in response.items() if x!=p and x not in cs[p]}
 inq={x:z for x,z in packet.items() if x!=q and x not in cs[q]}
 np=max(0,len(inp)-(c-len(cs[p])));nq=max(0,len(inq)-(c-len(cs[q])))
 assert len(vp)==np and vp<=extra and vp<=set(cs[p])
 assert len(vq)==nq and vq<=reply
 probability/=comb(len(extra),np)*comb(len(reply),nq)
 for x in vp:del cs[p][x]
 for x in vq:del cs[q][x]
 cs[p].update(inp);cs[q].update(inq)
 assert len(cs[p])==c and len(cs[q])==c
 return probability

def check(c,ell,strong=False):
 n=3*c+5;cs,data=make(c,ell,n,strong);p,q,a,v,w,b,M,A,B=data
 assert reach(cs,p,range(n))==set(range(n))
 assert all(reach(cs,x,range(M),True)==set(range(M)) for x in range(M))
 if strong:
  assert all(reach(cs,x,range(n),True)==set(range(n)) for x in range(n))
  assert set(cs[M])&set(range(M))=={b[-1]}
  assert all(not(set(cs[x])&set(range(M))) for x in range(M+1,n))
 else:
  assert all(not(set(cs[x])&set(range(M))) for x in range(M,n))
 ra=set(a[1:1+ell-3]);rb=set(b[1:1+ell-3])
 assert len(ra)==len(rb)==ell-3
 prob=move(cs,v,w,{a[0],b[0]}|rb,{a[0],b[-2],b[-1]}|rb,{a[0]},{a[0],b[-2]},c,ell,M)
 assert set(cs[v])==set(b)
 prob*=move(cs,p,q,{v,a[0]}|ra,{v,a[-2],a[-1]}|ra,{v},{v,a[-2]},c,ell,M)
 assert set(cs[p])==set(a)
 assert all(set(cs[x])<=A for x in A)
 assert all(not(set(cs[x])&A) for x in range(n) if x not in A)
 assert reach(cs,p,range(n))==A
 den=c*comb(c-1,ell-1)*comb(c,ell)*(ell-1)*comb(ell,2)
 core_prefix=Fraction(1,M*M*den*den);assert prob==core_prefix
 if strong:
  # Symbolic argument, separate from the finite state checks above:
  # use independent rate-one Poisson clocks at every vertex. The second
  # core activation time tau has mean 2/M and is independent of all outside
  # clocks. In an unmodified, standalone cyclic outside overlay, rotational
  # symmetry gives E[indegree(gateway,t)] <= c. The counting intensity of
  # outside events whose initiator or target is the gateway is therefore
  # at most 1 + indegree(gateway,t). Hence E[N_touch(tau)] <= 2(c+1)/M,
  # so P(N_touch(tau)=0) >= 1/(c+2). Until its first touch the actual gateway
  # modification has no effect on the outside process: its row is never
  # read. Conditional on the first two core initiator labels being v,p,
  # neither prescribed core exchange reads or exports an outside cache.
  # The same cache certificate therefore succeeds with the lower bound
  # below. This is a lower bound, not an exact finite-prefix probability.
  expected=core_prefix/(c+2)
  threshold=max(3*c+5,(c+2)**2*(c+1)*M*M*den*den+2)
 else:
  expected=core_prefix
  threshold=max(3*c+5,(c+2)*(c+1)*M*M*den*den+2)
 assert expected-Fraction((c+2)*(c+1),threshold-1)>0
 return expected,threshold

if __name__=='__main__':
 trials=[]
 for c in range(3,11):
  for ell in range(3,c+1):
   trials.append((c,ell,check(c,ell),check(c,ell,True)))
 for c,ell in ((20,5),(20,20),(50,5)):
  trials.append((c,ell,check(c,ell),check(c,ell,True)))
 print('all_parameter_checks_passed',len(trials),'weak_and_strong_constructions',2*len(trials))
 for c,ell,weak,strong in trials:
  if (c,ell) in ((3,3),(4,3),(20,5)):
   print('c',c,'ell',ell,'weak_probability',weak[0],'weak_threshold',weak[1],
         'strong_probability_lower_bound',strong[0],'strong_threshold',strong[1])
