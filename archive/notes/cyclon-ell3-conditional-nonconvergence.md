# Conditional local convergence can fail: exact uniform-victim CYCLON, c=ell=3

## Claim and scope

Use exactly the mandatory-removal kernel in Section7: iid uniform initiators, uniform oldest ties, discard incoming self/duplicates without refreshing, insert every usable incoming descriptor using vacancies then uniformly selected sent-entry victims. In particular a resident whose identity occurred in the received buffer but was discarded as a duplicate remains an eligible victim.

For every n>=648002 there is a deterministic, full-cache, ALL-ZERO-AGE, weakly connected initial state such that at least one peer's available singleton sample distribution fails to converge to uniform on the other n-1 identities. The whole initial graph is weakly connected; it is not claimed strongly connected after adding the large outside component.

The construction also works from n>=72002 if two designated partners are given age1 and all other ages0. We use the stronger all-zero initialization below.

## Initial state

Let S={0,1,2,3,4}, T={5,6,7,8,9}, O={10,...,n-1}; n>=14 suffices to define the construction. All ages are zero. The ten core caches are

 i | C_i
 0 | {1,5,2}
 1 | {5,3,4}
 2 | {0,1,3}
 3 | {0,1,4}
 4 | {0,1,2}
 5 | {6,2,7}
 6 | {2,8,9}
 7 | {5,6,8}
 8 | {5,6,10}
 9 | {5,6,7}.

Each outside j=10+k, 0<=k<n-10, has the three cyclic successors
 C_j={10+((k+h) mod(n-10)): h=1,2,3}.
All caches contain three distinct nonself identities. The ten core vertices are strongly connected (in particular the S/T bridge runs S->5 and {5,6}->2). The outside cycle is weakly connected and the edge8->10 joins it to the core. No outside cache contains a core identity. Thus the full initial graph is weakly connected.

## An isolation event of probability independent of n

Let tau be the time of the second initiation by one of the ten core peers. The core initiator subsequence is iid uniform on those ten peers. Condition on its first two entries being5 then0, which has probability1/100.

All other events before tau are outside events. They cannot affect a core cache: outside caches initially contain only outside identities, and this property is preserved by exchanges involving only outside peers. Neither of the two specified core exchanges touches vertex8, so the sole outward boundary descriptor8->10 also cannot transfer an outside descriptor into another core cache during these two exchanges. Hence the following exact exchanges remain available regardless of all intervening outside events.

First, peer5 chooses oldest partner6. Its three entries are tied, so this has probability1/3. Its full outgoing packet is{5^0,2^1,7^1}; the responder's full reply is{2^0,8^0,9^0}.
- Initiator5 discards duplicate2, accepts8,9, fills the vacancy from mandatory removal of6, and chooses2 as its one additional victim among the two eligible sent entries{2,7}: probability1/2. Its new cache is{7,8,9}.
- Responder6 discards duplicate2, accepts5,7, and chooses{2,8} as its two victims among three sent entries{2,8,9}: probability1/3. Its new cache is{9,5,7}.
Thus the designated first exchange has conditional probability1/18.

Second, peer0 chooses oldest partner1. Its own cache was unaffected, so again this is a three-way zero-age tie: probability1/3. Its outgoing packet is{0^0,5^1,2^1}; the reply is{5^0,3^0,4^0}.
- Initiator0 discards duplicate5, accepts3,4, and chooses5 as its one additional victim among{5,2}: probability1/2. Its new cache is{2,3,4}.
- Responder1 discards duplicate5, accepts0,2, and chooses{5,3} as its two victims among{5,3,4}: probability1/3. Its new cache is{4,0,2}.
The second exchange likewise has probability1/18.

Let E denote these choices. Therefore
  P(E)=p0=(1/100)(1/18)^2=1/32400.
The random time tau is almost surely finite. On E, after tau every cache in S contains only S identities, and every cache outside S contains only identities outside S. This partition persists forever: neither side can create an identity from the other side without receiving one first.

## Distributional obstruction, including conditioning on availability

At least one cache in S remains nonempty forever after tau on E. This holds initially at tau. To verify this without assuming that a duplicate initiator descriptor is protected, let a be the active cache size. If a>=2, mandatory partner removal leaves a-1>=1 residents, and processing incoming descriptors never further reduces cardinality: every victim is replaced by an inserted entry. If a=1, the outgoing packet consists only of the fresh initiator descriptor. The responder either accepts it or already knows it; in the duplicate case there is no other usable incoming entry and hence no victim. The responder is therefore nonempty. Thus the last nonempty cache cannot disappear. Empty initiations do nothing.

For i in S let beta_i(t)=P(C_i(t) nonempty), and let nu_i,t be the singleton output law conditional on availability. It is well-defined for every finite t: the event that i has never initiated has positive probability, and passive processing never reduces cache cardinality because every victim is replaced by an inserted entry. Its initially nonempty cache therefore remains nonempty on that event. Write U_i for uniform on V\{i}, and d_i(t)=TV(nu_i,t,U_i).

On E intersect {tau<=t}, each available sample at i in S lies in S\{i}, and at least one such peer is available. Therefore
  sum_(i in S) beta_i(t) nu_i,t(S\{i}) >= P(E,tau<=t).
But U_i(S\{i})=4/(n-1), beta_i<=1, and the TV bound on any event gives
  sum_(i in S) beta_i(t) nu_i,t(S\{i})
  <= 20/(n-1)+sum_(i in S) d_i(t).
Consequently
  liminf_(t->infty) sum_(i in S) d_i(t)
  >= p0-20/(n-1).
For n>=648002, the right side is strictly positive. Hence the five conditional laws cannot all converge to their uniform targets; at least one observer has
  limsup_t d_i(t) >= (p0-20/(n-1))/5 >0.
This disproves the claim of local conditional uniform convergence from every weakly connected initial state for this exact kernel, even with full zero-age initialization, reliable exchanges and iid random initiation.

## Interpretation

This is a failure of an explicit completion of the published protocol's replacement choices. A policy forbidding eviction of residents whose identities appeared in the incoming packet would exclude the designated victims2 (first exchange) and5 (second exchange). This proof does not establish a counterexample for that alternative rule, nor for all implementations named CYCLON. It does establish that connectivity preservation is a necessary substantive hypothesis for a general convergence theorem under the exact rule above.
