# All shuffle lengths at full cache capacity

Independently audited working theorem, 16 November 2026. Promoted to the
manuscript as `thm:fullcapacityalllengths`; this is not external peer review
or formal verification. The proposed range is c=n-1
and every 1<=L<=n-1, under the adopted protected/MIN mandatory-removal
kernel with iid uniform global initiators and weakly connected arbitrary
finite-integer-age starts. It does not cover sparse capacities c<n-1.

## Proposed conclusion and induction order

For full capacity c=n-1, every fixed allowed shuffle length has a uniform
finite-horizon canonical common atom, hence a unique stationary full-state
law, convergence, and conditional uniform local samples at deterministic
event times. The constants are implicit; no polynomial mixing bound is
asserted.

Induct first on L, with lengths one through three already established for
all populations. At a new length L>=4, assume the full-capacity theorem
for every smaller length and every allowed population. Within this length,
induct on n=L+1,L+2,... . Thus a smaller-population full-capacity kernel of
length min(L,s-1) is known: if s<=L use the outer induction; otherwise use
the inner induction. No lower-length theorem at a sparse capacity is
silently assumed.

## Structural tools remain inside the full-capacity family

The frozen-cut contact and universal-zero-anchor reduction in the
parameterized framework specialize to full capacity. Reserving one
anchor at c=n-1 gives capacity n-2 on n-1 remaining identities. In a
component of s vertices, effective residual capacity is s-1 and length
min(L-1,s-1), strictly below L. Thus all component common atoms needed
for F_L and U_L are supplied by the outer induction alone.

The open-cut part uses F_(L-1) at full capacity on the reduced population.
Start with the already established F_3 (or the earlier F_2). Successively
construct full-capacity F_L before the population induction for C_L.
If a lower cut statement needs a connected auxiliary completion, one frozen
outside row can contain every other reduced identity at full capacity.
This changes no preboundary exchange, since all outside rows are frozen.
There is no F_L/C_L circularity. The general all-length finite-age reset
is independently available.

## Analysis of an arbitrary closed class

Fix n and a closed communicating class C of this full-capacity kernel.
There are never any evictions: each row has only n-1 possible nonself
identities, so its valid merge union cannot overflow capacity n-1.
Consequently the underlying undirected graph only gains edges. Mandatory
selected-partner removal preserves that edge through the fresh reverse
descriptor at the responder. Communication within C implies that one
fixed connected graph G underlies every state of C.

### 1. Freeze one row and erase its incoming references

Choose any peer q and a state of C at which q's row has its maximum size
m_q over C. Freeze q. If m_q<n-1, any novel passive insertion would
exceed that maximum, so no new identity can enter its row. If m_q=n-1,
its row already contains every possible identity. In either case, its
identity set S is fixed and its numerical ages can only decrease by MIN.
Let M be its initial maximum age, taking M=0 for an empty row.

Apply the finite proof from frozen maximum-row erasure, with the same
M throughout: a general colored reset above M never activates q and
bounds every numerical age by a fixed B; minimum-q-copy phases raise
that minimum above B or erase q sooner; a final such reset then erases
all remaining q references. For the full-row case the only change in
that proof is the justification of fixed identities; all reset and
minimum-age arguments are unchanged. The phases invoke only the
smaller-length full-capacity tools identified above.

The resulting state is still in C. Peer q has not initiated and retains
exactly S. No other row contains q. Every underlying edge incident to q
must therefore be represented by q's outgoing row: S=N_G(q). In
particular S is nonempty, since G is connected and n>=2.

### 2. The complement is connected

Let W=V minus {q}. Suppose G restricted to W had more than one weak
component. Each component has a neighbor of q because G is connected.
Let u be an oldest cached head of q. Choose v in S from a different
component than u. Since L>=2 and q has at least two heads, v can be
included in the request extras of a legal q->u exchange. The received
v descriptor is protected at u, so the exchange creates an undirected
u-v edge between distinct components of G restricted to W. That
contradicts the fixed graph G of the closed class.

Therefore G restricted to W is connected. This contradiction is only a
proof of connectivity; the q activation need not be executed in the
actual construction. The q-frozen state from step 1 is retained.

### 3. Normalize the complement and obtain a universal zero

There are no q descriptors in W, so W is closed and connected. Its
actual W-only dynamics are exactly a full-capacity kernel on n-1 peers,
with capacity n-2 and length min(L,n-2). When the inherited capacity or
buffer bound is larger than the possible local row, the effective bounds
coincide. This is equality of the conditional transition rule given a W
initiator, or an exact finite controlled-path simulation; prescribed actual
initiators still have probability 1/n, not 1/(n-1). Outside q stays frozen.

The outer or inner induction supplies a finite path to any prescribed
canonical H(W,n-2). Inspect an oldest head u of q before this path and
choose the canonical root r in W different from u. There is such an r
because n>=L+1>=5 at the new induction steps. The frozen q row and its
oldest choice u do not change during normalization.

At that canonical state every peer of W except r caches r^0, while r is
empty. In particular u caches r^0. Activate q toward u and require r in
u's reply; it occupies one legal reply slot. Peer q receives protected
r^0. Peer u keeps its existing r^0, since there are no evictions and MIN
cannot increase its age. All other r holders are unchanged. Thus r^0
is now universal at all peers other than its owner r.

The full-capacity U_L reduction reaches the same prescribed labelled
canonical H(V,n-1). Every closed class C therefore reaches this atom.

## From closed classes to a uniform common atom

Use the existing uniform finite-age reset to reach a fixed finite set F
with positive probability in a fixed horizon, from every initial state.
The finite reachability graph on F has terminal strongly connected
components. Each generates a genuine closed communicating class: from
any state reachable from such a component, another reset returns to F;
terminality forces that return into the same component. Hence every
reset state has a finite path to a closed class and then, by the preceding
construction, to H(V,n-1).

Choose one such path for each state of the finite set F. Pad them to a
common length using the positive no-op at the canonical atom's empty
root. Take the minimum of the finitely many probabilities of these
padded paths. Composing with the initial reset gives a uniform
finite-horizon atom bound. This does not presume irreducibility or
aperiodicity before the bound is proved.

The standard atom contraction gives uniqueness and full-state convergence.
Relabelling symmetry gives conditional uniform sampling, and relabelled
canonical atoms give positive availability for every allowed sample size.
This closes the population induction at L and then the outer length
induction. The sparse-capacity case remains open because evictions can
change the underlying graph and a frozen full row can acquire unbounded
new numerical ages; neither obstruction is removed here.


## Arbitrary-capacity overflow consequence

The manuscript's `cor:alllengthoverflow` couples a capacity-c chain to
full capacity at the same n,L until the first merge union exceeds c.
Before then all rows, ages and packet laws agree. At that event the
sparse endpoint evicts and ends at size c. A uniform full-capacity atom
hit by T has probability at least gamma and necessarily crosses c when
c<n-1. Therefore the next-eviction waiting tail is at most
(1-gamma)^floor(t/T), with expected wait at most T/gamma, from every
state and after finite stopping times. Evictions recur almost surely.
The same coupling gives hitting of some full row; it does not identify
a prescribed observer or prove sparse-capacity mixing.

Independent final manuscript audits accepted both the theorem and this
corollary, including the stopping-time qualification and the fact that
there is no post-overflow coupling. Exact finite transition checks are
recorded in docs/VERIFICATION.md; they corroborate local identities rather
than establish the induction or its implicit probability constants.
