# Proof dependencies and reading routes

Reconciled **20 October 2026**. Main source: [paper/main.tex](../paper/main.tex). Labels below are stable TeX search keys, not theorem numbers. Status and exact scopes are in [RESULTS.md](RESULTS.md).

All “proved” nodes refer to working-paper proofs, not peer review or formal verification. A finite checker ordinarily supports a proof; the three-peer 487-state contraction explicitly uses an exhaustive exact finite certificate as part of its proof.

## Fast reading routes

- **Understand the protocol first:** `sec:target`, then `lem:receiveprotect` and `prop:thesisunion`.
- **Strongest practical qualitative theorem:** `thm:thesisgeneraltwo` (`ell=2`, any allowed `c,n`), with the predecessor construction summarized below.
- **Explicit small-cache quantitative theorem:** `thm:c2explicitmix`, then `prop:c2availabilityquant` and `cor:c2samplemixquant`. It is a quadratic witness and exponential mixing bound.
- **Actual random-execution progress:** `thm:c2readycontact`, `cor:c2readytemporal`, `cor:c2successfulsourcecover`.
- **Current fast-mixing target:** `lem:c2transientavailability`, `prop:c2localcouplingtarget`, `lem:c2symmetrycoupling`.
- **A completed small finite version of that target:** `prop:c2threepositivity` and `prop:c2threeordinarysample`; then `prop:c2caprankobstruction` for why simple age projections fail beyond it.
- **Generic length-three/higher proof gap:** `thm:threefirstcontact`, `prop:threezeroanchor`, `prop:zeroexpansioncriterion`; read the conditional callbacks and their counting limit before trying to compose them.

## Shared logical infrastructure

```text
Exact algorithm / assumptions (sec:target)
  + protected merge feasibility (lem:receiveprotect)
  -> lossless knowledge-union / weak connectivity (prop:thesisunion)

Uniform common-atom minorization at a self-loop atom
  -> unique stationary full-state law + uniform geometric TV (lem:atom)
  + label equivariance + positive availability
  -> conditional local uniform samples (thm:stationary)

Uniform finite-age reset alone
  -> finitely many stationary regimes + continuous-time mixture convergence
  DOES NOT -> one regime or uniform samples
```

`H(V,c)` is the labelled zero-age canonical state, with the final label empty and earlier labels caching up to the `c` greatest later labels. An empty canonical root supplies a no-op for padding controlled paths to one common time. A **finite reset family** is different from a **single common atom**.

## Singleton foundation

| Node | Main dependencies | What it supplies |
|---|---|---|
| `thm:mandatoryone` | Capacity-one identity moves, cycle reduction, age clearing, tree move connectivity | All-`n` common atom and explicit stationary rooted-tree law at `c=ell=1`. |
| `lem:source`, `lem:extend`, `thm:generalone` | Source clearing, source separation, reserved callback, induction on population | Canonical atom for arbitrary capacity at `ell=1`, with explicit recursive time bound. |
| `thm:thesisone` | The preceding constructive invariants survive minimum-age duplicate handling | Singleton convergence for the adopted kernel. Do not identify its full age law with the no-refresh law. |

Checker reading: [verify_capacity_one.py](../verification/mandatory-removal/verify_capacity_one.py), [verify_singleton_general.py](../verification/mandatory-removal/verify_singleton_general.py).

## General age recurrence, independently of uniqueness

```text
lem:generalcolor (strict lexicographic young/old potential)
  -> thm:thesisgeneralreset (uniform finite family F_B for every fixed ell>=2)
  -> cor:thesisgeneralregimes
       finitely many closed regimes
       continuous-time convergence to an initial-dependent mixture
       exponential stationary age tails
```

The potential is `(nc-F, sum f_i^2, sum o_i ell^(c-f_i))`. A finite initial-age gap makes all old descriptors older than all young ones for the controlled horizon. The resulting constants do not depend on initial age magnitudes. These results handle recurrence, not the remaining generic stationary-class/symmetry question.

Checker: [verify_thesis_general_reset.py](../verification/mandatory-removal/verify_thesis_general_reset.py).

## Full shuffle-length-two proof

### Anchors and contact

- `lem:anchorreduction`: reserving a universal age-zero anchor in requests/replies simulates the lower `(c-1,ell-1)` kernel on residual components.
- `prop:anchorcanonical`: at `ell=2`, the lower singleton construction empties the owner, normalizes residual components, merges roots by a four-exchange gadget, and reaches any prescribed labelled atom.
- `prop:anyanchor`: a universally cached identity with arbitrary ages can be refreshed to a universal zero anchor.
- `thm:firstcontact`: minimum-age raising plus holder routing gives a uniform first-contact path across any cut at `ell=2`.
- `prop:rootreachability`: repeated first contact expands a prescribed peer's directed reachable set in a **controlled construction**. This is not monotonicity of its reachable set under every random execution.

