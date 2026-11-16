# General full-shuffle capacity-three convergence theorem

Working proof integrated as `thm:c3generaluniform` after separate end-to-end and final-text audits, 16 November 2026. See [audit scope](C3-AUDIT.md). This note concerns **exactly `c=ell=3`**, for arbitrary `n>=4`. It does not settle sparse capacity `c>=4` at length three, higher shuffle lengths, or a polynomial mixing bound. Numerical tests corroborate local identities but do not establish this theorem.

## Theorem scope

Under the adopted protected/MIN protocol, with iid uniform initiators, oldest-partner tie choices, mandatory partner deletion, and full three-entry shuffles, the countable chain on weakly connected caches with arbitrary finite nonnegative integer ages has a unique stationary probability law. There are constants `T(n)<infinity` and `gamma(n)>0` such that a prescribed canonical labelled atom `H(V,3)` satisfies

```
inf_x P^T(x,{H(V,3)}) >= gamma,
sup_x ||P^t(x,.)-pi||_TV <= (1-gamma)^floor(t/T).
```

At stationarity each observer is available for every request size `1<=b<=3` with positive probability; its ordered local sample is uniform among ordered distinct nonself labels conditional on availability. The same conditional law is the limit from every allowed initial state. No usable or polynomial bound on `T` or `gamma^-1` is asserted.

## Inputs and dependency boundaries

Existing manuscript results:

1. `thm:thesisgeneralreset`: a finite family of bounded-age connected states is hit with a uniform finite-block probability, for every fixed shuffle length. This is independent of the proposed generic length-three conclusion.
2. `thm:thesisgeneraltwo`: full convergence/common-atom accessibility at shuffle length two for every allowed capacity. On residual components below, only capacity two and the established singleton-capacity base case are needed.
3. `lem:anchorreduction`: a reserved common zero anchor simulates the lower-length residual kernel, with empty residual initiator events omitted.
4. `thm:threefirstcontact`: holder-only finite first contact with a frozen cut, derived using the lower-length theorem, not a generic length-three convergence assumption.
5. `prop:threezeroanchor`: a universal zero anchor yields a finite path to any prescribed labelled canonical atom, and the established finite-reset/common-atom argument gives uniform convergence once all closed classes reach such an anchor.

New independently reviewed proof inputs:

6. `C3-LEARNED-TARGET-CALLBACK.md`: owner boundary service through any specified subset of zero holders; no initially shared secondary identity or bounded age band is needed. In particular, a cached nonholder gives a finite path to strict holder gain while preserving existing holders.
7. `C3-OUTWARD-HOLDER-GAIN.md`: with empty owner, all target holders zero, and a holder-to-nonholder edge, a finite path strictly increases the holder count. Its proof uses terminal gadgets and a global maximum-age potential, not a convergence assumption.

All statements below use actual full-shuffle transitions, never occasional shorter shuffles in the original chain. Smaller shuffle lengths occur only in the proved reserved-anchor simulation.

## 1. Zeroification and a classwise holder-count bound

Fix an identity `a`. Starting with any positive-age copy, freeze the owner and current zero holders until the first boundary contact supplied by the holder-only first-contact theorem. Such a boundary is initially reachable because an outside positive holder already caches `a`, which lies in the frozen cut. During the controlled preboundary path the target holder count does not decrease and old zeros remain frozen.

If the terminal responder is a zero holder, its full reply refreshes the active target copy to zero, while its own protected zero survives. If the terminal responder is owner `a`, the active holder can lose its copy; the fresh initiator entry is then a cached nonholder at the owner. Apply learned-target nonholder service. This restores at least the lost holder and creates a new zero while preserving all original zeros. In either case the endpoint has strictly more zeros and no smaller holder count than before the step.

Repeat while a positive holder remains. The bounded integer zero count strictly increases at each step, so a finite endpoint has all target copies zero and at least the original number of holders.

Now fix any closed class and let `k` be its largest attained zero count for `a`; this maximum exists because the count is in `{0,...,n-1}`. Zeroification implies `N_a<=k` at every class state. At a state with `Z_a=k`, all holders are zero, since any positive holder would give a zeroified endpoint with more than `k` zeros. Write their set as `I`. Also `k>=1`: if there are no copies, weak connectivity forces the owner's cache nonempty, and its activation creates a fresh zero.

## 2. Owner-directed service and an empty-owner maximizing state

At a zero-maximizing state there can be no directed cache path from owner `a` to a nonholder. To prove this, take a simple path whose internal vertices lie in `I`. Let the owner retain its first head `p`, and apply boundary service with `H` consisting of all zero holders except the remaining path vertices. Preterminal contacts are restricted to `H`, so the remaining path rows are untouched. The first contact outside `H` either reaches a nonholder, contradicting `N_a<=k`, or reaches an untouched path vertex. Its full reply supplies the next path head, which is received and protected at the owner. Repeating with the shorter suffix eventually reaches a nonholder, the same contradiction. No prescribed-target service across an intervening nonholder is assumed.

Let `R` be the set directed-reachable from `a`, including `a`. Then `R\{a} subset I`, and every cache row in `R` contains identities only in `R` by the definition of reachability. Freeze all peers outside `R`. There is a universal zero anchor within `R`.

