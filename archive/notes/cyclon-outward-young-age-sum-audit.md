# Independent audit of the root's uniform outward-routing bound

The root's proposed young-age-sum bound is valid. Let N=nc and start the
outward construction by marking all descriptors old; every subsequent fresh
self descriptor is young and duplicate marks use OR. Every marked-young
descriptor at global elapsed event t has numerical age <=t. MIN merging
can only decrease this age upper bound, regardless of initial old ages.

The existing controller ensures F, the number of young descriptors, never
decreases. Every zero-holder contact strictly increases F. A nonholder
migration with an old selected partner also strictly increases F. Therefore
in a constant-F chunk every nonterminal event is a nonholder migration
with a selected young partner, and the source/responder pre-cache identity
sets are disjoint from each other and from source-self as in the existing
generaloutwardgain lemma.

At such an event write f_p for the number of young entries in the active
full cache and b for the selected young partner's age BEFORE the common
increment. The old anchor a is also resident, so f_p<=c-1. The selected
young copy is removed, all other young active entries increment by one,
and the fresh source identity p arrives at the responder at age zero.
Any young responder victim is returned and copied to a novel active
location; its numerical age is unchanged. If a returned young descriptor
were NOT evicted at the responder, its second copy would strictly increase
F. Thus every young reply copy is an exact transfer in a constant-F event.
There are no other young losses: the sole extra victim at the initiator
is old a, and disjointness excludes duplicate/self filtering on the reply.

Consequently, with S the sum of numerical ages of all marked-young copies,

    Delta S = (f_p-1)-b <= c-2-b.

An inequality suffices if implementing extra MIN decreases; the upper
bound is unchanged. During a constant-F chunk there is no zero-anchor
refresh, so the current anchor's age is A+t_local, A>=0, even as it migrates.
The oldest rule requires b>=A+t_local. Hence

    Delta S <= c-2-A-t_local <= c-2-t_local.

If the chunk starts at global time t0, S_start<=N*t0. After L chunk events,

    0<=S_end<=N*t0+(c-2)L-L(L-1)/2.

Solving the quadratic gives the conservative bound

    L<=2c+2sqrt(N(t0+1)).

Now append one strict-F event, or the event entering a terminal gadget.
Since N>=2c+1 for the relevant n>=c+1,c>=3, the resulting next time obeys

    sqrt(t_next+1)<=sqrt(t0+1)+sqrt(N).

There are at most N strict-F events and at most N+1 chunks. Starting with
sqrt(0+1)=1, the total unfinished body is bounded by

    [1+(N+1)sqrt(N)]^2.

Add the explicit terminal gadget budget separately (underfull-holder
service or empty-owner double callback). Neither depends on initial ages.
For an integer-only formula one can replace sqrt(N) by N or ceil(sqrt(N)),
or use a simple polynomial majorant such as 4(N+1)^3, leaving ample slack.

This audit establishes a uniform polynomial CONTROLLED PATH bound. It does
not establish comparable typical-random-execution drift: the F-monotone
reply/victim controller is chosen deliberately. Any mixing estimate obtained
by following its whole specified path still incurs an exponentially small
success probability.
