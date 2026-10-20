import sys
from random import Random
sys.path.insert(0,'/Users/martijndevos/Documents/decentralized-learning-simulator/docs/peer-sampling-convergence/mandatory-removal')
from verify_thesis_anchor import Actual
from verify_thesis_half_dense import holders, owner_double

def run(seed,limit=3000):
 r=Random(seed);n=7;c=3;a=0;p=1;q=2
 I={p}|set(r.sample([3,4,5,6],r.randrange(1,5)))
 x=[{} for _ in range(n)]
 for v in range(1,n):
  pool=sorted(set(range(1,n))-{v})
  chosen=r.sample(pool,c-(v in I))
  x[v]=({a:0} if v in I else {})|{u:r.choice((0,1,2,1000000)) for u in chosen}
 x[p]={0:0,2:1000001,3:r.choice((0,1,1000000))}
 x[q]={u:r.choice((0,1,2,1000000)) for u in sorted(set(range(n))-set(x[p])-{p})}
 z=Actual(x,c);initial=[v.copy() for v in x];H=len(holders(z,a));active=p;pred=None
 history=[];seen={};migrations=resets=0
 for t in range(limit):
  key=(active,pred,tuple(tuple(sorted(row.items())) for row in z.x))
  if key in seen:return 'cycle',t-seen[key],migrations,resets,initial,history[seen[key]:]
  seen[key]=t
  P=z.x[active]
  if P[a]==0:
   cand=[q for q in P if q!=a and P[q]==max(P.values())]
  else:
   cand=[q for q in P if P[q]==max(P.values())]
  q=a if a in cand else r.choice(cand)
  if q==a:
   owner_double(z,a,active,pred,r)
   return 'gain-owner',t+1,migrations,resets,initial,history
  old=holders(z,a);Q=z.x[q]
  if q in old:
   known=(set(Q)&(set(P)|{active}))-{a}
   D=r.choice(sorted(known)) if known else r.choice(sorted(set(Q)-{a}))
   reply=[a,D]
  else:
   known=set(Q)&(set(P)|{active})
   if known:
    first=r.choice(sorted(known));reply=[first]+r.sample(sorted(set(Q)-{first}),1)
   else:
    retained=max(Q,key=lambda v:(Q[v],r.random()))
    reply=sorted(set(Q)-{retained})
  out={active,a};needed=max(0,len(Q)+len(out-set(Q))-c)
  eligible=set(reply)-out
  victims=sorted(eligible,key=lambda v:(Q[v],v))[:needed]
  history.append((active,q,reply,victims))
  z.step(active,q,[a],reply,vq=victims)
  if len(holders(z,a))==H+1:return 'gain-direct',t+1,migrations,resets,initial,history
  if len(z.x[active])<c:
   return 'gain-underfull',t+1,migrations,resets,initial,history
  if q in old:
   resets+=1
  else:
   assert active not in holders(z,a) and q in holders(z,a)
   pred,active=active,q;migrations+=1
 return 'limit',limit,migrations,resets,initial,history

if __name__=='__main__':
 counts={};worst=(0,None);bestmig=(0,None)
 for seed in range(100000):
  ans=run(seed);kind,t,m,rr,initial,history=ans
  counts[kind]=counts.get(kind,0)+1
  if t>worst[0]:worst=(t,(seed,kind,m,rr,initial,history));print('WORST',worst,flush=True)
  if m>bestmig[0]:bestmig=(m,seed)
  if kind in ('cycle','limit'):
   print('FOUND',seed,ans,flush=True);break
 print('DONE',counts,'worst',worst,'bestmig',bestmig)
