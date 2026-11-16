# Migration verification — 20 October 2026

The research was checked from a standalone copy with Python 3.9.6, without importing the simulator project.

| Check | Result |
| --- | --- |
| Focused current-model suite | **5/5 passed** |
| Full curated current-model suite | **26/26 passed**, including the complete quadratic-path run and exact three-peer certificate |
| Repository-relative Markdown links and documented labels | Passed |
| Maintained Python syntax and machine-path check | Passed |
| Generated manuscript/archive indexes | Up to date |
| Preserved source artifacts | All **146** saved SHA-256 checksums matched |
| Manuscript | Byte-identical to the original source; built-in compilation succeeded in staging and at the final destination |

The full curated suite took about 189 seconds in this environment. Elapsed times are diagnostic, not performance guarantees.

Reproduction:

```sh
python3 -B tools/run_checks.py
python3 -B tools/run_checks.py --full
python3 -B tools/check_repository.py
```

The [full output](../verification/records/migration-2026-10-20.log) and [machine-readable summary](../verification/records/migration-2026-10-20.json) are saved. The original mixed-model JSON is preserved separately under `verification/records/retention-original.json`.

The eight historical variant/helper files remain available, but their standalone legacy checks were not included in the curated run. Archived explorations were preserved, not all executed or certified. Successful finite checks do not establish arbitrary-size theorems unless accompanied by the analytic argument or exact finite projection specified in the manuscript.

At the final destination, all 146 preserved artifact hashes matched, the focused suite passed again (5/5), repository integrity checks passed, and built-in compilation of `paper/main.tex` succeeded.

## Research continuation — 16 November 2026

The three-peer time-zero projection and subsequent generic tools were checked in a cloud checkout. This is a research working proof, not external peer review or formal verification.

- Full curated suite: **28/28 passed** (235.28 seconds).
- Latest focused suite, including the independently derived three-peer transition kernel, IID-refresh counterexample, and finite-horizon compression checker: **7/7 passed**.
- Generated index check and repository integrity checks passed: 104 declarations, 52 headings, 125 labels, 39 maintained Python files.
- `git diff --check` passed.
- Independent adversarial reviews found no gap in the time-zero projection, the no-op-thinning availability argument, or the finite-horizon gap/provenance argument. This is internal review only; the arbitrary-network polynomial sampling rate and unrestricted shuffle-length convergence theorem remain open. Existing arbitrary-network convergence for shuffle lengths one and two is unchanged; length three is currently covered only under the documented dense-cache assumptions.
- PDF compilation was attempted. A local format build allowed TeX to parse the complete manuscript, but final PDF production remained blocked by the environment's missing configured font map (`cmsy6` embedding failure). No successful PDF build is claimed for this checkout.

The arbitrary-network availability bound is a symbolic consequence of the existing contact theorem. The finite-horizon compression checks corroborate a symbolic all-size proof; they are not a finite certificate for generic mixing. The three-peer 56-event result, by contrast, explicitly includes an exhaustive finite integer certificate.

## Contraction-route and conditional-callback continuation — 16 November 2026

- Latest full curated suite: **31/31 passed** (235.92 seconds).
- Latest focused suite: **10/10 passed**, including the new 95 exact coupon-law pairs, 434 target-drift cases, frozen-pair invariant checks, and 6,600 conditional callback starts.
- Two explicit callback regressions pass. Independent review caught and corrected a case distinction: a second macro inserting no internal head can still require a third macro. The proof now uses the single-head argument for that case; no immediate-termination claim remains.
- Repository and generated-index checks passed: 108 declarations, 52 headings, 129 labels, 42 maintained Python files. `git diff --check` passed.
- The latest manuscript completed two `pdflatex -draftmode` passes using a local format. The second pass had no undefined or multiply defined references or LaTeX errors. This validates source processing, not final PDF rendering; configured font embedding remains unavailable and no PDF build is claimed.

The full-state TV compression and antisymmetric block criterion are symbolic reductions, not achieved polynomial contraction estimates. The coupon bound constrains full-state blocks, not local-query mixing. The new age-band callback is explicitly conditional on shared secondary descriptors and does not establish their reachability. The owner-frozen note proves obstructions to specific potentials/interventions, not slow mixing under the adopted scheduler.

## Capacity-three continuation — 16 November 2026

- Full maintained suite: **37/37 passed** (251.10 seconds in this cloud run).
- Repository checks: 408 local links, 136 labels, 48 maintained Python files.
- Manuscript index: 115 declarations, 53 headings.
- `git diff --check`: passed.
- Two TeX draft-mode passes: passed with no undefined or multiply-defined references and no LaTeX errors. Final PDF embedding remains unavailable because this environment lacks the configured font mapping; no new PDF is claimed.
- Separate mathematical end-to-end and actual-final-text audits: see [the scoped record](research/C3-AUDIT.md). Finite checks do not replace the symbolic proof.

The theorem is full `c=ell=3`, arbitrary `n>=4`, with qualitative uniform geometric constants. Sparse larger capacities and polynomial mixing are not claimed.
