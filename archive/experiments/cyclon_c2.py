from itertools import product,combinations

def exchange(C,p):
 C=[dict(v) for v in C]
 for j in C[p]:C[p][j]+=1
 top=max(C[p].values()); qq=[j for j in C[p] if C[p][j]==top]
 if len(qq)>1:return
 q=qq[0]
 sendp={j:a for j,a in C[p].items() if j!=q};sendp[p]=0
 sendq=dict(C[q])
 def merge(old,inc,owner,preferred):
  novel={j:a for j,a in inc.items() if j!=owner and j not in old}
  rem=sorted(old,key=lambda j:(j!=preferred,-old[j],j))
  for j,a in novel.items():del old[rem.pop(0)];old[j]=a
 merge(C[p],sendq,p,q)
 merge(C[q],sendp,q,None)
 return tuple(tuple(sorted(v.items())) for v in C)

def conn(C):
 n=len(C);s={0};prev=0
 while len(s)>prev:
  prev=len(s)
  s|={j for i in s for j,a in C[i]}
  s|={i for i in range(n) if any(j in s for j,a in C[i])}
 return len(s)==n
n=4
choices=[tuple(combinations([j for j in range(n) if j!=i],2)) for i in range(n)]
for choiceset in product(*choices):
 for signs in product([0,1],repeat=n):
  C=tuple(tuple(zip(row,[s,1-s])) for row,s in zip(choiceset,signs))
  if not conn(C):continue
  init=C;phase=0;seen={};traj=[]
  while (C,phase) not in seen:
   if len(traj)>400:break
   seen[C,phase]=len(traj);traj.append((C,phase))
   C=exchange(C,phase)
   if C is None:break
   phase=(phase+1)%n
  if C is not None and (C,phase) in seen:
   cyc=traj[seen[C,phase]:]
   print('FOUND initial',init,'cycle',cyc);raise SystemExit
print('no tie-free cycle')
