# Results registry

Last reconciled with [the paper source](../paper/main.tex): **20 October 2026**.

**Status convention.** “PROVED” means that the working paper contains a proof, including internal independent audits where recorded. These are research working proofs, not peer-reviewed results or Lean/formal-verification certificates. “COMPUTER-ASSISTED” identifies a proof whose finite step is an exhaustive exact calculation. Ordinary finite tests support proofs but do not establish arbitrary-network claims. “CONDITIONAL” means a proved implication or local lemma with additional hypotheses; those hypotheses have not been shown universally reachable. “OPEN” is not an achieved result.

The authoritative mathematical statements are in the single [paper/main.tex](../paper/main.tex). Search the **stable TeX labels** below; line numbers and theorem numbers change. See [DEPENDENCIES.md](DEPENDENCIES.md) for how the arguments fit together.

## The adopted model

The main target is `sec:target`, with kernel `\widehat P_ell`. All positive claims below use this model unless explicitly placed in the variants section.

- Fixed membership of `n >= 2` honest peers; no churn, failures, message loss, concurrent exchanges, or external identity introduction.
- A common capacity `c` and fixed shuffle length `ell`, with `1 <= ell <= c <= n-1`. Caches may be empty or underfull and contain distinct nonself identities. Capacities are homogeneous.
- Arbitrary finite nonnegative **integer** initial ages, with no common initial bound. Initial overlay is **weakly connected**; full caches and strong connectivity are not required.
- Independent uniform **global initiators**, including empty-cache peers; an empty initiator is a no-op. Equivalently, independent rate-one Poisson clocks produce this embedded chain. The original fixed periodic scheduler is not covered by these positive theorems.
- The initiator increments its resident ages, chooses a uniform oldest partner, and requests its own fresh age-zero descriptor plus `min(ell-1, cache_size-1)` extras. The responder returns a uniform `min(ell, responder_cache_size)` subset from its pre-exchange cache, without incrementing responder ages.
- **Mandatory partner removal.** Every valid received identity is protected; duplicates keep the **minimum** age. Vacancies are filled first, then only **sent resident identities absent from the incoming packet** may be victims. Unsent residents and newly received entries cannot be victims.
- Exchanges are atomic and reliable. Ties, subsets, and eligible victim sets are uniform, with the conditional independence specified in the algorithm section.

The sampling target is an ordered uniform sample without replacement from a cache at a **deterministic observation time**, conditional on enough cached identities. Waiting/retrying until availability is a different observation rule. Uniform local samples do not imply independent samples across times/peers, a uniform full overlay, or a useful mixing rate.

All time bounds below count **global activation events, including no-ops**. A block of `n` events gives one initiation per peer on average.

## Complete convergence and uniform-sampling results

These establish unique stationary full-state law, convergence including descriptor ages, positive stationary availability for every allowed request size, and conditional uniform local samples.

| Status | Parameter range | Stable TeX label | Scope notes |
|---|---|---|---|
| PROVED | `ell=1`, every `n` and allowed `c` | `thm:thesisone` | Transfers the singleton constructions to protection + minimum ages. |
| PROVED | `c=ell=1`, every `n>=2` | `thm:mandatoryone` | Explicit stationary law: uniform labelled rooted spanning trees, all ages zero, arcs toward the empty root. |
| PROVED | `c=ell=2`, every `n>=3` | `thm:thesisc2` | First arbitrary-population multi-entry theorem. The later quantitative proof also supplies a direct constructive common atom. |
| PROVED | `ell=2`, every `n>=3`, `2<=c<=n-1` | `thm:thesisgeneraltwo` | Covers fixed small caches in arbitrarily large networks. No practical general-`c` mixing estimate is extracted. |
| PROVED | `ell=3`, `max(3,n-2)<=c<=n-1` | `thm:dense3uniform` | Nearly full-cache regime. Useful structurally, but not the practical fixed-small-cache target. |

Earlier special cases `thm:thesishalfdense` (`ell=2`, `n<=2c`) and `thm:thesisdense` (`ell=2`, `c>=n-2`) are retained proofs now subsumed by `thm:thesisgeneraltwo`.

### Explicit two-entry-cache bounds

