# outward holder gain for length three, capacity at least four

Independently reviewed working proof, integrated on 16 November 2026. Exactly `ell=3`, `c>=4`; arbitrary population `n>=c+1`. Uses the arbitrary-capacity learned-target callback in `LENGTH-THREE-ARBITRARY-CAPACITY-CALLBACK-CANDIDATE.md`. Neither note is a polynomial-time bound or a result for longer shuffle lengths.

## Claim and invariant

Here a nonholder always means a peer different from owner `a` that lacks identity `a`. The owner is excluded.

Suppose owner `a` is empty, exactly `h` peers hold `a`, all at age zero, and some holder caches a nonholder. A finite legal path reaches `N_a>h`.

Choose a current holder `p` with a cached nonholder target `r`. Let `Z` be all initial holders except `p`. Until a terminal gadget, only the current holder initiates. At every unfinished endpoint the holder set is exactly `Z union {current}`; members of `Z` remain passive and keep their zero copies. The current caches a designated nonholder target. A migration replaces the current and designates its old initiator as the new nonholder target.

Define the **fixed identity set** `Y=V\(Z union {a})`. Because `Z` remains exactly the passive zero holders, `Y` always consists of the current holder and all nonholders. In particular, the current initiator and its designated nonholder target belong to `Y`, whereas every selected zero holder and anchor `a` do not.

Let `F=sum_v |C_v intersect Y|` count cache entries whose identities lie in this fixed set, and let `d` be current cache size. We construct a bounded lexicographically nondecreasing potential

```
(F, c-d),  with 0<=F<=nc and 0<=c-d<=c.
```

Every zero-holder contact strictly increases it. Nonholder migrations weakly increase it. Owner contacts and direct gains terminate. No auxiliary descriptor coloring or provenance mark is required; MIN affects ages, not membership in `Y`.

## Owner-contact terminal gadget

Suppose current `p` selects the empty owner `a`. Pick an oldest residual `s` at `p`. If it is a nonholder, send `s` and any other residual companion `t` (when present). If it is a holder, use the designated nonholder `r` as companion `t`. Execute `p -> a`.

The owner now has fresh `p^0`, `s` and, if present, `t` with their incremented ages. Its oldest residual `s` is also still oldest at frozen `p`, whose residual ages all increased equally. Execute `a -> s`, sending fresh `a`, `p`, and companion `t`. These three identities are protected at `s` (with possible MIN refreshes).

If `s` is an old holder, require its reply to contain `a`. The owner has at most two retained entries after deleting `s`, and at most two usable reply entries after filtering self-`a`; capacity `c>=4` therefore retains companion `t=r`. If `s` was a nonholder, we will already get the desired gain below and do not need this owner retention.

Now execute the still-legal `p -> s`. Include companion `t` among its extras, and fill the other extra slot, when required, with any other resident `u`. The request has fresh `p`, companion `t`, and at most one additional identity `u`. The first two already occur at `s`, so at most one identity is novel there. Require `a,p` in its reply. If `s` is full and `u` is novel, choose a third reply identity `x` outside `{a,p,t}` and evict `x`. Such an identity exists because `c>=4`; it cannot equal novel `u`, so it is eligible. If no eviction is needed, complete the reply arbitrarily. Thus `s` retains `a`. If no companion exists, the request contains only already-known `p`, so this argument is easier.

The active `p` has at least two vacancies, from deleting `a` in the first event and `s` now. Its reply includes self-`p`, hence at most two usable identities. It therefore receives and retains `a` without any active eviction. All initial holders are now restored. If `s` was a nonholder, we have strict gain. Otherwise the owner still caches untouched nonholder `r`; arbitrary-capacity learned-target nonholder service creates an extra holder while preserving existing ones. This terminates successfully.

## Zero-holder contacts

Let the current select `q in Z`; `q` is outside `Y`, and it returns protected `a^0`. Write `C` for the current preincrement identity set and `D` for the responder's set. The designated nonholder `r` differs from `a,q,p`.

### q knows both p and r

Send `a,r` as the extras and request reply `a,p,r`. All incoming responder identities are already known, so no responder eviction occurs. At the active endpoint `p` self-filters, while `a,r` are duplicates. Deleting the uncounted partner `q` strictly decreases current cache size. No counted entry is lost, so `F` does not decrease and the lexicographic potential strictly increases. The designated target is retained.

### q knows p but not r

Send `a,r`; reply with `a,p` and one other resident `D0` when a third reply is required. If the responder is full, choose `D0` absent from current `C`, and evict it to admit `r`. Such a resident exists: its `c-2` entries outside `{a,p}` can overlap `C` in at most `d-3<=c-3` identities, since current `C` contains `a,q,r`, and neither `q` nor absent `r` can be one of those responder entries.

Any counted victim is copied into a new active location by the reply. At most one active novel identity is returned, since `p` self-filters and `a` is a duplicate; mandatory partner deletion supplies its vacancy. The counted target `r` remains active and gains a new passive copy. Thus `F` strictly increases. An underfull responder needs no eviction and the same strict gain holds.

### q does not know p

Send `a,B`. If the current is full, choose `B!=r`, possible because `c>=4`; this keeps the designated target unsent and hence ineligible for active eviction. If the current is underfull, choose any legal second extra, including `r` if necessary; at least two vacancies after partner deletion accommodate the at most two usable novel reply entries, so the target still cannot be evicted.

