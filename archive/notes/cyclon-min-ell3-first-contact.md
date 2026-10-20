# Uniform frozen-boundary first contact for ell=3

Kernel: the adopted protected+MIN protocol, integer ages, c>=3. The result below applies to every finite n and every c>=3 (with c<=n-1), using the newly completed arbitrary-capacity ell=2 theorem. It proves holder-only first contact, not common-class uniqueness, stationary uniformity, or full zeroification at ell=3.

Fix nonempty proper G, let S=V\G, s=|S|, and suppose a cache in S contains identity r in G. Freeze G. There is a controlled path of uniformly bounded length, independent of all numerical initial ages, that contacts G using only S initiators.

## Lower-length constants

On population N=n-1 with capacity d=c-1, the ell=2 first-contact theorem supplies a finite controlled horizon A_a for every outside size 1<=a<=N-1. It does not require weak connectivity or assumptions on the frozen caches.

For each 2<=k<=n-1, set d_k=min(c-1,k-1), ell_k=min(2,k-1). Let U_k be a common-atom accessibility horizon for the adopted kernel on k weakly connected peers at these parameters. These horizons exist uniformly over arbitrary ages. For k>=3 and d_k>=2, use the now completed arbitrary-capacity ell=2 theorem; if k=2, use the ell=1 capacity-one theorem. If the configured capacity exceeds k-1, the effective-capacity description has identical valid-cache updates because overflow is impossible.

The common-atom theorem gives a fixed positive-probability horizon, hence from each starting state at least one controlled path of length at most U_k to a state with an empty designated cache. The root/order may be prescribed; only existence of some empty cache is needed here.

Choose

    E = 1 + max( {A_a:1<=a<=n-2} union {U_k:2<=k<=n-1} union {0} ).

This is a finite constant depending only on n,c and previously proved lower-length theorems. No truncation, rank quotient, or subtraction of the anchor age is used.

## One minimum-age copy can be removed in at most E exchanges

Let m be the minimum age of r among S caches and let A be its outside holders. All members of A store exactly the descriptor r_m; they may have arbitrary other ages, including ages smaller than m.

For an A-internal controlled exchange, reserve r as one outgoing extra and one reply entry. Delete the r descriptor from these caches. The remaining exchange is exactly the adopted kernel of capacity c-1 and length two: the original length-three packet is the reduced fresh self plus its one reduced extra, together with r; the original reply is its at-most-two reduced reply, together with r. The anchor is protected at both endpoints and MIN restores its age to m. All other capacities, merges, and eligible victim counts agree.

The only extra constraint is oldest selection. A prescribed oldest residual partner is an actual oldest partner whenever its age is at least m. If the residual maximum is smaller than m, the anchor r is the actual oldest and its selection contacts owner r in G immediately, which is already success. If the residual cache is empty, the full cache is the singleton r_m and its next activation likewise contacts G. Thus arbitrary lower-length paths can be simulated until an early successful owner contact; no assumption about the magnitude of m is needed.

There are two cases.

1. Some residual A cache contains an identity outside A, other than r. Work on W=V\{r}; put arbitrary empty auxiliary caches at W\A and invoke the lower-length first-contact theorem with active set A and frozen set W\A. All caches inspected before the terminal contact are A caches, so the auxiliary choices outside A never affect the simulated path. At the first terminal contact with q outside A, either q belongs to original G (success), or q is in S\A and lacks r_m. Execute the full exchange with a reply containing r whenever q has it. The active r_m is incremented to m+1, no incoming r_m exists, and the outgoing anchor has age m+1. Thus at least one minimum copy disappears and no new one is born. The prescribed auxiliary terminal reply is irrelevant because the construction stops there and chooses a legal actual reply instead.

2. Every residual A cache contains only A identities. Pick one weak component K of its residual identity graph. If |K|=1 its residual cache is empty and the next full activation contacts owner r. Otherwise the reduced K kernel has effective parameters d_|K|,ell_|K| above. Simulate its common-atom path. If it is interrupted by an actual oldest anchor, G is contacted; otherwise it ends with an empty reduced cache, and one additional full activation contacts owner r. The configured residual capacity c-1 may exceed |K|-1, but then both descriptions have no possible overflow and induce exactly the same valid-cache updates. Buffer lengths are likewise truncated by available cache size.

These paths take at most E exchanges. Every preterminal initiator belongs to A and sends r, and every internal responder is also in A and returns r_m. The count of minimum copies stays fixed until the terminal event, at which it decreases or G is contacted. At most s such phases therefore increase the outside minimum r-age by at least one within sE exchanges, or contact G.

## Holder-only routing after minimum raising

This strengthens the earlier reset-or-hit completion and uses no maximal-holder assumption or no-extra-eviction condition. Put R_s=(sc+1)c. Raise the outside minimum r-age above R_s in at most sE(R_s+1) exchanges, or contact G, by the preceding minimum-copy phases.

Now color every existing descriptor OLD and every newly created fresh self YOUNG. Duplicate colors merge by YOUNG-OR, independently of the numerical MIN supplier. Thus at routing time t every YOUNG descriptor has age at most t. All r descriptors remain OLD and have age greater than R_s. Every selected partner of an r-holder is therefore OLD during the next R_s events.

Let F be the total number of YOUNG descriptors in S, f_p their number at peer p, and M the maximum f_p over r-holders in S. Choose an r-holder p with f_p=M. In its outgoing extra set reserve r and, if Y_p is not contained in Y_q, one descriptor in Y_p\Y_q. These are at most two required extras, feasible at length three: if a cache has only two entries both are the OLD partner and OLD r, so there is no required YOUNG extra. Fill the ordinary extra set to its required size.

