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
