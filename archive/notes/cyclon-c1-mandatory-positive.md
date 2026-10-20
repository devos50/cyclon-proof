# Arbitrary-n theorem: mandatory CYCLON with c=ell=1

Let n>=2, reliable atomic exchanges, iid uniform initiators, finite nonnegative integer ages, mandatory partner removal, and duplicate discard without refresh. Start from any weakly connected cache graph (each cache empty or singleton). Set

    L = 2n^2+n-3,    delta = n^(-L).

There is a unique stationary distribution on the weakly connected state space: uniform over the all-age-zero directed rooted labelled trees, with edges directed toward the unique empty-cache root. Moreover

    ||P^t(x,.) - pi||TV <= (1-delta)^floor(t/L).

The stationary probability that peer i is empty is 1/n. Conditional on nonemptiness, its cached identity is uniform among the other n-1 peers. Thus the unconditional stationary output gives probability 1/n to every other identity and probability 1/n to the unavailable symbol.

## Exact move

Write f(p)=q, and r=f(q), allowing r=bottom. If p empty, nothing happens. Otherwise the mandatory update is:

    if r=p: f'(p)=bottom, f'(q)=p;
    otherwise: f'(p)=r, f'(q)=p.

Only these two entries change. There is no age choice because each nonempty cache has one descriptor.

## Connected states reach zero-age rooted trees within 2(n-1) moves

A connected partial functional graph is either a directed rooted tree (n-1 arcs, one empty vertex) or a connected total functional graph (n arcs, one directed cycle). A cycle has length at least two. If its length is m>=3, activating a cycle vertex p replaces cycle segment p->q->r by p->r and q->p: q leaves the cycle and its length decreases by one. At length two, activating either endpoint removes one reciprocal arc, producing a rooted tree. At most n-1 activations suffice.

Once a rooted tree has been reached, it stays a rooted tree. Every nontrivial move is inverted by activating q in the resulting tree; this includes q initially empty, where the move reverses the p-q edge and transfers the root to p.

Now mark every positive-age descriptor. During a capacity-one activation the initiator's incremented descriptor is removed. The responder's descriptor, if present, moves to the initiator and is replaced by a fresh age-zero self descriptor. No marked descriptor is copied. Choosing a marked holder as initiator therefore reduces the number of marked descriptors by exactly one. At most n-1 further activations clear all positive ages. Once all ages are zero they remain zero.

## Every zero-age rooted tree reaches one fixed zero-age Hamiltonian path

Start with a current directed path consisting only of the root. Whenever an off-path vertex remains, there is an off-path p whose parent q lies on the path. Activating p inserts p between q and its previous parent; if q was the root, p becomes the new root. Thus at most n-1 moves produce a Hamiltonian path.

Any two Hamiltonian path orders can be related by adjacent transpositions, at most n(n-1)/2 in total. The first two vertices a,b can be swapped with one activation of a: a->b->y becomes b->a->y, including y=bottom.

For an interior pair, write the path segment x->a->b->y, where y may be bottom. The four activations x,x,a,b produce:

    (f(x),f(a),f(b))
    (a,b,y)
    (b,x,y)
    (y,x,x)
    (a,y,x)
    (b,y,a).

This swaps a,b and preserves every other outgoing edge. It also works when b is the root (y=bottom), with intermediate empty vertices treated as roots.

Sorting a Hamiltonian path into the fixed order 1->2->...->n therefore costs at most 2n(n-1) moves. Combined with tree-to-path insertion, at most (n-1)+2n(n-1) moves suffice from any zero-age rooted tree.

Including the initial tree/age reduction yields at most

    2(n-1)+(n-1)+2n(n-1)=2n^2+n-3=L

moves from any admissible aged state to the same atom z. Shorter paths can be padded to exactly L by activating z's empty root. Each prescribed initiation has probability 1/n, so

    P^L(x,{z}) >= n^(-L)=delta.

## Stationarity and outputs

The zero-age rooted-tree identity chain is finite and irreducible by the construction above and inverse moves. Pair each marked transition (f,p,T_p f) with its reverse (T_p f,q,f), where q=f(p). Root activations are self-loops. Therefore its transition matrix is symmetric and its stationary law is uniform.

The uniform minorization over the entire countable weakly connected state space gives the displayed total-variation bound and uniqueness. Relabelling invariance and the unique root imply pi(root=i)=1/n. Permutations fixing i act transitively on the other labels, so pi(f(i)=j)=1/n for every j!=i.

If e_t denotes the full-state TV bound and the conditional output is defined, its distance from the uniform law on other peers is at most n*e_t/(n-1). Availability tends to (n-1)/n. For t>=L, availability is positive for every observer by applying the same common-atom construction to a path whose root is some other vertex.
