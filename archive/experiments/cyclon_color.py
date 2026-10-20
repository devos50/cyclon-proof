from itertools import combinations, product
from collections import defaultdict,deque
import sys
n=int(sys.argv[1]);c=int(sys.argv[2]);ell=int(sys.argv[3])
def choices(xs,k):return combinations(xs,k)
def merge(ca,inc,sent,peer):
 new={j:a for j,a in inc.items() if j!=peer and j not in ca}
 k=max(0,len(new)-(c-len(ca)))
 for rem in choices(tuple(sent),k):
  d={j:a for j,a in ca.items() if j not in rem};d.update(new)
  yield tuple(sorted(d.items()))
def succ(s):
 for p,cp in enumerate(s):
  a=dict(cp)
  if not a:continue
  old=[v for v,k in cp if k]
  for q in old or list(a):
   remain={v:k for v,k in cp if v!=q};b=dict(s[q])
   for other in choices(tuple(remain),min(ell-1,len(remain))):
    out={p:0,**{v:remain[v] for v in other}}
    for resp in choices(tuple(b),min(ell,len(b))):
     incoming={v:b[v] for v in resp}
     for np in merge(remain,incoming,other,p):
      for nq in merge(b,out,resp,q):
       ns=list(s);ns[p]=np;ns[q]=nq
       yield tuple(ns)
opts=[]
for i in range(n):
 cache=[]
 for k in range(c+1):
  for ids in combinations([j for j in range(n) if j!=i],k):
   for colors in product((0,1),repeat=k):cache.append(tuple(zip(ids,colors)))
 opts.append(cache)
def conn(s):
 seen={0}
 while True:
  ns=seen|{j for i,cc in enumerate(s) for j,a in cc if i in seen}|{i for i,cc in enumerate(s) for j,a in cc if j in seen}
  if ns==seen:return len(seen)==n
  seen=ns
states=[s for s in product(*opts) if conn(s)]
print('states',len(states),flush=True)
idx={s:i for i,s in enumerate(states)};rev=[[] for _ in states];unconn=[];mono=[]
for i,s in enumerate(states):
 mo=sum(a for cc in s for j,a in cc)
 sm=list(set(succ(s)))
 if min(sum(a for cc in ns for j,a in cc) for ns in sm)>mo:mono.append(s)
 for ns in sm:
  if ns not in idx:unconn.append((s,ns));continue
  rev[idx[ns]].append(i)
goal=[i for i,s in enumerate(states) if not any(a for cc in s for j,a in cc)]
seen=set(goal);queue=deque(goal)
while queue:
 for j in rev[queue.popleft()]:
  if j not in seen:seen.add(j);queue.append(j)
print('unreachable',len(states)-len(seen),'disconnectedges',len(unconn),'no_nonincrease',len(mono),flush=True)
if len(seen)<len(states):
 bad=next(s for i,s in enumerate(states) if i not in seen)
 print('bad',bad)
if unconn:print('disconnection',unconn[0])
if mono:print('nonmono',mono[0])
