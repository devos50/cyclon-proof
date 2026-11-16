# Verification guide

The main checks use Python 3.9 or later and its standard library. Keep assertions enabled. The optional `--numerical` mode of the recurrent mixing benchmark additionally needs NumPy; the curated runner never enables it.

```sh
python3 tools/run_checks.py --list
python3 tools/run_checks.py
python3 tools/run_checks.py --full
python3 tools/run_checks.py --check c2_three_peer
```

The default suite runs five focused checks. `--full` opts into all 26 curated checks for the current model, including earlier subcases. Some enumerate millions of local transitions or execute more than a million exchanges. The runner prints each result, continues after failures, and returns a nonzero exit status if any check fails. Use `--timeout SECONDS` to impose an optional limit on each child process.

The current model uses mandatory removal of the selected partner, protection of received descriptors, minimum-age duplicate merging, fixed common cache capacity and shuffle length, reliable atomic exchanges, static membership, and independent uniform global initiators. A controlled-path verifier prescribes outcomes that have positive probability in that model; it does **not** simulate an ordinary random execution or establish a useful random mixing rate by itself.

Finite controller checks corroborate the written arbitrary-size proofs. The three-peer antisymmetric certificate is different: an analytic exact projection reduces its stated three-peer theorem to a finite operator calculation. Diagnostics and checks of earlier protocol variants have separate status below.

## Focused default suite

| Runner name | Check | Default runner coverage |
|---|---|---|
| `c2_quantitative` | Quadratic controlled path to the common atom and availability gadgets | Reduced smoke coverage: `--max-n 10 --seeds 3 --availability-n 5` |
| `c2_ready` | Exact local cases for the ordinary ready-copy cut-contact drift | Full local enumeration: 14,260 cases |
| `c2_three_peer_order` | Exact time-zero arbitrary-age three-peer sampling certificate | Full 1306-state projection, 3918 numerical lifts, integer query powers through 56 events |
| `c2_three_peer` | Exact arbitrary-age three-peer conditional-sampling certificate | Full 487-state operator and 974 numerical lifts |
| `c2_refresh_obstructions` | Refresh, connected-history and old-lineage counterexamples | Exact rational certificates |
| `c2_age_projection_obstruction` | Failure of age capping plus global ranks as an exact projection | Exact four-peer two-event query comparison |

## Current-model inventory

All files in this table are under `verification/mandatory-removal/`. Run any one with `python3 verification/mandatory-removal/FILE.py`; default means no extra arguments. Counts are reproduced workload descriptions, not promises of elapsed time. The full runner adds `--zeroify` to the fast first-contact check; all other full commands use script defaults.

Dependency abbreviations: **A**=`verify_thesis_anchor.py`; **S**=`verify_singleton_general.py`; **C**=`verify_thesis_cooperative_owner.py`; **H**=`verify_thesis_half_dense.py`; **G**=`verify_thesis_general_two.py`; **R**=`verify_c2_recurrent_mixing.py`; **T**=`verify_thesis_c2_saturation.py`. These are sibling files, not packages to install. The standard library is used throughout this table.

