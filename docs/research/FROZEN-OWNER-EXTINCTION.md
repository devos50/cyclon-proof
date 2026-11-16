# Owner-frozen reference extinction: route and obstruction

Research note, 16 November 2026. This records an open route and a proved obstruction, not a new mixing theorem. The adopted model is in [MODEL.md](../MODEL.md).

## Why consider freezing owners?

A possible route to the transposition coupling is to extinguish references to two target identities and then make their external caches equal. Freezing the two owners for `O(n log n)` ordinary activations has inverse-polynomial probability. This alone does not imply that reference extinction or cache matching occurs within such a window. First contact and extinction are distinct tasks.

The existing readiness charging argument also applies when the target owner's activations are replaced by no-ops: before contact, all relevant readiness changes occur at other clocks. Thus the first incoming exchange remains fast. This observation does not control all remaining references after that contact, because other exchanges can copy the target.

## Exact single-label positive-drift obstruction

For `n>=4`, use distinct peers `a,h,s`, an arbitrary integer `A>0`, and the connected initial overlay

- `C_a = empty`;
- `C_h = {a^A, s^0}`;
- `C_p = {h^0}` for every other peer `p`, including `s`.

The target-copy count `N_a` equals one. Its only copy is uniquely oldest in its cache and strictly older than every other descriptor in the network. Even if the owner `a` is frozen, the next ordinary global event has:

- Initiator `a`: no-op, since its cache is empty.
- Initiator `h`: contacts `a`, deletes the sole `a` copy, and receives an empty reply. Hence `Delta N_a=-1`.
- Initiator `s`: contacts `h`; the reply contains `a,s`, and self-filtering leaves `a` at `s`. At `h`, the fresh received `s` is a protected duplicate, so `h` retains `a`. Hence `Delta N_a=+1`.
- Any of the `n-3` remaining leaves `p`: contacts `h` and receives both `a,s`. The hub needs one victim to insert fresh `p`, chosen uniformly from its two old entries. If `s` is evicted, the target copy is duplicated; if `a` is evicted, it is transferred. Conditional expected change is `1/2`.

Therefore

`E[Delta N_a] = (-1 + 1 + (n-3)/2)/n = (n-3)/(2n) > 0`.

This is a symbolic all-`n` argument under the exact protected/MIN, mandatory-removal, length-two kernel. Since the owner's cache starts empty, freezing its clock makes no difference to this one-step calculation. In particular the same positive drift also occurs under the unmodified adopted scheduler.

The [exact checker](../../verification/mandatory-removal/verify_c2_frozen_owner_obstruction.py) enumerates every next-event branch for `3<=n<=40` and `A` in `{1,2,10^6}`. It verifies the complete increment law:

- `Pr(Delta N_a=-1)=1/n`;
- `Pr(Delta N_a=0)=(n-1)/(2n)`;
- `Pr(Delta N_a=+1)=(n-1)/(2n)`.

These finite cases corroborate the symbolic calculation. The checker does not establish a lower bound on extinction time.

## Remaining obligation

A valid extinction argument must account for copying and graph structure, or work over multiple events. The count `N_a` alone is not a supermartingale, even with an inactive owner and strict oldest priority. This counterexample does **not** show exponential extinction time, rule out an amortized potential, or refute a polynomial symmetry-set hitting bound.

## The drift obstruction persists at linear target prevalence

Take `H` disjoint hub/special-leaf pairs and `L` ordinary leaves, with `n=1+2H+L`. The owner is empty. For each hub `h`, set `C_h={a^A,s_h^0}` and `C_s_h={h^0}`. Each ordinary leaf stores one chosen hub. Then `N_a=H`, every target copy is strictly oldest and globally maximal, and the same calculation gives

`E[Delta N_a]=(-H+H+L/2)/n=L/(2n)`.

For `L=H`, target prevalence is linear in `n` while the positive drift stays bounded away from zero. Thus positive drift is not confined to a rare-label regime. The checker covers 320 further exact cases with `1<=H<=10`, `0<=L<=15`, and two positive target ages. Under a scheduler choosing uniformly only among the `n-1` nonowners, the expectation is instead `L/(2(n-1))`.

## Age-only reweighting cannot repair this one-step potential

Every target copy that survives or is created in the multi-hub calculation still has numerical age `A`: active hubs remove their incremented target, while responding hubs send the unincremented age `A`. Therefore for **any** positive function `w` of numerical age, the separable potential

`V = sum_{v: a in C_v} w(age_v(a))`

has expected one-step drift `w(A) L/(2n)>0` when `L>0`. No positive age-only weighting of target copies is a uniform supermartingale for the owner-frozen process. The checker also verifies the surviving target ages. This does not exclude potentials involving other descriptors, occupancy/graph structure, signed terms, or multistep drift.

## Freezing two owners can block symmetry accessibility completely

The single-frozen-owner first-contact observation cannot be applied blindly when *two* owners are frozen. On four peers, take

- `C_a={b^0,r^0}` and `C_b={a^0,s^0}`;
- `C_r={s^0}` and `C_s={r^0}`.

This overlay is weakly connected, but neither outside cache references `a` or `b`. If both owner activations are replaced by no-ops, every actual exchange stays within `{r,s}`. Inductively, outside caches never acquire `a` or `b`, and the two target caches never change. Their external targets differ (`r` versus `s`), so the state never enters the transposition symmetry set `F_(ab)`. The checker corroborates four event steps; the invariant proves the all-time statement.

This does not refute a polynomial symmetry-set bound under the original scheduler. It says that a proof using a frozen pair needs an accessibility/preparation step or a different adaptive coupling; simply conditioning on no target initiations is insufficient uniformly over initial states.
