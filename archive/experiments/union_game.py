from itertools import product

def transition(s,p,q):
 u=(s[p]|s[q]) & ~(1<<p|1<<q)
 t=list(s);t[p]=u;t[q]=u|1<<p
 return tuple(t)
def connected(s):
 seen=1
 while True:
  z=seen
  for p,c in enumerate(s):
   if seen>>p&1: z|=c
   elif c&seen:z|=1<<p
  if z==seen:return seen==(1<<len(s))-1
  seen=z

def solve(n,target):
 opts=[[s for s in range(1<<n) if not s>>p&1] for p in range(n)]
 states=[s for s in product(*opts) if connected(s)]
 wins={s:0 for s in states if target(s)}
 todo=set(states)-wins.keys();turn=0
 while True:
  new=[]
  for s in todo:
   for p,c in enumerate(s):
    if c and all(transition(s,p,q) in wins for q in range(n) if c>>q&1):new.append(s);break
  if not new:break
  turn+=1
  for s in new:todo.remove(s);wins[s]=turn
  print('n',n,'turn',turn,'new',len(new),'remaining',len(todo),flush=True)
 print('FINAL',n,len(states),len(wins),len(todo),'example',next(iter(todo),None))
 return wins,todo
if __name__=='__main__':
 for n in (3,4):
  print('someempty');solve(n,lambda s:0 in s)
  print('designated0empty');solve(n,lambda s:s[0]==0)
