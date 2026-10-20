exec(open('/private/tmp/cyclon_frozen_search.py').read().split('for trial in range')[0])
import json
random.seed(3)

def apply(C,e):
 p,q,r=e
 if q not in C[p] or r not in C[q]:return False
 for j in C[p]:C[p][j]+=1
 if C[p][q]!=max(C[p].values()):return False
 age=C[q][r]
 if r!=p and r not in C[p]:del C[p][q];C[p][r]=age
 if p not in C[q]:del C[q][r];C[q][p]=0
 return True

def replay(init,trace,show=False):
 C=[dict(row) for row in init]
 for e in trace:
  if not apply(C,e):return
  if show:print(e,C)
 return C

def minimize(init,tr):
 changed=True
 while changed:
  changed=False
  for k in range(len(tr)//2,0,-1):
   for i in range(len(tr)-k+1):
    cand=tr[:i]+tr[i+k:];out=replay(init,cand)
    if out is not None and frozen(out):tr=cand;changed=True;break
   if changed:break
 return tr
best=None
for trial in range(12000):
 C=[dict.fromkeys(random.sample([q for q in range(4) if q!=p],2),0) for p in range(4)]
 if not conn(C):continue
 init=tuple(tuple(sorted(v.items())) for v in C);trace=[]
 for t in range(80):
  p=random.randrange(4);a=max(C[p].values());q=random.choice([q for q,v in C[p].items() if v==a]);r=random.choice(list(C[q]));e=(p,q,r)
  assert apply(C,e);trace.append(e)
  if frozen(C):
   trace=minimize(init,trace)
   if best is None or len(trace)<len(best[1]):
    best=(init,trace);print('best',len(trace),flush=True)
    open('/private/tmp/cyclon_zero_best.json','w').write(json.dumps(best))
   break
 if best is not None and len(best[1])<=6:break
print('BEST',best)
print('final',replay(*best))
