from itertools import product,combinations
from collections import deque
import sys

def norm(f,ba,head,ha):
 lo=min(ba+ha)
 return tuple(f),tuple(a-lo for a in ba),tuple(head),tuple(a-lo for a in ha)

def outs(s):
 f,b,h,a=s
 for i in (i for i in (0,1) if a[i]==max(a)):
  q=h[i];r=h[1-i];x=f[q]
  if x==r:continue
  nf=list(f);nb=list(b);nh=list(h);na=list(a)
  nf[q]=r;nb[q]=a[1-i]+1;nh[i]=x;na[i]=b[q];na[1-i]+=1
  if nh[0]>nh[1]:nh.reverse();na.reverse()
  yield norm(nf,nb,nh,na)

def run(N,lim=3000000):
 starts=[]
 for f in product(*[[x for x in range(N) if x!=q] for q in range(N)]):
  for h in combinations(range(N),2):starts.append(norm(f,[0]*N,h,[0,0]))
 seen={s:i for i,s in enumerate(starts)};states=starts;adj=[];q=deque(starts)
 while q and len(states)<lim:
  s=q.popleft();es=[]
  for t in outs(s):
   if t not in seen:seen[t]=len(states);states.append(t);q.append(t)
   es.append(seen[t])
  adj.append(es)
  if len(adj)%100000==0:print('progress',N,len(adj),len(states),flush=True)
 print('graph',N,len(states),len(adj),'maxgap',max(max(s[1]+s[3]) for s in states),flush=True)
 # topological eliminate sinks, measure longest noncollapse path
 rem=[len(es) for es in adj];rev=[[] for _ in states]
 for i,es in enumerate(adj):
  for j in es:rev[j].append(i)
 qq=deque(i for i,r in enumerate(rem) if r==0);d=[0]*len(states);k=0
 while qq:
  j=qq.popleft();k+=1
  for i in rev[j]:
   d[i]=max(d[i],d[j]+1);rem[i]-=1
   if rem[i]==0:qq.append(i)
 print('eliminated',k,'remainingcycle',len(states)-k,'maxpath',max(d),flush=True)
 if len(states)>k:
  root=next(i for i,r in enumerate(rem) if r);chain=[];idx={};j=root
  while j not in idx:
   idx[j]=len(chain);chain.append(j);j=next(w for w in adj[j] if rem[w])
  for i in chain[idx[j]:]:print(states[i])
if __name__=='__main__':run(int(sys.argv[1]))
