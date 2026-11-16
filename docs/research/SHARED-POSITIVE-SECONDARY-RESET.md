# A local finite-age reset with a shared positive secondary

Conditional structural lemma, 16 November 2026. This does not prove owner
boundary service or access to the hypotheses below. Unlike a common-atom
normalization, it uses only the already established all-length colored
finite-age-reset argument, not convergence at a lower length.

## Domain and statement

Fix 4<=L<=c<=n-1. Owner a caches p and otherwise only identities in a
nonempty set H, with p outside H union {a}. Every peer in H caches a^0
and p, and every other identity it caches belongs to H. All p ages at
H union {a} are at most a finite nonnegative integer M. They need not
be zero or equal. All other ages may be arbitrarily large.

Write h=|H|, d=min(c-2,h-1), e=min(L-2,h-1). If h>=3, let

 R=(h d+1)(h d^2+1)(h d e^d+1).

This is the old-lineage elimination horizon supplied by the general
colored-reset lemma at residual parameters (h,d,e), where e>=2.
For h=2 use R=2, since d=e=1 and each old-initiator event removes at least
one old residual descriptor. For h=1 use R=1 as a harmless bound for the
empty residual system. Set

 B=M+(h d+1)R,
 T=(c+1)R+c,
 K=B+c^2+c.

A controlled path of at most T actual events leaves every residual age
at peers of H at most B, every owner age at most K, and every p age at
most M. It preserves all a^0 anchors, all p identities, residual closure,
and every outside row. The owner's p remains cached throughout. Every
exchange is internal to H union {a}; no contact with p is needed.

This is a bounded internal-state hitting construction, not a common atom,
not a below-p clearing theorem, and not a stationary-regime theorem for
the original unrestricted protocol.

## Residual reset while the owner is frozen

Reserve a,p in every H-to-H request and reply. Their endpoint p ages
become min(u+1,v), so the global p-age maximum never increases. The a
ages return to zero by protected MIN. For residual rows, the request,
reply, vacancy and victim counts are exactly the reduced (d,e) kernel,
as in the shared-zero-secondary embedding. A residual initiation is
legal whenever its selected age exceeds the reserved anchor ages.

There are at most h d residual descriptors. Among the h d+1 disjoint
intervals

 (M+jR, M+(j+1)R],  j=0,...,h d,

one is empty of their initial ages. Put A=M+jR for such an interval.
Color initial residual ages at most A young and those above A+R old.
Run the existing reduced colored-reset controller along its **unpadded
old-initiator-only path**. Its old descriptors retain ages above A+R;
its young descriptors have ages at most A+t after t events. The controller
always selects an old residual oldest. That residual is also oldest in
the actual row: its age exceeds M+R, whereas the active p anchor before
increment is at most M and the primary anchor is zero. After increment
the same ordering holds. Thus every nontrivial prescribed reduced step
is an actual legal step. No arbitrary lower-kernel padding is imported.

The old-lineage elimination finishes in at most R steps. Final residual
ages are at most A+R<=B. The argument needs no connectedness of the
residual graph; the colored lexicographic descent works on all its rows.
At h=2 the sole old residual is deleted when it initiates; any old reply
is transferred rather than duplicated, giving the same conclusion in at
most two steps. At h=1 there are no residual entries to reset.

## Bounding the owner's residual ages

The preceding residual reset freezes the owner's possibly large ages.
To bound those as well, choose an empty interval (A,A+c] among c+1
consecutive width-c intervals above B. The owner has at most c-1
non-p entries, so such an interval exists with A<=B+c^2. Color its
initial non-p entries at most A young and those above A+c old.

While an owner-old entry remains:

1. Freeze the owner and reset all H residuals to at most B using the
   preceding construction.
2. Activate the owner. Its oldest entry is owner-old: after at most c
   owner activations, every owner-young age is at most A+c, and p is at
   most M. The selected old head lies in H.
3. Include p in the request extras and a,p in the reply, completing both
   buffers legally. The incoming owner residual ages are at most B<=A.
   Mandatory deletion removes its selected old head; no new owner-old
   entry can arrive. Additional old residents may be evicted, which only
   helps. Both anchors at the responder are received/protected.

Each round removes at least one owner-old entry. There are at most c
rounds, and all young owner ages stay at most A+c<=K. Old owner extras
may have been copied into H, even if their active copies were evicted.
Therefore perform one **final** H residual reset after the owner phase.
This proves the total bound (c+1)R+c and the stated endpoint bounds.

## Probability and limits of the reduction

Every finite controlled exchange uses legal oldest ties, exact buffer
sizes and eligible victims. Under the adopted iid model the prescribed
path has positive probability. The usual per-event lower bound yields
at least (n c 16^c)^(-T) probability of hitting the stated bounded
internal-state set within T events from a state in this domain.

This probability cannot automatically be iterated under the unrestricted
chain: other choices can leave the reserved-anchor domain. A separate
explicit auxiliary restricted controller would be needed before making
recurrence claims inside that domain. Outside rows are frozen along the
witness but may have arbitrary ages, so only the internal state is bounded.

Most importantly, neither reaching the domain nor subsequent service to
p is proved. The bound is above M, not below every local p age. It cannot
replace the unresolved positive-secondary boundary-service argument.

## Exact transition corroboration

The separate checker `verify_shared_positive_secondary_reset.py` passes
2,025 starts and 6,505 actual-kernel exchanges: 5,344 residual exchanges
and 1,161 owner exchanges, with 3,186 residual-reset calls and 2,290
non-first age-gap choices. It includes h=1 and h=2, unequal secondary
ages bounded by M up to 10^6, all three colored-potential decreases,
owner-old extras, and the required final reset. It asserts the numerical
bounds, retained primary zeros/secondary identities, closure, and frozen
outside rows. These finite checks corroborate the symbolic construction;
they do not establish owner service or generic accessibility.
