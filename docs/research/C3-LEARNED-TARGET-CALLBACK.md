# Capacity-three owner service without initially shared secondaries

Working proof independently reviewed and integrated in the manuscript, 16 November 2026. See [audit scope](C3-AUDIT.md). The intended model is exactly `c=ell=3`, with mandatory partner removal, received protection, minimum-age merging, integer ages, and full replies. This note does not assert the generic convergence theorem or a polynomial ordinary-execution bound.

## Boundary-service statement

Fix owner `a`. Let `H` be **any subset** of its current zero holders, so every `q in H` caches `a^0`. Suppose the owner caches some identity `p` outside `H union {a}`. There is a finite legal controlled path ending with an owner contact to a peer outside `H`, preserving every original `a^0` copy throughout and never decreasing the total number `N_a` of identity-`a` holders.

In particular, taking `H` to be the full current zero-holder set gives a strict zero-count increase. There is **no assumption** that members of `H` initially know `p`, or that any secondary ages agree or lie in a bounded band. No uniform numerical horizon in the initial ages is extracted here.

## Owner-only learning and fixed holder set

Initially let only `a` initiate, preferring an outside-`H` partner in every oldest tie. Stop on any such contact. Before then every responder is in `H`, returns `a^0` in its forced complete reply, and receives protected fresh `a^0`. Thus `H` remains a set of zero holders; every other original zero is untouched. The full zero-holder set is unchanged before the final boundary contact. The owner never becomes empty, because we retain its distinguished target `p` as follows.

Send `p` among the request extras. After filtering returned self-`a`, at most two reply identities are usable. Mandatory deletion leaves at least one vacancy. If the owner cache was underfull, no victim is needed. If it was full and a victim is needed, it had one other extra `r`. If `r` was received, it would be a duplicate, leaving at most one novel usable reply and hence no victim requirement. Therefore when a victim is needed, `r` is eligible and can be chosen instead of `p`. If `p` itself is received it is protected anyway. This proves legal retention of `p` at every preterminal owner exchange.

Every contacted `q in H` receives and protects `p`. Once a member of `H` learns `p`, it never loses it during this owner-only phase, since every subsequent request to it contains `p`. Let `J` be the subset that knows `p`. Then `J` grows monotonically and can grow only finitely many times.

If owner-only execution reaches the boundary, we have the required finite path. Otherwise consider any resulting infinite legal owner-only sequence. This is only a proof device, not an event claimed to have positive probability under the iid scheduler. After its last first contact with an unknown-`p` responder, every future responder has `{a^0,p}` and at most one residual entry. Its reply now has at most one usable identity besides the already resident `p`, so no active eviction occurs and the owner's cache size never increases. After finitely many further decreases, the number of owner heads outside `{p}` is a constant, either one or two; zero would make the next partner `p` and finish.

All `p` ages used in this tail are bounded by a finite constant. At the start of the tail every such age is finite; subsequently an owner/responder pair with ages `(u,v)` updates both to `min(u+1,v)`, which is no larger than `max(u,v)` for integer ages. No unseen responder appears later. No finiteness of the full aged state space is assumed.

## A local one-head completion argument

We will use the following elementary fact. Suppose a finite set `S` consists of zero holders, every member knows `p`, and every residual identity at `S` lies in `S`. The owner cache is `{p,Q}` for some `Q in S`; all other peers remain frozen. Then a finite path finishes at `p`.

Inspect the actual oldest owner head. If it is `p`, finish. Otherwise freeze the owner and prepare `Q` by the usual singleton residual clearing: while its residual partner is in `S` and has age at least the current `p` age, let only `Q` initiate, reserving `a,p`. The actual oldest rule permits these choices. First visits install fresh `Q` pointers at responders, and a repeat self-filters the returned pointer, so preparation stops within `|S|` exchanges. Old zeros and the shared `p` entries remain protected. The maximum `p` age over `S union {a}` cannot increase.

The subsequent owner contact to `Q` has no active victim and leaves at most one residual owner head. If another nonfinishing macro is required, that returned head's age `b` must satisfy `b>w`, where `w=min(u+1,v)` is the new owner secondary age. Preparation stopped at `b<v`, with `v` the prepared `Q` secondary age. These inequalities force `w=u+1`. Thus every continuing macro strictly increases the owner's secondary age, bounded above by the finite initial maximum on `S union {a}`. After finitely many macros only `p` is available or oldest, and the owner contacts it. Closedness of the residual identities ensures no unshared outside row is read. All original zeros outside `S` are simply frozen.

## Stable one-head tail

If the hypothetical owner-only tail has one head besides `p`, that head must lie in `H`, or the next exchange would finish. Requests contain only `a,p`; both are duplicates at every subsequently visited responder. Consequently residual identities and their ages at those responders do not change. The owner's unique head follows a fixed functional graph. An empty residual or a residual outside `H` finishes; otherwise the walk eventually enters a directed cycle `S` in `H`. Every member of the cycle has been visited and knows `p`; its residual points to the next cycle member. Freeze at any sufficiently late cycle head and apply the local one-head argument. This constructs a finite finishing path, contrary to needing the hypothetical continuation.

