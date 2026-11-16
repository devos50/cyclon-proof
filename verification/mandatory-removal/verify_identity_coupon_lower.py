#!/usr/bin/env python3
"""Exact finite corroboration of the zero-age identity coupon lower bound.

This tests the adopted kernel, not a replacement process; no stationarity
or all-parameter proof is inferred from finite enumeration.
"""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_finite_horizon_age_compression import branches, key


def check_state(state, seen):
    untouched = [p for p in range(1, len(state)) if not seen & (1 << p)]
    for p in untouched:
        assert state[p] == ((0, 0),)
        assert all(p not in dict(row) for row in state)
    holders = sum(0 in dict(row) for row in state)
    assert holders >= len(untouched)
    return len(untouched)


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    cases = transitions = 0
    for n in range(2, 6):
        for c in range(1, n):
            for length in range(1, c + 1):
                start = key([{}] + [{0: 0} for _ in range(n - 1)])
                law = {(start, 0): Fraction(1)}
                for t in range(4):
                    assert sum(law.values()) == 1
                    mean = sum(mass * check_state(state, seen)
                               for (state, seen), mass in law.items())
                    second = sum(mass * check_state(state, seen)**2
                                 for (state, seen), mass in law.items())
                    mu = (n - 1) * Fraction(n - 1, n)**t
                    joint = Fraction(n - 2, n)**t
                    assert mean == mu
                    assert second == mu + (n - 1)*(n - 2)*joint
                    assert second - mean**2 <= mu
                    cases += 1
                    if t == 3:
                        break
                    following = defaultdict(Fraction)
                    for (state, seen), mass in law.items():
                        for choice, successor, probability in branches(state, c, length):
                            updated = seen | (1 << choice[0])
                            check_state(successor, updated)
                            following[successor, updated] += mass * probability
                            transitions += 1
                    law = following
    print(f'PASS {cases} exact horizon laws and {transitions} kernel branches; '
          'untouched rows, absent identifiers, occupancy domination, coupon moments.')


if __name__ == '__main__':
    main()