### Capacity two

```text
lem:c2sourcegain
  -> lem:c2extremal (maximum fresh-copy states)

lem:c2infection (four exchanges, empty owner, outward zero-holder edge)
  + residual singleton component normalization
  + extremal zero-count / minimum component-count argument
  -> universal zero anchor in every closed class
  + prop:anchorcanonical
  -> all closed classes reach the same labelled H(V,2)
  + general finite reset / finite path selection / atom padding
  -> thm:thesisc2
  + thm:stationary
  -> conditional uniform samples for b=1,2
```

The later `thm:c2explicitmix` is a more direct quantitative construction. It replaces class extrema with finite progress and therefore does not need the general reset to remove an initial-age dependence.

### Arbitrary capacity at length two

```text
thm:firstcontact + owner cached-target service
  -> prop:zeroify (increase zeros without decreasing endpoint holder count)
  -> cor:maxholders (class maximum of zero count bounds ALL holders)

lem:generalownerservice
  -> empty-owner maximizing states

lem:generaloutwardgain
  tracked current holder + permanently passive old zero holders
  bounded nondecreasing young count
  numerical-age budget excludes infinite constant-count migration plateaux
  -> no outward holder-to-nonholder edge at an extremum

incoming first contact + residual singleton root normalization
  -> one more zero if any nonholders remain (c>=3)
  -> universal zero anchor
  + prop:anchorcanonical + general reset + lem:atom + thm:stationary
  -> thm:thesisgeneraltwo
```

`thm:thesishalfdense` and `thm:thesisdense` are earlier special-case proofs. The general outward lemma removes their capacity/population restrictions. Do not restore a density restriction when citing the final length-two theorem.

Checkers: [verify_thesis_c2_saturation.py](../verification/mandatory-removal/verify_thesis_c2_saturation.py), [verify_thesis_general_two.py](../verification/mandatory-removal/verify_thesis_general_two.py), [verify_thesis_first_contact.py](../verification/mandatory-removal/verify_thesis_first_contact.py).

## Quantitative capacity-two branch

```text
c2 residual source-only clearing (at most n events)
  + cached-target owner service (at most n+2)
  + stopped clearing / immediate owner repair
  + four-exchange infection
  + singleton component-decrease steps
  -> one strict zero-count gain in at most 5n+12 events

positive-copy gain <=n+4
  + at most n-1 endpoint zero-count gains
  + O(n^2) final residual canonicalization
  -> thm:c2explicitmix: controlled horizon 16n^2
  -> common-atom probability (4n)^(-16n^2)
  -> exp(O(n^2 log n)) full-state mixing upper bound
```

Temporary loss of a zero is allowed. The repaired **macro endpoint count** must strictly increase; holder identities need not form an increasing set. A polynomial number of controlled exchanges does not make their prescribed-history probability polynomial.

- `prop:c2availabilityquant`: stationary label symmetry + connectedness yields a one-entry availability lower bound; a two-event cache-filling argument yields the two-entry lower bound.
- `cor:c2samplemixquant`: full-state TV plus those availability bounds gives the explicit conditional sample horizons.
- `prop:c2samplelower`: an initially unknown leaf cannot be contacted before it initiates; gives an `Omega(n)` baseline.

Checker: [verify_thesis_c2_quantitative.py](../verification/mandatory-removal/verify_thesis_c2_quantitative.py).

## Ordinary random histories and the unresolved mixing bridge

```text
holder count across a fixed cut cannot decrease before crossing (c=2)
  + readiness transfers / losses charged to at most 2R initiator clocks
  + drift of Psi(R)=n(2+5(4/5)^R)
  -> thm:c2readycontact: E[first cut contact]<=7n, geometric block tail
  -> cor:c2readytemporal: connected interaction graph in expected O(n^2)
  -> cor:c2successfulsourcecover: all peers emit fresh selves quickly

lem:younginteractioncomponents
  -> young connectivity is exactly cumulative interaction connectivity
```

**Missing arrow:** none of those statements implies uniform labels. Exact finite examples show that even all descriptors becoming young can leave the returned identifier biased.

The direct sampling route is:

```text
lem:c2transientavailability: alpha_x,i(t)>=1/(20n) for t>=2n
  + equivariance under swapping target labels a,b
  -> prop:c2localcouplingtarget
       conditional error <=10n(n-2)*beta_x,i(t)

PROVE uniform polynomial-scale contraction of beta
  -> polynomial one-ID sampling bound (OPEN for arbitrary n)
```

`lem:c2symmetrycoupling` offers a sufficient meeting mechanism: run a process and its relabelled copy until the state is fixed by that transposition, then couple identically. A polynomial hitting bound for that symmetry set is **not known**. Equal observer cache identity sets would already suffice for query coupling; a full-state meeting is stronger than necessary.

