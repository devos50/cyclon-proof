#!/usr/bin/env python3
"""Exact finite checks of the conditional b-sample coupon lower bound."""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_finite_horizon_age_compression import branches, key


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled.')
    cases = transitions = 0
    for n in range(2, 6):
        observer = n - 1
        for c in range(1, n):
            for length in range(1, c + 1):
                for b in range(1, c + 1):
                    target = tuple(range(b))
                    caches = [{}] + [{0: 0} for _ in range(n - 1)]
                    caches[observer] = {j: 0 for j in target}
                    initial = key(caches)
                    law = {(initial, False): Fraction(1)}
                    horizon = 3 if n <= 4 else 2
                    for t in range(horizon + 1):
                        query = defaultdict(Fraction)
                        available = untouched = Fraction(0)
                        for (state, seen), mass in law.items():
                            row = dict(state[observer])
                            if not seen:
                                assert state[observer] == initial[observer]
                                assert all(observer not in dict(r) for r in state)
                                untouched += mass
                            if len(row) >= b:
                                available += mass
                                for sample in combinations(sorted(row), b):
                                    query[sample] += mass / comb(len(row), b)
                        alpha = Fraction(n - 1, n)**t
                        assert untouched == alpha
                        assert available >= alpha > 0
                        assert query[target] / available >= alpha
                        M = comb(n - 1, b)
                        uniform = Fraction(1, M)
                        distance = sum(abs(query.get(s, 0) / available - uniform)
                                       for s in combinations(range(n - 1), b)) / 2
                        assert distance >= max(0, alpha - uniform)
                        if M == 1:
                            assert distance == 0
                        cases += 1
                        if t == horizon:
                            break
                        following = defaultdict(Fraction)
                        for (state, seen), mass in law.items():
                            for choice, successor, weight in branches(state, c, length):
                                following[successor, seen or choice[0] == observer] += mass * weight
                                transitions += 1
                        law = following
                        assert sum(law.values()) == 1
    print(f'PASS {cases} exact conditional-query laws and {transitions} kernel branches.')


if __name__ == '__main__':
    main()
