# Uniform owner-terminal restoration for arbitrary shuffle length

Research lemma, 16 November 2026, independently audited. Valid for every L>=3, c>=L, under the exact fixed-buffer protected/MIN mandatory-removal model. The three-event restoration is unconditional; final holder gain when the chosen residual is already a holder depends on generic owner nonholder service, which is not proved for arbitrary L.

## Statement

Let C_a be empty. Suppose p holds a as an actual oldest entry and caches a nonholder distinct from a. There is a legal three-event path

 p -> a, a -> s, p -> s

that restores every original a holder and leaves s with a^0. If an oldest non-a residual s is a nonholder, this is a strict holder gain. Otherwise the path leaves a cached untouched nonholder at owner a, so any valid owner nonholder-service lemma completes a strict gain. Other original target copies may have arbitrary ages.

## Exact packet construction

Let d=|C_p|>=2 and choose s as an oldest non-a entry, preferring nonholders in a tie. In p->a, choose its e=min(L-1,d-1) extras to include s. If s is a holder, also include a designated nonholder r; this is feasible because L>=3 and the distinct entries a,s,r imply d>=3. Fill any remaining required slots arbitrarily. Let E be the companions besides s, so |E|=e-1<=L-2.

The empty reply deletes a at p. Owner a receives exactly fresh p and the sent s,E, with resident numerical ages incremented once. Since s was oldest among all non-a residents, it is oldest both at the new owner cache and at frozen p.

Execute a->s. Its cache has 1+e<=L entries, so the exact request is {a,p} union E, of size 1+e<=L. These identities are valid and protected at s. If s was an old holder, require a in its reply and retain r at the owner by the established general designated-owner-target retention lemma. The assumption of that lemma holds because r is sent as an extra and self-a is returned. No density assumption is used.

Execute frozen p->s. Its required number of extras is f=min(L-1,d-2). Include all E. The difference f-|E| is zero when d<=L and one when d>=L+1. Thus the request is fresh p, all E, and at most one additional resident u. Whenever u exists, necessarily c>=d>=L+1, and |E|=L-2.

The responder already contains p and every E identity, so only u can be novel. Require a,p in the reply. If s is full and u is novel, choose x outside the installed set {a,p} union E and also include x in the reply. This is possible: the installed set then has exactly L entries while c>=L+1. Since u is novel, x differs from u. It is not in the incoming request and is an eligible sent-resident victim. Evict x, not a. Fill any other required reply slots legally. If no overflow occurs no victim is needed. Therefore a^0 survives at s.

The reply supplies received/protected a^0 to p. Unlike the length-three special case, other active extra evictions may occur, but they cannot remove the received target and do not affect target-holder preservation. No other target holder was activated or lost its a copy.

If s was initially a nonholder, restoring p while retaining the new copy at s increases N_a. If s was a holder, all original holders are restored and owner a still caches r, whose row was untouched. A generic owner nonholder-service result would then create an additional holder. This dependency is essential and is not assumed established above length three.

## Boundary cases

- When d=2, E is empty and the three request sizes are 2,2,1; no novel third-request resident exists.
- At full shuffle c=L, u cannot exist, so the third request consists entirely of identities already installed at s and causes no passive eviction.
- The safe-x branch is used only at proper capacity c>=L+1, with L>=3 ensuring the required reply entries a,p,x fit.
- MIN may lower ages of duplicates, but cannot affect legality of the frozen p choice or the two required protected target copies.
