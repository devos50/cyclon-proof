# Arbitrary n, arbitrary capacity c>=2, mandatory ell=1: common zero-age atom

THIS IS A CONSTRUCTIVE PROOF, pending independent audit. Exact kernel: active p increments cache ages, chooses an oldest q, removes q; sends fresh p only; responder q returns one uniformly selected pre-exchange descriptor (or nothing if empty); discard self and already-known identities without refreshing; fill vacancies, then replace the sent descriptor if needed. Capacity c; iid uniform initiators; uniform ties/replies. Any designated legal choices below have positive probability. Start weakly connected.

## Preliminaries

**Weak connectivity for ell=1.** Every exchange preserves its weak component. The removed p->q edge is replaced by q->p, either pre-existing or freshly inserted. If q was full and did not know p, its returned r is replaced by p; p retains or inserts r (r!=p,q), so the deleted q->r edge is represented by q->p->r. Every other resident edge persists. If q already knew p it makes no cache changes.

**Clearing block B(p).** Repeatedly activate p. Whenever contacted q already knows p, choose response p. Otherwise choose any response. First contacts to a q not knowing p cause q to learn p permanently during the block. There are at most n-1 such first-learning events. Every other activation shrinks C_p by one. Thus p empties in at most K=n+c-1 activations, regardless of ages or legal oldest choices. The choices when q does not know p remain freely controllable. If all ages were zero at block start, all ages are zero at its end: other nodes only receive fresh p; only p's residents are incremented, and all are gone when p empties.

Clearing each vertex once, even from arbitrary finite initial ages, produces a globally zero-age state, since after its own clearing each vertex receives only fresh later initiators. This costs at most nK activations.

## Canonical atom

For ordered V={0,...,m}, define H(V,c) by

  C_i = the min(c,m-i) GREATEST elements of {i+1,...,m},

all ages zero. Equivalently every nonlast vertex points to m and as many other largest later vertices as capacity allows. C_m is empty. H is weakly connected. We prove by induction on n=m+1 that every zero-age weakly connected state reaches H by a finite positive-probability path, for every fixed c>=2.

## Lemma A: separate an unknown source

From any zero-age weakly connected state, clear 0, then clear each member of W=V\{0}, while leaving 0 passive. At the end:

1. all ages are zero;
2. no W cache contains 0;
3. C_0 is nonempty and consists of W identities;
4. the graph induced by W is weakly connected.

Proof of (4) is the key. Immediately after clearing 0, every weak component of the graph induced by W contains some descriptor of identity 0: C_0 is empty, the whole graph is connected, so each W component must attach to 0 by an incoming W->0 edge.

During the remaining blocks, the W component partition can only coarsen. Exchanges entirely within W preserve its connectivity by the ell=1 edge-transfer proof, including when the response happens to be 0. An exchange with passive 0 deletes only the active p->0 edge outside W and adds or retains p->r for the response r in W, so it deletes no W edge.

The first W activation contacting 0 gives C_0 its first member and defines an anchor W component. Thereafter every identity held in C_0 lies in that anchor (which may grow): a new p contacting 0 receives an anchor identity r, unless r=p, in which case p was already in the anchor. Thus p joins the anchor before fresh p is stored at 0.

Every initial W component eventually joins the anchor. Otherwise such a component retains a 0 descriptor until a clearing block selects it. A descriptor 0 can be deleted only (i) by its holder contacting 0, directly joining the anchor, or (ii) by a full responder returning 0 and replacing it by fresh p. In case (ii), active p already holds or receives 0 and must contact 0 before its block finishes; the responder and p are linked in W. Hence deleting a component's last 0 descriptor forces it into the anchor. But after all W blocks no 0 descriptor exists, because every W node has been cleared and later passive injections contain only nonzero initiator identities. Contradiction.

The same argument guarantees at least one contact to 0, so C_0 is nonempty. Finally, once 0 is globally unknown in W, it cannot reappear while 0 remains inactive: initiator messages contain only their own nonzero identities, and replies can only copy identities already stored. Hence 0 can now be frozen, and its cache will not change during any evolution restricted to W.

## Lemma B: extend a canonical W by an unknown source 0

Assume all ages zero; no W cache contains 0; W is exactly H(W,c); C_0 is any nonempty cache in W. Let m=max W, d=min(c,|W|), J=the d greatest W labels, S=J\{m}. We construct a path ending with

  C_0=J;  0 globally unknown in W;  W weakly connected;  all ages zero.

### Phase 1: clear 0 using smallest-ID replies

Use B(0), choosing response 0 whenever the responder already knows 0 and otherwise its smallest cached identity.

