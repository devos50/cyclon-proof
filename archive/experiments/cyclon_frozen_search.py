import random

def frozen(C):
 for p in range(4):
  vals=C[p];a=max(vals.values());Q=[q for q,v in vals.items() if v==a]
  if len(Q)!=1:return False
  q=Q[0]
  if p not in C[q] or C[q][p]<=max(v for j,v in C[q].items() if j!=p):return False
  if set(C[p])-{q}!=set(C[q])-{p}:return False
 return True

def conn(C):
 for p in range(4):
  S={p};old=0
  while len(S)>old:
   old=len(S);S|={q for i in S for q in C[i]}
  if len(S)!=4:return False
 return True
for trial in range(20000):
 # Prioritize the proposed frozen identity graph, with all ages zero.
 if trial%2: C=[{1:0,2:0},{0:0,2:0},{3:0,0:0},{2:0,0:0}]
 else:
  C=[dict.fromkeys(random.sample([q for q in range(4) if q!=p],2),0) for p in range(4)]
  if not conn(C):continue
 init=tuple(tuple(sorted(v.items())) for v in C);trace=[]
 for t in range(1000):
  p=random.randrange(4)
  for q in C[p]:C[p][q]+=1
  a=max(C[p].values());q=random.choice([q for q,v in C[p].items() if v==a]);r=random.choice(list(C[q]));age=C[q][r]
  # Only replace an actually sent entry when inserting a novel descriptor.
  if r!=p and r not in C[p]:del C[p][q];C[p][r]=age
  if p not in C[q]:del C[q][r];C[q][p]=0
  trace.append((p,q,r))
  if frozen(C):
   print('FOUND',trial,t+1,'initial',init,'trace',trace,'final',C);raise SystemExit
print('NONE')