| File / runner name | Model, checked result and limits | Sibling dependencies | Default workload |
|---|---|---|---|
| `verify_thesis_c2_quantitative.py` / `c2_quantitative` | Current (c=\ell=2): complete controlled paths with a quadratic event bound, arbitrary finite ages, probability bounds and availability gadgets; finite checks support the general written proof | A, T | 1,008 complete paths through (n=30); 351,100 exchanges; 1,728 availability states |
| `verify_c2_ready_drift.py` / `c2_ready` | Current (c=\ell=2): readiness-loss and transport cases behind the ordinary linear expected cut-contact theorem | A | 14,260 local cases, ages 0–3 |
| `verify_c2_three_peer_order_projection.py` / `c2_three_peer_order` | Current (n=3,c=ell=2): exact within-row order projection from time zero; conditional error <10^-6 for every t>=56; no arbitrary-n rate | R, indirectly A | 1306 states; 3918 corroborating lifts; exact integer powers through 56 |
| `verify_c2_three_peer_antisymmetric.py` / `c2_three_peer` | Current (n=3,c=\ell=2): exact positivity projection and antisymmetric contraction, including arbitrary-age burn-in; no arbitrary-(n) rate | R, indirectly A | 487 projected states; 974 unequal-age lifts; exact integer powers through 8 events |
| `verify_c2_recurrent_mixing.py` / `c2_recurrent_mixing` | Current (n=3,c=\ell=2): exact benchmark restricted to the recurrent class; optional NumPy diagnostics are not exact certificates | A | 75 recurrent states; 50 default time steps; optional `--numerical` |
| `verify_c2_refresh_counterexample.py` / `c2_refresh_obstructions` | Current (c=\ell=2): exact counterexamples to naive memory-erasure and refresh arguments; does not contradict convergence | G | Small exact rational examples |
| `verify_c2_age_projection_obstruction.py` / `c2_age_projection_obstruction` | Current (n=4,c=\ell=2): a cap-plus-rank projection gives identical summaries but query laws differing by (1/32); no impossibility claim for every possible projection | A | Small exact rational two-event laws |
| `verify_capacity_one.py` / `capacity_one` | Mandatory-removal (c=\ell=1) identity dynamics: tree closure, reversibility, uniform identity counts and swap words; duplicate policies do not alter this identity update | None | Connected identity states on (n=2,\ldots,6) |
| `verify_thesis_anchor.py` / `anchor` | Current $\ell=2$: exact MIN simulation of residual singleton algorithms, universal-anchor canonicalization and component merges; assumes an existing universal zero anchor | S, with its transition overridden by exact MIN | 576 starts; 1,829,148 actual exchanges; potentially substantial |
| `verify_thesis_c2_saturation.py` / `c2_saturation` | Current $c=\ell=2$: incoming-boundary, infection, source-gain and positive-copy gadgets under their stated hypotheses | A | 52,964 exhaustive states; 118,498 boundary witnesses; random and auxiliary checks |
| `verify_thesis_general_two.py` / `general_two` | Current $\ell=2$, arbitrary capacity: outward holder gain and plateau inequalities, conditional on the specified empty-owner/zero-holder setup | A, H | 20,136 starts through (n=30); 74,801 exchanges |
| `verify_thesis_two_reset.py` / `two_reset` | Current $\ell=2$: protected MIN age-gap reset; erases OLD color, not all initially YOUNG lineage information | None | 6,840 nonvacuous age-gap starts through (n=20) |
| `verify_thesis_general_local.py` / `general_local` | Current all-length reset: exhaustive colored one-step lexicographic inequalities, not the numerical age-gap or convergence theorem alone | None | 1,099,391 local pairs; 3,887,740 moves; 190 larger plateau cases; substantial |
| `verify_thesis_general_reset.py` / `general_reset` | Current all-length numerical age-gap reset controller; does not establish uniqueness for every shuffle length | None | 11,400 starts; 373,413 controlled exchanges |
| `verify_thesis_first_contact.py` / `first_contact` | Current $\ell=2$: frozen-boundary minimum-copy reduction and reset-or-contact; stops at contact before inspecting the frozen responder | A | 28,036 small exhaustive states plus 1,365 random and 455 high-age starts |
| `verify_thesis_first_contact_fast.py` / `first_contact_fast` | Current $\ell=2$: polynomial controlled holder-only first contact; `--zeroify` adds terminal refresh and owner callback | None | 9,100 cases, 21,507 exchanges; `--zeroify`: 9,100 cases, 32,008 exchanges |
| `verify_thesis_half_dense.py` / `half_dense` | Current $\ell=2,c\ge3,n\le2c$: earlier outward-gain subcase, superseded in scope by the arbitrary-capacity result | A | 10,777 starts; 36,204 exchanges |
| `verify_thesis_dense.py` / `dense` | Current $\ell=2,c\ge n-2$: earlier no-extra-eviction, outward and root-contact subcases | A | 43,338 local transitions; 468 root cases; 2,120 random witnesses |
| `verify_thesis_holder_routing.py` / `holder_routing` | Current $3\le\ell\le c$: high-anchor final routing stage only; does not check preceding minimum raising or full convergence | None | 20,475 starts; 54,280 exchanges |
| `verify_thesis_owner_cycle.py` / `owner_cycle` | Current larger shuffles: exact owner-only service obstruction and cooperative repair; auxiliary frozen-scheduler obstruction, not iid-convergence counterexample | None | Full/proper-shuffle invariant branches through length 30 |
| `verify_thesis_cooperative_owner.py` / `cooperative_owner` | Current $\ell=3$: conditional shared-zero-anchor callback, both closed and arbitrary residual sets; assumes the anchors | S, with exact MIN residual override | Two suites of 15,120 starts; 647,065 + 186,403 exchanges |
| `verify_thesis_cooperative_general.py` / `cooperative_general` | Current arbitrary $\ell\ge3$: conditional callback with $\ell-2$ shared secondary zero anchors; does not bootstrap those anchors | C | 660 starts; 4,774 exchanges |
| `verify_thesis_cooperative_vector.py` / `cooperative_vector` | Current full shuffles: conditional callback with a common positive-age vector; outside preference in oldest ties is essential to the controller | C | 540 starts; 1,421 exchanges |
| `verify_thesis_proper_owner.py` / `proper_owner` | Current proper shuffles: target-retaining service when every old-zero holder has at least $\ell+1$ entries; conditional and potentially age-dependent | C | 1,716 starts; 7,734 exchanges, bounded numerical age gaps |
| `verify_thesis_underfull_bootstrap.py` / `underfull_bootstrap` | Current proper shuffles: local underfull-zero gain and a two-exchange near-complete bootstrap; excludes the unresolved empty missing-peer premise | C | 33,520 local cases; 5,720 near-complete starts |
| `verify_thesis_dense_three_owner.py` / `dense_three_owner` | Current $\ell=3,c\ge n-2$ callback, plus a conditional all-capacity last-missing-zero subcase at $c\ge4$; no general bootstrap claim | C | 18,400 dense and 27,200 near-complete starts; about 468,000 exchanges |
| `verify_thesis_dense_three_boundary.py` / `dense_three_boundary` | Current $n=5,c=\ell=3$: final singleton-responder component-minimum gadget, assuming the preceding extremal setup | C | 144 exact boundary cases |

