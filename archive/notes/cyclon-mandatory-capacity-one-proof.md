# Arbitrary-n capacity-one mandatory CYCLON: complete aged-chain theorem

n>=2, c=ell=1, iid uniform initiators, mandatory partner removal, no self/duplicate cache entries; duplicates do not refresh ages; empty initiators do nothing. Every weakly connected initial configuration with arbitrary finite nonnegative integer ages is allowed.

Represent identities by f(p) in (V\{p}) union {bottom}. If p is nonempty, put q=f(p), r=f(q). The identity update is:
- r=p: f'(p)=bottom and f'(q)=p (responder's duplicate unchanged).
- r=bottom: f'(p)=bottom and f'(q)=p.
- r distinct from p,q: f'(p)=r and f'(q)=p.
Other pointers do not change.

THEOREM. Let D=2n(n-1), delta=n^(-D). The full countable age-and-identity chain has a unique stationary law pi: uniform on all n^(n-1) labelled rooted spanning trees, with every descriptor age zero. For every weakly connected initial aged state x,
  ||P^t(x,.)-pi||TV <= (1-delta)^floor(t/D).
For each observer i, pi(f(i)=bottom)=1/n and pi(f(i)=j)=1/n for every j!=i. Thus conditional peer samples converge to uniform, with limiting availability1-1/n.

1. Weak connectivity is invariant. A nonreciprocal length-two path p->q->r is replaced by q->p->r, connecting the same three vertices. Contacting an empty root reverses the edge p-q. A reciprocal exchange removes only one of two opposite arcs, preserving their undirected edge.

2. Weakly connected functional graphs with outdegree<=1 consist either of one directed cycle (all vertices nonempty) with inward trees, or of a rooted spanning tree (exactly one empty vertex). This follows by following outgoing pointers; distinct terminal cycles/empty sinks cannot share a weak component.

3. A rooted tree remains rooted. If there is a cycle of length k>=3, activate a cycle vertex p: p->q->r becomes q->p->r and q leaves the cycle, reducing k by one. At cycle length2, activate one endpoint: mandatory removal makes it empty and produces a rooted tree. Thus every weakly connected identity state reaches the rooted-tree set in at most n-1 prescribed activations.

4. All rooted-tree identity moves are reversible. If p activates with parent q, initiating q in the result restores the prior state, including when q was the empty root. Marked transitions (f,p,g) pair bijectively with their reversed marked transitions (g,q,f). The empty-root initiation is a self-loop. Thus the iid-uniform identity kernel restricted to rooted trees is symmetric, and the uniform law is stationary.

5. Rooted-tree identity irreducibility and diameter. Fix an anchor a. Initially take its directed path to the empty root. If a vertex p lies outside that path but its parent q lies on it, activating p inserts p immediately after q on the path: q->r becomes q->p->r. This also works if r=bottom, when p becomes the new root. Such a p always exists unless the path is Hamiltonian. Thus <=n-1 moves produce a directed Hamiltonian path beginning at a.

If a directed Hamiltonian path has consecutive distinct vertices x,u,v followed by y (where y may be bottom), the word x,x,u,v swaps u,v and preserves all other outgoing edges:
                 f(x) f(u) f(v)
 initial           u    v    y
 x                 v    x    y
 x,x               y    x    x
 x,x,u             u    y    x
 x,x,u,v           v    y    u
All moves are valid in rooted trees, including y=bottom. Adjacent swaps among the n-1 vertices following anchor a generate all anchored Hamiltonian paths. At most (n-1)(n-2)/2 swaps are needed; each costs four moves. Reversing the insertion path of the target tree yields rooted-tree diameter <=2(n-1)+2(n-1)(n-2)=2(n-1)^2.

6. In a rooted tree, every positive-age descriptor disappears when its current carrier initiates. The initiator's age-incremented descriptor is removed; the responder's old descriptor, if present, transfers to the initiator, and the responder installs a fresh age-zero initiator descriptor. No descriptor is copied, and no retained age is increased. The number of positive-age descriptors therefore decreases by exactly one when a positive carrier initiates, and never increases. At most n-1 prescribed activations reset every age to zero. Age-zero states are closed under the rooted-tree dynamics.

7. Common atom. First reach a rooted tree (<=n-1 moves), reset ages (<=n-1), then reach a fixed rooted star z with age zero (<=2(n-1)^2). Total <=D=2n(n-1). Pad with z's empty-root no-op to exactly D steps. Every prescribed initiator has probability1/n, giving P^D(x,{z})>=n^(-D)=delta uniformly. Doeblin contraction gives existence, uniqueness and the claimed full-state bound. The stationary law from step4 with ageszero is invariant, hence it is the unique pi.

8. Cayley's formula gives n^(n-1) rooted labelled trees. Uniform relabelling makes the root uniform, so P(f(i)=bottom)=1/n. Permutations fixing i act transitively on other identities, giving pi(f(i)=j)=((n-1)/n)/(n-1)=1/n. Conditional uniformity follows.
