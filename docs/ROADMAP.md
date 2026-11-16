# Research roadmap

This is a working research record, not a publication claim. The manuscript is [paper/main.tex](../paper/main.tex), and the fixed target is summarized in [MODEL.md](MODEL.md). Authorship, submission plans, and external review status are not set here.

## Current general result (16 November 2026)

The internally audited working theorem `thm:allparametersuniform` now covers
every allowed fixed length, capacity, and population for the adopted kernel.
See [the source-route record](research/GENERAL-SOURCE-CONVERGENCE.md).
Two independent end-to-end internal audits have passed; external peer review,
formal verification, and useful/polynomial mixing rates are not claimed.
Earlier checkpoints below retain their historical controller hypotheses.
Statements there that general qualitative convergence remained open are
superseded by this result. Current priorities are external review, proof
simplification, and useful sampling rates, not isolated length-four casework.

## Current boundaries

All rows refer to the adopted protected, mandatory-removal, minimum-age model with independent uniform initiators.

| Parameters or question | Current draft result | Source labels |
| --- | --- | --- |
| $\ell=1$, arbitrary allowed $n,c$ | Unique full-state stationarity, convergence, positive availability, conditional uniform samples | thm:mandatoryone, thm:generalone, thm:thesisone |
| $\ell=2$, arbitrary allowed $n,c$ | Same full convergence and sampling result | thm:thesisc2, thm:thesisgeneraltwo |
| $c=\ell=2$, arbitrary $n$ | Explicit pessimistic mixing bound from a quadratic controlled witness | thm:c2explicitmix |
| $c=\ell=2$, arbitrary $n$ | Ordinary cut contact in expected time at most $7n$ events | thm:c2readycontact |
| $c=\ell=2$, arbitrary $n$ | Ordinary temporal connectivity in $O(n^2+n\log(1/\varepsilon))$ events with high probability | cor:c2readytemporal |
| $c=\ell=2$, arbitrary $n$ | All peers emit fresh selves in $O(n\log(n/\varepsilon))$ events with high probability | cor:c2successfulsourcecover |
| $n=3,c=\ell=2$, arbitrary finite initial ages | Exact finite projection and certified $O(\log(1/\varepsilon))$ one-sample bound | prop:c2threepositivity, prop:c2threeordinarysample |
| $\ell=3,c\ge n-2$ | Full convergence and conditional sampling | thm:dense3uniform |
| $c=\ell=3$, every $n\ge4$ | Full convergence and conditional sampling; qualitative constants | thm:c3generaluniform |
| $\ell=3$, every allowed $n,c$ | Full convergence and conditional sampling; implicit constants | thm:threegeneraluniform |
| $c=n-1$, every allowed $\ell$ | Full convergence and conditional sampling | thm:fullcapacityalllengths |
| Every allowed fixed $\ell,c,n$ | Unique full-state stationarity, implicit uniform geometric convergence, positive availability, conditional uniform samples | thm:allparametersuniform |
| Every fixed allowed $\ell\ge2$ | Finite-age recurrence, finitely many stationary regimes, continuous-time convergence to a possibly initial-dependent mixture, stationary age tails | thm:thesisgeneralreset, cor:thesisgeneralregimes |

The paper retains older results for other conventions. Their scope must not be silently combined with the adopted model.

## Quantitative direction: useful sampling rates for small fixed caches

The practical target is a fixed small cache with arbitrarily large membership. Start with $c=\ell=2$ and one returned identifier.

The present full-state bound uses
$$
T_n=16n^2,\qquad \Gamma_n=(4n)^{-T_n},
$$
giving an $\exp(O(n^2\log n))\log(1/\varepsilon)$ upper bound. It is explicit but too pessimistic to describe practical performance. Further shortening the prescribed witness is lower priority than controlling ordinary executions.

### The next precise target

Fix observer $i$ and exchange two other labels $a,b$ everywhere in the initial state. Couple executions from $x$ and $\sigma_{ab}x$. Let $Q$ be the single-query law, including $\bot$. Control
$$
\beta_{x,i}(t)=
\max_{a\ne b,\ a,b\ne i}
\|Q_{x,i,t}-Q_{\sigma_{ab}x,i,t}\|_{\mathrm{TV}}.
$$

The proved reduction **prop:c2localcouplingtarget** converts contraction of this quantity into conditional uniformity. It does not require coupling every age and cache in the network.

Two routes remain:

