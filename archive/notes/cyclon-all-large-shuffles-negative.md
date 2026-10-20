# Fixed-shuffle nonconvergence for every 3<=ell<=c under literal uniform sent-entry victims

## Exact scope

Fix integers c>=3 and 3<=ell<=c. Use the mandatory-removal model with iid uniform initiators, uniform oldest ties, uniform extra/reply subsets, and independent uniform eligible victim sets at the two endpoints. Duplicate descriptors are filtered before victim selection and their resident copies remain eligible sent-entry victims. All initial caches below are full and all descriptor ages are zero.

For all sufficiently large n there is a deterministic weakly connected initialization from which at least one observer's singleton peer law, conditional on availability, fails to converge to uniform on the other n-1 peers. The 2(c+2)-vertex core is strongly connected. The complete padded initialization is weakly connected, not asserted strongly connected.

## Construction

Let
 A={p,q,a_1,...,a_c}, B={v,w,b_1,...,b_c}, M=2(c+2), O={o_0,...,o_(n-M-1)}.
Use n>=3c+5, so |O|>=c+1. The caches are
 C_p={q,v,a_1,...,a_(c-2)},
 C_q={v,a_2,...,a_c},
 C_v={w,a_1,b_1,...,b_(c-2)},
 C_w={a_1,b_2,...,b_c}.
For every a_i, set C_(a_i)=A\{a_i,q}. For every b_i, set C_(b_i)=B\{b_i,w}, except replace b_1 by o_0 in C_(b_c). Every outside o_j stores its c cyclic successors in O. Every cache has exactly c distinct nonself identities; every age is zero.

A and B are individually strongly connected before the exchanges: every a_i points p, p points q and a_1, and q reaches all other a_i; the analogous B argument uses v,w, with b_c still pointing v after the boundary replacement. The core has cross arcs p,q->v and v,w->a_1, so it is strongly connected. The arc b_c->o_0 connects the outside cycle to it in the underlying undirected graph. No outside node initially knows any core identity.

Choose fixed sets
 R_A subset {a_2,...,a_(c-2)}, R_B subset {b_2,...,b_(c-2)},
with |R_A|=|R_B|=ell-3; these exist since ell<=c. For c=ell=3 they are empty.

## Two isolating exchanges

Let tau be the second initiation by a core node. The first two core initiators are v then p with probability1/M^2, independent of all intervening outside events. On this event no other core node initiates. Outside events remain confined to O, and neither prescribed exchange touches b_c as an endpoint; consequently the sole outward boundary descriptor cannot introduce outside addresses into any prescribed core buffer. The core states used next are therefore unaffected by all intervening outside activity.

First prescribe v->w, with extra buffer
 S_v={a_1,b_1} union R_B,
reply
 T_w={a_1,b_(c-1),b_c} union R_B,
initiator victim a_1 and responder victims {a_1,b_(c-1)}.
At v, a_1 and R_B are duplicates; exactly b_(c-1),b_c are new. Mandatory removal supplies one vacancy, and replacing a_1 supplies the second. Thus C_v becomes {b_1,...,b_c}.
At w, a_1 and R_B are duplicates; exactly fresh v and b_1 are new. Replacing {a_1,b_(c-1)} makes both insertions. All remaining w entries are in B. Therefore these two endpoints lose every A identity.

Next prescribe p->q, extra buffer
 S_p={v,a_1} union R_A,
reply
 T_q={v,a_(c-1),a_c} union R_A,
initiator victim v and responder victims {v,a_(c-1)}.
At p, v and R_A are duplicates; exactly a_(c-1),a_c are new, so C_p becomes {a_1,...,a_c}.
At q, v and R_A are duplicates; exactly fresh p and a_1 are new. The two specified victims remove its last B identity. Hence every A cache now contains only A identities, while every cache outside A contains no A identity. This separation is permanent under copying and self injection.

All prescribed packets have the required sizes. Each initiator's c old entries are tied. The extra buffer is chosen from c-1 entries, the reply from c entries, the initiator's one additional victim from ell-1 sent extras, and the responder's two victims from ell sent entries. Conditional on a prescribed initiator, each exchange therefore has probability
 beta=[c * binom(c-1,ell-1) * binom(c,ell) * (ell-1) * binom(ell,2)]^(-1).
The isolation event E has probability
 p_star=beta^2/M^2,
independent of n. Its completion time tau is almost surely finite. For c=ell=3, beta=1/18 and p_star=1/32400.

## Conditional marginal obstruction

Passive cache cardinality never decreases: j usable new entries add j slots and replace only max(0,j-vacancies) old entries. In particular, after any nonempty initiation its responder is nonempty: if already nonempty it stays so, and if empty it accepts the fresh nonself initiator. Thus at least one A cache remains nonempty forever after isolation. Empty initiations do nothing.

For i in A let alpha_i(t)=P(C_i(t) nonempty), nu_i,t be the singleton law conditional on availability, U_i uniform on V\{i}, and d_i(t)=TV(nu_i,t,U_i). Availability has positive probability at every finite t because the event i has never initiated has positive probability and passive updates cannot empty its initially nonempty cache.

On E intersect {tau<=t}, every available A sample lies in A\{i}, and at least one A peer is available. Consequently
 sum_(i in A) alpha_i(t) nu_i,t(A\{i}) >= P(E,tau<=t).
On the other hand U_i(A\{i})=(c+1)/(n-1), alpha_i<=1, and TV controls this event, giving
 sum_(i in A) alpha_i(t) nu_i,t(A\{i})
 <= (c+2)(c+1)/(n-1) + sum_(i in A) d_i(t).
Therefore
 liminf_(t->infty) sum_(i in A) d_i(t)
 >= p_star-(c+2)(c+1)/(n-1).
If n-1>(c+2)(c+1)/p_star, this is positive, so at least one fixed observer i in A fails to converge to the uniform conditional peer law. More precisely some i satisfies
 limsup_t d_i(t) >= [p_star-(c+2)(c+1)/(n-1)]/(c+2)>0.

Writing
 D=c * binom(c-1,ell-1) * binom(c,ell) * (ell-1) * binom(ell,2),
an explicit sufficient threshold is
 n >= max(3c+5, (c+2)(c+1)M^2D^2+2).
For c=ell=3 this is n>=648002.

## Interpretation

This is a counterexample for the stated literal duplicate-filter-then-uniform-victim completion, including every proper shuffle length3<=ell<c. It is not a claim about every implementation called CYCLON. Protecting resident identities that appeared in the incoming packet forbids the critical victims a_1 and v and excludes this construction. The result demonstrates an actual conditional marginal obstruction, rather than merely observing that disconnection can occur.
