# Resume this research

Status updated on **16 November 2026**. This is a working mathematical draft; authorship, publication plans, and external review are not established here.

All described work is saved. This handoff does not imply an active background run or scheduled research continuation.

## Start here

1. Read [MODEL.md](MODEL.md) for the exact protocol and sampling rule.
2. Read [ROADMAP.md](ROADMAP.md) for result boundaries and priorities.
3. Use [paper/main.tex](../paper/main.tex) as the single mathematical source, including all proofs and bibliography.
4. Find results by stable TeX labels, because numbering and source lines may change.

The latest research priority is a **parameterized proof for arbitrary shuffle lengths**, rather than repeating separate length-by-length arguments. The conditional induction now isolates owner boundary service and outward holder growth as the remaining obligations. Length four is a diagnostic case, not the final target. Useful sampling rates remain open and secondary.

## Completed draft scope

For the adopted mandatory-removal, received-protection, minimum-age protocol with independent uniform initiators:

- Lengths one and two have full convergence and conditional sampling proofs for every allowed network size and common cache capacity.
- Length three now has a full proof for every allowed population and capacity (`thm:threegeneraluniform`). Lengths four and above remain open.
- Every fixed shuffle length has finite-age recurrence and finitely many possible stationary regimes. This alone does not settle sampling in the open cases.

“Proved” here refers to the current draft arguments and stated certificates, rather than external publication or peer review.

## Quantitative progress

For $c=\ell=2$, arbitrary $n$:
$$
T_n=16n^2,\qquad \Gamma_n=(4n)^{-T_n}.
$$
A controlled witness gives full-state error at most $(1-\Gamma_n)^{\lfloor t/T_n\rfloor}$, hence a pessimistic $\exp(O(n^2\log n))\log(1/\varepsilon)$ bound. This is not polynomial mixing.

Ordinary executions additionally satisfy:

- Expected first cut crossing at most $7n$ global events, with a tail halving every $14n$ events.
- Temporal connectivity within $O(n^2+n\log(1/\varepsilon))$ events with high probability.
- Fresh self emission by all peers within $O(n\log(n/\varepsilon))$ events with high probability.

The readiness proof counts full caches $\{r^A,s^B\}$ with $A\ge B$. For readiness count $R>0$, crossing probability is at least $R/(2n)$; readiness falls by at most one, with probability at most $2R/n$. The potential
$$
\Psi(R)=n\bigl(2+5(4/5)^R\bigr),
$$
set to zero after crossing, has conditional drift at most $-1$. This proves the $7n$ bound directly.

These communication guarantees do not establish a sampling rate.

## Where contraction work stopped

**prop:c2localcouplingtarget** reduces local uniformity to contraction between query laws from $x$ and $\sigma_{ab}x$, fixing observer $i$. Include the unavailable output $\bot$. The difference equals the output-probability difference for target labels $a,b$.

A proved symmetry-set coupling also reduces the task to hitting $F_\sigma=\{z:\sigma z=z\}$. No polynomial hitting bound is available.

**A polynomial local-contraction theorem for arbitrary $n$ remains open.**

A completed special case is available for **three peers, arbitrary finite initial ages**:

- **New:** local zero/positive flags plus the order/equality of the two positive ages within each row give an exact **1306-state projection from time zero**.
- Exact integer query powers certify error below `10^-6` at **every time at least 56 events**, improving the older 216-event sufficient horizon. At 55 events the worst error is still above `10^-6`.
- See `prop:c2threeorderprojection`, `prop:c2three56sample`, and `verify_c2_three_peer_order_projection.py`. This remains an `n=3` result, not arbitrary-network polynomial mixing.

The earlier general-epsilon certificate remains valid:

- After burn-in, each cache has at most one positive-age entry.
- Zero/positive flags form an exact 487-state Markov projection.
- Integer arithmetic certifies eight-event antisymmetric contraction $34447/69984<1/2$ and four-event availability at least $5/9$.
- A sufficient sampling horizon is
  $$
  \left\lceil\frac{\log(9/\varepsilon)}{\log(3/2)}\right\rceil
  +8\left\lceil\log_2(3/\varepsilon)\right\rceil.
  $$
  At $\varepsilon=10^{-6}$, this is 216 global events.

Find **prop:c2threepositivity** and **prop:c2threeordinarysample**. The separate 75-state exact benchmark covers recurrent starts only and must not replace the all-initial-age certificate.

Four peers can produce two positive entries in one cache, so positivity flags are insufficient. Capped ages plus all global age ranks also fail as an exact query projection (**prop:c2caprankobstruction**). This rules out that particular projection, not every possible abstraction.

## Reproduce the latest checks

