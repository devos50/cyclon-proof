# Independent audit: constructive quantitative stages at ell=2, c>=3

The parent agent's proposed extension is sound, contingent only on the
separate quantitative bound for generaloutwardgain. No closed-class maximum
is needed for any stage.

Maintain a chosen owner identity a and demand only strict Z_a improvement
at macro endpoints. When a macro starts with positive-age a copies, the
existing zeroify proposition supplies one block of at most
R=T_(n-1)+n+c events that strictly increases Z_a. It is unnecessary to
finish all positive copies before charging an increase. Eventually either
Z_a=n-1 or no positive copies remain.

Suppose now all a copies are zero; let I be its holder set, k=|I|, and
J=V\(I union {a}). If k=0, no a descriptors exist, and weak connectivity
forces a nonempty owner cache. One owner activation creates a fresh copy.
Otherwise k>0.

If a has a directed path to J, the existing owner-service shortest-path
argument gains a holder/zero in at most (n-1)(n+c) owner activations. Every
old holder is passive and receives protected fresh a^0 if touched; the
endpoint still has all a copies zero.

Otherwise its reachable set R lies in I union {a} and is outclosed. Empty
the owner by choosing an oldest cached q, normalizing q's residual weak
component inside R\{a} to a singleton-shuffle canonical state with q last,
then a->q. Universal zero anchors inside R make anchor-reduction exact;
the outside is frozen. Q's reply is only a^0, filtered as self at owner a,
so the owner cache loses q and never gains a usable entry. At q, incoming
fresh a^0 plus at most one extra fit capacity c>=2. At most c iterations
empty the owner. All old zeros survive and remain zero.

Let C1(n,c-1) denote a uniform arbitrary-age singleton canonicalization
bound for any residual component; excess configured slots are explicitly
allowed by the singleton proof. Owner emptying costs

    E=c(C1+1).

For a convenient entirely explicit bound one may use

    K=2^(n+1)n^2 >= C1(n,c-1),

because the existing B_m(d) recurrence gives
C1(m,d)<= (2^m-1)m(m+d-1), with m<=n and d=c-1<=n-2.

Now C_a is empty and all a copies are zero.

## Outward case

If some I holder caches a J identity, generaloutwardgain applies exactly
as stated and produces endpoint holder count N_a>=k+1. It may temporarily
lose zeros, so do not claim Z monotonicity during this construction.
Afterward repeat the existing zeroify block until no positive a copies
remain. There are at most n-1 blocks, costing <=(n-1)R, and their endpoint
N_a counts never decrease. Thus the final Z_a=N_a>=k+1. If the outward
path has an affine age bound F(M), this macro has explicit length

    E+F(M+E)+(n-1)R,

where global maximum age increases by at most one per executed event.

## Incoming case

If I has no outgoing J edge, its residual caches contain only I identities.
Weak connectivity, the empty owner, and no a descriptor in J force an
incoming J->I boundary edge. Freeze I union {a} and use firstcontact on J,
pausing immediately before its first boundary exchange P->Q. Before that
boundary exchange, J has no a descriptor: internal J exchanges cannot
generate a because owner a is frozen. Therefore the boundary partner is
Q in I, never owner a.

Keep P frozen and normalize only Q's residual component inside I via
the c-1 singleton simulation, with Q last. All I anchors stay at zero,
the owner stays empty, and P's ages and actual oldest choice Q do not
change. Then C_Q={a^0}. Resume P->Q. The request consists of P^0 and
at most one other identifier; neither is a. They and Q's resident a^0
fit capacity c>=3, so Q retains its zero. Its reply a^0 gives P a new
zero in the mandatory vacancy. No other a descriptor changes, so this
gains Z_a while leaving all a copies zero. The post-emptying cost is

    <= T_(n-1)+K+1.

No residual-component minimum argument is required at c>=3, because the
third slot preserves Q's anchor in this incoming contact.

## Canonicalization and age recurrence

Once the anchor is universal, its complete labelled canonicalization costs
at most

    C = E+(n-1)K+4(n-2)+K
      = (c+n)K+c+4(n-2).

Choose a as the desired final largest label at the outset. Normalize
residual components once, merge empty component roots with the existing
four-event gadget, and normalize the final connected residual state once.
There is no need to normalize between root merges: the retained root u
stays singleton {a^0} and every not-yet-merged root is untouched singleton.

Starting after the general reset with maximum age <=B, an explicit affine
bound F(M)=alpha M+beta yields a recurrence for at most n-1 strict-gain
macros. If A(M) uniformly dominates R, the source service, emptying,
outward-plus-zeroification, and incoming costs, define

    M_0=B,  M_(j+1)=M_j+A(M_j).

Then n-1 stages cost at most M_(n-1)-B and every intermediate maximum age
stays below the corresponding cumulative budget. This closes an explicit
all-c common-atom estimate, despite its large constants. The initial reset
cost H and probability delta must remain in the final theorem, because
the age-dependent stage bound is not uniform over arbitrary initial ages.
