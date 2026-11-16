# Capacity-three outward holder gain

Working proof independently reviewed and integrated in the manuscript, 16 November 2026. See [audit scope](C3-AUDIT.md). Model: exactly `c=ell=3`, mandatory partner deletion, received protection, MIN merging, and full replies. This is a finite accessibility argument, not a polynomial time bound. Its callback input is the independently reviewed learned-target service lemma in `C3-LEARNED-TARGET-CALLBACK.md`.

## Statement

Suppose owner `a` is empty, exactly `h` peers hold `a`, all at age zero, and some holder caches a nonholder. A finite legal path attains `N_a>h`.

We first establish two terminal gadgets valid in the more general invariant: a distinguished current holder `p` caches at least one nonholder; its `a` age can be arbitrary; every other holder has `a^0`; and the owner is empty. Until a terminal gadget begins, only nonholder migrations will occur.

## Terminal gadget 1: contact with the empty owner

Suppose the actual oldest partner of `p` is `a`. Write its other entries as `r:R` and, if present, `s:S`. At least one residual is a nonholder. Execute `p -> a`. The current holder loses `a`, but retains all residuals with their ages incremented; the previously empty owner receives fresh `p^0` and those incremented residuals.

Choose a maximum-age residual `s` (using `r` instead if there is only one). This identity is an actual oldest partner both at the owner and at frozen `p`.

If `s` is a nonholder, execute `a -> s`, then `p -> s`. In the first exchange `s` receives protected fresh `a^0`, `p^1`, and, when present, the other residual sent with its twice-incremented age (possibly MIN-refreshed at the responder). In the second exchange the request consists of fresh `p^0` and that same twice-incremented other residual. Every requested identity is already at `s`, so `s` retains its new `a` copy. Its full reply gives `a` to `p`. Thus two holders are created after losing only one: strict gain.

Otherwise `s` is a zero holder and the other residual `r` is a nonholder. Execute `a -> s`, retaining `r` at the owner. This retention is legal because the reply contains self-`a`, so at most two usable reply identities remain; if a victim is necessary, `p` rather than `r` can be chosen. The responder becomes exactly

```
C_s = {a^0, p^e, r^d},  0 <= e <= 1,  0 <= d <= R+2.
```

The frozen cache of `p` still has `s^(S+1), r^(R+1)`, with `S>=R`, so `p -> s` remains an oldest-legal choice. Its request `{p^0,r^(R+2)}` consists entirely of identities already at `s`. Hence `s` retains `a^0`, and `p` regains `a^0` from the full reply. All original holders are restored. The owner still caches the untouched nonholder `r`. The learned-target lemma's nonholder strengthening now creates an additional holder without losing an old one. Again `N_a>h`.

This argument does not assume that the current `a` age is zero or that both outside targets can be retained simultaneously.

## Terminal gadget 2: contact with another zero holder

Suppose current `p` selects another holder `q`. Since `p` also caches a nonholder, its cache must be full:

```
C_p = {a^A, q^Q, r^R},  r a nonholder.
```

Execute `p -> q`. The active reply contains `a^0`, so `p` retains and refreshes its target copy. The forced full request makes the responder exactly

```
C_q = {a^0, p^0, r^d},  0 <= d <= R+1.
```

Now `q -> r` is oldest-legal, choosing `r` in a possible all-zero tie. If `q` retains `a`, the nonholder `r` acquires it and we have a strict gain. Otherwise this is a migration: `q` loses `a`, and the responder becomes exactly

```
C_r = {q^0, a^1, p^e},  0 <= e <= 1.
```

All other holders, including `p`, remain zero holders. The current holder `r` caches nonholder `q`; its target `a` is an oldest tie. The owner is still empty. Invoke terminal gadget 1 with current `r`. This produces strict gain. Thus any zero-holder contact can be terminated successfully, irrespective of the old numerical ages.

## Exact nonholder migration

Consider an oldest contact from current `p` to nonholder `q`. If the active copy of `a` survives, the protected request creates a new copy at `q`, giving strict gain.

A loss of the active copy is possible only when `q` is full and does not cache `p`. Indeed, otherwise its self-filtered reply has at most two identities. If both are novel, the active second extra can be evicted instead of `a`; if that extra is received, only one novel identity remains. For an underfull current with cache `{a,q}`, two reply identities fit alongside `a` without eviction.

In a loss case the full reply consists of three identities excluding both `a` and `p`, so the active final cache has exactly the old `C_q` identity set; a retained duplicate may have a smaller MIN-merged age. Thus `p` becomes a nonholder. If the current was full with second extra `r`, the new current `q` has exactly `{p^0,a^(A+1),r^d}` with `d<=R+1` after a possible MIN merge. If the current was underfull with cache `{a,q}`, choose any one old responder entry `D` as survivor; the responder becomes `{p^0,a^(A+1),D}`. These are legal protected merges. In either case the new current has a cached nonholder predecessor `p`. All other holders remain unchanged zero holders, and the owner stays empty.

## Why the controller terminates

At every step choose an actual oldest partner of the current holder. An owner contact invokes gadget 1; another holder contact invokes gadget 2; a nonholder contact either gives a gain or performs the exact migration just described. Thus an infinite unfinished controlled trajectory would consist solely of nonholder migrations.

Let the initial current `a` age be `A` (zero for the stated theorem), and number these migrations by `t`. The current anchor then has age exactly `A+t`, because each migration increments and transfers it without a duplicate refresh.

For each identity `s != a`, let `M_s(t)` be its maximum stored age anywhere, or zero if absent, and define `K_s(t)=M_s(t)-t`. Every event increments only active residents by one; copies, MIN merges, and fresh selves never exceed their input age bounds. Hence every `K_s` is nonincreasing. When `s` is selected as partner, its active descriptor is mandatorily removed and is not sent; the responder cannot return itself. Every other stored `s` descriptor has unchanged or reduced age. Therefore

```
K_s(t+1) <= K_s(t)-1  whenever s is selected.
```

Oldest legality also requires the selected descriptor's pre-increment age to be at least `A+t`, so a selected `s` must satisfy `K_s(t)>=A`. Each identity can consequently be selected at most `(M_s(0)-A+1)_+` times. There are finitely many identities. This contradicts an infinite unfinished migration trajectory.

The controller therefore reaches a finite terminal gadget or direct gain. Each prescribed finite sequence of scheduler, tie, and victim choices has positive probability. No probability is assigned to an infinite schedule. The numerical length may depend on the initial ages, and no polynomial random-time estimate follows.

## Remaining integration obligations

This note alone does not assert the complete arbitrary-size convergence theorem. Its learned-target input, zeroification, existence of an empty-owner extremal state, and the incoming-boundary minimum-component argument must be linked and audited separately. Exact finite regression tests corroborate local merges but are not the proof of the unbounded-age argument.
