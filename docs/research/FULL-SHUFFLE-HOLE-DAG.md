# Full-capacity full-shuffle hole DAG and stationary availability

## Scope

Adopted protected/MIN mandatory-removal kernel, iid uniform initiators, fixed membership, and **L=c=n-1**. This is a new structural invariant and availability bound, not a polynomial mixing theorem. The argument below has passed an independent internal adversarial audit, not formal verification or external review.

For each peer p define its hole set D_p=V\(C_p union {p}), ignoring descriptor ages. Draw a hole arc p→j when j is in D_p.

## Exact hole update

No eviction can occur at full capacity. Full shuffles send every available nonpartner descriptor and reply with the entire passive cache. For a legal contact p→q let I=D_p intersection D_q. Then exactly

- D_q'=I;
- D_p'=I union {q};
- all other hole sets are unchanged.

The intersection contains neither p nor q. At the active endpoint q is removed unconditionally and cannot return in q's own reply. Every other missing identity must have been absent at both endpoints. At the passive endpoint fresh p is inserted and all the active endpoint's other identities are received. This proves the formulas independently of all numerical ages and oldest ties.

## DAG invariant

If the hole graph is acyclic before the contact, it remains acyclic afterwards. All hole arcs after the contact were already present except the new arc p→q. Any new simple directed cycle must therefore use p→q. It cannot be a two-cycle, since q→p is absent. Write its next edge q→r. Because q's new outgoing holes equal I, r was already a hole of p. The remaining simple path r→...→p avoids p and q until its final endpoint, so all its arcs were already present. Replacing p→q→r by the old edge p→r would produce an old directed cycle, a contradiction.

An empty active row is a no-op, also preserving the property. The argument proves an invariant for every legal oldest choice, not merely for an average update.

## Stationary consequence

The full-capacity canonical H(V,n-1) has an acyclic hole graph: its holes point towards lower canonical labels. Its entire reachable class therefore has acyclic holes. Starting from H, the existing unique-stationarity/full-state-convergence theorem implies that the stationary law π is supported on hole DAGs. This does not assert that every arbitrary initial hole graph is acyclic at time zero.

Order any hole DAG topologically as v_1,...,v_n with arcs pointing forward. Peer v_i has at most n-i holes, hence

|C_(v_i)| >= (n-1)-(n-i)=i-1.

Thus, for every 1<=b<=n-1, at least n-b peers have caches of size at least b. In particular some cache is full in every such state. By stationary label symmetry, for each fixed observer i,

a_b=π(|C_i|>=b) >= (n-b)/n.

This improves the complete-undirected-support bound for multi-identifier requests and gives full-cache availability at least 1/n. It is a **stationary fixed-observer bound**. The deterministic aggregate count holds at every hole-DAG state, but the same fixed-observer probability bound does not follow for an arbitrary nonexchangeable transient law.

The bound is sharp as a statement about all hole DAGs: the canonical H has row sizes 0,1,...,n-1. No claim that stationary equality holds is made.

## Sampling consequence, not a mixing-rate claim

If a valid full-state estimate is d(t), the standard sharp conditioning inequality gives conditional ordered-b sample error at most

n*d(t)/(n-b).

This applies to convergence towards π and is considered when the actual sampling event has positive probability; d(t)<(n-b)/n guarantees it. The hole-DAG invariant does not by itself bound d(t), couple labels, or make fresh-source/communication coverage sufficient for mixing.

## Verification

`python3 -B verification/check_fullcapacity_fullshuffle_hole_dag.py` enumerates every labelled DAG on n=2,3,4 vertices, checks every legal identity contact (a superset of the numerical oldest-legal choices), compares the hole formula against direct full-packet identity merging, and checks the aggregate availability inequality. These finite checks supplement, rather than replace, the all-n proof above.

## Why a full-row token alone does not prove mixing

There is a short exact controller obstruction, not a counterexample to the iid protocol. On n=4,c=L=3, take

- C_0={1^1,2^0,3^0};
- C_1={0^1,3^0};
- C_2={1^1,3^0};
- C_3=empty.

The hole graph is acyclic. Initiating 0, then1, then2 gives contacts 0→1→2→0, each with a unique oldest partner. After these three events the full numerical state is exactly restored. The unique full row follows the contact responder, while owner3 remains empty and its universal zero descriptor is never contacted. Thus a controller that only follows a full-row token can cycle forever, despite the DAG invariant. The iid scheduler is not this controller: the infinite prescribed word has probability zero, and other legal initiations can break the cycle. No slow-mixing lower bound follows from the example.
