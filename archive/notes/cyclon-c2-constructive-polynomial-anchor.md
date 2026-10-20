# Constructive c = ell = 2: polynomial controlled common-atom path

UPDATE: The O(n^4) coarse bound below sharpens immediately to O(n^3), as
independently observed by the finite_abstraction agent. In the only
non-gain boundary branch, Q is an isolated residual component. Its
normalization therefore requires ZERO events, and that branch costs only
the one P->Q exchange. At most k-1 such events precede the one final gain
attempt, whose normalization costs at most D. Thus replace the phase
budget G below by

    G3 = E+(n-1)+D+6 = 3D+n+7.

The positive-copy gain blocks and all-zero propagation blocks all strictly
increase the SAME zero count, so there are at most n-1 such gain blocks
combined, not n-1 of each. The only possible extra initial event is creating
a zero when no a descriptor exists anywhere. With the sharper D below,

    1+(n-1)G3+C = 6n^3-15n^2+16n-8 <= 6n^3.

Even using D=2n(n-1) instead of the sharper 2(n-1)(n-2) gives total
6n^3-3n^2+8n-12<=6n^3. Hence L=8n^3 is a conservative audited choice.
With the safe per-event probability 1/(4n), one may report

    Gamma=(4n)^(-8n^3),
    t_mix(epsilon)<=8n^3 ceil(Gamma^(-1) log(1/epsilon))
                  = exp(O(n^3 log n)) log(1/epsilon),

up to the ceiling's additive term. The later sections record the original
coarser count and detailed local reasoning, which remains valid.

This is a candidate strengthening of the existing draft proof. It uses exactly
the adopted algorithm and all ages may initially be arbitrary finite integers.
There is no finite-family enumeration, reset, or closed-class maximum in the
argument below. Its local gadgets are existing lemmas in main.tex.

## Constants and the capacity-one subroutine

Fix the intended final empty root / anchor identity a. Put

    S = (n-1)(n+1) = n^2-1,
    D = 2(n-1)(n-2).

Theorem mandatoryone sends any weakly connected capacity-one component of m
vertices to the zero-age star with any prescribed root in at most 2m(m-1)
non-noop exchanges. Thus any residual component on at most n-1 vertices can
be normalized in at most D events. When every member stores a^0, the
anchor-reduction simulation implements this subroutine exactly and preserves
all those zeros. Global-scheduler probability will be assessed separately;
do not use a reduced scheduler probability.

## 1. Eliminate positive a copies with bounded strict zero-count gains

Let I denote the current set of a^0 holders and k=|I|. Suppose p stores a^A,
A>0. This is not an I member. If its actual oldest partner is a, contact a.
The owner now caches fresh p^0; since p was not a zero holder, sourcegain
applies and raises k in at most S additional owner events. No old I member
is lost.

Otherwise its cache is exactly {a^A,u^B} and u is oldest. The full request
{p^0,a^(A+1)} forces C_u={p^0,a^b}. If u was a zero holder, b=0 and its
full pre-exchange reply gives p an a^0 copy: k has increased immediately,
with the old zero at u protected. Otherwise b>0, so u was not a zero holder
and its next activation necessarily selects owner a (a^b vs p^0). After
u->a, the owner caches fresh u^0 and sourcegain raises k. These first two
events touch no old zero holder. Thus each positive-copy block costs at most
S+2=n^2+1 and raises k strictly.

Repeat while any positive a copy remains: at most n-1 such blocks are
possible. If there is initially no a descriptor at all, weak connectivity
forces the owner's cache to be nonempty, and one owner activation creates
a zero copy; no positive a is created. We may conservatively allocate

    Z = 1+(n-1)(n^2+1) = n^3-n^2+n

events for this stage. At its endpoint all a descriptors are zero and k>=1.

## 2. Increase k while preserving the all-a-zero property at the endpoint

Assume all a descriptors are zero and k<n-1. If a directed path from a
reaches a nonmember of I union {a}, sourcegain raises k in at most S events.
Because the owner alone initiates, all a descriptors remain zero.

Otherwise the directed reachable set R from a lies in I union {a}; R is
out-closed. Empty C_a using at most two iterations: choose an oldest q in
C_a, normalize q's residual capacity-one component inside R\{a} with q as
root, so C_q={a^0}, then activate a->q. Its only reply is a self identity,
so the owner loses q and receives no usable entry. At q the incoming fresh
a and at most one extra fit capacity two. All zeros survive and outside R
is frozen. Each normalization costs at most D, so this costs at most

    E = 2(D+1).

Now C_a is empty. If a zero holder p caches a nonholder x, apply the
four-exchange infection gadget. Its endpoint preserves the old zero holders
and adds x; all a descriptors are again zero. This costs four events.

Otherwise every I cache is a^0 plus at most one residual identity in I.
Let d be the number of weak residual components on I. Weak connectivity
provides P in J=V\(I union {a}) caching Q in I. Inspect an actual oldest
partner of P and freeze P while normalizing Q's residual component with Q
as root, at cost at most D.

* If P's oldest partner u lies in J, P has {u,Q}. Run P->u, then u->Q.
  Full received protection makes C_u={P^0,Q^b} after the first step, so
  Q is legal oldest on the next step. Root Q replies only a^0. At the
  endpoint k is unchanged: u becomes a zero holder, Q loses its zero;
  owner a is empty, P remains a nonholder, and u stores a^0 plus P^1.
  Four-exchange infection u,P raises k. All a copies are zero at the
  endpoint. Cost at most D+6.

