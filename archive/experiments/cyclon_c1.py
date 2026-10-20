from itertools import product

def update(f,p):
 q=f[p]; r=f[q]
 if r==p:return f
 g=list(f);g[p]=r;g[q]=p;return tuple(g)
def conn(f):
 s={0}; old=0
 while len(s)>old:
  old=len(s)
  s|={f[i] for i in s}
  s|={i for i in range(len(f)) if f[i] in s}
 return len(s)==len(f)
for n in range(3,7):
 states=[f for f in product(*[tuple(j for j in range(n) if j!=i) for i in range(n)]) if conn(f)]
 unseen=set(states); comps=[]
 while unseen:
  s=unseen.pop();comp={s};front=[s]
  while front:
   s=front.pop()
   for p in range(n):
    t=update(s,p)
    if t not in comp:comp.add(t);unseen.discard(t);front.append(t)
  comps.append(comp)
 print(n,len(states),len(comps),sorted(map(len,comps)))