1. A multistep or transport coupling that tolerates copying and collisions while contracting label bias.
2. A polynomial hitting bound for $F_\sigma=\{z:\sigma z=z\}$. The proved symmetry-set coupling would then give contraction. For $n\ge4$, this set includes two target peers with identical external caches and no incoming references to either. Its polynomial hitting bound is not proved.

Readiness and source coverage provide quantitative communication tools. The missing quantitative step is a useful contraction rate for label bias.

### The completed three-peer case

The latest improvement (16 November 2026) uses an exact **1306-state local-order projection from time zero**, valid for every finite initial age. Exact query powers prove conditional error below `10^-6` at all times `t>=56`; some state still exceeds that error at `t=55`. This replaces the previous 216-event sufficient horizon at that tolerance, without changing the open arbitrary-network problem. See `prop:c2threeorderprojection`, `prop:c2three56sample`, and [the checker](../verification/mandatory-removal/verify_c2_three_peer_order_projection.py).

The older general-epsilon argument is retained:

After burn-in on three peers, every cache has at most one positive entry. Zero/positive flags then form an exact 487-state Markov projection. Exhaustive integer arithmetic certifies
$$
\max_z\|P^8(z,\cdot)-P^8(\sigma z,\cdot)\|_{\mathrm{TV}}
=\frac{34447}{69984}<\frac12.
$$

This proves a local rate from every finite-age initial state. It is stronger in scope than the separate 75-state recurrent-start benchmark.

Four peers can have two positive entries, so positivity alone is insufficient. Capped absolute ages augmented by global age ranks also fail as an exact query projection. A richer projection or different coupling is needed.

Useful checkers:

- [Quadratic witness](../verification/mandatory-removal/verify_thesis_c2_quantitative.py)
- [Ordinary readiness](../verification/mandatory-removal/verify_c2_ready_drift.py)
- [Three-peer antisymmetric certificate](../verification/mandatory-removal/verify_c2_three_peer_antisymmetric.py)
- [Recurrent benchmark](../verification/mandatory-removal/verify_c2_recurrent_mixing.py)
- [Age-projection obstruction](../verification/mandatory-removal/verify_c2_age_projection_obstruction.py)
- [Refreshing counterexamples](../verification/mandatory-removal/verify_c2_refresh_counterexample.py)

## Current priority: parameterized arbitrary-length convergence

The earlier convergence benchmark was $\ell=4$ with a fixed small capacity and arbitrary $n$; the general source theorem now covers it. All allowed length-three capacities are now covered by `thm:threegeneraluniform`; the length-three callback and static-identity potential do not automatically extend to larger shuffle lengths.

Nearly full caches are useful for testing proof mechanisms, but further extensions confined to that regime have lower practical priority.

Existing tools include holder-only first contact at length three, universal-zero-anchor reduction, conditional cooperative callbacks, and a zero-count expansion criterion. A sufficient remaining statement is:

> For fixed identity $a$, every connected state with fewer than $n-1$ age-zero copies of $a$ can reach a state with strictly more such copies through a finite legal path.

Only endpoint improvement is needed. Temporary losses may be restored later; requiring fresh-copy preservation at every intermediate event can unnecessarily exclude useful constructions.

Conditional callback lemmas do not prove that their shared-descriptor or occupancy hypotheses are universally accessible. Shared zero-anchor constructions cannot cover the last $\ell-3$ missing fresh copies when $\ell\ge4$; a separate endgame or a new progress measure is needed.

Useful checkers:

- [Holder routing](../verification/mandatory-removal/verify_thesis_holder_routing.py)
- [Cooperative callbacks](../verification/mandatory-removal/verify_thesis_cooperative_general.py)
- [Common age vectors](../verification/mandatory-removal/verify_thesis_cooperative_vector.py)
- [Proper-shuffle owner service](../verification/mandatory-removal/verify_thesis_proper_owner.py)
- [Owner-only obstruction](../verification/mandatory-removal/verify_thesis_owner_cycle.py)
- [Length-three boundary proof](../verification/mandatory-removal/verify_thesis_dense_three_boundary.py)

## Audit and presentation

Before a submission-ready claim:

- Re-audit the full length-two dependency chain under the exact adopted kernel.
- Separate main proofs from retained variants and historical intermediate statements.
- Distinguish exact finite certificates from random or finite-case corroboration of symbolic proofs.
- Retain the analytic projection justification alongside the integer three-peer certificate.
- State scheduler, time units, and conditioning events explicitly.