## Earlier protocol variants and supporting engines

These files are preserved for provenance and dependencies. They are excluded from both curated suites. Their successful execution would not certify the adopted protected-MIN protocol.

| File | Actual scope/status | Command/dependencies and cost |
|---|---|---|
| `verification/verify.py` | Mixed early checks: retention-model capacity-one classes, periodic counterexample, duplicate-discard frozen twins and other local certificates | `python3 verification/verify.py`; standard library; bounded enumerations through six peers |
| `mandatory-removal/verify_singleton_general.py` | Standalone singleton controller uses duplicate discard and keeps resident duplicate ages. **Keep this sibling file**: A and C subclass its controller and override its transition with exact MIN | Run directly only to reproduce that earlier model. Standard library; 1,102 exhaustive and 264 random starts |
| `mandatory-removal/verify_lineage_erasure.py` | Earlier mandatory-removal, duplicate-discard lineage controller; received duplicates can remain eligible victims | Standard library; 3,300 starts; CLI `--max-n`, `--seeds`, `--max-age` |
| `mandatory-removal/verify_capacity_two_reset.py` | Earlier $c=\ell=2$ age reset using the preceding duplicate-discard engine | Depends on `verify_lineage_erasure.py`; 2,240 default starts |
| `mandatory-removal/verify_shuffle_two_reset.py` | Earlier arbitrary-capacity $\ell=2$ duplicate-discard reset, rather than the later MIN controller | Standard library; 6,840 default starts |
| `mandatory-removal/verify_large_shuffle_obstruction.py` | Conditional nonconvergence for the earlier duplicate-discard/eligible-duplicate-victim model. **Does not refute the adopted model** | Standard library; algebraic constructions checked across 39 parameter choices |
| `mandatory-removal/cyclon3.py` | Small exploratory three-peer transition/BFS helper with duplicate discard; no certification entry point | Standard library; also imported by `verify_reset.py`; direct BFS can be expensive |
| `mandatory-removal/verify_reset.py` | Earlier three-peer duplicate-discard reset controller | Depends on `cyclon3.py`; fixed exhaustive numerical checks; excluded from curated execution |

