# A complete convergence proof for the one-entry CYCLON projection

This theorem concerns cache capacity and shuffle length `c = ell = 1`. Its identities follow the original replacement semantics: keep the current entry when the reply is self or a duplicate. It does not concern a variant that unconditionally deletes the partner before the exchange. Descriptor ages have no influence when each nonempty cache contains only one entry.

## Model

Let `U = {1,...,n}`, `n >= 2`. A state is a function `f: U -> U` with `f(i) != i`; node `i`'s cache consists of `f(i)`. Assume the undirected graph of `f` is connected. At each atomic step choose `p` uniformly and independently from `U`, put `q=f(p)` and `r=f(q)`, and apply

- If `r=p`, leave `f` unchanged.
- If `r != p`, replace `f(p)` by `r` and `f(q)` by `p`, leaving all other values unchanged.

Write this operation `T_p` and its transition kernel `P`.

## Theorem

For every fixed observer `i`, every initial connected state `f`, and every `j != i`, the probability `Pr_f[f_t(i)=j]` tends to `1/(n-1)`.

For `n >= 4`, put `D=2n(n-2)` and `delta=n^(-D)`. Then

`||Law_f(f_t(i))-Unif(U\{i})||_TV <= (1-delta)^floor(t/D)`.

For `n=3` the right side may be replaced by `(8/9)^floor(t/2)`. For `n=2` the distance is identically zero.

## Proof for n >= 4

### 1. The state space is invariant

Nontrivial updates have three distinct vertices `p,q,r`, so introduce no self-loop. In the underlying undirected graph the connected path `p-q-r` becomes the connected path `q-p-r`. All other edges remain. Thus weak connectivity is preserved.

### 2. Every move has an equally likely inverse

If `g=T_p f != f` and `q=f(p)`, then `g(q)=p` and `g(p)=r`, so `T_q g=f`. The association between a transition choice `(f,p)` and its inverse `(g,q)` is a bijection, and every choice has probability `1/n`. Consequently `P(f,g)=P(g,f)`. In particular, the uniform distribution on any communicating component is stationary.

### 3. Every state reaches a Hamilton directed cycle in at most n-2 steps

A connected functional digraph has exactly one directed cycle, of length at least two, with directed trees feeding into it. If not all vertices are on the cycle, choose a tree vertex `p` whose parent `q=f(p)` lies on the cycle, and set `r=f(q)`. Since `p` is off the cycle, `r != p`. Operation `T_p` replaces the cycle arc `q->r` by `q->p->r`, inserting `p` into the cycle. Repeat until the cycle contains every vertex.

### 4. All Hamilton directed cycles communicate

Consider four consecutive distinct vertices `x,a,b,y` on a Hamilton cycle, with arcs `x->a->b->y`. Apply the word

`T_x, T_x, T_a, T_b`.

The successive affected arcs are:

1. `x->b`, `a->x`, `b->y`;
2. `x->y`, `a->x`, `b->x`;
3. `x->a`, `a->y`, `b->x`;
4. `x->b`, `b->a`, `a->y`.

All other arcs remain unchanged. This swaps adjacent vertices `a,b` in the cyclic ordering. All four operations are nontrivial, including for `n=4`, where the intermediate remaining cycle is a two-cycle.

Fix vertex `1` as the first vertex of the cyclic list. Adjacent swaps among the remaining `n-1` vertices connect all Hamilton cycles, using at most `binom(n-1,2)` swaps, or `2(n-1)(n-2)` elementary operations.

Together with Step 3 and reverse moves, this proves irreducibility and bounds the distance between any two connected states by

`2(n-2)+2(n-1)(n-2)=2n(n-2)=D`.

### 5. A common atom gives a quantitative bound

Choose the state `s` with `s(1)=2`, `s(2)=1`, and `s(j)=1` for `j>=3`. It has a self-loop, obtained by choosing actor `1`. Every state has a path to `s` of length at most `D`; pad it with actor-1 self-loops at `s` to length exactly `D`. Every specified actor word has probability `n^(-D)`. Hence

`P^D(f,{s}) >= delta=n^(-D)` for every state `f`.

Thus `P^D(f,.) >= delta delta_s(.)`. The residual kernels have mass `1-delta`, so total variation contracts by at most `1-delta` every `D` steps. Since the finite irreducible symmetric chain has uniform stationary law `pi`,

`||P^t(f,.)-pi||_TV <= (1-delta)^floor(t/D)`.

### 6. The stationary local sample is uniform

The connected state space is invariant under all permutations of peer identities. The uniform stationary law is therefore invariant under all permutations fixing `i`. Such permutations act transitively on `U\{i}`, forcing `pi(f(i)=j)=1/(n-1)` for every `j!=i`. Projection cannot increase total variation, proving the claim.

## The case n=3

There are eight connected loop-free functional states. They form two communicating classes, each consisting of a directed three-cycle `h` and its three images `T_p h`. Each class has the transition graph of a four-state star: the center moves to each leaf with probability `1/3`; each leaf returns to the center with probability `1/3` and stays with probability `2/3`. Its stationary law is uniform on the four states. For any observer, two of the four states point to each of the other two identities, so its stationary sample is uniform.

Fix any leaf `s` of the class. Every state reaches `s` in two steps with probability at least `1/9` (padding at the leaf when necessary). Thus the same minorization argument gives the stated `(8/9)^floor(t/2)` bound. Full-state convergence to a common stationary law across both classes is false, despite local uniformity.

## The case n=2

The unique state is `1->2`, `2->1`, so the sole admissible peer is sampled with probability one at every time.

## Limitations

The upper bound is intentionally coarse and establishes existence of finite-time convergence. It is not a practical mixing estimate, and it does not prove enhanced CYCLON convergence for multi-entry caches. For `c>1`, oldest-first partner selection and duplicate-sensitive cache updates reintroduce the unbounded-age and graph-coupling difficulties.