Lean formalization was discussed and explicitly deferred by the user until the mathematical proofs are finalized. Do not start it during routine continuation.

## Failed shortcuts and nonresults

- Connected interaction history does not imply uniform samples.
- All descriptors being fresh, or every peer having sent its fresh self, does not imply exact uniformity. The three-peer counterexamples are exact.
- Young-edge components coarsen, but total young-entry count need not increase under ordinary executions.
- Total OLD-copy count and the number of copies at the current minimum OLD age can both have positive expected drift.
- Straight synchronous row-Hamming coupling can expand.
- Collapsing target labels to one anonymous color loses owner/reference correlations and is not an exact Markov projection.
- Owner-only service can fail for longer full shuffles. Those restricted cycles do not refute the all-peer random protocol.
- Polynomial controlled-path length does not establish polynomial expected mixing time.
- Failure of the cap-plus-rank projection does not rule out every finite abstraction or prove unbounded recurrent ages.
- The earlier nearly full length-three theorem alone does not cover fixed small caches; the new general length-three theorem does, without a practical mixing bound.
- Counterexamples for retention, unprotected victims, or periodic schedules do not refute the adopted model.

The arbitrary-network polynomial sampling bound remains open; the arbitrary-shuffle convergence theorem now has an internally audited working proof. No completion date is established.


## Availability refinement (16 November 2026)

The conditioning step now has an arbitrary-`n` constant availability bound: `exp(-8)/8` after `8(n-1)` events (`lem:c2constanttransientavailability`). Hence pairwise label-bias decay would incur only a linear population factor (`cor:c2linearconditioningfactor`). This sharpens a prerequisite but does not prove the needed decay. Continue prioritizing a genuine contraction or a rigorous obstruction, rather than treating communication or availability as sampling uniformity.

## New finite-horizon tool (16 November 2026)

For a fixed test horizon `T`, `prop:finitehorizonagecompression` removes arbitrary-age truncation uncertainty: initial global consecutive gaps capped at `T+1` give an exact identity-trajectory representative with maximum initial age `nc(T+1)`. All numerical ages then evolve normally. This permits rigorous finite certificates for richer abstractions or candidate couplings, while their state-space cost can be enormous. The missing generic step is still a quantitative label-bias contraction argument, not age boundedness alone.

`prop:c2iidrefreshbias` now rules out a freshness-conditioning shortcut directly under the adopted iid scheduler at deterministic time two; no random-permutation scheduler is needed for this negative result.

A further rigorous certificate route is available: `prop:finitehorizonfulltv` reduces the uniform full-state transposition coefficient at a chosen horizon to bounded initial ages. `cor:finiteantisymmetriccertificate` then converts a certified coefficient below one into iterated bias contraction. This finite family may be enormous; no efficient arbitrary-`n` enumeration or polynomial gap is asserted. Do not confuse a scalar query threshold (which only persists) with this operator contraction (which multiplies).

A full-state transposition certificate cannot contract in fewer than `n-1` events and needs `Omega(n log n)` events for a fixed constant factor (`prop:antisymmetriccouponlower`). This is compatible with polynomial work, but reinforces the distinction between full-overlay and direct-query contraction. See also [owner-frozen extinction obstructions](research/FROZEN-OWNER-EXTINCTION.md) before choosing a count-based potential or freezing both swapped owners.

## Conditional callback refinement (16 November 2026)

The full-shuffle callback now covers shared secondary vectors with coordinate-wise unit-width bands, not only identical vectors (`lem:fullbandcallback`). The [conditional proof](research/UNIT-WIDTH-CALLBACK.md) uses at most three macros and includes a non-dense `n=6,c=3` example. A possible next step is establishing these bands or extending the callback to arbitrary shared-anchor ages. Neither is proved here; the shared-identity requirement and `|I|<=n-c+1` endgame limitation remain.

The high-age-star coupon argument also establishes `Omega(n log n)` worst-case full-state mixing at fixed error (`cor:fullstatemixingcouponlower`). Thus this barrier applies to any full-state proof, while a faster single-query rate remains logically possible. It does not supply a matching upper bound.


## Capacity-three learned-target boundary service (16 November 2026)

