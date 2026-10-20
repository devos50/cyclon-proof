# Audited obstruction to unconditional-initial-state conditional sample uniformity

This result concerns the literal kernel with c=ell=3, mandatory partner removal,
duplicate discard before insertion, and uniform replacement among sent resident
slots. It is NOT a theorem about every CYCLON implementation. Its initial overlay
is weakly connected (the ten-peer core is strongly connected, but the extension
is one-way), every cache is full, and every initial descriptor age is zero.

Use core peers 0,...,9 with caches

 C0={1,5,2}; C1={5,3,4}; C2={0,1,3}; C3={0,1,4}; C4={0,1,2};
 C5={6,2,7}; C6={2,8,9}; C7={5,6,8}; C8={5,6,10}; C9={5,6,7}.

For n>=14 let O={10,...,n-1}. Give every outsider three distinct outsider
neighbors, for example its next three neighbors on a cyclic ordering of O.
Then O is strongly connected and all its cache identities are in O. The edge
8->10 joins the core to O weakly. The ten-peer core remains strongly connected
when the original C8={5,6,9} is changed to {5,6,10}.

Let E be the following outcome at the first two *core initiations*:

1. Peer5 initiates toward6, sending{5,2,7}, receiving{2,8,9}. At5, after mandatory
   removal, fill one vacancy and replace resident2, giving C5={7,8,9}. At6 replace
   residents2,8 by5,7, giving C6={5,7,9}.
2. Peer0 initiates toward1, sending{0,5,2}, receiving{5,3,4}. At0 fill one vacancy
   and replace resident5, giving C0={2,3,4}. At1 replace residents5,3 by0,2,
   giving C1={0,2,4}.

Outsider initiations before and between these two events cannot affect the core.
Until a core vertex initiates, outsiders only know outsider identities and their
exchanges remain inside O. Core8's outgoing outsider descriptor is never read:
8 has not initiated, and the two prescribed exchanges involve only(5,6),(0,1).
Their messages include identity8, but do not read its cache. Thus every core
state involved in E is exactly the prescribed initial one, regardless of outsider
activity.

The first two core initiators are iid uniform on the ten core peers. Each chosen
partner is one of three zero-age ties. Messages are full and deterministic.
Each active endpoint's chosen victim has probability1/2, while each responder's
specified two-victim subset among three sent slots has probability1/3. Therefore

 P(E)= (1/10)^2 (1/3)^2 [(1/2)(1/3)]^2 = 1/32400 =: p.

The value1/3600 would omit the two age-tie factors; it applies only to a modified
initial-age assignment forcing the partners, not this all-zero initialization.

On E, S={0,1,2,3,4} is separated forever. Its caches contain only S identities;
every cache outside S contains no S identity. Both properties are preserved by
all subsequent exchanges. Let E_t be the event E has completed by observation
time t. Core initiations occur infinitely often almost surely, so P(E_t)->p.

At least one cache in S stays nonempty forever. Initially all are full. Any
nonempty-cache initiation inside S leaves its responder nonempty: passive cache
cardinality never decreases under fill-then-replace, and an initially empty
responder inserts at least the fresh nonself initiator identity. This argument
does not require the initiator descriptor itself to survive duplicate filtering
and replacement. Empty-cache activations do nothing. No outside exchange can affect S. Consequently, pathwise on E_t,

 sum_(i in S) 1{C_i(t) nonempty} >= 1.

Let A_i(t) denote nonemptiness, and conditionally on A_i(t) let Z_i(t) be a
uniformly chosen cached identity. Every available sample on E_t lies in S, hence

 sum_(i in S) P(A_i(t), Z_i(t) in S\{i}) >= P(E_t).

Suppose every peer's conditional marginal converged to uniform on the n-1 other
identities. Then for i in S,

 P(A_i(t), Z_i(t) in S\{i})
 <= P(Z_i(t) in S\{i} | A_i(t)) -> 4/(n-1).

Therefore p <= 20/(n-1), a contradiction whenever n>=648002.

More quantitatively, writing d_i(t) for the conditional singleton TV distance,

 max_(i in S) d_i(t) >= [P(E_t)-20/(n-1)]/5,

so

 limsup_t max_(i in S) d_i(t) >= 1/162000 - 4/(n-1) > 0

for the same population threshold. Since S is finite, at least one fixed peer
has positive limsup distance and cannot converge to uniform.

This is stronger than positive-probability disconnection alone: the fixed small
closed component and arbitrarily large harmless outside network turn it into a
rigorous marginal-law contradiction. It establishes that a theorem covering all
weakly connected full-cache zero-age initializations and all n is false for this
specific uniform-victim completion. Strongly connected initializations of the
entire large network are not covered by this construction.
