# Protected + MIN, ell=2: an arbitrary-age universal anchor can be zeroized

Fix a peer a. Assume every p != a contains a descriptor for a, with arbitrary
nonnegative integer age. The owner's cache C_a and all other descriptors are
arbitrary. Under mandatory oldest-partner removal, protected received identities,
and MIN duplicate merging, there is a controlled positive-probability path of
at most 2(n-1)(n+c-1) events to a state in which every p != a contains a^0.
Thus universal identity accessibility, without an age qualification, suffices
for the previously proved common-canonical-atom reduction.

## Pair-clearing observation

Suppose a single active node x keeps a target z cached, every possible responder
other than z contains the identity x, and each such responder is prescribed to
return x together with z whenever it knows z (otherwise x plus any permissible
other entry). Choose z as the outgoing extra whenever the selected oldest
partner differs from z. The responder always learns/retains z. The active node
has at most one usable incoming identity, since incoming x is its self identity;
thus the mandatory vacancy suffices, the target z is retained, and its cache
size never increases. After a responder has once been contacted, it permanently
retains z during the x-only block, and future replies {x,z} add no usable new
identity, strictly shrinking x's cache. Therefore x reaches z in at most
K=n+c-1 events. The argument is valid for all ages and every actual oldest tie
outcome. Duplicate MIN refreshes can change the next selected partner, but not
this decreasing-size/first-visit argument.

The same conclusion holds if every responder contains z rather than x,
provided replies always include z and include x when known: before reaching z,
there is at most one new usable incoming identity because z is a resident
duplicate. Each first contact establishes a persistent x copy at the responder,
and repeats then return {x,z} and shrink the active cache.

## Increase the number of zero-age a copies

Let I={v != a : C_v[a]=0}. If I contains every nonowner, stop. Choose p != a
whose resident a descriptor has positive age. Keep only p active. Whenever its
oldest selected partner q differs from a, choose a as its extra, and prescribe
q's reply to contain its resident a, together with p if p is present. If p is
absent from q, choose any permissible second entry. Every q != a initially
contains a, and incoming identities are protected. Thus the second form of the
pair-clearing observation applies.

Stop immediately if p receives a^0. Then p joins I and no prior member of I has
lost its zero-age copy: all other peers were passive and their anchor copies
were protected, while MIN with a nonnegative incoming age cannot increase 0.

If this has not happened, within K events p contacts a. The mandatory removal
makes p lose its positive-age a descriptor. The owner cannot return a self
descriptor, so p remains the only nonowner lacking a. The owner receives and
retains p^0. Every former member of I remains unchanged at age0.

Now keep only a active, with p as the target. Every responder other than p
still contains a. Choose p as the extra whenever the selected partner is not p;
return a and p when p is known, otherwise a and any permissible other entry.
The first form of the pair-clearing observation applies. In at most K further
events a contacts p. Fresh self a^0 is then received and protected at p, so p
joins I and universality is restored. All earlier members of I were passive;
any contacted one received a^0 and therefore stayed at age0.

Each iteration enlarges I by at least one and restores the universal-identity
hypothesis. There are at most n-1 iterations. The total length is at most
2(n-1)K. All prescribed initiators, extra choices, oldest-tie choices, reply
choices, and feasible victim choices have positive probability. No assumption
on the initial ages, owner's cache, residual connectivity, or cache fullness is
used.

## Scope

This proves arbitrary-age universal anchor -> universal zero-age anchor. It
does not prove that a universal identity can be reached from an arbitrary
weakly connected state. That remaining identity-saturation question is strictly
weaker than requiring direct zero-age saturation from every state.
