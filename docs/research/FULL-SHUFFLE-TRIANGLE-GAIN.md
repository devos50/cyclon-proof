# A three-exchange full-shuffle holder gain

**Status:** independently reviewed symbolic local gadget, integrated in the
manuscript with exact kernel regression checks. This is not a generic
convergence or mixing-time theorem.

## Label-ready statement (`lem:fullshuffletrianglegain`)

Under the adopted protected/MIN protocol, let `ell=c>=2`. Suppose owner a
has an empty cache and a distinct peer p caches a and some peer r that does
not cache a. Assume a is an oldest entry at p and r is an oldest entry among
p's entries other than a. Then the three prescribed exchanges

```
p -> a,   a -> r,   p -> r
```

are legal full-shuffle exchanges. At their end the set of identity-a holders
is exactly its initial set together with r. Both p and r hold `a^0`, and
all peers outside `{a,p,r}` retain their entire initial caches. Other initial
holders need not hold age zero. Initial cache sizes may be below capacity.

The claim concerns the final holder set: the first exchange temporarily
removes p's a-copy. If a has age zero at p, legality of the first exchange
forces every p-entry age to be zero, so any nonholder residual r satisfies
the second oldest condition automatically.

## Proof

Write the initial p cache as `{a^A} union {v^b_v:v in E}`, with `r in E`,
`A>=max b_v`, and `b_r=max b_v`. All ages are finite nonnegative integers.
The first exchange has empty reply and no overflow. It leaves

```
Cp = {v^(b_v+1): v in E},
Ca = {p^0} union {v^(b_v+1): v in E}.
```

Thus r is oldest at a, since `b_r+1>=1>0`. The second exchange sends the
full packet

```
{a^0,p^1} union {v^(b_v+2): v in E minus {r}}.
```

Every identity in this packet is valid at r and is protected after merge.
The packet has `|E|+1<=c` entries. It may coexist with old entries when p
was initially underfull, but in particular r now holds `a^0`, p, and every
identity in `E minus {r}`. Minimum-age merging can only lower duplicate
ages and does not affect this identity argument.

The cache of p has not changed during the second exchange. Hence r is
still oldest there. In the third exchange p sends

```
{p^0} union {v^(b_v+2): v in E minus {r}}.
```

Every sent identity is already resident at r, by the previous paragraph.
There are no novel received identities, hence no eviction at r; its `a^0`
survives. Because `ell=c`, r's entire cache is returned to p, including
`a^0`, which is inserted and protected. No other cache has changed. This
proves the exact holder-set and zero-age assertions.

## Scope and evidence

For positive `A`, the condition that a designated nonholder r is oldest
among the residual entries is essential to this specific three-event
schedule. If a holder residual outranks r, neither the second nor third
partner choice is justified by this proof. Additional routing or callback
arguments are needed in that case. No claim is made here for `ell<c`.

Run the durable checker:

```sh
python3 -B verification/mandatory-removal/verify_full_shuffle_triangle_gain.py
```

It checks 2,120 capacity-three cases, exhausting responder identity sets
for the stated small populations and testing ordered ages including
`10^6`, plus 9,273 cases with `n=4,...,14`, every `c=2,...,n-1`, full shuffle,
and varied underfull cache sizes. It uses `ActualThree` with `ell=c`,
asserting legal oldest choices, protected merges, final holder sets, and
unchanged outside caches. Finite tests corroborate the symbolic argument;
they are not a proof of a generic rate.

## Capacity-three completion when a holder residual is older

**Conditional corollary using the learned-target callback.** At `c=ell=3`,
suppose a is empty, p caches a as an oldest entry, and p also caches some
nonholder r. Then there is a finite legal path ending with strictly more
identity-a holders than initially, preserving every initial holder at the
endpoint. No zero-age assumption on the other holders is needed. This
statement depends on the nonholder strengthening in
[C3-LEARNED-TARGET-CALLBACK.md](C3-LEARNED-TARGET-CALLBACK.md); the three-event
prefix alone is independently verified here.

If an oldest residual at p is a nonholder, the preceding triangle lemma
already gives the claim. Otherwise p is full with
`Cp={a^A,r^R,s^S}`, where `A>=S>R` and s is a holder of a. (If tied, select
the nonholder r.) Perform `p->a, a->s, p->s`.

After the first event `Cp={r^(R+1),s^(S+1)}` and
`Ca={p^0,r^(R+1),s^(S+1)}`. Thus s is a legal oldest partner at both a and,
while p is frozen, p. In `a->s`, choose the owner victim to retain r.
This is legal: s's full reply contains a, leaving at most two usable reply
identities. The owner's residents after mandatory removal are p and r,
so at most one victim is needed. If p is received, at most one other usable
identity is novel, so no victim is needed; otherwise p is eligible and can
be sacrificed. If r is received, it is protected in any case.

The request to s is `{a^0,p^1,r^(R+2)}`. Since all three identities are valid
at s and protected, these become exactly its cache identities, with its
existing duplicates possibly lowering their ages. The subsequent `p->s`
request is `{p^0,r^(R+2)}`. Both identities are already resident at s, so
there is no eviction and its `a^0` survives. Its full reply restores `a^0`
to p. Every original holder is now present again; p and s are zero holders,
and the owner still caches r, which remains a nonholder.

The learned-target nonholder callback applied to r therefore yields a
strict final holder gain. If the callback first contacts a positive holder,
its existing nonholder-strengthening argument retains r and iterates zero
gains until it reaches a nonholder. This final step is a symbolic use of
that separate working lemma, not asserted as an executed check here.

The durable checker additionally verifies 600 such restoration prefixes,
including arbitrary s-row identity sets and ages up to `10^6`. It asserts
exact restoration of the initial holder set, zero ages at p and s, owner
retention of the nonholder r, and unchanged outside caches.

Suggested manuscript label: `lem:c3ownerterminalgain`. This local terminal
gadget does not on its own establish that a general outward-holder
controller reaches its hypotheses or that arbitrary-network convergence
follows.
