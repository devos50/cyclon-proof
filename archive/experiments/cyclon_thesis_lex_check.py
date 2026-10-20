from random import Random


def run(n,c,ell,seed):
 rng=Random(seed);H=(n*c+1)*(n*c*c+1)*(n*c*ell**c+1);a=H
 X=[]
 for p in range(n):
  ids=[q for q in range(n) if q!=p];rng.shuffle(ids)
  X.append({q:(rng.randint(0,a) if (old:=bool(rng.randrange(2)))==False else 2*H+rng.randint(1,1000000),old) for q in ids[:rng.randrange(c+1)]})
 def pick(z,k):
  z=list(z);rng.shuffle(z);assert len(z)>=k;return z[:k]
 def phi():
  fs=[sum(not v[1] for v in P.values()) for P in X]
  F=sum(fs);V=sum(f*f for f in fs);W=sum(sum(v[1] for v in P.values())*ell**(c-f) for P,f in zip(X,fs))
  return (n*c-F,V,W),fs
 def merge(v,w):
  if w[0]<v[0]:return w
  if w[0]==v[0]:assert w[1]==v[1]
  return v
 t=0;counts=[0,0,0]
 while any(v[1] for P in X for v in P.values()):
  before,fs=phi();f=max(fs[p] for p,P in enumerate(X) if any(v[1] for v in P.values()))
  p=pick([p for p,P in enumerate(X) if fs[p]==f and any(v[1] for v in P.values())],1)[0]
  P=X[p];M=max(v[0] for v in P.values());q=pick([q for q in P if P[q][0]==M],1)[0];Q=X[q]
  assert P[q][1]
  k=min(ell-1,len(P)-1);m=min(ell,len(Q))
  missing=[z for z,v in P.items() if not v[1] and (z not in Q or Q[z][1])]
  S=pick(missing,1) if missing else []
  S+=pick([z for z in P if z!=q and z not in S],k-len(S))
  U={p:(0,False),**{z:(P[z][0]+1,P[z][1]) for z in S}}
  J={z:v for z,v in U.items() if z not in Q}
  rq=max(0,len(Q)+len(J)-c)
  E=set(Q)&set(U)|{z for z,v in Q.items() if not v[1] and (z in P or z==p)}
  D=pick([z for z in Q if z not in E],rq)
  B={z for z in S if not P[z][1] and z in Q}|({p} if p in Q else set())
  T=D+list(B);T+=pick([z for z in Q if z not in T],m-len(T))
  rem={z:(v[0]+1,v[1]) for z,v in P.items() if z!=q}
  reply={z:Q[z] for z in T if z!=p}
  I={z:v for z,v in reply.items() if z not in rem};rp=max(0,len(rem)+len(I)-c)
  elig=[z for z in S if z not in reply];O=pick([z for z in elig if P[z][1]],min(rp,sum(P[z][1] for z in elig)))
  VP=O+pick([z for z in elig if not P[z][1]],rp-len(O))
  newP={z:v for z,v in rem.items() if z not in VP}
  for z,v in reply.items():newP[z]=merge(newP[z],v) if z in newP else v
  newQ={z:v for z,v in Q.items() if z not in D}
  for z,v in U.items():newQ[z]=merge(newQ[z],v) if z in newQ else v
  X[p]=newP;X[q]=newQ;t+=1
  after,fs2=phi();assert after<before,(n,c,ell,seed,before,after,P,Q,p,q,S,D,T,VP,newP,newQ)
  j=next(i for i,(u,v) in enumerate(zip(before,after)) if u!=v);counts[j]+=1
  assert t<=H
  for P in X:
   for age,old in P.values():assert age>2*H if old else age<=H+t
 return t,counts
if __name__=='__main__':
 N=0;w=(0,None);cs=[0,0,0]
 for n in range(3,21):
  for c in range(2,n):
   for ell in range(2,c+1):
    for seed in range(10):
     t,z=run(n,c,ell,seed);N+=1;cs=[x+y for x,y in zip(cs,z)]
     if t>w[0]:w=t,(n,c,ell,seed)
 print(N,w,cs)
