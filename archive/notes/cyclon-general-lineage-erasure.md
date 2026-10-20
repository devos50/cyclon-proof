# General mandatory-removal CYCLON: initial-lineage erasure is accessible

Assumptions: static n>=2, capacity c>=1 (c may exceed effective universe size without affecting proof), shuffle length 1<=ell<=c; reliable atomic exchanges; ages increment only at the initiator; mandatory deletion of the chosen oldest partner; initiator sends fresh age-zero self plus min(ell-1,a-1) other entries; responder returns min(ell,b) pre-exchange entries; duplicates/self filtered without refreshing ages; insert all usable incoming descriptors, filling vacancies before replacing only sent descriptors; each valid buffer/victim/tie/initiator choice has positive probability. An old mark is attached to every descriptor initially present; copies inherit their source mark, new self descriptors are fresh.

The theorem concerns erasure of initial descriptor lineages, not erasure of all initial-state dependence.

## 1. One-entry protection with slack

If ell<c, an arbitrary designated nonpartner entry at an initiator, or designated entry at a responder, can be retained.

At an initiator of size a>ell, exclude it from the ell-1 extra entries. If a<=ell, all a-1 nonpartner entries are eligible but mandatory deletion creates c-a+1>=ell-a+2 vacancies. At most ell usable replies require at most a-2 replacements, so a designated nonpartner can remain.

At a responder of size b>ell, exclude it from the reply. If b<=ell, all b entries are eligible, but c-b>=ell+1-b vacancies leave at most b-1 required victims.

Even when ell=c, a designated responder entry remains protectable whenever its identity appears in the incoming packet: that incoming duplicate is discarded, leaving at most c-1 usable insertions and hence at most b-1 victims in the responder's all-b reply buffer.

## 2. Routing a designated descriptor until its identity is contacted

Choose a cached descriptor of identity z and age a. Activate its current holder, retaining that particular descriptor whenever possible. For ell<c the preceding lemma always allows retention unless it is the selected partner.

For ell=c, write P for its current holder p's identity cache, of size A, and Q for the responder cache. All A-1 nonpartner entries are sent. After partner deletion there are c-A+1 vacancies. A nonpartner target is unavoidably evicted only if all A-1 eligible entries must be replaced, which requires exactly c usable replies. Hence Q is full, its complete reply is disjoint from P union {p}, and its incoming packet consists of A new identities. The target is necessarily accepted there. Follow that copy. Its age is exactly the previous tracked age plus one, since it was incremented at the initiator before transmission.

Thus in either regime we can ensure a distinguished descendant exists with age a+t after t routing events, until its identity z is selected as partner.

Let M_s(t) be the global maximum age of descriptors with identity s, with value zero when absent. For every scheduler, K_s(t)=M_s(t)-t is nonincreasing: resident ages increase by at most one per event, copies preserve their source age, and newly generated self descriptors have age zero. Whenever s is selected as partner, M_s cannot increase in that event: the unique initiating s descriptor is deleted and excluded from the outgoing packet, responder s has no self descriptor, and every other s descriptor remains unincremented. Therefore K_s decreases by at least one.

While the tracked descriptor survives, any selected partner s!=z has age at least a+t before increment, hence K_s(t)>=a. Identity s can be selected at most (M_s(0)-a+1)_+ times. Consequently the target identity z is contacted within

  1 + sum_{s!=z} (M_s(0)-a+1)_+ <= 1+(n-1)(B+1)

routing events, where B is the initial global maximum age. This includes all s!=z because the tracked holder may change.

## 3. Clearing one old identity by growing an immune set

Fix identity r. Call a peer immune when it stores a fresh r descriptor. Retain that descriptor at each immune peer, and do not activate immune peers during this stage. Peer r itself cannot be immune, since self descriptors are excluded.

If old r remains, pick a holder and route a distinguished old r descriptor as in Section 2 until it is selected as partner. Previously immune peers remain passive. When ell<c, their fresh r is protected by the slack lemma. When ell=c, every nonfinal routing packet contains the tracked old r, since the partner has a different identity and all nonpartner entries are sent. An immune responder therefore discards this duplicate and can protect its fresh r. Moreover it cannot be a forced-migration destination, because its reply r is already known at the initiating holder, preventing c usable replies.

At the final routing exchange, let q be the tracked holder. It deletes r, and responder r cannot return its own identity, so q is now r-free. Responder r receives fresh q. If q was absent, it inserts it; if q was already present, retain it. This last retention is always possible: incoming q is discarded as a duplicate, leaving at most c-1 usable incoming descriptors and at most b-1 required responder victims.

Now activate only peer r, retaining its cached q when possible. Stop as soon as q is selected or is unavoidably evicted. The constant-holder version of the virtual-age argument ensures such a stop within 1+(n-2)(B+1) events, for the maximum B at the start of this block.

If q is selected, q has remained passive and r-free until this contact, and receives the fresh self descriptor r, becoming newly immune.

If q is unavoidably evicted, this can happen only for ell=c with c usable replies. The responder u is then full and has no identity in C_r union {r}; in particular it does not know r. It accepts the fresh self descriptor r and becomes newly immune. It is unnecessary to immunize the original q in this case.

Previously immune peers stay passive throughout this r-only block. Every incoming packet contains fresh r, so their duplicate rejection leaves enough freedom to preserve fresh r even for ell=c.

Each iteration therefore adds a genuinely new immune peer, using at most two forcing blocks. After at most n-1 iterations no old r exists anywhere, since all peers other than r are immune or extinction occurred earlier. Old r cannot be recreated: copying preserves identity and color, and new self r descriptors are fresh.

## 4. General accessibility theorem and explicit bound

Repeat Section 3 for all n identities. This requires at most

  D=2n(n-1)

forcing blocks and removes every initial descriptor lineage, for every n,c,ell under the stated kernel.

If M0 is the initial maximum age and S the elapsed length, all current ages are at most M0+S. Put R=M0+S+1. A forcing block has length at most 1+(n-1)R<=nR. Hence R increases by at most a factor n+1 per block. The entire execution has length at most

  ((n+1)^D-1)(M0+1).

Every descriptor remaining afterward was generated during this execution and has age at most the execution length. All prescribed choices are legal and have positive probability.

This is an age-dependent reachability result. It does not supply a uniform finite-set reset, a Foster-Lyapunov drift inequality, positive recurrence, or convergence. Even complete initial-lineage erasure does not remove dependence of fresh descriptor locations on the initial topology.
