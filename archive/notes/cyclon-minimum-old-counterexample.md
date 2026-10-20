# A reachable positive-drift minimum-old-age counterexample

The count of old descriptors at the globally minimum old age is not a
supermartingale for c=ell=2, even with strict old/young age separation and
even when the colored state is reached from an all-old marking.

Take n>=10 and distinct nodes q,r,s,h,x; the other L=n-5 nodes are ordinary
leaves. Fix m>=2 and K>m. Initially mark EVERY descriptor old and set

    C_q = empty,
    C_h = {r^m,s^m},
    C_x = {q^K,h^(m-1)},
    C_p = {q^0} for p in {r,s} and all ordinary leaves.

This overlay is weakly connected. For every such p, execute p->q then q->p.
Both are singleton exchanges. They leave C_p={q^0_young} and restore empty
C_q. All other caches are unchanged. Next execute x->q, then q->h. The
oldest choices are uniquely forced: first K>m-1 at x, then m>0 at q.
The endpoint is

    C_q = {r^m_old,s^m_old},
    C_h = {q^0_young,x^1_young},
    C_x = {h^m_old},
    C_p = {q^0_young} for p in {r,s} and the L ordinary leaves.

No old descriptor has age below m; every young descriptor has age <=1<m.
There are exactly M_m=3 old descriptors at age m.

Under one ordinary uniformly selected initiator:

* Each ordinary leaf copies both old m entries from q into its empty-after-
  partner-removal cache, while q evicts only one old entry to admit the
  leaf's fresh identity. Thus Delta M_m=+1, regardless of the victim choice.
* If q initiates, its two old m entries increment, and neither responder r
  nor s returns another old m. Thus Delta M_m=-2, for either oldest tie.
* If x initiates toward h, it deletes its old h^m and receives only young
  entries. Thus Delta M_m=-1.
* If h initiates, its uniquely oldest descriptor is young x^1. Its fresh h
  descriptor converts x's resident old h^m to young by duplicate OR marking.
  Thus Delta M_m=-1.
* If r or s initiates, its own old descriptor in q is filtered at the active
  cache and refreshed to young at q; the other old entry is copied, giving
  Delta M_m=0.

Therefore

    E[Delta M_m] = (L-2-1-1)/n = (n-9)/n > 0.

This is a valid numerical-age execution of protected+MIN CYCLON, not merely
an arbitrary auxiliary coloring. Every preparatory exchange has positive
probability and every old/young merge uses OR marking. All preparation
choices are deterministic at c=ell=2 for these states. The attached exact
rational checker verifies n=10,...,40 and m=2 or m=1,000,000, enumerating all
oldest ties and passive victims in the final random activation.

The simpler state with only q holding two minimum-old descriptors and many
singleton-young leaves already gives positive drift (n-5)/n; the construction
above removes any concern that such young self descriptors may be
unreachable from an all-old marking.
