# Protected + MIN CYCLON: shuffle length2 at capacities c>=n-2

Assume n>=4, 2<=c<=n-1, ell=2 and c>=n-2. The c=2 case is already covered by
the independent arbitrary-n capacity2 theorem. The argument below proves
universal-anchor accessibility in every closed class for c>=3, and hence
uniform geometric convergence and uniform conditional sampling by the already
proved finite-age-reset/common-atom criterion.

Use the audited generic positive-anchor zeroification proposition: from any
state containing a positive-age a copy there is a path increasing the number
of zero-age a holders, preserving all prior zero holders, and with endpoint
total a-holder count not decreased. Repeating makes every a copy age0.
Consequently, in any closed class, if k is its maximum number of a^0 holders,
then no reachable state can have more than k total a holders. Every maximum-k
state has exactly k total a holders, all age0.

## 1. No initiator extra can be evicted at these capacities

In any ell=2 exchange, if the active pre-cache has at most c-1 entries, its
post-partner-removal vacancy is at least two, enough for the at-most-two valid
incoming entries. No active replacement is needed.

If the active pre-cache P has c entries, then its knowledge P union {p} has
c+1>=n-1 distinct IDs. There is at most one possible valid incoming ID absent
from this knowledge. The removed partner q cannot occur in q's own reply, and
an incoming self identity p is discarded. Thus at most one new usable reply
ID can arrive, which fits the mandatory partner vacancy. Again no active
replacement is needed. Therefore the active extra always survives unless it
was itself the mandatory selected partner (which is removed before extras
are chosen).

## 2. Maximal anchor count excludes any I-to-J edge

Fix a closed class and a maximum-k state for owner a. Let I be all a^0 holders,
and J=V\(I union {a}); no J vertex contains a at any age. Suppose p in I caches
a target z in J. Activate only p. As long as responders lie in I, choose any
oldest nonanchor partner (possible because a is age0 and target z is present),
send a as the extra, and reply a^0 together with p when known; otherwise use
a^0 and a permissible second descriptor/victim. The active anchor resets0,
and every responder keeps its protected a^0. Target z cannot be an active
extra victim, and in fact Section1 rules out any active extra eviction.

Every first responder learns and retains p; repeats then return {a,p}, adding
no new usable identity and shrinking p's cache. Thus within n+c-1 exchanges
p contacts some vertex of J. The incoming a is new there and protected, while
p retains its own a by Section1. Total a-holder count increases above k,
contradicting maximality. Therefore every I cache uses only IDs in I union {a}.

## 3. Residual single-node clearing

The owner cannot cache a target in J: the source-only cached-target controller
would contact a nonzero peer, insert fresh a^0 there, and preserve every old
zero holder, contradicting maximum k. Thus C_a uses only I IDs. It need not
be empty.

Freeze a. Every I cache contains a^0 and uses only I residual identities.
Reserve a as the outgoing extra and as one reply entry; the other reply entry
is the residual ell=1 reply. MIN resets a to0 at both endpoints. Hence the
residual dynamics on I exactly implement mandatory ell=1 with capacity c-1.
For any chosen Q in I, activate only Q until its residual cache is empty:
when a residual responder knows Q, require it to reply Q; otherwise use any
permissible residual reply. First visits that learn Q occur at most |I|-1
times, and all other visits strictly shrink the active residual cache. Thus
the standard single-node ell=1 clearing bound is finite, independently of
ages and the relation between configured capacity and local population size.
Skip a residual no-op once the residual cache becomes empty, so the actual
cache ends as C_Q={a^0}, without contacting owner a. Every old I zero remains
zero, every nonholder is untouched, and the owner's cache is irrelevant.

## 4. Normalize the next passive boundary vertex before the first contact

Assume k<n-1, so J is nonempty. With no owner-to-J or I-to-J edge, weak connectivity gives a J-to-I edge; a J-to-a edge is impossible because J has
no a descriptor. Freeze G=I union {a}, and use the proved first-contact lemma
to find an outside-only path whose next exchange is P->Q with P in J, Q in I.
Before that terminal exchange, all activated/responding peers were in J;
therefore they still have no a descriptor and all I caches remain unchanged.

Pause the outside path immediately before this exchange. On I, perform only
the residual Q-only ell=1 clearing from Section3. Then Q's actual cache is
exactly {a^0}. These controlled I-only moves never contact J (the residual
I graph is closed), so P's cache and its ages are unchanged. Q remains a legal oldest selected partner at P.

Now perform that same exchange P->Q. The responder initially has one entry,
a^0, and receives at most two distinct valid new IDs. Since c>=3, all fit:
Q retains a^0. Its preexchange reply is only a^0. At the active P this one
new entry fits the mandatory partner vacancy and is retained. Thus P becomes
an additional zero-age a holder while Q stays zero. This contradicts k.

Therefore k=n-1 in every closed class: it contains a universal zero-age
anchor for any prescribed owner a. The universal-anchor reduction reaches
the same labelled canonical H(V,c), so there is one closed class. The finite
uniform age-reset family and the empty-root self-loop give a common-atom
minorization, a unique stationary law, and uniform geometric total-variation
convergence. Label equivariance gives uniform stationary output conditional
on availability, and uniform cache subsets conditional on cache cardinality.

## Scope

Combined with the separate c=ell=2 theorem, this closes ell=2 for c=2 and for
c in {n-2,n-1}. It does not prove the intermediate range 3<=c<=n-3. The only
capacity restriction in the saturation argument is Section1's prevention of
active extra eviction; the residual-clearing incoming argument itself works
for every c>=3 whenever I-to-J edges can first be excluded.
