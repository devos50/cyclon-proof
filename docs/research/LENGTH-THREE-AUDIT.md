# General three-entry proof audit record

16 November 2026. Internal mathematical review of a working proof, not formal verification or external peer review.

## Accepted scope

The actual manuscript text of `lem:threegeneralcallback`, `cor:threegeneralzeroify`, `lem:threeownerterminalgain`, `lem:threesparseoutwardgain`, and `thm:threegeneraluniform` received independent local, end-to-end, and final-transcription reviews. No remaining material gap was identified.

The theorem covers every allowed `n>=4`, `3<=c<=n-1`, at **fixed shuffle length three**, under the adopted protected/MIN kernel and iid uniform initiators. Initially underfull weakly connected states and arbitrary finite nonnegative integer ages are allowed. It supplies implicit uniform geometric convergence and conditional uniform sampling, not polynomial or practical mixing bounds. Lengths four and above remain open.

## Specific checks and repairs

- The callback's fair extra/reply choices are prescribed controls used to construct a finite path, not fairness assumptions about an infinite random execution.
- After finite learning and cache-growth phases, the residual-age multiset is genuinely closed under the specified transfers. Passive minimum copies are eventually selected, and the recurrent identity set becomes residually closed.
- Restarts cannot introduce infinitely many head increases: each is charged to a first learning, and clearing preserves the learned set.
- Sparse outward progress uses a **fixed identity set**, not an ambiguous lineage color. Its bounded lexicographic potential accounts for changing the distinguished current holder and for migration into an underfull cache.
- In the unknown-initiator zero-holder case, an extra B already known by the responder **must be returned**. This protects its active copy. Omitting this branch can invalidate strict potential growth; the proof and targeted regression explicitly include it.
- Victims used to compensate potential losses are chosen from replied identities absent at the active cache, so they are transferred to genuinely new locations rather than duplicate-merged without compensation.
- Direct nonholder gain with one overlapping reply identity uses a **different** sent extra as victim; this needs capacity at least four. Capacity three has its separate proof.
- With partial three-entry replies, owner-directed routing explicitly requests both the primary anchor and the next path head. Neither is presumed to be returned automatically from a larger cache.
- The owner-restoration gadget explicitly requires the primary anchor in the holder's partial reply.
- Residual normalization uses effective capacity `min(c-1,m-1)` and length `min(2,m-1)`, not capacity two at every component.
- Closed-class accessibility follows from the finite reset family's reachability graph, not assumed irreducibility or aperiodicity. The minorization minimum is taken after empty-root padding.

## Verification boundary

Exact controlled-path checkers corroborate the callback, restoration, potential and age-budget identities, with underfull caches, large ages, and explicit failure-sensitive regressions. These finite checks are not the proof of arbitrary-network convergence. The symbolic finite-path arguments and the independent audit of all invoked prior results supply that argument.

Final validation: the complete maintained suite passed **40/40** checks. Repository/index/whitespace checks passed, and two TeX draft-mode passes had no undefined or multiply-defined references and no LaTeX errors. No final PDF is claimed from this environment.
