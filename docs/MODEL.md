# Model and observation rule

This describes the **adopted proof target**, denoted $\widehat P_\ell$ in [the paper](../paper/main.tex), Section **sec:target**. The paper retains other conventions in separate sections; their hypotheses must be read separately.

This is working research. Publication status, authorship, and external peer review are not established by this repository.

## State and assumptions

- Fixed labelled membership $V=\{1,\ldots,n\}$, $n\ge2$.
- Common cache capacity $c$ and fixed shuffle length $\ell$, with $1\le\ell\le c\le n-1$.
- Cache $C_v$ contains at most $c$ descriptors $u^a$: $u\ne v$, and $a$ is a finite nonnegative integer.
- No duplicate identities within a cache. Empty and underfull caches are allowed.
- Initially, $v\to u$ means $u\in C_v$. The underlying undirected graph is connected. Strong connectivity and full caches are not required.
- Initial ages have no required common upper bound.
- Static honest peers, reliable atomic exchanges, no churn, crashes, message loss, or external identity introductions.

## Randomness and time

Each global activation chooses one initiator independently and uniformly from all $n$ peers, including those with empty caches.

Independent rate-one Poisson clocks have this embedded event chain. One unit of continuous time has $n$ events on average. A “round” of $n$ activations does not guarantee that every peer initiated.

The original fixed periodic scheduler is a separate model. These independent-activation results do not automatically cover it.

Oldest ties, extra subsets, reply subsets, and eligible victim subsets are uniform. Conditional on the state and preceding choices in the exchange, choices are independent, including victim choices at its two endpoints. Subsequent events use fresh randomness.

## One activation

Shuffle length includes the initiator's fresh self descriptor; it does not count only additional peer identifiers.

For initiator $p$:

1. If $C_p$ is empty, do nothing.
2. Otherwise increment every resident age at $p$ by one.
3. Choose an oldest identity $q\in C_p$, uniformly among maximum-age ties.
4. Choose a uniform subset $S$ of $\min(\ell-1,|C_p|-1)$ other descriptors. Send
   $$
   B_p=\{p^0\}\cup S.
   $$
   Extras retain their incremented ages; the partner $q$ is absent from this packet.
5. Responder $q$ forms $B_q$, a uniform subset of $\min(\ell,|C_q|)$ descriptors from its pre-exchange cache. It does not increment its ages.
6. Remove $q$ from the initiator's resident cache unconditionally, then merge:
   $$
   C_p'=\operatorname{Merge}_p(C_p\setminus\{q\},B_q,\operatorname{ids}(S)),
   \qquad
   C_q'=\operatorname{Merge}_q(C_q,B_p,\operatorname{ids}(B_q)).
   $$
   The right-hand $C_p$ has its incremented ages. All other caches stay unchanged.

Both packets are formed before either merge. Sending a descriptor alone does not remove its resident copy. It is removed only if chosen as an eligible victim, apart from the contacted partner's mandatory deletion.

At $\ell=2$, a full initiator sends its own fresh address and one other entry. At $c=\ell=2$, request extras and full replies are forced; scheduler, oldest-tie, and eligible-victim randomness remain.

## Merge

For receiver $v$, let $A$ be its resident cache after any mandatory deletion, $R$ the incoming packet, and $E$ the sent identities eligible for replacement. Define
$$
D=\operatorname{ids}(R)\setminus\{v\},\qquad
N=D\setminus\operatorname{ids}(A),\qquad
d=\bigl(|N|-(c-|A|)\bigr)_+.
$$

Then:

1. Ignore any received self descriptor.
2. For every received identity already resident, keep the minimum resident/incoming age.
3. Protect every valid received identity from eviction, including duplicates.
4. Choose a uniform $d$-element victim subset of
   $$
   E\cap\operatorname{ids}(A)\setminus D.
   $$
5. Remove these victims and insert every new received identity with its received age.

Use vacancies first. Newly received entries and unsent residents cannot be victims. The paper proves that enough eligible victims always exist, including in underfull cases.

**Received-identity protection and minimum-age duplicate merging are fixed parts of the model.** They follow the adopted thesis convention, rather than being occasional proof interventions.

## Observation and target

At deterministic observation time $t$, observer $i$ requests $b\le c$ peers.

- Availability means $|C_i(t)|\ge b$.
- If available, select $b$ distinct cache identities uniformly without replacement and order them uniformly.
- Selection ignores ages.
- Output $\bot$ when unavailable.

The target is positive limiting availability and
$$
\left\|
\mathcal L_x\!\left(S_i^{(b)}(t)\mid |C_i(t)|\ge b\right)
-\operatorname{Unif}\bigl((V\setminus\{i\})_b\bigr)
\right\|_{\mathrm{TV}}\longrightarrow0
$$
for every allowed initial state.

Unique full-state stationarity, convergence including ages, and positive stationary availability are a sufficient route. Relabelling symmetry then gives the conditional uniform sample law.

Separate claims include independence across peers or times, uniformity of the full overlay, retry-until-available sampling, periodic scheduling, concurrent exchanges, heterogeneous capacities, failures, churn, and an efficient mixing time. None follows merely from the stated sampling target.

## Proof controllers versus ordinary executions

Accessibility arguments sometimes prescribe which peer initiates and which legal subset is chosen. These are positive-probability witness paths under the unchanged protocol. Their length alone is not an expected time bound for random executions.

Readiness, temporal-connectivity, and source-cover theorems instead concern ordinary uniform random executions. They are communication guarantees, not a general-network sampling rate.

See [ROADMAP.md](ROADMAP.md) for result boundaries and [RESUME.md](RESUME.md) for the research handoff.

