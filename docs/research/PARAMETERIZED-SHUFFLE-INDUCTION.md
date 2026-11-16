# Parameterized induction interface for arbitrary shuffle length

**Status update, 16 November 2026:** The manuscript's new general source-route
working theorem (`thm:allparametersuniform`) supplies source creation and
complement joining through `lem:generalsourcecreation` and
`lem:generalsourceextension`. Two independent end-to-end internal audits have passed.
The construction below retains its original local/conditional scope. Its
historical source-accessibility obligation is discharged by that new route,
not by assuming the earlier restricted controllers work. This is not formal
verification, external peer review, or a polynomial mixing bound.

Research framework for audit, 16 November 2026. This isolates obligations; it does not prove arbitrary-length convergence. Fix an integer L>=3, n>=L+1, and L<=c<=n-1. All statements refer to the unchanged protected/MIN mandatory-removal kernel with exact fixed buffer sizes.

## Induction package and structural consequences

Assume (C_j), a uniform finite-horizon canonical common atom, for every smaller length j<L and every allowed population/capacity. Also assume (F_(L-1)), uniform holder-only first contact with a frozen cut at the immediately preceding length, including target-holder preservation except at terminal owner contact. No separate F_1 hypothesis is needed: the induction begins with the established F_2. The finite-age reset is independently available at every length.

Then the following hold at length L, without density:

1. **F_L:** uniform holder-only first contact, with a finite horizon independent of initial ages.
2. **U_L:** any universal zero anchor has a finite legal path to any prescribed labelled canonical atom.

For F_L, repeat the established minimum-age-holder construction. Within the current minimum-age holders of target r, reserve r in requests and replies. Removing that anchor gives length L-1 and capacity c-1. A residual oldest choice is actual-oldest if its age is at least the common target age; otherwise the target owner is already an actual oldest choice and the first contact succeeds. Open residual cuts use F_(L-1) on n-1 identities, capacity c-1. Closed residual components of m vertices have effective parameters

 d_m=min(c-1,m-1), e_m=min(L-1,m-1).

For m>=2, 1<=e_m<=d_m<=m-1, and e_m<L; C_(e_m) applies. A singleton contacts the target owner immediately. Take the maximum of the finitely many lower-length first-contact/common-atom horizons to define E. Each E-event phase removes a current minimum target copy or reaches the cut. At most s such phases raise the outside minimum by one, where s is outside population.

Raise the minimum R_s+1 times, where R_s=(sc+1)c, unless contact occurs first. The all-length young-count/holder-maximum routing argument then finishes within R_s events. Its reserved old target and required young difference need two extra slots, available because L>=3. The reply/victim bound is |D_q|+|Q intersect U|<=min(L,|Q|). Thus one may take

 T_L=s E (R_s+1)+R_s,
 eta_L=(nc 16^c)^(-T_L).

These are finite constants, not claimed practical or polynomial. No occasional shorter original shuffle is used: shorter kernels appear only under an exact reserved-anchor simulation.

For U_L, reserve the universal a^0 anchor and normalize residual components using the same d_m,e_m. To empty the owner, freeze it while normalizing its actual oldest head Q's residual component to root Q, so C_Q={a^0}. The owner's contact deletes Q; at Q fresh a and at most L-1 extras fit capacity c>=L. Repeat until the owner is empty. The established four-exchange component merges and root changes use caches of size at most two, so remain exact at every L>=2. Normalize the resulting residual component to obtain the prescribed canonical atom.

## Two remaining local obligations

The following pair suffices to finish the induction at L.

**B_L: Owner boundary service.** For every owner a, every subset H of its zero holders, and every cached p outside H union {a}, there is a finite legal path to an owner contact outside H, preserving all existing holders and zero copies before/through this contact. Every preterminal exchange is internal to H union {a}; all outside rows remain frozen. The designated p remains cached at the owner before the final contact. If the terminal responder differs from p, include p in the final request as an extra. The terminal reply may be any prescribed legal subset (in particular one containing a and a designated next path head when present). When a holder is the terminal responder, require a in that reply and choose active victims to retain p via the general designated-owner-target lemma. Thus service can continue through positive holders without losing its fixed nonholder target. No age-uniform local duration is required.

**O_L: Empty-owner outward gain.** If owner a is empty, all its h holders are zero, and some holder caches a nonholder distinct from a, a finite legal path attains N_a>h. Endpoint preservation of individual old holders is not required for this obligation.

B_L plus F_L first gives zeroification: positive-holder first contact with the frozen owner/zero cut either refreshes a positive copy or loses one at the owner, whose fresh cached nonholder permits B_L recovery. Repeating strict zero gains terminates. Consequently in a closed class, k=max Z_a bounds N_a everywhere; all holders at a zero maximizer are zero.

