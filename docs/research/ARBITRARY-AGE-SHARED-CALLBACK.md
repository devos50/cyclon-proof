# Full-shuffle callback with arbitrary shared-secondary ages

Research continuation, 16 November 2026. The symbolic argument has passed two independent adversarial reviews. It is retained as a separate research lemma rather than a general convergence theorem. It removes age-band restrictions from a **conditional** shared-secondary callback; it does not establish that the shared-secondary identities are accessible from arbitrary states.

## Conditional statement

Use the adopted protected/MIN protocol, with full shuffle `ell=c>=3`. Fix owner `a` and let `I={q != a: a^0 in C_q}`. Suppose `P` is a set of `c-2` identities cached by `a` and by every member of `I`. There are **no restrictions on any secondary age**, including at the owner. Then some finite legal controlled path increases `Z_a` by one, preserves every old zero throughout, and never decreases `N_a`.

The no-self rule implies `P` is disjoint from `I union {a}`. No age-independent numerical horizon is asserted. The common-descriptor accessibility and higher-length endgame restrictions remain open.

## Owner-only normal form

Call entries outside `P` in the owner's cache its residual heads; there are at most two. Every `q in I` has the reserved anchors `{a} union P` and at most one residual pointer. Always prefer an outside-`I` owner partner when it is oldest or tied: such a contact ends the construction with a new zero. Until then, only the owner initiates and every responder is in `I`.

For a contact `a -> q`, the reply contains all reserved anchors and at most one residual. Mandatory deletion of `q` supplies the space for that at most one novel residual, so no other active resident is evicted. All secondary identities remain at the owner. Both endpoints' secondary coordinate ages become `min(u+1,v)`, where `u` is its old owner age and `v` its old responder age. Thus every secondary age in `{a} union I` remains at most their initial finite maximum `M`. Passive secondary vectors at individual zero holders are coordinatewise nonincreasing during owner-only execution. All old zeros and all target copies are preserved.

If the owner has no `I` head, its next contact gives the gain. If it has one `I` head plus a residual outside head `s`, either it contacts an outside head and finishes, or `s` stays cached while the other head walks through `I`. Each visited responder has its residual overwritten by `s`. A repeat therefore returns `s`, removing the last `I` head. This case is finite independently of ages.

The remaining one-head case is an underfull owner with cache exactly `P` plus one `I` head. The two-head case has both residual heads in `I`.

## One residual head, arbitrary secondary vectors

In the underfull one-head case, the owner's packet contains only fresh `a` and `P`. These are all duplicates at its responder, so no residual entry is replaced there. Consequently the residual graph on `I`, including its numerical residual ages, stays fixed during owner-only execution.

If this walk does not finish by reaching an empty/outside residual or choosing an outside oldest partner, it eventually follows a directed cycle `S` inside `I`. The passive secondary vectors on that cycle are coordinatewise nonincreasing nonnegative integers. After finitely many strict decreases they stabilize, say at vectors `v_q`. After contacting `q`, the owner's vector equals `v_q`, because the responder's vector is unchanged by that exchange. For a cycle edge `q -> r` of residual age `L_q`, continued nontermination gives

- `L_q > max(v_q)`, because otherwise a secondary outside-`I` identity is oldest or tied and would be selected;
- `min(v_q+1,v_r)=v_r` coordinatewise, because the next stable contact does not change `r`'s vector.

Now freeze the owner when its head is a cycle vertex `Q`. Let only `Q` initiate along its residual pointers. The first residual is strictly older than every secondary anchor. An internal exchange from the currently represented cycle vertex to the next one sets `Q`'s secondary vector to the next `v_r`, so the same oldest legality remains true for the next residual age `L_r`. The primary anchor stays zero. Each responder gets a fresh residual pointer to `Q`; on the cycle's return, the reply is self-filtered and `Q`'s residual cache empties. The owner has stayed frozen, so its originally inspected oldest choice `Q` is unchanged. Its next contact to `Q` removes the sole residual head and returns no replacement. It can then contact an outside secondary and gain a zero.

## Two residual heads: divergence, not guaranteed coalescence

As long as owner-only execution retains two distinct `I` heads, its exact residual update is

- old owner heads `q:A`, `s:B`, with selected oldest `A>=B`;
- old responder residual `q -> r:C`, where `r` is in `I` and differs from `s`;
- new owner heads `s:(B+1)`, `r:C`;
- new responder residual `q -> s:(B+1)`.

An empty/outside residual or `r=s` instead reduces the problem to an already handled case. Do **not** assume the two-head process itself always coalesces: an independently found oldest-legal five-vertex pointer cycle can repeat with increasing ages.

Suppose the owner-only two-head process continues forever. Let `S` be the set of identities selected infinitely often. Eventually both root heads belong to `S`. Indeed, after a putative final selection of some other identity, a root head outside `S` would stay fixed forever. The other head would follow a finite pointer walk, overwriting every visited pointer to that fixed head. Revisiting a vertex would then force coalescence, a contradiction. After every member of `S` has been selected once more, all residual pointers at `S` also point inside `S`.

Restrict attention to the ages of the two owner heads and all residual pointers at `S`. Each update removes root ages `A,B` from this multiset and inserts `B+1` twice; `C` merely moves from a responder pointer to an owner head. The minimum is nondecreasing, and no new copy of its current value can be created. Every copy of the minimum in a passive pointer eventually moves to the root, because its source vertex is selected infinitely often, and every root minimum disappears on the next update. Hence all copies of each minimum disappear after finite time. Integer-valuedness implies this restricted minimum tends to infinity. This divergence argument does not require the oldest inequality, although the original owner trajectory obeys it.

At a finite time all pointers at `S` have age at least `M`. Freeze the owner immediately before its next inspected oldest head `Q in S`. Perform `Q`-only residual clearing inside `S`. Every unvisited pointer has its original age at least `M`, while every secondary coordinate remains at most `M`, so the selected residual is an actual oldest partner. Each visited responder points freshly to `Q`; on the first repeat, its reply is self-filtered and the active residual empties. Thus clearing is finite. All original zeros remain protected. The owner's next, still-legal contact to `Q` returns only the anchors and removes one of its two `I` heads. The one-head argument then finishes.

## Scope of the proposed result

The reasoning is an existence argument for a finite legal path, not an expected random completion time. Its infinite-trajectory alternatives are only a proof device: each leads to a finite prefix followed by a finite clearing intervention. Shared-secondary identities remain a substantive assumption. The stronger claim that oldest-first two-head pointers always coalesce is false and is neither needed nor asserted here.
