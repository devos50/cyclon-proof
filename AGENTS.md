# Working in this repository

This repository contains CYCLON proof research only. Work here; do not write CYCLON files back into the simulator/Conflux project.

Before continuing, read `docs/RESUME.md`, `docs/MODEL.md`, and the relevant entries in `docs/RESULTS.md`. Use `docs/DEPENDENCIES.md` and `docs/MANUSCRIPT-INDEX.md` to locate arguments by stable LaTeX labels. The current research priorities are in `docs/ROADMAP.md`.

## Mathematical status

- A written working proof, a conditional reduction, an exact finite certificate, a simulation, and a conjecture are different kinds of evidence. Record the distinction.
- Preserve the exact algorithm, scheduler, integer-age, connectivity, and observation assumptions with each result. Historical variants in the manuscript and archive do not automatically apply to the adopted protected/MIN algorithm.
- The general fixed-shuffle-length convergence theorem and arbitrary-network polynomial sampling bound are not complete. Never infer sampling uniformity or rapid mixing merely from temporal connectivity, fresh-source coverage, or lineage erasure.
- An explicit exponentially pessimistic bound exists for two-entry caches; it is not a polynomial expected mixing bound.
- Lean formalization is deferred at the user's request. Do not start it without new authorization.
- There is no background or scheduled research task. Continue proof work when requested.

## Where to put work

- `paper/main.tex`: full mathematical statements and proofs; keep it compiling. Do not split it mechanically or rewrite old model variants during unrelated work.
- `docs/`: curated current status, assumptions, dependencies, and research handoff. Keep these in sync when claims change.
- `verification/`: maintained exact checks. Preserve helper imports and state which protocol each script implements.
- `archive/`: historical notes and explorations, which may be incomplete, superseded, or wrong. Preserve raw provenance rather than silently promoting them to current results.
- `tools/`: navigation and verification orchestration, not new protocol assumptions.

Run the appropriate checks after a change. The focused suite is `python3 -B tools/run_checks.py`; list available suites first. Refresh the generated source index with `python3 tools/build_index.py`. Compile the saved manuscript using the built-in LaTeX compiler when available. Record exactly what was run, and distinguish newly rerun checks from historical reports.

All paths and commands in maintained tools should be repository-relative or derived from `__file__`. Do not introduce machine-specific paths or rely on files in `/tmp` or another project.

Before publication or stronger mathematical claims, seek an adversarial independent proof review. Do not promise a completion date or a generic polynomial rate that has not been established.
