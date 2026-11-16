# Results registry

Last reconciled with [the paper source](../paper/main.tex): **16 November 2026**.

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
| PROVED | `c=ell=3`, every `n>=4` | `thm:c3generaluniform` | Arbitrary-population full capacity-three convergence; qualitative constants only, no polynomial mixing bound. |
| PROVED | `ell=3`, every `n>=4`, `3<=c<=n-1` | `thm:threegeneraluniform` | Full arbitrary-capacity three-entry convergence; implicit constants, no polynomial bound. |
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
| PROVED | On `n=3,c=ell=2`, within-row positive-age ranks plus zero flags give an exact **1306-state time-zero projection** for all finite initial ages. | `prop:c2threeorderprojection` |
| COMPUTER-ASSISTED PROOF | Exact integer query powers certify one-ID conditional error below `10^-6` at **every `t>=56`** from all connected finite-age starts; at `t=55` some start exceeds this tolerance. | `prop:c2three56sample` |
| PROVED | On `n=3,c=ell=2`, each updated cache has at most one positive-age entry. After coupon-cover burn-in, collapsing every positive age to one is an **exact** Markov projection with 487 connected states. | `prop:c2threepositivity` |
| COMPUTER-ASSISTED PROOF | Exact eight-event antisymmetric contraction `34447/69984 < 1/2`, and minimum availability `5/9` after four events, on all 487 projected states. | `prop:c2threeordinarysample` |
| COMPUTER-ASSISTED PROOF | From **every arbitrary-age connected initial state** on three peers, sufficient one-ID error-`epsilon` horizon is `ceil(log(9/epsilon)/log(3/2)) + 8 ceil(log2(3/epsilon))`. For `epsilon=10^-6`, 216 events suffice by this older bound; the time-zero certificate improves this to 56. | `prop:c2threeordinarysample` |
| EXACT BENCHMARK | The family reachable from the canonical atom has 75 states, all ages at most one. Worst recurrent-start conditional error **at time 8** is `9483/1420660`; **at time 25** it is `18359438816999/23769834206568612112`. | Paper's “exact three-peer recurrent-class benchmark” paragraph |

The 487-state projection does **not** say arbitrary actual numerical ages become at most one. It tracks identities and whether ages are zero or positive, which is sufficient for queries in this special three-peer invariant family. The 75-state benchmark has the narrower recurrent-start scope.

Checkers: [verify_c2_three_peer_order_projection.py](../verification/mandatory-removal/verify_c2_three_peer_order_projection.py) (time-zero projection and 56-event certificate), [verify_c2_three_peer_antisymmetric.py](../verification/mandatory-removal/verify_c2_three_peer_antisymmetric.py) (exact integer certificate, standard library), [verify_c2_recurrent_mixing.py](../verification/mandatory-removal/verify_c2_recurrent_mixing.py) (exact local powers; optional NumPy full-state diagnostics).

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
2. **Length-four convergence:** fixed `ell=4`, starting with small capacities and arbitrarily large `n`. All allowed length-three capacities are now covered qualitatively by `thm:threegeneraluniform`.
3. **Full arbitrary-length convergence** for the adopted fixed-length model, including the zero-count-improvement/endgame gap.
4. A richer query-sufficient projection or direct coupling beyond the special three-peer case.

Not claimed: heterogeneous capacities, churn/fault tolerance, the original periodic scheduler's convergence, uniform complete-overlay law, independent successive samples, generic polynomial mixing, or a Lean formalization. Lean work was explicitly deferred until the mathematical proofs are finalized.

## Population-independent transient availability (16 November 2026)

**PROVED (working symbolic argument).** `lem:c2constanttransientavailability` establishes, for the adopted `c=ell=2` protocol, every `n>=3`, arbitrary finite initial ages, and every observer,

`alpha_x,i(t) >= exp(-8)/8` for every integer `t >= 8(n-1)`.