The historical record `verification/records/retention-original.json` was produced by the early `verify.py` and is a legacy snapshot. A single JSON `passed` field does not identify the protocol or prove every theorem in this repository.

## Archived research scripts and results

Temporary research files are supporting material unless explicitly promoted into the curated inventory. This includes finite searches, provisional potentials, owner-frozen games, old protocol counterexamples, and Monte Carlo diagnostics. Keep their original names and provenance together with any associated Markdown notes and JSON results. Do not infer correctness from a filename containing `verify` or a note containing a proposed theorem.

Recent supporting material includes the exact minimum-old-age counterexample and its checker, label-drift obstructions, young-component notes, and finite Monte Carlo hub diagnostics. The latter do not certify stationarity, a mixing rate, or absence of a rare adverse family.

## Relocation and dependencies

The 34 original Python files have no hardcoded user-directory or temporary-directory references in executable code. Their current sibling imports are relocatable if `verification/mandatory-removal/` stays together. Maintained usage examples use the new repository paths. Do not move `verify_singleton_general.py` out of the sibling directory without adjusting both A and C imports.

Some archived temporary experiments do need path repair in their copied versions:

- `cyclon-c2-montecarlo.py`, `cyclon_c2_n3_exact_local.py`, `search_cyclon_frontier.py`, and `search_cyclon_underfull_empty.py` insert the original simulator's absolute verification directory into `sys.path`.
- `cyclon_c2_rand.py`, `cyclon_periodic.py`, `cyclon_color_game.py`, `cyclon_color_game_monotone.py`, `cyclon_color_game_stats.py`, and `cyclon_identity_scc.py` load a sibling experiment through an absolute temporary path and `exec`.
- `cyclon_zero_certificate.py` loads `cyclon_frozen_search.py` through an absolute temporary path and writes `cyclon_zero_best.json` there.
- `cyclon_c2_uniform_erasure_verify.py` dynamically loads the earlier lineage engine through the working-directory-relative path `docs/peer-sampling-convergence/mandatory-removal/verify_lineage_erasure.py`. This also needs attention when reproducing that historical experiment.

The exploratory archive is kept verbatim, including historical paths. Those paths are not dependencies of the curated checks; running an archived experiment directly can require replacing them with paths resolved relative to `__file__`. Record such edits and keep exploratory programs outside `tools/run_checks.py --full`.

## Constant transient availability proof (16 November 2026)

`lem:c2constanttransientavailability` and `cor:c2linearconditioningfactor` are symbolic consequences of the existing arbitrary-population contact theorem, scheduler thinning, and protected passive reception. They are not finite certificates. The supporting readiness checker was rerun: `python3 -B verification/mandatory-removal/verify_c2_ready_drift.py` passed 14,260 endpoint cases. These finite checks corroborate the contact proof; they do not independently establish the arbitrary-`n` availability statement.

## Finite-horizon compression checker

