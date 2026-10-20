# Protected+MIN CYCLON, ell=2: general outward-holder gain

Assume arbitrary finite n, c>=3, an empty owner cache C_a, and initially H
holders of identity a, all with age zero. Suppose a holder p caches a
nonholder. There is a finite controlled path with more than H a-holders.
No density assumption is used. All ages are the actual numerical ages.

## Previously established terminal gadgets

1. A zero-holder with an underfull cache and a cached nonholder target can
   force a holder gain: activate only that holder, send a as its extra,
   require a^0 and the initiator ID if known in holder replies, and choose
   a nonanchor oldest partner in a tie. Its target is unsent and retained;
   the cache cannot grow during holder contacts, repeated responders shrink
   it, and a nonholder is reached within n+c events. At that event the
   two-entry reply fits two mandatory vacancies, so the old a survives and
   the responder newly learns a.
2. An empty-owner double callback gives a gain if the current a-holder u
   contacts owner a while caching a nonholder v. Send v extra. The owner
   becomes {u^0,v^(B+1)} and u loses a. Owner->v is forced; send u extra.
   This restores the one lost holder. Since owner pre-size is2 and c>=3,
   its at-most-two reply cannot evict extra u. Owner still caches nonholder
   u. Owner-only cached-target service then adds another holder. Net +1.
3. At a nonholder responder q, if its cache has any ID in C_p union {p},
   include one such ID in the reply. At most one usable new ID arrives at
   p, so its mandatory vacancy suffices and p keeps a while q learns a.
   Such replies allow the required protected victims: if q knows p only
   a is new, and otherwise both outgoing IDs are new and all returned
   resident IDs are eligible. This gives a direct holder gain.

## Controlled trajectory and fixed passive holders

Only one a-holder is activated at a time; call it the current holder.
At every nonowner contact it sends fresh self and a. Stop at any holder
gain. If a nonholder contact does not give a gain using gadget3, the old
current holder must be full and must evict its sent a after receiving two
novel reply IDs. The responder has no ID in the current cache or current
self. It acquires protected a and fresh predecessor^0; the old current
loses a and remains full. Follow the responder as the new current holder.
This is a migration. The old current is a frozen nonholder predecessor
cached at the new current, and the old current's cache does not contain
the new current's identity (it removed it and the responder cannot reply
with itself).

Let Z be the INITIAL a^0 holders other than the initial current p. Until a
gain, the holder set is ALWAYS exactly Z union {current}. Every member of
Z remains a passive zero-holder and is never an initiator. Past current
holders are nonholders until one becomes current again by a migration.
Thus every current created by a migration caches a nonholder predecessor.
That predecessor survives holder contacts: it is unsent, and a passive
zero-holder partner cannot equal it. If it is itself contacted, the next
event gives a gain or a new migration and a new predecessor.

After a holder contact, return a^0 so the current anchor refreshes to0.
If its cache becomes underfull, invoke gadget1 with its retained predecessor
(or the initially cached nonholder target) and finish with a gain. Otherwise
continue with the full current cache. An underfull current created directly
by a migration also finishes: a nonholder contact gives a gain immediately;
a holder contact refreshes a to0 and enters gadget1; an owner contact uses
gadget2. Hence an unfinished trajectory may assume its current is full.

The owner is frozen and empty until a terminal use of gadget2. For a
zero-age current anchor choose an oldest nonanchor in a tie. Such a
nonanchor exists because a nonholder predecessor/target remains cached.
For a positive current anchor choose any actual oldest partner. If it is
owner a, invoke gadget2. All other cases are covered below.

## Auxiliary colors

Initially color every descriptor OLD. Every fresh self descriptor is
YOUNG. On duplicate merging color by OR: the result is YOUNG if either
input is YOUNG, regardless of which input provides the minimum age.
These colors are proof-only bookkeeping. Let F count all YOUNG cache
entries. It lies between0 and nc. Identity a is always OLD before the
terminal owner gadget. More importantly, every identity q in the fixed
passive set Z is permanently OLD: q is never an initiator, so no fresh
q descriptor is ever generated.