Run from the repository root with Python 3 and assertions enabled:

~~~sh
python3 verification/mandatory-removal/verify_thesis_c2_quantitative.py
python3 verification/mandatory-removal/verify_c2_ready_drift.py
python3 verification/mandatory-removal/verify_c2_refresh_counterexample.py
python3 verification/mandatory-removal/verify_c2_three_peer_antisymmetric.py
python3 verification/mandatory-removal/verify_c2_three_peer_order_projection.py
python3 verification/mandatory-removal/verify_c2_age_projection_obstruction.py
~~~

These scripts use the standard library and sibling helpers.

The readiness checker covers 14,260 endpoint cases supporting the symbolic structural proof. The three-peer certificate instead exhausts an analytically justified exact projection, using integer powers. Do not silently truncate unrestricted ages.

The refreshing checker verifies a three-peer star example:

- All initial descriptors are replaced by young ones, yet the conditional output is $3/7,4/7$.
- Conditioning on every peer actually initiating a successful exchange still gives output $3/5,2/5$, availability $5/8$, and conditioning-event probability $2/3$.
- OLD-copy count can have positive expected drift.

Therefore refreshing and communication alone cannot close the sampling proof.

## Next session

Pursue a coupling or richer query-sufficient projection controlling **label bias**, with the three-peer integer certificate as a concrete model. Use readiness as a tool, rather than claiming the missing sampling bridge is complete.

For the separate general-convergence task, prioritize length four with fixed small capacities and arbitrary $n$. All length-three capacities are now covered by `thm:threegeneraluniform`; no polynomial rate follows.

Lean formalization is deferred at the user's request. Do not begin it until the proof work is ready and the user returns to that task.


## Arbitrary-population availability refinement (16 November 2026)

`lem:c2constanttransientavailability` now gives `alpha_x,i(t) >= exp(-8)/8` for every `t>=8(n-1)` at `c=ell=2`, uniformly over arbitrary finite initial ages. This yields the linear-in-`n` conditioning factor `4 exp(8) (n-2)` in `cor:c2linearconditioningfactor`, an alternative to the earlier quadratic factor. Its numerical constant is pessimistic. The missing task remains contraction of label bias; this result is not a generic mixing proof.

## Generic finite-horizon progress (16 November 2026)

`prop:finitehorizonagecompression` now gives an exact all-size, all-length reduction: for horizon `T`, cap **successive global initial-age gaps**, anchored at zero, at `T+1`. Every initial state has a representative with maximum age `nc(T+1)` and exactly the same cache-identity trajectory law through `T`. The proof tracks provenance plus at most `T` increments, preserving comparisons and MIN ties. This is initial compression, not repeated truncation or a fixed Markov projection.

`cor:finitehorizoncertification` consequently allows finite exact certificates covering all initial ages at fixed parameters and horizon. The state family is huge; no polynomial rate or generic contraction is established. The checker is `verification/mandatory-removal/verify_finite_horizon_age_compression.py`.

A strengthened shortcut counterexample is now `prop:c2iidrefreshbias`: at deterministic time two under the actual iid scheduler, conditioning on complete refreshing and observer availability yields a deterministic, maximally biased two-label sample. The corresponding exact enumeration was added to the existing refreshing checker.

These continuation results do not replace the existing arbitrary-network convergence theorems for lengths one and two. The open targets remain a useful polynomial sampling rate as membership grows, length-four and general higher-length convergence.

`prop:finitehorizonfulltv` now permits exact bounded-initial-age checks of the **full-state antisymmetric** contraction coefficient, not just query errors. The injective age map is common across both compared starts. `cor:finiteantisymmetriccertificate` explains why such a uniform coefficient can be iterated without repeating compression. A practical certificate or symbolic polynomial bound for growing populations remains missing.

The full-state finite-certificate route has a proved coupon-collector limitation (`prop:antisymmetriccouponlower`): no strict contraction before `n-1` events, and a fixed constant contraction factor requires `Omega(n log n)` events. A high-age in-star separates the full laws; this is not the same as a local-query lower bound. The [owner-frozen research note](research/FROZEN-OWNER-EXTINCTION.md) also rules out positive age-only copy potentials and unconditional frozen-pair accessibility as shortcuts.

## Additional conditional callback progress

`lem:fullbandcallback` now permits shared secondary ages to differ by one at full shuffle `ell=c>=3`; exact equality across holders is unnecessary. Three preparation/owner macros suffice, rather than the common-vector lemma's two. The [research note](research/UNIT-WIDTH-CALLBACK.md) includes the proof and two `n=6,c=3` regressions. Its checker passed 6600 seeded configurations. This is conditional progress only: obtaining shared identities and narrow age bands remains open, as does the higher-length last-zero endgame.

