from collections import deque

def moves(st):
 for p,cp in enumerate(st):
  if not cp: continue
  d=dict(cp); M=max(d.values())
  for q in (q for q,a in cp if a==M):
   s=[dict(c) for c in st]
   inc={v:a+1 for v,a in cp if v!=q}
   out={p:0,**inc}
   reply=dict(st[q])
   s[p]=inc
   for v,a in reply.items():
    if v!=p and v not in s[p]: s[p][v]=a
   for v,a in out.items():
    if v!=q and v not in s[q]: s[q][v]=a
   yield tuple(tuple(sorted(c.items())) for c in s), (p,q)

def bfs(st,lim=1000000):
 seen={st:None}; queue=deque([st]); found=None
 while queue and len(seen)<lim:
  x=queue.popleft()
  if all(a==0 for c in x for v,a in c):found=x;break
  for y,m in moves(x):
   if y not in seen: seen[y]=(x,m);queue.append(y)
 if found:
  path=[]
  while seen[found]:
   prev,m=seen[found];path.append((m,found));found=prev
  path.reverse();return len(seen),path
 return len(seen),None
if __name__=='__main__':
 st=(((1,17),(2,39)),((0,23),),((1,8),))
 n,p=bfs(st)
 print(n,p)