Checkers: [verify_c2_ready_drift.py](../verification/mandatory-removal/verify_c2_ready_drift.py), [verify_c2_refresh_counterexample.py](../verification/mandatory-removal/verify_c2_refresh_counterexample.py).

## Three-peer antisymmetric certificate

```text
n=3 structural fact:
  active cache after an exchange has <=1 entry
  passive cache has a protected fresh age-zero entry
  -> every updated cache has <=1 positive-age entry, permanently
  + coupon-cover bound 3*(2/3)^m
  -> prop:c2threepositivity: exact 487-state zero/positive projection

exact transition matrix P=A/6, A integer
  + exact relabelling equivariance
  + max_z TV(P^8(z,.),P^8(sigma z,.))=34447/69984<1/2
  + min availability after 4 events=5/9
  -> antisymmetric observables contract by 1/2 per 8 events
  + burn-in event and conditional availability
  -> prop:c2threeordinarysample
       all arbitrary-age starts; O(log(1/epsilon)) one-ID bound
```

This proof does not require mixing the entire numerical-age process. The actual positive ages need not become one; the projection of their signs is sufficient here. The 75-state recurrent-start benchmark is a separate calculation and is not the scope-reduction proof.

At four peers, one exchange can leave two positive entries at the active cache. `prop:c2caprankobstruction` further rules out absolute-age capping plus global ranks as a query-sufficient projection from arbitrary-age starts. A richer abstraction retaining relevant differences is still possible; no general impossibility theorem is asserted.

Checkers: [verify_c2_three_peer_antisymmetric.py](../verification/mandatory-removal/verify_c2_three_peer_antisymmetric.py), [verify_c2_recurrent_mixing.py](../verification/mandatory-removal/verify_c2_recurrent_mixing.py), [verify_c2_age_projection_obstruction.py](../verification/mandatory-removal/verify_c2_age_projection_obstruction.py).

## Length three and higher

```text
complete lower-length-two theorem
  -> thm:threefirstcontact (all c,n at ell=3)
  -> prop:threezeroanchor (universal zero anchor suffices)

near-full no-extra-eviction + cooperative owner repair
  -> lem:dense3callback
  -> cor:dense3zeroify
  + extremal outward closure / residual component argument
  -> universal zero anchor at c>=n-2
  + prop:threezeroanchor + reset / common-atom / symmetry
  -> thm:dense3uniform
  -> cor:densefourstructure (first contact + anchor-to-atom only)
```

The dense length-three theorem does not settle fixed capacities 3 or 4 with large `n`. Its length-four consequence does not show that a universal anchor is accessible.

### Conditional ingredients are not a complete generic proof

| Ingredient | Depends on | Does not supply |
|---|---|---|
| `lem:largezerocallback` | Proper shuffle, zero-holder occupancy at least `ell+1`, retained target | Reaching that occupancy from arbitrary underfull states. |
| `lem:threecooperativecallback` | `ell-2` additional shared zero anchors | Generic reachability of shared anchors; last `ell-3` missing zeros at `ell>=4`. |
| `lem:fullpositivecallback` | Full shuffle and a common age vector on `c-2` shared entries | Generic synchronization or the final counting-obstructed stage. |
| `prop:nearcomplete3` | Length three, capacity at least four, only one missing zero, owner caches that target | Reaching this near-complete state from arbitrary starts. |
| `lem:underfullzeroreply`, `lem:emptytargetthree` | Specific local underfull/empty-target configurations | Universal access to these local configurations. |
| `prop:owneronlyobstruction` | A legal family with a cached nonholder inaccessible under owner-only initiation | Any counterexample under the original all-peer iid scheduler. |

### Exact generic induction obligation

`prop:zeroexpansioncriterion` isolates a sufficient route:

1. For **every** connected state at a remaining length and every identity `a` with `Z_a<n-1`, prove finite positive-probability access to a strictly larger **endpoint** `Z_a`.
2. Repeat at most `n-1` times to get a universal zero anchor.
3. Reserve that anchor and invoke already established lower-length common-atom constructions on residual components.
4. Empty the owner, merge roots, and normalize to one labelled atom.
5. Use the general finite reset to make finite path selection uniform over arbitrary initial ages; pad at the atom; apply `lem:atom` and `thm:stationary`.

For `ell=3`, all lower-length premises are available, but the small-cache zero-expansion step is still missing. For a fully generic theorem, this obligation must be established successively over all larger lengths, including the shared-anchor counting endgame.

## Variants and negative results: separate branches

`thm:periodic` concerns periodic phases, not independent uniform initiators. `thm:twins` concerns retention without duplicate refresh. `thm:largerobstruction` and `cor:strongobstruction` concern a replacement completion that does not protect all received identities. `prop:availability` concerns unconditional request availability. None is a contradiction to the adopted conditional-sampling theorems.

