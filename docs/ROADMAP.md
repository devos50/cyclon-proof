# Research roadmap

This is a working research record, not a publication claim. The manuscript is [paper/main.tex](../paper/main.tex), and the fixed target is summarized in [MODEL.md](MODEL.md). Authorship, submission plans, and external review status are not set here.

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
| $\ell=3,4\le c<n-2$ | General sampling theorem open | — |
| Fixed $\ell\ge4$ | General sampling theorem open | — |
| Every fixed allowed $\ell\ge2$ | Finite-age recurrence, finitely many stationary regimes, continuous-time convergence to a possibly initial-dependent mixture, stationary age tails | thm:thesisgeneralreset, cor:thesisgeneralregimes |

The paper retains older results for other conventions. Their scope must not be silently combined with the adopted model.

## Priority 1: useful sampling rates for small fixed caches

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

Readiness and source coverage provide quantitative communication tools. The missing step is contraction of label bias.

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

## Priority 2: longer shuffles with small caches

The next convergence benchmark is $\ell=3$, $c=4$, and arbitrary $n$. The full $c=\ell=3$ case is now covered by `thm:c3generaluniform`; its two-residual-head argument does not automatically extend to larger caches.

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
- The nearly full length-three theorem does not cover fixed small caches as $n$ grows.
- Counterexamples for retention, unprotected victims, or periodic schedules do not refute the adopted model.

The arbitrary-network polynomial sampling bound and the arbitrary-shuffle convergence theorem remain open. No completion date is established.


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

The constants are qualitative. Sparse capacities `4<=c<n-2` at length three, general higher lengths, and polynomial mixing remain open. Earlier continuation entries describing capacity-three outward gain as open are superseded by this theorem. The [assembled proof](research/C3-GENERAL-CONVERGENCE.md), [outward argument](research/C3-OUTWARD-HOLDER-GAIN.md), and [terminal gadgets](research/FULL-SHUFFLE-TRIANGLE-GAIN.md) record the dependency chain and corrected MIN-age inequalities.
