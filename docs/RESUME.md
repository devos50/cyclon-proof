# Resume this research

## General fixed-length working proof (16 November 2026)

The manuscript now contains `thm:allparametersuniform`, a working proof for every
`n>=2` and `1<=L<=c<=n-1` under the adopted iid protected/MIN mandatory-removal
kernel, initially weak connectivity, and arbitrary finite nonnegative integer ages.
It asserts a uniform common atom, unique full-state stationarity, uniform geometric
convergence with implicit constants, positive stationary availability, and limiting
conditional uniform ordered local samples. Two independent end-to-end internal audits of the theorem and actual
manuscript text have passed. This is not
external peer review, formal verification, or a polynomial/practical mixing bound.

The new route uses `lem:partialcolorsource`, `lem:generalsourcecreation`, and
`lem:generalsourceextension`. It bypasses the earlier general owner-service and
outward-growth obligations rather than proving those particular controllers work.
Historical conditional results and controller counterexamples below retain their
original scopes; statements that general convergence remained open describe the
previous checkpoint and are superseded by this working theorem.

Status updated on **16 November 2026**. This is a working mathematical draft; authorship, publication plans, and external review are not established here.

All described work is saved. This handoff does not imply an active background run or scheduled research continuation.

## Start here

1. Read [MODEL.md](MODEL.md) for the exact protocol and sampling rule.
2. Read [ROADMAP.md](ROADMAP.md) for result boundaries and priorities.
3. Use [paper/main.tex](../paper/main.tex) as the single mathematical source, including all proofs and bibliography.
4. Find results by stable TeX labels, because numbering and source lines may change.

The latest priorities are external mathematical review, proof simplification, and useful sampling rates; the general source-route theorem has passed independent internal audits. Do not resume isolated length-four casework as though qualitative convergence were still the current missing step.

## Completed draft scope

For the adopted mandatory-removal, received-protection, minimum-age protocol with independent uniform initiators:

- Lengths one and two have full convergence and conditional sampling proofs for every allowed network size and common cache capacity.
- Length three now has a full proof for every allowed population and capacity (`thm:threegeneraluniform`). The new general source theorem extends the working convergence claim to all larger lengths and capacities, with independent internal audits completed.
- Every allowed shuffle length now has full convergence at capacity c=n-1; arbitrary proper capacities additionally have uniform full-row hitting and repeated evictions.
- Every fixed shuffle length has finite-age recurrence and finitely many possible stationary regimes. This recurrence result alone does not settle sampling; the general common-atom theorem supplies the additional argument.

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

This supersedes earlier continuation entries saying sparse length-three convergence remained open. Proper-capacity convergence at lengths four and above and polynomial/practical mixing bounds remain open. These are internally audited mathematical working proofs, not formal verification or external peer review.


## Parameterized shuffle induction (16 November 2026)

**CONDITIONAL, not arbitrary-length convergence.** `prop:shuffleinductionstructure` derives uniform cut contact and universal-anchor reduction at length L from lower-length common atoms and cut contact at L-1. `prop:shuffleinductionclosure` identifies two sufficient remaining obligations: boundary service through any subset of zero holders, with preterminal locality, persistent target and free terminal reply; and outward holder growth from an empty-owner zero-maximizing state. These obligations are established through length three, not for general L. `lem:generalownerterminalprefix` supplies an unconditional three-event restoration prefix at all L>=3, but its holder-terminal branch still needs boundary service to obtain a gain. `prop:longeroutwardcontrollercycle` gives a forced restricted-controller cycle for every allowed L>=4, so the length-three strict-potential proof cannot simply be reused. This is not a counterexample to the protocol.

See [the parameterized framework](research/PARAMETERIZED-SHUFFLE-INDUCTION.md) and [general restoration prefix](research/GENERAL-OWNER-TERMINAL-RESTORATION.md). This historical route isolated reusable boundary-service and outward-growth mechanisms. The new source route bypasses those obligations; this conditional framework itself does not assert their resolution or a polynomial rate.


## Arbitrary-length service and sampling alternatives: research-only continuation

The following independently reviewed **conditional research notes** are not new arbitrary-length convergence theorems and have not been promoted to manuscript claims:

