# Cooperative callback with unit-width secondary age bands

Working conditional lemma, 16 November 2026. This broadens the common-age-vector lemma `lem:fullpositivecallback` in the manuscript. It does **not** establish that its shared-anchor hypotheses are accessible from arbitrary states, or close the generic convergence theorem.

## Statement

Use the adopted protected/MIN protocol at full shuffle `ell=c>=3`. Fix owner `a` and let `I={q != a: a^0 in C_q}`. Suppose a set `P` of `c-2` secondary identities is cached by `a`. For each `p in P`, fix an integer `m_p>=0`. Assume:

1. Every `q in I` contains `a^0` and every `p in P` at age in `{m_p,m_p+1}`.
2. The owner's copy of each `p` has age at least `m_p`.

Then a finite legal controlled path increases `Z_a` by one, preserves every original zero throughout, and never decreases `N_a`. At most three preparation-and-owner macros followed by one owner exchange suffice, with at most `3(|I|+1)+1` exchanges in total. Ages and caches outside this hypothesis are unrestricted. In particular `P` is disjoint from `I union {a}`, by the no-self rule.

The hypothesis still forces `|I| <= n-c+1`; this result does not remove the shared-anchor endgame obstruction for `c>=4`.

## Proof

Let `M=max_{p in P} m_p`. Prefer an outside-`I` owner partner whenever one is oldest or tied. Such an exchange finishes immediately: its responder receives protected fresh `a^0`, while other zero holders are unchanged.

Otherwise inspect an actual oldest owner head `Q in I` and freeze the owner. Every zero holder has the `c-1` reserved anchors `{a} union P` and at most one residual entry. Prepare `Q` as follows. If its residual cache is empty, stop. If its residual identity is outside `I`, stop before contacting it. If its residual age is below the maximum current secondary-anchor age at `Q`, stop. In every other case select this internal residual partner `R`, which is an actual oldest choice, and perform the full shuffle. All reserved anchors are sent and returned, so they are protected. The `a` anchor stays zero. For every secondary coordinate, endpoint ages `(u,v)` become the common value `min(u+1,v)`. This belongs to `{m_p,m_p+1}` when both input ages do. Thus all hypotheses about old zero holders are preserved.

On residual identities this is exactly a capacity-one singleton exchange. The active residual is replaced by the responder's pre-exchange residual, with a returned self identity filtered. The responder's residual becomes fresh `Q^0`. Only `Q` initiates during preparation. A first visit to a responder establishes this fresh pointer; a repeat returns it and empties `Q`'s residual cache. Therefore at most `|I|` preparation exchanges occur before a stopping case. Oldest legality is checked before every step, rather than assumed from the residual dynamics. The owner's inspected oldest choice remains unchanged throughout.

Now execute owner `a -> Q`. The complete reply contains its self anchor, all secondary anchors, and at most one residual. After filtering self, at most one valid reply identity is novel at the owner. The mandatory partner deletion supplies a vacancy, so no active resident is evicted. Every secondary owner entry survives. Its incremented age is at least `m_p+1`, while the reply age is at most `m_p+1`. Minimum merging therefore resets the owner's secondary vector **exactly to `Q`'s pre-exchange vector**. The passive responder keeps that same vector; received protection keeps every anchor, including `a^0`. Outside holders are untouched. Existing owner heads outside `I` survive until the terminating contact.

If a macro inserts a new `I` head of age `b`, its preparation must have stopped because it was below the current maximum secondary age at `Q`. The exact vector reset makes this also the owner's post-macro maximum, so the inserted head is strictly younger than that maximum. The maximum belongs to `{M,M+1}`, and consequently `b<=M`.

There are at most two owner heads outside `P`. If at most one belongs to `I`, its macro either removes it, replaces it by an outside head, or inserts an `I` head strictly younger than a secondary. An outside partner can then be selected and the path finishes. A returned `I` head that duplicates the other retained head also reduces the number of `I` heads to one, and minimum merging makes that head strictly younger than a secondary; this case finishes immediately rather than requiring the distinct-head argument below.

Suppose there are two initial `I` heads. After the first macro its inserted `I` head, if any, is strictly younger than an owner secondary, so cannot be selected at the very next macro. Hence a second nonfinishing macro must select the other initial head. If the first macro inserted no `I` head, that second macro starts with at most one and the single-head argument finishes. If the second macro inserts no `I` head, at most one remains: one further macro suffices by the same single-head argument. Otherwise, apart from the already handled duplicate case, there are two inserted heads. The second is strictly younger than the current maximum secondary age. The first has aged once and is at most `M+1`, while the secondary maximum is in `{M,M+1}`.

The only way a third nonfinishing macro is necessary is that the first inserted head is now `M+1` and the secondary maximum has fallen to `M`. In that case the second inserted head must have age at most `M-1`, since it was strictly below that maximum. A third macro selects the first head. The other head ages to at most `M`, the secondary maximum remains at least `M`, and any newly inserted `I` head is strictly below that maximum. Thus an outside partner can now be selected. This proves the three-macro bound. Each macro uses at most `|I|` preparation exchanges and one owner exchange; one final exchange completes the gain.

## A three-macro regression example

For `n=6`, `c=ell=3`, use `a=0`, `P={1}`, `m_1=1`, `I={2,3,4,5}`, and:

```
C_0={1^1,2^3,3^3}; C_1=empty;
C_2={0^0,1^2,4^1}; C_3={0^0,1^1,5^0};
C_4=C_5={0^0,1^1}.
```

Choosing owner partners `2,3,4,1` executes three nonfinishing macros followed by the gain. No internal preparation is needed. The first three owner caches are respectively `{1^2,3^4,4^1}`, `{1^1,4^2,5^0}`, and `{1^1,5^1}`. The fourth contact selects `1` in a tie and creates its fresh zero. This verifies why the old two-macro count does not carry over unchanged.

Deleting `5^0` from `C_3` gives a second regression: the second macro inserts no residual but leaves owner cache `{1^1,4^2}`. A third macro is still necessary before the final contact. Therefore it is important not to conclude immediate termination merely because the second macro inserts no `I` head.

## Verification scope

The accompanying [checker](../../verification/mandatory-removal/verify_thesis_cooperative_bands.py) verifies exact legal controlled transitions, secondary-band invariants, an independent residual update, preservation of all original zeros, and the three-macro bound. Its seeded initial configurations are finite corroboration of the symbolic lemma, not an exhaustive all-state certificate or a proof of generic convergence.
