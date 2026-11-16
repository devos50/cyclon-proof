# Arbitrary-length service from one shared zero secondary

Conditional working lemma, 16 November 2026. This is a parameterized
lower-length reduction, not a proof of general owner boundary service.

## Hypotheses and conclusion

Use the adopted protected/MIN kernel with 3<=L<=c<=n-1. Assume the
canonical common-atom theorem for every effective smaller-length kernel
invoked below. Let a be an owner, H a subset of its zero holders, and
p outside H union {a}. Suppose:

- Every q in H caches both a^0 and p^0.
- Every other identity cached by a member of H belongs to H.
- The owner's cache contains p and otherwise only identities in H.
  Its initial p-age is arbitrary and finite.

There is a finite legal path to an owner contact with p, preserving all
initial a holders and zero copies. Before that last contact, every
exchange is internal to H union {a}, p remains cached by the owner, and
all outside rows are frozen. The terminal reply may be any legal reply.
No age-independent local duration or generic accessibility is claimed.

## Exact lower-length embedding

Delete the reserved identities a,p from each row in H. The residual
identity graph is closed on H. Within one of its weak components of size
m>=2, reserve a^0,p^0 in every request and reply. The residual protocol
has effective capacity d_m=min(c-2,m-1) and shuffle length
l_m=min(L-2,m-1). Thus 1<=l_m<=d_m, and l_m<L.

At an active peer with d>0 residual entries, select its residual oldest
partner. This is an actual oldest choice: both reserved ages are zero
before increment, and every residual age is nonnegative. The count of
request extras is

 2 + min(L-3,d-1) = min(L-1,d+1),

where the first two are a,p. A responder with d_q residual entries
returns both anchors and min(L-2,d_q) residual entries, giving

 2 + min(L-2,d_q) = min(L,d_q+2).

Both anchors are received/protected and remain zero by MIN. Subtracting
the two protected slots gives exactly the lower-kernel vacancy and
eligible-victim rules. No shorter actual shuffle is used. Residual
empty-cache activations are omitted from the finite witness rather than
executed as actual contacts with a or p; they are no-ops in the reduced
chain. Every remaining finite prescribed activation/subset/tie/victim
choice has positive probability in the actual iid protocol.

## Clearing the owner's inspected head

If p is an oldest owner entry, choose it and finish. Otherwise inspect an
oldest Q in H and freeze the owner. If Q's residual weak component is a
singleton, Q already has no residual entry. Otherwise the assumed
lower-length common-atom theorem supplies a finite legal normalization
of this component to its prescribed canonical root Q. The embedding
above leaves Q's actual row exactly {a^0,p^0}. All other components and
the owner have stayed frozen.

The owner's previously inspected contact with Q is still legal. Include
p in its request extras and choose any other required extras. They all
belong to H. The reply is necessarily {a^0,p^0}, since Q has only two
entries and L>=3. At the owner, self-a is filtered, p is a protected
duplicate, and mandatory deletion removes Q. There is no novel identity
or active eviction. Hence the number of owner heads in H decreases by
exactly one, and its p-age becomes zero.

At Q the request has at most L identities and includes both a and p;
those two old anchors plus all residual incoming identities fit capacity
c>=L. Both zero anchors survive. Residual identities still belong to H,
although their weak components may merge. Thus all hypotheses needed
for the next clearing step persist. Recompute components and repeat.
There are at most |C_a|-1 such owner-head deletions before p is the only
head, or p is selected earlier. This does not bound the normalization
subpaths independently of the initial ages.

The last contact installs fresh a^0 at p. If p was already an a holder,
this refreshes it without losing another holder; otherwise it adds a
holder. No other row changes. Any legal terminal reply is compatible
with this conclusion.

## Scope and obstruction still open

Only one secondary identity is required, even when p is the sole peer
outside H union {a}. This differs from demanding L-2 distinct secondary
anchors. However neither common zero-age p copies nor residual closure
has been established for arbitrary owner-service starts. With positive
p ages, a residual oldest head may be younger than p, invalidating the
reserved-anchor simulation. The all-younger dichotomy describes a
conditional response to that blockage but does not remove it globally.

Independent review checked the exact request/reply sizes, singleton
component case, omission of reduced no-ops, preservation under the
owner's head deletion, and arbitrary terminal reply. No finite test is
being substituted for the lower-length theorem or the symbolic proof.

There is a direct obstruction to preparing this zero-secondary hypothesis
under the strong boundary-service locality condition. If every initial
p descriptor available inside H union {a} has age at least m>0, and p
never initiates, no p^0 descriptor can be created there: all new p copies
come from existing p copies by nonnegative increments and MIN. The lower
bound m is invariant until the terminal boundary contact. Consequently
this particular zero-secondary preparation is impossible for such
starts, not merely an unproved intermediate step. A general service
proof must handle positive secondary ages or use a different interface.

## Finite embedding checks

`verification/mandatory-removal/verify_shared_zero_secondary_embedding.py`
compares 52,920 full-kernel transitions with an independent reduced-kernel
implementation over 3,528 components for L=3..9, c=L..L+3 and m=2..c+4.
It covers effective length/capacity clipping, 7,507 empty responders,
78,370 duplicate MIN refreshes, and 4,946 active / 17,065 passive victim
choices. Another 1,456 cases check normalized owner-head deletion; a
singleton regression checks omission of the reduced no-op. These finite
checks corroborate the embedding identities, not arbitrary-size
accessibility or the assumed lower-length theorem.
