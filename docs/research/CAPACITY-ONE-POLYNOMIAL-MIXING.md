# Polynomial mixing at capacity one

## Status and scope

Internally independently audited working proof, not formal certification or external peer review. The standalone source is `paper/capacity-one-mixing.tex`.

For the adopted protected/MIN mandatory-removal algorithm with **c = shuffle length = 1**, fixed membership, independent uniform global initiators, atomic reliable exchanges, arbitrary weakly connected initialization, and arbitrary finite nonnegative integer ages, the note gives a polynomial worst-case **full-state** mixing bound. Conditional one-ID sampling follows with an explicit availability factor.

This does **not** establish polynomial mixing for capacity two or higher. The rate is deliberately loose and no optimality is claimed.

## Quantitative statement

For n >= 3 define N = n^(n-1) and H = n(n-1)²/2 and G = 3 n² (n-1) min{(n-1)floor(n²/4), 2n-1}. In global events:

`d(s+t) <= sqrt(N n) exp(-s/H) + n (1-1/n)^s + (sqrt(N)/2) exp(-t/G)`.

The manuscript gives explicit integer choices of s,t ensuring error at most epsilon. Their asymptotic size is `O(n^5 log(n/epsilon))`. The same asymptotic bound covers initially rooted-tree overlays. For n=2 the exact worst-case full-state error is `2^(-t)` for t >= 1.

Stationary availability of a one-ID sample is `(n-1)/n`; conditional error is at most `n/(n-1)` times full-state error. No cross-time independence follows.

A separately audited depth variational argument proves an **Omega(n^(3/2)) full-state mixing lower bound** for every fixed error below 1/2. It uses the exact Cayley-tree root-distance distribution and Dirichlet energy identity, not numerical spectral extrapolation. This lower bound is not claimed for a conditional local query; the polynomial upper bound is not tight.

## Proof mechanism

1. The zero-age rooted-tree chain is reversible and uniform. Each tree rotation is inverted by activating its former responder.
2. Compare it with the spanning-tree down-up walk, using the graphic matroid spectral gap from Anari, Liu, Oveis Gharan and Vinzant, *Log-Concave Polynomials II*, Theorem 1.1 and its matroid specialization: https://arxiv.org/html/1811.01816v3 . The transition convention was checked directly.
3. Implement every basis exchange in at most `3(n-1)` actual rotations/root moves. Every intermediate tree retains the same forest obtained by removing the exchanged edge. A root-aware weighted congestion count gives gap at least `1/G`: a slide fixes one attachment endpoint, and the central root crossing fixes both.
4. Handle initial directed cycles by a killed-chain lift: delete one cycle edge to represent the state as a rooted tree plus a marked vertex. Restricting the lift to root reversals at fixed tree and mark gives a path Poincare bound. Each projected edge has one lift, yielding a cycle-absorption exponent `1/H`, independent of the tree mixing rate.
5. Independently bound extinction of initial descriptor tokens by `n(1-1/n)^s`. Capacity one transfers rather than branches these tokens; all young descriptors remain age zero. A deterministic-time union bound combines the two entrance estimates.

**Important correction preserved:** a directed cycle can grow when a branch vertex activates. Cycle length is not monotone, and old-token extinction alone does not imply tree entrance. The killed-chain lift, not either false assertion, supplies the entrance argument.

## Verification

Run:

```sh
python3 -B verification/verify_c1_polynomial_comparison.py --max-n 5
pdflatex -interaction=nonstopmode -halt-on-error paper/capacity-one-mixing.tex
```

The checker uses only Python's standard library and no external state files. It enumerates rooted trees by Prüfer codes and verifies all elementary down-up exchanges and root choices, transition endpoints, path lengths, the retained common forest, lift transition images, edge multiplicity, exact stationary depth counts, the depth Dirichlet-energy identity, root-aware slide constraints, and multiplicity-one root-only lift mapping. Finite checks corroborate, rather than replace, the arbitrary-n proof.

This capacity-one result does not modify the general proof or promote its implicit all-capacity rate to a polynomial one.

## Root-aware refinement

This refinement improves the former `O(n^9 log(n/epsilon))` upper bound to `O(n^5 log(n/epsilon))` without changing the model or lower bound. It removes overcounting in canonical-path congestion and avoids invoking whole-tree mixing merely to create an empty root. The published exponent is still a loose upper bound, not an estimate of typical runtime.
