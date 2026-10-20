from itertools import combinations,product
from collections import defaultdict
import sys,time

def ss(z,k):return list(combinations(z,k))
def game(n,c,r=0):
 opts=[list(ss([q for q in range(n) if q!=p],k)) for p in range(n) for k in []]
 opts=[[frozenset(u) for k in range(c+1) for u in combinations([q for q in range(n) if q!=p],k)] for p in range(n)]
 st=list(product(*opts)); ix={x:i for i,x in enumerate(st)}
 wins={i:0 for i,x in enumerate(st) if not any(r in z for z in x)}
 loss=[];maxrank=0
 def outcomes(x,p,q):
  P=x[p];Q=x[q];rem=P-{q}
  for S in ss(list(rem),min(1,len(rem))):
   O={p}|set(S)
   for T in ss(list(Q),min(2,len(Q))):
    I=set(T)-{p}-rem;J=O-Q-{q}
    rp=max(0,len(rem)+len(I)-c);rq=max(0,len(Q)+len(J)-c)
    for VP in ss(S,rp):
     for VQ in ss(T,rq):
      y=list(x);y[p]=frozenset(rem-set(VP)|I);y[q]=frozenset(Q-set(VQ)|J)
      yield ix[tuple(y)]
 # reverse ANDOR dependencies each (state,p,q) succeeds once any successor wins
 remqs={}; prerev=defaultdict(set); success={}; actions=defaultdict(list)
 for i,x in enumerate(st):
  if i in wins:continue
  for p in range(n):
   if p==r or not x[p]:continue
   a=(i,p);remqs[a]=len(x[p]);actions[i].append(a)
   for q in x[p]:
    act=(i,p,q)
    targets=set(outcomes(x,p,q))
    for j in targets:prerev[j].add(act)
 # workqueue ranks preserves min? sufficient max
 queue=list(wins)
 for j in queue:
  rank=wins[j]
  for act in prerev[j]:
   if act in success:continue
   success[act]=True;i,p,q=act;a=i,p;remqs[a]-=1
   if remqs[a]==0 and i not in wins:
    wins[i]=rank+1;maxrank=max(maxrank,rank+1);queue.append(i)
 print(n,c,'states',len(st),'winning',len(wins),'maxrank',maxrank)
 for i in range(len(st)):
  if i not in wins:
   print('losing',st[i]);break
 return st,wins
if __name__=='__main__':game(int(sys.argv[1]),int(sys.argv[2]))
