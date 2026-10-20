# Dense capacities, ell=3: cooperative callback without common target ages

Candidate theorem, prepared for independent audit.

Use protected received IDs, MIN duplicates, mandatory oldest removal, ell=3,
and c>=max(3,n-2). Let I be all current zero-age a holders. Suppose owner a
caches a peer p outside I, p!=a. Then a finite positive-probability controlled
path increases Z_a, preserves every original zero at its macro endpoints,
and does not decrease N_a. Temporarily one prepared zero holder may lose
zero status, but the immediately following owner event restores it.

## Dense and two-target preliminaries

At c>=n-2 there is never any active-extra eviction. If the active cache has
d entries before removal, free slots after removal are c-d+1, whereas valid
new reply identities number at most n-d-1. The former bounds the latter.

If owner a caches two distinct peers p,r outside I, keep only a active and
always send p,r as its two extras. Stop at the first outside-I response.
Every preceding responder contains a^0. First visits include a in the reply;
that responder receives/protects a,p,r and thereafter retains all three
while passive. Repeats return exactly a,p,r: self-a filters and both targets
are known, so owner size shrinks. First visits grow size by at most1. There
are at most n-3 first visits; targets cannot be evicted. Thus a finite path
reaches outside I and gives a zero gain. Every old zero is preserved.

## Preparing a single inspected owner head

Inspect an actual oldest Q in the owner's cache. If Q is outside I, activate
owner and finish. Otherwise freeze owner a and prepare this Q only:

(A) If p is absent from C_Q, or |C_Q|>=4, stop preparation. Its eventual owner
reply can contain a and exclude p. (If p is present, size>=4 supplies the
spare reply choice.)

(B) Otherwise C_Q is {a^0,p^m}, or {a^0,p^m,R^b}.

If the latter has R outside I, then R differs from a,p,Q. Immediately perform
a->Q with reply {a,p,R}. The owner keeps p and gains R if not already known.
It now has two distinct outside-I targets, so the two-target lemma finishes.

Otherwise, when R lies in I and b>=m, select R (including on a tie) and perform
Q->R. Outgoing extras are a,p. Require the reply to include a and include p
when known; if the responder knows BOTH p and Q, prescribe exactly {a,p,Q}.
All old zero anchors stay0, and dense no-extra-eviction keeps p at Q. Stop if
(A) is reached; otherwise repeat from (B). All contacted I peers receive
fresh Q, a and p, protected. Since only Q initiates, these copies persist.
A repeat returns {a,p,Q}, giving no usable new residual at Q, so its cache
becomes {a,p}. There are at most |I|-1 first responders before a repeat or
another stopping event. Thus this internal part is finite.

If there is no residual R, or m>b, p is a legal actual oldest partner at Q.
Execute Q->p. The received reply cannot contain self-p, so p disappears from
Q. Dense no-extra-eviction retains Q's a descriptor; its age can now be
positive. Then IMMEDIATELY activate a->Q. Its inspected partner is still
actual oldest because a was frozen. Require its reply to contain a; it
automatically excludes p. At a, retain target p via the designated-target
victim lemma. At Q, received fresh a^0 restores its original zero status.
This completes one owner macro. No further Q preparation occurs after Q->p.

If (A) instead stopped preparation, execute a->Q with a reply containing a
and excluding p, retain p at the owner, and complete the owner macro.

Every macro that has not already invoked the finishing two-target branch
therefore preserves I at its endpoint and makes exactly one owner activation
whose reply excludes p. Hence the owner p-age increases by exactly1 per macro.
All other old zeros are passive or refreshed by the internal I exchanges.
N_a cannot fall: all active retained anchors are kept, and the final a->Q
restores its zero.

## Macro-time age potential

Let t count completed nonfinishing owner macros, and let A be the initial
owner p-age. Then the owner's designated target has age A+t. For each
identity s other than a,p, let M_s(t) be its maximum stored age at macro
boundaries, or0 when absent. Define K_s(t)=M_s(t)-t.

Claim1: M_s(t+1)<=M_s(t)+1.

Every internal Q->R preparation starts from a cache with at most three
entries a,p,R and selects its sole nonanchor residual R. Thus it increments
NO transmitted or retained nonanchor descriptor: R was removed, Q is a
fresh self at0, and a,p are the two anchors. All incoming nonanchor ages are
passive pre-existing ages. These internal preparation events cannot increase
any M_s for s!=a,p.

There is at most one final Q->p preparation. It can increment at most its
one residual R, by1. The owner was frozen throughout preparation. Its final
activation increments its own copies by1, each from an age at most M_s(t),
while Q is passive in that activation. Thus no single copy is incremented
twice; copied preparation ages are at most M_s(t)+1. This proves Claim1.

Claim2: If Q is the selected owner partner of this macro, then
M_Q(t+1)<=M_Q(t).

There is no Q descriptor in Q's own cache, so none can be incremented during
preparation. All fresh Q descriptors sent then have age0. In the owner event,
its Q descriptor is mandatorily removed, cannot be an extra, and Q cannot
reply with its own self identity. Every other Q copy is passive and unchanged
or MIN-refreshed. This proves Claim2.

Consequently every K_s is nonincreasing and K_Q drops by at least1 whenever
owner selects Q. Owner-oldest selection gives M_Q(t)>=A+t, or K_Q(t)>=A.
Thus each identity Q other than a,p can be selected at most
(M_Q(0)-A+1)_+ times. Finitely many nonfinishing macros can occur. Each has
finite preparation length. Therefore the construction must eventually
contact outside I (directly or via the two-target finishing branch), giving
strict zero gain with all original zeros restored.

## Scope

This would prove the missing owner-callback obligation in the dense ell3
regime. It still assumes an outside-I peer is cached by the owner. A separate
source/exploration or saturation argument is needed if the owner has no such
cached peer; positive-anchor first contact supplies one unless it already
zeroifies a positive copy. Do not infer arbitrary-state universal-anchor
accessibility from the callback statement without that final composition.
