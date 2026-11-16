# Conditional all-younger owner-service dichotomy

Local working lemma, 16 November 2026. Exact protected/MIN protocol with
shuffle length `L>=4` and capacity `c>=L`. This is **not** an owner-service
proof: the post-exchange age condition below is an additional hypothesis,
not a property established for arbitrary states.

## Statement

Let owner a cache distinct identities p and q, with q an oldest entry.
Suppose q caches `a^0,p^v`, owner a caches `p^u`, and `v<=u+1`.
Every residual entry of q (excluding a,p) has age strictly below v.

Let B consist of the `L-2` oldest owner entries other than p,q, or all
such entries if fewer are available. Send p and B as extras. Require
`a,p` and every identity in `B intersect C_q` in q's reply, and fill the
remaining required reply slots legally. These requirements fit: B has at
most `L-2` identities. Use any legal victim choices.

Assume **also** that every residual entry at q after the exchange has age
strictly below v. Then p remains at the owner with age exactly v, and:

1. If some B identity was novel at q, p is strictly older than every other
   remaining owner entry.
2. If no B identity was novel but the request has fewer than L entries,
   the same conclusion holds.
3. Otherwise the request is full and no B identity was novel. The owner's
   number of non-p heads decreases by exactly one.

Strict oldest here allows an owner containing only p. The lemma does not
assume a common upper bound on the original finite integer ages.

## Proof

The owner receives p from q, so p is protected and its age becomes
`min(u+1,v)=v`. The same formula applies to the passive p copy. Every
returned identity other than a,p is a pre-exchange q residual and hence
arrives with age below v. Returned self-a is filtered.

A B identity already resident at q is required in the reply. Its returned
age is below v, and MIN therefore makes its surviving owner copy below v.
If a B identity is novel at q, the passive merge must insert and protect
it with the incremented owner age. The assumed postcondition then forces
its incremented age below v, so its surviving owner copy also has age
below v.

In case 1, choose any novel B identity b. Every owner head excluded from
B,p,q had pre-exchange age at most that of b because B contained the
oldest eligible heads. After increment, those unsent heads are therefore
also below v. Together with the preceding paragraph and the incoming
age bound, this covers every surviving owner entry other than p.

In case 2, B contains every owner head other than p,q, so there are no
unsent heads to consider. All surviving B copies and all incoming
non-p identities are below v.

In case 3, B has exactly `L-2` identities and all occur at q. The required
reply `a,p` together with B already fills all L slots. At the owner it
contains only self-a and duplicates. There is no insertion or eviction;
mandatory deletion of q is the only identity-set change. Thus the
non-p head count falls by exactly one.

## Exact checks and limitation

Run:

```sh
python3 -B verification/mandatory-removal/verify_all_younger_owner_service.py
```

The checker tests 28,000 seeded legal transitions across `L=4,...,10`,
`c=L,...,L+4`, and every initial owner size `2,...,c`, with ages including
`10^6`. Reply completion and eligible victim subsets vary over legal
choices. It verifies the hypotheses and **explicitly filters out**
18,788 transitions that fail the postcondition. The remaining cases pass:
3,785 novel-B oldest outcomes, 5,152 short-request oldest outcomes, and
275 full-overlap head drops.

The large excluded group must not be treated as successful owner service.
A global argument would still need to reach this conditional regime or
handle its complement. These finite checks corroborate the local proof
only; they do not establish arbitrary-length convergence.

## Consequence for a prescribed owner-only trajectory

Here termination means an owner contact with p (or an earlier permitted
service boundary); in particular every preterminal responder differs from p.
Suppose only a initiates before termination, always retains and sends p,
requires a in zero-holder replies, and requires p in replies whenever it
is already present. A zero holder learns p on its first visit and cannot
lose it on subsequent visits: the incoming p is protected. There are
finitely many first visits. After the last such visit, every responder
already has p. Its p-age changes from v to min(v,u+1), a nonincreasing
nonnegative integer sequence. There are finitely many responders, so
after a finite trajectory prefix every passive p-age has stabilized.
At each subsequent contact stabilization implies v<=u+1 and the owner's
new p-age is exactly v. This argument supplies the inequality in the
local lemma; it does not assume an a priori bound on initial ages.

Now use the oldest-B request and required known-B replies of the lemma
once all contacts are with learned responders. If an infinite unfinished
owner-only trajectory had all responder residuals strictly younger than
p both before and after every sufficiently late exchange, each such
exchange would either make p strictly oldest (and hence terminate at the
next activation), or decrease the owner's finite non-p head count.
Neither permits an infinite unfinished tail. Therefore that trajectory
must have infinitely many contacts violating at least one of the two
strict residual-age conditions.

This is a deterministic hypothetical-trajectory argument, not an event
of positive probability asserted for an infinite prescribed schedule.
It does not show how to exploit those residual-eligible contacts.
In particular, if peers other than a initiate during cooperative
preparation, their individual p-ages can increase; the coordinatewise
stabilization argument above no longer applies. Under exchanges that
reserve p at both endpoints the global p-age maximum is nonincreasing,
but this weaker fact is not a replacement proof of stabilization.
