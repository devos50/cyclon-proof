# Constructive quantitative c=ell=2 proof

LATEST UPDATE: the quadratic construction independently audited by the root
and constructive agent supersedes the cubic full-star normalization below.
The dedicated verifier now implements root-only clearing during all growth
phases. A positive-age block costs at most n+4; an all-zero gain phase costs
at most 5n+12; the final canonicalization costs at most 8n^2+2. Thus

    T(n)=(n-1)(5n+12)+8n^2+2
        =13n^2+7n-10 <=16n^2.

The default verifier passes 1,008 whole paths on n=3,...,30, with 351,100
exact exchanges. Worst observed length is 1,154 at n=30 versus the tighter
polynomial bound 11,900. Counts:727positive blocks;7,880owner gains split
6,930direct nonholder services and950outward repairs;658outward infections;
incoming2,800singleton,1,780nontrivial-root,520outside-extra,423outside-oldest,
10component decreases. Each latter is one exchange. Every prescribed-event
probability is checked to be at least1/(4n). Consequently the explicit
minorization and mixing estimates improve to exp(O(n^2 log n)).

In owner-root clearing, stop when an outside residual x is encountered.
Execute Q->x, a->Q, x->a, then owner-only nonholder service. Only Q's old
zero can be temporarily lost; a->Q restores it, x->a deletes the single
positive-age a copy and installs nonholder x at the owner. Endpoint all
copies are zero and Z gains one. The owner remains frozen before a->Q,
so Q remains a legal actual-oldest head. In incoming-boundary normalization,
a nontrivial component need only supply an ACTUAL incoming v->Q after Q is
cleared; v need not be an arbitrary other component vertex and its residual
age need not be zero. The infection gadget permits that arbitrary age.

The rest of this note records the earlier cubic construction and audit.

This note audits the main.tex c=ell=2 proof and replaces its maximum-Z/minimum-components argument with an explicit controlled construction. No main.tex edits were made by this agent.

All paths use the fixed adopted CYCLON algorithm. All counts below are global activation events. Fix the desired ultimate anchor a (choose the largest label for H(V,2)). Let I be its zero-age holders, Z=|I|, and J=V\(I union {a}). Put

    D(m)=2m(m-1), including D(0)=D(1)=0,
    E(n)=2[D(n-1)+1]=4(n-1)(n-2)+2.

The capacity-one theorem gives a path of at most D(m) reduced events from an arbitrary aged weak component of m vertices to any specified zero-age rooted star. Omitting its empty-cache no-ops only decreases the number of actual lifted events.

## 1. Faster positive-age normalization at c=2

If p stores a^A, A>0, there is a block of at most n+4 events which increases Z, preserves every initially zero copy throughout, and does not decrease the endpoint total identity-a holder count N.

If p's oldest is a, perform p->a; p loses a, and a receives protected fresh p0. Otherwise C_p={a^A,u^B} with u an oldest partner. Perform p->u. The received pair forces C_u={p0,a^b}. If u initially held a0, then b=0 and its full reply gives p a0: immediate Z gain, with N not decreased. Otherwise b>0 (integer ages matter) and u->a is forced, giving the owner fresh u0. Neither preliminary initiator was an old zero holder.

In the owner-contact cases, the owner now caches a target z that no longer holds a. Activate only a, always send z as extra until selected, and at every holder responder require a and z when known. The self entry a is filtered at the owner; hence at most one usable reply fits the mandatory vacancy, the target is retained, and owner cache size never increases. Each first responder learns z and every repeat returns a,z and shrinks that cache. Within n+2 events a contacts a nonholder (at latest z). This repairs the possible loss of one a-holder and gives fresh a0 to that responder. All initially zero holders were passive and retain protected a0 whenever touched. Thus the entire block has at most 2+(n+2)=n+4 events.

Iterate while a positive-age a copy remains. Each block increases Z and preserves existing zeros, so at most n-1 blocks occur. Cost at most (n-1)(n+4). The endpoint has all identity-a copies at age zero, N no smaller than initially.

## 2. Empty owner or immediate Z gain

Assume all a copies are zero. If a reaches some J vertex by a directed cache path, Lemma c2sourcegain produces a Z gain in at most (n-1)(n+1)=n^2-1 events, preserving all zeros and never generating positive a copies.

Otherwise its reachable set R is closed and R\{a} consists entirely of zero holders. To empty C_a, inspect an actual oldest q in C_a. Normalize q's residual capacity-one component in R\{a} to a star rooted at q, at cost at most D(n-1). The lifted simulation freezes a and keeps all a0 anchors. Now C_q={a0}; a->q receives only filtered self a, removes q, and inserts at most one extra at q beside protected a0. Thus |C_a| drops by one. Repeat at most twice. Cost E(n). All a copies remain zero and all old holders remain zero at the endpoint.

If now an I->J edge exists, Lemma c2infection gives Z gain in four events. Its endpoint again has all a copies zero, though the owner need not remain empty. This is sufficient, since preparation is repeated after a gain.

## 3. Quantitative component-descent macro

We are now in a normalized state: all a copies zero, C_a empty, every I cache is {a0} plus at most one residual ID in I. Write k=|I| and d for the number of weak residual components. If J is nonempty, weak connectivity gives P in J caching some I vertex. Fix an actual oldest partner and freeze P while normalizing the relevant residual component. The following construction takes at most D(k)+6 events and either strictly increases Z or preserves k and all normalized conditions while decreasing d by one.

* Oldest u lies in J. Then P's other entry is Q in I. Normalize Q's residual component with root Q, so C_Q={a0}. Perform P->u, forcing C_u={P0,Q^b}, then choose u->Q (legal oldest/tie). Q returns a0, u becomes {a0,P1}, and Q loses a0 because its protected incoming pair is {u0,P1}. The zero count remains k and the owner remains empty. P still has no a, since both original endpoint caches lacked it. Apply the four-exchange infection with u as holder and P as nonholder. Net Z gain, all a copies zero at the endpoint. Two preliminary plus four infection events.