* Otherwise P's oldest is Q in I. If P is singleton, P->Q gains a zero
  and Q keeps its own: cost at most D+1. If P={Q,X}, the exchange P->Q
  replaces Q by P in the zero set, and C_P={a^0,X^(A+1)}. Q's incoming
  pair is {P^0,X^(A+1)} and contains no a. If X was in J, apply infection
  P,X and gain. If X was in I and Q's normalized residual component had
  another member v, then C_v={a^0,Q^0} with Q now a nonholder; apply
  infection v,Q and gain. Either cost is at most D+5.

* Sole remaining case: Q was an isolated residual component and X was in
  another I component. Replacing isolated Q by P with its edge P->X reduces
  d by exactly one. The owner stays empty, all a descriptors stay zero,
  k is unchanged, and every residual I' identity still lies inside I'.
  There were no other I->Q residual edges, because Q was isolated.
  Thus this case can be repeated, without further owner clearing, at most
  k-1 times before one of the gain cases must occur.

Consequently at most k normalization/boundary attempts, each <=D+6 events,
give a strict k gain. A uniform per-gain budget is

    G = 2(D+1)+(n-1)(D+6) = 2n(n^2-2n+2).

It also dominates S and the direct four-event infection case for n>=3.
At most n-1 gains therefore produce a universal zero anchor in
Z+(n-1)G events from any initial aged connected state.

## 3. A fully explicit canonicalization budget

From a universal zero anchor, empty C_a at cost E. Normalize every residual
component to a zero-age rooted star. The sum of the capacity-one budgets
2m(m-1) over a partition of n-1 is at most D. Merge the component roots
using the existing four-exchange table, at most n-2 times. Finally normalize
the connected residual graph to the star rooted at the desired second-last
label, at cost at most D. The result is exactly H(V,2) with a last.
Thus

    C = E + 2D + 4(n-2) = 4D+4n-6.

The full controlled length is at most

    L0 = Z+(n-1)G+C
       = 2n^4-5n^3+15n^2-23n+10
       <= 2n^4, for n>=3,

since 2n^4-L0 = 5n^2(n-3)+23n-10>0. Pad at the empty root to L=2n^4.

## 4. Probability of prescribed outcomes for c=ell=2

Every prescribed one-event outcome has probability at least 1/(2n), which
is much sharper than the general 1/(nc^5) bound:

* A degree-two initiator has at most two oldest ties. Its request and the
  full pre-exchange reply are otherwise forced. Both incoming request
  identities are valid and protected at the responder, forcing its complete
  cache, and any active victim is the unique sent extra. Hence all other
  identity/victim choices are deterministic.
* A degree-one initiator has no oldest tie and sends only itself. Only the
  responder may make a binary victim choice, if its cache was full and did
  not already contain that initiator. The initiator receives at most two
  entries into its newly empty cache.
* Empty-root padding has probability 1/n.

Thus the common-atom claim is

    P^L(x,{H(V,2)}) >= (2n)^(-L),  L=2n^4,

uniformly over arbitrary finite initial ages. This gives the deliberately
coarse explicit full-state mixing estimate

    t_mix(epsilon) <= L ceil((2n)^L log(1/epsilon))
                   = exp(O(n^4 log n)) log(1/epsilon).

For precision around epsilon close to 1, include the additive L term from
the ceiling.

## 5. Conditional one-identifier sampling has only a constant-factor cost

Every connected overlay has at least n-1 undirected edges, hence at least
n-1 directed cache entries. Since each nonempty cache has at most two
entries, at least (n-1)/2 peers have nonempty caches in every state.
Stationary relabelling symmetry therefore yields, for each observer i,

    p_i = pi(C_i nonempty) >= (n-1)/(2n) >= 1/3.

For arbitrary probability laws mu,nu and event A with both conditioning
probabilities positive,

    TV(mu(.|A),nu(.|A)) <= TV(mu,nu)/nu(A).

Indeed, splitting the signed restriction mu-nu to A into masses a_+ and
a_-, the usual normalization triangle bound equals
(a_++a_-+|a_+-a_-|)/(2nu(A))
=max(a_+,a_-)/nu(A)<=TV(mu,nu)/nu(A).

Apply the local query kernel (including its availability flag), which
contracts TV. The stationary conditional identifier is uniform by label
symmetry, and the finite-time conditional query error is consequently at
most 3(1-gamma)^floor(t/L) whenever the query is available with positive
probability. For t>=L positivity follows by choosing a relabelled canonical
atom whose empty root differs from i. Thus a sufficient bound is

    t_sample(epsilon) <= L ceil(gamma^(-1) log(3/epsilon)).

## What remains to audit

Check the constructive use of each existing infection branch without
maximality, especially that the failed component-decrease branch preserves
all-a-zero and residual closure. Temporary zero losses in the J->I contact
are permitted: strict improvement is only required at macro endpoints.
Check E and C subroutine budgets and the sharp per-event 1/(2n) bound.

No claim of a useful polynomial mixing time is made. The polynomial length
is a worst-case specially controlled path; following it at random costs an
exponentially small probability.
