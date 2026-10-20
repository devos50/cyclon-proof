exec(open('/private/tmp/cyclon_c1.py').read().split('for n in range')[0])
from collections import Counter
for n in range(3,7):
 best=None
 for f0 in product(*[tuple(j for j in range(n) if j!=i) for i in range(n)]):
  if not conn(f0):continue
  seen={};traj=[]; f=f0;phase=0
  while (f,phase) not in seen:
   seen[f,phase]=len(traj);traj.append((f,phase)); f=update(f,phase);phase=(phase+1)%n
  traj=traj[seen[f,phase]:]
  noops=sum(update(f,p)==f for f,p in traj)
  count=Counter(f[0] for f,p in traj if p==0)
  if len(count)<n-1 or len(set(count.values()))>1:
   if not noops:
    best=(f0,traj,count);break
 print('n',n,'nonreciprocal biased orbit',best)
