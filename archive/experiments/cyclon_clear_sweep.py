from itertools import combinations,product
import sys
n=int(sys.argv[1]);c=int(sys.argv[2]);replymax=bool(int(sys.argv[3]));tiemax=bool(int(sys.argv[4]))
opts=[[ids for k in range(min(c,n-i-1)+1) for ids in combinations(range(i+1,n),k)] for i in range(n)]
def connected(s):
 seen={0}
 while True:
  ns=seen|{v for u,cc in enumerate(s) for v in cc if u in seen}|{u for u,cc in enumerate(s) for v in cc if v in seen}
  if ns==seen:return len(seen)==n
  seen=ns
def sweep(s):
 cc=[{j:0 for j in row} for row in s]
 for p in range(n):
  for t in range(n+c):
   if not cc[p]:break
   cc[p]={j:a+1 for j,a in cc[p].items()};a=max(cc[p].values());qs=[j for j,aa in cc[p].items() if aa==a];q=(max if tiemax else min)(qs)
   if p in cc[q]:r=p
   elif cc[q]:r=(max if replymax else min)(cc[q])
   else:r=None
   ra=cc[q].get(r)
   del cc[p][q]
   if r is not None and r!=p and r not in cc[p]:cc[p][r]=ra
   if p not in cc[q]:
    if len(cc[q])>=c:del cc[q][r]
    cc[q][p]=0
  assert not cc[p]
 assert all(a==0 for row in cc for a in row.values())
 return tuple(tuple(sorted(row)) for row in cc)
states=[s for s in product(*opts) if connected(s)]
print('Fstates',len(states),flush=True)
known={};attr=[]
for s in states:
 if s in known:continue
 path=[];where={};t=s
 while t not in known and t not in where:
  where[t]=len(path);path.append(t);t=sweep(t)
 if t in known:ai=known[t]
 else:ai=len(attr);attr.append(path[where[t]:])
 for t in path:known[t]=ai
print('attractors',len(attr),'cycles',list(map(len,attr)))
for aa in attr[:10]:print(aa)
