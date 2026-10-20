from itertools import product,combinations
from collections import deque

def go(k,cap):
 alive={};pred={};succs={}
 for f in product(*[[q for q in range(k) if q!=p] for p in range(k)]):
  for a,b in combinations(range(k),2):
   for vals in product(range(cap+1),repeat=k+2):
    if min(vals)!=0:continue
    w=vals[:k];x,y=vals[k:];z=(f,a,b,w,x,y);succ=[]
    for q,e,qe,ee in ((a,b,x,y),(b,a,y,x)):
     if qe<ee:continue
     d=f[q]
     if d==e:continue
     g=list(f);g[q]=e;v=list(w);v[q]=ee+1
     uu,vv=sorted((e,d));xx,yy=(ee+1,w[q]) if uu==e else (w[q],ee+1)
     m=min(*v,xx,yy);v=[u-m for u in v];xx-=m;yy-=m
     if max(*v,xx,yy)>cap:continue
     succ.append((tuple(g),uu,vv,tuple(v),xx,yy))
    alive[z]=len(succ);succs[z]=succ
    for nz in succ:pred.setdefault(nz,[]).append(z)
 queue=deque(z for z,d in alive.items() if d==0);done=0
 while queue:
  nz=queue.popleft();done+=1
  for z in pred.get(nz,[]):
   alive[z]-=1
   if alive[z]==0:queue.append(z)
 print(k,cap,len(alive),'cycle_reachable',len(alive)-done,flush=True)
 if len(alive)>done:
  z=next(z for z in alive if alive[z]>0);path=[];seen={}
  while z not in seen:
   seen[z]=len(path);path.append(z)
   z=next(nz for nz in succs[z] if alive[nz]>0)
  cyc=path[seen[z]:];print('CYCLE',len(cyc),cyc,flush=True)
for k,cap in ((3,2),(3,3),(3,4),(4,2),(4,3)):go(k,cap)