If `q` already knows `B`, **include B in the reply**, together with `a` and a third identity when required. The only new passive identity is `p`, so at most one passive victim is needed. If needed choose that third reply identity outside `C`, copying any counted victim to a new active location. Such a choice exists whenever the responder is full: `|D\\C|>=|D|-d+1>=1`, since `q in C` but `q notin D`. Because `B` is returned, it is protected at the active endpoint; at most one other novel identity is returned. Fresh `p` adds a genuinely new counted passive entry, and no counted loss is uncompensated. Thus `F` strictly increases. Including `B` here is essential: otherwise losing an active counted B already present passively could cancel the strict fresh-p increase.

If `q` does not know `B`, both `p,B` are new passive identities. At most two passive victims are needed; select all necessary victims among reply residents absent from `C`. There are enough: if `e=|D|`, current `C` contains `q,B` absent from `D`, so

```
|D\\C| >= e-d+2 >= e-c+2.
```

The number of needed victims is `max(0,e+2-c)`. Include them in the reply alongside `a`, completing the at-most-three-entry reply legally. Every counted passive victim is copied to a new active location. The only possible active extra victim is `B`; if it is lost, it has just been copied into a new passive location, compensating its contribution. Fresh `p` is an additional new counted entry. Hence `F` strictly increases. This counting also covers underfull responder caches and shorter replies.

In every case the designated target remains cached and counted, and all target holders remain unchanged zero holders except that the current is refreshed to zero.

## Nonholder contacts: either gain or disjoint migration

Let the oldest selected `q` be a nonholder. Include `a` in the request, so `q` gains a protected copy. If active `a` can be retained, strict holder gain terminates.

An underfull current can always retain `a`. If its size is two, the sole retained `a` plus three reply identities fit in capacity at least four. Otherwise mandatory deletion supplies at least two vacancies; at most three novel replies can require one victim. Choose the other sent extra `B` if it is not returned. If it is returned, it is a duplicate and at most two novel identities arrive, requiring no victim.

For a full current, if `q` knows initiator `p`, include `p` in the reply, leaving at most two usable identities and allowing retention of `a` by the same one-victim argument. If `q` instead knows any current residual identity `x` other than selected `q` and anchor `a`, include `x` in the reply and choose sent extra `B!=x`; there are at least two candidate residual extras because `c>=4`. The duplicate `x` leaves at most two novel identities. If `B` is also returned there is no overflow; otherwise evict `B`, not `a`. Again there is a strict gain.

Thus an unfinished migration need only occur when the current is full, the responder lacks `p`, and its resident identities are disjoint from all current residents. If its reply has fewer than three identities, retain `a` by evicting at most `B` and finish. Otherwise all three reply identities are novel. The active merge deletes partner `q` and its two sent extras `a,B`, becoming a nonholder; all other residents are unsent and retained. The responder receives three new protected identities `p,a,B`. Choose every necessary passive victim among the three replied residents, so each counted victim is copied to a new active location.

Old current `p` is now a nonholder, and its fresh `p^0` at the responder becomes the new designated target in `Y`. The new current is the responder. Its `a` age is exactly the previous current age plus one, since the recipient was a nonholder. Other holders `Z` stay passive zeros. Identity-count bookkeeping gives

```
F_new-F_old >= 1 - indicator(selected q belongs to Y) >= 0.
```

The only other active extra victim `B` is newly copied to the responder, compensating its contribution; `a` is outside `Y`. Before the migration the current was full, so `c-d=0`. If `F` is unchanged, the new current has `c-d_new>=0`, ensuring lexicographic nondecrease even if the new responder remains underfull.

## Finite termination

The lexicographic potential ranges over a finite set. It is strictly increased by every zero-holder contact and weakly increased by every unfinished migration. An infinite unfinished trajectory would therefore eventually consist solely of nonholder migrations.

Begin that tail with current anchor age `A`. After `t` migrations its age is exactly `A+t`; there are no zero-holder refreshes in the tail. For each `s!=a`, put `K_s(t)=M_s(t)-t`, where `M_s(t)` is its maximum stored numerical age, or zero if absent. Each `K_s` is nonincreasing. When `s` is selected as partner, the active `s` entry is removed and not sent; all other `s` entries have unchanged or lower ages, so `K_s` decreases by at least one. Oldest selection requires `K_s(t)>=A` whenever `s` is chosen. Every identity can therefore be selected only finitely many times in this tail, contradicting infinitude.

The controlled path must reach direct gain or the owner-contact terminal gadget in finite time. Each finite prescribed action has positive probability. MIN ages cannot invalidate compensation in the static identity count; only the exact novel-anchor age is used in the numerical tail argument.

## Scope and audit cautions

This is a qualitative outward-gain proof conditional on the arbitrary-capacity learned-target callback. It is not itself the complete general length-three convergence assembly, and it says nothing about polynomial sampling or lengths four and above. In particular, the instruction to return already-known `B` in the unknown-initiator case is necessary for the claimed strict potential increase.

## Final integration status

This working result is now integrated in the manuscript after independent end-to-end and actual-text audits. See [the audit record](LENGTH-THREE-AUDIT.md). Earlier candidate wording in this research history is superseded by that status; no formal-verification or external-review claim is made.
