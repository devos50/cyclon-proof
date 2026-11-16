#!/usr/bin/env python3
"""Exact obstruction to using target-copy count as an extinction potential.

One target copy is uniquely oldest, and the target owner's cache is empty.
Freezing that owner's clock does not change the next transition. Nonetheless
expected copy-count drift is (n-3)/(2n)>0 for every n>=4. This does not refute
polynomial extinction or a multistep/state-dependent potential.
"""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_finite_horizon_age_compression import branches, key


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    cases = 0
    for n in range(3, 41):
        for target_age in (1, 2, 10**6):
            state = key([{}, {0: target_age, 2: 0}] + [{1: 0} for _ in range(n - 2)])
            distribution = defaultdict(Fraction)
            by_initiator = defaultdict(Fraction)
            assert sum(0 in dict(row) for row in state) == 1
            for choice, successor, weight in branches(state, 2, 2):
                change = sum(0 in dict(row) for row in successor) - 1
                distribution[change] += weight
                by_initiator[choice[0]] += weight * change
            assert distribution == {-1: Fraction(1, n), 0: Fraction(n - 1, 2 * n), 1: Fraction(n - 1, 2 * n)}
            assert by_initiator[0] == 0
            assert by_initiator[1] == -Fraction(1, n)
            assert by_initiator[2] == Fraction(1, n)
            assert all(by_initiator[p] == Fraction(1, 2 * n) for p in range(3, n))
            drift = sum(change * mass for change, mass in distribution.items())
            assert drift == Fraction(n - 3, 2 * n)
            cases += 1
    paired_cases = 0
    for hubs in range(1, 11):
        for leaves in range(16):
            for target_age in (1, 10**6):
                n = 1 + 2 * hubs + leaves
                caches = [{} for _ in range(n)]
                for h in range(1, hubs + 1):
                    special = hubs + h
                    caches[h] = {0: target_age, special: 0}
                    caches[special] = {h: 0}
                for leaf in range(1 + 2 * hubs, n):
                    caches[leaf] = {1 + (leaf - 1 - 2 * hubs) % hubs: 0}
                distribution = defaultdict(Fraction)
                for _, successor, weight in branches(key(caches), 2, 2):
                    assert all(age == target_age for row in successor for peer, age in row if peer == 0)
                    change = sum(0 in dict(row) for row in successor) - hubs
                    distribution[change] += weight
                assert distribution == {-1: Fraction(hubs, n),
                                        0: Fraction(2 + leaves, 2 * n),
                                        1: Fraction(2 * hubs + leaves, 2 * n)}
                assert sum(change * mass for change, mass in distribution.items()) == Fraction(leaves, 2 * n)
                paired_cases += 1
    # Freeze a=0 and b=1. Outside rows contain neither target; hence outside
    # exchanges never acquire either, and both asymmetric target rows persist.
    initial = key([{1: 0, 2: 0}, {0: 0, 3: 0}, {3: 0}, {2: 0}])
    frontier = {initial}
    pair_branches = 0
    for _ in range(4):
        following = set()
        for state in frontier:
            for choice, successor, _ in branches(state, 2, 2):
                if choice[0] in (0, 1):
                    successor = state
                assert successor[:2] == initial[:2]
                assert all(peer not in (0, 1) for row in successor[2:] for peer, _ in row)
                following.add(successor)
                pair_branches += 1
        frontier = following
    print(f'PASS {paired_cases} multi-hub cases: E[Delta N_a]=L/(2n).')
    print(f'PASS {pair_branches} frozen-pair branches; symbolic invariant gives nonaccessibility for all times.')
    print(f'PASS {cases} exact cases: E[Delta N_a]=(n-3)/(2n), positive for every n>=4.')
    print('Scope: one-step potential obstruction, not an extinction-time lower bound.')


if __name__ == '__main__':
    main()
