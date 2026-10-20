from random import Random
r=Random(42)

def trial(n,capsteps=10000,ages=True):
 # cache p=0 full2, all others know0, plus exactlyone differentother
 C=[{} for _ in range(n)]
 for q in range(1,n):
  f=r.choice([s for s in range(1,n) if s!=q]);C[q]={0:0,f:r.randrange(100) if ages else 0}
 C[0]={x:r.randrange(100) if ages else 0 for x in r.sample(range(1,n),2)}
 for t in range(capsteps):
  if len(C[0])<=1:return t,C
  P=C[0];M=max(P.values());q=r.choice([s for s in P if P[s]==M]);ext=next(s for s in P if s!=q)
  for s in P:P[s]+=1
  out={0:0,ext:P[ext]};reply=C[q].copy();del P[q]
  ip={s:a for s,a in reply.items() if s!=0 and s not in P}
  iq={s:a for s,a in out.items() if s not in C[q]}
  for s,a in reply.items():
   if s in P:P[s]=min(P[s],a)
  for s,a in out.items():
   if s in C[q]:C[q][s]=min(C[q][s],a)
  if len(P)+len(ip)>2:
   assert ext not in reply;del P[ext]
  if len(C[q])+len(iq)>2:
   vs=[s for s in reply if s not in out];assert len(vs)==1;del C[q][vs[0]]
  P.update(ip);C[q].update(iq)
 return None,C
if __name__=='__main__':
 for n in range(4,15):
  ts=[]
  for k in range(10000):
   t,C=trial(n)
   if t is None:print('NONSHRINK',n,C,flush=True);break
   ts.append(t)
  print(n,'max',max(ts),'mean',sum(ts)/len(ts),flush=True)
