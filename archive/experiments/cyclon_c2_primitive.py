from itertools import combinations
from collections import deque

def moves(st,protected=True):
 for p,cp0 in enumerate(st):
  if not cp0: continue
  M=max(a for v,a in cp0)
  for q,aq in cp0:
   if aq!=M:continue
   P={v:a+1 for v,a in cp0 if v!=q};out={p:0,**P};Q=dict(st[q]);rep=Q
   Ip={v:a for v,a in rep.items() if v!=p and v not in P}
   Iq={v:a for v,a in out.items() if v!=q and v not in Q}
   kp=max(0,len(Ip)-(2-len(P)));kq=max(0,len(Iq)-(2-len(Q)))
   ep=[v for v in P if not protected or v not in rep]
   eq=[v for v in rep if not protected or v not in out]
   for vp in combinations(ep,kp):
    for vq in combinations(eq,kq):
     rows=list(st);rows[p]=tuple(sorted([(v,a) for v,a in P.items() if v not in vp]+list(Ip.items())));rows[q]=tuple(sorted([(v,a) for v,a in Q.items() if v not in vq]+list(Iq.items())))
     yield tuple(rows),(p,q,vp,vq)

def bfs(start,goal,lim=3000000,maxdepth=30):
 seen={start:None};queue=deque([(start,0)])
 while queue and len(seen)<lim:
  st,d=queue.popleft()
  if st==goal:
   path=[]
   while seen[st]:
    prev,m=seen[st];path.append((m,st));st=prev
   return len(seen),list(reversed(path))
  if d==maxdepth:continue
  for ns,m in moves(st):
   if ns not in seen:seen[ns]=(st,m);queue.append((ns,d+1))
 return len(seen),None
if __name__=='__main__':
 # A0,R1,S2,P3
 start=(((2,0),),((0,0),(2,0)),(),((1,0),(2,0)))
 goal=(((2,0),),((0,0),(2,0)),(),((0,0),(2,0)))
 n,path=bfs(start,goal)
 print('seen',n,'length',None if path is None else len(path))
 for m,st in path or []:print(m,st)
