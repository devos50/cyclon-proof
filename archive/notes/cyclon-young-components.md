# Young-component partition: exact monotonicity and ordinary-process bound

Mark all descriptors old at an observation time. Fresh self descriptors are
young thereafter; a duplicate merge is young if either input is young.
This proof-only OR marking does not require old ages to exceed young ages.
Let Y be the undirected graph containing an edge {u,v} whenever at least one
stored descriptor between u and v is young.

For every adopted CYCLON exchange p->q, the component partition of Y is
updated by merging exactly the pre-exchange components containing p and q.
No previous young component splits. The argument holds at every capacity
and shuffle length under received-entry protection and sent-only victims:

* Fresh p0 at q inserts the young undirected edge p-q.
* A removed selected young p->q is replaced by that edge in reverse.
* A young active extra p->r that is evicted is received and protected at q;
  its previous young edge reroutes through p-q-r.
* A young passive victim q->r is copied and protected at p, rerouting via
  q-p-r. If r=p and the copy is self-filtered, fresh p at q preserves the
  original undirected edge directly.
* All other young descriptors survive; duplicate OR marking preserves
  young edges at their retained/received locations.

Conversely every young extra derives from an old young edge incident to p,
and every young reply derives from an old young edge incident to q. Thus
no new young edge leaves the union of their previous components. The only
partition change is their merger. Starting with all descriptors old, this
is exactly the connected-component partition of the cumulative interaction
graph since the observation time.

For c=ell=2 on a connected overlay, if this partition is disconnected,
connectivity supplies a cache descriptor p->r crossing two young components.
Force p as the next initiator, probability 1/n. If its actual oldest partner
is in another component, the first exchange already merges components.
Otherwise its oldest partner q is in p's component and its only extra is r.
The request forces C_q={p0,r^A}, with A>=0 after MIN merging. The r copy
cannot be young: r lies outside q's young component. Choose q as the next
initiator, probability 1/n, and r as oldest/tied partner, probability at
least 1/2. This merges two components by the second event. The first
oldest tie need not be charged separately: either outcome crosses directly
or supplies the same conditional second-event success probability.

Therefore at every two-event block start with disconnected young graph,
the probability of reducing the number of young components is at least

    p_n = 1/(2n^2).

Other random exchanges cannot reverse this progress. The connectivity time
is stochastically bounded by twice a negative-binomial waiting time for at
most n-1 successes with probability p_n. In particular

    E tau <= 4 n^2 (n-1).

Using a binomial lower-tail bound, for delta in (0,1), it suffices to take

    m >= [2(n-1)+8 log(1/delta)]/p_n

two-event blocks, giving a tail of at most delta. Thus the high-probability
bound is O(n^3+n^2 log(1/delta)) global activation events.

This is a genuine ordinary-process polynomial bound, not a probability
assigned to one long prescribed execution. It does NOT establish memory
erasure, old-descriptor extinction, coupling, or sampling uniformity: a
connected interaction history can coexist with old identity bias. It is a
potential ingredient in a stronger mixing argument.

Local exhaustive color checks over all 486 identity/color/victim outcomes
at c=ell=2 show that total young descriptor count itself is not monotone:
the singleton reciprocal young pair p->q, q->p loses one young copy when p
initiates. Selected-old exchanges do satisfy DeltaYoung>=0 and DeltaOld<=0
for every outcome. Even the count of entirely old caches is not monotone
under ordinary scheduling: P={qYoung}, Q={pYoung,rOld} becomes
P'={rOld}, Q'={pYoung,rOld}, creating another entirely old cache.
