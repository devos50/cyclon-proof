exec(open('/tmp/cyclon_color.py').read().split('opts=[]')[0])
opts=[]
for i in range(n):
 opts.append([tuple(zip(ids,colors)) for k in range(c+1) for ids in combinations([j for j in range(n) if j!=i],k) for colors in product((0,1),repeat=k)])
def conn(s):
 seen={0}
 while True:
  ns=seen|{j for i,cc in enumerate(s) for j,a in cc if i in seen}|{i for i,cc in enumerate(s) for j,a in cc if j in seen}
  if ns==seen:return len(seen)==n
  seen=ns
states=[s for s in product(*opts) if conn(s)];idx={s:i for i,s in enumerate(states)}
print('states',len(states),flush=True)
rev=[[] for _ in states];actions=[];qgroups=[];owner=[]
for si,s in enumerate(states):
 for p,cp in enumerate(s):
  a=dict(cp)
  if not a:continue
  old=[v for v,k in cp if k]
  partners=old or list(a)
  ai=len(actions);actions.append([si,len(partners)])
  for q in partners:
   gi=len(qgroups);qgroups.append(False);owner.append(ai)
   remain={v:k for v,k in cp if v!=q};b=dict(s[q]);targets=set()
   for other in choices(tuple(remain),min(ell-1,len(remain))):
    out={p:0,**{v:remain[v] for v in other}}
    for resp in choices(tuple(b),min(ell,len(b))):
     incoming={v:b[v] for v in resp}
     for np in merge(remain,incoming,other,p):
      for nq in merge(b,out,resp,q):
       ns=list(s);ns[p]=np;ns[q]=nq;targets.add(idx[tuple(ns)])
   for ti in targets:rev[ti].append(gi)
win={i:0 for i,s in enumerate(states) if not any(a for cc in s for j,a in cc)};queue=deque(win)
while queue:
 ti=queue.popleft()
 for gi in rev[ti]:
  if qgroups[gi]:continue
  qgroups[gi]=True;ai=owner[gi];si,rem=actions[ai];rem-=1;actions[ai][1]=rem
  if rem==0 and si not in win:win[si]=win[ti]+1;queue.append(si)
print('winning',len(win),'losing',len(states)-len(win),'maxrankupper',max(win.values()),flush=True)
if len(win)<len(states):print('losingexample',next(s for i,s in enumerate(states) if i not in win))

byold=defaultdict(int)
for i,r in win.items():
 m=sum(a for cc in states[i] for j,a in cc);byold[m]=max(byold[m],r)
print(dict(sorted(byold.items())))
def steps(s,p,q):
 cp=s[p];a=dict(cp);remain={v:k for v,k in cp if v!=q};b=dict(s[q]);targets=set()
 for other in choices(tuple(remain),min(ell-1,len(remain))):
  out={p:0,**{v:remain[v] for v in other}}
  for resp in choices(tuple(b),min(ell,len(b))):
   incoming={v:b[v] for v in resp}
   for np in merge(remain,incoming,other,p):
    for nq in merge(b,out,resp,q):
     ns=list(s);ns[p]=np;ns[q]=nq;targets.add(tuple(ns))
 return targets
si=max(win,key=win.get);s=states[si]
print('WORST TRACE')
for t in range(30):
 print('rank',win[idx[s]],'M',sum(a for cc in s for j,a in cc),'state',s)
 if not any(a for cc in s for j,a in cc):break
 options=[]
 for p,cp in enumerate(s):
  if not cp:continue
  old=[j for j,a in cp if a];partneropts=[]
  for q in old or [j for j,a in cp]:
   succs=steps(s,p,q)
   ns=min(succs,key=lambda ns:(win.get(idx[ns],10000000),sum(a for cc in ns for j,a in cc),ns))
   partneropts.append((win.get(idx[ns],10000000),q,ns))
  worst=max(partneropts,key=lambda x:x[0]);options.append((worst[0],p,worst[1],worst[2]))
 rr,p,q,s=min(options,key=lambda x:x[:3]);print('action',p,'worst partner',q)
