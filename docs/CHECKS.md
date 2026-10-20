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
