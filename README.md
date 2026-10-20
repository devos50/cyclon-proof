# CYCLON convergence research

Research working proofs, partial results, counterexamples, and exact finite verification for an explicitly specified CYCLON peer sampler. This is a standalone repository, separated from the simulator project on 20 October 2026.

**The fully general convergence and useful mixing-time questions remain open.** “Proved” in the research notes means a written working argument under its stated assumptions, not an independently peer-reviewed or Lean-certified theorem. Finite checks and simulation are identified separately.

## Start here

| Need | Read |
| --- | --- |
| Resume the research quickly | [Current handoff](docs/RESUME.md) |
| What is proved, conditional, or open? | [Results registry](docs/RESULTS.md) |
| Exact protocol, scheduler, and sampling rule | [Model and assumptions](docs/MODEL.md) |
| Which arguments depend on which? | [Proof dependencies](docs/DEPENDENCIES.md) |
| What should we work on next? | [Prioritized roadmap](docs/ROADMAP.md) |
| Run or interpret the computational checks | [Verification guide](docs/VERIFICATION.md) |
| Find a particular theorem or label | [Generated manuscript index](docs/MANUSCRIPT-INDEX.md) |
| Read the full mathematical arguments | [LaTeX manuscript](paper/main.tex) |
| Unfinished or unintegrated arguments | [Partial results](docs/PARTIAL-RESULTS.md) |
| Recover older ideas and experiments | [Archive guide](archive/README.md), [catalog](docs/ARCHIVE-INDEX.md) |
| External references | [Primary sources](docs/SOURCES.md) |
| Check what was migrated | [Migration notes](docs/MIGRATION.md) |

## Repository layout

```text
paper/                    Mathematical manuscript (main.tex)
docs/                     Current model, result status, dependencies, roadmap, handoff
verification/             Maintained verification scripts and historical records
  mandatory-removal/      Related kernels/helpers kept together for sibling imports
tools/                    Portable check runner and generated source index
archive/                  Earlier notes, proof fragments, explorations, and PDF snapshots
```

The manuscript remains intact to preserve the existing proofs, cross-references, and editor preview. Markdown is the navigation and research-status layer. There is no need to reread the entire manuscript to resume work. Archived notes are historical material; the current model and results registry govern their interpretation.

## Run checks

Python 3.9 or later is sufficient for the standard-library checks. No simulator, package installation, or network connection is needed.

```sh
python3 -B tools/run_checks.py --list
python3 -B tools/run_checks.py
python3 tools/build_index.py --check
python3 -B tools/check_repository.py
```

Read the verification guide before a larger suite: some historical scripts exercise different replacement or scheduling rules, and some exhaustive runs are expensive. Optional numerical diagnostics in one script use NumPy; the exact certificates do not require it.

After editing the manuscript:

```sh
python3 tools/build_index.py
```

Open `paper/main.tex` in the Codex LaTeX editor for compilation and PDF preview. If a local TeX installation is available, `make pdf` writes generated output under `build/`. The PDF files under `archive/pdf/` are older snapshots and do not represent the latest manuscript.

## Git

This directory has its own Git history. A remote is deliberately not chosen; it can later be added for the desired hosting service. Generated TeX files, Python caches, and local verification logs are ignored. The preserved manuscript, scripts, Markdown records, archived research, and historical PDF snapshots belong in version control.

No repository-wide license or authorship attribution has been invented. Those can be selected before publication.