`python3 -B verification/mandatory-removal/verify_finite_horizon_age_compression.py` (suite name `finite_horizon_compression`) checks 110,000 integer offset comparisons and 52,741 coupled legal branches from 48 initial configurations. It covers every `1<=ell<=c<=min(3,n-1)` for `2<=n<=5` at horizon two or three; its independent generic transition implementation is also checked against the existing four-peer kernel on the gap-obstruction states. These finite cases corroborate `prop:finitehorizonagecompression`; the arbitrary-size claim is supplied by the written provenance argument. No mixing inequality is certified by this script.

The refreshed `verify_c2_refresh_counterexample.py` additionally enumerates all ordinary iid two-event paths for `prop:c2iidrefreshbias`, asserting refreshing mass `2/9`, conditional availability `1/2`, and deterministic conditional output. The proof also explicitly lists the only two refreshing histories; no simulation or schedule conditioning is hidden in the enumeration.

The three-peer order-projection checker now also compares all 1,306 transition rows against an independent three-peer-specific implementation that does not call the shared `outcomes`/`Actual` kernel. This regression and the 3,918 numerical-lift corroborations pass. The symbolic projection argument, not the lift samples, establishes arbitrary-initial-age coverage.

For `prop:finitehorizonfulltv`, the compression checker additionally constructs a common map on all source-age-plus-offset values, verifies that it is well-defined and injective, and checks full aged successors against that map across the enumerated branches. This strengthens the previous identity-only regression. The finite runs remain corroboration of a symbolic reduction, not a computed arbitrary-population contraction certificate.

## Additional contraction-route checks

- `verify_c2_frozen_owner_obstruction.py` checks 114 single-hub and 320 multi-hub next-event laws, including unchanged surviving target ages; a separate 60-branch check corroborates the frozen-pair invariant. These support the [symbolic research note](research/FROZEN-OWNER-EXTINCTION.md), not an extinction-time bound.
- `verify_antisymmetric_coupon_lower.py` compares 95 exact star/transposed terminal-law pairs for `n=3..5`, every allowed capacity/length, and `T=0..4`. It checks equality of the separating-event probability with the coupon tail and the second-moment lower bound. The all-size claim is proved symbolically in `prop:antisymmetriccouponlower`.

## Unit-width full-shuffle callback checks

`python3 -B verification/mandatory-removal/verify_thesis_cooperative_bands.py` passed 6600 seeded exact controlled paths for `n=4..14`, every `3<=c=ell<=n-1`, including coordinate-specific lower ages up to `10^6`. The run contains 19145 legal exchanges, 2307 independently evaluated singleton-residual updates, and a longest path of 11 exchanges. Forty-four starts require three nonfinishing macros; two explicit `n=6,c=3` regressions also exercise the third-macro cases. The script checks exact owner-vector resets, all original zero copies, legal oldest choices, and the path bound. This is finite corroboration of the symbolic conditional lemma `lem:fullbandcallback`, not exhaustive all-state enumeration or generic convergence.

`cor:fullstatemixingcouponlower` is a symbolic extension of the coupon-star construction. Its additional step uses continuity of a probability measure on decreasing high-age events. The existing exact coupon checker corroborates the star event only; no simulation or finite stationary-age cutoff is used in the proof.

## Learned-target continuation and exact coalescence obstruction (16 November 2026)

The new learned-target checker covers 5,100 seeded capacity-three starts with arbitrary tested ages up to one million, genuine nonholders, arbitrary chosen subsets of zero holders, and targets that may themselves already hold a zero outside that subset. Its 5,918 exact controlled exchanges include 40 head-count increases charged to newly learned targets and 48 legal clearings. This is corroboration of the qualitative symbolic proof, not an exhaustive state-space or mixing certificate. The scalar one-head checker adds 2,400 starts and 5,684 exchanges.

The [oldest-pointer counterexample](research/OLDEST-POINTER-CYCLE.md) is different: a finite exact affine-cycle certificate proves that owner-only oldest-first coalescence is false. Its checker compares all 144 exchanges in two periods against the adopted kernel and proves repetition by translation invariance. The callback proof uses high-age divergence followed by a separate clearing intervention, not the disproved coalescence claim.


