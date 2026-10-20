exec(open('/tmp/cyclon_color.py').read().split('opts=[]')[0])
opts=[]
for i in range(n):
 opts.append([tuple((j,0) for j in ids) for k in range(c+1) for ids in combinations([j for j in range(n) if j!=i],k)])
def conn(s):
 seen={0}
 while True:
  ns=seen|{j for i,cc in enumerate(s) for j,a in cc if i in seen}|{i for i,cc in enumerate(s) for j,a in cc if j in seen}
  if ns==seen:return len(seen)==n
  seen=ns
states=[s for s in product(*opts) if conn(s)];idx={s:i for i,s in enumerate(states)}
adj=[sorted({idx[t] for t in succ(s)}) for s in states]
rev=[[] for _ in states]
for i,nn in enumerate(adj):
 for j in nn:rev[j].append(i)
visited=set();order=[]
for i in range(len(states)):
 if i in visited:continue
 stack=[(i,0)];visited.add(i)
 while stack:
  u,k=stack[-1]
  if k>=len(adj[u]):order.append(u);stack.pop();continue
  v=adj[u][k];stack[-1]=(u,k+1)
  if v not in visited:visited.add(v);stack.append((v,0))
comps=[];co={}
for i in order[::-1]:
 if i in co:continue
 ci=len(comps);co[i]=ci;comp=[];stack=[i]
 while stack:
  u=stack.pop();comp.append(u)
  for v in rev[u]:
   if v not in co:co[v]=ci;stack.append(v)
 comps.append(comp)
closed=[cc for k,cc in enumerate(comps) if all(co[v]==k for u in cc for v in adj[u])]
print('n c ell',n,c,ell,'states',len(states),'scc_count',len(comps),'closed sizes',list(map(len,closed)))
for cc in closed:
 byedges=defaultdict(int)
 for i in cc:byedges[sum(map(len,states[i]))]+=1
 print('edgecounts',dict(sorted(byedges.items())))
 print('max sizes',sorted({max(map(len,states[i])) for i in cc}))
 print('example min',min((sum(map(len,states[i])),states[i]) for i in cc))
