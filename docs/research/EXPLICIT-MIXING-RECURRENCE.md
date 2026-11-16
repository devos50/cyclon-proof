# Candidate explicit all-parameter mixing bound

Status: independent adversarial audit passed for the recurrence, conditional on the cited existing base lemmas; constants were then sharpened in joint review. Not externally reviewed or formally verified. This is an explicit, extremely pessimistic upper bound, not a claim of polynomial or near-optimal mixing. Exact model is the iid uniform-global-initiator, protected/MIN, mandatory-partner-removal, finite nonnegative integer-age model in `paper/generic-proof.tex`. Initial overlay is weakly connected. Time means global events, not parallel rounds.

## Definitions

Let A(n,c,l) bound the length of a controlled path from every allowed state to any prescribed labelled zero-age canonical H(n,c), uniformly over initial numerical ages. One-vertex A=0, with effective c=l=0 only in this convention. Let F(n,c,l,s) bound first cut contact with a frozen complement, starting with a cached cut edge and active side of size s. No global connectivity is needed for F.

All maxima over component sizes include singleton cost zero. For l>=2 set

M = max_{1<=m<n} A(m,min(c-1,m-1),min(l-1,m-1));
E = 1 + max{ M, max_{1<=s<n-1} F(n-1,c-1,l-1,s) }.

The extra one covers an empty residual root's owner contact or terminal contact after normalization. Open-cut first-contact paths already include their boundary event, so this is conservative.

Define Q(N;d,e) as the maximum sum of A(m,min(d,m-1),min(e,m-1)) over integer partitions of N. Qproper restricts to partitions with at least two parts. These are finite dynamic programs, not maxima over numerical states. All component costs in Qproper(N) use m<N.

## Base horizons

A(n,1,1)=2n(n-1).
For c>=2,l=1: B_1=0, B_m=2m(m+c-1)+2B_(m-1), A=n(n+c-1)+B_n.
For c=l=2 use existing stronger A=16n² (main manuscript thm:c2explicitmix), rather than this recurrence's vastly weaker value.

F(n,c,1,s)=s+c: pick an active peer p caching an outside identity and activate p repeatedly. Until crossing, that outside descriptor cannot be evicted at l=1. Each first responder learns p, and never subsequently loses p while only p initiates. Prescribe p in replies of repeat responders. There are at most s-1 first responders and at most c shrinking replies before crossing. This proof does not require all active peers to hold the same outside identity.

For l=2 use established explicit first-contact horizon: D=s(s+c), J=(sc+1)(2s+c), F=D(J+1)+J.
For l>=3 use structural-induction horizon F=sE((sc+1)c+1)+(sc+1)c.

## Uniform source creation (new quantitative use of existing lemma)

t_0=1, t_j=1+j*t_(j-1) for 1<=j<=c-1; K=(n-1)t_(c-1), D=nc*l^c, R=(nc+1)(nc²+1),
H=R((K+1)(D+1)+1), B=(nc+1)H.
Then
S(n,c,l)=(B+1)(n-1)E+H
bounds creation of an incoming-free nonempty source q while q never initiates.

Proof: freeze q. At current minimum stored q-age k, use the existing minimum-holder residual construction. Reserving q leaves precisely capacity c-1,length l-1 internally. A residual oldest younger than k causes an immediate q-contact instead. Closed residual components normalize using lower A; open residual cuts use lower F. An internal contact preserves minimum copies, and a terminal contact removes at least one minimum copy while creating none. Each phase costs at most E, and at most n-1 phases clear a given integer minimum level. In at most B+1 levels either q is absent or all q-copies have age >B. Apply the existing partial-color source reset for H events using a vacant age band. Its conclusion erases q references without requiring a bound on q's passive row. Weak connectivity and passive nonemptiness imply C_q is nonempty.

Sharpened tenure count: on a fixed-young-count plateau, a q-tenure at a row with f young descriptors can create at most c-f-1 child tenures: every non-q activation deletes one old non-q head and receives only young entries. Its children have strictly larger f. Thus the maximum family size at f is at most t_(c-f-1), rather than the original c-ary depth bound. There are at most n-1 initial roots. The rest of partialcolorsource is unchanged.

The argument uses l>=2, not l>=4; l=2 uses F1 and the established length-one canonical theorem. Every original legal event is retained, and no genuinely shorter original shuffle is substituted.

## Universal-anchor normalization

The existing reserved-zero construction has uniform horizon
U(n,c,l)=(c+3)M + Q(n-1;c-1,l-1) + c + 4(n-2)+1.

