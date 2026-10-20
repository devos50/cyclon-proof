from random import Random

def run(n,c,s,seed,high=False):
 rng=Random(seed);Sset=set(range(s));G=set(range(s,n));r=s
 J=(s*c+1)*(2*s+c);B=s*(s+c);Tmax=B*(J+1)+J
 X=[]
 for p in range(n):
  ids=[q for q in range(n) if q!=p];rng.shuffle(ids)
  P={q:(rng.randrange(1000*J+1),True) for q in ids[:rng.randrange(c+1)]}
  if p in Sset and rng.randrange(2)==0:
   if r not in P and len(P)==c:P.pop(next(iter(P)))
   P[r]=(J+1+rng.randrange(J+1) if high else rng.randrange(5),True)
  X.append(P)
 if not any(r in X[p] for p in Sset):
  p=rng.randrange(s)
  if len(X[p])==c:X[p].pop(next(iter(X[p])))
  X[p][r]=(J+1 if high else 0,True)
 t=0;migs=0;epochs=0;route_steps=0
 def pick(z,k):
  z=list(z);rng.shuffle(z);assert len(z)>=k;return z[:k]
 def holdercount():return sum(r in P for P in X)
 def minr():return min(X[p][r][0] for p in Sset if r in X[p])
 def young():return sum(not v[1] for p in Sset for v in X[p].values())
 def merge(v,w):return (min(v[0],w[0]), v[1] and w[1])
 def select(p):return pick([q for q in X[p] if X[p][q][0]==max(v[0] for v in X[p].values())],1)[0]
 def step(p,q,routing=False):
  nonlocal t,migs
  P=X[p];Q=X[q];assert r in P and q!=r
  out={p:(0,False),r:(P[r][0]+1,P[r][1])}
  rq=max(0,len(Q)+len(set(out)-set(Q))-c)
  known=[z for z in (p,r) if z in Q]
  if len(known)==2:T=[p,r];DQ=[];assert rq==0
  elif len(known)==1:
   z=known[0];cand=[u for u in Q if u!=z]
   if rq:
    assert rq==1
    if routing:cand=[u for u in cand if Q[u][1] or (u not in P and u!=p)]
    DQ=pick(cand,1);T=[z]+DQ
   else:DQ=[];T=[z]+pick(cand,min(2,len(Q))-1)
  else:
   cand=list(Q)
   if routing:cand=[u for u in cand if Q[u][1] or (u not in P and u!=p)]
   DQ=pick(cand,rq);T=DQ+pick([u for u in Q if u not in DQ],min(2,len(Q))-len(DQ))
  reply={u:Q[u] for u in T if u!=p}
  rem={u:(v[0]+1,v[1]) for u,v in P.items() if u!=q}
  newids=set(reply)-set(rem);rp=max(0,len(rem)+len(newids)-c)
  eligible=[r] if r not in reply else []
  DP=pick(eligible,rp);forced=r in DP
  f0=young();hc=holdercount()
  NP={u:v for u,v in rem.items() if u not in DP}
  for u,v in reply.items():NP[u]=merge(NP[u],v) if u in NP else v
  NQ={u:v for u,v in Q.items() if u not in DQ}
  for u,v in out.items():NQ[u]=merge(NQ[u],v) if u in NQ else v
  X[p]=NP;X[q]=NQ;t+=1
  assert holdercount()>=hc
  assert set(DQ)<=set(T)-set(out)
  assert set(DP)<={r}-set(reply)
  assert len(NP)<=c and len(NQ)<=c
  if routing:
   assert P[q][1]
   assert young()>=f0
   if forced:assert p not in Q and r not in Q and young()>f0;migs+=1
  return forced
 while minr()<=J:
  m=minr();before=minr();epoch_steps=0
  while any(r in X[p] and X[p][r][0]==m for p in Sset):
   p=pick([p for p in Sset if r in X[p] and X[p][r][0]==m],1)[0]
   count=0
   while True:
    q=select(p)
    if q in G:return t+1,False,migs,epochs,route_steps
    h0=sum(r in X[u] and X[u][r][0]==m for u in Sset)
    step(p,q)
    count+=1;epoch_steps+=1
    assert count<=s+c
    assert minr()>=m
    h1=sum(r in X[u] and X[u][r][0]==m for u in Sset)
    assert h1<=h0
    if h1<h0:break
   assert epoch_steps<=B
  assert minr()>before;epochs+=1;assert epochs<=J+1
 for p in Sset:X[p]={u:(v[0],True) for u,v in X[p].items()}
 p=pick([p for p in Sset if r in X[p]],1)[0];segment=0
 while True:
  q=select(p)
  if q in G:
   assert route_steps+1<=J and t+1<=Tmax
   return t+1,True,migs,epochs,route_steps+1
  forced=step(p,q,routing=True);route_steps+=1;segment+=1
  assert route_steps<=J and segment<=2*s+c
  assert minr()>J and migs<=s*c
  if forced:p=q;segment=0

if __name__=='__main__':
 cases=steps=fast=migs=ep=0;worst=(0,None)
 for n in range(3,16):
  for c in range(2,n):
   for s in range(1,n):
    for seed in range(5):
     for high in [False,True]:
      t,f,m,e,j=run(n,c,s,seed,high);cases+=1;steps+=t;fast+=f;migs+=m;ep+=e
      if t>worst[0]:worst=t,(n,c,s,seed,high)
 print(cases,steps,fast,migs,ep,worst)