`cor:fullstatemixingcouponlower` now gives a genuine worst-case full-state mixing lower bound, not just a restriction on an antisymmetric proof strategy: at fixed error it is `Omega(n log n)`. This uses arbitrary finite initial ages in the worst-case supremum and does not transfer to age-blind local sampling.


## Capacity-three learned-target boundary service (16 November 2026)

**Symbolic working result, independently reviewed:** `lem:c3learnedcallback` gives finite owner boundary service through any specified subset of zero holders at exactly `c=ell=3`, without a shared-secondary or age-band assumption. `cor:c3zeroify` gives some nonholder gain when the owner caches a nonholder, and zeroification without decreasing endpoint holder count. This does not promise service to a prescribed nonholder or an age-uniform gadget duration. The proof is in [C3-LEARNED-TARGET-CALLBACK.md](research/C3-LEARNED-TARGET-CALLBACK.md); `verify_thesis_c3_learned_callback.py` corroborates exact finite transitions, not the unbounded-age argument. Full convergence additionally requires the separately audited outward-holder and extremal arguments.

## Arbitrary-population full capacity-three theorem (16 November 2026)

**Working proof integrated:** `thm:c3generaluniform` proves unique full-state stationarity, uniform geometric convergence, positive stationary availability, and limiting conditional uniform samples for **exactly `c=ell=3`, every `n>=4`**, with arbitrary finite nonnegative integer ages and initially underfull weakly connected caches under the adopted iid scheduler. The proof combines learned-target boundary service, zeroification, owner-directed emptying without circular outward closure, the new outward-gain gadgets and age potential, the incoming minimum-component contradiction, and the existing finite reset/common atom argument. Separate end-to-end and final-text audits are recorded in the research continuation. This is a mathematical working proof, not formal verification or external peer review.

At this earlier capacity-three stage, sparse larger capacities were still open; the subsequent all-capacity length-three theorem below supersedes that boundary. Higher lengths and polynomial mixing remain open. Earlier continuation entries describing capacity-three outward gain as open are superseded by this theorem. The [assembled proof](research/C3-GENERAL-CONVERGENCE.md), [outward argument](research/C3-OUTWARD-HOLDER-GAIN.md), and [terminal gadgets](research/FULL-SHUFFLE-TRIANGLE-GAIN.md) record the dependency chain and corrected MIN-age inequalities.

## All capacities at shuffle length three (16 November 2026)

**Working proof integrated:** `thm:threegeneraluniform` now covers every `n>=4` and `3<=c<=n-1` at fixed `ell=3`, with the adopted protected/MIN kernel, iid initiators, initially weak connectivity, and arbitrary finite integer ages. It proves unique full-state stationarity, uniform geometric convergence with implicit constants, positive stationary availability, and conditional uniform local sampling for every request size up to capacity. The arbitrary-capacity callback, empty-owner restoration, and fixed-identity lexicographic outward potential are linked to the lower-length residual normalization and finite-reset/common-atom argument. The [full assembly](research/LENGTH-THREE-GENERAL-CONVERGENCE.md) and [sparse outward proof](research/SPARSE-LENGTH-THREE-OUTWARD-GAIN.md) state the scope and necessary controlled reply choices.

This supersedes earlier continuation entries saying sparse length-three convergence remained open. Lengths four and above and polynomial/practical mixing bounds remain open. These are internally audited mathematical working proofs, not formal verification or external peer review.


## Parameterized shuffle induction (16 November 2026)

**CONDITIONAL, not arbitrary-length convergence.** `prop:shuffleinductionstructure` derives uniform cut contact and universal-anchor reduction at length L from lower-length common atoms and cut contact at L-1. `prop:shuffleinductionclosure` identifies two sufficient remaining obligations: boundary service through any subset of zero holders, with preterminal locality, persistent target and free terminal reply; and outward holder growth from an empty-owner zero-maximizing state. These obligations are established through length three, not for general L. `lem:generalownerterminalprefix` supplies an unconditional three-event restoration prefix at all L>=3, but its holder-terminal branch still needs boundary service to obtain a gain. `prop:longeroutwardcontrollercycle` gives a forced restricted-controller cycle for every allowed L>=4, so the length-three strict-potential proof cannot simply be reused. This is not a counterexample to the protocol.

See [the parameterized framework](research/PARAMETERIZED-SHUFFLE-INDUCTION.md) and [general restoration prefix](research/GENERAL-OWNER-TERMINAL-RESTORATION.md). The priority is resolving the reusable boundary-service and outward-growth mechanisms, not adding isolated length-four cases. No polynomial rate or general-length convergence is claimed.
