# A genuine enhanced, mandatory-removal, multi-entry convergence theorem

Parameters: n=3, c=ell=2, iid uniform initiators, uniform oldest-age tie breaks; caches are sets of nonself identities with finite nonnegative integer ages; duplicates discard without refreshing ages; responses use the complete pre-exchange responder cache; initiator sends its fresh self and its other entry (if any), removes the contacted partner unconditionally, then accepts usable replies; responder inserts usable received entries into vacancies (no additional capacity issues arise when n=3). Empty initiators are no-ops. Start in any weakly connected identity overlay.

THEOREM: The entire countable-state chain has a unique stationary distribution pi on weakly connected states and, for delta=6^(-20),
  ||P^t(x,.)-pi||TV <= (1-delta)^floor(t/20).
Pi is invariant under all peer relabellings. Consequently a uniformly ordered b-tuple sampled from peer i's cache, conditionally on size >=b, tends in TV to the uniform law on distinct tuples excluding i, for b=1,2. Availability tends to a strictly positive value. This is a theorem for actual age-driven, multicache CYCLON, although only the minimal n=3 case.

PROOF:

Simplification: The responder never deletes a descriptor: all possible nonself identities number only two, and it merely unions usable incoming descriptors into its cache. The initiator always finishes with at most one entry: its partner cannot be returned by that partner, and its own identity is filtered. Thus if the initiator initially has two entries, it finishes with exactly its other entry (incremented by one). If it has one, it finishes with the responder's possible third identity, or empty.

Weak connectivity is invariant. If any full cache exists afterward it is automatic; otherwise an exchange with an empty responder reverses an edge, a reciprocal singleton exchange deletes only one of two reciprocal arcs, and a distinct singleton chain creates a full responder.

Use F,S,T to denote distinct vertices. A chain configuration has F full, S pointing F, T pointing S:
 C_F={S^a,T^b}, C_S={F^d}, C_T={S^e}.

Lemma 1 (chain age reset). From every chain configuration, an all-age-zero state of form Z(full U, singleton V->W, empty W) is reachable in at most eight exchanges.
If b>=a, use the five exchanges
  F->T, S->F, F->S, T->S, T->F.
They are legal, and end
  C_F={T^0}, C_S={F^0,T^0}, C_T=empty.
The fourth oldest choice is valid even when e=0 (a tie).
If a>b, activate full F toward near-chain vertex S, producing a new chain whose full vertex is S, near vertex T, and leaf F, with full ages (near,leaf)=(b+1,d). If d>=b+1, apply the five-step reset after relabelling. Otherwise d<=b, activate full S toward near vertex T. The new full T has ages (near F,leaf S)=(d+1,e). If e>=d+1, reset. Otherwise e<=d<=b; activate full T toward near F. The new full F has ages (near S,leaf T)=(e+1,b+1); the leaf is now oldest. Three rotations suffice, followed by five reset steps.

Lemma 2 (identity reduction). Any weakly connected state reaches a chain configuration within seven exchanges.
- Three full caches: one activation leaves two full and one singleton.
- Two full caches A,B and a singleton C: Activate a full A. If its oldest is full B, the number of full caches falls to one, with two singleton caches. Otherwise it contacts singleton C and C becomes full. If C previously pointed B, its new ages are B^u,A^0, so choose full B next (oldest or age-zero tie) and reduce. If C previously pointed A, its new cache is {A^u,B^(v+1)}, where v was A's residual B age. If B is oldest, activate C toward B and reduce. Otherwise activate C toward singleton A. A then becomes full with entries B^(v+1),C^0, so B is strictly oldest. Activate A toward B and reduce. Thus at most three full activations suffice.
- Two full, one empty: Activate a full. Contacting the other full yields one full, one singleton, one empty; contacting the empty yields two full, one singleton, handled above. At most four steps reach one-full states.
- One full, two singletons: If their arrows form a chain ending at the full vertex, done. If both point to the full vertex, activate either singleton toward the full; it now points to the other singleton, giving a chain. If the two singletons point at one another, let Q be an oldest neighbor of the full vertex. Activate Q toward the other singleton, making Q empty, then activate the full vertex toward Q. This yields a chain with Q full. At most two steps.
- One full F, one singleton S, one empty E: If S points F, activate S toward F, obtaining S->E. By activating S->E if needed, arrange that an oldest neighbor of F is empty. Activate F toward that empty vertex. Now there is one full and two singletons. At most three steps before the preceding case.
- One full, two empty: one full activation yields one full, one singleton, one empty.
- No full, three singletons: Weak connectivity guarantees a directed path P->Q->R with all three distinct. Activate P toward Q, obtaining one full and two singletons.
- No full, two singletons and one empty: Weak connectivity gives a directed path to the empty root, or two arrows into the empty root. In the path case activate the leaf toward its singleton parent, producing one full/one singleton/one empty. In the two-arrow case reverse one arrow by activating it toward the empty root, then use the path case. At most two steps.
No other weakly connected cache-size pattern exists. The worst routes to a chain take at most seven exchanges: two-full/empty -> two-full/single -> one-full/two-single -> chain takes <=1+3+2=6; no-full two-single -> one-full/single/empty -> one-full/two-single -> chain takes <=2+3+2=7; other cases are no longer.

Thus every weakly connected aged state reaches some all-zero Z in <=15 exchanges.

Lemma 3 (common atom). Write Z(F,S,E) for C_F={S^0,E^0}, C_S={E^0}, C_E=empty. The operation S->E implements Z(F,S,E)->Z(F,E,S) in one exchange. The operation F->S followed by F->E implements Z(F,S,E)->Z(S,E,F) in two exchanges (in the intermediate state F->E has age1 and then disappears). These operations generate S3. More specifically, to prescribe the full vertex, use at most one swap and one rotation (three steps), then at most one swap to prescribe the remaining roles. Any desired Z is reachable from any other in <=4 steps.

Combine: fixed common atom z=Z(1,2,3) is reachable from every x in <=19 steps. Pad to exactly20 by repeatedly activating its empty vertex (a no-op). Each designated initiation has probability1/3 and each designated oldest choice probability>=1/2. Hence P^20(x,{z})>=6^-20 uniformly in x. Doeblin's theorem gives existence, uniqueness, and the displayed bound (can also prove by splitting P^20=delta*delta_z+(1-delta)R and contraction).

The weakly connected state space is invariant under peer relabelling, as is the transition rule, so uniqueness implies pi is relabelling-invariant. Permutations fixing observer i act transitively on distinct b-tuples, proving conditional uniformity of the stationary output. For every observer i, choose a relabelled atom with i full; the same minorization gives pi(cache_i full)>=delta, so availability is positive for b=1,2. Full-state TV convergence implies convergence of the output and its conditioning.