* Oldest Q lies in I. Normalize Q's component with root Q. If P is singleton, P->Q gives P a0 and Q keeps its a0 beside fresh P0: Z gain. Otherwise C_P={Q,X}; perform P->Q. Q becomes {P0,X^(A+1)} and loses a; P becomes {a0,X^(A+1)}. The new zero set is I'=(I\{Q}) union {P}. If X lies in J, apply infection from P to X, giving a gain. If Q's former residual component had another vertex v, then after normalization C_v={a0,Q0}; apply infection from v to now-nonholder Q, again giving a gain. The sole remaining case is that Q was an isolated residual component and X is in another I component. Replacing isolated Q by P with edge P->X reduces d by one. No other holder points to Q, so I' remains outclosed, all a copies remain zero, and owner stays empty.

The nongain case requires another component, so cannot occur at d=1. Crucially, its Q component is a SINGLETON, so its normalization costs ZERO events and the entire nongain macro is exactly one event P->Q. Therefore at most k-1 one-event nongains precede one final gain macro of at most D(k)+6 events. The total is at most (k-1)+D(k)+6, not k[D(k)+6]. No re-preparation is needed between nongain macros.

An optional stronger routing choice avoids the component descent loop entirely. Immediately after this isolated-Q swap, Q's cache is exactly {P0,X^(A+1)} with A>=0, so X is its unique oldest partner. The component containing X now also contains P via the new P->X edge. Freeze Q, normalize that component with root X, and perform Q->X. This restores Q's zero and removes X's zero, while untouched P has {a0,X0}. Apply infection P->X to restore X and gain the new holder P. Cost of this entire branch is 1+D(k)+1+4=D(k)+6, and all initial old zeros are restored at its endpoint. Thus a normalized-state gain can in fact be forced within D(k)+6 events, just as in the other branches. The O(n^3) bound below is conservative and does not need this refinement. The current numerical checker uses the original component-descent controller and confirms the zero-normalization-cost observation.

## 4. Explicit whole path length

For a deliberately loose uniform notation use the whole population in D and define

    A(n)=3D(n)+n+7=6n^2-5n+7,
    C_safe(n)=4D(n)+4n+2=8n^2-4n+2.

From any state, if a positive copy exists, the positive-copy block costs at most n+4<=A(n) events and increases Z. If no positive copy exists and Z<n-1, the owner path gain costs at most n^2-1<=A(n), or owner clearing and outward-edge gain costs at most E(n)+4<=A(n), or owner clearing and component descent costs at most E(n)+(n-2)+D(n-1)+6<=A(n). All latter gain endpoints again have all a copies zero. Thus the entire procedure can be organized into at most n-1 Z-increasing phases, each of cost A(n). It is unnecessary to count the preliminary normalization separately.

To reach the fixed labelled H(V,2), empty the universal owner in E(n) events, normalize all residual components in at most D(n-1) events total (sum D(m_i)<=D(n-1)), merge their roots in at most 4(n-2) events, then normalize the connected residual graph to the specified star in at most D(n-1) events. This costs

    C(n)=E(n)+2D(n-1)+4(n-2)
        =8(n-1)(n-2)+4n-6.

This C(n) is below the simpler C_safe(n). Consequently an explicit universal horizon is

    L(n)=(n-1)A(n)+C_safe(n)
        =6n^3-3n^2+8n-5 <= 6n^3, n>=3.

This bound deliberately overcounts many stages. The earlier O(n^4) sum was unnecessarily charging the worst component normalizer at every component-decrease event; the singleton observation improves it to O(n^3).

Pad to exactly L(n) events using H's empty-root no-op. At c=ell=2 the outgoing extras and full-cache replies have no subset choices. An oldest tie costs at most 1/2 and the only possible nontrivial victim choice is a passive responder choosing one of two old residents when it receives one valid new ID; that costs at most 1/2. Initiator probability 1/n therefore makes every prescribed exchange have probability at least 1/(4n). Using the existing documented 1/(nc^5)=1/(32n) bound is also safe if one wishes to avoid introducing this sharper elementary count.

Thus inf_x P^{L(n)}(x,{H}) >= (4n)^(-L(n)); full-state mixing obeys the resulting common-atom bound. This yields the very pessimistic but explicit event estimate

    t_mix(eps) <= L(n) ceil[(4n)^{L(n)} log(1/eps)]
               = exp(O(n^3 log n)) log(1/eps),

with the usual harmless ceiling/additive terms. No finite-age-reset step is needed for this c2 construction: it handles arbitrary finite initial ages directly.

## Audit status

I found no new gap in the existing c2 structural proof. Important endpoint distinctions: the infection lemma does not need to preserve an empty owner; boundary macros need preserve only the zero COUNT, not every old zero identity; the only nongain boundary case really does retain the full normalized state and decreases d. These distinctions are what make the extremal argument constructive.

The dedicated numerical checker is `verify_thesis_c2_quantitative.py`. Its default run passes 1,008 complete connected arbitrary-age starts on n=3,...,30 with 664,562 exact exchanges. The longest actual path has 2,518 events; its n=30 polynomial bound is 159,535. Every local normalizer is checked against D(m), including cycle removal, positive-age deletion, one Hamiltonian-order sort and inverse target insertion. All 10 component-decrease occurrences cost exactly one event. It also checks the two-event availability construction on all 1,728 connected outdegree-at-most-one states through n=5: 1,716 have a three-distinct directed path and 12 are in-stars. The already-full-cache availability branch is symbolically immediate from passive cardinality monotonicity.