| Status | Result | Stable TeX label |
|---|---|---|
| PROVED | For `c=ell=2`, every state reaches a prescribed canonical atom with `T_n=16n^2`, `Gamma_n=(4n)^(-T_n)`: `P^T_n(x,{h}) >= Gamma_n`. | `thm:c2explicitmix` |
| PROVED | Full-state error `<= (1-Gamma_n)^floor(t/T_n)`; sufficient mixing horizon `T_n ceil(Gamma_n^(-1) log(1/epsilon))`. This is `exp(O(n^2 log n)) log(1/epsilon)`, **not polynomial mixing**. | `thm:c2explicitmix` |
| PROVED | Stationary one-entry availability `>= (n-1)/(2n) >= 1/3`; two-entry availability `>= n^(-3)`. | `prop:c2availabilityquant` |
| PROVED | Explicit conditional sample bounds use `log(12/epsilon)` for one ID and `log(4n^3/epsilon)` for two IDs in the same common-atom expression. | `cor:c2samplemixquant` |
| PROVED | Some initial state has one-ID error at least `((1-1/n)^t - 1/(n-1))_+`; worst-case fixed-error local mixing is at least `Omega(n)` global events. | `prop:c2samplelower` |

The quadratic witness is independent of initial ages and needs **no age reset before its construction**. Its exponentially small prescribed-history probability is why the resulting mixing estimate is poor. For arbitrary `c` at `ell=2`, `cor:twoimplicitmixing` records the finite-family construction; its unspecified finite path maximum is not an explicit useful `n,c` rate.

Primary checker: [verify_thesis_c2_quantitative.py](../verification/mandatory-removal/verify_thesis_c2_quantitative.py). This checker supports the constructive proof; its finite runs are not the arbitrary-`n` proof.

## Ordinary random executions at `c=ell=2`

These bounds concern the actual independent uniform scheduler, rather than one rare controlled word.

| Status | Result | Stable TeX label |
|---|---|---|
| PROVED | Every fixed nontrivial cut is contacted in expected time `<=7n`; tail `Pr(tau>14nk)<=2^(-k)`, uniformly over initial ages. | `thm:c2readycontact` |
| PROVED | Observed interaction graph becomes connected in expected time `<=7n(n-1)`; sufficient high-probability time `14n ceil(n-1+log2(1/epsilon))`. | `cor:c2readytemporal` |
| PROVED | A specified peer initiates a nonempty exchange in expected time `<=8n`; all peers emit a fresh self descriptor by `16n ceil(log2(n/epsilon))` with probability `>=1-epsilon`. | `cor:c2successfulsourcecover` |
| PROVED | Auxiliary young-descriptor components equal the cumulative interaction graph's components, for **every** shuffle length under the adopted merge rules. | `lem:younginteractioncomponents` |
| PROVED | At any observer, finite-time nonempty probability `>=1/(20n)` for every `t>=2n`, without using a common atom. | `lem:c2transientavailability` |

**These are communication/availability guarantees, not sampling mixing bounds.** Young connectivity or complete replacement of initial descriptors does not establish exchangeability of labels. The exact three-peer fresh-but-biased example has availability `7/12` and conditional output probabilities `(3/7,4/7)` after one random permutation of initiators.

Checkers: [verify_c2_ready_drift.py](../verification/mandatory-removal/verify_c2_ready_drift.py), [verify_c2_refresh_counterexample.py](../verification/mandatory-removal/verify_c2_refresh_counterexample.py).

### A precise target for a faster general-network proof

`prop:c2localcouplingtarget` reduces one-ID sampling error to pairwise label bias. Let `Q_x,i,t` include empty output `bottom`, and let `sigma_ab` swap two target labels while fixing observer `i`. Define

`beta_x,i(t) = max_(a!=b, a,b!=i) TV(Q_x,i,t, Q_sigma_ab(x),i,t)`.

For `t>=2n`, conditional one-ID error is at most `10n(n-2) beta_x,i(t)`. A bound `beta <= K_n exp(-t/L_n)` **uniform over all initial states and observers**, with polynomial `K_n,L_n`, would give polynomial single-ID mixing. **Such a bound remains OPEN.**

`lem:c2symmetrycoupling` bounds label-pair distance by the tail for hitting a state invariant under that transposition. This is a valid conditional coupling route; no polynomial symmetry-set hitting bound is proved.

## Exact three-peer ordinary sampling results

These are genuinely finite calculations with analytic scope reductions, not arbitrary-network evidence promoted to a theorem.

