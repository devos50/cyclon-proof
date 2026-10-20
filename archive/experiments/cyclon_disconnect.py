from collections import deque
# p,q,a,x,y,v,w,z,u,t=0..9
C=[{1,5,2},{5,3,4},{0,1,3},{0,1,4},{0,1,2},{6,2,7},{2,8,9},{5,6,8},{5,6,9},{5,6,7}]
def reach(s):
 seen={s};q=deque([s])
 while q:
  for v in C[q.popleft()]:
   if v not in seen:seen.add(v);q.append(v)
 return seen
print('initial strongly connected',all(len(reach(i))==10 for i in range(10)),'sizes',list(map(len,C)))
# v initiates w; drop w, accept u,t and evict a; w accepts v,z and evicts a,u
C[5]={7,8,9};C[6]={9,5,7}
print('after1 strongly connected',all(len(reach(i))==10 for i in range(10)))
# p initiates q; p drops q, accepts x,y and evicts v; q accepts p,a evicts v,x
C[0]={2,3,4};C[1]={4,0,2}
print('after2 reachable from p',reach(0),'from v',reach(5),'sizes',list(map(len,C)))