- [All-younger owner service](research/ALL-YOUNGER-OWNER-SERVICE.md): under explicit pre/post residual-age hypotheses, a contact either makes the secondary target oldest or decreases owner head count. Owner-only passive-age stabilization does not extend to arbitrary cooperative preparation.
- [Shared-zero-secondary service](research/SHARED-ZERO-SECONDARY-SERVICE.md): a closed zero-holder region sharing one zero-age secondary supports an exact lower-length reduction. Preparing zero secondary ages is impossible from strictly positive copies while that secondary's owner is frozen, so this is not a generic accessibility proof.
- [Threshold-censored lower kernels](research/THRESHOLD-CENSORED-LOWER-KERNEL.md): the singleton-capacity threshold-clearing lemma is proved; higher-capacity searches are bounded diagnostics, including ten explicitly unresolved five-peer runs.
- [Even-class symmetry sampling](research/EVEN-CLASS-SYMMETRY-SAMPLING.md): for n>=5, invariance of every recurrent class under even relabellings suffices for deterministic-time one-ID sampling, without unique full-state stationarity. The proof handles cyclic phases and availability. Class invariance, or the sufficient bound of fewer than n recurrent classes, remains unproved. Under the same unproved class-invariance hypothesis, availability is automatic for every b<=min(c,floor(n/2)); larger b only needs one available state in each class, since availability propagates through phases.

These isolate possible reusable routes toward arbitrary lengths. At that historical checkpoint the convergence range was all capacities at lengths one through three and all lengths at full capacity. The new general source theorem supersedes that range; the particular general owner-service/outward-growth controllers and useful polynomial rates remain unresolved.


### Shared positive-secondary internal reset

[The local positive-secondary reset](research/SHARED-POSITIVE-SECONDARY-RESET.md) supplies an all-length conditional construction that bounds internal ages while preserving a shared primary zero and arbitrary bounded secondary ages, with outside rows frozen. It uses the existing colored reset, not a lower-length convergence assumption. The probability claim is hitting a bounded internal-state set within a finite horizon, not fixed-time minorization or unrestricted-chain recurrence. Neither reaching this shared closed region nor serving the secondary target is proved.


### Closed-class occupancy inheritance

[Clipped-capacity inheritance](research/CLIPPED-CAPACITY-OCCUPANCY.md) shows that a closed class with maximum row size m<c has exactly the kernel of capacity m and length min(L,m). Canonical accessibility for that smaller kernel contradicts the bound via two legal growth events. With the currently established lengths one through three, every closed class at any L>=4 therefore attains some row of size at least four. Assuming the full lower-length induction package gives max occupancy at least L, and hence a full row when c=L. This is not full occupancy for every proper capacity, fixed-observer availability without symmetry, or arbitrary-length convergence.


### Frozen maximum-row erasure

[The frozen-row reduction](research/FROZEN-MAXIMUM-ROW-ERASURE.md) gives a finite reference-erasure path for a peer frozen at its own classwise maximum row size below capacity, assuming the lower-length first-contact/common-atom package. A fixed numerical reset bound and minimum-age raising replace an auxiliary recurrence argument. In a no-eviction class, this forces each peer's maximum row size to equal its degree in the fixed underlying graph. Combined with the still-unproved A_n class-invariance hypothesis, it yields full-cache availability and hence conditional uniform sampling for every allowed sample size. Neither class invariance nor arbitrary-length convergence is established. The minimum-age argument does not confuse an incremented cached descriptor with a fresh zero.


## Every length at full capacity; arbitrary-capacity overflow

**Internally audited working theorem:** `thm:fullcapacityalllengths` proves uniform canonical common-atom accessibility, unique full-state stationarity/convergence, and conditional uniform sampling for every 1<=L<=n-1 at capacity c=n-1. The outer length / inner population induction stays within full-capacity kernels. Frozen-source erasure makes the complement closed; a no-eviction graph argument makes it connected; normalization and one source contact create a universal zero anchor. See [the full proof record](research/FULL-CAPACITY-ALL-LENGTHS-CANDIDATE.md).

`cor:alllengthoverflow` couples any proper-capacity kernel with the full-capacity kernel until their first overflow. It gives uniform finite-horizon hitting of some full row, a geometric waiting tail for the next eviction, and infinitely many evictions almost surely, for every allowed length/capacity. Constants are implicit. This proves neither sampling uniformity nor unique stationarity at sparse capacities. It does not guarantee a full row at a prescribed observer. Every closed class nevertheless contains a full-row state, removing the additional availability hypothesis from the conditional even-class-symmetry sampling criterion. The new common-atom working theorem supplies uniqueness and hence class invariance; the overflow coupling alone did not establish it.


## Query-only uniformity is not one-step preserved

The [age-blind uniformity diagnostic](research/AGE-BLIND-UNIFORMITY-NOT-PRESERVED.md) gives an exact all-length example: complete caches produce initially uniform samples, but a unique oldest identity at an observer gives one-event conditional TV error b/[n(n-1)] for 1<=b<=n-2. This rules out a universally nonincreasing nonnegative query-only potential vanishing exactly at uniformity. It does not contradict eventual convergence or rule out age-aware/block arguments. The main sparse convergence problem remains open.
