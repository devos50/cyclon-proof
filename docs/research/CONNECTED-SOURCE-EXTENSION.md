# Connected-source extension at arbitrary capacity

**Status update, 16 November 2026:** The manuscript's new general source-route
working theorem (`thm:allparametersuniform`) supplies source creation and
complement joining through `lem:generalsourcecreation` and
`lem:generalsourceextension`. Two independent end-to-end internal audits have passed.
The construction below retains its original local/conditional scope. Its
historical source-accessibility obligation is discharged by that new route,
not by assuming the earlier restricted controllers work. This is not formal
verification, external peer review, or a polynomial mixing bound.

Working conditional construction, 16 November 2026. The convergence interface uses the
model's finite nonnegative integer ages. This does not establish general
sparse-capacity convergence. The protocol is unchanged: mandatory removal,
protected incoming identities, MIN ages, and exact fixed-size buffers.

## Local two-exchange lemma

Let n>=2 and 1<=L<=c<=n-1. Fix q, W=V\{q}, and a nonempty
source row C_q=S, |S|=s<=c, with arbitrary nonnegative ages. Assume the
rows on W are the prescribed canonical H(W,d), d=min(c,n-2): in a
chosen order each row contains the min(d, number of higher vertices)
greatest higher vertices, all at age zero. A singleton W has an empty row.
In particular no W row contains q.

If s>=2, choose an oldest u in S and an oldest v in S\{u}. Choose the
canonical order with u greatest and v second greatest. There is a legal
two-exchange path to a universal zero u anchor (every vertex other than
u contains u at age zero), independently of all allowed request extras.

1. Activate q and choose u. The root u replies empty. Mandatory removal
   leaves q with S\{u}, all surviving ages incremented. The fresh-q
   request has min(L,s)<=c entries and fits in u's initially empty row.
2. Activate q and choose v. This is oldest because the surviving ages
   received identical increments and no reply in step 1. The untouched
   v row is exactly {u^0}, so its reply is forced. The request has
   min(L,s-1) entries, excludes u, and is received by v alongside u^0.
   Their union has at most 1+min(L,s-1)<=s<=c entries: no eviction is
   necessary. Thus v retains u^0. At q the mandatory vacancy accommodates
   u^0, giving a row of size s-1. All other W rows except root u were
   untouched and already contained u^0.

If s=1, put u (the only source neighbour) greatest. The exchanges q->u
and then u->q leave q={u^0} and u empty. The first leaves u={q^0}; the
second responder q is empty. Every other W row retains u^0. This also
handles n=2 without invoking a zero-capacity smaller-population theorem.

For a fixed canonical start, the probability of this two-event success
is at least 1/(n^2 s(s-1)) when s>=2, and 1/n^2 when s=1. These bounds
use uniform initiation and oldest tie breaking; all extras work. They
are not bounds on the cost or probability of obtaining the start state.

## What permits complement normalization?

Suppose instead q has no incoming references, its row is nonempty, and
the induced W overlay is weakly connected. Freeze q. No W-only exchange
can introduce q: no W packet contains it. The W dynamics are exactly
the unchanged kernel with effective parameters

    c' = min(c,n-2), L' = min(L,n-2).

Indeed an oversized capacity is inactive when only n-2 nonself identities
exist, and clipping L preserves both exact request and reply sizes.
Global initiation only rescales the probability of a chosen W path.
For n>=3 these parameters satisfy 1<=L'<=c'<=n-2. Thus a prescribed
canonical common-atom theorem for (n-1,c',L') normalizes W while q stays
frozen. Choose u,v from the source's frozen ages before normalization.
For n=2 W is already the singleton canonical state.

This reduction is not automatically covered by existing theorems:
- L<=3 is already covered at every capacity.
- For n<=c+2, W has full effective capacity, so the established
  full-capacity theorem supplies normalization at arbitrary L.
- For n>c+2 and L>=4, c'=c and L'=L, and a smaller-population sparse
  theorem at the same length is generally needed. It is not currently
  proved for arbitrary parameters.

## Joining disconnected source complements through a full-capacity core

The connected-complement hypothesis can itself be removed if the required
smaller-population component normalizations are available. Let q be
incoming-free, S=C_q nonempty, and W=V\{q}, in a weakly connected state.
Each weak component A of W meets S: otherwise it has no edge to q or to
another W component, contradicting overall weak connectivity.

