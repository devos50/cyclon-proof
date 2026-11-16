# One old-zero owner head permits arbitrary shared secondary ages

Conditional working lemma, 16 November 2026. This is a qualitative extension of the callback mechanism, not a generic accessibility theorem. Both independent mathematical reviews accepted the argument below. The band-free result here is specifically for `c=ell=3`, with one secondary identity; it is not asserted for arbitrary secondary vectors.

## Statement

Let `I={q != a: a^0 in C_q}`. Suppose every member of `I` caches a shared secondary identity `p`, at an arbitrary finite nonnegative age, and owner `a` also caches `p`. By no-self, `p` is outside `I union {a}`. Assume the owner's cache contains **at most one identity in `I`**. It may also cache another identity outside `I`.

Put `u_0=age_{C_a}(p)` and `M_0=max_{v in I union {a}} age_{C_v}(p)`. There is a controlled path increasing `Z_a` by one, preserving all original zeros throughout, and not decreasing `N_a`, with at most

`(M_0-u_0+1)(|I|+1)+1`

exchanges. This bound depends on initial ages; it is not an age-uniform or ordinary-execution mixing estimate.

## Proof

Use the singleton-residual preparation from [the unit-width callback](UNIT-WIDTH-CALLBACK.md), but with no band assumption. Prefer an outside-`I` owner head in every oldest tie and finish if one is available. Otherwise freeze the owner and prepare its unique `I` head `Q`: reserve `a,p`, and let only `Q` initiate while its residual partner is internal to `I` and has age at least its current `p` age. These are legal oldest choices. Stop at an empty residual, an outside residual, or a residual age below the current `p` age. First visits establish a fresh pointer to `Q`; a repeat clears the residual, so at most `|I|` preparation exchanges occur.

In every preparation exchange, both endpoint `p` ages become `min(u+1,v)`. This lies between the two old values, since ages are integers. Thus the maximum `p` age over `I union {a}` never increases. The same property holds in the subsequent owner exchange. All old `a^0` copies remain protected.

The complete owner reply contains `a,p` and at most one residual. Self-filtering and the mandatory vacancy prevent active eviction. Hence at most one `I` head remains at the owner after every macro.

If a macro leaves no `I` head, an outside contact finishes. Otherwise write `b` for its returned `I` head's age, `v` for the prepared `Q` secondary age, and `u` for the owner's pre-macro secondary age. Preparation stopped at `b<v`, and the owner's new secondary age is `w=min(u+1,v)`. To require another nonfinishing macro, the sole `I` head must be strictly older than every outside head, in particular `b>w`. These inequalities imply `w=u+1`; if the minimum were `v`, they would contradict `b<v`.

Therefore every macro after which work must continue increases the owner's secondary age by exactly one. That age is bounded above by `M_0`, because the global maximum never increases. There can be at most `M_0-u_0` such macros and at most one final macro before an outside contact. Each macro uses at most `|I|+1` exchanges, and one last exchange creates the new zero. All previous zeros were preserved, and other identity-`a` holders were untouched until that final refresh.

## Boundary and remaining gap

The argument is useful whenever another construction reduces the owner's `I`-head count to one, including by a duplicate reply, an empty residual, or an outside residual. It does not prove that a two-`I`-head owner can always be reduced this way. For multiple secondary coordinates, the maximum owner age can fall when coordinates reset differently; the scalar monotonicity argument must not be silently reused.

The [checker](../../verification/mandatory-removal/verify_thesis_cooperative_scalar.py) uses exact transitions on finitely many seeded starts. Those paths corroborate, rather than replace, the symbolic proof.
