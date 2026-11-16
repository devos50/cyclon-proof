#!/usr/bin/env python3
"""Exact finite corroboration for the c=L=1 comparison proof.

Enumerates rooted trees by Prüfer codes, all elementary down-up exchanges,
and all root choices. Verifies rotation legality, endpoints, path-length
bound, common-forest property, killed-chain lift mapping and multiplicity.
This corroborates finite instances, not the arbitrary-n mathematical proof.
No third-party packages or external data files required.
"""
import argparse
import itertools
import heapq
from collections import deque


def rooted_trees(n):
 for code in itertools.product(range(n),repeat=n-2):
  deg=[1]*n
  for x in code:deg[x]+=1
  leaves=[i for i in range(n) if deg[i]==1];heapq.heapify(leaves);adj=[[] for _ in range(n)]
  for x in code:
   y=heapq.heappop(leaves);adj[x].append(y);adj[y].append(x);deg[x]-=1
   if deg[x]==1:heapq.heappush(leaves,x)
  x,y=leaves;adj[x].append(y);adj[y].append(x)
  for root in range(n):
   p=[-2]*n;p[root]=-1;todo=[root]
   for v in todo:
    for w in adj[v]:
     if p[w]==-2:p[w]=v;todo.append(w)
   yield tuple(p)

def edges(p):return {tuple(sorted((i,j))) for i,j in enumerate(p) if j>=0}
def path(E,s,t):
 adj={i:[] for e in E for i in e}
 for a,b in E:adj[a].append(b);adj[b].append(a)
 prev={s:None};queue=[s]
 for a in queue:
  if a==t:break
  for b in adj[a]:
   if b not in prev:prev[b]=a;queue.append(b)
 out=[];x=t
 while x is not None:out.append(x);x=prev[x]
 return out[::-1]

def simulate(p,e,f,rf):
 p=list(p);T=edges(p);u,v=e;a,b=f
 # orient e to have a in u component
 F=T-{e};A={u};todo=[u]
 for x in todo:
  for ee in F:
   if x in ee:
    y=ee[0] if ee[1]==x else ee[1]
    if y not in A:A.add(y);todo.append(y)
 if a not in A:a,b=b,a
 hist=[tuple(p)]
 def act(x):
  q=p[x];assert q>=0;r=p[q];p[q]=x;p[x]=r;hist.append(tuple(p))
 def rootmove(r):
  for x in path(edges(p),p.index(-1),r)[1:]:act(x)
 rootmove(v)
 for x in path(T,u,a)[1:]:act(x)
 rootmove(a)
 for x in path(T,v,b)[1:]:act(x)
 rootmove(rf)
 assert len(hist)-1<=3*(len(p)-1)
 assert edges(p)==F|{tuple(sorted((a,b)))} and p.index(-1)==rf
 assert all(F <= edges(z) and len(edges(z)-T)<=1 and len(T-edges(z))<=1 for z in hist)
 return hist

parser=argparse.ArgumentParser();parser.add_argument("--max-n",type=int,default=5);args=parser.parse_args()
for n in range(2,args.max_n+1):
 states=list(rooted_trees(n));count=0;mx=0
 for p in states:
  T=edges(p)
  for e in sorted(T):
   F=T-{e};u,v=e
   for a in range(n):
    for b in range(a+1,n):
     if (a,b) in F:continue
     # disconnected iff graph after adding remains tree
     E=F|{(a,b)}
     try:path(E,0,n-1)
     except (KeyError,ValueError):continue
     seen={0};todo=[0]
     for x in todo:
      for ee in E:
       if x in ee:
        y=ee[0] if ee[1]==x else ee[1]
        if y not in seen:seen.add(y);todo.append(y)
     if len(seen)<n:continue
     for rf in range(n):
      hist=simulate(p,e,(a,b),rf);count+=1;mx=max(mx,len(hist)-1)
 print(n,'checked',count,'maxlength',mx,flush=True)

from collections import Counter

def act(z,p):
 z=list(z);q=z[p]
 if q<0:return tuple(z)
 r=z[q];z[q]=p;z[p]=-1 if r==p else r
 return tuple(z)
def project(t,a):
 z=list(t);r=z.index(-1)
 if r!=a:z[r]=a
 return tuple(z)
for n in range(2,args.max_n+1):
 ts=list(rooted_trees(n));mult=Counter();checks=0
 for tt in ts:
  t=tuple(tt);r=t.index(-1)
  for a in range(n):
   u=project(t,a)
   for p in range(n):
    nt=act(t,p);v=project(nt,a)
    if u==v or (-1 in u and -1 in v):continue
    if -1 not in u:
     assert v==act(u,p),(n,t,a,p,u,v,act(u,p))
    else:
     assert act(v,r)==u
    edge=tuple(sorted((u,v)));mult[edge]+=1;checks+=1
 # each undirected referenceedge counted both directions
 mx=max(mult.values())//2
 assert mx<=n
 print(n,'legal projected steps',checks,'max undirected multiplicity',mx,flush=True)

# Exact stationary-depth counting and Dirichlet-energy corroboration.
from fractions import Fraction
from math import prod

def depth(p):
    k = 0
    v = 0
    while p[v] >= 0:
        k += 1
        v = p[v]
    return k

for n in range(2, args.max_n + 1):
    states = list(rooted_trees(n))
    hist = [0] * n
    squared_changes = 0
    total_depth = 0
    for p in states:
        d = depth(p)
        hist[d] += 1
        total_depth += d
        decreasing = 0
        for initiator in range(n):
            delta = depth(act(p, initiator)) - d
            assert abs(delta) <= 1
            squared_changes += delta * delta
            decreasing += delta == -1
        assert decreasing == d
    assert squared_changes == 2 * total_depth
    for k, count in enumerate(hist):
        probability = Fraction((k + 1) * prod(range(n - k, n)), n ** (k + 1))
        assert count == len(states) * probability
    print(n, 'depth counts', hist, 'energy identity', squared_changes, '=', 2 * total_depth, flush=True)