Use the general protected fresh-count controller: responder victims exclude all incoming IDs and all YOUNG IDs already at the initiator (also the self ID p); every YOUNG victim is returned as a new protected copy at p. Strengthen its reply requirement by including ALL responder IDs already in the outgoing packet U, not merely its YOUNG ones. If d0=|C_q intersect U| and r_q victims are needed, then r_q+d0<=min(ell,|C_q|), so this stronger reply remains feasible. At the initiator choose OLD eligible extras as victims first. The already audited general fresh-count inequality applies unchanged, including when extra OLD IDs are protected by their reply.

Consequently F never decreases. On F plateau, the controlled-choice argument implies Y_p subset Y_q and p in Y_q, hence f_q>=f_p+1. The responder q cannot already have held r, by maximality of f_p among r-holders. It newly accepts protected r. On this plateau the only YOUNG changes are t responder victims copied to new initiator locations, so

    f_p'=f_p+t,   f_q'=f_q-t,   0<=t<=f_q-f_p-1.

The bound on t follows because the victim IDs avoid Y_p union {p}. Thus f_q'>=f_p+1=M+1, and the new r-holder q raises M even if p loses its r extra. Other old r-holders are unchanged. In all cases the integer lexicographic pair

    (sc-F, c-1-M)

strictly decreases at each internal routing exchange. The second coordinate is nonnegative because r is OLD at every r-holder, and it takes at most c values. The first takes at most sc+1 values. Therefore at most R_s=(sc+1)c exchanges contact G.

Every initiator in this complete first-contact construction is an r-holder. Every preterminal packet includes r, and the reply contains r whenever the responder knows it (the strengthened all-shared-IDs rule). Hence the total number of r-holders never decreases before the terminal owner-r contact; this is exactly the holder-count property used at length two.

A uniform controlled horizon is

    T3 = sE(R_s+1)+R_s,  R_s=(sc+1)c.

Each prescribed full-protocol event has probability at least beta=(n c 16^c)^(-1), hence contact probability at least beta^T3. Before any random cross exchange the outside presence of r is preserved, so the full-chain geometric block-tail argument applies as at length two.

## Scope and the remaining gap

The result now IS holder-only, including its final routing stage. It holds at ell=3 for every capacity c>=3, since the lower-ell2 common-atom theorem is now established for arbitrary capacity. It still does not prove general positive-anchor zeroification: after a terminal owner contact the owner-only callback at length three remains unresolved. No full common-class or stationary-uniformity claim is made without universal-zero-anchor accessibility.

More generally the same holder-routing proof works for every ell>=3, reserving r plus one required YOUNG-difference extra. An inductive first-contact theorem therefore follows whenever length ell-1 has uniform first-contact access and uniform empty-cache access on the residual components encountered.

## Additional structural lemma: a universal zero anchor suffices

For every c>=3, a state with universal a^0 reaches a common labelled all-zero canonical state at length three. This is conditional accessibility only; the general production of the universal zero anchor is not proved.

Reserve a in outgoing extras and replies and freeze its owner. The standard anchor reduction exactly simulates the lower-length ell=2, capacity c-1 kernel on the other peers. Each residual weak component therefore admits its lower-length common atom, with any prescribed root/order. All anchor zeros remain zero.

First empty C_a. For any currently cached q, normalize q's current residual component with root q, so C_q={a^0}. Activate a toward q. This is a legal oldest target if q is chosen from the owner's actual oldest entries; normalize that q after it is chosen, since the normalization does not touch owner a. Its sole reply is self a and is discarded. Thus C_a loses q, while its remaining entries are retained and q's anchor is protected by incoming fresh a^0. Other owner's extras may join residual components but cannot remove an anchor. Repeating at most c times empties C_a.

Normalize each current residual component to a rooted lower-length canonical state, and choose two roots u,v. Their actual caches are {a^0}. The four-event path

    u->a,  v->a,  a->v,  a->u

merges these components, preserves every zero anchor at its endpoint, and restores the empty owner. Indeed after the first two events C_u is empty, C_v={u^0}, and C_a={u^0,v^0}. Choose v on the zero-age tie. The third event returns u^0, leaving C_a={u^0} and C_v={a^0,u^0}; the fourth leaves C_a empty and C_u={a^0}. These buffers have length at most two, so the calculation holds without modification for every configured ell>=2 and c>=2. All other caches remain unchanged. Normalize the merged residual component and repeat until the residual graph is connected. Finally apply its lower-length common-atom path with a fixed order. The owner stays empty and all descriptor ages are zero, giving the same labelled endpoint from every universally anchored state.

## Caution: owner-only target service is false at length three

Take n=4, c=ell=3, owner a=0 and nonholder target z=1, and let

    C_0={1^0,2^1}, C_1=empty,
    C_2={0^0,1^0,3^1}, C_3={0^0,1^0,2^1}.

Activating only owner0 produces an exact two-event cycle. Its unique oldest
partner is2, the request is {0^0,1^1}, and the full reply is {0^0,1^0,3^1}.
MIN leaves C_2 unchanged and changes C_0 to {1^0,3^1}. The next unique oldest
partner3 returns to the displayed state. Target1 is never contacted. Thus
shrinking a three-entry owner cache to two entries does not finish a callback.
This is an obstruction to an owner-only proof, not to full convergence.

The same example has a cooperative repair preserving both old zero holders:
activate2->3, then0->2, then0->1. The first event leaves C_2={0^0,1^0} and
C_3={0^0,1^0,2^0}. The second returns only 0^0,1^0 and leaves the owner with
the singleton1^0. The third sends fresh0^0 to nonholder1 and makes it a new
zero holder. The missing general lemma is a cooperative version of this
repair for arbitrary zero-holder residual graphs.
