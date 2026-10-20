# Dense ell=3 saturation, including the c=3,n=5 endgame

Assume the independently audited dense owner-callback lemma and the existing
ell3 holder-only first-contact theorem. Work with ell=3 and c>=max(3,n-2).
Then the adopted protected MIN kernel has a common canonical atom, and hence
full convergence and uniform conditional sampling, for every allowed n,c in
this dense regime.

## Positive-copy zeroification with identity restoration

Fix a. Freeze owner a and all current a^0 holders I. The holder-only first
contact controller, starting from positive a copies, either contacts I and
refreshes a positive copy to0 without lowering total a-identity count, or
contacts owner a and removes one positive a copy at P. In the latter case
the owner caches fresh P^0, and P is now a nonholder.

Apply the dense owner-callback lemma with target P. Its macros never lower
N_a; the only possible temporary zero loss is restored by the next owner
activation. If it creates a zero at another positive holder, N_a may still be
one below its initial value, but P stays cached at the owner by dense
no-extra-eviction and remains nonzero. Apply the callback again. Each call
adds at least one zero, so after at most n-1 calls either P receives a (in a
preparation or directly) or all other nonowners are already zero and the next
outside contact must be P. Therefore N_a is restored and Z_a strictly grows.
All original zeros are preserved at macro endpoints.

In a closed class maximize Z_a, calling the maximum k. Repeated zeroification
shows that every class state has N_a<=k. At a maximizing state all a copies
are zero, so N_a=Z_a=k. The owner cannot cache a nonholder, since the callback
would increase Z_a. Thus C_a is contained in I.

## Holder-outward closure

There can be no cache edge from an I peer h to a nonholder x. Otherwise keep
only h active, always send a and x as extras, and until an outside-I response
prescribe replies containing a and h,x whenever known. The active a copy is
refreshed0, x is retained by dense no-extra-eviction, and owner a is never
selected because a0 is no older than retained x. First responders learn
h,a,x; repeats return exactly those three and shrink the active cache.
First visits can grow it by at most1, so a nonholder response eventually
occurs. It retains h's a identity and inserts a at the nonholder, giving
N_a>=k+1, contradiction.

Hence I has no outward residual edge. Reserve a0 and use the generic ell2
common-atom theorem on I components. Normalize each owner-oldest target's
component with that target as root, then a->root has only self-a in its reply
and deletes that owner head. Its extras lie inside I. This empties the owner
and preserves all zero anchors and residual component closures.

## Incoming-boundary contradiction for c>=4

If I is proper, weak connectivity and its outward closure, together with the
empty owner, supply a J->I edge, where J=V\(I union {a}) consists of
nonholders. Freeze I and owner; use ell3 first contact from J. Before the
terminal event no J peer can learn a. Pause just before terminal P->Q in I,
normalize Q's residual I-component with Q as root, and resume. Then C_Q={a0}.
The request has at most3 entries, so at c>=4 all fit beside the old anchor.
The active P receives a0, old Q keeps a0, and Z_a increases, contradiction.
For c=3,n=4 the same argument works because a nonholder can cache at most
n-2=2 identities, hence its request has at most2 entries and still fits.

## The only remaining dense case: c=3,n=5

Among the class states with maximal Z_a=k, empty owner, and the consequent
I-outward closure, choose one minimizing the number d of residual weak
components on I. Run and pause the same J->I first-contact path, and normalize
Q's component with Q as root. This preserves d and all extremal properties.

If P's request has at most2 entries, the preceding argument gives a zero gain.
Otherwise P's cache was exactly {Q,R,S}, with R,S distinct, and the outgoing
request is {P0,R^u,S^v}. The reply from Q is just a0. Thus the exact endpoint
is

    C_P={a0,R^u,S^v},     C_Q={P0,R^u,S^v}.

The old zero at Q is forced out by received-ID protection and capacity3;
P becomes the new zero. All other anchor copies and the empty owner are
unchanged. Thus N_a=Z_a=k remains true, with new zero set I'=(I\Q) union {P}.

If R or S was in old J, then new zero P caches an anchor-nonholder, violating
the already proved outward closure at this class state. Hence both R,S lie
in I\{Q}. If Q's normalized component had another peer, that peer caches Q
because the canonical component has root Q. It still is a zero holder, but Q
is now a nonholder: again outward closure is violated. Therefore Q's old
component was a singleton.

Removing that singleton lowers the component count by1. Adding P, which has
residual edges to R,S in the remaining components, creates no new component
and may merge two. Thus the new residual component count is strictly below d,
contradicting minimality. This handles c=3,n=5.

Consequently every closed class has a universal zero anchor. The established
universal-zero-anchor reduction for ell3 and the generic ell2 theorem give
common H(V,c), and finite-age reset plus empty-root padding yields uniform
geometric full-state convergence and conditional uniform samples.
