# Resume this research

Status recorded on **20 October 2026**. This is a working mathematical draft; authorship, publication plans, and external review are not established here.

All described work is saved. This handoff does not imply an active background run or scheduled research continuation.

## Start here

1. Read [MODEL.md](MODEL.md) for the exact protocol and sampling rule.
2. Read [ROADMAP.md](ROADMAP.md) for result boundaries and priorities.
3. Use [paper/main.tex](../paper/main.tex) as the single mathematical source, including all proofs and bibliography.
4. Find results by stable TeX labels, because numbering and source lines may change.

The latest research priority is a **useful local sampling rate for a fixed small cache with arbitrarily large membership**, starting with $c=\ell=2$ and one returned identifier. Further nearly full cache results have lower practical priority.

## Completed draft scope

For the adopted mandatory-removal, received-protection, minimum-age protocol with independent uniform initiators:

- Lengths one and two have full convergence and conditional sampling proofs for every allowed network size and common cache capacity.
- Length three has a full proof for $c\ge n-2$. Smaller capacities at length three and the general higher-length theorem remain open.
- Every fixed shuffle length has finite-age recurrence and finitely many possible stationary regimes. This alone does not settle sampling in the open cases.

“Proved” here refers to the current draft arguments and stated certificates, rather than external publication or peer review.

## Quantitative progress

For $c=\ell=2$, arbitrary $n$:
$$
T_n=16n^2,\qquad \Gamma_n=(4n)^{-T_n}.
$$
A controlled witness gives full-state error at most $(1-\Gamma_n)^{\lfloor t/T_n\rfloor}$, hence a pessimistic $\exp(O(n^2\log n))\log(1/\varepsilon)$ bound. This is not polynomial mixing.

Ordinary executions additionally satisfy:

- Expected first cut crossing at most $7n$ global events, with a tail halving every $14n$ events.
- Temporal connectivity within $O(n^2+n\log(1/\varepsilon))$ events with high probability.
- Fresh self emission by all peers within $O(n\log(n/\varepsilon))$ events with high probability.

The readiness proof counts full caches $\{r^A,s^B\}$ with $A\ge B$. For readiness count $R>0$, crossing probability is at least $R/(2n)$; readiness falls by at most one, with probability at most $2R/n$. The potential
$$
\Psi(R)=n\bigl(2+5(4/5)^R\bigr),
$$
set to zero after crossing, has conditional drift at most $-1$. This proves the $7n$ bound directly.

These communication guarantees do not establish a sampling rate.

## Where contraction work stopped

**prop:c2localcouplingtarget** reduces local uniformity to contraction between query laws from $x$ and $\sigma_{ab}x$, fixing observer $i$. Include the unavailable output $\bot$. The difference equals the output-probability difference for target labels $a,b$.

A proved symmetry-set coupling also reduces the task to hitting $F_\sigma=\{z:\sigma z=z\}$. No polynomial hitting bound is available.

**A polynomial local-contraction theorem for arbitrary $n$ remains open.**

A completed special case is now available for **three peers, arbitrary finite initial ages**:

- After burn-in, each cache has at most one positive-age entry.
- Zero/positive flags form an exact 487-state Markov projection.
- Integer arithmetic certifies eight-event antisymmetric contraction $34447/69984<1/2$ and four-event availability at least $5/9$.
- A sufficient sampling horizon is
  $$
  \left\lceil\frac{\log(9/\varepsilon)}{\log(3/2)}\right\rceil
  +8\left\lceil\log_2(3/\varepsilon)\right\rceil.
  $$
  At $\varepsilon=10^{-6}$, this is 216 global events.

Find **prop:c2threepositivity** and **prop:c2threeordinarysample**. The separate 75-state exact benchmark covers recurrent starts only and must not replace the all-initial-age certificate.

Four peers can produce two positive entries in one cache, so positivity flags are insufficient. Capped ages plus all global age ranks also fail as an exact query projection (**prop:c2caprankobstruction**). This rules out that particular projection, not every possible abstraction.

## Reproduce the latest checks

Run from the repository root with Python 3 and assertions enabled:

~~~sh
python3 verification/mandatory-removal/verify_thesis_c2_quantitative.py
python3 verification/mandatory-removal/verify_c2_ready_drift.py
python3 verification/mandatory-removal/verify_c2_refresh_counterexample.py
python3 verification/mandatory-removal/verify_c2_three_peer_antisymmetric.py
python3 verification/mandatory-removal/verify_c2_age_projection_obstruction.py
~~~

These scripts use the standard library and sibling helpers.

The readiness checker covers 14,260 endpoint cases supporting the symbolic structural proof. The three-peer certificate instead exhausts an analytically justified exact projection, using integer powers. Do not silently truncate unrestricted ages.

The refreshing checker verifies a three-peer star example:

- All initial descriptors are replaced by young ones, yet the conditional output is $3/7,4/7$.
- Conditioning on every peer actually initiating a successful exchange still gives output $3/5,2/5$, availability $5/8$, and conditioning-event probability $2/3$.
- OLD-copy count can have positive expected drift.

Therefore refreshing and communication alone cannot close the sampling proof.

## Next session

Pursue a coupling or richer query-sufficient projection controlling **label bias**, with the three-peer integer certificate as a concrete model. Use readiness as a tool, rather than claiming the missing sampling bridge is complete.

For the separate general-convergence task, prioritize length three with capacity three or four and arbitrary $n$. Conditional callbacks still need universal accessibility or a zero-count improvement argument.

Lean formalization is deferred at the user's request. Do not begin it until the proof work is ready and the user returns to that task.

