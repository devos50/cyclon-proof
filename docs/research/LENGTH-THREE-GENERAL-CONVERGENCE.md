# general convergence theorem for three-entry shuffles

Working proof integrated after independent end-to-end and final-text audits, 16 November 2026. Exactly `ell=3`, all `n>=4` and `3<=c<=n-1`. This is an internally audited working theorem, not a formally checked or externally peer-reviewed result. It does not settle shuffle lengths four and above or polynomial mixing/sampling rates.

Throughout, for a fixed owner `a`, a **nonholder means a peer different from a whose cache lacks a**. The owner itself is not counted as a holder or nonholder of its own identity.

## Theorem scope

For the adopted mandatory-removal, received-protection, minimum-age-merge algorithm with fixed three-entry shuffles and iid uniform initiators, there is a unique stationary probability law on weakly connected cache states with arbitrary finite nonnegative integer ages. For a prescribed labelled canonical atom `H(V,c)`, there are finite constants `T(n,c)` and `gamma(n,c)>0` such that

```
inf_x P_3^T(x,{H(V,c)}) >= gamma,
sup_x ||P_3^t(x,.)-pi||_TV <= (1-gamma)^floor(t/T).
```

For every observer and request size `1<=b<=c`, stationary availability is positive and its ordered local sample is uniform among ordered distinct nonself labels conditional on availability. The same conditional sampling limit holds from every allowed initial state. No polynomial, practical, or explicit useful bound for these constants is asserted.

## Dependencies and noncircularity

Previously established manuscript inputs:

- `thm:thesisgeneralreset`: uniform finite-age reset for each fixed shuffle length, independent of generic length-three convergence.
- `thm:thesisgeneraltwo` and the singleton base case: lower-length common-atom accessibility at every allowed capacity.
- `lem:anchorreduction`: legal simulation of that lower-length kernel while reserving a common zero anchor.
- `thm:threefirstcontact`: holder-only first contact with a frozen cut. Its proof uses lower-length results, not the present theorem.
- `prop:threezeroanchor`: a universal zero anchor at length three yields a finite path to any labelled canonical atom.
- `lem:atom` and the previously established label-equivariance/sample-symmetry argument.

New proof inputs under separate audit:

- `lem:threegeneralcallback` and `cor:threegeneralzeroify`, corresponding to `LENGTH-THREE-ARBITRARY-CAPACITY-CALLBACK-CANDIDATE.md`: boundary service at every capacity, followed by nonholder gain and zeroification.
- `lem:threeownerterminalgain`: the empty-owner terminal gadget, valid for arbitrary current target age; it requires only the callback, not convergence.
- Capacity-three outward gain and assembled convergence in `C3-OUTWARD-HOLDER-GAIN.md` and `C3-GENERAL-CONVERGENCE.md`.
- For `c>=4`, `SPARSE-LENGTH-THREE-OUTWARD-GAIN.md`: outward gain using the fixed-identity lexicographic potential. Its corrected policy explicitly returns already-known extra B when the zero responder lacks the current initiator. Without this policy the claimed strict potential increase is not justified.

Only the reserved-anchor simulation changes the effective shuffle length. No original trajectory is assumed to perform occasional shorter shuffles.

## 1. Classwise holder bound

Fix identity `a`. General zeroification gives, from any state, a finite path to a state where every target copy is zero and the endpoint holder count is no smaller. Its mechanism is a positive-holder first contact with the frozen owner/zero-holder cut: contact with a zero holder refreshes the active copy; contact with the owner may lose one holder, but gives the owner a cached nonholder and the learned-target callback restores at least that count while adding a zero. All prior zeros survive, so finitely many strict zero-count increases suffice.

In any closed communicating class let `k` be the largest attained `Z_a`. This maximum exists because the count ranges over finitely many integers. Zeroification implies `N_a<=k` at every class state. At a maximizing state all holders are zero; otherwise zeroification from it would exceed `k`. Write their set as `I`.

Also `k>=1`. If no peer caches `a`, weak connectivity requires a nonempty outgoing cache at `a`; an owner activation then creates a fresh zero copy.

## 2. Restricted owner closure and emptying

At a zero-maximizing state no nonholder is directed-reachable from owner `a`. Suppose a simple path to one exists, with all its internal vertices in `I`. Apply boundary service retaining the first path head, with the allowed responder set `H` consisting of the zero holders outside the remaining path. Before the boundary contact all remaining path rows are untouched. A contact outside `H` either reaches a nonholder, giving forbidden holder gain, or reaches an untouched path vertex whose reply can include `a` and the next path head. Require that next head in the reply; it is protected at the owner. Repeating along strictly shorter suffixes gives a nonholder gain, contradiction.

The reply selection is legal for partial shuffles: at a path vertex the two required identities are `a` and its successor, leaving at most one arbitrary filler. Before this terminal boundary event the callback policy applies only to off-path zero holders. No ability to retain a prescribed target across a different nonholder contact is assumed.

