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
| $\ell=3,3\le c<n-2$ | General sampling theorem open | — |
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

The meaningful next convergence benchmark is $\ell=3$, $c=3$ or $c=4$, and arbitrary $n$. Capacity four offers a spare slot and may be the easier first target.

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