Normalize each A independently while q is frozen. Order all vertices of
S intersect A above every vertex of A\S. A singleton requires no theorem.
The resulting rows of vertices in S intersect A reference only higher
vertices of S intersect A. Each non-S vertex still contains A's greatest
vertex r_A in S at age zero. The independent normalizations are legal:
components have no outgoing references to q or other components.

Now K={q} union S is a closed subsystem, weakly connected because q
caches every vertex in S. Its population is s+1, capacity is effectively
s, and length is effectively min(L,s), where s=|S|<=c. Thus it is FULL
capacity, even when the ambient system is sparse. The established
full-capacity theorem, not an unproved smaller sparse theorem, normalizes
K to its canonical state with q ranked LEAST. Freeze all vertices outside
K during this path. Their incoming edges to K impose no constraint on
K-only exchanges and their caches do not change.

At the endpoint q holds exactly S at zero, and every S row references
only higher S vertices. Therefore q is again globally incoming-free.
The induced graph on S is connected through its greatest vertex (a
singleton S is trivially connected). Every frozen non-S vertex still
points to r_A in S. Hence all of W is now connected. This argument also
covers K=V: then s=n-1 forces c=n-1, so the invoked theorem is still the
already established full-capacity theorem, not a circular sparse induction.

One can now normalize W and apply the two-exchange extension. The
full-capacity core path need not preserve source status or complement
connectivity at intermediate times; only its endpoint is used.

## Conditional alternative induction interface

At length L>=4 assume canonical common atoms for all smaller lengths
and capacities (the hypothesis yielding U_L in
PARAMETERIZED-SHUFFLE-INDUCTION.md). Induct on population n at fixed L,
assuming all allowed capacities at smaller populations. Add this single
unproved source-accessibility obligation:

> Every closed communicating class contains a state with an incoming-free
> vertex q whose row is nonempty.

Normalize the complement components by the smaller-population induction
(or smaller-length theorem if clipping lowers L), join them using the
full-capacity core, and normalize the resulting connected W. The local
lemma gives a universal zero anchor. U_L gives a prescribed canonical
atom. The existing independent finite-age reset/finite-reset-state bridge
promotes closed-class accessibility to uniform finite-horizon minorization:
terminal SCCs of the finite reset-state reachability graph generate closed
classes; choose one atom-reaching path per reset state, take the maximum
finite length, and pad at the atom using its empty root. No uniform bound
on source-access paths is assumed.

This is a conditional route, not a proof of source accessibility or a new
unconditional convergence regime. Absence of incoming references alone
does not imply a connected complement; the core construction supplies
connectivity using the stated normalization hypotheses.

## Why the witness remains an obligation

Holder-only first contact F_L does not by itself erase all incoming q
references: holder-only initiation allows a nonholder responder, which
receives the reserved q descriptor and becomes another holder. One terminal
contact with q removes one copy but need not offset earlier growth.

A single arbitrary source exchange does not justify the core construction.
Disconnected W components cannot simply be joined and then normalized.
A source exchange q->u can transmit representatives of other components
to u, but also inserts fresh q^0 there. W is no longer closed under its
smaller-population kernel. Moreover the transmitted extras have ages at
least one, so an immediate u->q to restore source status is generally
illegal. A proposed zero anchor relayed as an extra likewise increments
its age; presence propagation alone is not a universal-zero construction.
These are gaps in those routes, not protocol counterexamples.

## Validation and scope

The symbolic two-exchange argument was independently audited twice. An
independent scratch enumerator checked 26,403 outcomes (n=2..6, all
capacities and lengths, varied source subsets and ages). The repository
checker `verification/mandatory-removal/verify_connected_source_extension.py`
checks representative source-label configurations at n=2..8, every c,L,s,
strict/tied ages, and every allowed request subset. Label choices are
quotiented by relabeling. It also checks 1,407 core-closure/endpoint
configurations for n=2..7 across all complement partitions meeting S and
all capacities/source sizes, with exact buffer clipping at every length.
These endpoint checks do not construct the core-normalization paths; those
are supplied by the established full-capacity theorem. The core argument
was independently audited by three reviewers. Finite checks corroborate
the lemma; the proof
above covers arbitrary sizes and ages. Neither proves the accessibility
obligation or polynomial mixing time.
