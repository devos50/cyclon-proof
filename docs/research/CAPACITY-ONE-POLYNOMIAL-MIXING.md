# Polynomial mixing at capacity one

## Status and scope

Internally independently audited working proof, not formal certification or external peer review. The standalone source is `paper/capacity-one-mixing.tex`.

For the adopted protected/MIN mandatory-removal algorithm with **c = shuffle length = 1**, fixed membership, independent uniform global initiators, atomic reliable exchanges, arbitrary weakly connected initialization, and arbitrary finite nonnegative integer ages, the note gives a polynomial worst-case **full-state** mixing bound. Conditional one-ID sampling follows with an explicit availability factor.

This does **not** establish polynomial mixing for capacity two or higher. The rate is deliberately loose and no optimality is claimed.

## Quantitative statement

For n >= 3 define N = n^(n-1) and H = n(n-1)²/2 and G = 3 n² (n-1) min{(n-1)floor(n²/4), 2n-1}. In global events:

`d(s+t) <= sqrt(N n) exp(-s/H) + n (1-1/n)^s + (sqrt(N)/2) exp(-t/G)`.

The manuscript gives explicit integer choices of s,t ensuring error at most epsilon. The original spectral choices have size `O(n^5 log(n/epsilon))`. A classical logarithmic Sobolev refinement now improves the strongest upper bound to `O(n^4 [log² n + log(1/epsilon)])`, including arbitrary weakly connected finite-age initialization. The source gives the explicit smoothing and spectral-decay times, with negative eigenvalues handled separately. For specific parameters, take the smaller of the spectral and entropy sufficient times. For n=2 the exact worst-case full-state error is `2^(-t)` for t >= 1.

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

## Classical logarithmic Sobolev refinement

The strongest current upper bound is `O(n^4 [log² n + log(1/epsilon)])` global events, not merely the earlier spectral `O(n^5 log(n/epsilon))` bound. It remains far from the `Omega(n^(3/2))` full-state lower bound.

The additional primary-source inputs are:

- Cryan, Guo and Mousa, *Modified log-Sobolev inequalities for strongly log-concave distributions*, Lemma 11 / equation (32): https://arxiv.org/html/1903.06081v3 . The proof uses their **half-step entropy factorization**, not an unjustified comparison of modified logarithmic Sobolev forms along paths.
- Diaconis and Saloff-Coste, *Logarithmic Sobolev inequalities for finite Markov chains*, Theorem 3.5(ii): https://pi.math.cornell.edu/~lsc/papers/log-aoap.pdf . The classical inequality has the convention `alpha = inf E(f,f)/Ent(f²)`, hence hypercontractivity exponent `4 alpha`.

A new elementary completion-space entropy bound converts the factorization into a classical inequality, which the already audited squared-difference path comparison can transfer. Continuous-time hypercontractivity is used only to bound positive spectral components in L². Negative eigenvalues are separately controlled using holding probability `1/n`; the final result is for the original discrete-event chain, not a change of scheduler.

No claim for capacity two or higher, optimality, or matching local-query lower bound is added. The checker additionally exercises the elementary uniform-space entropy inequality on deterministic test vectors; these numerical checks do not replace its analytic proof or the cited theorems.
