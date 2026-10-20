# Historical research archive

This archive preserves intermediate work recovered during the repository migration. It is not a second current results registry. Browse the [file catalog](../docs/ARCHIVE-INDEX.md), [script inventory](../docs/ARCHIVED-SCRIPTS.md), and [partial-result guide](../docs/PARTIAL-RESULTS.md).

- `notes/`: early proof sketches, partial results, audits, diagnostics, and abandoned approaches.
- `experiments/`: exploratory programs and saved search output. Some use earlier algorithm conventions, expensive searches, top-level execution, or original temporary paths.
- `fragments/`: intermediate TeX proof snippets. Many were subsequently integrated into `paper/main.tex`; earlier numerical bounds may have been superseded.
- `pdf/`: old manuscript snapshots. The current mathematical source is `paper/main.tex`.
- `build-logs/`: historical compilation logs for those snapshots.

Raw archived files are preserved verbatim for provenance. Their claims may be conditional, superseded, incomplete, or false under the adopted model. In particular, early unprotected-victim negative examples and duplicate-discard models do not refute convergence of the protected/MIN target.

Use the [current results registry](../docs/RESULTS.md), [model](../docs/MODEL.md), and [verification guide](../docs/VERIFICATION.md) before reusing an archived argument. The maintained checks live in `verification/`; archived experiments are not run by the check runner.

Historical `/tmp` paths and references to the former simulator project remain in raw archive files. They document the original exploration rather than runtime dependencies of the maintained repository.

The [migration manifest](../docs/MIGRATION-MANIFEST.json) maps every original archive filename to its saved path and checksum. No new research result was inferred from filenames during archiving.