| Status | Result | Stable TeX label / source |
|---|---|---|
| PROVED | On `n=3,c=ell=2`, each updated cache has at most one positive-age entry. After coupon-cover burn-in, collapsing every positive age to one is an **exact** Markov projection with 487 connected states. | `prop:c2threepositivity` |
| COMPUTER-ASSISTED PROOF | Exact eight-event antisymmetric contraction `34447/69984 < 1/2`, and minimum availability `5/9` after four events, on all 487 projected states. | `prop:c2threeordinarysample` |
| COMPUTER-ASSISTED PROOF | From **every arbitrary-age connected initial state** on three peers, sufficient one-ID error-`epsilon` horizon is `ceil(log(9/epsilon)/log(3/2)) + 8 ceil(log2(3/epsilon))`. For `epsilon=10^-6`, 216 events suffice. | `prop:c2threeordinarysample` |
| EXACT BENCHMARK | The family reachable from the canonical atom has 75 states, all ages at most one. Worst recurrent-start conditional error **at time 8** is `9483/1420660`; **at time 25** it is `18359438816999/23769834206568612112`. | Paper's “exact three-peer recurrent-class benchmark” paragraph |

The 487-state projection does **not** say arbitrary actual numerical ages become at most one. It tracks identities and whether ages are zero or positive, which is sufficient for queries in this special three-peer invariant family. The 75-state benchmark has the narrower recurrent-start scope.

Checkers: [verify_c2_three_peer_antisymmetric.py](../verification/mandatory-removal/verify_c2_three_peer_antisymmetric.py) (exact integer certificate, standard library), [verify_c2_recurrent_mixing.py](../verification/mandatory-removal/verify_c2_recurrent_mixing.py) (exact local powers; optional NumPy full-state diagnostics).

**Generalization obstruction:** `prop:c2caprankobstruction` proves that on four peers, any fixed cap of absolute ages, even with the complete current global age ordering/equalities, is not query-sufficient on arbitrary-age starts. Two such indistinguishable starts have two-event query laws differing by exact TV `1/32`. This does not rule out every richer finite projection or prove unbounded recurrent ages. Checker: [verify_c2_age_projection_obstruction.py](../verification/mandatory-removal/verify_c2_age_projection_obstruction.py).

## Results for every shuffle length

| Status | Result | Stable TeX label |
|---|---|---|
| PROVED | Lossless pairwise identity-union exchange and preservation of weak connectivity. | `prop:thesisunion` (merge feasibility: `lem:receiveprotect`) |
| PROVED | Uniform access to a finite bounded-age family for every fixed `ell>=2`, arbitrary allowed `n,c`, arbitrary finite initial integer ages. | `lem:generalcolor`, `thm:thesisgeneralreset` |
| PROVED | Finitely many closed stationary regimes; continuous-time TV convergence to an initial-state-dependent mixture at some geometric rate; exponential stationary age tails. | `cor:thesisgeneralregimes` |

For the general reset, the paper gives

`H=(nc+1)(nc^2+1)(nc ell^c+1)`, `B=(nc+1)H`, `delta=(nc 16^c)^(-H)`,

with `P^H(x,F_B)>=delta` and `F_B` the finite connected age-`<=B` family. These results **do not establish uniqueness or uniform samples at the unresolved lengths**. Generic embedded-chain convergence is not silently substituted for the stated continuous-time mixture result.

Checker: [verify_thesis_general_reset.py](../verification/mandatory-removal/verify_thesis_general_reset.py).

## Higher-length building blocks and conditional progress

| Status | Parameter/hypothesis | Conclusion and stable TeX label |
|---|---|---|
| PROVED | `ell=2`, all `c,n`, one outside cache knows a cut-side identity | Holder-only first-contact controller, uniform horizon/probability; `thm:firstcontact`. Repeated contacts: `cor:repeatedcontact`. Root reachability: `prop:rootreachability`. |
| PROVED | `ell=3`, all allowed `c,n` | Holder-only uniform first contact across any cut; `thm:threefirstcontact`. This alone is not uniform sampling. |
| CONDITIONAL | Universal zero-age anchor at `ell=2` or `ell=3` | Finite path to any labelled canonical atom; `prop:anchorcanonical`, `prop:threezeroanchor`. Anchor removal: `lem:anchorreduction`. |
| CONDITIONAL | `ell=4`, `c>=max(4,n-2)` | First contact and universal-zero-anchor-to-atom reduction; `cor:densefourstructure`. Anchor accessibility remains open. |
| CONDITIONAL | Proper shuffle `2<=ell<c`; all old zero holders have occupancy at least `ell+1`; owner caches/reaches a nonzero holder | Zero-count gain preserving old zeros; `lem:largezerocallback`. Ages may affect path length. |
| CONDITIONAL | `ell>=3`; all old zero holders share `ell-2` additional zero-age identities also cached by owner | Cooperative callback and zero-count gain; `lem:threecooperativecallback`. |
| CONDITIONAL | Full shuffle `ell=c>=3`; corresponding `c-2` shared entries have a common integer age vector | Cooperative callback; `lem:fullpositivecallback`. |
| CONDITIONAL | `ell=3,c>=4`; exactly one nonowner lacks `a^0`, and owner caches that peer | Finish the last zero without a density assumption; `prop:nearcomplete3`. |
| CONDITIONAL | Proper shuffle, underfull zero responder; or stated local empty-target/oldest configuration | Local fresh-copy gains; `lem:underfullzeroreply`, `lem:emptytargetthree`. Universal accessibility of these configurations is unproved. |
| PROVED NEGATIVE AUXILIARY RESULT | Every `m>=3`, `ell=m`, `n=m+2`, capacity `m` or `m+1` | An owner-only execution can remain unable to contact a cached nonholder target; `prop:owneronlyobstruction`. This is **not a counterexample to iid all-peer CYCLON**. |

