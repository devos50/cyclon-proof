# Constant-threshold lower-kernel diagnostic

Research diagnostic, 16 November 2026. The underlying transition is the
adopted protected/MIN mandatory-removal kernel. Fix a threshold `m>=1`:
an initiator is allowed only if its **pre-event** maximum resident age is
at least m. Other initiations are omitted (equivalently, treated as no-ops).
This changes the available controlled paths. An ordinary common-atom
theorem does not by itself establish reachability under this restriction.

This is only a diagnostic for shared positive secondary ages. In an actual
reserved-anchor embedding, the secondary ages may vary between rows and
change during interactions. A constant-threshold result would not alone
justify that more general embedding.

## Exact singleton base, every threshold

**Local analytic lemma:** for residual capacity and length both one, every
allowed event decreases the total number of descriptors of age at least
m by at least one. Consequently after at most the initial number of such
descriptors (at most n) allowed events, every age is below m. At m=1 this
is precisely the all-zero-age condition. This holds for arbitrary finite
initial ages, any population, any permitted choices, and without a
connectivity assumption.

Proof: the active row has one descriptor, whose age is at least m. That
descriptor is mandatorily deleted and is not transmitted. The sole request
is the fresh active identity at age zero. If the responder is empty,
no old high descriptor is introduced. If it stores the active identity,
its age is reset to zero by MIN and its reply is self-filtered at the
active endpoint. Otherwise its sole old descriptor is copied to the
active endpoint and replaced at the responder by the fresh zero. This
merely transfers that descriptor's high/low status. Thus the initial
active high descriptor disappears without an uncompensated high arrival.

This count argument does not extend unchanged to larger caches: retained
active low descriptors may increment across the threshold.

## Exact bounded-state searches

The separate tool is
`verification/mandatory-removal/diagnose_threshold_censored_kernel.py`.
It enumerates every legal successor, using pre-event threshold one, and
builds a graph of states within a stated absolute age bound. Transitions
leaving that bound are recorded as boundary exits, **not clipped or
redirected**. Reverse reachability from all-zero states supplies finite
legal witnesses within the bound. A separate removal computation finds
the greatest nonzero subset closed under every actual successor; a
surviving connected state would be an exact obstruction, not a truncation
artifact. No such closed subset was found in the tested cases.

With age bound 2, all connected starts whose ages are in `{0,1}` had a
witness:

| n | c | length | Initial starts | Largest shortest witness |
|---|---|---|---|---|
| 2 | 1 | 1 | 8 | 1 |
| 3 | 1 | 1 | 100 | 2 |
| 3 | 2 | 1 | 704 | 3 |
| 3 | 2 | 2 | 704 | 3 |
| 4 | 1 | 1 | 1760 | 3 |

The same families were checked at age bound 4, with the same witness
results and no closed nonzero subset. The largest graphs examined had
46,656 states for three peers/capacity two and 65,536 states for four
peers/capacity one. These searches do not exhaust unrestricted ages or
larger populations. The tool also checks the singleton analytic count on
750 exact transitions with thresholds including `10^6`.

## Sampled larger cases and unresolved searches

A second mode uses 12 reproducible connected starts per parameter set,
initial ages in `{0,1,2,7}`, and ordinary forward BFS with **depth at most
8 and at most 10,000 discovered states per start**. Ages are not capped
or modified in this mode.

- `n=4,c=2,length=1`: all 12 witnessed, largest witness length 4;
  largest search 1,566 states, largest encountered age 8.
- `n=4,c=2,length=2`: all 12 witnessed, largest witness length 5;
  largest search 1,620 states, largest encountered age 8.
- `n=5,c=3,length=3`: 2 witnessed, largest witness length 5;
  the other 10 hit the 10,000-state limit. Largest encountered age 9.
  Those ten cases are **unresolved**, not counterexamples.

Run:

```sh
python3 -B verification/mandatory-removal/diagnose_threshold_censored_kernel.py
python3 -B verification/mandatory-removal/diagnose_threshold_censored_kernel.py --age-bound 4
python3 -B verification/mandatory-removal/diagnose_threshold_censored_kernel.py --sample-only
```

No higher-capacity censored convergence theorem follows from these checks,
and no obstruction to unrestricted CYCLON convergence is claimed.
