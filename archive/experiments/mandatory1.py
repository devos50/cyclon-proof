from itertools import product
from collections import Counter,deque

def conn(s):
 seen={0};todo=[0]
 while todo:
  p=todo.pop()
  ns={q for q,r in enumerate(s) if r==p}
  if s[p]>=0:ns.add(s[p])
  for q in ns-seen:seen.add(q);todo.append(q)
 return len(seen)==len(s)

def move(s,p):
 q=s[p]
 if q<0:return s
 r=s[q]
 t=list(s)
 t[p]=-1 if r in (-1,p) else r
 if r!=p:t[q]=p
 return tuple(t)
for n in range(2,7):
 opts=[[-1]+[q for q in range(n) if q!=p] for p in range(n)]
 states={s for s in product(*opts) if s.count(-1)==1 and conn(s)}
 unseen=set(states);cs=[]
 while unseen:
  first=unseen.pop();todo=[first];c={first}
  while todo:
   s=todo.pop()
   for p in range(n):
    t=move(s,p)
    assert t in states
    assert s in {move(t,q) for q in range(n)}
    if t in unseen:unseen.remove(t);c.add(t);todo.append(t)
  cs.append(c)
 print(n,len(states),sorted(map(len,cs)))