Let `R` be the set reachable from `a`, including `a`. Then `R\{a}` consists entirely of zero holders, and every cache of a vertex in `R` contains identities only in `R`. Freeze the complement. For an actual oldest owner head `Q`, normalize its residual weak component inside `R\{a}` to the lower-length canonical state with root `Q`, reserving `a^0`. If the component has `m` vertices, its effective residual capacity is `min(c-1,m-1)` and shuffle length `min(2,m-1)`. These parameters lie in the established length-two range; size-two components use the singleton base case, and singleton components need no action. Reduced empty-initiator no-ops are omitted.

The frozen owner keeps its actual oldest choice. The normalized root has cache `{a^0}`. The subsequent `a -> Q` receives only self-`a`, deleting one owner head without replacement. At `Q`, fresh `a` plus at most two extras fit in capacity `c>=3`, preserving its zero. Recompute residual components and repeat until the owner is empty. Every target zero is preserved. Thus every closed class has an empty-owner zero-maximizing state.

This uses only closure of the owner's reachable set, not global outward closure. It is therefore not circular with the outward-gain lemma that requires an empty owner.

## 3. Outward closure

Consider any empty-owner state with `Z_a=k`. All its holders are zero by step 1. At `c=3`, use the capacity-three outward-gain lemma. At `c>=4`, use the static-potential outward-gain lemma. If a holder cached any nonholder, either result would give a finite path with `N_a>k`, contradicting the classwise bound. Consequently every such maximizing state satisfies

```
C_i subset I union {a}  for all i in I.
```

The sparse lemma's numerical tail is independent of the potential marking issue: after its bounded lexicographic potential stabilizes, only nonholder migrations remain. Their new target copy is novel at its recipient, so its age increases exactly by one per migration; global per-identity maximum age minus elapsed events strictly decreases when that identity is selected. This excludes infinite migration tails. No finite-state assumption on ages or random-scheduler fairness is used.

## 4. Incoming boundary yields a universal zero anchor

For `c=3`, the separately audited minimum-residual-component argument in `C3-GENERAL-CONVERGENCE.md` applies for every `n>=4`. It handles the possible swap of a zero holder across a full three-entry boundary packet. Its use of outward closure is justified by step 3, and its component minimum is over empty-owner maximizing states obtained in step 2.

Now take `c>=4`. Suppose nonholders `J=V\(I union {a})` remain at an empty-owner maximizer. Weak connectivity forces an edge from `J` to `I`: the owner is empty, no nonholder caches `a`, and outward closure excludes edges from `I` to `J`.

Freeze `I` and the owner. By the established length-three first-contact theorem, there is a finite outside-initiator path reaching a first boundary contact `P -> Q`, where `P in J` and `Q in I`. Stop immediately before it. No outside peer has acquired `a` before this first boundary.

Pause all outside peers, leaving the pending actual oldest choice of `P` unchanged. Reserve the common zero anchor and normalize the residual component of `Q` inside `I` to its lower-length canonical root. It now has `C_Q={a^0}`. Resume `P -> Q`.

The initiator gains `a^0` from the sole reply; mandatory deletion supplies its vacancy. The responder receives at most three identities, none equal to `a`, because the initiator was a nonholder. These fit alongside its old anchor in capacity at least four. Thus `Q` keeps `a^0` and `P` becomes an additional zero holder. All other zero holders are unchanged. This contradicts maximality of `k`.

Hence `J` is empty: every closed class contains a universal zero anchor.

## 5. Uniform finite reset, common atom, and sampling

The universal-zero-anchor proposition now supplies a finite path from every closed communicating class to the same prescribed canonical atom.

To justify existence and accessibility of such classes, let `F` be the finite reset family from the uniform finite-age-reset theorem. Make a finite directed graph on `F`, connecting two vertices when a finite positive-probability path in the full chain connects them; intermediate states may lie outside `F`. From any `f in F`, choose a terminal strongly connected component `D` in its reachable subgraph. Every state `y` reachable from `D` has a finite path back to some `g in F`, since uniform reset has positive probability from every state. Terminality forces `g in D`. Therefore all states reachable from `D` communicate with it; their set is closed by reachability and forms a closed communicating class. Every `f` thus reaches a class and then the common atom.

Choose one such path for each of the finitely many reset states, and pad their lengths to a common finite maximum using the atom's positive-probability empty-root self-loop. Their minimum path probability is positive. Compose these paths with the uniform reset block to obtain the asserted common-atom minorization. The existing atom/minorization lemma yields unique stationary probability and uniform geometric total-variation convergence. Aperiodicity comes from this atom self-loop and is not presumed in the earlier class argument.

Label equivariance makes the unique stationary law invariant under relabelling. Relabelled canonical atoms ensure each observer has positive probability of a full cache, giving positive availability for every `b<=c`. The ordered-sampling symmetry argument gives conditional uniformity. Full-state total-variation convergence together with the positive limiting denominator implies convergence of the conditional sample laws.

The age-dependent finite accessibility arguments are made uniform only through the separate finite reset. The resulting constants are existential; this proof does not imply polynomial local sampling or practical convergence time.

## Final integration status

This working result is now integrated in the manuscript after independent end-to-end and actual-text audits. See [the audit record](LENGTH-THREE-AUDIT.md). Earlier candidate wording in this research history is superseded by that status; no formal-verification or external-review claim is made.