At most c residual component normalizations plus c owner contacts empty the owner. Normalize initial residual components at cost Q. Merge their roots with at most n-2 four-event gadgets; the same untouched root can be reused, so intermediate renormalization is unnecessary. Normalize the final residual component once. If needed, change to the prescribed final root by one additional residual normalization and one exchange, then normalize the final residual component again. This explains the three additional M terms. Some are redundant for a particular order, but the bound covers all orders.

## Constructive full-capacity recurrence (avoids closed classes)

Write J(n,l)=A(n,n-1,l), using the preceding bases. For l>=2, except the stronger n=3,l=2 base, set

m=ceil((n-2)/(l-1)),
J(n,l)=(m+1)S(n,n-1,l)+m+J(n-1,min(l,n-2))+1+U(n,n-1,l).

At capacity n-1 there are never evictions, so the underlying undirected graph only gains edges. Create incoming-free q. If its complement is disconnected, q has a cached neighbor in every complement component. Take an oldest u at q and include representatives v from up to l-1 other complement components as extras in q→u. This creates all complementary edges uv simultaneously. Recreate a source; no complementary edge can have been lost. After at most ceil((n-2)/(l-1)) such merges, one final source creation leaves connected complement. Normalize that complement with root r different from q's frozen oldest u. The exchange q→u returns r0 and creates universal r0 (no evictions). Apply U. The case n=2 is already length one.

## Arbitrary capacity recurrence

For 2<=l<=c<n-1, except c=l=2's stronger base, put

A(n,c,l)=S(n,c,l)+Qproper(n-1;c,l)
         +max_{1<=s<=c} J(s+1,min(l,s))
         +A(n-1,c,l)+2+U(n,c,l).

This counts existing source extension exactly: normalize disconnected complement components with source-neighbor labels highest; normalize the closed core {q} union C_q by independent full-capacity J; normalize the now-connected complement with the two selected heads highest; use two contacts to universal zero; then U. If the complement is already connected the initial component/core steps are unnecessary, so the displayed bound still applies. Since c<n-1, A(n-1,c,l) is an allowed smaller-population input. Qproper has no current-population term.

Well-foundedness: first establish all lengths <l; then all full-capacity J(n,l) by n induction (source and U use strictly lower l); then sparse A(n,c,l) by n induction. Thus no circular dependency remains.

## Mixing consequence

Let T=A(n,c,l). Put Z=nc*binom(c-1,l-1)*binom(c,l), multiplied at proper capacity c<n-1 by binom(l-1,floor((l-1)/2))*binom(l,floor(l/2)); omit both victim factors at full capacity. Set p=1/Z, gamma=p^T. Each specified event has probability at least p: row subset counts are monotone up to their full-capacity binomials; eligible victim sets have at most l-1/l identities and central binomials bound their choices. At full capacity there are no victims. This sharpens nc16^c and exactly recovers nc² for proper-capacity length1 and4n for proper-capacity c=l=2. Adaptivity is allowed: multiply conditional lower bounds along the state-dependent legal controller. Pad the canonical atom using its empty-root no-op to exactly T events. Then P^T(x,{h})>=gamma uniformly over initial ages and all allowed x.

Consequently full-state TV<= (1-gamma)^floor(t/T). Exact inversion gives T*ceil(log(1/epsilon)/[-log(1-gamma)]); the simpler T*ceil(gamma^(-1)log(1/epsilon)) is valid. For existing c=l=2 retain gamma=(4n)^(-16n²), which is stronger than generic p^T.

For conditional query use stationary availability a_b and the sharp transfer TVconditional<=TVfull/a_b (independent worker proved separately). Relabelled full-cache canonical atoms give a_b>=gamma, so a fully explicit but weak bound follows by replacing epsilon with epsilon*gamma. For b=1 use the much better general a1>=ceil((n-1)/c)/n, and at full capacity a1>=(n-1)/n.

## Boundary of progress

This is a constructive explicit all-parameter rate where the general manuscript left finite-family path minima implicit. It is not a useful estimate of practical mixing. For (n,c,l)=(4,3,3), even using the existing c=l=2 quadratic base the horizon is 54,446,588,124 events, then the Doeblin probability exponentiates that number. The enormous cost exposes the limitation of forcing one exact path; it does not show actual executions are slow. The best existing worst-case full-state lower bound is only Omega(n log n), leaving a very large gap. Finite-age resets, fresh emissions and communication connectivity alone do not contract a query law. A sharper probabilistic coupling/conductance argument remains necessary for a meaningful analogue of PeerSwap's rate.