The proof uses the existing `7n` expected singleton-cut contact bound, independent thinning of empty-observer no-ops, and a no-observer-activation event of constant probability. It does not assume that a cut crossing makes the sample uniform. `cor:c2linearconditioningfactor` consequently replaces the quadratic conditioning factor by the alternative linear factor `4 exp(8) (n-2)` after that burn-in. The constant is large; retain the earlier bound when smaller. Decay of pairwise label bias remains **OPEN**.

## Generic finite-horizon age reduction

| Status | Scope and claim | Source |
|---|---|---|
| PROVED | Every allowed `n,c,ell`, fixed integer horizon `T`: capping consecutive global initial-age gaps at `T+1`, anchored at zero, preserves the complete identity trajectory law through `T`; representative initial ages are at most `nc(T+1)`. | `prop:finitehorizonagecompression` |
| PROVED | Fixed-parameter finite-time query laws over arbitrary initial ages equal those over the finite bounded-age family; exact exhaustive certification is possible in principle. No efficiency or contraction claim. | `cor:finitehorizoncertification` |

This differs from the false fixed absolute-cap-plus-ranks projection: the retained gap data depend on the requested horizon. The [checker](../verification/mandatory-removal/verify_finite_horizon_age_compression.py) corroborates the symbolic proof, rather than proving arbitrary-size mixing by finite cases.

## Refresh-conditioned bias under the actual iid scheduler (16 November 2026)

**PROVED counterexample.** `prop:c2iidrefreshbias` uses the zero-age three-peer star at deterministic time two. Complete refreshing has probability `2/9` and gives a connected interaction graph. Conditional on refreshing and observer-1 availability, the output is identity 2 with probability one (TV error `1/2`). This is separate from the earlier random-permutation example. The extra freshness conditioning must not be confused with the target conditioned only on availability. It refutes a shortcut, not convergence.

Uniform finite-horizon availability and conditional-error bounds, once certified for every initial state, persist at every later observation time by Markov conditioning and convexity. This does not imply multiplicative contraction across successive blocks.

## Full-state finite-horizon certificates (16 November 2026)

**PROVED reduction.** `prop:finitehorizonfulltv` strengthens age-gap compression: a common injective map on every reachable age `a_j+k`, `0<=k<=T`, preserves full-state TV exactly. For a fixed transposition, `sup_x TV(P^T(x),P^T(sigma x))` equals a finite maximum over weakly connected initial states with ages at most `nc(T+1)`. For arbitrary pairs of starts, use their combined initial levels and the bound `2nc(T+1)`. Transitions are never truncated.

**CONDITIONAL contraction criterion.** `cor:finiteantisymmetriccertificate` shows that a verified full-state antisymmetric coefficient `rho<1` yields pairwise query bias at most `rho^floor(t/T)` for all initial ages. This is not true merely from a scalar query threshold. No new polynomial-in-`n` coefficient was obtained; such a rate still requires polynomial block length and inverse contraction gap. Antisymmetric contraction alone does not prove uniqueness in label-invariant parts of the state space.

## Full-state contraction block lower bound

`prop:antisymmetriccouponlower` proves for every allowed `n,c,ell` that the full-state transposition coefficient is at least the probability that `n-1` leaf coupons have not all appeared in `T` uniform activations. In particular the coefficient is exactly one when `T<n-1`, and fixed-constant contraction requires `Omega(n log n)` events. This constrains the full-state certificate route, not the local single-query mixing time; it does not rule out polynomial sampling rates.

## Unit-width secondary-anchor callback (16 November 2026)

**CONDITIONAL WORKING RESULT:** `lem:fullbandcallback` applies at every full shuffle `ell=c>=3`. If every old `a^0` holder shares `c-2` secondary identities, each at one of two adjacent coordinate-specific ages `{m_p,m_p+1}`, and the owner's corresponding ages are at least `m_p`, at most `3(|I|+1)+1` controlled exchanges gain a zero while preserving all old zeros. This broadens `lem:fullpositivecallback` beyond exactly common ages. The shared identities/bands are not proved universally accessible, and `|I|<=n-c+1` still prevents resolving the higher-length endgame. See [proof details](research/UNIT-WIDTH-CALLBACK.md) and [checker](../verification/mandatory-removal/verify_thesis_cooperative_bands.py).

