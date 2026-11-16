# Uniform query marginals need not be preserved for one event

Scoped exact obstruction, 16 November 2026. This concerns the adopted
oldest-first protected/MIN kernel, not the different basic-shuffle model in
Busnel, Beraldi and Baldoni. It does **not** contradict eventual convergence.

## Statement

For every `n>=3` and every shuffle length `1<=L<=n-1`, at capacity `c=n-1`
there is a deterministic connected initial state in which every observer's
age-blind sample is exactly uniform, but a specified observer's one-event
conditional sample is nonuniform for every `1<=b<=n-2`.

Fix observer `i` and another identity `j`. Initially every cache contains
all other peers. Give `j` a uniquely largest age in `i`'s row; all ages may
be chosen from `{0,1}`. Other rows' ages do not matter. One convenient test
family gives every peer `v` its successor modulo `n` as unique oldest.
All initial ordered samples are uniform because the rows are complete.

In an exchange initiated by `p` toward its oldest `q`, no merge can overflow
capacity `n-1`. The active row deletes `q` unconditionally and can never
receive `q` back from `q`'s own cache (self identities are forbidden).
Every other valid received identity is already resident. Thus its final
identity set is exactly `V minus {p,q}`. The responder's identity set
remains complete. These facts do not depend on the legal packet subsets,
shuffle length, or duplicate MIN ages.

Consequently, after one iid-uniform activation the observer `i` has the
complete row with probability `1-1/n`, and exactly `V minus {i,j}` with
probability `1/n`. For `1<=b<=n-2`, availability remains one, and its ordered
sample law is

    (1 - 1/n) U_b(V minus {i}) + (1/n) U_b(V minus {i,j}).

Here `U_b(A)` denotes the uniform law on ordered distinct `b`-tuples from
`A`. Under the first uniform law, the probability of including `j` is
`b/(n-1)`. The second law is exactly the first conditional on excluding
`j`. Hence the exact total-variation error is

    b / (n(n-1)) > 0.

For `b=n-1`, availability instead drops to `1-1/n`; conditional on
availability, the ordered output remains uniform.

For a single sample, the explicit probabilities are

    P(S_i(1)=j) = 1/n,
    P(S_i(1)=k) = (n-1)/(n(n-2)),  k != i,j.

The uniform comparator is `1/(n-1)` for every `k != i`.

## What this rules out

For any fixed `1<=b<=n-2`, a nonnegative potential depending only on the
current query law, vanishing
exactly at the uniform law, cannot be universally nonincreasing under the
adopted kernel: it starts at zero here and becomes positive. In particular,
a direct import of a max-marginal preservation/attraction proof would need
additional age-state hypotheses or an enlarged state/observable.

The same complete cache identities with a different unique oldest identity
produce a different next-event query law. Identity marginals alone are
therefore insufficient to determine their own evolution. Full-state
relabeling symmetry, which includes ages, is a stronger condition and is
not present in this example. Uniform initial samples do not imply that
stronger symmetry.

This neither refutes the established full-capacity working convergence
theorem nor rules out a suitable age-aware, multi-event, or coupling
argument. It is not a counterexample to sparse-capacity convergence and
makes no claim about the journal paper's different protocol.

## Exact corroboration

`verification/mandatory-removal/verify_age_blind_uniformity_transient.py`
enumerates all request/reply subsets at the first event for `n=3..8` and
every allowed shuffle length, using the exact adopted merge checker. It
checks the resulting identity rows and rational one-sample probabilities,
then verifies the all-`b` TV formula by exact subset enumeration. The
symbolic argument above establishes the unrestricted parameter statement;
the finite enumeration only corroborates it.