**Symbolic working result, independently reviewed:** `lem:c3learnedcallback` gives finite owner boundary service through any specified subset of zero holders at exactly `c=ell=3`, without a shared-secondary or age-band assumption. `cor:c3zeroify` gives some nonholder gain when the owner caches a nonholder, and zeroification without decreasing endpoint holder count. This does not promise service to a prescribed nonholder or an age-uniform gadget duration. The proof is in [C3-LEARNED-TARGET-CALLBACK.md](research/C3-LEARNED-TARGET-CALLBACK.md); `verify_thesis_c3_learned_callback.py` corroborates exact finite transitions, not the unbounded-age argument. Full convergence additionally requires the separately audited outward-holder and extremal arguments.

## Arbitrary-population full capacity-three theorem (16 November 2026)

**Working proof integrated:** `thm:c3generaluniform` proves unique full-state stationarity, uniform geometric convergence, positive stationary availability, and limiting conditional uniform samples for **exactly `c=ell=3`, every `n>=4`**, with arbitrary finite nonnegative integer ages and initially underfull weakly connected caches under the adopted iid scheduler. The proof combines learned-target boundary service, zeroification, owner-directed emptying without circular outward closure, the new outward-gain gadgets and age potential, the incoming minimum-component contradiction, and the existing finite reset/common atom argument. Separate end-to-end and final-text audits are recorded in the research continuation. This is a mathematical working proof, not formal verification or external peer review.

At this earlier capacity-three stage, sparse larger capacities were still open; the subsequent all-capacity length-three theorem below supersedes that boundary. Higher lengths and polynomial mixing remain open. Earlier continuation entries describing capacity-three outward gain as open are superseded by this theorem. The [assembled proof](research/C3-GENERAL-CONVERGENCE.md), [outward argument](research/C3-OUTWARD-HOLDER-GAIN.md), and [terminal gadgets](research/FULL-SHUFFLE-TRIANGLE-GAIN.md) record the dependency chain and corrected MIN-age inequalities.

## All capacities at shuffle length three (16 November 2026)

**Working proof integrated:** `thm:threegeneraluniform` now covers every `n>=4` and `3<=c<=n-1` at fixed `ell=3`, with the adopted protected/MIN kernel, iid initiators, initially weak connectivity, and arbitrary finite integer ages. It proves unique full-state stationarity, uniform geometric convergence with implicit constants, positive stationary availability, and conditional uniform local sampling for every request size up to capacity. The arbitrary-capacity callback, empty-owner restoration, and fixed-identity lexicographic outward potential are linked to the lower-length residual normalization and finite-reset/common-atom argument. The [full assembly](research/LENGTH-THREE-GENERAL-CONVERGENCE.md) and [sparse outward proof](research/SPARSE-LENGTH-THREE-OUTWARD-GAIN.md) state the scope and necessary controlled reply choices.

This supersedes earlier continuation entries saying sparse length-three convergence remained open. Proper-capacity convergence at lengths four and above and polynomial/practical mixing bounds remain open. These are internally audited mathematical working proofs, not formal verification or external peer review.


## Parameterized shuffle induction (16 November 2026)

**CONDITIONAL, not arbitrary-length convergence.** `prop:shuffleinductionstructure` derives uniform cut contact and universal-anchor reduction at length L from lower-length common atoms and cut contact at L-1. `prop:shuffleinductionclosure` identifies two sufficient remaining obligations: boundary service through any subset of zero holders, with preterminal locality, persistent target and free terminal reply; and outward holder growth from an empty-owner zero-maximizing state. These obligations are established through length three, not for general L. `lem:generalownerterminalprefix` supplies an unconditional three-event restoration prefix at all L>=3, but its holder-terminal branch still needs boundary service to obtain a gain. `prop:longeroutwardcontrollercycle` gives a forced restricted-controller cycle for every allowed L>=4, so the length-three strict-potential proof cannot simply be reused. This is not a counterexample to the protocol.

See [the parameterized framework](research/PARAMETERIZED-SHUFFLE-INDUCTION.md) and [general restoration prefix](research/GENERAL-OWNER-TERMINAL-RESTORATION.md). The priority is resolving the reusable boundary-service and outward-growth mechanisms, not adding isolated length-four cases. No polynomial rate or general-length convergence is claimed.


## Arbitrary-length service and sampling alternatives: research-only continuation

The following independently reviewed **conditional research notes** are not new arbitrary-length convergence theorems and have not been promoted to manuscript claims:

