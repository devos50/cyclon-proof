# Explicit polynomial controlled path for c = ell = 2

This note does not assume bounded initial ages. All paths use the adopted protection/MIN CYCLON algorithm. Let n >= 3, fix a final owner label a, and write k = Z_a for the number of nonowner peers storing a at age zero. Put

    D = 2 n (n-1),   g = (n-1)(n+1) = n^2 - 1.

The capacity-one theorem supplies a path from every connected reduced component of size m to the rooted zero-age star with any prescribed root, costing at most 2m(m-1) exchanges. Therefore normalizing all components of any residual partition of at most n peers costs at most D. The anchor simulation omits reduced no-ops, so this is also an upper bound for actual exchanges.

## 1. A positive-age a copy yields a bounded zero-count gain

Suppose p stores a^A with A>0. If its oldest partner is a, exchange p -> a. No old zero holder is touched, the owner learns p^0, and p remains a nonzero holder (indeed, it loses its a descriptor). Thus a directed path from owner a reaches nonzero peer p. Lemma c2sourcegain gives a zero-count gain within g further events, preserving all old zeros.

Otherwise C_p = {a^A, u^B}, with u an actual oldest partner. Exchange p -> u with packet {p^0,a^(A+1)}. If u already stores a^0, its reply gives p a^0, while protection/MIN keeps u's zero; this increases k immediately. Otherwise neither p nor u was a zero holder, and u's final cache is exactly {p^0,a^b} for some b>0. The next exchange u -> a is forced, so the owner learns nonzero peer u^0 without touching old zero holders. Lemma c2sourcegain again increases k in at most g more events. This case costs at most g+2 overall.

## 2. Empty the owner if no immediate bounded gain applies

If a directed path from a reaches any peer outside I union {a}, where I is the current zero set, apply c2sourcegain in at most g events. Otherwise all peers reachable from a belong to I union {a}; their cache sets are closed under outgoing edges. Assume also that no positive-age a copies remain, since Step 1 would otherwise apply.

To empty C_a, choose an actual oldest q in it. Freeze a and all vertices outside its reachable component. Normalize q's residual weak component after removing the zero anchor a by the capacity-one construction, with q its root. This costs at most D, gives C_q={a^0}, and preserves all a-zero copies globally. One exchange a -> q then removes q from C_a, since its reply consists only of the owner's own identity. Any other owner entry is sent as the extra and fits at q; it is never evicted at the owner. Repeat at most twice. Thus C_a becomes empty in at most 2(D+1) events, k unchanged, no positive-age a copies introduced.

If k=0 and neither Step 1 nor source gain applies, no peer caches a and C_a is empty, contradicting weak connectivity. Thus the following phase has k>=1.

## 3. Replace the closed-class extremum by strict finite progress

Now C_a is empty, no positive-age a descriptors exist, and I is the zero set. Write J=V\(I union {a}). If J is empty we are done. If any cache edge I -> J exists, Lemma c2infection gives a zero-count gain in four events.

Otherwise every I cache is a^0 plus at most one residual identity from I. Let d be the number of weak components of that residual graph. Weak connectivity, C_a empty, absence of I -> J, and absence of J -> a force an edge from J into I. Choose a peer P in J having such an edge. Inspect its actual oldest partner and freeze P during residual normalization. Normalize all residual components to zero-age rooted stars, picking any needed root Q as below; cost at most D. The owner and all J caches are unchanged; k, d, and the component partition stay unchanged.

Case A: P's oldest partner u belongs to J. Its other entry is some Q in I; choose Q as its component's root. Exchange P -> u. Since neither had a, u's cache is exactly {P^0,Q^b} and P still has no a. Exchange u -> Q, a legal oldest choice. Root Q replies only a^0, leaving C_u={a^0,P^1}, and its incoming pair {u^0,P^1} removes Q's old zero. The zero count is still k, owner still empty, and the new zero holder u points to nonzero holder P. Apply c2infection in four more events. Total phase cost <=D+6 and k strictly increases.

