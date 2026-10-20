# Shuffle length three, capacity three: a common positive second anchor suffices

Consider the mandatory-removal, received-ID-protected, MIN-duplicate kernel
with c=ell=3. Fix an owner a, let I be all current holders of a at age zero,
and let p be a peer outside I, distinct from a. Suppose:

* every q in I stores a^0 and p^m, for one common integer m>=0;
* p belongs to C_a with age at least m.

There are no restrictions on other cache IDs, including the other owner IDs.

Then a controlled path of at most 2(n+4)+1 exchanges creates a new zero-age
copy of a, preserves every original zero-age copy of a, and does not decrease
the total number of a-holders. The estimate is deliberately loose and does
not depend on m or any initial age gap. The claim is conditional: it does
not treat unequal second-anchor ages.

## Partial clearing of an actual owner head

If the owner's selected oldest partner is outside I, execute that exchange
and finish. Otherwise call its actual oldest partner Q in I, and freeze a.
At peers in I reserve a and p as the two outgoing extras, and reply with both
anchors. Each peer has at most one residual descriptor. Both anchors retain
ages 0 and m: active copies increment, passive copies have 0 and m, MIN
refreshes the active copies, and all received anchor IDs are protected.

Run the ordinary Q-only shuffle-one residual clearing controller, but stop
before any activation whose residual cache is empty, whose residual partner
lies outside I, or whose residual age is strictly less than m. Every executed reduced oldest choice is legal in
the original kernel: its age is at least m, and ties with p or a are resolved
in favor of the residual partner.

This interrupted clearing has at most |I|+3 exchanges. One can see this
without appealing to any recurrence result. Whenever Q visits a residual
partner u, that passive cache receives the protected triple {Q,a,p}; thus
its residual pointer becomes Q. If Q later revisits u, the reply contains Q,
which is filtered as the active self ID, and Q's residual becomes empty.
There are at most |I|-1 distinct possible residual partners. The process
may stop earlier at an outside-I residual partner or a residual age below m. Consequently its endpoint is

    C_Q = {a^0,p^m}, or C_Q = {a^0,p^m,R^b},
    where R is outside I or b<m.

The owner's cache and numerical ages are unchanged while this occurs.

## The owner removes an old head

Now activate a with its previously selected oldest partner Q. Include p as
an extra and, when present, the only other owner-cache ID H as the second
extra. The reply contains a,p and possibly R^b. The owner filters a, merges
p by MIN, and can receive at most the single new residual ID R. The vacancy
from mandatory removal of Q accommodates R, so no additional owner entry
is evicted. The endpoint owner p-age is exactly m: it was at least m before
activation, hence its incremented age is at least m+1, and Q replies p^m.
Every newly received I-head has age less than m; newly received outside-I
heads need no age restriction. If R already was the other
head H, MIN can only decrease that head's age.

At Q, fresh a^0 and the outgoing p descriptor are received and protected.
The latter has age at least m+1, so its merge leaves p^m. The possible third incoming ID H may belong to any peer. Thus all original
zero anchors and the common second-anchor layer p^m survive. No residual
closure property is needed.

## At most two such owner-head exchanges

The owner has at most two I-heads besides p. After the first normalization
and owner-head exchange its p-age is m, its newly inserted I-head (if any)
has age less than m, and the only other possible head is one original head
H whose age has increased by one.

If any outside-I head is selected, finish with a fresh zero copy there.
Otherwise the newly inserted head, if it belongs to I, is strictly younger
than m. If the other head H has age at most m, p is oldest or tied unless
an outside-I head outranks it, in which case that outside contact finishes.
If H has age above m and belongs to I, normalize and remove H in a second
block. During this second owner exchange the first inserted head increments
once, so its age becomes at most m. The second inserted I-head, if any, has age below m, while p again is
refreshed to m. Hence either p is oldest or tied, or an outside-I head is
oldest. In either case an outside-I partner may be selected immediately. For m=0 the low-age residual case is
impossible, so an I-head simply disappears in each block.

The last exchange reaches p or another outside-I peer and creates/refreshes
its a descriptor to age zero,
and increases the zero-holder count. All original zero holders retained
their protected a^0 throughout. They never selected a because their chosen
residual partner had age at least m and ties were resolved in its favor.
No a-holder loses its a descriptor. Two clearing blocks, two owner-head
exchanges and the final exchange give 2(n+4)+1 as claimed.
