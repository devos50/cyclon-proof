# Closed-class occupancy and clipped-capacity inheritance

Structural reduction, 16 November 2026. This gives an occupancy obstruction for closed classes. It does not prove that the classes are unique, invariant under relabellings, or accessible from one another.

## Exact inheritance lemma

Fix allowed parameters `(n,c,L)` for the adopted protected/MIN kernel. Let `C` be a closed communicating class, and let `m` be the maximum cache size attained anywhere in `C`. This maximum exists because cache sizes have finitely many possible values. Weak connectivity gives `m>=1`.

If `m<c`, the original kernel restricted to `C` agrees exactly, including transition probabilities, with the kernel of capacity `m` and shuffle length `min(L,m)`. In particular, `C` is also a closed communicating class of that clipped kernel.

### Proof

Every row of every state in `C` has size at most `m`. For each possible packet choice, an endpoint with resident set `A` after mandatory deletion, and novel valid incoming set `N`, finishes with size

`min(c, |A|+|N|)`.

If the union size exceeded `m`, this final size would also exceed `m`, because `c>m`. Every legal choice has positive probability and closure requires the successor to lie in `C`. Therefore every possible merge union at either endpoint has size at most `m`. No eviction occurs, either at capacity `c` or at capacity `m`.

For row sizes at most `m`, the exact request and reply sizes are unchanged when `L` is replaced by `min(L,m)`. Oldest choices, uniform subsets, self filtering, mandatory deletion, and MIN duplicate ages are also unchanged. There are no nontrivial victim choices. Thus the complete transition laws agree. Closure and communication follow immediately.

## Canonical growth witness

Suppose `1<=m<c<=n-1`. Write `T` for the greatest `m` labels, and `q` for the least label in `T`. There are at least two distinct labels `p,r` below `q`, since `m<=n-2`.

At the canonical zero-age state `H(V,m)`, both `p` and `r` cache exactly `T`, and `q` caches `T \ {q}`, of size `m-1`.

Under the larger-capacity `(c,L)` kernel, prescribe two contacts:

1. `p -> q`. This is an allowed oldest tie. Every extra lies in `T \ {q}`, already resident at `q`, while fresh `p^0` is novel. Thus `q` finishes with exactly `{p} union (T \ {q})`, of size `m`, all at age zero. The choice of the legal reply does not change this fact.
2. `r -> q`. Peer `r` has not been touched and its zero-age tie still permits this contact. Fresh `r^0` is novel at `q`, while every extra is already resident there. Since `c>=m+1`, no replacement is needed and `q` finishes with size `m+1`.

This works for every allowed `L`, including `L=1`, and also when `m=1` (the first responder starts empty). Exact buffer sizes are respected. The two-event history has positive probability; no age truncation is used.

## Consequence of smaller-kernel canonical accessibility

If every weakly connected state of the clipped `(n,m,min(L,m))` kernel can reach `H(V,m)`, then no closed class of the larger `(n,c,L)` kernel can have maximum occupancy `m<c`.

Indeed, the inheritance lemma makes that class closed under the clipped kernel, so its finite canonical-access path must stay in the class. The two-event larger-capacity growth witness then leaves the class's purported occupancy bound, a contradiction.

This hypothesis is canonical accessibility, not merely symmetry or finiteness of the set of regimes.

## Scope in the shuffle-length induction

Assume canonical accessibility is established for every smaller shuffle length and every allowed population/capacity. Then any closed class at shuffle length `L` must attain a cache of size at least `L`: otherwise `m<L<=c` and the clipped shuffle length is `m<L`, so the previous consequence applies.

In particular, for `c=L`, each class has a state with a full cache. This is an occupancy statement at some peer, not a common-atom theorem and not by itself a fixed-observer sampling theorem. Under the separate even-class-invariance hypothesis, relabelling and phase propagation can transfer availability to each observer and phase.

With only the presently established lengths one through three, the unconditional consequence is that every closed class at any `L>=4` has maximum occupancy at least four. The stronger bound `m>=L` for arbitrary `L` remains conditional on the smaller-length induction hypotheses. No claim of full-cache accessibility at all capacities is made.

## Exact finite checks

`verify_clipped_capacity_growth.py` checks the canonical two-event witness for 2,002 parameter choices with `3<=n<=13`, `1<=m<c<=n-1`, and every `1<=L<=c`. It uses the existing exact protocol implementation. These tests corroborate the explicit witness; the class-inheritance result is the symbolic argument above.
