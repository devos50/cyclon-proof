# Partial results, unintegrated arguments, and superseded routes

**Historical checkpoint, superseded on 16 November 2026.** The general
working theorem `thm:allparametersuniform` now proves qualitative convergence
for every allowed fixed length, capacity, and population in the adopted kernel.
References below to missing accessibility or open length-four-and-higher
convergence describe earlier controller routes, not the current theorem.
Their specific conditional hypotheses and controller obstructions retain their
original scopes. See [the source-route record](research/GENERAL-SOURCE-CONVERGENCE.md).
The new result has independent internal audits, not external peer review or
formal verification; useful/polynomial mixing rates remain open.


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

## Owner-frozen extinction route: new obstructions

The [current research note](research/FROZEN-OWNER-EXTINCTION.md) separates first contact from extinction. Target-reference count can have positive drift even with a frozen owner and every target descriptor strictly oldest, including when the target has linearly many copies. Freezing both transposed owners can also make the symmetry set inaccessible from a connected state. These are exact obstructions to specific shortcuts, not lower bounds on ordinary extinction/mixing time or a rejection of adaptive coupling.

## Shared anchors with unit-width ages

The conditional full-shuffle callback is now proved for secondary ages in coordinate-wise pairs `{m_p,m_p+1}` (`lem:fullbandcallback`), with a three-macro bound. See [UNIT-WIDTH-CALLBACK.md](research/UNIT-WIDTH-CALLBACK.md). The hypotheses are still an accessibility gap: arbitrary states need not have the shared secondary identities, let alone the stated bands. Unrestricted shared-anchor ages and a generic zero-count gain remain open. The existing counting obstruction for the last missing zeros at `ell>=4` is unchanged.


## Capacity-three learned-target boundary service (16 November 2026)

**Symbolic working result, independently reviewed:** `lem:c3learnedcallback` gives finite owner boundary service through any specified subset of zero holders at exactly `c=ell=3`, without a shared-secondary or age-band assumption. `cor:c3zeroify` gives some nonholder gain when the owner caches a nonholder, and zeroification without decreasing endpoint holder count. This does not promise service to a prescribed nonholder or an age-uniform gadget duration. The proof is in [C3-LEARNED-TARGET-CALLBACK.md](research/C3-LEARNED-TARGET-CALLBACK.md); `verify_thesis_c3_learned_callback.py` corroborates exact finite transitions, not the unbounded-age argument. Full convergence additionally requires the separately audited outward-holder and extremal arguments.

## Arbitrary-population full capacity-three theorem (16 November 2026)

**Working proof integrated:** `thm:c3generaluniform` proves unique full-state stationarity, uniform geometric convergence, positive stationary availability, and limiting conditional uniform samples for **exactly `c=ell=3`, every `n>=4`**, with arbitrary finite nonnegative integer ages and initially underfull weakly connected caches under the adopted iid scheduler. The proof combines learned-target boundary service, zeroification, owner-directed emptying without circular outward closure, the new outward-gain gadgets and age potential, the incoming minimum-component contradiction, and the existing finite reset/common atom argument. Separate end-to-end and final-text audits are recorded in the research continuation. This is a mathematical working proof, not formal verification or external peer review.

At this earlier capacity-three stage, sparse larger capacities were still open; the subsequent all-capacity length-three theorem below supersedes that boundary. Higher lengths and polynomial mixing remain open. Earlier continuation entries describing capacity-three outward gain as open are superseded by this theorem. The [assembled proof](research/C3-GENERAL-CONVERGENCE.md), [outward argument](research/C3-OUTWARD-HOLDER-GAIN.md), and [terminal gadgets](research/FULL-SHUFFLE-TRIANGLE-GAIN.md) record the dependency chain and corrected MIN-age inequalities.

## All capacities at shuffle length three (16 November 2026)

**Working proof integrated:** `thm:threegeneraluniform` now covers every `n>=4` and `3<=c<=n-1` at fixed `ell=3`, with the adopted protected/MIN kernel, iid initiators, initially weak connectivity, and arbitrary finite integer ages. It proves unique full-state stationarity, uniform geometric convergence with implicit constants, positive stationary availability, and conditional uniform local sampling for every request size up to capacity. The arbitrary-capacity callback, empty-owner restoration, and fixed-identity lexicographic outward potential are linked to the lower-length residual normalization and finite-reset/common-atom argument. The [full assembly](research/LENGTH-THREE-GENERAL-CONVERGENCE.md) and [sparse outward proof](research/SPARSE-LENGTH-THREE-OUTWARD-GAIN.md) state the scope and necessary controlled reply choices.

This supersedes earlier continuation entries saying sparse length-three convergence remained open. Lengths four and above and polynomial/practical mixing bounds remain open. These are internally audited mathematical working proofs, not formal verification or external peer review.