Every nonroot W vertex initially knows m. A full responder contains at least two entries (c>=2), so its minimum is not m; replacing that minimum by fresh 0 retains m. An underfull responder does not evict anything. Thus throughout this phase every W vertex other than m retains its edge to m; W stays connected.

The block visits m. Otherwise take the greatest visited W vertex q. At its first visit, its untouched original canonical cache has a neighbor r>q, namely its minimum successor. This r is either already pending in C_0 or is inserted there; an unselected resident cannot be overwritten in ell=1. It must eventually be visited, contradiction. (If greatest visited q=m, done.) Because m starts empty and is only passive, it ends with exactly C_m={0}. All ages are again zero.

### Phase 2: create c-1 protected target entries at 0

For each j in S, first activate j toward m, then finish clearing j. At each unprocessed responder q, protect m if it is resident: when q is full and does not know j, choose a reply other than m; if q already knows j, use reply j; underfull replies are unrestricted.

Every j in S still knows m when its block begins. All ages are zero at every block boundary, so m can be chosen in the initial age tie. At that first j->m event choose reply 0. Before the event C_m consists of 0 and earlier S initiators, hence has size at most d-1<c (or <=c-1). Fresh j fills a vacancy, preserving 0. During the rest of j's block, m already knows j, so use reply j whenever revisited. Thus C_m remains exactly {0} plus the processed S initiators.

The initiator j either already retains a 0 descriptor or receives it from m. It cannot be overwritten without being selected because ell=1 receives at most one entry into the vacancy created by mandatory removal. Therefore j contacts 0 before its clearing finishes. C_0 only ever receives fresh S initiators during this phase and has fewer than c entries, so after all S blocks

  C_0=S,  C_m={0} union S.

Every processed j is now 0-free. All ages are zero.

### Phase 3: purge all other 0 holders while protecting one reservoir

Clear every h in W\J, keeping 0 at m: if m is full and does not already know h, choose any reply other than 0; this is possible because c>=2. If m knows h, reply h. An underfull m does not evict anything.

At passive 0, protect all S entries. Since |S|=c-1 whenever W\J is nonempty, there is at most one unprotected resident. For a new h, fill the vacancy if available; otherwise return/evict the unique unprotected resident. For a duplicate h, use reply h. These choices also satisfy the clearing-block rule.

At the end all W vertices except m have been cleared since their last possible acquisition of 0, and no fresh nonzero initiator message can reintroduce 0. Thus the sole remaining 0 descriptor is at m. C_0 contains S and at most one unprotected entry. All ages are zero.

### Phase 4: final callback from the reservoir

Activate m toward 0 first, which is a legal zero-age tie. If C_0 has an unprotected entry, choose it as the response/victim; otherwise use any response (possibly none), filling a vacancy. Fresh m is new at C_0 because m has never initiated in the construction. Consequently C_0 becomes exactly J.

This activation removes the globally last 0 descriptor. Finish B(m). With 0 now globally unknown and inactive, it cannot be contacted again; C_0=J remains fixed. All ages are zero at block end.

W is connected at the end. It was connected after Phase 1. Subsequently 0 is passive, so 0-involving exchanges only add W edges, while W-only exchanges preserve W connectivity, as proved in Lemma A.

This proves Lemma B. It uses exactly n clearing blocks, counting the special first activation in each relevant block. Every block ends globally zero-age.

## Induction

Base n=1 is the empty cache.

Given a zero-age connected state on V:

1. Apply Lemma A. Source 0 is unknown, C_0 nonempty, W connected and all ages zero.
2. Freeze 0. Apply the induction hypothesis to W, obtaining H(W,c); C_0 is unaffected because no one knows 0.
3. Apply Lemma B, obtaining C_0=J, 0 unknown, W connected and all ages zero.
4. Freeze 0 and apply induction to W a second time. C_0=J stays fixed.

The result is exactly H(V,c).

A uniform finite path-length bound is available recursively: B_1=0 and

  B_n <= 2n(n+c-1)+2B_(n-1).

Lemma A costs n clearing blocks and Lemma B n clearing blocks. Adding initial arbitrary-age clearing costs n(n+c-1). Pad any shorter path at H's empty root. A conservative per-activation probability lower bound is (n c^2)^(-1), accounting for initiator, oldest tie, and chosen response. Hence a uniform common-atom Doeblin bound follows with that finite total length.

## Remaining audit targets

- Verify Lemma A's W-component/anchor proof for descriptor-0 coalescence.
- Verify each special first activation in Lemma B is a zero-age tie.
- Verify protection policies are compatible with fast clearing when the responder knows the initiator.
- Verify Phase 1 greatest-visited argument and persistent m edge.

If these pass, this closes the ell=1 arbitrary-n arbitrary-capacity convergence theorem, including uniform stationary conditional local samples by relabelling symmetry. It does NOT settle ell>=2.
