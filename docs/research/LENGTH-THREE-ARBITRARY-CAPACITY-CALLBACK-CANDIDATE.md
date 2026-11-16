# Owner boundary service for arbitrary capacity at length three

Independently reviewed working proof, integrated in the manuscript on 16 November 2026. Exactly `ell=3`, `c>=3`; not higher lengths. This is a finite existential accessibility argument, not a stochastic fairness assertion or quantitative bound.

## Statement

Fix owner a and any subset H of its zero holders. If its cache contains p outside H union {a}, a finite legal path ends with owner contact outside H, preserving all existing holders and all existing zero copies. No initial shared-p assumption.

## Controlled owner-only policy

Until boundary contact, retain p and include it in the request. Every responder q in H replies with a, and after learning p replies with a,p plus one residual C (when present). Retaining p before learning is legal explicitly: the reply contains self-a, leaving at most two usable identities; mandatory deletion supplies at least one vacancy, so at most one victim is needed. If the other sent extra B is received, it is already a duplicate and at most one reply identity is novel, requiring no victim. Otherwise B is an eligible victim instead of p. With no B the owner has only p and its selected head and sufficient vacancies. Responders learn p on first visit and never lose it on later owner contacts. Thus after finitely many first learnings every recurrent responder knows p.

Once p is known, owner reply has at most one novel identity; owner head count k excluding p cannot increase. If q has no residual, it decreases. If q has a residual already among the owner's retained non-p heads, choose that identity as C: again k decreases. Otherwise choose a minimum-age residual C.

For k>=2 send p and one other retained head B as the two extras. Choose B with bounded-fair rotation: assign newly arriving heads the current timestamp and choose a retained head with oldest last-sent timestamp, updating its timestamp when sent. Any head remaining unselected forever is eventually sent. This is an explicitly chosen deterministic control policy, not a property of the random scheduler.

Suppose no boundary is ever reached and k stabilizes at k>=2. At every late event the responder residuals are disjoint from retained owner heads, since overlap would force a decrease. In particular B is novel at q. A not-full q gains one entry; a full q evicts C, the only sent residual not received. Passive occupancies never decrease. After finitely many such increases, every infinitely visited responder is full.

Let S be the infinitely selected responders. A root head outside S appearing after the last outside-S selection would persist forever. By the B policy it is sent to some recurrent q. That q retains it until its next visit (only the owner is active), when overlap forces a head decrease. Contradiction. Thus eventually every owner head belongs to S.

At this tail, include the k owner-head ages and all residual ages at S in one multiset. Select root q:A and send another root B:b; return q residual C:d. Owner deletes A, increments every retained root head, and receives C:d. Responder removes C:d and inserts B:(b+1). The old C merely moves. Every old root minimum disappears, and no new copy of the current minimum is created. Each passive minimum is eventually removed because its source is visited infinitely often and minimum C is chosen. Consequently the integer minimum tends to infinity.

This argument initially allows residual pointers from S to outside S. Such a pointer retains its fixed age until returned as C. The diverging minimum forces that return, contradicting the already established eventual owner-head containment in S. Thus S is residually closed on a sufficiently late tail.

The p ages on owner plus S have finite maximum M: each endpoint update is min(u+1,v), between the old integer ages. Freeze owner once all S residuals have age at least M. Choose its actual oldest head Q. With a,p reserved, use Q-only singleton residual clearing inside S (residual capacity c-2). Return Q whenever known. First visits install fresh Q, repeats self-filter Q and shrink its residual cache. Initial residual ages >=M make all chosen residual partners legal against p, and p stays <=M. The residual cache clears after finitely many events. The still-legal owner contact Q then returns only a,p, reducing k. All old zero holders survive. Restart as necessary. Across both owner-only prefixes and these clearing interventions the learned set J is monotone. Owner head count can increase only on a first learning, by at most one, and there are finitely many such learnings. Clearing interventions strictly reduce head count and never undo learning. Thus repeated interventions cannot continue indefinitely, even when they subsequently expose previously unvisited responders.

## Stable one-head phase

Owner cache is {p,Q}. If p is oldest, finish. Otherwise Q is oldest. Owner requests contain only a,p, so passive residual graphs and ages do not change. In this one-head phase choose C in a fair cyclic rotation through each responder's residual entries. Empty residual rows immediately reduce to p. On a hypothetical infinite stable learned tail, every residual outgoing edge of every infinitely visited vertex is traversed infinitely often. Thus its infinitely visited set S is residually closed, and all its members know p. This fairness is an explicitly controlled choice, not an assumption on random trajectories.

Freeze owner and perform Q-only singleton clearing, but stop when residual cache empties or its maximum age b falls below Q's p age v. Until stopping, choose residual oldest partners, reserving a,p. First visits/repeats make this finite. Owner then contacts frozen Q, retaining p with new age w=min(u+1,v), and receiving at most one residual of age b<v. If continuation is required, b>w; hence w=u+1. The global p maximum on owner plus S cannot increase. Only finitely many continuing macros are possible. This gives a boundary contact with p.

## Audit obligations

1. Verify bounded-fair B policy and closure argument with changing root heads.
2. Verify one-head fair-reply policy gives residual closedness after the finite learning and head-count transients.
3. Verify Q-only clearing remains inside S and preserves p bounds and all a-zero holders.
4. This is only the callback. Sparse-capacity outward gain and extremal assembly must be separately established; the capacity-three terminal gadgets cannot simply be copied when packets are partial.

## Final integration status

This working result is now integrated in the manuscript after independent end-to-end and actual-text audits. See [the audit record](LENGTH-THREE-AUDIT.md). Earlier candidate wording in this research history is superseded by that status; no formal-verification or external-review claim is made.
