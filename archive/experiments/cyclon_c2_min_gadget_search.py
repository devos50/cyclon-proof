from itertools import combinations
from collections import deque

def moves(st,active=None):
 for p,cp0 in enumerate(st):
  if active is not None and p not in active:continue
  if not cp0: continue
  M=max(a for v,a in cp0)
  for q,aq in cp0:
   if aq!=M:continue
   P={v:a+1 for v,a in cp0 if v!=q};out={p:0,**P};Q=dict(st[q]);rep=Q
   Ip={v:a for v,a in rep.items() if v!=p and v not in P}
   Iq={v:a for v,a in out.items() if v!=q and v not in Q}
   kp=max(0,len(Ip)-(2-len(P)));kq=max(0,len(Iq)-(2-len(Q)))
   ep=[v for v in P if v not in rep];eq=[v for v in rep if v not in out]
   for vp in combinations(ep,kp):
    for vq in combinations(eq,kq):
     A={v:a for v,a in P.items() if v not in vp};B={v:a for v,a in Q.items() if v not in vq}
     for v,a in rep.items():
      if v!=p:A[v]=min(A.get(v,a),a)
     for v,a in out.items():
      if v!=q:B[v]=min(B.get(v,a),a)
     rows=list(st);rows[p]=tuple(sorted(A.items()));rows[q]=tuple(sorted(B.items()))
     yield tuple(rows),(p,q,vp,vq)

def holders(st,a=0):return {p for p,c in enumerate(st) if p!=a and dict(c).get(a)==0}
def reach(st,a=0):
 R={a}
 while True:
  S=R|{q for p in R for q,a in st[p]}
  if R==S:return R
  R=S

def bfs(start,goal,active=None,lim=2000000,maxdepth=12,restriction=None):
 seen={start:None};queue=deque([(start,0)])
 while queue and len(seen)<lim:
  st,d=queue.popleft()
  if goal(st):
   path=[]
   while seen[st]:
    prev,m=seen[st];path.append((m,st));st=prev
   return len(seen),list(reversed(path))
  if d==maxdepth:continue
  for ns,m in moves(st,active):
   if restriction is not None and not restriction(ns):continue
   if ns not in seen:seen[ns]=(st,m);queue.append((ns,d+1))
 return len(seen),None
if __name__=='__main__':
 # a0,p1,x2,y3,t4,d5,e6. Only first3 act, allotherspassive.
 start=(((3,0),(4,0)),((0,0),(2,0)),((5,0),(6,0)),((0,0),),((0,0),),(),())
 I=holders(start);R=reach(start)
 goal=lambda st:len(holders(st))>len(I) or (I<=holders(st) and R<reach(st))
 num,path=bfs(start,goal,active={0,1,2})
 print('seen',num,'length',None if path is None else len(path),'initialI',I,'initialR',R,flush=True)
 for m,st in path or []:print(m,st,'I',holders(st),'R',reach(st),flush=True)