B_L through subsets H excludes directed owner paths to nonholders at a maximizing state: exclude the untouched suffix vertices from H, and require a and the next path head in each terminal path-vertex reply. These fit since L>=2. The next head is received/protected; shorten the suffix until contradiction. The owner's reachable region is therefore closed and contains only owner plus zero holders. Normalize only that region using the lower-length kernels and empty the owner as in U_L. This avoids circular use of O_L.

Now O_L excludes every holder-to-nonholder edge at each empty-owner maximizer.

## Incoming-boundary endgame for every L

Let I be the zero-holder set at an empty-owner maximizer and J the nonholders. If J is nonempty, weak connectivity, empty owner, and outward closure give an edge J->I. Use F_L to pause before a first outside contact P->Q, with Q in I. Normalize Q's closed residual component with root Q while P is frozen. Then C_Q={a^0} and P's pending oldest choice is unchanged.

If c>=L+1, the request has at most L identities and fits beside Q's anchor. P gains a^0 through its mandatory vacancy, while Q retains it, a contradiction.

If c=L, minimize additionally the number of residual weak components on I among all empty-owner maximizers. An underfull P has request size at most L-1, again giving a gain. Otherwise write its full cache {Q,R_1,...,R_(L-1)}. The boundary endpoint identity sets are

 C_P'={a,R_1,...,R_(L-1)},
 C_Q'={P,R_1,...,R_(L-1)}.

All displayed a copies at P are zero; Q loses its old zero because all L received entries are protected. Mandatory removal supplies P's one reply vacancy; no surviving resident is evicted. The new zero set swaps Q for P and owner stays empty. Every R_j must lie in old I minus {Q}, or new holder P has a forbidden outward edge. If Q's normalized component was nontrivial, another old holder points to root Q, a forbidden outward edge to the new nonholder. Thus Q's old component was singleton. Replacing it by P attached to the R_j in remaining components strictly decreases component count. This contradiction works for every L>=2; there is no separate higher-length endgame obstruction once B_L and O_L are available.

Hence every closed class reaches a universal zero anchor and U_L gives the common atom. The independent finite reset yields a finite reset-state reachability graph, whose terminal SCCs generate actual closed communicating classes. Choose and pad one path per finite reset state to the prescribed atom, obtaining uniform minorization. The common-atom contraction and label symmetry then give C_L and conditional sampling uniformity. Age-dependent B_L/O_L constructions do not need uniform durations because the reset precedes their use.

## Current bottlenecks, not proved induction hypotheses

The package is established through L=3. Thus F_4 and U_4 follow, but C_4 does not follow without B_4/O_4 (or another route).

The length-three callback relied on one residual reply slot after reserving self-a and one target p. For L>=4, an overlap can coexist with novel replies without decreasing owner head count. Passive overlap copies may repeatedly refresh an owner minimum; the previous minimum-draining proof no longer applies directly.

Likewise, the length-three outward lexicographic controller used the fact that a reply containing a and the initiator leaves one residual slot. More slots can introduce additional old-identity copies and increase the active cache without increasing the static outside-holder identity count. A higher-dimensional residual progress measure or a lower-length reduction on equality cases is needed. Neither a failed controller nor an owner-only cycle is a counterexample to the full protocol.

## Exact obstruction to the unchanged outward controller, every L>=4

Take five distinct identities a,p,r,q,s, with

 C_a={}, C_p={a^0,r^0,q^1},
 C_q={a^0,p^0,r^0,s^1}, C_s={a^0,p^0,r^0,q^1},
 C_r={p^0}.

This is a five-node core. For any allowed parameters 4<=L<=c<=n-1, add n-5 peers, each with singleton cache {r^0}, and never activate them in the restricted trajectory. Thus the construction is a legal five-node instance only when n=5,c=L=4; all larger parameter choices use this explicit embedding. The overlay is weakly connected. Its a holders are p,q,s, all zero. Current p caches nonholder r, and owner a is empty, so this is a legitimate outward-gain starting state.

If only current p initiates, its unique oldest head alternates q,s forever. The request is forced to be {p^0,a^1,r^1}. Each responder has four entries, so its entire cache is the required reply at every L>=4. Passive MIN merges change nothing. The active self-p reply filters out, refreshing a,r to zero and replacing the selected head with the other head at age one. Thus C_p alternates exactly between {a^0,r^0,q^1} and {a^0,r^0,s^1}. There is no sampling or victim choice that changes this restricted trajectory.

For fixed Z={q,s} and Y=V minus (Z union {a}), both the static count F and the current cache size remain constant (F=6 on the five-peer core, and F=n+1 after the singleton-peer embedding). Hence the length-three strict-zero-contact potential cannot extend unchanged. This is an obstruction only to current-only control and that strict potential; cooperative activation is allowed in the actual process and may escape. It is not a counterexample to convergence.