We choose replies/victims so that F never falls, and strictly rises whenever
the current contacts Z or selects an OLD nonholder partner.

### Passive zero-holder contact

Let current p contact q in Z. The selected q descriptor and the sent a
descriptor are OLD. If q knows p, reply {a,p}; the current cache shrinks
and gadget1 finishes. Otherwise fresh p is newly accepted at q and is
YOUNG. Require the reply {a,D} (or only a if q is a singleton). If q needs
a victim, choose D with identity absent from C_p. Such D exists: a full
responder has c-1 nonanchor residents. The initiator cache contains a and
the selected partner q, neither of which can be one of those residents,
leaving at most c-2 shared IDs. Thus at least one nonanchor resident is
absent from C_p. If the responder is underfull no victim is required and
any second reply entry is allowed.

The responder requires at most one victim, because a is already known.
If that victim is YOUNG, its reply makes the copy at p YOUNG and compensates
its removal at q. The selected partner q is OLD and the only possible
initiator victim a is OLD. The fresh new p copy at q adds another YOUNG
entry. Therefore F strictly increases by at least one. A reply causing
the active cache to shrink simply enters the terminal underfull gadget.

### Nonholder contact

If gadget3 gives a gain, stop. Otherwise the responder cache is disjoint
from C_p union {p}; a migration occurs. Choose all needed responder victims
inside its two-entry reply. Every YOUNG victim is copied to a previously
absent identity at p, compensating its removal. The initiator's sent victim
a is OLD. Fresh p at q adds one YOUNG entry; only the selected partner can
remove a YOUNG entry at the initiator. Thus

    Delta F >= 1 - 1{selected partner is YOUNG}.

In particular F never falls and strictly rises for an OLD partner.

## Finite plateaux from actual ages

Every finite unfinished controlled state has another positive-probability
event of the prescribed kind. Suppose a trajectory did not terminate with
a gain. Since F is a bounded nondecreasing integer, it would eventually
be constant. No passive zero-holder contact can then occur, and every
selected nonowner partner must be YOUNG. Every step on the plateau is a
nonholder migration. After its first step the current a copy has positive
age, and it increments by one at every subsequent migration without any
minimum refresh: the responder did not previously know a.

This cannot continue indefinitely. Start at any state on the plateau with
current a age A>=1. Let M_s(t) be the global maximum age of identity s,
using0 if absent, after t further events, and K_s(t)=M_s(t)-t.
For every identity s, K_s is nonincreasing: only active residents increment,
fresh selves have age0, and copying/MIN never exceeds an input age.
When identity s!=a is selected as partner, every copy of s at the active
cache is removed, s is not sent (the extra is a), and its own responder
cannot return s. All other s copies have unchanged or reduced ages.
Hence K_s decreases by at least one on that step.

The tracked a age before event t is A+t. Any selected partner s has age at
least A+t, so K_s(t)>=A. Each identity s can be selected at most
(M_s(0)-A+1)^+ times while this is true. Summing gives a finite bound on
the plateau length. Its only possible exits are a strict F increase or
owner contact, which already yields a holder gain. This contradicts an
infinite unfinished trajectory.

Thus the controlled path terminates after finitely many events with more
than H a-holders. The witness length is age-dependent; the proof asserts
no uniform bound here. Every event has positive probability, so the finite
path is accessible in the original chain.

## Full ell=2 conclusion

In a closed communicating class, let k be the maximum number of a^0 holders.
The previously proved positive-copy zeroification bounds TOTAL holders by k
throughout the class and excludes positive copies at a k-maximizer. Choose
such a maximizer with empty owner by the established source-only/anchored
normalization argument. The theorem above rules out every outward I->J edge.
Residual ell=1 normalization plus a paused first incoming contact adds a
zero if J is nonempty, since c>=3 lets a singleton anchor and two incoming
IDs coexist. Hence every class contains a universal zero-age anchor.
The common canonical atom and uniform finite-age reset then imply a unique
stationary law and uniform geometric full-state convergence for fixed
ell=2 and EVERY capacity c>=3. The separate c=2 theorem completes all
2<=c<=n-1.
