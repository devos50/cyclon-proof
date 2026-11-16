"""Audited recursive controlled horizons for the adopted CYCLON kernel.
No simulated trajectory or empirical mixing assertion. Integers count global events.
"""
from functools import cache
from math import log10, comb

# Optional independently proved stronger base, main.tex thm:c2explicitmix.
USE_C2_BASE = True

@cache
def partition_sum(total,c,l, proper=False):
    # max sum of canonical horizons over component-size partitions; singleton=0.
    upper=total-1 if proper else total
    dp=[0]*(total+1)
    for t in range(1,total+1):
        dp[t]=max(A(m,min(c,m-1),min(l,m-1))+dp[t-m]
                  for m in range(1,min(t,upper)+1))
    return dp[total]

@cache
def lower_M(n,c,l):
    return max(A(m,min(c-1,m-1),min(l-1,m-1)) for m in range(1,n))

@cache
def phase(n,c,l):
    atoms=lower_M(n,c,l)
    contacts=max((F(n-1,c-1,l-1,s) for s in range(1,n-1)),default=0)
    return 1+max(atoms,contacts)

@cache
def F(n,c,l,s):
    assert 1<=s<n and 1<=l<=c<=n-1
    if l==1: return s+c
    if l==2:
        d=s*(s+c); j=(s*c+1)*(2*s+c)
        return d*(j+1)+j
    r=(s*c+1)*c
    return s*phase(n,c,l)*(r+1)+r

@cache
def source(n,c,l):
    tenures=1
    for j in range(1,c): tenures=1+j*tenures
    k=(n-1)*tenures; d=n*c*l**c; r=(n*c+1)*(n*c*c+1)
    h=r*((k+1)*(d+1)+1)
    b=(n*c+1)*h
    return (b+1)*(n-1)*phase(n,c,l)+h

@cache
def universal(n,c,l):
    m=lower_M(n,c,l)
    q=partition_sum(n-1,c-1,l-1)
    return (c+3)*m+q+c+4*(n-2)+1

@cache
def full(n,l):
    if n==1: return 0
    if l==1: return base(n,n-1)
    if USE_C2_BASE and n==3 and l==2: return 16*n*n
    merges=(n-2+l-2)//(l-1)
    return ((merges+1)*source(n,n-1,l)+merges
            +full(n-1,min(l,n-2))+1+universal(n,n-1,l))

@cache
def base(n,c):
    if n==1: return 0
    if c==1: return 2*n*(n-1)
    b=0
    for m in range(2,n+1): b=2*m*(m+c-1)+2*b
    return n*(n+c-1)+b

@cache
def A(n,c,l):
    if n==1: return 0
    assert 1<=l<=c<=n-1,(n,c,l)
    if l==1: return base(n,c)
    if USE_C2_BASE and c==2 and l==2: return 16*n*n
    if c==n-1: return full(n,l)
    p=partition_sum(n-1,c,l,True)
    core=max(full(s+1,min(l,s)) for s in range(1,c+1))
    return source(n,c,l)+p+core+A(n-1,c,l)+2+universal(n,c,l)

def event_denominator(n,c,l):
    z=n*c*comb(c-1,l-1)*comb(c,l)
    if c<n-1:
        z*=comb(l-1,(l-1)//2)*comb(l,l//2)
    return z

def self_test(limit=12):
    from math import factorial, ceil
    import itertools
    # Check every allowed parameter, plus independence from the optional C2 input.
    global USE_C2_BASE
    totals=[]
    for use_base in (False, True):
        USE_C2_BASE=use_base
        for fun in (partition_sum, lower_M, phase, F, source, universal, full, base, A):
            fun.cache_clear()
        count=0
        for n in range(2,limit+1):
            for c in range(1,n):
                for l in range(1,c+1):
                    value=A(n,c,l)
                    assert isinstance(value,int) and value>0
                    assert value>=1
                    z=event_denominator(n,c,l)
                    assert 1<=z<=n*c*16**c
                    if l==c==n-1: assert z==n*c
                    if l==c==2 and n>3: assert z==4*n
                    count+=1
        totals.append(count)
    # Independent tenure closed form and earlier conservative bound.
    t=1
    for c in range(1,21):
        if c>1: t=1+(c-1)*t
        assert t==sum(factorial(c-1)//factorial(j) for j in range(c))
        assert t<=(c+1)**c
    # Distinct representative packets reduce any initial complement partition.
    for n in range(3,limit+1):
        for l in range(2,n):
            worst=0
            for initial in range(1,n):
                k=initial; steps=0
                while k>1:
                    k-=min(l-1,k-1); steps+=1
                worst=max(worst,steps)
            assert worst==(n-2+l-2)//(l-1)
    # Q's unbounded-partition DP agrees with explicit small partition generation.
    def partitions(t,lower=1):
        if t==0: yield ()
        for first in range(lower,t+1):
            for rest in partitions(t-first,first): yield (first,)+rest
    for total in range(2,8):
        for c in range(1,5):
            for l in range(1,c+1):
                for proper in (False,True):
                    want=max(sum(A(m,min(c,m-1),min(l,m-1)) for m in p)
                             for p in partitions(total) if not proper or len(p)>1)
                    assert partition_sum(total,c,l,proper)==want
    assert A(4,3,3)==54446588124
    print(f"PASS: {totals} allowed parameter cases (safe/strong C2 bases), "
          "tenure recurrence c<=20, merge counts, partition DP, regression value.")

if __name__=='__main__':
    self_test()
    for n,c,l in [(3,2,2),(4,3,3),(5,3,3),(8,4,4),(10,4,4)]:
        t=A(n,c,l); logden=log10(event_denominator(n,c,l))
        print((n,c,l),'T=',t,'log10(T)=',log10(t),
              'log10(log10(1/gamma))=',log10(t)+log10(logden))