The shared-zero callback requires `Z_a<=n-ell+1`, so at `ell>=4` it cannot finish the last `ell-3` missing zeros. The common-positive-vector full-shuffle analogue requires `Z_a<=n-c+1`. Merely reaching shared descriptors is insufficient for a generic proof.

**Exact sufficient remaining obligation:** `prop:zeroexpansioncriterion`. For every connected state with `Z_a<n-1`, find a finite positive-probability path with strictly larger **endpoint count** `Z_a`. Temporary losses and changes of holder identities are permitted. If this is established at every larger length, lower-length anchor reduction and the reset/common-atom argument prove the full generic theorem. The universal obligation remains **OPEN**.

Related checkers: [verify_thesis_holder_routing.py](../verification/mandatory-removal/verify_thesis_holder_routing.py), [verify_thesis_cooperative_general.py](../verification/mandatory-removal/verify_thesis_cooperative_general.py), [verify_thesis_cooperative_vector.py](../verification/mandatory-removal/verify_thesis_cooperative_vector.py), [verify_thesis_proper_owner.py](../verification/mandatory-removal/verify_thesis_proper_owner.py), [verify_thesis_owner_cycle.py](../verification/mandatory-removal/verify_thesis_owner_cycle.py), [verify_thesis_underfull_bootstrap.py](../verification/mandatory-removal/verify_thesis_underfull_bootstrap.py).

## Other conventions: keep their conclusions separate

The paper preserves earlier investigations. Their parameter names do not make them the adopted kernel.

| Status | Convention / result | Stable TeX label |
|---|---|---|
| PROVED NEGATIVE | Four peers, `c=ell=1`, fixed periodic phases: no uniform convergence even from a strongly connected zero-age full state. | `thm:periodic` |
| PROVED NEGATIVE | Retention with already-known descriptors discarded without refreshing ages: frozen full strongly connected states. | `thm:twins`, `prop:zero` |
| PROVED NEGATIVE | Mandatory removal does not guarantee that an **unconditional full-capacity request** can always be answered. This does not refute availability-conditioned uniformity. | `prop:availability` |
| PROVED NEGATIVE | A different uniform-victim replacement completion fails conditional uniformity for `ell>=3`, including strongly connected full zero-age starts. Received-identity protection excludes this construction. | `thm:largerobstruction`, `cor:strongobstruction` |
| PROVED VARIANT | Capacity-one retention variant converges under its stated random scheduler. | `thm:positive` |
| PROVED VARIANT | Protected protocol with an independent positive probability of singleton shuffles converges for every maximum shuffle length. The no-refresh statement and adopted MIN extension are distinguished in the paper. This is **variable length**, not the fixed-length target. | `thm:protectedmixture`, plus the adopted-mixture paragraph immediately before “Established results and remaining problem” |
| PROVED VARIANT | Earlier lineage-erasure/age-reset results for no-refresh kernels are retained with their original assumptions. They must not be silently applied to MIN because MIN changes future oldest choices. | `thm:lineages`, `thm:tworeset`, `prop:tworegimes` |

## Open priorities and exclusions

1. **Useful single-ID mixing for arbitrary `n` at `c=ell=2`.** Aim for uniform decay of pairwise label bias, not another rarer canonical word. The current universal sampling upper bound remains exponential.
2. **Practical length-three convergence:** `ell=3` with fixed small capacity `c=3` or `c=4` and arbitrarily large `n`. Nearly full-cache length-three results do not settle this.
3. **Full arbitrary-length convergence** for the adopted fixed-length model, including the zero-count-improvement/endgame gap.
4. A richer query-sufficient projection or direct coupling beyond the special three-peer case.

Not claimed: heterogeneous capacities, churn/fault tolerance, the original periodic scheduler's convergence, uniform complete-overlay law, independent successive samples, generic polynomial mixing, or a Lean formalization. Lean work was explicitly deferred until the mathematical proofs are finalized.
