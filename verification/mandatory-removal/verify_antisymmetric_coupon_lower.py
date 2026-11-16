#!/usr/bin/env python3
"""Exact finite checks of the arbitrary-age antisymmetric coupon lower bound.

An in-star with center a and age A>T retains a high-age a descriptor exactly
when some initially occupied leaf has not initiated. The transposed start
has no high-age a descriptor at time T. This provides a full-state TV lower
bound, NOT a lower bound of order n log n for the local query law.
"""
from collections import defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_finite_horizon_age_compression import branches, key


def coupon_tail(n, time):
    cover = sum((-1)**k * comb(n - 1, k) * Fraction(n - k, n)**time
                for k in range(n))
    return 1 - cover


def distribution(start, time, capacity, length):
    law = {start: Fraction(1)}
    for _ in range(time):
        following = defaultdict(Fraction)
        for state, mass in law.items():
            for _, successor, weight in branches(state, capacity, length):
                following[successor] += mass * weight
        law = dict(following)
    assert sum(law.values()) == 1
    return law


def high_target(state, age):
    return any(peer == 0 and value >= age for row in state for peer, value in row)


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    cases = 0
    for n in range(3, 6):
        for time in range(5):
            age = time + 1
            original = key([{}] + [{0: age} for _ in range(n - 1)])
            swapped = key([{1: age}, {}] + [{1: age} for _ in range(n - 2)])
            for capacity in range(1, n):
                for length in range(1, capacity + 1):
                    first = distribution(original, time, capacity, length)
                    second = distribution(swapped, time, capacity, length)
                    witness_mass = sum(mass for state, mass in first.items() if high_target(state, age))
                    assert witness_mass == coupon_tail(n, time)
                    assert not any(high_target(state, age) for state in second)
                    distance = sum(abs(first.get(state, 0) - second.get(state, 0))
                                   for state in first.keys() | second.keys()) / 2
                    assert distance >= witness_mass
                    if time < n - 1:
                        assert distance == 1
                    missing_mean = (n - 1) * Fraction(n - 1, n)**time
                    assert witness_mass >= missing_mean / (1 + missing_mean)
                    cases += 1
    print(f'PASS {cases} exact star/transposed-law pairs: high-age witness equals coupon tail.')
    print('Scope: full-state antisymmetric coefficient lower bound, not local-query mixing lower bound.')


if __name__ == '__main__':
    main()