To empty the owner without assuming global outward closure, inspect an actual oldest head `Q`. Reserve `a^0` and normalize the residual weak component of `Q` in `R\{a}` to the lower-length canonical state with root `Q`. Its effective residual parameters are `min(2,m-1)` for both capacity and full shuffle, where `m` is the component size; a singleton requires no operation. For components of size at least three this is a legal length-two/capacity-two simulation; size two uses the singleton-capacity base case. The owner remains frozen, and now `C_Q={a^0}`. Execute the still-legal `a -> Q`. Its only reply is self-`a`, so the owner's head count decreases by one. At the responder fresh `a` and at most two owner extras fit in capacity three, preserving its zero.

Recompute residual components and repeat until the owner is empty. All zeros in `R` survive, outside zeros stay frozen, and no nonholder acquires `a`. Thus the same closed class has an empty-owner zero-maximizing state. This avoids the circular use of global outward closure to empty the owner.

## 3. Outward closure at every empty-owner maximizer

At any empty-owner state with `Z_a=k`, all holders are zero by step 1. If one caches a nonholder, the outward-holder-gain lemma gives `N_a>k` along a finite path in the closed class. This contradicts the classwise bound. Therefore every such state has

```
C_i subset I union {a}  for every i in I.
```

This assertion applies again after each later construction that ends with empty owner and `k` zero holders; the set of holders need not stay fixed.

## 4. Incoming boundary and minimum residual components

Among the empty-owner zero-maximizing states in the class, choose one minimizing the number `d` of residual weak components on `I` after deleting the common anchor `a`. Suppose nonholders `J=V\(I union {a})` remain.

Weak connectivity supplies an edge from `J` to `I`: there are no edges from the empty owner, no `a` descriptor in `J`, and no edge from `I` to `J` by step 3. Freeze `I` and `a`, and use the length-three first-contact theorem to stop immediately before an outside initiator `P` contacts `Q in I`. No outside peer can have acquired `a` before this first crossing.

Pause the outside. Reserve `a^0` and normalize `Q`'s residual component to its canonical state rooted at `Q`. This preserves `d`, keeps all target zeros, leaves the owner empty, and leaves the pending actual oldest choice of frozen `P` unchanged. Now `C_Q={a^0}`. Resume `P -> Q`.

If `P` has at most two cache entries, its request has at most two identities. Those fit alongside the old `a^0` at `Q`; the reply gives `a^0` to `P`. This yields `k+1` zeros, a contradiction.

Otherwise write `C_P={Q,R,S}`. Its full request consists of fresh `P` and its two other entries. The exact endpoint identity sets are

```
C_P' = {a,R,S},  with a at age zero,
C_Q' = {P,R,S},  with P at age zero.
```

Mandatory deletion at `P` provides a vacancy for the sole reply, so neither retained extra needs dense no-eviction. At `Q`, all three received identities are protected, forcing its old `a` out. The new zero-holder set is `I'=(I\{Q}) union {P}`, still of size `k`, and the owner remains empty.

If `R` or `S` were outside old `I`, new holder `P` would have an outward edge to a nonholder, contradicting step 3 at this new state. Thus both are in `I\{Q}`. If `Q`'s normalized residual component had more than one vertex, at least one remaining old holder would still cache root `Q` in the connected canonical residual graph. That is another forbidden outward edge to the now-nonholder `Q`.

Therefore the removed `Q` component was a singleton. Removing it and adding `P` attached to `R,S` in the remaining components strictly decreases the residual component count, contradicting minimality of `d`. Hence `J` was empty.

This argument has no `n=5` restriction: that restriction in the earlier dense theorem was only how its cases were divided. The transition and component argument apply to every `n>=4` at capacity three.

## 5. Canonical atom and the probabilistic conclusion

Every closed communicating class therefore contains a state with universal zero anchor `a`. The existing universal-zero-anchor proposition gives a finite path from such a class to any fixed labelled `H(V,3)`.

For completeness, the finite-reset bridge also proves that the required closed communicating classes exist and are reachable. Let `F` be the finite reset family, and put a directed edge between two members whenever a finite positive-probability path connects them (the path may leave `F`). From any `f in F`, choose a terminal strongly connected component `D` in the reachable part of this finite graph. Every state `y` reachable from `D` has a finite positive-probability path back to some `g in F`, by the uniform reset. Terminality forces `g` to lie in `D`; otherwise `D` would reach a distinct component. Thus every such `y` communicates with `D`. The set of states reachable from `D` is closed by definition and is a communicating class. Consequently every `f in F` reaches a closed class, and hence the common atom.

Choose one finite path from each of the finitely many `f` to the atom. Pad their lengths to a common maximum using the atom's positive-probability empty-root self-loop. The minimum of these finitely many path probabilities is positive. Compose with the uniform reset block to obtain a uniform common-atom minorization. This establishes existence and uniqueness of a stationary probability law and the claimed uniform geometric total-variation bound by the existing atom/minorization lemma. Aperiodicity is supplied by the atom's self-loop, not presumed earlier.

Label equivariance gives symmetry of the unique stationary law. Relabelled canonical atoms provide every observer a full cache with positive stationary probability. Thus every local request size up to three has positive stationary availability and a uniform ordered conditional sample. Total-variation convergence of the full chain and a positive limiting denominator imply the same conditional sampling limit from each initial state.

The proof is qualitative. Its age-dependent accessibility gadgets are combined with the separate uniform finite-age reset; they are not themselves claimed to have an age-uniform duration. This assembly supplies finite constants, not polynomial or practical bounds.
