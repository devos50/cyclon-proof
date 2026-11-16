# General fixed-length convergence: source-route proof record

16 November 2026. **Internally audited working proof**, not external peer
review or formal verification. The authoritative statement and proof are
`thm:allparametersuniform` and its three preceding lemmas in
[paper/main.tex](../../paper/main.tex).

## Scope

Every `n>=2`, `1<=L<=c<=n-1`, initially weakly connected state with arbitrary
finite nonnegative integer ages, under the explicitly adopted iid-global-
initiator, protected/MIN, mandatory-partner-removal kernel. The result gives
unique full-state stationarity and uniform geometric convergence with implicit
constants. Ordered local samples at deterministic observation times are uniform
in stationarity, conditional on sufficient cache size, with positive stationary
availability. It does not assert independence between samples, availability one,
all CYCLON implementations/schedulers, or a useful/polynomial mixing rate.

## New mechanism

Freeze an owner q as an initiator, allowing its passive row to import old
entries. In the general colored controller choose a maximum-young-count old
holder outside q. The total young count F never decreases. On F plateaus, the
sum V of squared row-young counts does not increase, even when the responder
is q and holds old entries.

On a joint F,V plateau all young sets are fixed and every responder has
strictly more young entries than its initiator. Thus a responder outside q
must be entirely young: otherwise it contradicts maximal initiator choice.
In particular a row holding an old q copy cannot be passively replenished.
While that copy persists, its row has at most c initiations before losing it.
New q copies arise only as request extras at strictly higher young-count
levels. Their genealogies therefore have bounded depth and branching.

Contacts with q are consequently bounded on each plateau. Between them the
old weighted potential W decreases. Finitely many F,V plateaus give a uniform
colored q-extinction horizon H. Unlike the old full-capacity proof, this does
not require q's row to have bounded numerical ages or fixed identities.

The lower-length minimum-copy phases first raise every surviving q copy above
`(nc+1)H`, without initiating q. A pigeonhole gap among the current descriptor
ages then supplies an H-event numerical old/young separation. The partial
colored controller erases q. Its outgoing row is nonempty by passive protection
and preserved weak connectivity, even if the last copy disappears by eviction
rather than by an owner contact.

The already audited source construction normalizes complement components with
source neighbors ranked highest, normalizes the resulting closed full-capacity
core with q ranked least, and thereby joins the complement. Complement
normalization plus the two-event extension gives a universal zero anchor.
The lower-length anchor normalization reaches the prescribed canonical atom.

## Dependencies and uniformity

Outer induction is on length, carrying lower-length common atoms and first
contact; lengths 1–3 are established bases. Inner induction is on population
at a fixed length, simultaneously for every allowed capacity. Component
normalization uses smaller population or clipped smaller length. The core
normalization uses the independently proved full-capacity theorem.

The source paths are used as finite legal paths, not as an asserted useful or
age-independent source-hitting bound. The independent general finite-age reset
reaches a fixed finite family. Finite path selection and empty-root padding
then give the uniform common-atom minorization. Existing contraction and label
symmetry give the full-state and conditional-sampling conclusions.

## Audit and finite validation

Two independent reviewers audited the complete argument and actual manuscript
text. Additional independent audits checked the plateau genealogy and the
source/core extension. Precision corrections included closed versus open
singleton residual components, the ambient residual first-contact embedding,
and possible last-copy removal by eviction.

- New trajectory checker: 11,400 starts, 371,507 exact-kernel-matched exchanges,
  n=3..20, all allowed capacities/lengths at least two, ten reproducible seeds.
  Includes 17,599 frozen-owner contacts on F,V plateaus; maximum path 98.
- New exhaustive local F/V checker: 1,796,305 colored cache pairs and 7,310,428
  controller completions through n=7, including 137,634 frozen-owner cases
  where strict W descent cannot be used. Also 190 larger transfer checks.
- Source extension: 2,852 exact two-event paths and 1,407 core endpoint cases.
- Integrated prior/current regression suite: 52/52 passed, followed by the
  additional exhaustive local checker above. These are complementary checks,
  not formal or computer-assisted certificates of the arbitrary-size theorem.

Historical failures of particular owner-only, overlap, token, or outward
controllers remain valid diagnostics. The new proof bypasses those controllers;
it does not retroactively prove them correct.
