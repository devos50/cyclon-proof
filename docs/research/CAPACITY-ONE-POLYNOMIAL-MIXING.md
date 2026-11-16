# Polynomial mixing at capacity one

## Status and scope

Internally independently audited working proof, not formal certification or external peer review. The standalone source is `paper/capacity-one-mixing.tex`.

For the adopted protected/MIN mandatory-removal algorithm with **c = shuffle length = 1**, fixed membership, independent uniform global initiators, atomic reliable exchanges, arbitrary weakly connected initialization, and arbitrary finite nonnegative integer ages, the note gives a polynomial worst-case **full-state** mixing bound. Conditional one-ID sampling follows with an explicit availability factor.

This does **not** establish polynomial mixing for capacity two or higher. The rate is deliberately loose and no optimality is claimed.

## Quantitative statement

For n >= 3 define N = n^(n-1) and G = 3 n² (n-1)² floor(n²/4). In global events:

`d(s+t) <= sqrt(N n) exp(-s/(n² G)) + n (1-1/n)^s + (sqrt(N)/2) exp(-t/G)`.

The manuscript gives explicit integer choices of s,t ensuring error at most epsilon. Their asymptotic size is `O(n^9 log(n/epsilon))`. On an initially rooted-tree overlay, the sharper bound is `O(n^7 log(n/epsilon))`. For n=2 the exact worst-case full-state error is `2^(-t)` for t >= 1.

Stationary availability of a one-ID sample is `(n-1)/n`; conditional error is at most `n/(n-1)` times full-state error. No cross-time independence follows.

A separately audited depth variational argument proves an **Omega(n^(3/2)) full-state mixing lower bound** for every fixed error below 1/2. It uses the exact Cayley-tree root-distance distribution and Dirichlet energy identity, not numerical spectral extrapolation. This lower bound is not claimed for a conditional local query; the polynomial upper bound is not tight.

## Proof mechanism

1. The zero-age rooted-tree chain is reversible and uniform. Each tree rotation is inverted by activating its former responder.
2. Compare it with the spanning-tree down-up walk, using the graphic matroid spectral gap from Anari, Liu, Oveis Gharan and Vinzant, *Log-Concave Polynomials II*, Theorem 1.1 and its matroid specialization: https://arxiv.org/html/1811.01816v3 . The transition convention was checked directly.
3. Implement every basis exchange in at most `3(n-1)` actual rotations/root moves. Every intermediate tree retains the same forest obtained by removing the exchanged edge. A weighted congestion count gives gap at least `1/G`.
4. Handle initial directed cycles by a killed-chain lift: delete one cycle edge to represent the state as a rooted tree plus a marked vertex. The rooted-tree Poincare bound gives a polynomial cycle-absorption estimate.
5. Independently bound extinction of initial descriptor tokens by `n(1-1/n)^s`. Capacity one transfers rather than branches these tokens; all young descriptors remain age zero. A deterministic-time union bound combines the two entrance estimates.

**Important correction preserved:** a directed cycle can grow when a branch vertex activates. Cycle length is not monotone, and old-token extinction alone does not imply tree entrance. The killed-chain lift, not either false assertion, supplies the entrance argument.

## Verification

Run:

```sh
python3 -B verification/verify_c1_polynomial_comparison.py --max-n 5
pdflatex -interaction=nonstopmode -halt-on-error paper/capacity-one-mixing.tex
```

The checker uses only Python's standard library and no external state files. It enumerates rooted trees by Prüfer codes and verifies all elementary down-up exchanges and root choices, transition endpoints, path lengths, the retained common forest, lift transition images, edge multiplicity, exact stationary depth counts, and the depth Dirichlet-energy identity. Finite checks corroborate, rather than replace, the arbitrary-n proof.

This add-only increment does not modify the general proof or promote its implicit all-capacity rate to a polynomial one.
