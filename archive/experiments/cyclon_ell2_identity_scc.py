#!/usr/bin/env python3
"""ID-level feasibility graph; partners are arbitrary cache entries.
This overapproximates the age-driven chain: SCC results are not age-realizability
or convergence proofs. Exact buffers and victim rules are retained.
"""
from itertools import combinations,product
from collections import Counter
import sys,time
POP=[bin(m).count("1") for m in range(1<<10)]


def bits(m):
 while m:
  v=m&-m;yield v;m-=v

def subsets(m,k):
 return [sum(xs) for xs in combinations(list(bits(m)),k)]

def connected(code,n):
 full=(1<<n)-1;seen=1
 while True:
  old=seen
  for p in range(n):
   row=(code>>(n*p))&full
   if seen>>p&1:seen|=row
   elif row&seen:seen|=1<<p
  if seen==old:return seen==full

def graph(n,c,protected=False):
 start=time.monotonic();allm=(1<<n)-1
 choices=[[m<<(n*p) for m in range(1<<n) if not(m>>p&1) and POP[m]<=c] for p in range(n)]
 states=[sum(rows) for rows in product(*choices) if connected(sum(rows),n)]
 ids={s:i for i,s in enumerate(states)};adj=[];rev=[[] for _ in states]
 replies={m:subsets(m,min(2,POP[m])) for m in range(1<<n)}
 for ix,s in enumerate(states):
  outs=set()
  for p in range(n):
   P=(s>>(n*p))&allm
   if not P:outs.add(ix);continue
   for qb in bits(P):
    q=qb.bit_length()-1;Q=(s>>(n*q))&allm;pr=P&~qb
    for extra in (list(bits(pr)) if pr else [0]):
     out=(1<<p)|extra
     for reply in replies[Q]:
      ip=reply&~((1<<p)|pr);iq=out&~Q
      np=max(0,POP[ip]-(c-POP[pr]));nq=max(0,POP[iq]-(c-POP[Q]))
      ep=extra&~reply if protected else extra
      eq=reply&~out if protected else reply
      for vp in subsets(ep,np):
       for vq in subsets(eq,nq):
        pnew=(pr&~vp)|ip;qnew=(Q&~vq)|iq
        mask=(allm<<(n*p))|(allm<<(n*q))
        t=(s&~mask)|(pnew<<(n*p))|(qnew<<(n*q))
        j=ids.get(t)
        assert j is not None,(n,c,s,p,q,extra,reply,t)
        outs.add(j)
  a=list(outs);adj.append(a)
  for j in a:rev[j].append(ix)
  if ix and ix%50000==0:print('progress',n,c,protected,ix,len(states),round(time.monotonic()-start,2),flush=True)
 print('graph',n,c,protected,'states',len(states),'arcs',sum(map(len,adj)),'seconds',round(time.monotonic()-start,2),flush=True)
 seen=bytearray(len(states));order=[]
 for root in range(len(states)):
  if seen[root]:continue
  seen[root]=1;stack=[(root,0)]
  while stack:
   v,k=stack[-1]
   if k==len(adj[v]):order.append(v);stack.pop();continue
   w=adj[v][k];stack[-1]=(v,k+1)
   if not seen[w]:seen[w]=1;stack.append((w,0))
 comp=[-1]*len(states);components=[]
 for root in reversed(order):
  if comp[root]>=0:continue
  label=len(components);members=[];stack=[root];comp[root]=label
  while stack:
   v=stack.pop();members.append(v)
   for w in rev[v]:
    if comp[w]<0:comp[w]=label;stack.append(w)
  components.append(members)
 terminal=[k for k,members in enumerate(components) if all(comp[w]==k for v in members for w in adj[v])]
 print('SCC',n,c,protected,'count',len(components),'terminal_sizes',sorted(len(components[k]) for k in terminal),'size_histogram',dict(Counter(map(len,components))),flush=True)
 for k in terminal:
  stats=Counter()
  locals=Counter()
  for ix in components[k]:
   s=states[ix];ds=[POP[(s>>(p*n))&allm] for p in range(n)]
   stats[(min(ds),max(ds),ds.count(c),ds.count(0))]+=1
   row=s&allm
   for q in range(1,n):locals[q]+=bool(row>>q&1)
  print('terminal_stats',n,c,protected,dict(stats),'observer0_neighbor_counts',dict(locals),flush=True)
 return states,adj,comp,components,terminal

if __name__=='__main__':
 if len(sys.argv)>1:graph(int(sys.argv[1]),int(sys.argv[2]),bool(int(sys.argv[3])))
 else:
  for n,c in [(4,2),(4,3)]:
   for protected in (False,True):graph(n,c,protected)
