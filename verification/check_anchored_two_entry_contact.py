#!/usr/bin/env python3
"""Exact diagnostics of the special c=L=2 empty-owner/universal-zero lemma.
Not a general mixing certificate. The all-n proof is in the paired research note.
"""
from itertools import product
from fractions import Fraction


def merge(owner, resident, incoming, sent, capacity):
    incoming={j:a for j,a in incoming.items() if j!=owner}
    new=set(incoming)-set(resident)
    d=max(0,len(new)-(capacity-len(resident)))
    eligible=set(sent)&set(resident)-set(incoming)
    # Internal anchor-reserved c=2 exchanges force every required victim.
    assert d==0 or len(eligible)==d
    victims=set() if d==0 else eligible
    out={j:a for j,a in resident.items() if j not in victims}
    for j,a in incoming.items():out[j]=min(out.get(j,a),a)
    assert len(out)<=capacity and owner not in out
    return out


def original_internal(C,p,r):
    P={j:a+1 for j,a in C[p].items()};Q=C[r].copy()
    assert P[r]==max(P.values())
    extras=set(P)-{r}
    outgoing={p:0,**{j:P[j] for j in extras}}
    reply=Q.copy();del P[r]
    out=[row.copy() for row in C]
    out[p]=merge(p,P,reply,extras,2)
    out[r]=merge(r,Q,outgoing,set(Q),2)
    return out


def check(n):
    options=[]
    for p in range(1,n):
        options.append([None]+[(r,a) for r in range(1,n) if r!=p for a in (0,1,2)])
    states=events=0
    for rows in product(*options):
        residual=[None]+list(rows)
        C=[{}]+[{0:0,**({} if row is None else {row[0]:row[1]})} for row in rows]
        ready=lambda row:row is None or row[1]==0
        R=sum(ready(row) for row in rows)
        hazard=Fraction(sum(2 if row is None else 1 if row[1]==0 else 0 for row in rows),2*n)
        assert Fraction(R,2*n)<=hazard<=Fraction(R,n)
        for p in range(1,n):
            row=residual[p]
            if row is None:continue # this initiation contacts anchor, not internal
            r,a=row
            actual=original_internal(C,p,r)
            want=residual.copy()
            reply=residual[r]
            want[p]=None if reply is None or reply[0]==p else reply
            want[r]=(p,0)
            assert actual[0]=={}
            for v in range(1,n):
                expected={0:0,**({} if want[v] is None else {want[v][0]:want[v][1]})}
                assert actual[v]==expected
            RR=sum(ready(row) for row in want[1:])
            assert R<=RR<=R+2
            if not ready(row):assert RR>=R+1
            events+=1
        states+=1
    return states,events


def threshold(n):
    choices=[]
    for k in range(1,n):
        bound=n*sum((Fraction(1,n-1-r) for r in range(k)),Fraction())+Fraction(2*n,k)
        assert bound<=Fraction(n*k,n-k)+Fraction(2*n,k)
        choices.append((bound,k))
    return min(choices)


def comparison_mean(n):
    m=n-1
    f=Fraction(2*n,m)
    for r in range(m-1,-1,-1):
        f=(n+(m-r)*f)/Fraction(2*m-r,2)
    beta=Fraction(2)
    for j in range(2,m+1):beta*=Fraction(2*(j-1),2*j-1)
    assert f==n*beta+Fraction(n,m)
    return f


def check_early_cycle(n):
    # Explore every surviving branch, including zero-age oldest ties.
    m=n-1
    states={tuple((1+p % m,1) for p in range(1,n))}
    for step in range(n-3):
        following=set()
        for rows in states:
            assert all(row is not None for row in rows)
            R=sum(row[1]==0 for row in rows)
            # Owner no-op; exactly R/(2n) killing mass is omitted.
            following.add(rows)
            for p in range(1,n):
                r,a=rows[p-1]
                reply=rows[r-1]
                assert reply[0]!=p, (n,step,rows,p)
                out=list(rows);out[p-1]=reply;out[r-1]=(p,0)
                RR=sum(row[1]==0 for row in out)
                assert RR==R+(a>0)
                following.add(tuple(out))
        states=following
    return len(states)


if __name__=='__main__':
    for n in (3,4,5):print('PASS original/stopped/readiness:',n,check(n))
    for n in range(4,9):print('PASS early-cycle exact comparison:',n,check_early_cycle(n))
    for n in range(3,129):
        exact=comparison_mean(n)
        assert exact<=threshold(n)[0]
    print('PASS exact beta integral / birth-kill recurrence n=3..128')
    for n in (3,4,8,16,64,128):
        value,k=threshold(n)
        print('threshold n=',n,'k=',k,'B_n=',value,'approx=',float(value),'sharper mean=',float(comparison_mean(n)))
