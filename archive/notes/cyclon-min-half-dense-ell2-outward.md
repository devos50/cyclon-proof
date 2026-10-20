# Protected+MIN CYCLON, ell=2: outward gain when n<=2c

Assume c>=3, n<=2c, and an empty owner cache C_a. Initially exactly H peers
hold identity a, and all these copies have age zero. Suppose some holder p
caches a nonholder. Every buffer has its ordinary maximum size; every
controlled reply/victim choice has positive probability. The following
finite controlled path increases the TOTAL number of a-holders beyond H.
It does not assume any global connectivity.

## Owner-only cached-target service

If owner a caches a nonholder target z, activate only a and retain z as the
extra whenever another partner is selected. Stop at the first nonholder
responder. Until that event every responder holds a; require its reply to
contain a, and z if known (otherwise any other entry if one exists).
The self a reply is discarded, so at most one usable ID arrives and the
mandatory vacancy suffices: z stays cached and the owner cache never grows.
A first-visited responder learns protected z; a repeat returns {a,z} and
shrinks the owner cache. Thus a nonholder is contacted within n+c events.
All old a-holders retain a because the owner sends fresh protected a^0.
The first nonholder newly accepts a^0, increasing total holder count by one.
This argument is valid for arbitrary c>=2 and arbitrary finite ages.

## Empty-owner double callback

Suppose a current a-holder u caches some nonholder v and its oldest partner
is owner a. Send v as the extra in u->a. The owner is empty, so u loses its
a copy and the owner becomes {u^0,v^(B+1)}, where B>=0 was v's age at u.
The next owner activation is forced toward v. Send u as its extra. At v,
fresh a^0 creates a new holder, restoring the one lost holder. At the owner,
mandatory removal leaves only u; the at-most-two reply fits because c>=3.
Hence u remains cached. But u is still a nonholder: it removed a in the
first event and the empty owner returned nothing. Owner-only cached-target
service with target u now adds another holder. Net gain is at least one.
All other old a-holders were passive and retain their copies throughout.

This macro needs no condition on the cache at v except that it lacks a.

## Single-holder service before a nonholder contact

If a zero-holder p caches a nonholder target x, activate only p while it
contacts other a-holders. Choose an oldest nonanchor in a tie and always
send a as the extra. Require each holder reply to contain a^0 and p if
known, otherwise any second entry if one exists. The anchor refreshes to
zero, while at most one other usable ID arrives. Thus p's cache does not
grow. The target x is unsent and cannot be an eligible victim; it remains
cached until selected. Each responder learns fresh p; a repeated responder
returns {a,p}, causing the active cache to shrink. A nonholder is contacted
within n+c events. This service preserves every a-holder before that event.

If p is underfull at that first nonholder contact, mandatory removal creates
at least two vacancies. Its at-most-two reply cannot evict the sent a.
The responder newly accepts a, so total holder count increases.

## Controlled replies at nonholders

Let an a-holder p contact a nonholder q, sending fresh p and a. If q's
cache contains any ID in C_p union {p}, include one such ID in its reply.
It is a duplicate or self-filtered at p (q itself cannot be in C_q), so at
most one usable new ID arrives. Mandatory removal suffices and p keeps a;
q newly accepts a, giving a holder gain.

These replies always admit protected victim choices. If q knows p, only a
is new and the other reply entry is an eligible victim if required. If q
does not know p, both outgoing IDs are new, so any returned residents are
eligible victims, including the returned ID already known at p.

Consequently the only case that fails to give a holder gain has p full,
two usable novel reply IDs, and

    C_q disjoint from C_p union {p}.

It follows that |C_q|<=n-c-1<=c-1. The initiator is forced to evict its sent
a, remains full after replacing two removed IDs by two novel reply IDs,
and becomes a nonholder. The responder newly accepts protected a and fresh
p^0; its new size is min(c,|C_q|+2). Call this a migration and follow the
new a-holder q. The previous initiator p remains cached at q and is a
nonholder. Freeze it unless it later becomes the tracked holder again.
The number of a-holders is unchanged; the only possible positive-age a
copy is now at q. All other a copies remain zero.

## Finish by a full-cache potential

Follow the current a-holder. Initially use single-holder service at the
specified zero-holder p. After a migration the new holder has a positive
a copy and a cached nonholder predecessor. At each activation:

* If the selected partner is owner a, choose that predecessor as extra and
  apply the empty-owner double callback. This increases holder count.
* If the selected partner is another holder, require a^0 and the active
  peer's identity if known. The active anchor refreshes to zero and its
  cached nonholder predecessor is unsent and survives. Continue by the
  single-holder service. If the active cache has become underfull, it
  stays underfull during this service and its first nonholder contact
  therefore gives a gain.
* If the selected partner is a nonholder, use the controlled reply above.
  Either it gives a gain or causes a migration.

If a new holder after migration is underfull, the same cases yield a gain:
a nonholder contact cannot evict a; a holder contact refreshes a to zero
and enters the underfull service; an owner contact invokes double callback.

It remains to consider a path with no gain and all tracked holders full.
Every migration strictly increases the number of full NONOWNER caches:
the old active holder stays full, and the responder was underfull
(|C_q|<=c-1) but becomes full. Other exchanges preserving a full active
cache cannot reduce this number, because passive cache cardinalities never
decrease. A holder exchange that makes the active cache underfull leads
to a gain by the preceding paragraph. Owner contacts also lead to a gain.
Thus this integer can strictly increase only finitely many times, at most
n-1. Between migrations, single-holder service lasts at most n+c events;
a positive tracker has just one activation before gain, migration, or
entry to that service. Hence the whole controlled witness is finite.
A conservative length bound is

    (n+1)(n+c+1).

(At most n-1 migrations; at most n services of length n+c; the final
owner macro has two exchanges plus one cached-target service.)

## Consequence in a closed class

The separately proved positive-copy zeroification implies that, if k is
the maximum number of a^0 holders in a closed communicating class, every
state in that class has at most k TOTAL a-holders. Choose a maximizing
state with empty owner. The outward-gain lemma excludes all I->J edges,
where I is the set of a^0 holders and J is the set of nonholders other
than the owner. The incoming-contact/residual-root normalization argument
then completes universal-anchor accessibility as in the dense-case proof.
Therefore fixed ell=2 converges for c>=3 and n<=2c; the separate capacity2
theorem covers all n with c=2.
