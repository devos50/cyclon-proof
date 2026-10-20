from itertools import product
from cyclon3 import moves

def connected(st):
 a=[set() for _ in st]
 for p,c in enumerate(st):
  for q,_ in c:a[p].add(q);a[q].add(p)
 seen={0};todo=[0]
 while todo:
  for q in a[todo.pop()]-seen:seen.add(q);todo.append(q)
 return len(seen)==3

class Trace:
 def __init__(self,s):self.s=s;self.tr=[]
 def go(self,p,q=None):
  opts=list(moves(self.s));opts=[(s,m) for s,m in opts if m[0]==p and (q is None or m[1]==q)]
  assert opts,(self.s,p,q)
  self.s,m=opts[0];self.tr.append(m)
 def oldest(self,p):
  m=max(a for _,a in self.s[p]);return [q for q,a in self.s[p] if a==m]
 def chain(self):
  full=[p for p,c in enumerate(self.s) if len(c)==2]
  if len(full)!=1:return None
  f=full[0]
  s=next((p for p,c in enumerate(self.s) if p!=f and len(c)==1 and c[0][0]==f),None)
  if s is None:return None
  t=3-f-s
  if len(self.s[t])==1 and self.s[t][0][0]==s:return f,s,t
  return None
 def makechain(self):
  n=0
  while self.chain() is None:
   n+=1;assert n<15,(self.s,self.tr)
   full=[p for p,c in enumerate(self.s) if len(c)==2]
   one=[p for p,c in enumerate(self.s) if len(c)==1]
   empty=[p for p,c in enumerate(self.s) if len(c)==0]
   if len(full)>=2:
    choices=[(p,q) for p in full for q in self.oldest(p) if q in full]
    if choices:self.go(*choices[0])
    else:self.go(full[0])
   elif len(full)==1 and len(one)==2:
    f=full[0]
    if all(self.s[p][0][0]==f for p in one):self.go(one[0],f)
    else:
     q=self.oldest(f)[0];other=3-f-q
     assert self.s[q][0][0]==other
     self.go(q,other);self.go(f,q)
   elif len(full)==1 and len(one)==1:
    f=full[0];s=one[0];e=empty[0]
    if self.s[s][0][0]==f:self.go(s,f)
    q=self.oldest(f)[0]
    if q==s:self.go(s,e)
    self.go(f,q)
   elif len(full)==1:
    self.go(full[0])
   elif len(one)==3:
    p=next(p for p,c in enumerate(self.s) if self.s[c[0][0]][0][0]!=p)
    self.go(p)
   else:
    p=next((p for p in one if len(self.s[self.s[p][0][0]])==1),None)
    if p is None:self.go(one[0])
    else:self.go(p)
  return self.chain()
 def reset(self):
  f,s,t=self.makechain()
  for _ in range(4):
   assert self.chain()==(f,s,t)
   ages=dict(self.s[f])
   if ages[t]>=ages[s]:break
   self.go(f,s);f,s,t=s,t,f
  else:assert False
  for p,q in [(f,t),(s,f),(f,s),(t,s),(t,f)]:self.go(p,q)
  assert all(a==0 for c in self.s for _,a in c)
  # Z(full s, single f, empty t)
  f,s,e=s,f,t
  def swap(f,s,e):
   self.go(s,e);return f,e,s
  def rot(f,s,e):
   self.go(f,s);self.go(f,e);return s,e,f
  if f!=0:
   if e==0:f,s,e=swap(f,s,e)
   f,s,e=rot(f,s,e)
  if s!=1:f,s,e=swap(f,s,e)
  assert (f,s,e)==(0,1,2)
  assert self.s==(((1,0),(2,0)),((2,0),),())
  assert len(self.tr)<=19,(len(self.tr),self.tr)
  return len(self.tr)

def allstates(maxage):
 options=[]
 for p in range(3):
  others=[q for q in range(3) if q!=p]
  opts=[()]
  for bits in product(range(-1,maxage+1),repeat=2):
   cc=tuple((q,a) for q,a in zip(others,bits) if a>=0)
   if cc:opts.append(cc)
  options.append(opts)
 return product(*options)

if __name__=='__main__':
 count=0;worst=0;wst=None
 for s in allstates(4):
  if connected(s):
   tr=Trace(s);k=tr.reset();count+=1
   if k>worst:worst=k;wst=s
 print('All passed',count,'worst',worst,'start',wst)
