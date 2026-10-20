# Partial results, unintegrated arguments, and superseded routes

Use this guide before treating a recovered note as a current theorem. The [results registry](RESULTS.md) describes what the manuscript currently claims; the [archive catalog](ARCHIVE-INDEX.md) lists every saved artifact. A note may contain a valid conditional lemma while its proposed global conclusion remains open.

## Longer shuffles: substantial local tools, missing accessibility

The manuscript includes universal-zero-anchor reductions, holder-only length-three first contact, shared-zero-anchor callbacks, common-age-vector full-shuffle callbacks, proper-shuffle large-cache service, and nearly complete zero-set endgames. Their precise hypotheses and labels are in [RESULTS.md](RESULTS.md#higher-length-building-blocks-and-conditional-progress).

The unresolved issue is reaching those hypotheses or obtaining a strict endpoint increase in the zero-holder count from every connected state. Callback composition alone is not a general proof. Shared-anchor count restrictions leave additional endgame gaps for longer shuffles. Prioritize fixed small capacities, rather than extending only the nearly-full-cache regime.

Relevant archived note families:

- `cyclon-min-ell3-*`, `cyclon-min-shared-anchors-*`: cooperative callbacks.
- `cyclon-min-dense-ell3-*`: dense length-three completion and its boundary endgame, integrated in the manuscript under its density assumptions.
- `cyclon-min-zero-rich-*` and `cyclon-min-proper-large-zero-source-exploration.md`: conditional occupancy/bootstrap work.

## Unintegrated quantitative outward-gain strengthening

The saved notes propose a uniform controlled horizon for the arbitrary-capacity length-two outward-holder gain. The later young-age-sum argument proposes a polynomial horizon of the form `(nc+2)^3+n+c+2`. It uses a controlled trajectory and a sum of ages on constant-young-count plateaux.

This strengthening was discussed and internally audited in temporary notes, but is **not integrated as the current manuscript theorem or a general random mixing estimate**. Reconcile its hypotheses, time indexing, strict-event count, and checker evidence before promotion. The earlier maximum-young-age construction gives a larger, different bound.

Start with:

- [Young-age sum construction](../archive/notes/cyclon-outward-young-age-sum-audit.md).
- [Independent sum audit](../archive/notes/cyclon-outward-young-sum-audit.md).
- [Earlier maximum-age construction](../archive/notes/cyclon-outward-young-age-uniformity.md).
- [Constructive-stage audit](../archive/notes/cyclon-general-two-constructive-stage-audit.md).

Even a polynomial controlled-path length still gives a pessimistic prescribed-history probability. It does not establish polynomial ordinary mixing.

## Direct label-bias mixing: current open problem

The manuscript contains a local pairwise-label reduction, transient availability bound, and symmetry-set coupling. A uniform polynomial contraction or symmetry-set hitting-time bound remains unproved for arbitrary network size.

The special three-peer certificate is complete within its explicitly stated computer-assisted scope. Positivity, absolute-age caps, and current age ranks do not by themselves provide the required general projection.

The following failures are useful constraints on future attempts:

- [Label-drift and fixed-weight Hamming obstacles](../archive/notes/cyclon-c2-label-drift-obstructions.md).
- [Minimum-old-age multiplicity counterexample](../archive/notes/cyclon-minimum-old-counterexample.md).
- [Young components and their limitations](../archive/notes/cyclon-young-components.md). Its older `O(n^3)` communication estimate is superseded by the manuscript's readiness theorem.
- The maintained refresh and age-projection counterexamples are listed in [VERIFICATION.md](VERIFICATION.md).

## Superseded quantitative versions

Some archived capacity-two notes describe cubic or quartic controlled horizons, or an `O(n^2 log n)` temporal-connectivity bound. The current manuscript uses `T_n=16n^2`, expected cut contact `7n`, and high-probability temporal connectivity `O(n^2+n log(1/epsilon))`. Read current labels `thm:c2explicitmix`, `thm:c2readycontact`, and `cor:c2readytemporal`.

The archived 75-state three-peer script is superseded by its maintained counterpart for reproducibility. Its recurrent-start scope remains distinct from the 487-state arbitrary-initial-age certificate.

## Empirical diagnostics

[Hub/age diagnostic summary](../archive/notes/cyclon-c2-montecarlo-summary.md) and [its exploratory script](../archive/experiments/cyclon-c2-montecarlo.py) record finite simulations. These do not prove a rate, stationary law, or absence of rare adverse initial states. The raw script retains its original import path for provenance; it is not part of the portable maintained suite.

## Other protocol conventions

Early frozen states, periodic counterexamples, unprotected-victim failures, and duplicate-discard lineage results describe their own completions. Several are complete negative results for those variants; they do not automatically apply to the protected/MIN target. Preserve them, but read [MODEL.md](MODEL.md) before combining them with a positive argument.