- [All-younger owner service](research/ALL-YOUNGER-OWNER-SERVICE.md): under explicit pre/post residual-age hypotheses, a contact either makes the secondary target oldest or decreases owner head count. Owner-only passive-age stabilization does not extend to arbitrary cooperative preparation.
- [Shared-zero-secondary service](research/SHARED-ZERO-SECONDARY-SERVICE.md): a closed zero-holder region sharing one zero-age secondary supports an exact lower-length reduction. Preparing zero secondary ages is impossible from strictly positive copies while that secondary's owner is frozen, so this is not a generic accessibility proof.
- [Threshold-censored lower kernels](research/THRESHOLD-CENSORED-LOWER-KERNEL.md): the singleton-capacity threshold-clearing lemma is proved; higher-capacity searches are bounded diagnostics, including ten explicitly unresolved five-peer runs.
- [Even-class symmetry sampling](research/EVEN-CLASS-SYMMETRY-SAMPLING.md): for n>=5, invariance of every recurrent class under even relabellings suffices for deterministic-time one-ID sampling, without unique full-state stationarity. The proof handles cyclic phases and availability. Class invariance, or the sufficient bound of fewer than n recurrent classes, remains unproved. Under the same unproved class-invariance hypothesis, availability is automatic for every b<=min(c,floor(n/2)); larger b only needs one available state in each class, since availability propagates through phases.

These isolate possible reusable routes toward arbitrary lengths. The established unconditional convergence range is all capacities at lengths one through three, and all lengths at full capacity; general owner service, outward growth, and useful polynomial rates remain open.


### Shared positive-secondary internal reset

[The local positive-secondary reset](research/SHARED-POSITIVE-SECONDARY-RESET.md) supplies an all-length conditional construction that bounds internal ages while preserving a shared primary zero and arbitrary bounded secondary ages, with outside rows frozen. It uses the existing colored reset, not a lower-length convergence assumption. The probability claim is hitting a bounded internal-state set within a finite horizon, not fixed-time minorization or unrestricted-chain recurrence. Neither reaching this shared closed region nor serving the secondary target is proved.


### Closed-class occupancy inheritance

[Clipped-capacity inheritance](research/CLIPPED-CAPACITY-OCCUPANCY.md) shows that a closed class with maximum row size m<c has exactly the kernel of capacity m and length min(L,m). Canonical accessibility for that smaller kernel contradicts the bound via two legal growth events. With the currently established lengths one through three, every closed class at any L>=4 therefore attains some row of size at least four. Assuming the full lower-length induction package gives max occupancy at least L, and hence a full row when c=L. This is not full occupancy for every proper capacity, fixed-observer availability without symmetry, or arbitrary-length convergence.


### Frozen maximum-row erasure

[The frozen-row reduction](research/FROZEN-MAXIMUM-ROW-ERASURE.md) gives a finite reference-erasure path for a peer frozen at its own classwise maximum row size below capacity, assuming the lower-length first-contact/common-atom package. A fixed numerical reset bound and minimum-age raising replace an auxiliary recurrence argument. In a no-eviction class, this forces each peer's maximum row size to equal its degree in the fixed underlying graph. Combined with the still-unproved A_n class-invariance hypothesis, it yields full-cache availability and hence conditional uniform sampling for every allowed sample size. Neither class invariance nor arbitrary-length convergence is established. The minimum-age argument does not confuse an incremented cached descriptor with a fresh zero.


## Every length at full capacity; arbitrary-capacity overflow

**Internally audited working theorem:** `thm:fullcapacityalllengths` proves uniform canonical common-atom accessibility, unique full-state stationarity/convergence, and conditional uniform sampling for every 1<=L<=n-1 at capacity c=n-1. The outer length / inner population induction stays within full-capacity kernels. Frozen-source erasure makes the complement closed; a no-eviction graph argument makes it connected; normalization and one source contact create a universal zero anchor. See [the full proof record](research/FULL-CAPACITY-ALL-LENGTHS-CANDIDATE.md).

`cor:alllengthoverflow` couples any proper-capacity kernel with the full-capacity kernel until their first overflow. It gives uniform finite-horizon hitting of some full row, a geometric waiting tail for the next eviction, and infinitely many evictions almost surely, for every allowed length/capacity. Constants are implicit. This proves neither sampling uniformity nor unique stationarity at sparse capacities. It does not guarantee a full row at a prescribed observer. Every closed class nevertheless contains a full-row state, removing the additional availability hypothesis from the conditional even-class-symmetry sampling criterion. The general common-atom theorem now supplies uniqueness and class invariance; the coupling alone did not.