## Capacity-three learned-target boundary service (16 November 2026)

**Symbolic working result, independently reviewed:** `lem:c3learnedcallback` gives finite owner boundary service through any specified subset of zero holders at exactly `c=ell=3`, without a shared-secondary or age-band assumption. `cor:c3zeroify` gives some nonholder gain when the owner caches a nonholder, and zeroification without decreasing endpoint holder count. This does not promise service to a prescribed nonholder or an age-uniform gadget duration. The proof is in [C3-LEARNED-TARGET-CALLBACK.md](research/C3-LEARNED-TARGET-CALLBACK.md); `verify_thesis_c3_learned_callback.py` corroborates exact finite transitions, not the unbounded-age argument. Full convergence additionally requires the separately audited outward-holder and extremal arguments.

## Capacity-three arbitrary-population continuation checks

The triangle checker passes 2,120 ordered-age identity cases, 9,273 varied full-shuffle cases, and 600 holder-restoration prefixes. The outward controller passes 5,100 starts and 11,970 exchanges, including 629 migration steps with exact global maximum-age potential assertions, 371 callback-based terminals, and 120 zero-holder transfer branches. An explicit MIN-lowered tie regression guards against replacing received-age inequalities by false equalities. The dimension-independent boundary checker passes 16,650 local configurations for `n=4..40`: 11,250 zero gains, 4,662 outward-edge alternatives, and 738 strict component decreases. These finite checks corroborate local identities only. The arbitrary-size theorem rests on its symbolic proof and separate dependency audits, not these counts.

## General length-three continuation

The arbitrary-capacity callback checker passes 6,000 starts (19,483 exchanges, maximum 93) plus seven hard multi-residual regressions. The owner-terminal checker passes 8,360 starts (27,932 exchanges), including 1,182 safe forced replacements. The fixed-identity sparse outward checker passes 10,500 starts (21,257 exchanges), including 104 disjoint migrations and explicit known-B protection and underfull-migration regressions. It asserts strict lexicographic progress on every zero-holder contact and nondecrease on each migration, along with the exact per-identity age maxima inequalities. These finite counts corroborate the symbolic proof, not arbitrary-size convergence by themselves. The [audit record](research/LENGTH-THREE-AUDIT.md) distinguishes the mathematical argument from the tests.


## Parameterized induction validation

The general restoration checker passes 12,012 prefixes / 36,036 exchanges for n=4..14 and all allowed lengths/capacities, including 840 safe-victim branches and 4,290 extra-request branches. It does not invoke an unproved general callback. The restricted-controller cycle checker passes 1,140 embeddings / 22,800 exchanges for n=5..22, checking exact two-event repetition, legal forced packets, weak connectivity and constant identity potential. The complete suite passes **42/42 checks** in 259.38 seconds. These tests corroborate finite local identities, not the conditional induction's open hypotheses. Separate end-to-end mathematical review checked the actual manuscript, lower-length dependencies, full-capacity incoming swap, locality/free-reply interface, finite-reset probability quantifiers, and cycle embedding.


## Scoped positive-secondary research checks

The all-younger checker tests 28,000 legal transitions: 9,212 meet its explicit postcondition and pass, while 18,788 are excluded rather than counted as successes. The shared-zero-secondary embedding checker compares 52,920 transitions against an independent lower-kernel implementation and checks 1,456 normalized owner-head deletions. Both are curated full-suite checks. The separate threshold-censored diagnostic is not a convergence certificate: it records boundary exits without clipping, finds bounded witnesses for the stated small families, and explicitly reports ten unresolved five-peer searches stopped by the 10,000-state budget. Its analytic singleton threshold lemma is independent of these finite search results.

The phase-symmetry sampling reduction is symbolic, not numerically inferred. Its group-action, periodic-chain, availability, and entrance-mixture steps were independently audited. Neither finite regime count nor relabelling equivariance alone proves individual-class invariance.

