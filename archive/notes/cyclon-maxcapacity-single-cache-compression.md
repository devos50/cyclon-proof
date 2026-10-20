# Uniform single-cache compression at maximal capacity, shuffle length two

Assume n>=3, c=n-1, ell=2, and the exact mandatory-removal kernel.
Fix a peer p. There is an adaptive positive-probability policy using only
consecutive p initiations which reaches |C_p|<=1 in at most

    2 G_0 + (|C_p(0)|-1)_+
    <= 2(n-1)^2 + n-2

initiations, where

    G_0 = (n-1)^2 - sum_{q != p} |C_q(0)|.

The bound is independent of all descriptor ages. The policy succeeds for every
sequence of actual oldest-partner tie choices and every choice of the extra
entry. No chosen partner is assumed available outside the actual oldest set.

At maximal capacity, there are only n-1 permissible identities at each peer.
Thus incoming distinct nonself descriptors always fit after filtering; no
resident is ever replaced, except the mandatory partner at the active peer.
All passive cache cardinalities are consequently nondecreasing.

While |C_p|>=2, let q be its actual selected partner and r the selected extra
entry. If q already knows p and r, choose its reply to be exactly {p,r}.
This is legal because its cache contains those two different nonself identities.
The active peer discards p as self and r as a duplicate, and therefore its
cardinality decreases by exactly one. The passive cache receives only duplicate
identities and does not change.

If q does not know both p and r, choose any legal reply. The passive cache gains
at least one entry, because it receives fresh p and the extra r and there are
no replacement evictions. The active cache cardinality can increase by at most
one: it removes one partner and accepts at most two reply entries.

Call the second kind a growth event and the first kind a shrink event.
There are at most G_0 growth events, by the bounded nondecreasing total passive
cardinality. Before the first hit of active cardinality <=1, each shrink event
reduces that cardinality by one and each growth event can increase it by at
most one. There can therefore be at most |C_p(0)|-1+G_0 shrink events.
The displayed hitting bound follows. Initially |C_p|<=1 requires zero events.

All prescribed replies have positive probability. More quantitatively,
conditional on the required p initiations, each policy reply has probability
at least 1/binom(n-1,2); the policy puts no restrictions on extra-entry or oldest
tie randomness. Thus with D=2(n-1)^2+n-2, the probability of hitting cardinality
<=1 by global event D is at least [n*binom(n-1,2)]^(-D), by requiring the first D
initiators to be p and the prescribed replies until the stopping time. Behavior
after the hit is irrelevant to this hitting event.

This lemma does not prove that p can be emptied. For example, after compression
p can continue as a singleton walking among full passive caches indefinitely.
It also does not prove uniqueness of the recurrent class or conditional-uniform
peer marginals for ell=2. Its use is a uniform, age-compatible reduction of one
cache without changing the kernel.