Case B: P's oldest partner is Q in I. Choose Q as its component root and exchange P -> Q. If P was singleton, Q retains its zero (the one incoming P fits) and P gains a zero, so k increases. Otherwise write its other entry as X. Then the new caches are C_P={a^0,X^(A+1)} and C_Q={P^0,X^(A+1)} (with any allowed MIN ages in Q irrelevant), and the zero set is I'=(I\{Q}) union {P}, still size k. If X is in J, apply c2infection to the zero holder P and nonzero X. If X is in I and Q's old residual component contained another vertex v, that star leaf still stores {a^0,Q^0}; apply c2infection to v and now-nonzero Q. These cases cost <=D+5 and increase k.

The remaining case is: Q's old residual component was the singleton {Q}, while X belongs to another old I component. Remove Q from I and add P with its residual edge P -> X. No old I cache points to Q, and all other residual edges are untouched. Thus the new residual graph on I' is still closed and has exactly d-1 weak components. C_a is still empty and there is still no positive-age a descriptor anywhere. This returns directly to the beginning of Step 3, with k unchanged and d decreased.

Therefore at most d<=n phases of Step 3 yield a strict k gain. Each phase costs at most D+6. No class extremum, finite-state BFS, age bound, or recurrence theorem is used.

## 4. Explicit common-atom length

From every state with k<n-1, one strict zero-count gain therefore costs at most

    A = (g+2) + 2(D+1) + n(D+6).

This safely adds the alternative immediate-gain costs instead of taking a maximum. Iterate at most n-1 times to reach universal zero anchor a.

From there, Proposition anchorcanonical can be quantitatively implemented as follows: empty owner in <=2(D+1); normalize all residual components <=D; merge their roots using <=4n events; normalize the connected residual graph to a zero star with prescribed root b in <=D. This gives the prescribed labelled H(V,2), with a last and b penultimate, in

    C = 4D + 4n + 2

events. Hence every state reaches that fixed atom within

    T = (n-1) A + C = O(n^4).

Padding uses the empty owner a's no-op and does not modify the atom.

## 5. Probability and full-state mixing

For c=ell=2, extra choices and replies are deterministic because every other cached entry is sent. Initiator victim choice is deterministic: after mandatory partner removal there is at most one eligible extra. If the request has two entries, the responder's two protected incoming entries determine its final cache and victims uniquely. If the request has one entry and responder has two, there are at most two responder victim choices. Oldest ties have at most two choices. Therefore every prescribed exchange has probability >=1/(4n), and an empty-root no-op has probability 1/n.

Consequently P^T(x,{H}) >= (4n)^(-T), uniformly over all finite initial ages. The usual common-atom contraction gives

    sup_x ||P^t(x,.) - pi||_TV <= (1-(4n)^(-T))^floor(t/T),

and

    t_mix(eps) <= T ceil((4n)^T log(1/eps)).

This is n^{O(n^4)} log(1/eps) global events, or equivalently exp(O(n^4 log n)) log(1/eps), with explicit T above. It is not a practical mixing estimate. It is nevertheless fully explicit and removes the finite-family path-length black box in the c=ell=2 theorem.

## Audit cautions

## Sharpening: the controlled witness is actually O(n^3)

In Step 3 normalize ONLY the indicated component of Q, exactly as the existing `incoming()` verifier does. None of the other components needs to be a star: in the nontrivial Q-component branch the needed leaf v is in Q's own normalized component; in the singleton branch the other components are merely carried forward unchanged.

Crucially, every phase that decreases d has Q's component equal to the singleton {Q}. Such a component is already at its required rooted star and needs ZERO normalization exchanges. Thus every nonterminal component-decrease phase costs exactly one exchange, and there can be at most n-1 of them. The unique terminal gain phase costs at most D+6. The entire Step 3 therefore costs at most (n-1)+(D+6), rather than n(D+6).

