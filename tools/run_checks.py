#!/usr/bin/env python3
"""Run the curated CYCLON checks using only the Python standard library.

Default: five focused checks for the adopted c=ell=2 model.
--full: every curated current-model checker, at its default coverage.
Legacy model variants and archived exploratory searches are never implicit.
"""
import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
from time import monotonic
from typing import Optional, Tuple


@dataclass(frozen=True)
class Check:
    name: str
    filename: str
    purpose: str
    full_args: Tuple[str, ...] = ()
    quick_args: Optional[Tuple[str, ...]] = None


CHECKS = (
    Check('c2_quantitative', 'verify_thesis_c2_quantitative.py',
          'Quadratic controlled paths and availability gadgets',
          quick_args=('--max-n', '10', '--seeds', '3', '--availability-n', '5')),
    Check('c2_ready', 'verify_c2_ready_drift.py',
          'Exact ready-copy cases for ordinary cut-contact drift', quick_args=()),
    Check('c2_three_peer', 'verify_c2_three_peer_antisymmetric.py',
          'Exact 487-state arbitrary-age three-peer sampling certificate', quick_args=()),
    Check('c2_refresh_obstructions', 'verify_c2_refresh_counterexample.py',
          'Exact obstructions to naive refresh/lineage arguments', quick_args=()),
    Check('c2_age_projection_obstruction', 'verify_c2_age_projection_obstruction.py',
          'Exact four-peer obstruction to age-cap/rank projection', quick_args=()),
    Check('c2_recurrent_mixing', 'verify_c2_recurrent_mixing.py',
          'Exact three-peer recurrent-start benchmark; optional NumPy unused'),
    Check('capacity_one', 'verify_capacity_one.py',
          'Mandatory-removal capacity-one tree identities'),
    Check('anchor', 'verify_thesis_anchor.py',
          'Protected MIN anchor simulation and component merging'),
    Check('c2_saturation', 'verify_thesis_c2_saturation.py',
          'Exact two-entry saturation and four-exchange infection'),
    Check('general_two', 'verify_thesis_general_two.py',
          'Arbitrary-capacity length-two outward gain'),
    Check('two_reset', 'verify_thesis_two_reset.py',
          'Protected MIN length-two age-gap reset'),
    Check('general_local', 'verify_thesis_general_local.py',
          'Exhaustive local colored all-length reset cases'),
    Check('general_reset', 'verify_thesis_general_reset.py',
          'Numerical-age all-length reset controller'),
    Check('first_contact', 'verify_thesis_first_contact.py',
          'Frozen-boundary contact and minimum-copy reduction'),
    Check('first_contact_fast', 'verify_thesis_first_contact_fast.py',
          'Polynomial holder-only contact plus zeroification', full_args=('--zeroify',)),
    Check('half_dense', 'verify_thesis_half_dense.py',
          'Earlier half-dense length-two outward-gain subcase'),
    Check('dense', 'verify_thesis_dense.py',
          'Earlier dense length-two no-eviction and root subcase'),
    Check('holder_routing', 'verify_thesis_holder_routing.py',
          'High-anchor final routing stage for longer shuffles'),
    Check('owner_cycle', 'verify_thesis_owner_cycle.py',
          'Owner-only service obstruction and cooperative repair'),
    Check('cooperative_owner', 'verify_thesis_cooperative_owner.py',
          'Conditional shared-anchor owner service at length three'),
    Check('cooperative_general', 'verify_thesis_cooperative_general.py',
          'Conditional shared-zero-anchor owner service at every length'),
    Check('cooperative_vector', 'verify_thesis_cooperative_vector.py',
          'Conditional common positive-age-vector full-shuffle callback'),
    Check('proper_owner', 'verify_thesis_proper_owner.py',
          'Conditional proper-shuffle callback with large zero caches'),
    Check('underfull_bootstrap', 'verify_thesis_underfull_bootstrap.py',
          'Conditional proper-shuffle underfull-zero bootstrap'),
    Check('dense_three_owner', 'verify_thesis_dense_three_owner.py',
          'Dense length-three callback and near-complete-zero subcase'),
    Check('dense_three_boundary', 'verify_thesis_dense_three_boundary.py',
          'Five-peer length-three component-boundary gadget'),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument('--full', action='store_true',
                           help='run all 26 curated current-model checks at full default coverage')
    selection.add_argument('--check', action='append', choices=[c.name for c in CHECKS],
                           help='run this named check at full coverage; may be repeated')
    parser.add_argument('--list', action='store_true', help='list all checks without executing them')
    parser.add_argument('--timeout', type=float, default=0,
                        help='optional timeout in seconds per check; zero means no timeout')
    parser.add_argument('--verification-dir', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'verification',
                        help='override the directory containing mandatory-removal/ for migration checks')
    args = parser.parse_args()
    if args.timeout < 0:
        parser.error('--timeout must be nonnegative')
    if args.list:
        for check in CHECKS:
            group = 'quick/full' if check.quick_args is not None else 'full'
            print(f'{check.name:30} [{group:10}] {check.purpose}')
        print('Legacy protocol variants and exploratory archives are excluded from both suites.')
        return 0
    if not __debug__:
        parser.error('assertions must be enabled; do not run this runner with Python -O')
    if args.check:
        wanted = set(args.check)
        selected = [c for c in CHECKS if c.name in wanted]
        quick = False
    elif args.full:
        selected, quick = list(CHECKS), False
    else:
        selected = [c for c in CHECKS if c.quick_args is not None]
        quick = True
    script_dir = args.verification_dir.resolve() / 'mandatory-removal'
    missing = [str(script_dir / c.filename) for c in selected
               if not (script_dir / c.filename).is_file()]
    if missing:
        parser.error('missing verification files:\n' + '\n'.join(missing))
    child_env = os.environ.copy()
    child_env.pop('PYTHONOPTIMIZE', None)
    child_env['PYTHONDONTWRITEBYTECODE'] = '1'
    failed = []
    began = monotonic()
    for check in selected:
        extra = check.quick_args if quick else check.full_args
        command = [sys.executable, '-B', str(script_dir / check.filename), *extra]
        print(f'\nRUN {check.name}: {check.purpose}', flush=True)
        started = monotonic()
        try:
            completed = subprocess.run(
                command, cwd=args.verification_dir.resolve().parent,
                env=child_env, timeout=args.timeout or None, check=False)
            if completed.returncode:
                failed.append(check.name)
                print(f'FAIL {check.name}: exit {completed.returncode}', flush=True)
            else:
                print(f'PASS {check.name} ({monotonic() - started:.2f}s)', flush=True)
        except subprocess.TimeoutExpired:
            failed.append(check.name)
            print(f'FAIL {check.name}: timeout after {args.timeout:g}s', flush=True)
    print(f'\n{len(selected) - len(failed)}/{len(selected)} checks passed '
          f'in {monotonic() - began:.2f}s.', flush=True)
    if failed:
        print('Failed checks: ' + ', '.join(failed), flush=True)
    return int(bool(failed))


if __name__ == '__main__':
    raise SystemExit(main())
