# Protected MIN: shared-anchor cooperative callback

Use the mandatory-oldest-removal, received-identity-protected, MIN-duplicate
kernel, with fixed 3 <= ell <= c. Fix an owner a. Let I be all peers with a^0.
Let P contain ell-2 other peers. Suppose owner a caches every member of P and
every q in I caches a^0 and every member of P at age0. No other restrictions
on IDs or ages apply. In particular, residual caches can point outside I.

Then a finite positive-probability path adds a zero-age a copy, preserves every
old zero-age a copy, and does not decrease the number of a identities. A safe
length bound is c(n+c+1)+1.

Since peers cannot cache themselves, a is outside P and P is disjoint from I.
Thus the owner always has a cached outside-I identity until success. I empty
is immediate.

For an owner-oldest head Q in I, freeze the owner and all outside peers; keep
only Q active. Reserve the ell-1 zero anchors {a} union P in both buffers.
Removing them gives exactly shuffle length1 with configured capacity
c-ell+1. Stop at empty residual cache or before an outside-I residual partner
would be selected. Every selected residual oldest is a legal full oldest:
anchors have age0 at boundaries, all ages increment equally, and ties can
choose a residual entry. Before the stop, each first I responder learns Q^0
persistently, and repeats can return that residual self-Q together with the
anchors, strictly shrinking Q's residual cache. Therefore the block ends in
at most |I|+c events.

At the endpoint C_Q is either the ell-1 anchors alone, or contains the anchors
and an oldest outside residual r. Now activate owner a toward its unchanged
oldest Q. Choose every P identity among its extras and fill the one remaining
extra position arbitrarily if required. Q replies with all anchors, and also
r in the outside-residual case. The reply size is exactly min(ell,|C_Q|).
The owner discards self a, duplicates P, and receives at most the single
outside-I identity r. Its mandatory vacancy suffices without further eviction.
It loses Q, gains no I identity, and keeps P refreshed at0.

At passive Q, all anchors are received and protected. MIN preserves their
ages0 regardless of the optional last extra. Every other old zero holder is
passive. Thus the hypotheses persist with one fewer cached I head. At most c
such head removals occur; an owner-oldest outside-I partner must then be
selected, because P is nonempty and retained. Fresh a^0 adds a new zero copy.

This is a conditional callback theorem. It does not assert that the shared
anchor configuration can be reached from an arbitrary starting state.

## Full shuffle with a common positive age vector

When ell=c, the preceding statement has a positive-layer extension. Let
|P|=c-2 and suppose all q in I have a^0 and each s in P at one common age m_s.
Assume the owner has each s in P at age at least m_s. Set M=max_s m_s. Then a
zero gain preserving all old zeros and all anchor identities is reachable in
at most 2(n+c+1)+1 events.

Reserve all ell-1 anchors. Residual capacity is one. The Q-only block now stops
also before a residual age below M: executed residual oldest choices have age
at least M and are full-cache oldest. Reserved vectors remain unchanged by
MIN, because every contacted I peer has exactly the common vector. The owner
step receives at most one residual ID, sets its P ages to their m_s, and
preserves Q's vector because outgoing P ages are at least m_s+1.

An inserted I-head has age below M; an inserted outside-I head is already a
successful potential owner partner. There are only two owner head positions
outside P. After the first owner step, at most one original I-head can exceed
M. Normalize and remove it if it does. That second owner step increments the
first inserted LOW integer age by at most one, bringing it to at most M, and
inserts at most one new LOW I-head. Some target s in P has age M, hence is
oldest or tied unless an outside head is older. Select such an outside-I
partner and finish. If M=0, LOW residuals do not occur and heads simply vanish.

The integrality of ages is used in b<M implying b+1<=M. This positive-layer
extension requires the common vector and the initial owner componentwise age
inequality. It makes no claim for unequal second-anchor ages.