Taking the maximum of the alternative immediate-gain and empty-owner routes, a strict k gain costs at most

    A3 = 2(D+1) + (n-1) + (D+6) = 6n^2 - 5n + 7.

This dominates the immediate positive-copy bound g+2=n^2+1 for n>=3. Thus the full controlled path length is bounded by

    T3 = (n-1) A3 + C = 6n^3 - 3n^2 + 8n - 5 <= 6n^3.

The resulting safe clean common-atom parameters are

    T = 6n^3,   gamma = (4n)^(-6n^3).

They imply a completely explicit full-state mixing estimate exp(O(n^3 log n)) log(1/epsilon), uniformly over all finite initial ages. Independent audit should check the observation that no other residual component needs normalization; that is the only change from the conservative O(n^4) argument above.

## Original invariant audit cautions

## Optional simpler root-clearing refinement: T = (n+2)^3

A full capacity-one normalization is unnecessary for zero-count improvement. In any reduced capacity-one component of m vertices, repeatedly activate a chosen Q until its reduced cache is empty. Every responder permanently learns Q; revisiting any responder returns self Q and empties Q's reduced cache. There are at most m-1 distinct responders and one terminal revisit, so at most m exchanges. An empty responder also terminates. These moves preserve the residual weak component. If m>1, once Q is its empty root, weak connectivity guarantees some residual incoming neighbor v -> Q. This neighbor has cache {a^0,Q^A} for some A>=0, which is all the infection lemma needs; A need not be zero.

Use this Q-only clearing in Step 2: owner emptying costs <=2(n+1). Use it also for the indicated Q in Step 3: terminal gain phase costs <=n+6, while all singleton component decreases combined cost <=n-1. Thus the two alternative strict-k-gain costs are

    g+2 = n^2+1,      2(n+1)+(n-1)+(n+6) = 4n+7.

Take A4 = max(n^2+1,4n+7). After universal a^0, empty owner with the same 2(n+1) bound, then retain the original conservative full-star construction: normalize all residual components <=D, perform <=4n root-merge exchanges, normalize connected remainder <=D. Thus

    C4 = 2(n+1)+2D+4n = 4n^2+2n+2.

The total witness length is at most

    (n-1) A4 + C4
      = max((n+1)^3, 8n^2+5n-5)
      <= (n+2)^3,    n>=3.

The last inequality is explicit: (n+2)^3-(8n^2+5n-5)=n^2(n-2)+7n+13>0. Consequently T=(n+2)^3, gamma=(4n)^(-T) are a clean candidate theorem. This refinement requires no new stochastic assumption, only the elementary root-clearing bound above. Independent audit should check it before selection over the more conservative bound.

## Local single-ID conditioning

At stationary label symmetry, every peer has the same expected cache size. Weak connectivity guarantees at least n-1 directed descriptors globally, so E_pi|C_i| >= (n-1)/n. Capacity two gives stationary nonempty availability alpha_i >= (n-1)/(2n) >= 1/3. If full-state TV error is d, the standard conditioning bound gives single-ID conditional sampling error <=2d/alpha_i <=6d. Thus an explicit sufficient single-ID mixing time is T ceil((4n)^T log(6/epsilon)); there is no need to lower-bound availability using the very small atom mass.

The progress invariant is the NUMBER k of zeros, not the inclusion order of zero-holder sets. Case A/B transfers can lose a former zero Q before the infection adds an extra one. This is legitimate because each macro endpoint strictly increases k, or keeps k fixed and strictly decreases d.

All residual normalizations operate on genuinely closed residual components, preserving their partitions and all zero anchors. The cost D is independent of initial ages. When c=1 theorem constructions contain no-ops, omit them during anchor simulation; all substantive choices remain legal.

In Case B the displayed X age at Q may decrease by MIN only if Q had X before the normalization; however after normalization C_Q={a^0}, so no old X is actually present there. The exact age can safely be left unspecified because only its identity is used after that exchange.