`thm:protectedmixture` uses an independent positive probability of singleton shuffles, so a run of singleton events inherits the singleton common atom. The adopted MIN extension uses the same domination idea. This is a complete **modified variable-length** protocol theorem, not the missing fixed-length result.

## Claims that must not be inferred

- Finite age recurrence or cut crossing does not prove unique stationarity.
- Initial-lineage erasure, fresh-source coverage, or young connectivity does not prove uniform labels.
- An existence proof for a controlled path does not bound its typical waiting time by its length.
- The exact three-peer certificate gives no arbitrary-`n` polynomial rate.
- Capping absolute ages and retaining ranks fails, but that is not an impossibility theorem for every finite projection.
- Callback lemmas with shared descriptors do not prove their hypotheses are reachable.
- Full-state geometric convergence need not have a practical rate, and conditional uniformity does not imply independence.

## Time-zero three-peer refinement (16 November 2026)

`prop:c2threeorderprojection` uses the three-peer exchange geometry directly: the active cache has at most one identity and the passive cache contains fresh zero after every update. Within-row positive-age order therefore gives an exact projection without burn-in (1306 connected states). `prop:c2three56sample` combines that projection with exact integer query powers and positivity propagation, proving error below `10^-6` at every `t>=56`. It does not depend on numerical lift corroborations or imply an arbitrary-network rate. The prior 487-state general-epsilon certificate remains valid.

## Constant transient availability (16 November 2026)

`thm:c2readycontact` plus protected fresh-self reception and the independent uniform scheduler implies `lem:c2constanttransientavailability`: delete the empty observer's no-op activations, bound the outside-event first-fill mean by `7(n-1)`, then condition an `8(n-1)`-event block on no observer activation. Together with `prop:c2localcouplingtarget`, this gives `cor:c2linearconditioningfactor`. This branch does not depend on three-peer finite projections or provide label-bias contraction.

## Generic finite-horizon reduction (16 November 2026)

The all-length protocol uses ages only through increments, copies, oldest comparisons, fresh zero, and minimum merges. `prop:finitehorizonagecompression` uses bounded lineage offsets to preserve every relevant comparison after compressing initial gaps. It implies `cor:finitehorizoncertification` without needing the recurrence theorem or a mixing assumption. It does not yield a time-homogeneous projection, polynomial enumeration complexity, or the missing generic sampling bound.

`prop:c2iidrefreshbias` is an independent two-event counterexample under the adopted iid scheduler. It only uses forced exchanges from a three-peer star and does not depend on convergence, finite projections, or the cut-contact theorem.

`prop:finitehorizonagecompression` preserves equality and ordering of all source-age-plus-offset pairs, including across different histories. This gives the common injective reachable-age map in `prop:finitehorizonfulltv`. Equivariance then supplies `cor:finiteantisymmetriccertificate`; for `c=ell=2`, combine it with `cor:c2linearconditioningfactor` for a conditional sampling horizon. These are proved reductions, not an achieved generic contraction coefficient.

`prop:antisymmetriccouponlower` uses only the adopted mandatory partner deletion, fresh-self-only identity introduction, bounded per-event age increments, and the iid scheduler. It supplies a full-state coefficient lower bound for all shuffle lengths, independent of the convergence theorems. It does not imply the same lower bound for the local query observable.

## Unit-width secondary-anchor callback

`lem:fullbandcallback` extends the mechanism of `lem:fullpositivecallback`: full-shuffle reserved anchors leave a singleton residual; coordinate updates `min(u+1,v)` preserve each unit-width band; the owner resets exactly to the responder vector; the two nonsecondary owner heads permit a three-macro termination argument. It needs no density assumption or probabilistic mixing theorem. The checker corroborates these deterministic legal paths. Shared-anchor accessibility and the larger-length endgame do not follow.

`prop:antisymmetriccouponlower` supplies the exact high-age separating event. Letting its threshold tend to infinity under any fixed stationary law gives `cor:fullstatemixingcouponlower`; finite ages imply that stationary event probabilities vanish. This extension is symbolic and does not require a stationary tail rate, uniqueness in unproved regimes, or a new finite computation.


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

`cor:alllengthoverflow` couples any proper-capacity kernel with the full-capacity kernel until their first overflow. It gives uniform finite-horizon hitting of some full row, a geometric waiting tail for the next eviction, and infinitely many evictions almost surely, for every allowed length/capacity. Constants are implicit. This proves neither sampling uniformity nor unique stationarity at sparse capacities. It does not guarantee a full row at a prescribed observer. Every closed class nevertheless contains a full-row state, removing the additional availability hypothesis from the conditional even-class-symmetry sampling criterion. Class invariance itself remains open.