## Worst-case full-state mixing lower bound (16 November 2026)

**PROVED symbolic corollary.** `cor:fullstatemixingcouponlower` upgrades the high-age-star obstruction to distance from any fixed stationary probability law. For every event horizon `T`, worst-case full-state TV is at least the probability that one of `n-1` leaves has not initiated, hence at least `M_T/(1+M_T)` where `M_T=(n-1)(1-1/n)^T`. For the known unique `c=ell=2` stationary law this gives an `Omega(n log n)` full-state mixing lower bound at fixed error, with the displayed epsilon-dependent integer bound in the paper. The proof sends the initial star age to infinity after fixing `T`, removing the stationary age tail. It is not a single-query lower bound or a claim about one fixed start at every horizon.


## Capacity-three learned-target boundary service (16 November 2026)

**Symbolic working result, independently reviewed:** `lem:c3learnedcallback` gives finite owner boundary service through any specified subset of zero holders at exactly `c=ell=3`, without a shared-secondary or age-band assumption. `cor:c3zeroify` gives some nonholder gain when the owner caches a nonholder, and zeroification without decreasing endpoint holder count. This does not promise service to a prescribed nonholder or an age-uniform gadget duration. The proof is in [C3-LEARNED-TARGET-CALLBACK.md](research/C3-LEARNED-TARGET-CALLBACK.md); `verify_thesis_c3_learned_callback.py` corroborates exact finite transitions, not the unbounded-age argument. Full convergence additionally requires the separately audited outward-holder and extremal arguments.

## Arbitrary-population full capacity-three theorem (16 November 2026)

**Working proof integrated:** `thm:c3generaluniform` proves unique full-state stationarity, uniform geometric convergence, positive stationary availability, and limiting conditional uniform samples for **exactly `c=ell=3`, every `n>=4`**, with arbitrary finite nonnegative integer ages and initially underfull weakly connected caches under the adopted iid scheduler. The proof combines learned-target boundary service, zeroification, owner-directed emptying without circular outward closure, the new outward-gain gadgets and age potential, the incoming minimum-component contradiction, and the existing finite reset/common atom argument. Separate end-to-end and final-text audits are recorded in the research continuation. This is a mathematical working proof, not formal verification or external peer review.

At this earlier capacity-three stage, sparse larger capacities were still open; the subsequent all-capacity length-three theorem below supersedes that boundary. Higher lengths and polynomial mixing remain open. Earlier continuation entries describing capacity-three outward gain as open are superseded by this theorem. The [assembled proof](research/C3-GENERAL-CONVERGENCE.md), [outward argument](research/C3-OUTWARD-HOLDER-GAIN.md), and [terminal gadgets](research/FULL-SHUFFLE-TRIANGLE-GAIN.md) record the dependency chain and corrected MIN-age inequalities.

## All capacities at shuffle length three (16 November 2026)

**Working proof integrated:** `thm:threegeneraluniform` now covers every `n>=4` and `3<=c<=n-1` at fixed `ell=3`, with the adopted protected/MIN kernel, iid initiators, initially weak connectivity, and arbitrary finite integer ages. It proves unique full-state stationarity, uniform geometric convergence with implicit constants, positive stationary availability, and conditional uniform local sampling for every request size up to capacity. The arbitrary-capacity callback, empty-owner restoration, and fixed-identity lexicographic outward potential are linked to the lower-length residual normalization and finite-reset/common-atom argument. The [full assembly](research/LENGTH-THREE-GENERAL-CONVERGENCE.md) and [sparse outward proof](research/SPARSE-LENGTH-THREE-OUTWARD-GAIN.md) state the scope and necessary controlled reply choices.

This supersedes earlier continuation entries saying sparse length-three convergence remained open. Lengths four and above and polynomial/practical mixing bounds remain open. These are internally audited mathematical working proofs, not formal verification or external peer review.