Final scoped validation: **44/44 curated checks passed in 260.41 seconds**;
repository checks passed with 454 local links, 145 TeX labels, and 56
maintained Python files. A separate end-to-end audit accepted all four
research notes within their explicit hypotheses and search limits.
The manuscript mathematical source was unchanged in this increment.


## Shared positive-secondary reset and availability refinement

The reserved-positive-anchor checker passes 2,025 cases / 6,505 exact full-kernel events, including unequal positive secondary ages, singleton residual systems, all colored-potential decreases, owner interleaving, final residual reset, and frozen outside rows. Two independent symbolic reviews checked the actual note, unpadded old-only simulation, gap bounds, and hitting-within-horizon probability scope.

The even-class symmetry note now proves automatic availability for b<=min(c,floor(n/2)) under its unproved class-invariance hypothesis. If maximum row size m<c, no class transition can evict; the undirected graph is consequently monotone and constant, and even-permutation invariance forces it complete. Arc counting yields the stated occupancy bound. A non-observer initiation propagates availability to the next cyclic phase. This is a symbolic conditional argument, not a numerical finding or a proof of class invariance.


The completed positive-reset suite passed **45/45 checks in 278.92 seconds**. The subsequently added clipped-capacity growth check separately passes all 2,002 cases, including m=1 and every tested allowed shuffle length. The current registry consequently has 46 checks; this record does not describe a single 46-check full-suite run. Actual-text review verified exact transition-law inheritance and the two-event witness. The manuscript source remains unchanged.


## Frozen-row minimum-age bookkeeping

The local frozen-target checker passes 10,560 exact events, divided evenly among internal minimum preservation, higher-age boundary replies, absent-target boundary replies, and owner-terminal deletion. The target never initiates; the global minimum cannot decrease. The checker does not certify classwise maximum occupancy or lower-length accessibility. Those hypotheses and the fixed-bound finite-erasure argument are handled by a separate actual-text proof audit.


## Full-capacity all-length induction and overflow coupling

Three independent end-to-end reviews accepted the full-capacity induction; final manuscript transcription audits checked both `thm:fullcapacityalllengths` and `cor:alllengthoverflow`. The complement checker compares 11,400 exact transitions with an independent reduced kernel, plus 840 universal-zero source contacts and 840 cross-component edge insertions. The overflow checker passes 4,368 finite runs / 26,019 coupled exchanges: 21,752 identical pre-overflow steps and 4,267 first-overflow events; 101 runs reached their finite observation limit without an overflow. Those censored runs are not violations of the symbolic tail theorem, and the tests do not estimate its implicit constants.

The mathematical proof, not these finite counts, establishes the induction and uniform geometric overflow tail. Proper-capacity stationary uniqueness, sampling convergence without class symmetry, and polynomial mixing remain open.

Final validation for the full-capacity theorem increment: **49/49 curated
checks passed in 267.19 seconds**. Repository checks passed with 472 local
links, 147 TeX labels and 61 maintained Python files; the generated index
contains 126 declarations and 54 headings. Two final TeX draft-mode
passes completed with no undefined references or LaTeX errors. No new
rendered PDF is claimed. Three independent end-to-end proof reviews and
two final manuscript transcription reviews passed within the stated
model and scope.


## Transient age-blind uniformity obstruction

`verify_age_blind_uniformity_transient.py` enumerates 17,942 exact packet outcomes for n=3..8 and every allowed shuffle length at c=n-1, then checks rational sample laws for every b. The symbolic proof in [the note](research/AGE-BLIND-UNIFORMITY-NOT-PRESERVED.md) establishes the unrestricted parameter statement. This is an obstruction to universal one-step uniformity preservation, not to eventual convergence. The new checker and repository/index checks were rerun for this increment; the existing full-suite result above is historical, not a newly rerun 50-check suite.
