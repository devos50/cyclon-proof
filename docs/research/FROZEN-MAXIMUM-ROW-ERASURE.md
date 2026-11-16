# Frozen maximum-row erasure and conditional full availability

Structural research reduction, 16 November 2026. All statements use the
adopted iid-event protected/MIN mandatory-removal kernel, arbitrary finite
nonnegative integer ages, weak connectivity and fixed membership.
This does not prove class invariance or arbitrary-length convergence.

## Induction assumptions

Fix 3<=L<=c<=n-1. Assume canonical common-atom accessibility for every
smaller shuffle length and every allowed population/capacity, and the
frozen-cut first-contact statement F_(L-1). These are exactly the lower
hypotheses in the parameterized induction framework. Effective small
components use their clipped lower parameters, including length one.
The general all-length colored age-reset lemma is already available
independently of these assumptions.

## Finite erasure at a peer's maximum row

Let C be a closed communicating class. Fix a peer q and let m_q be the
maximum size of its row over states in C. Suppose m_q<c. From a state
attaining that maximum, there is a finite legal path, never initiating q,
that erases every stored q descriptor. The identities in q's own row
remain fixed throughout this path; its ages never increase.

No global no-eviction assumption is needed for this lemma. Other peers
may have full caches and evict descriptors. The claim concerns existence
of a finite controlled path, not a typical extinction time.

### 1. A fixed frozen-row bound

Freeze q at a state attaining m_q. Every finite non-q-initiated history
stays in C. If q received a novel identity, its passive row would finish
with size min(c,m_q+number_of_novel_identities)>m_q, contrary to maximality.
Thus every incoming valid identity at q is already resident. Its identity
set stays fixed, and duplicate MIN merges can only decrease its ages.
Let M be its initial maximum age, or zero if its row is empty. This same
M bounds q's row throughout all subsequent constructions.

Let

 R=(nc+1)(nc^2+1)(nc L^c+1),
 B=M+(nc+1)R.

These bounds are deliberately conservative. At any later state, among
the nc+1 disjoint intervals (M+jR,M+(j+1)R], j=0,...,nc, one contains no
stored age. Put A=M+jR for that interval; color descriptors of age at
most A young and those above A+R old. The unpadded colored-reset controller
eliminates the old descriptors within R events, selecting only old-holding
initiators. Peer q is always young, since its ages remain at most M.
It therefore never initiates. Final ages everywhere are at most A+R<=B.

This is a reset while q stays frozen, with B fixed from the original M,
not recomputed upward as the proof proceeds. It is a hitting-within-R
construction; no arbitrary padding or auxiliary stationary law is needed.

### 2. Raising the minimum q age

While q is frozen, no fresh q descriptor is generated. Increments, copies
and MIN merges cannot reduce the global minimum stored q age. If no q
copy remains, erasure is complete. Otherwise denote the finite minimum
by k and let S be all its holders.

There is a finite path that removes at least one k-copy without creating
another. Only S peers initiate. Reserve q in internal requests and replies.
At an internal S-to-S contact, the active copy increments to k+1 and the
passive copy is k; the protected MIN merge leaves both copies at k.
Deleting the reserved descriptor gives the exact residual kernel of
capacity c-1 and length L-1 on identities other than q.

If the residual graph has an outgoing edge from S, use F_(L-1) until the
first residual boundary contact, with the outside frozen. If it has no
outgoing edge, use the assumed lower-length common atom on a residual
weak component, rooted at a chosen peer. Effective parameters are
min(c-1,s-1), min(L-1,s-1) for a component of size s; a singleton has no
residual head. These lower paths are followed only while their selected
residual is an actual oldest entry. If a proposed residual oldest is
strictly younger than k, choose the reserved q instead and finish the
phase. Equality permits the prescribed residual tie. A normalized empty
residual row likewise contacts q directly.

At a residual boundary contact, the initiator's outgoing q descriptor
has age k+1. The responder has no q copy or one older than k, so no reply
can restore age k; no new k-copy is created at either endpoint. The
active k-copy is lost, regardless of whether the identity survives at a
larger age. At a direct owner contact, mandatory partner removal deletes
the sole active q copy, and owner q cannot store or return itself.
Again at least one k-copy disappears and none is created.

An intermediate boundary can be a holder of a larger q age; this causes
no difficulty. The argument tracks the minimum numerical age, not zero
count or total holder count. At most n-1 repetitions eliminate the
current minimum level, either erasing q entirely or raising its minimum
by at least one. Every phase is finite and all its initiators differ
from q.

### 3. Erasing the references

Repeat the preceding finite raising operation until q is absent or its
minimum exceeds the fixed B. This takes finitely many unit increases.
In the latter case apply the q-frozen reset from step 1. It ends with all
ages at most B. Since the minimum q age cannot decrease while q is
frozen, no q copy can remain. This proves finite erasure.

The proof does not extrapolate an infinite prescribed schedule and does
not infer extinction from a contact-rate bound. Its two ingredients are
finite minimum-raising paths and the fixed, q-frozen numerical reset.

## Consequence in a no-eviction class

Suppose the maximum row size anywhere in C is m<c. Every transition in C
then has no evictions: an overflowing merge would end with size c>m.
The underlying undirected graph can only gain edges, because the
mandatory selected edge is retained through the fresh reverse descriptor.
Communication within C therefore makes this graph one fixed graph G.

For any peer q, choose a state attaining its own maximum m_q<=m. Every
neighbor of q not in its frozen cache would require an incoming q copy
forever, since G is fixed. Finite erasure contradicts that requirement.
Consequently

 m_q=degree_G(q)

for every peer. This is a structural constraint, not a proof that G is
complete without a further symmetry hypothesis.

## Full availability under even-class invariance

Assume additionally n>=5 and that every individual closed class is
invariant under A_n. If a class had maximum occupancy m<c, its fixed
connected graph G would be A_n-invariant, hence complete. The preceding
constraint would give m_q=n-1 for every peer, contradicting m<c<=n-1.
Thus every class contains a state with a full cache of size c.

The separately proved symmetry/phase argument now gives positive
availability for every b<=c at every observer in every cyclic phase,
and deterministic-event-time conditional uniform ordered samples for
all such b. This conclusion still assumes individual-class invariance
and the lower-length induction package. Neither hypothesis is proved
for arbitrary lengths here. With currently established lower lengths,
the first new applicable induction step is L=4; this is not a proof of
length-four convergence or class invariance.

## Exact local corroboration

`verify_frozen_target_minimum_erasure_local.py` checks 10,560 actual-kernel
exchanges for n=4..13 and every tested 3<=L<=c<=n-1, with minimum ages
0, 1 and 10^6. It verifies internal minimum preservation, higher-age and
absent-target boundary replies, direct owner deletion, and nondecrease
of the global minimum. Full/underfull rows and eligible evictions are
included. These checks corroborate only the local age bookkeeping;
they do not establish the lower-length paths, the class maximum
hypothesis, or the global finite-erasure proof.
