# Weak connectivity for shuffle length two at every capacity c>=2

Exact convention: mandatory removal of partner, uniform reply subset size
min(2, responder cache size), outgoing fresh initiator plus at most one other
resident, duplicate discard, vacancies first, then replacement among ORIGINAL
sent residents. Newly inserted entries are not eligible victims.

**Lemma.** Every exchange preserves every weak component for ell=2 and c>=2.

Let p contact q. If p has no other entry, it sends only fresh p; otherwise let r
be its one other sent resident. Let R be the reply subset, with |R|<=2. The only
old p edges eligible for removal are p->q and possibly p->r; every removed q
resident belongs to R. We show every old edge is replaced by a path among the
same component's vertices.

First p and q remain connected. If q finally knows p, use the direct q->p edge.
Otherwise q must have initially known p and evicted that resident. Its fresh
incoming p was therefore discarded as duplicate. The only possible usable
incoming descriptor was r; hence r exists, was new at q, and is finally stored
there. The eviction also requires p in R. Because the reply contains p, the
initiator receives at most one usable new identity. Its mandatory removal has
created at least one vacancy, so no other p resident is evicted. In particular
p retains r. Thus p->r<-q connects the endpoints.

If p->r is removed, at least two usable new replies were inserted, since there
was a mandatory vacancy and only one other eligible p resident. Therefore |R|=2
and neither p nor r is in R (indeed both replies were previously unknown at p).
If q already knew r, it cannot evict r because r is outside its eligible reply
set R. If it did not know r, it inserts r and that newly inserted entry is not an
eligible victim. Thus q retains r and p's lost edge to r is transferred to q.

Consider any removed q->v edge. Then v belongs to R. If v=p the endpoint path
above suffices. Otherwise p either accepts v as a new identity, or already knows
v. A newly accepted v is retained because new entries are not eligible victims.
A previously known v is retained unless v=r, the only other eligible p slot.
But if v=r belongs to R, that duplicate reply leaves at most one usable new
reply, which fits the mandatory vacancy; p cannot then evict r. Therefore p
retains v, transferring q's lost edge to p.

All unchanged edges persist. Since p and q remain connected and every other lost
edge is retained at the other endpoint, every path in the original weak graph
has a replacement path in the new graph. Exchanges never introduce identities
from another weak component, so components are preserved exactly.

The proof allows arbitrary initial ages and every legal choice of oldest
partner, outgoing extra, reply subset, and eligible victims. In particular it
applies to the capacity-two/full-shuffle case. At ell>=3 the two-event
partition certificate shows this statement fails under the same literal
replacement completion.
