from random import Random

def run(k,seed,limit=100000):
 g=Random(seed);f=[g.choice([q for q in range(k) if q!=p]) for p in range(k)]
 w=[g.randrange(1,1000001) for _ in range(k)]
 a,b=g.sample(range(k),2);P={a:g.randrange(1,1000001),b:g.randrange(1,1000001)}
 for t in range(limit):
  q=max(P,key=lambda z:(P[z],g.random()));e=next(z for z in P if z!=q)
  d=f[q]
  if d==e:return t+1
  P={e:P[e]+1,d:w[q]};f[q]=e;w[q]=P[e]
 return None
if __name__=='__main__':
 for k in range(3,21):
  worst=(0,0)
  for seed in range(10000):
   t=run(k,seed)
   if t is None:print('TRAP',k,seed);quit()
   if t>worst[0]:worst=t,seed
  print(k,worst)
