exec(open('/private/tmp/cyclon_c2.py').read().split('n=4')[0])
import random
for n in [4,5,6,8]:
 for trial in range(10000):
  C=tuple(tuple(sorted(zip(random.sample([j for j in range(n) if j!=i],2),random.sample(range(10),2)))) for i in range(n))
  if not conn(C):continue
  init=C;phase=0;seen={};traj=[]
  while (C,phase) not in seen and len(traj)<500:
   seen[C,phase]=len(traj);traj.append((C,phase));C=exchange(C,phase)
   if C is None:break
   phase=(phase+1)%n
  if C is not None and (C,phase) in seen:
   cyc=traj[seen[C,phase]:]
   print('FOUND',n,'initial',init,'cycle',cyc);raise SystemExit
 print('n',n,'none')
