# Migration record — 20 October 2026

The research was moved into the standalone `cyclon-proof` repository at the user's request. No mathematical claim was strengthened as part of this organizational change.

## Preserved material

- The complete former `docs/peer-sampling-convergence/main.tex`, byte for byte, is now `paper/main.tex`.
- All Python sources from the former research directory are preserved under `verification/`, with related mandatory-removal helpers kept together. Usage examples were adjusted to the new relative paths; algorithm logic was not changed.
- The old `verification.json` report is retained as `verification/records/retention-original.json`. It is a historical report for early model variants, not the latest adopted-model test summary.
- CYCLON-specific temporary Markdown notes, TeX fragments, Python explorations, and JSON evidence were recovered into `archive/`.
- Existing project PDF exports and older temporary-build PDFs/logs are retained as historical snapshots. They predate the current manuscript.
- Markdown guides, a result registry, a roadmap, a handoff, and source indexing were added for future research.

The [migration manifest](MIGRATION-MANIFEST.json) records the origin group, original filename, saved relative path, and SHA-256 checksums for every preserved source artifact. The saved hash is compared again after copying to the destination. Temporary originals and archived raw notes are not treated as current mathematical authority.

Unrelated simulator research, operating-system metadata, Python bytecode caches, TeX auxiliary caches, and rendered preview PNGs were excluded. No Conflux repository history, dependencies, configuration, or remote was copied.

## Verification during migration

See [CHECKS.md](CHECKS.md) for actual reruns in the standalone copy. Earlier counts in the manuscript remain historical unless specifically listed as rerun. Reorganizing the repository is not an independent mathematical proof audit.

The original research directory and the two CYCLON PDF exports in the old project are removed only after destination checksum verification, successful standalone checks, and compilation of the relocated manuscript. Unrelated project files are left untouched.