## Stable two-head tail

A residual head outside `H` cannot persist indefinitely alongside an `H` head. If never selected, it stays cached because no active eviction occurs. Every visited responder then has its residual overwritten by that retained outside head. A repeat returns it as a duplicate and removes the last `H` head; an outside contact follows. Hence a hypothetical infinite stable two-head tail has both heads in `H`.

Let `S` be the finite set of identities selected infinitely often in this tail. Eventually both owner heads lie in `S`. Otherwise, after the last selection of a vertex outside `S`, a newly present outside-`S` head could never be selected and would remain cached. Repeating any of the finitely many other responders would return that retained head and coalesce the two owner heads, contradicting the stable two-head assumption. After each member of `S` is visited once more, all its residual pointers also lie in `S`: a responder's new pointer is precisely the other owner head. Every member knows `p`.

For a two-head update write the old heads as `q:A,s:B`, with selected oldest `A>=B`, and the responder's old residual as `r:C`. The stable case has `r in S` distinct from `s`; an empty/outside/duplicate residual would already change phase. The update is exactly

```
owner heads:     s:(B+1), r:C
q residual:     s:(B+1).
```

In the multiset consisting of both owner-head ages and all residual-pointer ages at `S`, this removes `A,B`, inserts `B+1` twice, and merely moves `C`. Its minimum cannot decrease, and no new copy at the current minimum is created. Every passive copy at that minimum eventually moves to an owner head, since its vertex is selected infinitely often. Every owner-head copy at that minimum disappears on the following update. There are finitely many copies. Thus every current minimum vanishes after finite time, and integer-valuedness implies that the restricted minimum tends to infinity.

Let `M` bound all `p` ages over `S union {a}` in this tail. At some finite time every residual pointer in `S` has age at least `M`. Freeze the owner before its next actual oldest head `Q in S` and perform `Q`-only singleton residual clearing inside `S`. On a first visit, the returned residual keeps its old age at least `M`; on a repeat, the fresh pointer to `Q` is self-filtered and the residual empties. Hence every nonempty residual selected during preparation is an actual oldest choice, since all secondary ages stay at most `M`. The primary zero remains protected. This clears `Q` in finitely many exchanges.

The owner's inspected head is unchanged while frozen. Its contact to the now-residual-empty `Q` returns only `a,p`, deleting one owner head without replacement. The owner now has `{p,R}` with `R in S`. The set `S` is still residually closed: preparation installed only pointers to `Q`, and the owner's exchange installs only the retained `R` at `Q`. The local one-head completion argument finishes at `p`. Other zero holders were untouched.

This exhausts the possible infinite owner-only alternatives. Each supplies a finite prefix and a finite finishing intervention, establishing the finite legal path claimed in the statement. Every prescribed finite choice has positive probability under the unchanged protocol; no probability is assigned to an infinite prescribed schedule.

## Nonholder strengthening and consequences

If the distinguished `p` initially lacks identity `a` altogether, repeat the zero-gain construction until some nonholder is contacted. A terminal responder that already has a positive `a` copy returns `a` in its complete reply, so the same one-victim argument permits retaining `p`; no holder was lost and the zero count strictly increases. The fixed nonholder `p` remains available as a target. Finitely many zero gains cannot continue while excluding `p`, so eventually a contact creates an additional identity-`a` holder. This restores a copy lost in a preceding holder-to-owner exchange.

Consequently the existing holder-only length-three first-contact theorem combines with this callback to give capacity-three zeroification: a boundary contact with a zero holder refreshes a positive active copy; a contact with owner `a` loses one positive copy but gives the owner a nonholder target, and the strengthened callback restores the holder count while gaining a zero.

The boundary-service formulation also permits owner-directed routing through zero holders: for a chosen directed path, put only the off-path zero holders in `H`, retain the first path head as `p`, and stop at the first path vertex contacted or a peer outside the zero-holder set. At a path vertex its full reply supplies the untouched next head, shortening the path. This is why `H` was allowed to be a subset rather than silently applying an all-zero-holder lemma to a target already in that set.

These results do **not** settle sparse capacity-three convergence. The dense proof separately used no-active-eviction to rule out an outward edge from a zero holder to a nonholder. In the sparse model a boundary exchange can transfer the sole identity-`a` copy from the active holder to the responder instead of increasing its count. A general outward-gain or replacement extremal argument remains necessary.

## Subsequent scope update

The later [general length-three proof](LENGTH-THREE-GENERAL-CONVERGENCE.md) extends the convergence conclusion to every allowed capacity at `ell=3`. This note retains the earlier capacity-three argument and its original audit scope; references here to sparse length-three convergence remaining open describe that earlier stage. Higher shuffle lengths and polynomial mixing remain open.
