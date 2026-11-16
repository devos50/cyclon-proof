"""Exact finite check of fullcapacity/fullshuffle hole DAG invariance.
The general proof is combinatorial; finite enumeration is not that proof.
"""
from itertools import product

def acyclic(D):
 n=len(D);ind=[0]*n
 for row in D:
  for j in row:ind[j]+=1
 todo=[i for i in range(n) if ind[i]==0];seen=0
 while todo:
  i=todo.pop();seen+=1
  for j in D[i]:
   ind[j]-=1
   if ind[j]==0:todo.append(j)
 return seen==n

def check(n):
 edges=[(i,j) for i in range(n) for j in range(n) if i!=j]
 graphs=events=0
 for bits in product((0,1),repeat=len(edges)):
  D=[set() for _ in range(n)]
  for bit,(i,j) in zip(bits,edges):
   if bit:D[i].add(j)
  if not acyclic(D):continue
  graphs+=1
  sizes=[n-1-len(row) for row in D]
  for b in range(1,n):assert sum(s<b for s in sizes)<=b
  for p in range(n):
   for q in range(n):
    if p==q or q in D[p]:continue
    E=[row.copy() for row in D];I=D[p]&D[q]
    E[p]=I|{q};E[q]=I
    # Independent direct identity merge: no victims at full capacity.
    caches=[set(range(n))-{i}-row for i,row in enumerate(D)]
    P,Q=caches[p],caches[q]
    active=(P-{q}) | (Q-{p})
    passive=Q | ((P-{q}) | {p})
    assert E[p]==set(range(n))-{p}-active
    assert E[q]==set(range(n))-{q}-passive
    assert acyclic(E),(D,p,q,E)
    events+=1
 return graphs,events
def token_cycle():
 C=[{1:1,2:0,3:0},{0:1,3:0},{1:1,3:0},{}]
 original=[row.copy() for row in C]
 for p,q in ((0,1),(1,2),(2,0)):
  P={j:a+1 for j,a in C[p].items()};Q=C[q].copy()
  assert [j for j,a in P.items() if a==max(P.values())]==[q]
  out={j:a for j,a in P.items() if j!=q};out[p]=0
  del P[q]
  for j,a in Q.items():
   if j!=p:P[j]=min(P.get(j,a),a)
  for j,a in out.items():
   if j!=q:Q[j]=min(Q.get(j,a),a)
  C[p],C[q]=P,Q
 assert C==original
 assert acyclic([set(range(4))-{i}-set(row) for i,row in enumerate(C)])
 return 'period-three full-row-token cycle checked exactly'

if __name__=='__main__':
 for n in range(2,5): print(n,check(n))
 print(token_cycle())
