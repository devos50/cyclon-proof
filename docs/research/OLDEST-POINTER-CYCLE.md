# Oldest-first two-head coalescence is not automatic

## Status and scope

**Exact counterexample to a stronger auxiliary conjecture.** A finite
oldest-first two-head pointer process need not coalesce. The example below
also embeds in the adopted protected/MIN CYCLON protocol with `n=7` and
`c=ell=3`. It is a prescribed infinite trajectory, not a positive-probability
infinite event under the iid scheduler, and does not refute convergence or
cooperative callback accessibility.

## Process and finite certificate

A root holds distinct heads `q:A,s:B`. Vertex `q` holds residual pointer
`r:C`. Selecting oldest head `q` requires `A>=B`. Unless `r=s` (coalescence),
the next root is `s:(B+1),r:C`, and q's pointer becomes `s:(B+1)`.
Other pointers remain unchanged. Missing or outside pointers count as
terminal progress in the callback interpretation.

Take five vertices `0,...,4` and initial data:

- Sorted root heads `(0,1)`, with ages `(1,1)`.
- Residual pointers `(1,2,3,4,0)`.
- Corresponding pointer ages `(0,0,1,1,1)`.

The inline 72-action fixture in
[`verify_oldest_pointer_cycle.py`](../../verification/mandatory-removal/verify_oldest_pointer_cycle.py)
specifies positions in the sorted current root heads. Every selected head
is oldest: 48 comparisons are strict and 24 are ties. No step coalesces.
After 72 steps the root labels and all pointer identities return to their
initial values, while **all seven ages increase by 12**. Every abstract
update commutes with adding a common constant to all ages, and all oldest
comparisons are invariant under that shift. Consequently the same action
sequence repeats forever, proving the counterexample without an infinite
simulation. No minimality of the number of vertices or period is claimed.

## Exact CYCLON embedding

Use owner `a=0`, secondary identity `p=1`, and map abstract vertex `v` to
peer `v+2`. The owner cache contains `p^0` and the two abstract heads.
Every mapped vertex has `{a^0,p^0,residual}`; the secondary peer is empty.
This is an allowed weakly connected initial state with full three-entry
caches except at p. Activate only the owner, using the fixture's oldest
partner. Full requests and replies are forced. The responder replaces its
old residual with the owner's retained head, and the owner takes the
responder's old residual. MIN merging keeps every secondary age at zero;
the fresh owner descriptor keeps every responder's owner age zero.

The checker compares the independent abstract update with the existing
`ActualThree` implementation after **each of 144 exchanges**, checks initial
connectivity, and verifies the exact affine return after both periods.
The selected head ages remain positive, so p never obstructs their oldest
status in any repeated period. This is a cycle modulo age translation,
not a finite-state periodic orbit of actual ages.

Run:

```sh
python3 -B verification/mandatory-removal/verify_oldest_pointer_cycle.py
```

## Why the high-age clearing alternative survives

The useful weaker fact is different: in any infinite noncoalescing
trajectory, the active residual ages eventually become arbitrarily large.
Here is the qualitative argument, which does not need oldest-first choices.
Let S be the vertices selected infinitely often. After the last selection
outside S, an outside-S root head would stay fixed. The other head then
walks through finitely many pointers, rewriting each visited pointer to
that fixed head; its first repeated vertex forces coalescence. Thus both
heads eventually lie in S. After every S vertex has been selected again,
all its residual pointers also lie in S.

The multiset consisting of the two root ages and all S-pointer ages is now
closed. Each step removes ages A and B and inserts two copies of B+1; the
old pointer age C merely moves to the root. Its minimum cannot decrease,
and no new copy of its current minimum can be created. Each minimum-age
pointer is eventually selected and moved to the root, where its copy
vanishes on the next step. Finitely many minimum copies therefore disappear
in finite time. The integer minimum tends to infinity.

In the conditional shared-secondary callback setting, secondary ages stay
bounded by their initial maximum M during a **pure owner-only phase**.
If that phase never makes progress, the preceding argument ensures a finite
time at which the forward closure R of the root heads is internal and all
its residual ages are at least M. Freeze the owner and activate its chosen
head Q repeatedly. On each first visit, the residual edge is an eligible
oldest choice; visited responders acquire a fresh pointer to Q. A repeated
vertex then returns Q, which is self-filtered, clearing Q's residual. This
takes at most `|R|` residual exchanges. The owner can then contact Q without
replenishing its second head. This argument permits additional legal
initiators; the counterexample forbids them by design.

This is a qualitative conditional route, not a polynomial time bound or
universal accessibility theorem. Interleaving other preparation exchanges
before the stopping test would require a separate invariant; the pure
owner-only multiset argument does not automatically apply to such paths.
